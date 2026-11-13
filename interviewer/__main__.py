"""Point d'entrée : python -m interviewer {devices,test,session,libre,transcrire}."""
from __future__ import annotations

import argparse
import sys
import time

from .config import load_config


def cmd_devices(cfg, args):
    import sounddevice as sd

    print(sd.query_devices())
    print("\nAPI audio :", ", ".join(h["name"] for h in sd.query_hostapis()))
    print("\nRenseignez une partie du nom dans config.yaml (audio.input_device / audio.output_device).")


def _step(title):
    print(f"\n--- {title} ".ljust(70, "-"))


def cmd_test(cfg, args):
    """Vérifie chaque brique, une par une, avec un diagnostic lisible."""
    import numpy as np
    import soundfile as sf

    from .audio import Recorder, db, find_device, play, resample_to_16k
    from .llm import make_llm

    ok = {}
    print(f"Configuration : {cfg['_source']}")
    cfg["data_dir"].mkdir(parents=True, exist_ok=True)
    wav = cfg["data_dir"] / "test_micro.wav"

    _step("1/4 Micro")
    rec_audio = None
    try:
        rec = Recorder(wav, cfg)
        print(f"Périphérique d'entrée : {rec.device if rec.device is not None else 'défaut Windows'}")
        rec.start()
        print("Silence 2 secondes…")
        floor = float(np.median(rec.measure(2.0)))
        print("Maintenant parlez normalement pendant 5 secondes (présentez-vous, par exemple)…")
        levels = rec.measure(5.0)
        rec.stop()
        rec_audio, sr = sf.read(str(wav), dtype="float32")
        peak = 20 * np.log10(max(float(np.max(np.abs(rec_audio))), 1e-9))
        speech = float(np.percentile(levels, 90)) if levels else -99
        print(f"Bruit de fond : {floor:.0f} dBFS   parole : {speech:.0f} dBFS   crête : {peak:.0f} dBFS")
        if peak > -1:
            print("  → SATURATION : baissez le gain du Yeti.")
        elif speech < -40:
            print("  → Voix trop faible : rapprochez-vous (15-20 cm, parlez dans le côté du Yeti) ou montez le gain.")
        if floor > -50:
            print("  → Bruit de fond élevé : coupez ventilateurs, fermez la fenêtre, mode cardioïde.")
        print(f"Enregistrement de test : {wav}")
        ok["micro"] = peak <= -1 and speech > -45
    except Exception as e:  # noqa: BLE001
        print(f"ÉCHEC micro : {e}")
        ok["micro"] = False

    _step("2/4 Transcription (Whisper)")
    try:
        from .stt import Transcriber

        t = time.time()
        stt = Transcriber(cfg)
        print(f"Modèle chargé sur {stt.device.upper()} en {time.time() - t:.1f} s")
        if rec_audio is not None:
            mono = rec_audio.mean(axis=1) if rec_audio.ndim == 2 else rec_audio
            t = time.time()
            text = stt.transcribe(resample_to_16k(mono, sr))
            print(f"Entendu ({time.time() - t:.1f} s) : « {text} »")
        if stt.device != "cuda":
            print("  → Le GPU n'est pas utilisé : voir la section « GPU » du guide d'installation.")
        ok["transcription"] = True
    except Exception as e:  # noqa: BLE001
        print(f"ÉCHEC transcription : {e}")
        ok["transcription"] = False

    _step("3/4 Modèle de langage (Ollama)")
    try:
        llm = make_llm(cfg)
        llm.check()
        t = time.time()
        r = llm.chat([{"role": "system", "content": "Tu es une intervieweuse. Réponds en une phrase."},
                      {"role": "user", "content": "Pose-moi une question sur mon enfance."}])
        print(f"Réponse ({time.time() - t:.1f} s, 1er appel plus lent) : {r}")
        ok["llm"] = True
    except Exception as e:  # noqa: BLE001
        print(f"ÉCHEC LLM : {e}")
        ok["llm"] = False

    _step("4/4 Voix de l'intervieweuse (dans le casque)")
    try:
        from .tts import make_tts

        tts = make_tts(cfg)
        audio, sr_tts = tts.say("Bonjour ! Si tu m'entends dans ton casque, tout fonctionne.")
        play(audio, sr_tts, find_device(cfg["audio"]["output_device"], "output"))
        print(f"Voix : {type(tts).__name__}, niveau {db(audio):.0f} dBFS")
        ok["voix"] = True
    except Exception as e:  # noqa: BLE001
        print(f"ÉCHEC voix : {e}")
        ok["voix"] = False

    _step("Bilan")
    for k, v in ok.items():
        print(f"  {'OK    ' if v else 'ÉCHEC '} {k}")
    if all(ok.values()):
        print("\nTout est prêt. Lancez : python -m interviewer session")
    return 0 if all(ok.values()) else 1


def cmd_session(cfg, args):
    from .llm import make_llm
    from .session import Session, TextIO

    llm = make_llm(cfg)
    try:
        llm.check()
    except RuntimeError as e:
        sys.exit(f"ERREUR : {e}")

    if args.texte:
        Session(cfg, TextIO(), llm, args.theme, args.minutes).run()
        return 0

    from .audio import Recorder
    from .keys import Keys
    from .session import VoiceIO
    from .stt import Transcriber
    from .tts import make_tts

    print("Chargement de la transcription et de la voix…")
    stt, tts = Transcriber(cfg), make_tts(cfg)
    # Le dossier de session doit exister avant de créer l'enregistreur : on crée la session d'abord.
    proxy = _LateIO()
    session = Session(cfg, proxy, llm, args.theme, args.minutes)
    rec = Recorder(session.dir / "audio.wav", cfg)
    proxy.target = VoiceIO(cfg, rec, stt, tts, Keys())
    input("\nCasque sur les oreilles ? Appuyez sur Entrée pour démarrer l'enregistrement… ")
    rec.start()
    try:
        session.run()
    finally:
        rec.stop()
        print(f"Audio : {session.dir / 'audio.wav'}")
    return 0


def cmd_libre(cfg, args):
    from .keys import Keys
    from .libre import record

    print("Enregistrement libre : seul VOTRE micro est enregistré (pas le son de Discord ni du jeu).")
    print("Rappels : casque obligatoire, et prévenez vos amis que vous enregistrez votre voix.")
    record(cfg, args.tag, args.max_heures, Keys())
    return 0


def cmd_transcrire(cfg, args):
    from pathlib import Path

    from .libre import pending, transcribe
    from .stt import Transcriber

    folders = [Path(args.dossier)] if args.dossier else pending(cfg)
    if not folders:
        print("Rien à transcrire.")
        return 0
    stt = Transcriber(cfg)
    for folder in folders:
        print(f"Transcription de {folder.name}…")
        transcribe(cfg, folder, stt)
    print("\nÉtape suivante : analyse en local (interviewer/prompts/analyse_session.md).")
    return 0


class _LateIO:
    """Délègue à l'E/S vocale, créée après le dossier de session."""

    mode = "voix"
    target = None

    def __getattr__(self, name):
        return getattr(self.target, name)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(prog="python -m interviewer", description="Agent interviewer mini-moi")
    ap.add_argument("--config", help="chemin d'un config.yaml (défaut : config.yaml à la racine)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("devices", help="lister micros et sorties audio")
    sub.add_parser("test", help="vérifier micro, transcription, LLM et voix")
    s = sub.add_parser("session", help="lancer une session d'entretien")
    s.add_argument("--theme", help="clé de thème (voir interviewer/questions/themes.yaml)")
    s.add_argument("--minutes", type=float, help="durée totale (les blocs sont mis à l'échelle)")
    s.add_argument("--texte", action="store_true", help="mode texte (sans micro), pour tester")
    lb = sub.add_parser("libre", help="enregistrer votre voix pendant une activité (ex. Discord)")
    lb.add_argument("--tag", default="discord", help="étiquette du registre (défaut : discord)")
    lb.add_argument("--max-heures", type=float, default=4, help="arrêt automatique (défaut : 4 h)")
    tr = sub.add_parser("transcrire", help="transcrire les enregistrements libres en attente")
    tr.add_argument("dossier", nargs="?", help="un dossier précis (défaut : tous ceux en attente)")
    args = ap.parse_args(argv)
    cfg = load_config(args.config)
    cmds = {"devices": cmd_devices, "test": cmd_test, "session": cmd_session,
            "libre": cmd_libre, "transcrire": cmd_transcrire}
    return cmds[args.cmd](cfg, args) or 0


if __name__ == "__main__":
    sys.exit(main())
