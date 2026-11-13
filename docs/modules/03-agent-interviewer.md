# Module 03 — Agent interviewer (« psychologue »)

## Rôle

Un agent conversationnel vocal qui mène des entretiens filmés. Il a **trois missions
simultanées** — c'est ce qui le distingue d'un simple questionnaire :

1. **Vous connaître** (pour la persona) : biographie, valeurs, opinions, travail, relations,
   anecdotes, goûts, manière de raisonner.
2. **Vous faire parler longtemps et naturellement** (pour la voix) : questions ouvertes,
   relances, laisser des silences.
3. **Varier vos états** (pour la voix et le visage) : vous faire rire, réfléchir,
   argumenter, raconter, vous émouvoir.

## Comportement

- Style d'un intervieweur bienveillant (biographe / psychologue), **pas** un thérapeute :
  il n'a pas vocation à diagnostiquer ni soigner. Si un sujet devient pénible, on passe.
- Une question à la fois, relances courtes (« Et ensuite ? », « Pourquoi ça ? »).
- Parle peu : objectif ≥ 80 % du temps de parole pour vous.
- Garde une mémoire des sessions précédentes : ne repose pas les mêmes questions,
  creuse les sujets ouverts, comble les trous de la persona.
- Surveille la couverture : thèmes abordés, émotions obtenues, minutes utiles collectées.

## Structure d'une session (30-45 min)

| Bloc | Durée | But |
|---|---|---|
| Échauffement | 3 min | Small talk, vérif son/image |
| Thème du jour | 20-25 min | Entretien approfondi sur 1 thème |
| Débat | 5 min | L'agent prend une position contraire → vous argumentez |
| Lecture | 5 min | Texte phonétiquement riche / phrases avec émotion imposée |
| Écoute *(V2 seulement)* | 2-3 min | L'agent raconte quelque chose, vous écoutez (données « écoute active » visage) |

## Banque de thèmes (v1)

Enfance et famille · Études · Parcours pro · Votre métier au quotidien · Collègues et
management · Projets dont vous êtes fier · Échecs · Opinions (tech, société, actu) ·
Loisirs · Voyages · Goûts (musique, films, bouffe) · Humour · Valeurs · Manies et habitudes ·
Comment vous prenez une décision · Comment vous réagissez en réunion.

## Architecture technique (proposition)

```
Micro ──► Whisper (GPU) ──► LLM local Ollama (prompt « intervieweuse » + profil) ──► Piper ──► Casque
                                         │
OBS / ffmpeg ──► video.mp4 + audio.wav   └──► meta.json (question, t_début, t_fin, thème)
```

- Interface : application web locale ou script Python ; un bouton « pause/stop ».
- L'agent doit utiliser une voix **clairement différente** de la vôtre (diarisation facile).
- Idéalement casque pour l'écoute de l'agent → votre micro n'enregistre que vous.

## Livrables phase 1

- `interviewer/prompts/system.md` — prompt de l'intervieweur
- `interviewer/questions/` — banque de thèmes et questions
- `interviewer/app/` — boucle vocale + enregistrement
- `interviewer/memory/` — résumé cumulatif des sessions (stocké chiffré, hors git)
