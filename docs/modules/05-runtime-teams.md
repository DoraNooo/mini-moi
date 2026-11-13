# Module 05 — Runtime temps réel dans Teams

## Branchement

Teams ne sait rien du clone : il voit une **caméra virtuelle** et un **micro virtuel**.

- Vidéo : rendu de l'avatar → OBS → OBS Virtual Camera → sélectionnée dans Teams.
- Audio sortant : TTS → câble audio virtuel (VB-Cable sous Windows, BlackHole sous macOS) → micro Teams.
- Audio entrant : sortie haut-parleur Teams → câble virtuel → STT du clone.

## Budget de latence (mode B)

| Étape | Cible |
|---|---|
| Détection fin de parole (VAD) | 200-400 ms |
| STT final | 100-300 ms |
| LLM premier token | 300-600 ms |
| TTS premier chunk audio | 100-300 ms |
| Avatar premier frame | 50-150 ms |
| **Total** | **≈ 1-1,5 s** |

Astuces : streaming partout, « fillers » naturels (« hmm », « alors… ») pendant que le
LLM réfléchit — et ce sont justement vos tics enregistrés.

## Gestion de tours de parole

Le plus dur en réunion à plusieurs : savoir quand on s'adresse à vous, ne pas couper
la parole, réagir à son prénom. Démarrer par des 1-à-1.

## Bouton d'arrêt

Raccourci clavier « reprendre la main » : coupe l'avatar et repasse sur votre vraie
caméra/micro instantanément.
