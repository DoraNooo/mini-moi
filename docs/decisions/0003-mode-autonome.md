# ADR-0003 — Mode cible : clone autonome

- **Statut :** accepté
- **Date :** 2026-11-13

## Décision

Le seul objectif est un clone qui participe **seul** à une visio : il écoute, décide quoi
répondre (LLM + persona), parle avec la voix clonée et s'affiche avec l'avatar.
Le mode « marionnette » (conversion en direct de la voix/du visage de l'utilisateur)
est abandonné.

Les interlocuteurs sont toujours informés qu'ils parlent au clone.

## Conséquences

- La persona (module 04) devient aussi importante que la voix et le visage.
- Pas de pipeline speech-to-speech (RVC etc.) : la voix est uniquement du TTS.
- Le visage doit gérer deux états : parler (lip-sync piloté par l'audio TTS) et écouter
  (hochements, regard, micro-expressions générés sans audio du clone).
- La latence de bout en bout et la gestion des tours de parole sont les risques
  techniques principaux de la phase 5.
