"""Transcription en direct avec faster-whisper (GPU si possible)."""
from __future__ import annotations

import os
import re
import site
import sys
from pathlib import Path

import numpy as np

# Phrases que Whisper « invente » sur les silences (issues des sous-titres de ses données d'entraînement)
HALLUCINATIONS = re.compile(
    r"(sous-titr\w*[^.!?]*|amara\.org[^.!?]*|merci d'avoir regardé[^.!?]*|"
    r"abonnez-vous[^.!?]*|ST'? ?\d+)[.!?]?", re.I)


def strip_hallucinations(text: str) -> str:
    return re.sub(r"\s+", " ", HALLUCINATIONS.sub("", text)).strip()


def _add_nvidia_dll_dirs():
    """Sous Windows, rend visibles les DLL CUDA installées par pip (nvidia-cublas-cu12, nvidia-cudnn-cu12)."""
    if os.name != "nt":
        return
    bases = list(site.getsitepackages()) + [site.getusersitepackages(), str(Path(sys.prefix) / "Lib" / "site-packages")]
    for base in bases:
        nv = Path(base) / "nvidia"
        if nv.is_dir():
            for b in nv.glob("*/bin"):
                os.add_dll_directory(str(b))
                os.environ["PATH"] = str(b) + os.pathsep + os.environ.get("PATH", "")


class Transcriber:
    def __init__(self, cfg: dict):
        _add_nvidia_dll_dirs()
        from faster_whisper import WhisperModel

        c = cfg["stt"]
        self.language = c["language"]
        attempts = [("cuda", "float16"), ("cpu", "int8")] if c["device"] == "auto" else \
            [(c["device"], "float16" if c["device"] == "cuda" else "int8")]
        last_err = None
        for device, compute in attempts:
            try:
                self.model = WhisperModel(c["model"], device=device, compute_type=compute)
                self.device = device
                if device == "cuda":  # force le chargement des DLL tout de suite
                    self.model.transcribe(np.zeros(16000, dtype=np.float32), language=self.language)
                return
            except Exception as e:  # noqa: BLE001
                last_err = e
                print(f"  (transcription : {device} indisponible → {e})")
        raise RuntimeError(f"Impossible de charger Whisper : {last_err}")

    def transcribe(self, audio16k: np.ndarray) -> str:
        if audio16k.size < 1600:
            return ""
        segments, _ = self.model.transcribe(audio16k, language=self.language, beam_size=5,
                                            condition_on_previous_text=False, vad_filter=True)
        text = " ".join(s.text.strip() for s in segments if s.no_speech_prob < 0.6)
        return strip_hallucinations(text)
