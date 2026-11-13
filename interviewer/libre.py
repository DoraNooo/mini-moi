"""Enregistrement libre (ex. parties Discord entre amis) : seulement VOTRE micro, transcription après coup.

Pendant le jeu, rien ne tourne sur le GPU : on enregistre le Yeti en FLAC (sans perte, les
silences ne prennent presque pas de place). La transcription se fait plus tard, quand le
PC est libre, avec « python -m interviewer transcrire ».
"""
from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path

from .audio import Recorder, db, to_mono
from .session import fmt_t


def _save(folder: Path, meta: dict):
    (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [f"# Enregistrement libre {meta['id']} — {meta['tag']}\n",
             "*Seule votre voix est enregistrée ; les répliques des autres ne figurent pas ici.*\n"]
    for t in meta["turns"]:
        lines.append(f"**[{fmt_t(t['t_start'])}]** {t['text']}\n")
    (folder / "transcript.md").write_text("\n".join(lines), encoding="utf-8")


def record(cfg: dict, tag: str, max_hours: float, keys) -> Path:
    data = Path(cfg["data_dir"])
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    folder = data / "libre" / f"{stamp}_{tag}"
    folder.mkdir(parents=True, exist_ok=True)
    meta = {"id": stamp, "mode": "libre", "tag": tag, "audio": "audio.flac", "transcrit": False, "turns": []}
    _save(folder, meta)

    rec = Recorder(folder / "audio.flac", cfg)
    rec.start()
    print("\nCalibration : 3 secondes de silence…")
    _, threshold = rec.calibrate(3.0, cfg["vad"]["margin_db"])
    print(f"Enregistrement en cours dans {folder}")
    print("Vous pouvez retourner jouer. Pour arrêter : revenez sur cette fenêtre et tapez q (ou Ctrl+C).")
    print(f"Arrêt automatique au bout de {max_hours:g} h.\n")

    speech, last_print = 0.0, time.monotonic()
    rec.listening = True
    try:
        while rec.now() < max_hours * 3600:
            if keys.poll() == "quitter":
                break
            while not rec._listen_q.empty():
                _, block = rec._listen_q.get_nowait()
                mono = to_mono(block)
                if db(mono) > threshold:
                    speech += len(mono) / rec.sr
            if time.monotonic() - last_print > 60:
                last_print = time.monotonic()
                print(f"  {fmt_t(rec.now())} enregistrées — environ {speech / 60:.1f} min de parole")
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        rec.listening = False
        rec.stop()
    meta["duree_s"] = round(rec.now(), 1)
    meta["parole_estimee_s"] = round(speech, 1)
    _save(folder, meta)
    print(f"\nTerminé : {fmt_t(rec.now())} enregistrées, environ {speech / 60:.1f} min de parole.")
    print("Quand le PC est libre, lancez : python -m interviewer transcrire")
    return folder


def pending(cfg: dict) -> list[Path]:
    root = Path(cfg["data_dir"]) / "libre"
    out = []
    for m in sorted(root.glob("*/meta.json")):
        if not json.loads(m.read_text(encoding="utf-8")).get("transcrit"):
            out.append(m.parent)
    return out


def transcribe(cfg: dict, folder: Path, stt, chunk_s: float = 300.0):
    """Transcrit le fichier par tranches (fichiers de plusieurs heures) et horodate chaque phrase."""
    import soundfile as sf

    from .audio import resample_to_16k
    from .stt import strip_hallucinations

    meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
    turns = []
    with sf.SoundFile(str(folder / meta["audio"])) as f:
        sr, total = f.samplerate, f.frames
        offset = 0
        while offset < total:
            block = f.read(int(chunk_s * sr), dtype="float32")
            mono = block.mean(axis=1) if block.ndim == 2 else block
            base = offset / sr
            print(f"  {fmt_t(base)} / {fmt_t(total / sr)}", end="\r")
            segments, _ = stt.model.transcribe(resample_to_16k(mono, sr), language=stt.language, beam_size=5,
                                               condition_on_previous_text=False, vad_filter=True)
            for s in segments:
                text = strip_hallucinations(s.text.strip())
                if text and s.no_speech_prob < 0.6:
                    turns.append({"role": "moi", "text": text, "t_start": round(base + s.start, 2),
                                  "t_end": round(base + s.end, 2), "block": "libre", "registre": meta["tag"]})
            offset += len(mono)
    meta["turns"], meta["transcrit"] = turns, True
    meta["parole_s"] = round(sum(t["t_end"] - t["t_start"] for t in turns), 1)
    _save(folder, meta)

    progress_path = Path(cfg["data_dir"]) / "progress.json"
    try:
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        progress = {"sessions": [], "lecture_phrases": 0, "lecture_emotions": 0}
    progress.setdefault("libre", []).append({"id": meta["id"], "tag": meta["tag"],
                                             "minutes_parole": round(meta["parole_s"] / 60, 1)})
    progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  {len(turns)} phrases, {meta['parole_s'] / 60:.1f} min de parole → {folder / 'transcript.md'}")
