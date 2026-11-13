# ADR-0005 — V1 = clone vocal, le visage en V2

- **Statut :** accepté
- **Date :** 2026-11-13

## Contexte

La webcam disponible (Logitech 720p) est insuffisante pour entraîner un avatar
crédible, et le visage est la brique la plus lourde et la plus risquée du projet.

## Décision

La première itération livre un **clone vocal** : voix clonée + persona, présent dans
Teams caméra coupée. Le visage devient la V2.

## Pourquoi c'est le bon ordre

- En réunion pro, beaucoup de participants ont la caméra coupée : un clone vocal est
  **utile tel quel**, en particulier pour présenter un document en partage d'écran.
- Les briques les plus importantes pour « être vous » (voix, tics, persona, gestion de
  la réunion) sont toutes dans la V1 ; la V2 ne fait que s'y brancher (l'avatar est
  piloté par l'audio produit par la V1).
- Moins de VRAM utilisée au runtime → plus de marge pour la qualité de la voix.
- Matériel suffisant dès aujourd'hui (Blue Yeti), aucun achat nécessaire.

## Conséquences

- Les sessions d'entretien V1 sont **audio d'abord**. Enregistrer en plus la webcam
  reste possible et gratuit (réserve de données pour la V2), mais n'est pas requis.
- La V2 prévoira des sessions vidéo dédiées, avec un meilleur matériel.
- Teams : photo de profil ou image fixe pendant les réunions du clone.
