# Module 01 — Voix

## Ce qu'on doit capturer

| Dimension | Comment on la capture | Comment on la reproduit |
|---|---|---|
| Timbre | N'importe quelle parole propre | Embedding locuteur / fine-tune |
| Prosodie (intonation, rythme, débit) | Parole **spontanée** (entretiens), pas seulement lue | Fine-tune sur parole spontanée |
| Tics de langage (« du coup », « euh », rires) | Transcription **verbatim** (on garde les « euh ») | Côté texte : le LLM persona les insère ; côté audio : le modèle sait les prononcer |
| Registre émotionnel | Questions qui font rire, s'énerver, s'émouvoir | Données étiquetées par émotion |
| Couverture phonétique | Bloc de lecture de textes phonétiquement riches | — |

Point important : **les tics de langage sont pour moitié un problème de texte**. Un TTS
parfait qui lit un texte « propre » sonnera faux. Le module persona doit produire du
texte qui contient vos hésitations et tournures ; le TTS doit savoir les rendre.

## Volumes de données visés

- Zero-shot (POC) : 10 s à 1 min suffisent pour un premier rendu.
- Fine-tune correct : 30 min à 1 h de parole nette.
- Haute fidélité : 3 h+ incluant spontané, lu, et émotions variées.

## Pipeline de préparation

1. Débruitage léger (pas trop : on perd le timbre) — ex. DeepFilterNet.
2. Diarisation : retirer la voix de l'agent interviewer.
3. Découpage en segments de 3-15 s (VAD).
4. Transcription verbatim (WhisperX) + alignement mot à mot.
5. Filtrage qualité (SNR, chevauchements, saturation).

## Évaluation

- Similarité locuteur automatique (ECAPA-TDNN / Resemblyzer).
- Taux d'erreur de transcription du clone (intelligibilité).
- Test d'écoute à l'aveugle (cf. VISION.md).
