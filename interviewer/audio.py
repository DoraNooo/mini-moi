"""Enregistrement continu du micro (fichier WAV de toute la session) + détection des tours de parole.

Principe : un seul flux micro ouvert du début à la fin de la session. Chaque bloc audio
est écrit dans audio.wav ET, quand on « écoute », envoyé au détecteur de fin de réponse.
Les horodatages sont calculés en nombre d'échantillons écrits : ils sont donc exactement
alignés sur audio.wav.
"""
from __future__ import annotations

import queue
import threading
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import keys as K

BLOCK_S = 0.03  # 30 ms


def db(block: np.ndarray) -> float:
    rms = float(np.sqrt(np.mean(np.square(block, dtype=np.float64)))) if block.size else 0.0
    return 20 * np.log10(max(rms, 1e-9))


def to_mono(block: np.ndarray) -> np.ndarray:
    return block.mean(axis=1) if block.ndim == 2 else block


def resample_to_16k(audio: np.ndarray, sr: int) -> np.ndarray:
    audio = audio.astype(np.float32)
    if sr == 16000:
        return audio
    if sr % 16000 == 0:
        f = sr // 16000
        n = len(audio) // f * f
        return audio[:n].reshape(-1, f).mean(axis=1)
    n_out = int(len(audio) * 16000 / sr)
    return np.interp(np.linspace(0, len(audio) - 1, n_out), np.arange(len(audio)), audio).astype(np.float32)


def find_device(name_or_index, kind: str):
    """kind = 'input' | 'output'. Renvoie un index sounddevice ou None (= défaut)."""
    if name_or_index is None or name_or_index == "":
        return None
    if isinstance(name_or_index, int):
        return name_or_index
    import sounddevice as sd

    key = "max_input_channels" if kind == "input" else "max_output_channels"
    matches = [i for i, d in enumerate(sd.query_devices())
               if d[key] > 0 and str(name_or_index).lower() in d["name"].lower()]
    if not matches:
        raise RuntimeError(f"Aucun périphérique {kind} contenant « {name_or_index} ». "
                           "Lancez « python -m interviewer devices ».")
    # Préférer l'API WASAPI sous Windows (meilleure qualité) si présente
    apis = sd.query_hostapis()
    for i in matches:
        if "WASAPI" in apis[sd.query_devices(i)["hostapi"]]["name"]:
            return i
    return matches[0]


@dataclass
class Turn:
    audio: np.ndarray      # mono float32, fréquence du micro
    t_start: float         # secondes depuis le début de audio.wav
    t_end: float
    action: str            # keys.FIN / PASSER / PAUSE / QUITTER
    had_speech: bool


class Recorder:
    def __init__(self, wav_path: Path, cfg: dict):
        a = cfg["audio"]
        self.sr = int(a["sample_rate"])
        self.channels = int(a["channels"])
        self.subtype = a["subtype"]
        self.device = find_device(a["input_device"], "input")
        self.wav_path = wav_path
        self.frames = 0
        self._q: queue.Queue = queue.Queue()
        self._listen_q: queue.Queue = queue.Queue()
        self.listening = False
        self._stop = threading.Event()

    # -- cycle de vie -------------------------------------------------------
    def start(self):
        import sounddevice as sd
        import soundfile as sf

        self._wav = sf.SoundFile(str(self.wav_path), "w", samplerate=self.sr,
                                 channels=self.channels, subtype=self.subtype)
        self._writer = threading.Thread(target=self._write_loop, daemon=True)
        self._writer.start()
        self._stream = sd.InputStream(samplerate=self.sr, channels=self.channels, dtype="float32",
                                      device=self.device, blocksize=int(self.sr * BLOCK_S),
                                      callback=self._callback)
        self._stream.start()
        self.t0 = time.monotonic()

    def stop(self):
        self._stream.stop()
        self._stream.close()
        self._stop.set()
        self._writer.join(timeout=5)
        self._wav.close()

    def _callback(self, indata, frames, time_info, status):
        self._q.put(indata.copy())

    def _write_loop(self):
        while not (self._stop.is_set() and self._q.empty()):
            try:
                block = self._q.get(timeout=0.1)
            except queue.Empty:
                continue
            self._wav.write(block)
            self.frames += len(block)
            if self.listening:
                self._listen_q.put((self.frames, block))

    def now(self) -> float:
        """Position actuelle dans audio.wav, en secondes."""
        return self.frames / self.sr

    # -- calibration & écoute -----------------------------------------------
    def _drain(self):
        while not self._listen_q.empty():
            self._listen_q.get_nowait()

    def measure(self, seconds: float) -> list[float]:
        self._drain()
        self.listening = True
        levels, end = [], time.monotonic() + seconds
        while time.monotonic() < end:
            try:
                _, block = self._listen_q.get(timeout=0.2)
                levels.append(db(to_mono(block)))
            except queue.Empty:
                pass
        self.listening = False
        return levels

    def calibrate(self, seconds: float, margin_db: float) -> tuple[float, float]:
        levels = self.measure(seconds)
        floor = float(np.median(levels)) if levels else -60.0
        threshold = float(np.clip(floor + margin_db, -50.0, -30.0))
        return floor, threshold

    def listen_turn(self, threshold_db: float, silence_s: float, min_speech_s: float,
                    keys: K.Keys) -> Turn:
        """Écoute jusqu'à la fin d'une réponse (silence prolongé après de la parole, ou touche)."""
        self._drain()
        keys.flush()
        self.listening = True
        blocks, speech_t, first_frame, last_frame = [], 0.0, None, None
        silence_after, action = 0.0, K.FIN
        try:
            while True:
                k = keys.poll()
                if k:
                    action = k
                    break
                try:
                    frame_end, block = self._listen_q.get(timeout=0.1)
                except queue.Empty:
                    continue
                mono = to_mono(block)
                dur = len(mono) / self.sr
                if first_frame is None:
                    first_frame = frame_end - len(mono)
                last_frame = frame_end
                blocks.append(mono)
                if db(mono) > threshold_db:
                    speech_t += dur
                    silence_after = 0.0
                elif speech_t >= min_speech_s:
                    silence_after += dur
                    if silence_after >= silence_s:
                        break
        finally:
            self.listening = False
        audio = np.concatenate(blocks) if blocks else np.zeros(0, dtype=np.float32)
        t_start = (first_frame or self.frames) / self.sr
        t_end = (last_frame or self.frames) / self.sr
        return Turn(audio, t_start, t_end, action, speech_t >= min_speech_s)


def play(audio: np.ndarray, sr: int, output_device=None):
    import sounddevice as sd

    sd.play(audio, sr, device=output_device)
    sd.wait()
