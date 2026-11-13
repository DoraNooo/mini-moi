# mini-moi

> Créer un double numérique (voix + visage + personnalité) suffisamment fidèle pour tenir
> une conversation en visio (Microsoft Teams).

**Statut :** Phase 0 — cadrage (presque terminée). Prochaine étape : phase 1, l'agent interviewer.

## Le projet en une image

```
             ┌──────────────────────────────────────────────┐
             │  3. AGENT INTERVIEWEUR (« psychologue »)      │
             │  pose des questions, vous répondez à l'oral,  │
             │  vous êtes filmé  ──►  sessions enregistrées  │
             └───────────────┬──────────────────────────────┘
                             │  une seule source de données,
                             │  trois usages
          ┌──────────────────┼───────────────────┐
          ▼                  ▼                   ▼
   ┌─────────────┐   ┌───────────────┐   ┌────────────────┐
   │ 1. VOIX     │   │ 2. VISAGE     │   │ PERSONA        │
   │ timbre,     │   │ apparence,    │   │ souvenirs,     │
   │ rythme,     │   │ expressions,  │   │ opinions,      │
   │ tics        │   │ lip-sync      │   │ façon de parler│
   └──────┬──────┘   └───────┬───────┘   └───────┬────────┘
          └──────────────────┼───────────────────┘
                             ▼
             ┌──────────────────────────────────────┐
             │ 4. RUNTIME TEMPS RÉEL                │
             │ caméra + micro virtuels ──► Teams    │
             └──────────────────────────────────────┘
```

Le point 3 est le **moteur** du projet : chaque session d'entretien produit en même temps
de l'audio (voix), de la vidéo (visage) et du contenu (personnalité). On ne fait pas trois
collectes de données séparées, on en fait une, bien conçue.

## Documentation

| Document | Contenu |
|---|---|
| [docs/VISION.md](docs/VISION.md) | Objectifs, périmètre, définition de « convaincant », modes d'usage |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Pipeline technique de bout en bout |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Phases, jalons, critères de sortie |
| [docs/modules/01-voix.md](docs/modules/01-voix.md) | Clonage de la voix |
| [docs/modules/02-visage.md](docs/modules/02-visage.md) | Avatar vidéo *(V2)* |
| [docs/modules/03-agent-interviewer.md](docs/modules/03-agent-interviewer.md) | L'agent « psychologue » et la collecte |
| [docs/modules/04-persona.md](docs/modules/04-persona.md) | Le « cerveau » : comment le clone sait ce que vous savez |
| [docs/modules/05-runtime-teams.md](docs/modules/05-runtime-teams.md) | Brancher le tout dans Teams |
| [docs/modules/06-reunion-pro.md](docs/modules/06-reunion-pro.md) | Présenter un document, suivre une réunion, répondre |
| [docs/PROTOCOLE-CAPTURE.md](docs/PROTOCOLE-CAPTURE.md) | Matériel et conditions d'enregistrement |
| [docs/ETHIQUE-SECURITE.md](docs/ETHIQUE-SECURITE.md) | Cadre légal, transparence, protection de vos données |
| [docs/QUESTIONS-OUVERTES.md](docs/QUESTIONS-OUVERTES.md) | Ce que le chef de projet doit savoir de vous pour avancer |
| [docs/decisions/](docs/decisions/) | Journal des décisions (ADR) |

## Arborescence prévue

```
mini-moi/
├── docs/            # cadrage, specs, décisions
├── interviewer/     # (phase 1) agent d'entretien + enregistrement
├── pipeline/        # (phase 2) découpage, nettoyage, transcription des sessions
├── voice/           # (phase 3) entraînement / inférence voix
├── face/            # (phase 4) entraînement / inférence visage
├── persona/         # (phase 3-5) base de connaissance + prompt de personnalité
├── runtime/         # (phase 5) orchestration temps réel → Teams
└── data/            # IGNORÉ PAR GIT — vos enregistrements, chiffrés
```
