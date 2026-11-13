"""Voix de l'intervieweuse : Piper (local, neuronal) avec repli sur les voix Windows (SAPI)."""
from __future__ import annotations

import io
import wave
from pathlib import Path

import numpy as np
import requests

PIPER_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main"


def _voice_url(name: str) -> str:
    # fr_FR-siwis-medium -> fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx
    lang_region, speaker, quality = name.split("-")
    return f"{PIPER_BASE}/{lang_region.split('_')[0]}/{lang_region}/{speaker}/{quality}/{name}.onnx"


def ensure_piper_voice(name: str, voices_dir: Path) -> Path:
    voices_dir.mkdir(parents=True, exist_ok=True)
    onnx = voices_dir / f"{name}.onnx"
    for path, url in ((onnx, _voice_url(name)), (Path(str(onnx) + ".json"), _voice_url(name) + ".json")):
        if not path.exists():
            print(f"  Téléchargement de la voix {path.name}…")
            r = requests.get(url, timeout=120)
            r.raise_for_status()
            path.write_bytes(r.content)
    return onnx


class TTS:
    def say(self, text: str) -> tuple[np.ndarray, int]:
        """Renvoie (audio float32 mono, fréquence)."""
        raise NotImplementedError


class PiperTTS(TTS):
    def __init__(self, cfg: dict):
        from piper import PiperVoice

        onnx = ensure_piper_voice(cfg["tts"]["piper_voice"], cfg["tts"]["voices_dir"])
        self.voice = PiperVoice.load(str(onnx))

    def say(self, text: str):
        try:  # API piper-tts >= 1.3
            chunks = list(self.voice.synthesize(text))
            sr = chunks[0].sample_rate
            audio = np.concatenate([c.audio_float_array for c in chunks]).astype(np.float32)
            return audio, sr
        except (AttributeError, TypeError, IndexError):
            buf = io.BytesIO()  # API piper-tts < 1.3
            with wave.open(buf, "wb") as w:
                self.voice.synthesize(text, w)
            buf.seek(0)
            with wave.open(buf, "rb") as w:
                sr = w.getframerate()
                pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
            return pcm.astype(np.float32) / 32768.0, sr


class SapiTTS(TTS):
    """Voix Windows (ex. Microsoft Hortense / Julie / Paul, pack de langue français requis)."""

    def __init__(self, cfg: dict):
        import pyttsx3

        self.engine = pyttsx3.init()
        for v in self.engine.getProperty("voices"):
            if "fr" in (str(v.languages) + v.id + v.name).lower():
                self.engine.setProperty("voice", v.id)
                break

    def say(self, text: str):
        import tempfile

        import soundfile as sf

        with tempfile.TemporaryDirectory() as d:
            p = str(Path(d) / "tts.wav")
            self.engine.save_to_file(text, p)
            self.engine.runAndWait()
            audio, sr = sf.read(p, dtype="float32")
        return (audio.mean(axis=1) if audio.ndim == 2 else audio), sr


class NoTTS(TTS):
    def say(self, text: str):
        return np.zeros(0, dtype=np.float32), 22050


def make_tts(cfg: dict) -> TTS:
    engine = cfg["tts"]["engine"]
    if engine == "none":
        return NoTTS()
    if engine == "piper":
        try:
            return PiperTTS(cfg)
        except Exception as e:  # noqa: BLE001
            print(f"  (Piper indisponible : {e} → repli sur les voix Windows)")
    return SapiTTS(cfg)
