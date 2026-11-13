# Module 02 — Visage

## Objectif réaliste

Teams compresse fortement la vidéo (souvent 720p, débit variable) : c'est une aide.
On vise un **buste face caméra**, cadrage webcam, éclairage de bureau — pas un rendu cinéma.

## Approches possibles

1. **Talking head 2D à partir d'une image/vidéo de référence** (LivePortrait, MuseTalk…)
   — rapide à mettre en place, temps réel possible, fidélité moyenne.
2. **Avatar personnalisé entraîné** (ex. avatars 3D Gaussian splatting, NeRF de tête)
   — demande des heures de vidéo multi-angles, rendu bien plus crédible, temps réel sur bon GPU.
3. **Service commercial** (HeyGen, Tavus…) — très rapide à tester, données envoyées chez un tiers.

Recommandation : POC avec 1 ou 3 pour calibrer, cible long terme 2.

## Ce que les sessions doivent capturer

- Parole naturelle face caméra (lip-sync, mouvements de tête, clignements).
- **Écoute active** : le clone passe la moitié d'une réunion à écouter
  (hochements, sourires, regard). Filmer aussi les moments où l'agent parle !
- Expressions variées : rire, réflexion, surprise, désaccord.
- Quelques sessions avec léger changement d'angle (± 20°) et d'éclairage.
- Avec et sans lunettes si vous en portez ; tenue habituelle de travail.

## Pièges connus

- Intérieur de la bouche et dents, langue.
- Bords du visage / cheveux sur fond variable → privilégier un fond fixe ou flou.
- Regard : un avatar qui fixe trop la caméra paraît étrange.
- Synchronisation audio/vidéo au runtime (dérive > 80 ms perceptible).
