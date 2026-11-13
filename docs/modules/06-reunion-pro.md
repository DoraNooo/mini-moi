# Module 06 — Le clone en réunion pro

Trois capacités, de la plus simple à la plus difficile.

## 1. Présenter un document préparé (ex. avancement de projet)

**Idée clé : une présentation se prépare à l'avance, donc elle peut être pré-générée.**
Pas de contrainte de latence, qualité maximale (on peut générer plusieurs prises et
garder la meilleure, comme un montage).

```
Document (PPTX / PDF / notes)
   │
   ▼  LLM + persona : rédige le discours dans votre style oral, slide par slide
Script (relu et validé par vous)
   │
   ▼  TTS voix clonée (hors ligne, qualité max)  →  audio par slide
   ▼  Avatar (hors ligne, qualité max)          →  vidéo par slide
   ▼
Lecteur de présentation : diffuse la vidéo sur la caméra virtuelle,
l'audio sur le micro virtuel, et avance les slides (PowerPoint piloté
par script) au bon moment, dans un partage d'écran Teams.
```

- Vous **validez le script** avant la réunion : le clone ne dit rien que vous n'avez pas approuvé.
- Les interruptions (« tu peux revenir sur la slide 3 ? ») basculent en mode Q/R (2.),
  puis la présentation reprend.

## 2. Répondre quand on l'interroge

- Pipeline temps réel (module 05) : écoute → transcription → LLM → voix → avatar.
- **Contexte de réunion** fourni en amont : ordre du jour, participants, documents,
  état du projet, chiffres clés. Le clone répond à partir de ça + de la persona.
- Ce qu'il ne sait pas : « Je n'ai pas le chiffre sous la main, je te le renvoie
  par écrit après la réunion. » → noté dans le compte rendu.

## 3. Suivre une réunion à plusieurs

- Transcription continue de toute la réunion, avec identification des intervenants.
- Détection « on s'adresse à moi » : prénom prononcé, question directe après sa
  présentation, tour de table.
- Comportement d'écoute à l'image (hochements, regard) même quand il ne parle pas.
- **Compte rendu pour vous** après la réunion : ce qui a été dit, ce que le clone a
  répondu, les questions restées ouvertes, les engagements à prendre (par vous).

## Garde-fous pro

- Ne prend **aucun engagement** (dates, budgets, validations) : « je confirme après ».
- Ne divulgue que ce qui est dans le contexte fourni pour cette réunion.
- Message d'annonce en début de réunion (« c'est mon clone qui vous présente
  l'avancement aujourd'hui »), cohérent avec l'AI Act et votre politique d'entreprise.
- Vous pouvez suivre la réunion en direct (transcription sur votre téléphone) et
  reprendre la main.
