# CV Generator

**[Français](README.fr.md)** | **[Português](README.pt.md)** | **[Español](README.es.md)**

Build a professional, recruiter-friendly, ATS-compatible two-column PDF CV — either with a **desktop app** (fill a form, pick your colors, click Generate) or **manually** with Python and JSON configuration files. Designed with recruiter appeal, ATS (Applicant Tracking System) compatibility, and academic admissions optimization in mind.

## Preview

![CV Preview](cv_preview.png)

> **Note:** This very CV earned me a place in my new master's degree program — which is pretty cool.

## What It Can Be Used For

- **Master's degree applications** (MonMaster, university dossiers) — optimized for French academic admissions committees
- **Job applications** — ATS-compatible layout with high keyword detection rates
- **Freelance / professional profiles** — clean, modern design with clickable links
- **Multilingual CVs** — switch between French, English, Spanish, and Portuguese with a single click

## Two Ways to Use It

| | Desktop app (release) | Manual (Python + JSON) |
| --- | --- | --- |
| For | Everyone — no technical knowledge needed | Users who want to fine-tune everything |
| Requires | Nothing on Windows/Linux; Python on macOS | Python 3.9+ |
| Controls | Content, photo, colors, sizes, section order, badges | All of that plus every advanced style parameter |

## Using the Desktop App (recommended)

### Getting it

Download the latest package from the [Releases page](https://github.com/In-Veritas/cv-generator/releases) and unzip it:

- **Windows** (`…-win64.zip`): double-click `CV-Generator.exe`. If SmartScreen shows "Windows protected your PC", click *More info* → *Run anyway* (the exe is simply not code-signed).
- **Linux** (`…-linux-x64.tar.gz`): run `chmod +x CV-Generator && ./CV-Generator` from the unpacked folder.
- **macOS / any OS** (`…-source.zip`): install Python 3.9+, then `pip3 install -r requirements.txt` and `python3 cv_gui.py`.

Keep the unzipped files together — the app reads `fonts/`, `cv_style.json`, `whale.png` and `app_icon.png` from its own folder.

### Using it

1. **Pick a language** — Français, English, Español or Português. It sets both the interface and the section titles printed on the PDF, and can be changed anytime from the *Language* menu.
2. **Fill in the tabs.** Every text box shows a grey instruction explaining what to write. In the list tabs (Education, Experience, Skills, Certifications), press *Add* to append an entry; select an entry to edit it — changes are saved automatically as you type.
3. **Choose your section order.** Drag the section tabs to reorder them — the PDF prints its sections in that exact order. The *Presets* menu offers **Professional** (Experience first — the default) and **Academic** (Education first).
4. **Style it.** The *Style* tab has color pickers and size controls, plus an *Import style JSON…* button that loads a full `cv_style.json` (see the manual section below for everything it can contain).
5. **Add certification badges.** The Certifications tab has a *Help* button with a step-by-step guide and a *Generate badge…* tool that crops any picture to a square and resizes it to 300×300 px.
6. **Generate.** The app checks the fields that recruiters' ATS and AI screening tools usually parse (name, contact info, objective, entries, skills, dates) and warns you if any are empty — then produces the PDF wherever you choose.

Tips: **File → Save CV data (.json)** keeps your work reusable (the file is fully compatible with the command-line generator below), and the little whale in the bottom-left corner opens my GitHub page.

The complete app manual — including troubleshooting — ships inside every package and is also readable here: [release_readme.md](release_readme.md).

### Building the app yourself

```bash
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --windowed --name CV-Generator --icon whale.ico cv_gui.py
```

A GitHub Actions workflow (`.github/workflows/build-release.yml`) builds the Windows, Linux and macOS packages automatically on demand or when a `v*` tag is pushed.

## Manual Usage (Python + JSON)

For full control, drive the generator directly and edit the JSON files by hand.

```bash
pip install -r requirements.txt
python generate_cv.py
```

### Options

```bash
python generate_cv.py --data cv_data.json --style cv_style.json --lang cv_lang.json -o output.pdf
```

| Flag      | Default         | Description                 |
| --------- | --------------- | --------------------------- |
| `--data`  | `cv_data.json`  | Path to CV content          |
| `--style` | `cv_style.json` | Path to visual style config |
| `--lang`  | `cv_lang.json`  | Path to language labels     |
| `-o`      | `cv_output.pdf` | Output PDF path             |

### The three JSON files

1. **`cv_data.json`** — Your content (who you are, what you've done). `cv_data_fr.json` is the French version of my own data, usable with `--data`.
2. **`cv_style.json`** — How it looks (colors, fonts, sizes, spacing).
3. **`cv_lang.json`** — Section labels and the footer sub-text in your chosen language.

The generator uses `fpdf2` to render a two-column layout: a dark navy sidebar (30%) with personal info, photo, objective, and contact details, and a white main area (70%) with the four content sections. All text in the main area is near-black on white for maximum ATS readability.

### Changing the language

Edit `cv_lang.json` and set the `"lang"` field to `"fr"`, `"en"`, `"es"` or `"pt"`. This changes section headers, the Objective box title, and the footer sub-text. The content itself (descriptions, titles) must be translated manually in `cv_data.json`.

### Changing the section order

Add a `"section_order"` key to `cv_data.json` (default order shown):

```json
"section_order": ["formations", "experiences", "skills", "certifications"]
```

### Descriptions and bullet points

Descriptions support a hybrid format — a context sentence followed by bullet points. Lines starting with `-` are rendered with colored bullet markers and proper indentation:

```json
"description": "Context sentence about the role.\n- First achievement or responsibility\n- Second achievement with quantified results"
```

### Certification badges

Put the badge image (e.g. downloaded from Credly) in `badges/`, then reference it in the certification entry — the image and the small link icon are clickable when `url` is set:

```json
{ "name": "IT Essentials", "issuer": "Cisco", "date": "2021",
  "url": "https://www.credly.com/...", "image": "badges/it_essentials.png" }
```

### Custom fonts

Add TTF/OTF files and reference them in the style (required for non-Latin alphabets):

```json
"fonts": {
  "heading": "MyFont",
  "body": "MyFont",
  "custom": {
    "MyFont": { "": "fonts/MyFont-Regular.ttf", "B": "fonts/MyFont-Bold.ttf", "I": "fonts/MyFont-Italic.ttf" }
  }
}
```

### Everything `cv_style.json` controls

- **Sidebar**: width ratio, background color, padding, photo size
- **Fonts**: heading/body families, custom TTF/OTF fonts
- **Font sizes**: every text element has its own configurable size
- **Colors**: every element has its own RGB color
- **Spacing**: gaps between every section, line height ratio
- **Badges**: padding, radius, gap, colors per style (filled/outlined/accent)
- **Skills section**: badge sizes, category colors
- **Certifications**: image size, grid layout, columns
- **Objective box**: background, border, title color, text color, padding, radius
- **Footer**: texts, font size, color, icons, link URLs and image

## File Structure

| File | Purpose |
| --- | --- |
| `generate_cv.py` | PDF generator (command line) |
| `cv_gui.py` | Desktop app (form interface on top of the generator) |
| `cv_data.json` / `cv_data_fr.json` | CV content (English / French version) |
| `cv_style.json` | Visual parameters (fonts, sizes, colors, spacing, badges, footer) |
| `cv_lang.json` | Language labels for section headers and footer |
| `fonts/` | Font Awesome 7 OTF files for icons |
| `badges/` | Certification badge images (Credly) |
| `whale.png` / `app_icon.png` / `whale.ico` | Footer mascot, window icon, exe icon |
| `release_readme.md` | User guide shipped inside the release packages |
| `.github/workflows/build-release.yml` | CI builds for Windows, Linux and macOS |
| `requirements.txt` | Python dependencies (`fpdf2`, `pillow`) |

## Design Research

### Color Scheme

The color palette was chosen based on research from resume industry sources on what performs best with both human recruiters and ATS/AI screening tools.

**Why Navy Blue?**

- Blue is the #1 recommended resume color across all sources — signals trust, reliability, and competence
- Especially fitting for tech/IT since most major tech companies use blue branding
- Deep navy heading color (`#003366`) achieved a **98% ATS keyword detection rate** in testing

| Element            | Hex       | Rationale                                          |
| ------------------ | --------- | -------------------------------------------------- |
| Sidebar background | `#1B2A4A` | Contrast ratio with white text: ~12.5:1 (WCAG AAA) |
| Section headers    | `#003366` | 98% ATS keyword detection rate                     |
| Item titles        | `#0476D0` | Recommended for IT/tech resumes                    |
| Body text          | `#212121` | Contrast with white: ~16:1 (WCAG AAA)              |
| Secondary text     | `#555555` | Contrast with white: ~7.5:1 (WCAG AA)              |

### ATS Compatibility Rules

1. Body text is near-black on white — the "90-10 Rule"
2. All critical keywords are in the white main content area, not the sidebar
3. High contrast ratios (minimum 4.5:1 per WCAG AA) on every text-background pair
4. Cohesive 2-color palette (navy + blue accent) plus neutrals
5. Standard fonts (Helvetica) — universally parseable by ATS

### Description Formatting

Descriptions follow academic CV best practices for master's applications:

- Hybrid format: one context sentence + bullet points
- Action verbs in the infinitive (French convention)
- Quantified achievements where possible
- Keywords mirroring target program descriptions

## Footer

The footer at the bottom of the sidebar displays a text line with decorative icons and a clickable link to this repository.

**Dynamic text:** When the CV name is "Gabriel Vérité" (the author), the footer reads *"Générateur de CV de ma conception"*. For any other name, it automatically changes to *"generated with CV Generator by In Veritas"*, where **In Veritas** is a clickable link to my GitHub page. Configurable via `text`, `text_other`, `text_other_link_text` and `text_other_link_url` in `cv_style.json`.

**Localized sub-text:** the line under it ("available open-source") follows the CV language via the `footer_sub` key in `cv_lang.json`.

**Certification dates:** Each certification entry supports an optional `"date"` field displayed in small italic text below the issuer.

### Whale Icon

The small whale next to the footer link is a personal touch — it's my favourite animal. It's purely decorative and has no impact on ATS parsing (it lives in the sidebar, outside the main content area). The same whale is the app's window icon (`app_icon.png`) and, inside the app, a clickable mascot that opens my GitHub page.

To remove it from the CV, clear the `image_right` field in `cv_style.json`:

```json
"footer": {
  "image_right": "",
  ...
}
```

## Attribution

- <a href="https://www.flaticon.com/free-icons/whale" title="whale icons">Whale icons created by Mayor Icons - Flaticon</a>

## Sources

- [Resumly - Resume Color Scheme for ATS Compatibility & Readability](https://www.resumly.ai/blog/resume-color-scheme-for-ats-compatibility-and-readability)
- [AI ResumeGuru - Resume Colors: ATS-Safe Guide](https://airesume.guru/blog/resume-color-ats-safe-tips)
- [Resume.io - Best colors for a resume](https://resume.io/blog/should-you-use-color-on-your-resume)
- [Enhancv - How Does Color on a Resume Impact Your Chances?](https://enhancv.com/blog/color-on-resume/)
- [Jobscan - Should You Use Color on Your Resume?](https://www.jobscan.co/blog/best-color-for-resume/)
- [WebAIM - Contrast and Color Accessibility (WCAG 2)](https://webaim.org/articles/contrast/)
- [Mastersportal - 6 Steps to Writing an Awesome Academic CV](https://www.mastersportal.com/articles/2626/6-steps-to-writing-an-awesome-academic-cv-for-masters-application.html)
- [MakeMyCV - CV Master : Les clés pour séduire le jury](https://makemycv.com/fr/cv-master)
