# ADR-0004 — Pas de clé API Claude pour démarrer

- **Statut :** accepté
- **Date :** 2026-11-13

## Contexte

L'agent interviewer a besoin d'un LLM pour poser des questions et relancer.
L'utilisateur préfère ne pas ouvrir de compte API payant dès le départ.

## Décision

Répartition en deux temps :

| Moment | Qui | Coût |
|---|---|---|
| **Pendant** la session (relances en direct) | **LLM local** via Ollama sur la RTX 4080 (modèle ~12-14 B, bon en français) | 0 € |
| **Entre** les sessions (analyse des transcriptions, plan de la session suivante, mise à jour du profil persona) | **Claude Code**, dans le cadre de l'abonnement Pro | inclus |

Pendant un entretien, la carte graphique est libre (pas d'avatar ni de TTS cloné à
faire tourner) : un LLM local tient sans difficulté. Les relances en direct demandent
peu d'intelligence ; le travail exigeant (comprendre la personne, planifier les thèmes)
est fait entre les sessions par Claude Code.

Le code de l'interviewer garde un **backend LLM interchangeable** (Ollama par défaut,
API Claude possible plus tard sans réécriture).

## Conséquences

- Démarrage sans aucun coût supplémentaire.
- Il faut installer Ollama sur le PC Windows.
- La question de l'API se reposera en **phase 5** (runtime en réunion), où la qualité
  du LLM détermine directement la crédibilité du clone. Décision à prendre sur la base
  d'un comparatif local vs API avec vos vraies données.
