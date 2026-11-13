"""Lecture non bloquante du clavier (Windows : msvcrt ; ailleurs : ligne + Entrée)."""
from __future__ import annotations

import os
import sys

# Actions renvoyées
FIN = "fin"          # Entrée : j'ai fini ma réponse
PAUSE = "pause"      # p
PASSER = "passer"    # s : je préfère passer à autre chose
QUITTER = "quitter"  # q


def _map(ch: str) -> str | None:
    ch = ch.lower()
    if ch in ("\r", "\n", ""):
        return FIN
    return {"p": PAUSE, "s": PASSER, "q": QUITTER}.get(ch[0])


class Keys:
    def poll(self) -> str | None:
        if os.name == "nt":
            import msvcrt

            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch in ("\x00", "\xe0"):  # touche spéciale : on ignore
                    msvcrt.getwch()
                    return None
                return _map(ch)
            return None
        import select

        r, _, _ = select.select([sys.stdin], [], [], 0)
        if r:
            return _map(sys.stdin.readline().strip())
        return None

    def wait_any(self) -> None:
        if os.name == "nt":
            import msvcrt

            msvcrt.getwch()
        else:
            sys.stdin.readline()

    def flush(self) -> None:
        if os.name == "nt":
            import msvcrt

            while msvcrt.kbhit():
                msvcrt.getwch()
