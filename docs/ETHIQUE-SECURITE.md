# Éthique, légal et sécurité

Ce n'est pas une formalité : un clone convaincant de vous est aussi **l'outil idéal pour
vous usurper**. Ces règles protègent d'abord vous.

## 1. Transparence envers les interlocuteurs

- Règle du projet : **le clone ne participe à une réunion qu'avec des personnes qui
  savent qu'elles parlent au clone** (ou qui l'ont accepté au préalable).
- Cadre légal : le règlement européen sur l'IA (AI Act, art. 50) impose de signaler
  les contenus audio/vidéo générés ou manipulés qui imitent une personne réelle
  (« deepfakes »), avec des obligations applicables à partir d'août 2026.
  À faire valider selon votre usage précis.
- Employeur : vérifier la politique interne (charte informatique, règles Teams,
  enregistrement des réunions, confidentialité). Assister à une réunion via un clone
  sans accord peut poser des problèmes contractuels.
- Toute personne qui apparaît ou est entendue dans les enregistrements doit avoir consenti.
- **Enregistrements libres (Discord, etc.)** : seul le micro de l'utilisateur est enregistré,
  jamais le son de Discord. Casque obligatoire, et les amis sont prévenus. Enregistrer la
  voix de quelqu'un à son insu, dans un cadre privé, est interdit en France
  (art. 226-1 du Code pénal).

## 2. Vos données sont biométriques

Voix et visage sont des données biométriques au sens du RGPD. Même si vous êtes le seul
concerné, traitez-les comme ultra-sensibles :

- Stockage **chiffré**, jamais dans git, jamais sur un cloud non chiffré.
- Les poids des modèles entraînés valent autant que les données : même protection.
- Services tiers (ElevenLabs, HeyGen…) : lire les CGU sur la conservation/réutilisation
  des données ; supprimer les données après le POC si on migre en local.
- Transcriptions = votre vie privée (et celle des gens que vous mentionnez) : même régime.

## 3. Protection anti-usurpation

- Prévenir vos proches / votre banque que votre voix peut être imitée ; convenir
  d'un **mot de passe familial** pour les demandes urgentes.
- Marquer les sorties du clone (watermark audio/vidéo invisible) quand c'est possible.
- Garder une trace (log) de chaque utilisation du runtime.

## 4. Garde-fous du clone

- Ne prend aucun engagement, ne valide rien, ne signe rien, ne transmet pas d'information
  confidentielle.
- Bouton d'arrêt immédiat (cf. module 05).
