# Vision et périmètre

## Objectif

Un double numérique capable de :

1. **parler avec votre voix** — timbre, intonation, rythme, débit, pauses, tics de langage
   (« du coup », « en fait », hésitations, rires…) ;
2. **apparaître avec votre visage** dans une visio Teams, avec un lip-sync et des
   micro-expressions crédibles ;
3. **répondre comme vous** — vos opinions, vos souvenirs, votre vocabulaire, votre humour.

## Deux modes d'usage (à trancher, cf. QUESTIONS-OUVERTES)

| | Mode A — « Marionnette » | Mode B — « Autonome » |
|---|---|---|
| Qui parle ? | Vous (ou quelqu'un) en direct | Un LLM avec votre persona |
| Ce que fait le système | Convertit la voix/visage en temps réel (speech-to-speech, face reenactment) | Génère le texte → voix clonée → visage animé |
| Difficulté | Moyenne | Élevée (latence, cohérence, persona) |
| Latence cible | < 300 ms | < 1,5 s entre fin de question et début de réponse |
| Utilité | Démo, tests de crédibilité, accessibilité | Le vrai « mini-moi » |

**Recommandation :** construire le mode A d'abord (il valide voix + visage isolément),
puis le mode B qui réutilise les mêmes briques.

## Définition de « convaincant » (mesurable)

On ne se contente pas d'impressions. Critères de sortie proposés :

- **Voix** : test à l'aveugle avec 5 proches — extraits de 10 s vrais vs clonés,
  taux d'identification correcte ≤ 60 % (≈ hasard). Similarité de locuteur (embedding
  ECAPA) ≥ 0,85 avec vos enregistrements réels.
- **Visage** : clip de 30 s en conditions Teams (720p, compression), même test aveugle.
  Pas d'artefacts visibles aux bords du visage, aux dents, aux lunettes, aux mains.
- **Persona** : 20 questions posées par un proche, réponses du clone vs les vôtres —
  le proche ne doit pas les distinguer au-delà du hasard.
- **Temps réel** : 10 minutes de visio sans décrochage, latence conforme au mode.

## Hors périmètre (pour l'instant)

- Le corps entier / les gestes des mains.
- Les langues autres que le français (à rediscuter).
- Toute utilisation sans que les interlocuteurs le sachent — voir `ETHIQUE-SECURITE.md`.
