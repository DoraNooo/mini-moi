"""Chargement de la configuration (config.yaml, sinon valeurs d'exemple)."""
from __future__ import annotations

import copy
from pathlib import Path

import yaml

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
EXAMPLE = PACKAGE_DIR / "config.example.yaml"


def _merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(path: str | None = None) -> dict:
    cfg = yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))
    candidate = Path(path) if path else REPO_ROOT / "config.yaml"
    if candidate.exists():
        cfg = _merge(cfg, yaml.safe_load(candidate.read_text(encoding="utf-8")) or {})
        cfg["_source"] = str(candidate)
    else:
        cfg["_source"] = f"{EXAMPLE} (pas de config.yaml trouvé)"
    data_dir = Path(cfg["data_dir"])
    cfg["data_dir"] = data_dir if data_dir.is_absolute() else REPO_ROOT / data_dir
    voices = Path(cfg["tts"]["voices_dir"])
    cfg["tts"]["voices_dir"] = voices if voices.is_absolute() else REPO_ROOT / voices
    return cfg
