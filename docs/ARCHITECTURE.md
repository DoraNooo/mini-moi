# Architecture

## Vue d'ensemble

```
COLLECTE (phase 1)                 PRÉPARATION (phase 2)              MODÈLES (phases 3-4)
──────────────────                 ─────────────────────              ────────────────────
Agent interviewer ─┐               ┌─► Audio : débruitage, VAD,  ───► Voix (TTS + conversion)
  (LLM + TTS)      │  session_N/   │   diarisation, découpage,
Caméra 1080p+ ─────┼─► video.mp4 ──┤   transcription Whisper
Micro dédié ───────┤   audio.wav   │
Log questions ─────┘   meta.json ──┼─► Vidéo : détection visage, ───► Visage (avatar animé)
                                   │   tri qualité, poses, expr.
                                   │
                                   └─► Texte : transcription     ───► Persona (RAG + profil)
                                       structurée, thèmes, faits

RUNTIME (phase 5)
─────────────────
Teams ──audio──► STT (Whisper streaming) ──► LLM + persona ──► TTS voix clonée ──┬──► Micro virtuel ──► Teams
                                                                                 └──► Avatar lip-sync ──► Caméra virtuelle ──► Teams
```

## Principe clé : une session = trois jeux de données

Chaque session d'entretien est enregistrée avec **audio séparé** (micro dédié, WAV 48 kHz
24 bits) et **vidéo** (≥ 1080p, ≥ 30 fps), synchronisés par un clap ou un timecode.
Le fichier `meta.json` contient les questions posées et leurs horodatages : il permet
de retrouver plus tard « la réponse à la question X » et sert de base à la persona.

## Choix technologiques (pistes, à valider par des POC)

| Brique | Open source (local / GPU loué) | Service commercial (plus rapide à tester) |
|---|---|---|
| Transcription | faster-whisper / WhisperX | — |
| Voix TTS | F5-TTS, XTTS-v2, GPT-SoVITS (fine-tune) | ElevenLabs (Professional Voice Clone) |
| Visage temps réel | LivePortrait, MuseTalk (lip-sync), avatars Gaussian splatting | HeyGen / Tavus (avatars interactifs) |
| LLM persona | Claude via API + RAG local | — |
| Sortie Teams | OBS Virtual Camera + câble audio virtuel (VB-Cable / BlackHole) | — |

Stratégie recommandée : **POC rapide avec les services commerciaux** pour savoir ce qui
est atteignable avec vos données, puis **migration vers l'open source** pour la maîtrise
des coûts et de la confidentialité (vos données biométriques ne quittent pas votre machine).
Les versions et licences exactes sont à revérifier au moment des POC (l'écosystème bouge
vite ; certaines licences, ex. XTTS-v2, interdisent l'usage commercial).

## Matériel (ADR-0002)

Ryzen 7 7800X3D · 32 Go DDR5 · **RTX 4080 (16 Go VRAM)**.

Stratégie retenue : **tout en local sauf le LLM** (API Claude, paiement à l'usage).
Raison : 16 Go de VRAM suffisent pour STT + TTS + avatar en simultané, pas pour
y ajouter un LLM assez bon pour imiter une personne.

Budget VRAM indicatif au runtime :

| Brique | VRAM |
|---|---|
| STT (faster-whisper large-v3-turbo) | ~2-3 Go |
| TTS voix clonée | ~3-6 Go |
| Avatar temps réel | ~4-8 Go |
| Teams + OBS + encodage | ~1 Go |
| **Total** | **~10-16 Go** → serré mais jouable, à mesurer |

Entraînement : fine-tune voix OK en local ; avatar personnalisé faisable en local mais
long (prévoir éventuellement quelques heures de GPU loué, ~1 €/h, ponctuellement).
- **Budget LLM** : l'abonnement Claude Pro couvre le pilotage du projet ici, mais
  l'agent interviewer et le runtime appellent l'API Claude, facturée à part
  (quelques euros par heure d'entretien — à chiffrer en phase 1).
