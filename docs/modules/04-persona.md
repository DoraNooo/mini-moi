# Module 04 — Persona (le « cerveau »)

Une voix et un visage parfaits qui disent des choses que vous ne diriez pas = clone raté.

## Composants

1. **Profil** (`persona/profile.md`) : synthèse rédigée à partir des entretiens — identité,
   valeurs, opinions, style d'humour, sujets sensibles, façon de dire non, etc.
2. **Guide de style oral** : tics de langage avec fréquence, expressions favorites,
   longueur typique des réponses, tutoiement/vouvoiement, registre selon l'interlocuteur.
   Extrait automatiquement des transcriptions verbatim.
3. **Mémoire factuelle (RAG)** : toutes les transcriptions découpées et indexées ;
   le clone retrouve « ce que j'ai dit sur X » avant de répondre.
4. **Garde-fous** : ce que le clone ne doit jamais faire (s'engager, promettre, décider,
   divulguer des infos confidentielles) — il répond « je reviens vers toi » à la place.

## Évaluation

Jeu de 50 questions de référence répondues par vous en vrai ; comparaison automatique
(LLM juge) + test humain à l'aveugle.
