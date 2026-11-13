# Plan d'action V1 : quand pourrez-vous tester votre clone ?

> **Principe :** inutile d'attendre la fin de la collecte pour tester. Chaque jalon
> s'appuie sur ce qui est déjà enregistré. On commence par des tests simples, de plus
> en plus proches de l'usage réel en réunion.

## Hypothèses de calcul

- La session pilote a donné environ 9 min de parole utile pour 20 min. Une session complète
  de 40 min doit donc donner **environ 18 min de parole utile**, lecture comprise.
- Rythme visé : **3 sessions par semaine** (soirs après 21 h et après-midi de week-end).
- Objectifs de données voix :
  - 1 h de parole utile : environ 4 sessions ;
  - 3 h de parole utile : environ 10 à 12 sessions.

## Les jalons

| # | Jalon | Ce que vous testez | Données nécessaires | Quand (estimation) |
|---|---|---|---|---|
| 1 | **Première écoute** | Votre voix clonée lit des phrases que vous n'avez jamais dites | 10 à 30 s de votre voix | **Session 2-3** (semaine 1) |
| 2 | **Mini-moi à l'écrit** | Vous discutez par écrit avec votre persona : répond-il comme vous ? | Profil après 4-5 sessions | **Semaine 2** |
| 3 | **Voix entraînée** | Voix affinée sur vos données, puis test à l'aveugle avec 3 à 5 proches | ≥ 1 h propre | **Semaine 3** (après ~5 sessions) |
| 4 | **Mini-moi parle** | Conversation orale avec votre clone sur le PC : vous parlez, il répond avec votre voix | Jalons 2 + 3 | **Semaine 4-5** |
| 5 | **Première présentation Teams** | Le clone présente un document (préparé et relu par vous) dans une réunion Teams avec un collègue informé | ~3 h + persona pro | **Semaine 5-6** (~12 sessions) |
| 6 | **Questions-réponses dans Teams** | Le collègue pose des questions, le clone répond en direct | Jalon 5 + pipeline temps réel | **Semaine 7-8** |
| 7 | **Vraie réunion** | Réunion à plusieurs, clone annoncé : il suit, répond quand on l'interroge, puis vous fait un compte rendu | Jalon 6 | **Semaine 9+** |

Ces dates dépendent surtout du nombre de sessions faites et de ce que révèlent les
premiers tests. Elles seront recalées à chaque jalon.

## Détail des jalons

### Jalon 1 : Première écoute *(prochain livrable)*
- **Comment** : une commande lit un texte de votre choix avec votre voix, en partant d'un
  extrait propre de vos sessions (clonage « zero-shot », sans entraînement).
- **Ce qui sera comparé** : 2 ou 3 modèles open source qui parlent français. Les
  candidats sont XTTS-v2 et F5-TTS, liste à confirmer selon l'état de l'art au moment du test.
- **Attendu, honnêtement** : un timbre reconnaissable, mais une intonation générique,
  pas encore votre rythme ni vos tics. C'est normal : ce test sert à mesurer le point de départ.
- **Critère de réussite** : vous reconnaissez votre voix, sans vous y tromper.

### Jalon 2 : Mini-moi à l'écrit
- **Comment** : un chat dans le terminal, avec un modèle local nourri de `profil.md`,
  `style_oral.md` et de toutes vos transcriptions.
- **Test** : vous préparez 20 questions et notez vos propres réponses. Le clone y répond
  à son tour, puis on compare. Faites aussi lire ses réponses à un proche.
- **Pourquoi si tôt** : c'est le meilleur moyen de savoir quels thèmes manquent, et donc
  d'orienter les sessions suivantes.

### Jalon 3 : Voix entraînée
- **Prérequis** : le pipeline de préparation (phase 2) découpe les sessions, retire la
  voix de Léa, transcrit mot à mot et applique les `corrections.md`.
- **Comment** : entraînement sur votre RTX 4080. Prévoir une soirée de calcul, sans
  rester devant l'écran.
- **Test à l'aveugle** : 10 extraits de 10 s, mélange de vrais et de clonés, écoutés par
  vos proches.
- **Critère de réussite** : vos proches ont raison à 70 % ou moins. La cible finale est
  60 %, c'est-à-dire le hasard.

### Jalon 4 : Mini-moi parle
- **Comment** : on assemble la transcription, la persona et la voix entraînée. Vous parlez
  au micro, le clone répond dans le casque.
- **Ce qui est mesuré** : le délai de réponse (cible < 1,5 s), le naturel, la présence de vos tics.
- **Décision à prendre ici** : modèle local ou API Claude pour le cerveau (ADR-0004).
  On comparera les deux sur vos propres questions.

### Jalon 5 : Première présentation Teams
- **Comment** :
  1. Vous fournissez un document, par exemple l'avancement d'un projet.
  2. Le clone rédige le discours dans votre style. **Vous le relisez et le corrigez.**
  3. L'audio est généré à l'avance, en qualité maximale.
  4. Pendant la réunion, le clone le diffuse via le micro virtuel et fait avancer les
     slides dans le partage d'écran.
- **Test** : réunion Teams privée avec un collègue au courant.
- **Prérequis côté collecte** : au moins 3 sessions sur les thèmes pro (« Toi en réunion »,
  « Le métier au quotidien », « Parcours pro »).

### Jalons 6 et 7
Voir `docs/modules/06-reunion-pro.md`. Ce sont les plus difficiles : écouter en continu,
savoir quand il faut répondre, gérer les tours de parole.

## Répartition du travail

| Vous | Moi (chef de projet + dev) |
|---|---|
| 3 sessions de 40 min par semaine | Jalon 1 : outil d'écoute de la voix clonée |
| Analyse locale après chaque session (5 min) | Phase 2 : pipeline de préparation des données |
| Tests aux jalons : votre avis, et celui de vos proches pour les tests à l'aveugle | Jalon 2 : chat persona |
| Choisir les thèmes si une envie vous prend | Jalons 3 à 7 : entraînement voix, assemblage, Teams |
| Collez-moi le bilan de chaque analyse | Ajuster Léa et le plan à chaque bilan |

## Ordre conseillé des thèmes (priorité à l'usage pro)

1. parcours_pro (prévu pour la session 2)
2. metier
3. reunions
4. collegues
5. fiertes_echecs
6. opinions_tech
7. humour (utile pour les émotions de la voix)
8. Thèmes libres : loisirs, goûts, voyages, valeurs, habitudes, opinions_societe

L'analyse inter-sessions peut adapter cet ordre en fonction des manques.
