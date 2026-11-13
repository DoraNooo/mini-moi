# Agent interviewer — guide d'installation et d'utilisation (Windows 11)

L'intervieweuse (« Léa ») vous pose des questions à voix haute dans votre casque. Vous
répondez naturellement au Blue Yeti. Toute la session est enregistrée en un seul fichier
audio, avec la transcription horodatée de chaque échange.

**Tout tourne sur votre PC** : modèle de langage (Ollama), transcription (Whisper sur la
RTX 4080), voix de synthèse (Piper). Rien n'est envoyé sur Internet pendant une session.

---

## 1. Installation (une seule fois, ~30 min)

Ouvrez **PowerShell** et lancez les commandes une par une.

### Outils
```powershell
winget install Python.Python.3.12
winget install Git.Git
winget install Ollama.Ollama
```
Fermez et rouvrez PowerShell après ces installations.

### Le projet
```powershell
cd $HOME\Documents
git clone https://github.com/DoraNooo/mini-moi.git
cd mini-moi
git checkout claude/admiring-shannon-a3wlzt
```

### Environnement Python
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r interviewer\requirements.txt
```
> Si PowerShell refuse d'activer l'environnement (« l'exécution de scripts est désactivée ») :
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, puis relancez la commande.

### Le modèle de langage
```powershell
ollama pull gemma3:12b
```
(environ 8 Go à télécharger)

### La configuration
```powershell
copy interviewer\config.example.yaml config.yaml
notepad config.yaml
```
Ce qu'il faut vérifier : `input_device: Yeti`. Mettez le nom de votre casque dans
`output_device` si ce n'est pas la sortie par défaut de Windows.

---

## 2. Réglages Windows et Blue Yeti (une seule fois)

- **Paramètres → Confidentialité → Microphone** : autoriser les applications de bureau.
- **Paramètres → Son → Yeti → Propriétés** :
  - format **48000 Hz** ;
  - **désactiver les « Améliorations audio »**, car on veut le son brut.
- **Yeti** :
  - mode **cardioïde** (le symbole cœur) ;
  - gain à environ 1/3 ;
  - parler **dans le côté avec le logo**, à 15-20 cm.
- **Casque obligatoire** : sinon le Yeti enregistre aussi la voix de Léa.

---

## 3. Vérification

Chaque fois que vous rouvrez PowerShell, activez d'abord l'environnement :
```powershell
cd $HOME\Documents\mini-moi
.\.venv\Scripts\Activate.ps1
```
Ensuite, listez les micros et casques :
```powershell
python -m interviewer devices
```
Puis lancez le test complet du micro, de la transcription, du modèle et de la voix :
```powershell
python -m interviewer test
```
Le test dit quoi corriger : voix trop faible, saturation, bruit de fond, GPU non utilisé…
Il doit se terminer par **OK** sur les quatre lignes.

---

## 4. Faire une session (~40 min)

```powershell
python -m interviewer session
```

Options :
- `--theme humour` : choisir le thème (liste dans `interviewer/questions/themes.yaml`).
- `--minutes 20` : faire une session plus courte.
- `--texte` : mode texte au clavier, pour essayer sans micro (non comptabilisé).

Pendant la session (la fenêtre PowerShell doit être active) :

| Touche | Effet |
|---|---|
| *(rien)* | Votre réponse se termine après 2,5 s de silence. |
| **Entrée** | « J'ai fini ma réponse » : Léa répond tout de suite. |
| **s** | « Je préfère passer » : Léa change de sujet sans insister. |
| **p** | Pause. Une touche pour reprendre. |
| **q** | Arrêter la session tout de suite (tout est sauvegardé). |

Vous pouvez aussi simplement **dire** « on passe » ou « on fait une pause ».

**Déroulé :**
1. Calibration : 3 s de silence.
2. Échauffement : 3 min.
3. Thème du jour : 25 min.
4. Débat, où Léa vous contredit exprès : 6 min.
5. Lecture de phrases affichées à l'écran : 6 min.

**Conseils pour de bonnes données :**
- Parlez comme à un collègue, avec vos « euh » et vos « du coup ». On veut **votre** façon de parler, pas une voix de présentateur.
- Développez : les longues réponses valent de l'or.
- Si Léa vous coupe trop tôt, augmentez `vad.silence_s` dans `config.yaml`, par exemple à 3.5.

**Ce qui est produit**, dans `data/sessions/<date_heure>/` :
- `audio.wav` : la session entière ;
- `meta.json` : chaque prise de parole avec son horodatage dans `audio.wav` ;
- `transcript.md` : la transcription lisible.

---

## 5. Après chaque session : l'analyse (5 min)

Ouvrez **Claude Code en local**, avec l'application de bureau ou le terminal, dans le dossier
`mini-moi`. Donnez-lui le contenu de `interviewer/prompts/analyse_session.md`.

Il met à jour votre profil (`data/persona/`) et prépare le plan de la session suivante
(`data/plans/prochaine_session.md`). Léa s'en servira automatiquement à la prochaine session.

> Ne faites **pas** cette analyse dans une session Claude Code « cloud » : il faudrait
> pousser vos transcriptions sur GitHub. Elles doivent rester sur votre PC.

---

## 6. Protéger vos données

`data/` contient votre voix et votre vie privée : ce dossier n'est jamais envoyé sur git.
Activez le **chiffrement du disque** :
- Windows 11 Famille : Paramètres → Confidentialité et sécurité → Chiffrement de l'appareil ;
- Windows 11 Pro : BitLocker.

Faites aussi une sauvegarde régulière sur un disque externe chiffré.

---

## En cas de problème

| Symptôme | Piste |
|---|---|
| `Aucun périphérique input contenant « Yeti »` | `python -m interviewer devices`, puis copier une partie du nom exact dans `config.yaml`. |
| Erreur à l'ouverture du micro | Mettre `channels: 2` dans `config.yaml`. |
| Transcription sur CPU (lente) | `pip install --force-reinstall nvidia-cublas-cu12 "nvidia-cudnn-cu12>=9,<10"`, et mettre à jour le pilote NVIDIA. |
| `Ollama ne répond pas` | Lancer l'application Ollama (icône lama dans la barre des tâches). |
| Léa répond lentement (> 5 s) | Essayer un modèle plus petit : `ollama pull mistral-nemo`, puis `llm.model: mistral-nemo`. |
| Pas de voix dans le casque | Mettre le nom du casque dans `audio.output_device`. |
