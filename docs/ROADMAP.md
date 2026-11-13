# Roadmap

Chaque phase a un **critère de sortie** : on ne passe pas à la suivante sans l'avoir atteint.

## Phase 0 — Cadrage *(en cours)*
- [x] Mise au propre de la vision et de l'architecture
- [x] Matériel (ADR-0002) et mode autonome (ADR-0003)
- [ ] Réponses aux [questions ouvertes](QUESTIONS-OUVERTES.md) restantes (OS, budget API, contexte d'usage)
- [ ] Choix du stockage chiffré pour `data/`
- **Sortie :** questions bloquantes répondues, stockage chiffré en place.

## Phase 1 — Agent interviewer + enregistrement
- [ ] Banque de questions v1 (cf. module 03)
- [ ] Agent conversationnel vocal (LLM + voix synthétique neutre + écoute)
- [ ] Enregistreur : vidéo + audio séparé + `meta.json` horodaté
- [ ] Session pilote de 20 min → vérification qualité audio/vidéo
- **Sortie :** une session pilote exploitable de bout en bout.

## Phase 2 — Collecte + pipeline de préparation *(en parallèle de la suite)*
- [ ] 10 à 20 sessions de 30-45 min (objectif : 3 h+ de parole nette, 5 h idéal)
- [ ] Bloc « lecture » : textes phonétiquement riches + émotions variées
- [ ] Pipeline : débruitage, découpage, transcription, extraction visage, indexation
- **Sortie :** dataset voix ≥ 1 h propre, dataset visage trié, transcriptions indexées.

## Phase 3 — Voix
- [ ] POC zero-shot (5 min de données) → mesure de la base
- [ ] Fine-tune sur le dataset complet
- [ ] Test aveugle avec des proches
- **Sortie :** critères voix de `VISION.md` atteints.

## Phase 4 — Visage
- [ ] POC talking-head à partir d'une vidéo de référence
- [ ] Modèle dédié (avatar personnalisé) entraîné sur les sessions
- [ ] Test en conditions Teams (compression, 720p)
- **Sortie :** critères visage atteints.

## Phase 5 — Persona + intégration temps réel
- [ ] Base de connaissance « moi » (RAG) + prompt de personnalité
- [ ] Pipeline streaming STT → LLM → TTS → avatar
- [ ] Caméra/micro virtuels, test en réunion Teams privée (vous + un complice informé)
- **Sortie :** 10 min de conversation fluide, latence < 1,5 s.

## Phase 6 — Itération
Boucle : nouvelles sessions ciblées sur les faiblesses détectées → réentraînement.
