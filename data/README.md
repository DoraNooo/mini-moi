# data/

Ce dossier est **ignoré par git** (sauf ce fichier). Il accueille localement :

```
data/
├── raw/          # enregistrements bruts des sessions (vidéo + audio séparé)
├── sessions/     # métadonnées par session (questions, horodatages, transcription)
├── voice/        # segments audio nettoyés, découpés, transcrits
├── face/         # frames / clips extraits pour l'entraînement visage
└── persona/      # transcriptions structurées pour la base de connaissance « moi »
```

Le stockage de référence doit être **chiffré** (disque chiffré ou coffre type VeraCrypt / Cryptomator)
et sauvegardé hors ligne. Voir `docs/ETHIQUE-SECURITE.md`.
