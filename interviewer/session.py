"""Déroulé d'une session d'entretien : échauffement → thème → débat → lecture → conclusion."""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import yaml

from . import keys as K
from .config import PACKAGE_DIR

SKIP_RE = re.compile(r"\b(on passe|on peut passer|question suivante|je préf[eè]re (ne )?pas|"
                     r"(je n'ai|j'ai) pas envie d'en parler|chang(e|eons|er) de sujet)\b", re.I)
PAUSE_RE = re.compile(r"\b(on (fait|peut faire) une pause|pause s'il te pla[iî]t)\b", re.I)

HELP = "  [Entrée] j'ai fini   [s] passer à autre chose   [p] pause   [q] arrêter la session"


def fmt_t(t: float) -> str:
    t = int(t)
    return f"{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}"


@dataclass
class Heard:
    text: str
    t_start: float
    t_end: float
    action: str
    had_speech: bool


# --------------------------------------------------------------------------- E/S
class VoiceIO:
    """Micro + transcription + voix de synthèse, avec enregistrement continu."""

    mode = "voix"

    def __init__(self, cfg, recorder, stt, tts, keys):
        from .audio import find_device

        self.cfg, self.rec, self.stt, self.tts, self.keys = cfg, recorder, stt, tts, keys
        self.out_dev = find_device(cfg["audio"]["output_device"], "output")
        self.threshold = -40.0

    def now(self) -> float:
        return self.rec.now()

    def calibrate(self):
        print("\nCalibration : restez silencieux 3 secondes…")
        floor, self.threshold = self.rec.calibrate(3.0, self.cfg["vad"]["margin_db"])
        print(f"  bruit de fond {floor:.0f} dBFS → seuil de parole {self.threshold:.0f} dBFS")
        if floor > -45:
            print("  ATTENTION : la pièce est bruyante (ventilateur ? fenêtre ?). La qualité de la voix en pâtira.")

    def say(self, text: str, nom: str) -> tuple[float, float]:
        from .audio import play

        print(f"\n{nom} : {text}")
        audio, sr = self.tts.say(text)
        t0 = self.now()
        if audio.size:
            play(audio, sr, self.out_dev)
        return t0, self.now()

    def listen(self, silence_s: float | None = None) -> Heard:
        from .audio import resample_to_16k

        v = self.cfg["vad"]
        print(HELP)
        turn = self.rec.listen_turn(self.threshold, silence_s or v["silence_s"], v["min_speech_s"], self.keys)
        text = ""
        if turn.had_speech:
            print("  (transcription…)", end="\r")
            text = self.stt.transcribe(resample_to_16k(turn.audio, self.rec.sr))
        print(f"Moi : {text or '(rien entendu)'}")
        return Heard(text, turn.t_start, turn.t_end, turn.action, turn.had_speech and bool(text))

    def wait_resume(self):
        print("\n=== PAUSE === appuyez sur une touche pour reprendre.")
        self.keys.wait_any()


class TextIO:
    """Mode texte pour tester le déroulé et les prompts sans micro ni GPU."""

    mode = "texte"

    def __init__(self):
        self.t0 = time.monotonic()

    def now(self) -> float:
        return time.monotonic() - self.t0

    def calibrate(self):
        pass

    def say(self, text: str, nom: str):
        t = self.now()
        print(f"\n{nom} : {text}")
        return t, self.now()

    def listen(self, silence_s=None) -> Heard:
        t0 = self.now()
        try:
            line = input("Moi (/s passer, /p pause, /q quitter) > ").strip()
        except EOFError:
            line = "/q"
        action = {"/s": K.PASSER, "/p": K.PAUSE, "/q": K.QUITTER}.get(line, K.FIN)
        text = "" if line.startswith("/") else line
        return Heard(text, t0, self.now(), action, bool(text))

    def wait_resume(self):
        input("=== PAUSE === Entrée pour reprendre ")


# --------------------------------------------------------------------------- Session
class Session:
    CONVERSATION_BLOCKS = ("echauffement", "theme", "debat")

    def __init__(self, cfg: dict, io, llm, theme_key: str | None = None, minutes: float | None = None):
        self.cfg, self.io, self.llm = cfg, io, llm
        self.nom = cfg["interviewer"]["nom"]
        self.data = Path(cfg["data_dir"])
        self.themes = yaml.safe_load((PACKAGE_DIR / "questions" / "themes.yaml").read_text(encoding="utf-8"))
        self.lecture = yaml.safe_load((PACKAGE_DIR / "questions" / "lecture.yaml").read_text(encoding="utf-8"))
        self.progress_path = self.data / "progress.json"
        self.progress = self._load_json(self.progress_path, {"sessions": [], "lecture_phrases": 0, "lecture_emotions": 0})
        self.theme_key = self._pick_theme(theme_key)
        self.durations = dict(cfg["session"])
        if minutes:  # mise à l'échelle de tous les blocs
            total = sum(self.durations.values())
            self.durations = {k: v * minutes / total for k, v in self.durations.items()}
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        sub = "sessions" if io.mode == "voix" else "sessions_test"
        self.dir = self.data / sub / stamp
        self.dir.mkdir(parents=True, exist_ok=True)
        self.id = stamp
        self.turns: list[dict] = []
        self.messages: list[dict] = [{"role": "system", "content": self._system_prompt()}]
        self.paused = 0.0
        self.stopped = False

    # -- préparation --------------------------------------------------------
    @staticmethod
    def _load_json(path: Path, default):
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return default

    def _covered(self) -> list[str]:
        return [s["theme"] for s in self.progress["sessions"]]

    def _plan_text(self) -> str:
        p = self.data / "plans" / "prochaine_session.md"
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def _pick_theme(self, forced: str | None) -> str:
        if forced:
            if forced not in self.themes:
                raise SystemExit(f"Thème inconnu « {forced} ». Choix : {', '.join(self.themes)}")
            return forced
        m = re.search(r"^\s*theme\s*:\s*(\w+)", self._plan_text(), re.M)
        if m and m.group(1) in self.themes:
            return m.group(1)
        covered = set(self._covered())
        return next((k for k in self.themes if k not in covered), "metier")

    def _system_prompt(self) -> str:
        profil_p = self.data / "persona" / "profil.md"
        profil = profil_p.read_text(encoding="utf-8")[:12000] if profil_p.exists() else \
            "Rien pour l'instant : c'est l'une des premières sessions."
        th = self.themes[self.theme_key]
        covered = sorted({self.themes[k]["titre"] for k in self._covered() if k in self.themes})
        adresse = "Tu tutoies la personne." if self.cfg["interviewer"]["tutoiement"] else "Tu vouvoies la personne."
        repl = {
            "{nom}": self.nom, "{adresse}": adresse, "{profil}": profil,
            "{plan}": self._plan_text() or "Pas de plan particulier : suis le thème.",
            "{theme}": th["titre"], "{pistes}": "\n".join(f"- {p}" for p in th["pistes"]),
            "{themes_couverts}": ", ".join(covered) or "Aucun.",
        }
        text = (PACKAGE_DIR / "prompts" / "system.md").read_text(encoding="utf-8")
        for k, v in repl.items():
            text = text.replace(k, v)
        return text

    # -- journalisation -----------------------------------------------------
    def _log(self, **turn):
        self.turns.append(turn)
        self._save()

    def _save(self):
        meta = {
            "id": self.id, "mode": self.io.mode, "theme": self.theme_key,
            "theme_titre": self.themes[self.theme_key]["titre"],
            "llm": self.cfg["llm"]["model"], "audio": "audio.wav" if self.io.mode == "voix" else None,
            "turns": self.turns,
        }
        (self.dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        lines = [f"# Session {self.id} — {meta['theme_titre']}\n"]
        for t in self.turns:
            who = {"agent": self.nom, "moi": "Moi"}.get(t["role"], t["role"])
            if t["role"] == "lecture":
                who = f"Lecture ({t.get('emotion') or 'neutre'})"
            if t["role"] == "evenement":
                lines.append(f"*[{fmt_t(t['t_start'])}] — {t['text']}*\n")
            else:
                lines.append(f"**[{fmt_t(t['t_start'])}] {who} :** {t['text']}\n")
        (self.dir / "transcript.md").write_text("\n".join(lines), encoding="utf-8")

    # -- dialogue -----------------------------------------------------------
    def _agent(self, user_content: str, block: str):
        self.messages.append({"role": "user", "content": user_content})
        keep = self.cfg["llm"]["max_history"]
        if len(self.messages) > keep + 1:
            self.messages = [self.messages[0]] + self.messages[-keep:]
        try:
            reply = self.llm.chat(self.messages)
        except Exception as e:  # noqa: BLE001
            print(f"  (erreur LLM : {e})")
            reply = "Pardon, j'ai perdu le fil une seconde. Tu peux continuer ce que tu disais ?"
        reply = reply or "Et ensuite ?"
        self.messages.append({"role": "assistant", "content": reply})
        t0, t1 = self.io.say(reply, self.nom)
        self._log(role="agent", text=reply, t_start=t0, t_end=t1, block=block)

    def _hear(self, block: str, **extra) -> Heard | None:
        """Écoute une réponse ; gère pause et arrêt. Renvoie None si la session est arrêtée."""
        while True:
            h = self.io.listen(extra.pop("silence_s", None))
            if h.text:
                self._log(role="moi", text=h.text, t_start=h.t_start, t_end=h.t_end, block=block, **extra)
            if h.action == K.QUITTER:
                self.stopped = True
                self._log(role="evenement", text="session arrêtée par l'utilisateur", t_start=self.io.now())
                return None
            if h.action == K.PAUSE or PAUSE_RE.search(h.text):
                t = time.monotonic()
                self._log(role="evenement", text="pause", t_start=self.io.now())
                self.io.wait_resume()
                self.paused += time.monotonic() - t
                if not h.text:
                    continue
            return h

    def _conversation_block(self, block: str, opening: str):
        minutes = self.durations[block]
        if minutes <= 0:
            return
        start, warned, paused_in_block = time.monotonic(), False, 0.0

        def elapsed():
            return (time.monotonic() - start - paused_in_block) / 60

        self._log(role="evenement", text=f"début du bloc {block}", t_start=self.io.now())
        self._agent(opening, block)
        while not self.stopped and elapsed() < minutes:
            p0 = self.paused
            h = self._hear(block)
            paused_in_block += self.paused - p0
            if h is None:
                return
            consignes = []
            if h.action == K.PASSER or SKIP_RE.search(h.text):
                consignes.append("La personne préfère ne pas continuer sur ce sujet. N'insiste pas : "
                                 "dis-le avec douceur et passe à un sujet complètement différent.")
                self._log(role="evenement", text="sujet passé", t_start=self.io.now())
            elif not h.had_speech:
                consignes.append("La personne n'a rien dit. Reformule plus simplement ou propose une autre piste.")
            if not warned and minutes - elapsed() < 1.2:
                warned = True
                consignes.append("Ce sujet se termine bientôt : pose une dernière question dessus.")
            if elapsed() >= minutes:
                return  # la transition est faite par le bloc suivant
            content = h.text or "(silence)"
            if consignes:
                content += "\n\n" + " ".join(f"[CONSIGNE : {c}]" for c in consignes)
            self._agent(content, block)

    def _lecture_block(self):
        minutes = self.durations["lecture"]
        if minutes <= 0 or self.stopped:
            return
        self._log(role="evenement", text="début du bloc lecture", t_start=self.io.now())
        intro = ("On termine par un petit exercice de lecture. Lis chaque phrase affichée à l'écran, "
                 "naturellement, comme si tu parlais. Quand une émotion est indiquée, joue-la.")
        t0, t1 = self.io.say(intro, self.nom)
        self._log(role="agent", text=intro, t_start=t0, t_end=t1, block="lecture")
        phrases, emotions = self.lecture["phrases"], self.lecture["emotions"]
        start, n, paused0 = time.monotonic(), 0, self.paused
        while not self.stopped and (time.monotonic() - start - (self.paused - paused0)) / 60 < minutes:
            if n % 4 == 3:
                item = emotions[self.progress["lecture_emotions"] % len(emotions)]
                self.progress["lecture_emotions"] += 1
                emotion, texte = item["emotion"], item["phrase"]
            else:
                emotion, texte = None, phrases[self.progress["lecture_phrases"] % len(phrases)]
                self.progress["lecture_phrases"] += 1
            n += 1
            print("\n" + "=" * 70)
            if emotion:
                print(f"  Émotion : {emotion.upper()}")
            print(f"  « {texte} »")
            print("=" * 70)
            h = self.io.listen(1.5)
            if h.action == K.QUITTER:
                self.stopped = True
                break
            if h.action == K.PAUSE:
                t = time.monotonic()
                self.io.wait_resume()
                self.paused += time.monotonic() - t
            if h.had_speech and h.action != K.PASSER:
                self._log(role="lecture", text=texte, entendu=h.text, emotion=emotion,
                          t_start=h.t_start, t_end=h.t_end, block="lecture")

    # -- point d'entrée -----------------------------------------------------
    def run(self):
        th = self.themes[self.theme_key]
        print(f"\nSession {self.id} — thème : {th['titre']}  ({sum(self.durations.values()):.0f} min)")
        print(f"Enregistrement dans : {self.dir}")
        self.io.calibrate()
        try:
            self._conversation_block("echauffement", "[CONSIGNE : Début de session. Salue la personne en une "
                                     "phrase et pose une question légère pour démarrer (sa journée, son humeur). "
                                     "N'aborde pas encore le thème principal.]")
            if not self.stopped:
                self._conversation_block("theme", f"[CONSIGNE : Passe maintenant en douceur au thème principal : "
                                         f"{th['titre']}. Pose une première question ouverte et concrète.]")
            if not self.stopped:
                self._conversation_block("debat", "[CONSIGNE : Bloc débat. Annonce en une phrase que tu vas jouer "
                                         "l'avocate du diable, puis prends le contre-pied d'une opinion qu'elle a "
                                         "exprimée aujourd'hui (ou une position provocatrice sur le thème) et "
                                         "demande-lui de te convaincre. Dans ce bloc, tu peux argumenter en deux "
                                         "phrases maximum.]")
            self._lecture_block()
            if not self.stopped:
                text = "[CONSIGNE : La session est terminée. Remercie la personne en une ou deux phrases chaleureuses, sans poser de question.]"
                self.messages.append({"role": "user", "content": text})
                try:
                    bye = self.llm.chat(self.messages)
                except Exception:  # noqa: BLE001
                    bye = "Merci beaucoup pour cette session, à la prochaine !"
                t0, t1 = self.io.say(bye, self.nom)
                self._log(role="agent", text=bye, t_start=t0, t_end=t1, block="conclusion")
        except KeyboardInterrupt:
            self._log(role="evenement", text="session interrompue (Ctrl+C)", t_start=self.io.now())
        finally:
            self._finish()

    def _finish(self):
        self._save()
        parole = sum(t["t_end"] - t["t_start"] for t in self.turns if t["role"] in ("moi", "lecture"))
        print(f"\nSession enregistrée : {self.dir}")
        print(f"Parole utile captée : {parole / 60:.1f} min")
        if self.io.mode != "voix":
            return
        self.progress["sessions"].append({"id": self.id, "theme": self.theme_key,
                                          "minutes_parole": round(parole / 60, 1),
                                          "complete": not self.stopped})
        self.progress_path.write_text(json.dumps(self.progress, ensure_ascii=False, indent=2), encoding="utf-8")
        total = sum(s["minutes_parole"] for s in self.progress["sessions"])
        print(f"Total collecté : {total:.0f} min / objectif 180 min ({len(self.progress['sessions'])} sessions)")
        print("\nÉtape suivante : analyse inter-sessions avec Claude Code en local "
              "(voir interviewer/prompts/analyse_session.md).")
