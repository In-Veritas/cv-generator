# In:Veritas CV Generator — Desktop App

*English below / Français plus bas*

---

## English

### What is this?

A desktop application that builds a professional, ATS-friendly, two-column PDF CV from a simple form. No installation and no Python required — just run the executable for your platform.

**Contents of this folder:**

| File / folder      | Purpose                                                              |
| ------------------ | -------------------------------------------------------------------- |
| `CV-Generator.exe` / `CV-Generator` | The application (Windows / Linux)                    |
| `cv_style.json`    | The default style (colors, fonts, sizes) — edit or import it in the app |
| `fonts/`           | Font Awesome fonts used for the icons on the CV (keep next to the exe) |
| `badges/`          | Example certification badge images (Cisco, from Credly)               |
| `whale.png`        | Decorative footer icon                                                |
| `app_icon.png` / `whale.ico` | Application window and taskbar icons (keep next to the executable) |
| `README.md`        | This file                                                             |

### Quick start

1. Unzip the folder anywhere (keep the files together).
2. Double-click `CV-Generator.exe`.
3. Pick your language — **Français, English, Español or Português**. The interface *and* the section titles printed on the PDF (Education, Skills…) follow this choice. You can change it later in the **Language** menu.
4. Fill in the tabs. Every text box shows a grey instruction explaining what to write — it disappears when you click on it.
   - **Personal**: name, headline, photo (use *Browse…* to pick a JPG/PNG — it is automatically cropped to a square), objective, about, contact details, GitHub/LinkedIn links.
   - **Education / Experience**: fill the form on the right and press *Add*. Select an entry in the list to edit it — your changes are saved automatically as you type. Press *Add* again to clear the form and start the next entry. Reorder with *Up/Down*. In descriptions, start a line with `- ` to get a colored bullet point.
   - **Skills**: optional sidebar badges (comma-separated) plus skill categories printed as colored pills in the main area.
   - **Certifications**: name, issuer, date, a link URL, and an optional badge image (see the badge tutorial below).
   - **Style**: pick your colors and sizes, or import a full style JSON.
5. **Section order**: drag the Education / Experience / Skills / Certifications tabs to reorder them — the PDF prints its sections in that exact order. The **Presets** menu offers two ready-made layouts: **Professional** (Experience first — the default) and **Academic** (Education first).
6. Press **Generate CV**, choose where to save the PDF, and you are done.

> The little whale in the bottom-left corner opens the project's GitHub page.

> **Tip:** use **File → Save CV data (.json)…** regularly so you never lose your work. Load it back with **File → Load CV data (.json)…** — the file is fully compatible with the open-source command-line generator.

### Linux and macOS

- **Linux**: the Linux package contains a `CV-Generator` binary instead of the `.exe`. From the unpacked folder, run:
  ```bash
  chmod +x CV-Generator && ./CV-Generator
  ```
  Built on Ubuntu 24.04 (x86-64); requires a desktop session. On other distributions, or if the binary refuses to start, use the source package below.
- **macOS**: there is no prebuilt app (macOS applications can only be compiled on a Mac). Use the **source package** instead — install Python 3.9+ from [python.org](https://www.python.org), then from the unpacked folder:
  ```bash
  pip3 install -r requirements.txt
  python3 cv_gui.py
  ```
  This runs the exact same application. If you want a real double-clickable app, build it on your Mac with: `pip3 install pyinstaller` then `pyinstaller --onefile --windowed --name CV-Generator cv_gui.py`.

### The missing-fields warning

When you press *Generate*, the app checks the fields that recruiters' ATS and AI screening tools usually parse: name, headline, email, phone, objective, about, education, experience, skills, and dates. If any of them are empty, it warns you that adding them could be important — you can still generate anyway.

### Customizing the style

The **Style** tab covers the most common needs: sidebar background, section header color, item title color, text color, photo size, font sizes and sidebar width.

For full control, edit a copy of `cv_style.json` (every color, size, spacing, badge shape and the footer are configurable) and load it with **Import style JSON…**. Anything missing from your file falls back to the default. This is also how you use a **custom font**: put a TTF/OTF next to the exe and reference it under `"fonts"` (required for non-Latin alphabets):

```json
"fonts": {
  "heading": "MyFont",
  "body": "MyFont",
  "custom": { "MyFont": { "": "fonts/MyFont-Regular.ttf", "B": "fonts/MyFont-Bold.ttf", "I": "fonts/MyFont-Italic.ttf" } }
}
```

### Tutorial — adding certification badges

A badge is the small square image displayed next to a certification (the `badges/` folder contains four real examples).

1. **Get the image.** On [Credly](https://www.credly.com), open your badge page and download the badge as a PNG (or right-click → *Save image as…* on any certification site). Square images around 300×300 px look best.
2. **Store it.** Put the PNG in the `badges/` folder next to the exe (any folder works, but keeping them together means the CV still builds if you move the whole folder).
3. **Link it in the app.** In the **Certifications** tab, fill in the name, issuer and date, then press *Browse…* next to *Badge image* and select your PNG.
4. **Make it clickable (optional).** Paste the public URL of the badge (e.g. `https://www.credly.com/badges/…`) in the *Link URL* field — on the PDF, both the image and the small link icon next to the name will open it.
5. Generate. Badges are laid out automatically in a two-column grid.

**Image not square?** Press **Generate badge…** in the Certifications tab: pick any picture and the app center-crops it to a square, resizes it to 300×300 px, saves it as a PNG and links it to the form in one go. A quick reminder of all these steps is available behind the **Help** button on the same tab.

### Troubleshooting

- **Windows says "Windows protected your PC" (SmartScreen).** The exe is not code-signed. Click *More info* → *Run anyway*. If you prefer, run the open-source Python version instead.
- **Icons (GitHub, phone, whale…) missing from the PDF.** The `fonts/` folder must stay next to the exe.
- **Generation fails with an encoding error.** The built-in fonts only cover Latin alphabets — add a Unicode font via a custom style JSON (see above).
- **The photo looks stretched.** It never should: photos are center-cropped to a square automatically. Prefer a portrait where your face is centered.

### Credits

Open source: <https://github.com/In-Veritas/cv-generator> — whale icon by [Mayor Icons – Flaticon](https://www.flaticon.com/free-icons/whale), icons by [Font Awesome](https://fontawesome.com).

---

## Français

### Qu'est-ce que c'est ?

Une application de bureau qui crée un CV PDF professionnel en deux colonnes, compatible ATS, à partir d'un simple formulaire. Aucune installation ni Python requis — lancez simplement l'exécutable de votre plateforme.

**Contenu du dossier :**

| Fichier / dossier  | Rôle                                                                  |
| ------------------ | --------------------------------------------------------------------- |
| `CV-Generator.exe` / `CV-Generator` | L'application (Windows / Linux)                       |
| `cv_style.json`    | Le style par défaut (couleurs, polices, tailles) — modifiable ou importable dans l'application |
| `fonts/`           | Polices Font Awesome pour les icônes du CV (à garder à côté de l'exe)  |
| `badges/`          | Exemples d'images de badges de certification (Cisco, via Credly)       |
| `whale.png`        | Icône décorative du pied de page                                       |
| `app_icon.png` / `whale.ico` | Icônes de fenêtre et de barre des tâches (à garder à côté de l'exécutable) |
| `README.md`        | Ce fichier                                                             |

### Démarrage rapide

1. Décompressez le dossier où vous voulez (gardez les fichiers ensemble).
2. Double-cliquez sur `CV-Generator.exe`.
3. Choisissez votre langue — **Français, English, Español ou Português**. L'interface *et* les titres de sections imprimés sur le PDF (Formations, Compétences…) suivent ce choix. Modifiable ensuite dans le menu **Langue**.
4. Remplissez les onglets. Chaque zone de texte affiche une consigne grise expliquant quoi écrire — elle disparaît au clic.
   - **Personnel** : nom, sous-titre, photo (bouton *Parcourir…*, recadrée automatiquement en carré), objectif, à propos, coordonnées, liens GitHub/LinkedIn.
   - **Formations / Expériences** : remplissez le formulaire à droite puis *Ajouter*. Sélectionnez une entrée dans la liste pour la modifier — vos changements sont enregistrés automatiquement pendant la saisie. Cliquez de nouveau sur *Ajouter* pour vider le formulaire et commencer l'entrée suivante. Réordonnez avec *Monter/Descendre*. Dans les descriptions, commencez une ligne par `- ` pour obtenir une puce colorée.
   - **Compétences** : badges optionnels de la colonne latérale (séparés par des virgules) et catégories affichées en pastilles colorées dans la zone principale.
   - **Certifications** : nom, organisme, date, URL et image de badge optionnelle (voir le tutoriel ci-dessous).
   - **Style** : choisissez couleurs et tailles, ou importez un style JSON complet.
5. **Ordre des sections** : faites glisser les onglets Formations / Expériences / Compétences / Certifications pour les réordonner — le PDF imprime ses sections dans cet ordre exact. Le menu **Préréglages** propose deux dispositions prêtes à l'emploi : **Professionnel** (Expériences d'abord — par défaut) et **Académique** (Formations d'abord).
6. Cliquez sur **Générer le CV**, choisissez où enregistrer le PDF, c'est terminé.

> La petite baleine en bas à gauche ouvre la page GitHub du projet.

> **Astuce :** utilisez régulièrement **Fichier → Enregistrer les données (.json)…** pour ne jamais perdre votre travail. Rechargez-les via **Fichier → Charger les données (.json)…** — le fichier est entièrement compatible avec le générateur en ligne de commande open source.

### Linux et macOS

- **Linux** : le paquet Linux contient un binaire `CV-Generator` à la place du `.exe`. Depuis le dossier décompressé :
  ```bash
  chmod +x CV-Generator && ./CV-Generator
  ```
  Compilé sur Ubuntu 24.04 (x86-64) ; nécessite une session bureau. Sur d'autres distributions, ou si le binaire refuse de démarrer, utilisez le paquet source ci-dessous.
- **macOS** : pas d'application précompilée (les applications macOS ne peuvent être compilées que sur un Mac). Utilisez le **paquet source** — installez Python 3.9+ depuis [python.org](https://www.python.org), puis depuis le dossier décompressé :
  ```bash
  pip3 install -r requirements.txt
  python3 cv_gui.py
  ```
  C'est exactement la même application. Pour une vraie application double-cliquable, compilez-la sur votre Mac : `pip3 install pyinstaller` puis `pyinstaller --onefile --windowed --name CV-Generator cv_gui.py`.

### L'avertissement des champs manquants

Au moment de générer, l'application vérifie les champs que les ATS et outils d'IA des recruteurs analysent habituellement : nom, sous-titre, email, téléphone, objectif, à propos, formations, expériences, compétences et dates. Si certains sont vides, elle vous avertit qu'il pourrait être important de les remplir — vous pouvez tout de même générer.

### Personnaliser le style

L'onglet **Style** couvre les besoins courants : fond de la colonne latérale, couleur des titres de sections et des entrées, couleur du texte, taille de la photo, tailles de police et largeur de colonne.

Pour un contrôle total, modifiez une copie de `cv_style.json` (chaque couleur, taille, espacement, forme de badge et le pied de page sont configurables) puis chargez-la via **Importer un style JSON…**. Tout paramètre absent de votre fichier reprend la valeur par défaut. C'est aussi ainsi qu'on utilise une **police personnalisée** : placez un TTF/OTF à côté de l'exe et référencez-le sous `"fonts"` (indispensable pour les alphabets non latins) :

```json
"fonts": {
  "heading": "MaPolice",
  "body": "MaPolice",
  "custom": { "MaPolice": { "": "fonts/MaPolice-Regular.ttf", "B": "fonts/MaPolice-Bold.ttf", "I": "fonts/MaPolice-Italic.ttf" } }
}
```

### Tutoriel — ajouter des badges de certification

Un badge est la petite image carrée affichée à côté d'une certification (le dossier `badges/` contient quatre exemples réels).

1. **Récupérez l'image.** Sur [Credly](https://www.credly.com), ouvrez la page de votre badge et téléchargez-le en PNG (ou clic droit → *Enregistrer l'image sous…* sur n'importe quel site de certification). Une image carrée d'environ 300×300 px rend le mieux.
2. **Rangez-la.** Placez le PNG dans le dossier `badges/` à côté de l'exe (n'importe quel dossier fonctionne, mais tout garder ensemble permet de déplacer le dossier sans casser le CV).
3. **Liez-la dans l'application.** Dans l'onglet **Certifications**, remplissez nom, organisme et date, puis cliquez sur *Parcourir…* à côté d'*Image du badge* et sélectionnez votre PNG.
4. **Rendez-la cliquable (optionnel).** Collez l'URL publique du badge (ex. `https://www.credly.com/badges/…`) dans le champ *URL du lien* — sur le PDF, l'image et la petite icône de lien à côté du nom l'ouvriront.
5. Générez. Les badges se disposent automatiquement en grille de deux colonnes.

**Image pas carrée ?** Cliquez sur **Générer un badge…** dans l'onglet Certifications : choisissez n'importe quelle image et l'application la recadre en carré, la redimensionne en 300×300 px, l'enregistre en PNG et la lie au formulaire d'un seul coup. Un rappel de toutes ces étapes se trouve derrière le bouton **Aide** du même onglet.

### Dépannage

- **Windows affiche « Windows a protégé votre ordinateur » (SmartScreen).** L'exe n'est pas signé numériquement. Cliquez sur *Informations complémentaires* → *Exécuter quand même*. Sinon, utilisez la version Python open source.
- **Icônes (GitHub, téléphone, baleine…) absentes du PDF.** Le dossier `fonts/` doit rester à côté de l'exe.
- **La génération échoue avec une erreur d'encodage.** Les polices intégrées ne couvrent que les alphabets latins — ajoutez une police Unicode via un style JSON personnalisé (voir plus haut).
- **La photo paraît déformée.** Impossible normalement : elle est recadrée automatiquement en carré. Préférez un portrait où votre visage est centré.

### Crédits

Open source : <https://github.com/In-Veritas/cv-generator> — icône baleine par [Mayor Icons – Flaticon](https://www.flaticon.com/free-icons/whale), icônes par [Font Awesome](https://fontawesome.com).
