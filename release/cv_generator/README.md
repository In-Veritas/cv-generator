# CV Generator

A Python script that generates a professional two-column PDF CV from JSON configuration files. Designed with recruiter appeal, ATS (Applicant Tracking System) compatibility, and academic admissions optimization in mind. Every single aspect of it is configurable through parameters. Beginners can just change the `cv_data.json` file, and the tech savy should be able to meddle with the `cv_style.json` file or similar or `generate_cv.py` in order to make more refined changes. Nevertheless a tutorial can be found underneath. You can also change the language of the CV using `cv_lang.json` but a manual review of the translated text is recommended.

## Preview

![CV Preview](cv_preview.png)

## What It Can Be Used For

- **Master's degree applications** (MonMaster, university dossiers) — optimized for French academic admissions committees
- **Job applications** — ATS-compatible layout with high keyword detection rates
- **Freelance / professional profiles** — clean, modern design with clickable links
- **Multilingual CVs** — switch between French, English, Spanish, and Portuguese with a single config change

## How It Works

The generator reads three JSON files and produces a one-page A4 PDF:

1. **`cv_data.json`** — Your content (who you are, what you've done)
2. **`cv_style.json`** — How it looks (colors, fonts, sizes, spacing)
3. **`cv_lang.json`** — Section labels in your chosen language

The script uses `fpdf2` to render a two-column layout: a dark navy sidebar (30%) with personal info, photo, objective, and contact details, and a white main area (70%) with formations, experiences, skills, and certifications. All text in the main area is near-black on white for maximum ATS readability.

Descriptions support bullet points: lines starting with `-` are automatically rendered with indented colored bullet markers.

## Usage

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

### Changing Language

Edit `cv_lang.json` and set the `"lang"` field:

```json
{
  "lang": "en"
}
```

Available: `"fr"` (French), `"en"` (English), `"es"` (Spanish), `"pt"` (Portuguese).

This changes section headers (Formations, Experiences, Skills, Certifications) and the Objective box title. The content itself (descriptions, titles) must be translated manually in `cv_data.json`.

## File Structure

| File               | Purpose                                                                     |
| ------------------ | --------------------------------------------------------------------------- |
| `generate_cv.py`   | Main generator script (~800 lines)                                          |
| `cv_data.json`     | CV content (personal info, formations, experiences, skills, certifications) |
| `cv_style.json`    | Visual parameters (fonts, sizes, colors, spacing, badges, footer)           |
| `cv_lang.json`     | Language labels for section headers                                         |
| `fonts/`           | Font Awesome 7 OTF files for icons                                          |
| `badges/`          | Certification badge images (Credly)                                         |
| `requirements.txt` | Python dependencies (`fpdf2`)                                               |

## Features

### Two-Column Layout

The sidebar (30%) + main content (70%) layout is one of the most popular modern CV formats:

- Sidebar groups personal/contact info separately from professional content
- Recruiters can quickly locate contact details
- Main area gives ample space for experience descriptions
- ATS systems can parse the main content area reliably

### Font Awesome Icons

The generator auto-detects Font Awesome OTF/TTF files in the `fonts/` directory:

- **Social links** (GitHub, LinkedIn) — `fa-brands` font
- **Contact markers** (email, phone, address) — `fa-solid` font
- **Certification links** — clickable link icon next to each name
- **Footer decorations** — configurable left/right icons

Falls back gracefully to text-only rendering if fonts are not present.

### Certification Badges

Each certification can display its official badge image (e.g., from Credly) alongside the name and issuer. Badge images are clickable and link to the certification page.

### Bullet Point Formatting

Descriptions support a hybrid format — a context sentence followed by bullet points:

```json
"description": "Context sentence about the role.\n- First achievement or responsibility\n- Second achievement with quantified results\n- Third bullet point"
```

Lines starting with `-` are rendered with colored bullet markers and proper indentation.

### Photo Support

Supports JPG, JPEG, PNG, BMP, and GIF formats. If the exact filename is not found, the generator tries common extensions automatically.

### Colored Skill Badges

The skills section uses colored pill badges grouped by category, each with a distinct color from the blue family for visual cohesion.

## Customization

### Changing Content

Edit `cv_data.json`:

- `personal`: name, title, photo, objective, about, contact info, social links
- `formations`: education entries with bullet-point descriptions
- `experiences`: work experience entries with bullet-point descriptions
- `skills_section`: categorized skill badges (languages, programming, tools, soft skills)
- `certifications`: certification entries with optional URLs and badge images

### Changing Style

Edit `cv_style.json` to adjust any visual parameter:

- **Sidebar**: width ratio, background color, padding, photo size
- **Fonts**: heading/body families, custom TTF/OTF fonts
- **Font sizes**: every text element has its own configurable size
- **Colors**: every element has its own RGB color
- **Spacing**: gaps between every section, line height ratio
- **Badges**: padding, radius, gap, colors per style (filled/outlined/accent)
- **Skills section**: badge sizes, category colors
- **Certifications**: image size, grid layout, columns
- **Objective box**: background, border, title color, text color, padding, radius
- **Footer**: text, font size, color, icons, optional link URL and image

### Using Custom Fonts

Add TTF/OTF files and reference them in the style:

```json
"fonts": {
  "heading": "MyFont",
  "body": "MyFont",
  "custom": {
    "MyFont": {
      "": "fonts/MyFont-Regular.ttf",
      "B": "fonts/MyFont-Bold.ttf",
      "I": "fonts/MyFont-Italic.ttf"
    }
  }
}
```

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

## Footer Whale Icon

The small whale icon next to the footer link is a personal touch — it's my favourite animal. This is purely decorative and has no impact on ATS parsing (it lives in the sidebar, outside the main content area).

To remove it, clear the `image_right` field in `cv_style.json`:

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
