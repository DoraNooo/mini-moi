"""Tests sans matériel : détection de fin de réponse, nettoyage LLM, déroulé de session."""
import threading
import time

import numpy as np
import pytest

from interviewer import keys as K
from interviewer.audio import Recorder, resample_to_16k
from interviewer.config import load_config
from interviewer.llm import FakeLLM, clean
from interviewer.session import Heard, Session

SR = 48000
BLOCK = int(SR * 0.03)


class NoKeys:
    def __init__(self, at=None):
        self.at, self.n = at, 0

    def poll(self):
        self.n += 1
        return self.at[1] if self.at and self.n >= self.at[0] else None

    def flush(self):
        pass


def _recorder(tmp_path):
    cfg = load_config()
    cfg["audio"]["input_device"] = None
    return Recorder(tmp_path / "a.wav", cfg)


def _feed(rec, pattern):
    """pattern : liste de (amplitude, durée_s). Simule le thread d'écriture."""
    def run():
        while not rec.listening:
            time.sleep(0.001)
        frames = 0
        for amp, dur in pattern:
            for _ in range(int(dur / 0.03)):
                frames += BLOCK
                block = (amp * np.sin(np.arange(BLOCK) / 5)).astype(np.float32).reshape(-1, 1)
                rec._listen_q.put((frames, block))
    threading.Thread(target=run, daemon=True).start()


def test_fin_de_reponse_apres_silence(tmp_path):
    rec = _recorder(tmp_path)
    _feed(rec, [(0.0005, 1.0), (0.2, 2.0), (0.0005, 0.3), (0.2, 1.0), (0.0005, 5.0)])
    turn = rec.listen_turn(-40, silence_s=2.0, min_speech_s=0.5, keys=NoKeys())
    assert turn.had_speech and turn.action == K.FIN
    dur = len(turn.audio) / SR
    assert 6.0 <= dur <= 6.5          # 1 + 2 + 0.3 + 1 + ~2 s de silence final, pas les 5 s
    assert turn.t_start == 0.0


def test_une_courte_pause_ne_coupe_pas(tmp_path):
    rec = _recorder(tmp_path)
    _feed(rec, [(0.2, 1.0), (0.0005, 1.5), (0.2, 1.0), (0.0005, 3.0)])
    turn = rec.listen_turn(-40, silence_s=2.0, min_speech_s=0.5, keys=NoKeys())
    assert len(turn.audio) / SR > 4.0


def test_touche_termine(tmp_path):
    rec = _recorder(tmp_path)
    _feed(rec, [(0.2, 10.0)])
    turn = rec.listen_turn(-40, 2.0, 0.5, keys=NoKeys(at=(5, K.PASSER)))
    assert turn.action == K.PASSER


def test_resample():
    assert len(resample_to_16k(np.zeros(48000), 48000)) == 16000
    assert len(resample_to_16k(np.zeros(44100), 44100)) == 16000


def test_clean():
    assert clean("<think>bla</think> **Léa :** Et ensuite ? [CONSIGNE : x]") == "Et ensuite ?"


class ScriptIO:
    mode = "texte"

    def __init__(self, answers):
        self.answers, self.said, self.t = list(answers), [], 0.0

    def now(self):
        return self.t

    def calibrate(self):
        pass

    def say(self, text, nom):
        self.said.append(text)
        return self.t, self.t

    def listen(self, silence_s=None):
        time.sleep(0.02)
        text, action = self.answers.pop(0) if self.answers else ("", K.QUITTER)
        self.t += 10
        return Heard(text, self.t - 10, self.t, action, bool(text))

    def wait_resume(self):
        pass


class SpyLLM(FakeLLM):
    def __init__(self):
        super().__init__()
        self.seen = []

    def chat(self, messages):
        self.seen.append(messages[-1]["content"])
        return super().chat(messages)


def test_session_passer_et_quitter(tmp_path):
    cfg = load_config()
    cfg["data_dir"] = tmp_path
    cfg["session"] = {"echauffement": 5, "theme": 0, "debat": 0, "lecture": 0}
    llm = SpyLLM()
    io = ScriptIO([("Ça va bien", K.FIN), ("", K.PASSER), ("on passe s'il te plaît", K.FIN), ("", K.QUITTER)])
    s = Session(cfg, io, llm, theme_key="metier")
    s.run()
    assert "CONSIGNE" in llm.seen[0]                       # ouverture
    assert llm.seen[1] == "Ça va bien"
    assert "ne veut pas continuer" in llm.seen[2]               # touche s
    assert "ne veut pas continuer" in llm.seen[3]               # « on passe » à l'oral
    assert s.stopped
    md = (s.dir / "transcript.md").read_text(encoding="utf-8")
    assert "Ça va bien" in md and "sujet passé" in md
    assert "Le métier au quotidien" in s.messages[0]["content"]


def test_theme_depuis_plan(tmp_path):
    cfg = load_config()
    cfg["data_dir"] = tmp_path
    (tmp_path / "plans").mkdir()
    (tmp_path / "plans" / "prochaine_session.md").write_text("theme: humour\n- piste", encoding="utf-8")
    s = Session(cfg, ScriptIO([]), FakeLLM(), None)
    assert s.theme_key == "humour"
    assert "- piste" in s.messages[0]["content"]


def test_accord_et_regles_dans_le_prompt(tmp_path):
    cfg = load_config()
    cfg["data_dir"] = tmp_path
    s = Session(cfg, ScriptIO([]), FakeLLM(), "metier")
    prompt = s.messages[0]["content"]
    assert "masculin" in prompt and "{accord}" not in prompt
    assert "jamais** pourquoi" in prompt
    cfg["interviewer"]["accord"] = "féminin"
    assert "au féminin" in Session(cfg, ScriptIO([]), FakeLLM(), "metier").messages[0]["content"]


def test_ordre_lecture_avant_theme_et_debat_contradictoire(tmp_path):
    cfg = load_config()
    cfg["data_dir"] = tmp_path
    cfg["session"] = {"echauffement": 0, "theme": 0, "debat": 5, "lecture": 0.0003}
    llm = SpyLLM()
    io = ScriptIO([("phrase lue", K.FIN), ("je ne suis pas d'accord", K.FIN), ("", K.QUITTER)])
    s = Session(cfg, io, llm, "metier")
    s.run()
    blocks = [t.get("block") for t in s.turns if t["role"] in ("moi", "lecture")]
    assert blocks[0] == "lecture"
    assert "avocate du diable" in llm.seen[0]
    assert "contradictrice" in llm.seen[1]
    assert s.progress["lecture_phrases"] == 1
