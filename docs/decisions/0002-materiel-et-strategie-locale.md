# ADR-0002 — Matériel et stratégie « local sauf le cerveau »

- **Statut :** accepté
- **Date :** 2026-11-13

## Contexte

Machine disponible : Ryzen 7 7800X3D, 32 Go DDR5, RTX 4080 (16 Go VRAM).
Question : peut-on tout faire en local, ou faut-il des abonnements externes ?

## Décision

| Brique | Où | Pourquoi |
|---|---|---|
| Transcription (STT) | Local | Whisper local = niveau des meilleurs services |
| Voix (TTS cloné) | Local | Fine-tune open source sur 3 h+ de données = très bon niveau |
| Visage (avatar) | Local | Possible ; c'est la brique la plus risquée, à évaluer en phase 4 |
| Cerveau (LLM persona) | **API Claude** (à l'usage, pas d'abonnement) | Un LLM local tenant dans la VRAM restante est nettement moins bon pour imiter une personnalité |
| Services commerciaux voix/vidéo | Optionnel, 1 mois max | Seulement comme **étalon** pour savoir si le local est à la hauteur |

## Conséquences

- Les données biométriques (voix, visage) restent sur la machine.
- Coût récurrent limité à l'API Claude (ordre de grandeur : quelques euros par heure de
  réunion ou d'entretien, à mesurer en phase 1).
- Le budget VRAM est serré : chaque brique doit être mesurée au runtime.
- Si la phase 4 montre que le visage local est insuffisant, on rouvre cette décision.
