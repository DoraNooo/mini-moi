# Roadmap

Chaque phase a un **critère de sortie** : on ne passe pas à la suivante sans l'avoir atteint.

> **V1 = clone vocal** (voix + personnalité, caméra coupée dans Teams).
> **V2 = ajout du visage**, une fois la V1 validée (ADR-0005).

## Phase 0 — Cadrage *(terminée)*
- [x] Mise au propre de la vision et de l'architecture
- [x] Matériel (ADR-0002), mode autonome (ADR-0003), sans clé API (ADR-0004), V1 vocale (ADR-0005)
- [x] Questions bloquantes répondues
- [ ] Chiffrement du disque activé sur le PC (à faire par vous, voir `interviewer/README.md`)
- **Sortie :** questions bloquantes répondues, stockage chiffré en place.

# V1 — Clone vocal

## Phase 1 — Agent interviewer + enregistrement *(en cours)*
- [x] Banque de 15 thèmes + 30 phrases de lecture + 12 phrases à émotion (`interviewer/questions/`)
- [x] Agent vocal : Ollama (gemma3:12b) + Whisper + voix Piper (`interviewer/`)
- [x] Enregistreur : audio Blue Yeti WAV + `meta.json` horodaté + `transcript.md`
- [x] Commande de diagnostic `python -m interviewer test`
- [x] Prompt d'analyse inter-sessions pour Claude Code local
- [ ] Installation sur le PC Windows + `test` au vert *(vous)*
- [ ] Session pilote de 20 min → vérification qualité audio *(vous, puis analyse ensemble)*
- [ ] *(optionnel)* vidéo webcam enregistrée en parallèle via OBS, réserve V2
- **Sortie :** une session pilote exploitable de bout en bout.

## Phase 2 — Collecte + pipeline de préparation *(en parallèle de la suite)*
- [ ] 10 à 20 sessions de 30-45 min (objectif : 3 h+ de parole nette, 5 h idéal)
- [ ] Bloc « lecture » : textes phonétiquement riches + émotions variées
- [ ] Pipeline : débruitage, découpage, transcription verbatim, indexation
- **Sortie :** dataset voix ≥ 1 h propre, transcriptions indexées.

## Phase 3 — Voix
- [ ] POC zero-shot (5 min de données) → mesure de la base
- [ ] Fine-tune sur le dataset complet
- [ ] Test aveugle avec des proches
- **Sortie :** critères voix de `VISION.md` atteints.

## Phase 4 — Persona + intégration Teams en audio (voir module 06)
- [ ] Base de connaissance « moi » (RAG) + profil + guide de style oral
- [ ] **4a — Présentation** : document préparé → script dans votre style (validé par vous)
      → audio **pré-généré** → diffusé dans Teams avec partage d'écran et avance des slides
      *(premier livrable « pro »)*
- [ ] **4b — Questions/réponses en 1-à-1** : streaming STT → LLM → TTS → micro virtuel
- [ ] **4c — Réunion à plusieurs** : suivre la discussion, détecter quand on l'interroge,
      compte rendu après réunion
- [ ] Image Teams : caméra coupée + photo de profil (ou image fixe « clone de … »)
- **Sortie :** une présentation de 5 min + 10 min de Q/R fluides (latence < 1,5 s)
  devant un collègue informé.

# V2 — Visage

## Phase 5 — Captation vidéo dédiée
- [ ] Matériel : smartphone sur pied ou meilleure webcam, éclairage (PROTOCOLE-CAPTURE)
- [ ] Sessions courtes dédiées au visage (parole, écoute, expressions, angles)

## Phase 6 — Avatar
- [ ] POC talking-head piloté par l'audio de la voix clonée
- [ ] Avatar personnalisé, test en conditions Teams (720p, compression)
- [ ] Branchement sur la caméra virtuelle, mode écoute + mode parole
- **Sortie :** critères visage de `VISION.md` atteints.

## Ensuite — Itération
Boucle : nouvelles sessions ciblées sur les faiblesses détectées → réentraînement.
