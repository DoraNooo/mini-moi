# ADR-0001 — Une seule collecte, trois usages

- **Statut :** accepté
- **Date :** 2026-11-13

## Contexte

Le projet a besoin de données voix, de données visage et de connaissances sur la
personne. Les collecter séparément serait long et fastidieux.

## Décision

Toutes les données proviennent des **sessions d'entretien filmées** menées par l'agent
interviewer (module 03). Chaque session est enregistrée avec audio séparé de haute
qualité, vidéo et métadonnées horodatées, puis découpée par le pipeline (phase 2)
en trois datasets : voix, visage, persona.

## Conséquences

- La qualité de captation (PROTOCOLE-CAPTURE.md) devient critique dès la phase 1.
- L'agent doit être conçu pour servir les trois usages (faire parler, varier les émotions,
  inclure des blocs lecture et écoute), pas seulement pour « poser des questions ».
- Les données brutes sont stockées une seule fois, chiffrées, hors git.
