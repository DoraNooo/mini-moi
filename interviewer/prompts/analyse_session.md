# Analyse inter-sessions — à faire avec Claude Code **en local** sur votre PC

> Pourquoi en local ? Les transcriptions sont votre vie privée : elles restent dans
> `data/` (non versionné) et ne doivent jamais être poussées sur GitHub.
> Ouvrez Claude Code (application de bureau ou terminal) dans le dossier du dépôt
> et collez la demande ci-dessous.

---

Lis la dernière session dans `data/sessions/` (fichier `transcript.md` le plus récent),
ainsi que `data/persona/profil.md`, `data/persona/style_oral.md` et `data/progress.json`
s'ils existent. Puis :

1. **Mets à jour `data/persona/profil.md`** : faits biographiques, métier et projets,
   opinions, valeurs, goûts, relations, anecdotes (résumées, avec le numéro de session
   source). Signale les contradictions avec ce qui était déjà noté plutôt que d'écraser.
   Ajoute une section « Sujets à éviter » si la personne a refusé ou mal vécu un sujet.
2. **Mets à jour `data/persona/style_oral.md`** à partir du verbatim : tics de langage et
   fréquence approximative, expressions favorites, façons de commencer et de finir une
   phrase, longueur typique des réponses, registre, humour, manière d'hésiter.
3. **Écris `data/plans/prochaine_session.md`** : thème conseillé (clé de
   `interviewer/questions/themes.yaml`) sur la première ligne au format `theme: <clé>`,
   puis 5 à 8 pistes concrètes qui comblent les trous du profil ou creusent des sujets
   ouverts, et une idée de position contradictoire pour le bloc débat.
4. **Donne-moi un bilan court** : minutes de parole utile, qualité des réponses
   (spontanées ou trop courtes), ce qui manque pour la voix (émotions, registres) et
   pour la persona.

Garde `profil.md` sous 3 000 mots : il est injecté dans le prompt de l'intervieweuse.
