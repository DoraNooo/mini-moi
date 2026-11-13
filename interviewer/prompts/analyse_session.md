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
   puis 5 à 8 pistes **concrètes** (« raconte une fois où… ») qui comblent les trous du
   profil ou creusent des sujets ouverts, puis une ligne `Idée de débat : <thèse tranchée>`
   contraire à ses opinions connues.
4. **Écris `data/sessions/<id>/corrections.md`** : mots ou noms mal transcrits par Whisper
   (avec la forme correcte probable) et phrases inventées par Whisper (« Sous-titrage… »,
   « Merci d'avoir regardé… ») avec leur horodatage. La phase 2 s'en servira pour nettoyer
   les données de voix.
5. **Vérifie le comportement de Léa** : accords grammaticaux, refus respectés sans
   demander pourquoi, débat réellement contradictoire, questions concrètes plutôt
   qu'abstraites. Liste les écarts dans le bilan (ils servent à corriger
   `interviewer/prompts/system.md`).
6. **Donne-moi un bilan court** : minutes de parole utile, qualité des réponses
   (spontanées ou trop courtes), ce qui manque pour la voix (émotions, registres) et
   pour la persona.

### Cas d'un enregistrement libre (`data/libre/…`, ex. Discord)
Seule la voix de l'utilisateur y figure : les répliques sont hors contexte, ne les
interprète pas comme des opinions. Dans ce cas :
- n'ajoute au profil que des faits explicites et certains ;
- dans `style_oral.md`, crée ou complète une section **« Registre détendu (entre amis / jeu) »**,
  séparée du registre normal : vocabulaire, jurons, blagues, exclamations, rires. Le clone
  pro ne doit **pas** utiliser ce registre en réunion, mais il doit savoir qu'il existe ;
- liste dans `corrections.md` les passages les plus expressifs (rire, enthousiasme,
  agacement), avec leur horodatage et l'émotion : ce sont des extraits précieux pour la voix ;
- ne crée pas de plan de session.

Garde `profil.md` sous 3 000 mots : il est injecté dans le prompt de l'intervieweuse.
