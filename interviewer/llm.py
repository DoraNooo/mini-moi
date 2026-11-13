"""Backends LLM interchangeables (ADR-0004) : Ollama local par défaut, faux backend pour les tests."""
from __future__ import annotations

import re

import requests


class LLM:
    def chat(self, messages: list[dict]) -> str:
        raise NotImplementedError


class OllamaLLM(LLM):
    def __init__(self, cfg: dict):
        c = cfg["llm"]
        self.url = c["url"].rstrip("/")
        self.model = c["model"]
        self.temperature = c["temperature"]

    def check(self) -> None:
        try:
            tags = requests.get(f"{self.url}/api/tags", timeout=5).json()
        except requests.RequestException as e:
            raise RuntimeError(f"Ollama ne répond pas sur {self.url} — est-il lancé ? ({e})") from e
        names = [m["name"] for m in tags.get("models", [])]
        if not any(n == self.model or n.split(":")[0] == self.model for n in names):
            raise RuntimeError(f"Modèle « {self.model} » absent. Lancez : ollama pull {self.model}")

    def chat(self, messages: list[dict]) -> str:
        r = requests.post(f"{self.url}/api/chat", timeout=120, json={
            "model": self.model, "messages": messages, "stream": False, "keep_alive": "30m",
            "options": {"temperature": self.temperature, "num_ctx": 8192},
        })
        r.raise_for_status()
        text = r.json()["message"]["content"]
        return clean(text)


class FakeLLM(LLM):
    """Pour tester le déroulé sans modèle : renvoie des relances génériques."""

    def __init__(self, cfg: dict | None = None):
        self.n = 0

    def check(self) -> None:
        pass

    def chat(self, messages: list[dict]) -> str:
        self.n += 1
        return f"Question de test numéro {self.n} : peux-tu m'en dire plus ?"


def clean(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)       # modèles « raisonneurs »
    text = re.sub(r"\[CONSIGNE[^\]]*\]", "", text)                   # ne jamais lire une consigne
    text = re.sub(r"[*_#`]+", "", text)                               # pas de markdown à l'oral
    text = re.sub(r"^\s*(Léa|Intervieweuse|Agent)\s*:\s*", "", text.strip(), flags=re.I)
    return re.sub(r"\s+", " ", text).strip()


def make_llm(cfg: dict) -> LLM:
    backend = cfg["llm"]["backend"]
    if backend == "ollama":
        return OllamaLLM(cfg)
    if backend == "fake":
        return FakeLLM(cfg)
    raise ValueError(f"Backend LLM inconnu : {backend}")
