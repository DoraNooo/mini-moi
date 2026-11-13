# Vision et périmètre

## Objectif

Un double numérique capable de :

1. **parler avec votre voix** — timbre, intonation, rythme, débit, pauses, tics de langage
   (« du coup », « en fait », hésitations, rires…) ;
2. **apparaître avec votre visage** dans une visio Teams, avec un lip-sync et des
   micro-expressions crédibles ;
3. **répondre comme vous** — vos opinions, vos souvenirs, votre vocabulaire, votre humour.

## Mode cible : autonome (décidé, ADR-0003)

Le clone **répond seul** : il écoute la réunion, un LLM nourri de votre persona formule
la réponse, la voix clonée la prononce, l'avatar l'anime. Vous n'êtes pas présent.

Le « mode marionnette » (vous parlez, le système transforme voix/visage) est **abandonné**
comme objectif. Ses briques (voix, visage) restent testées isolément pendant les phases 3-4.

Les interlocuteurs savent toujours qu'ils parlent au clone.

## Définition de « convaincant » (mesurable)

On ne se contente pas d'impressions. Critères de sortie proposés :

- **Voix** : test à l'aveugle avec 5 proches — extraits de 10 s vrais vs clonés,
  taux d'identification correcte ≤ 60 % (≈ hasard). Similarité de locuteur (embedding
  ECAPA) ≥ 0,85 avec vos enregistrements réels.
- **Visage** : clip de 30 s en conditions Teams (720p, compression), même test aveugle.
  Pas d'artefacts visibles aux bords du visage, aux dents, aux lunettes, aux mains.
- **Persona** : 20 questions posées par un proche, réponses du clone vs les vôtres —
  le proche ne doit pas les distinguer au-delà du hasard.
- **Temps réel** : 10 minutes de visio sans décrochage, latence < 1,5 s entre la fin
  d'une question et le début de la réponse.

## Découpage en versions (ADR-0005)

- **V1 — clone vocal** : voix + personnalité ; dans Teams, caméra coupée.
- **V2 — visage** : avatar vidéo, construit sur la V1.

## Hors périmètre (pour l'instant)

- Le corps entier / les gestes des mains.
- Les langues autres que le français (à rediscuter).
- Toute utilisation sans que les interlocuteurs le sachent — voir `ETHIQUE-SECURITE.md`.
