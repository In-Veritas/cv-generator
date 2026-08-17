#!/usr/bin/env python3
"""
In:Veritas CV Generator — graphical interface.

A form-based UI to fill in CV content, customize the style (colors, sizes),
pick a photo, and generate the PDF. Supports French, English, Spanish and
Portuguese interfaces, importing a cv_style.json, and warns about empty
fields that ATS / AI screening tools rely on.

Usage:
    python cv_gui.py              # open the interface
    python cv_gui.py --selftest   # headless smoke test (generates a sample PDF)
"""

import copy
import json
import os
import subprocess
import sys
import webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser

from generate_cv import CVGenerator

try:
    from PIL import Image, ImageTk
    _HAS_PIL = True
except ImportError:
    _HAS_PIL = False

APP_NAME = "In:Veritas CV Generator"
WINDOW_TITLE = "CV Generator"
APP_VERSION = "1.0"
WHALE_TINT = (27, 42, 74)   # dark navy, matches the sidebar
BADGE_SIZE = 300
GITHUB_URL = "https://github.com/In-Veritas"
SECTION_KEYS = ("formations", "experiences", "skills", "certifications")
PRESETS = {
    "professional": ["experiences", "formations", "certifications", "skills"],
    "academic": ["formations", "experiences", "skills", "certifications"],
}
DEFAULT_PRESET = "professional"


def base_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


# ── CV section labels (printed on the PDF) ─────────────────────────────

CV_LABELS = {
    "fr": {"formations": "Formations", "experiences": "Expériences",
           "skills": "Compétences", "certifications": "Certifications",
           "objective": "Objectif", "footer_sub": "disponible en open-source"},
    "en": {"formations": "Education", "experiences": "Experience",
           "skills": "Skills", "certifications": "Certifications",
           "objective": "Objective", "footer_sub": "available open-source"},
    "es": {"formations": "Formación", "experiences": "Experiencia",
           "skills": "Competencias", "certifications": "Certificaciones",
           "objective": "Objetivo", "footer_sub": "disponible en código abierto"},
    "pt": {"formations": "Formação", "experiences": "Experiência",
           "skills": "Competências", "certifications": "Certificações",
           "objective": "Objetivo", "footer_sub": "disponível em código aberto"},
}

# ── default style (fallback if cv_style.json is absent next to the app) ─

EMBEDDED_STYLE = {
    "sidebar": {"width_ratio": 0.30, "bg_color": [27, 42, 74], "padding": 8,
                "top_margin": 12, "photo_size": 40},
    "main": {"padding": 10, "top_margin": 8},
    "fonts": {"heading": "Helvetica", "body": "Helvetica", "custom": {}},
    "font_sizes": {"name": 16, "subtitle": 12, "section_header": 15,
                   "item_title": 9.5, "item_subtitle": 8, "item_date": 7,
                   "item_description": 7.5, "about": 8.5, "contact_label": 8,
                   "contact_value": 8, "link": 9},
    "colors": {"sidebar_name": [255, 255, 255], "sidebar_title": [176, 190, 210],
               "sidebar_text": [210, 220, 235], "sidebar_link": [210, 220, 235],
               "section_header": [0, 51, 102], "section_underline": [0, 51, 102],
               "item_title": [4, 118, 208], "item_subtitle": [33, 33, 33],
               "item_date": [85, 85, 85], "text": [33, 33, 33]},
    "spacing": {"line_height_ratio": 0.40, "after_name": 1, "after_title": 3,
                "after_photo": 5, "after_tech_badges": 3, "after_lang_badges": 5,
                "after_links": 5, "after_objective": 5, "after_about": 5,
                "between_items": 2.5, "between_sections": 1.5},
    "badges": {"padding_x": 7, "padding_y": 2.5, "gap": 3, "font_size": 8,
               "radius": 2, "border_width": 0.4,
               "filled_bg": [255, 255, 255], "filled_text": [27, 42, 74],
               "outlined_bg": [40, 60, 100], "outlined_text": [255, 255, 255],
               "outlined_border": [120, 150, 200],
               "accent_bg": [4, 118, 208], "accent_text": [255, 255, 255]},
    "section_header": {"underline_thickness": 0.5, "gap_after": 2},
    "links": {"gap": 10, "icon_gap": 2},
    "contact": {"line_height": 4.2, "label_width": 7,
                "markers": {"email": {"icon": "", "font": "fa-solid", "text": "Mail"},
                            "phone": {"icon": "", "font": "fa-solid", "text": "Tel"},
                            "address": {"icon": "", "font": "fa-solid", "text": "Adr"}}},
    "certifications": {"columns": 2, "row_height": 13, "col_gap": 2,
                       "date_font_size": 6.5, "image_size": 10, "image_gap": 2,
                       "name_font_size": 9, "issuer_font_size": 8,
                       "link_icon": "", "link_icon_font": "fa-solid",
                       "link_icon_size": 7, "link_icon_color": [4, 118, 208]},
    "skills_section": {"category_font_size": 7.5, "badge_font_size": 6,
                       "badge_padding_x": 3.5, "badge_padding_y": 1.5,
                       "badge_gap": 1.5, "badge_radius": 2, "category_gap": 2,
                       "category_colors": [[0, 51, 102], [4, 118, 208],
                                           [0, 100, 130], [60, 85, 130]]},
    "objective": {"font_size": 8, "title_font_size": 9, "title": "Objectif",
                  "padding": 4, "radius": 2, "bg_color": [38, 58, 95],
                  "border_color": [60, 95, 150], "title_color": [120, 170, 230],
                  "text_color": [210, 225, 242]},
    "footer": {"font_size": 7.5, "color": [200, 215, 240],
               "icon_left": "", "icon_font": "fa-solid",
               "image_right": "whale.png", "image_size": 3.5,
               "text": "Générateur de CV de ma conception",
               "text_sub": "disponible en open-source",
               "text_other": "generated with CV Generator by In Veritas",
               "text_other_link_text": "In Veritas",
               "text_other_link_url": "https://github.com/In-Veritas",
               "link_url": "https://github.com/In-Veritas/cv-generator"},
}


def deep_merge(base, override):
    """Merge override into a deep copy of base (dicts merged, others replaced)."""
    out = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def open_in_viewer(path):
    """Open a file with the OS default application (Windows/macOS/Linux)."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        pass


def set_app_user_model_id():
    """Give the process its own Windows taskbar identity.

    Without this, the taskbar may group the app under a stale or generic
    identity and show a placeholder icon instead of the window's own icon.
    Must be called before the first window is created.
    """
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "InVeritas.CVGenerator")
        except Exception:
            pass


def set_window_icon(win):
    """Use the whale badge as the window icon instead of the default Tk feather.

    On Windows the multi-size whale.ico is applied with iconbitmap, which
    hands the shell a native HICON — the reliable path for both the title
    bar and the taskbar button (iconphoto's converted photos made some
    taskbars fall back to an empty placeholder). Other platforms get the
    app_icon.png badge through iconphoto.
    """
    if sys.platform.startswith("win"):
        ico = os.path.join(base_dir(), "whale.ico")
        if os.path.exists(ico):
            try:
                win.iconbitmap(default=ico)
                win._whale_icon = ico
                return
            except tk.TclError:
                pass
    path = os.path.join(base_dir(), "app_icon.png")
    if not os.path.exists(path):
        path = os.path.join(base_dir(), "whale.png")
    if not os.path.exists(path):
        return
    try:
        if _HAS_PIL:
            src = Image.open(path).convert("RGBA")
            imgs = [ImageTk.PhotoImage(src.resize((s, s), Image.LANCZOS), master=win)
                    for s in (16, 24, 32, 48, 64, 128)]
        else:
            imgs = [tk.PhotoImage(file=path, master=win)]
        win.iconphoto(True, *imgs)
        win._whale_icon = imgs
    except Exception:
        pass


def make_badge_image(src, dst, size=BADGE_SIZE):
    """Center-crop an image to a square and resize it to a badge-sized PNG."""
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    if side != size:
        img = img.resize((size, size), Image.LANCZOS)
    img.save(dst, "PNG")


def load_default_style():
    path = os.path.join(base_dir(), "cv_style.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return deep_merge(EMBEDDED_STYLE, json.load(f))
        except Exception:
            pass
    return copy.deepcopy(EMBEDDED_STYLE)


# ── interface translations ─────────────────────────────────────────────

TR = {
    "en": {
        "lang_name": "English",
        "choose_lang": "Choose your language",
        "tab_personal": "Personal", "tab_education": "Education",
        "tab_experience": "Experience", "tab_skills": "Skills",
        "tab_certifications": "Certifications", "tab_style": "Style",
        "menu_file": "File", "menu_load_data": "Load CV data (.json)...",
        "menu_save_data": "Save CV data (.json)...",
        "menu_import_style": "Import style (.json)...",
        "menu_reset_style": "Reset default style", "menu_exit": "Exit",
        "menu_language": "Language", "menu_help": "Help", "menu_about": "About",
        "menu_presets": "Presets", "preset_academic": "Academic",
        "preset_professional": "Professional",
        "lbl_name": "Full name", "lbl_title": "Headline",
        "lbl_photo": "Photo", "lbl_objective": "Objective",
        "lbl_about": "About me", "lbl_email": "Email", "lbl_phone": "Phone",
        "lbl_address": "Address", "lbl_github": "GitHub URL",
        "lbl_linkedin": "LinkedIn URL",
        "ph_name": "e.g. Marie Dupont",
        "ph_title": "Line under your name — e.g. Master's Applicant, Software Engineer",
        "ph_objective": "1–2 sentences stating your career goal — shown in a highlighted box",
        "ph_about": "A short paragraph about you: your passion, background and what you are looking for",
        "ph_email": "e.g. marie.dupont@mail.com",
        "ph_phone": "e.g. 0612345678",
        "ph_address": "One line per row: street, then postal code + city, then country",
        "ph_github": "e.g. https://github.com/username (leave empty to hide)",
        "ph_linkedin": "e.g. https://www.linkedin.com/in/username (leave empty to hide)",
        "btn_browse": "Browse...", "btn_add": "Add", "btn_update": "Update",
        "btn_remove": "Remove", "btn_up": "Up", "btn_down": "Down",
        "btn_generate": "Generate CV", "btn_import_style": "Import style JSON...",
        "btn_reset_style": "Reset default style", "btn_choose": "Choose...",
        "lbl_entries": "Entries (select one to edit)",
        "lbl_entry_title": "Title", "lbl_entry_subtitle": "Institution / Company",
        "lbl_entry_date": "Dates", "lbl_entry_desc": "Description",
        "ph_edu_title": "e.g. Bachelor's Degree in Computer Science",
        "ph_edu_subtitle": "e.g. Lyon 2 Lumière University",
        "ph_edu_date": "e.g. September 2022 to June 2025",
        "ph_exp_title": "e.g. Software Development Intern",
        "ph_exp_subtitle": "e.g. ACME Corp",
        "ph_exp_date": "e.g. April 2025 to June 2025",
        "ph_desc": "One context sentence, then one line per bullet starting with \"- \". Use action verbs and quantified results",
        "frm_sidebar_badges": "Sidebar badges (optional)",
        "lbl_tech_badges": "Technical badges", "lbl_lang_badges": "Language badges",
        "ph_tech_badges": "Comma-separated, e.g. Python, SQL, Git (shown under the photo)",
        "ph_lang_badges": "Comma-separated, e.g. French (native), English C1",
        "frm_skill_cats": "Skill categories (printed in the main area)",
        "lbl_skill_cat": "Category name", "lbl_skill_items": "Skills",
        "ph_skill_cat": "e.g. Programming Languages",
        "ph_skill_items": "Comma-separated, e.g. Python, Java, SQL",
        "btn_badge_help": "Help",
        "btn_make_badge": "Generate badge...",
        "badge_help_title": "How to add badges",
        "badge_help_text": "1. Download your badge image (e.g. on Credly, open your badge page and save the PNG).\n2. Keep it in the 'badges' folder next to the app so everything stays together.\n3. Fill in the certification fields, press Browse... and select the image.\n4. Paste the badge's public URL in 'Link URL' to make it clickable on the PDF.\n\nAny picture works: 'Generate badge...' crops it to a square and resizes it to 300\u00d7300 px for you.",
        "msg_badge_saved": "Badge image created and linked to the form:\n{path}",
        "lbl_cert_name": "Name", "lbl_cert_issuer": "Issuer",
        "lbl_cert_date": "Date", "lbl_cert_url": "Link URL",
        "lbl_cert_img": "Badge image",
        "ph_cert_name": "e.g. IT Essentials",
        "ph_cert_issuer": "e.g. Cisco Networking Academy",
        "ph_cert_date": "e.g. 2024",
        "ph_cert_url": "e.g. https://www.credly.com/... (leave empty for no link)",
        "frm_colors": "Colors", "frm_sizes": "Sizes",
        "color_sidebar": "Sidebar background", "color_header": "Section headers",
        "color_item": "Item titles", "color_text": "Body text",
        "size_photo": "Photo size (mm)", "size_name": "Name font size",
        "size_header": "Section header size", "size_body": "Body text size",
        "size_sidebar_w": "Sidebar width (%)",
        "style_hint": ("Colors and sizes below override the default style. "
                       "Use \"Import style JSON...\" to load a full cv_style.json "
                       "with every advanced parameter."),
        "msg_missing_title": "Possibly important fields are empty",
        "msg_missing_intro": ("The following fields are empty. Recruiters' ATS and AI "
                              "screening tools often rely on them, so it could be "
                              "important to add them:"),
        "msg_missing_outro": "Generate the CV anyway?",
        "f_education": "At least one education entry",
        "f_experience": "At least one experience entry",
        "f_skills": "At least one skill category",
        "f_dates": "Dates on some education/experience entries",
        "msg_done_title": "CV generated",
        "msg_done_body": "Your CV has been generated:\n{path}",
        "msg_open_pdf": "Open it now?",
        "msg_err_title": "Generation failed",
        "msg_err_body": ("The CV could not be generated. If you used characters "
                         "outside Latin scripts, add a Unicode font via a custom "
                         "style JSON (see README)."),
        "msg_style_loaded": "Style imported successfully.",
        "msg_style_reset": "Default style restored.",
        "msg_data_saved": "CV data saved:\n{path}",
        "msg_data_loaded": "CV data loaded.",
        "msg_invalid_json": "This file is not a valid JSON file.",
        "dlg_images": "Images", "dlg_json": "JSON files", "dlg_pdf": "PDF files",
        "about_text": (APP_NAME + " v" + APP_VERSION + "\n\n"
                       "Form-based CV builder producing an ATS-friendly two-column PDF.\n"
                       "Open source: https://github.com/In-Veritas/cv-generator"),
    },
    "fr": {
        "lang_name": "Français",
        "choose_lang": "Choisissez votre langue",
        "tab_personal": "Personnel", "tab_education": "Formations",
        "tab_experience": "Expériences", "tab_skills": "Compétences",
        "tab_certifications": "Certifications", "tab_style": "Style",
        "menu_file": "Fichier", "menu_load_data": "Charger les données (.json)...",
        "menu_save_data": "Enregistrer les données (.json)...",
        "menu_import_style": "Importer un style (.json)...",
        "menu_reset_style": "Rétablir le style par défaut", "menu_exit": "Quitter",
        "menu_language": "Langue", "menu_help": "Aide", "menu_about": "À propos",
        "menu_presets": "Préréglages", "preset_academic": "Académique",
        "preset_professional": "Professionnel",
        "lbl_name": "Nom complet", "lbl_title": "Sous-titre",
        "lbl_photo": "Photo", "lbl_objective": "Objectif",
        "lbl_about": "À propos de moi", "lbl_email": "Email", "lbl_phone": "Téléphone",
        "lbl_address": "Adresse", "lbl_github": "URL GitHub",
        "lbl_linkedin": "URL LinkedIn",
        "ph_name": "ex. Marie Dupont",
        "ph_title": "Ligne sous votre nom — ex. Candidature Master, Développeuse logiciel",
        "ph_objective": "1 à 2 phrases sur votre objectif professionnel — affiché dans un encadré",
        "ph_about": "Un court paragraphe sur vous : votre passion, votre parcours, ce que vous recherchez",
        "ph_email": "ex. marie.dupont@mail.com",
        "ph_phone": "ex. 0612345678",
        "ph_address": "Une ligne par rangée : rue, puis code postal + ville, puis pays",
        "ph_github": "ex. https://github.com/pseudo (laisser vide pour masquer)",
        "ph_linkedin": "ex. https://www.linkedin.com/in/pseudo (laisser vide pour masquer)",
        "btn_browse": "Parcourir...", "btn_add": "Ajouter", "btn_update": "Modifier",
        "btn_remove": "Supprimer", "btn_up": "Monter", "btn_down": "Descendre",
        "btn_generate": "Générer le CV", "btn_import_style": "Importer un style JSON...",
        "btn_reset_style": "Style par défaut", "btn_choose": "Choisir...",
        "lbl_entries": "Entrées (sélectionnez-en une pour la modifier)",
        "lbl_entry_title": "Intitulé", "lbl_entry_subtitle": "Établissement / Entreprise",
        "lbl_entry_date": "Dates", "lbl_entry_desc": "Description",
        "ph_edu_title": "ex. Licence Informatique",
        "ph_edu_subtitle": "ex. Université Lyon 2 Lumière",
        "ph_edu_date": "ex. Septembre 2022 à juin 2025",
        "ph_exp_title": "ex. Stagiaire en développement logiciel",
        "ph_exp_subtitle": "ex. ACME Corp",
        "ph_exp_date": "ex. Avril 2025 à juin 2025",
        "ph_desc": "Une phrase de contexte, puis une ligne par puce commençant par « - ». Verbes d'action et résultats chiffrés",
        "frm_sidebar_badges": "Badges de la colonne latérale (optionnel)",
        "lbl_tech_badges": "Badges techniques", "lbl_lang_badges": "Badges de langues",
        "ph_tech_badges": "Séparés par des virgules, ex. Python, SQL, Git (sous la photo)",
        "ph_lang_badges": "Séparés par des virgules, ex. Français (natif), Anglais C1",
        "frm_skill_cats": "Catégories de compétences (zone principale)",
        "lbl_skill_cat": "Nom de la catégorie", "lbl_skill_items": "Compétences",
        "ph_skill_cat": "ex. Langages de programmation",
        "ph_skill_items": "Séparées par des virgules, ex. Python, Java, SQL",
        "btn_badge_help": "Aide",
        "btn_make_badge": "Générer un badge...",
        "badge_help_title": "Comment ajouter des badges",
        "badge_help_text": "1. Téléchargez l'image de votre badge (ex. sur Credly, ouvrez la page du badge et enregistrez le PNG).\n2. Rangez-la dans le dossier « badges » à côté de l'application pour tout garder ensemble.\n3. Remplissez les champs de la certification, cliquez sur Parcourir... et sélectionnez l'image.\n4. Collez l'URL publique du badge dans « URL du lien » pour le rendre cliquable sur le PDF.\n\nN'importe quelle image convient : « Générer un badge... » la recadre en carré et la met en 300\u00d7300 px.",
        "msg_badge_saved": "Image de badge créée et liée au formulaire :\n{path}",
        "lbl_cert_name": "Nom", "lbl_cert_issuer": "Organisme",
        "lbl_cert_date": "Date", "lbl_cert_url": "URL du lien",
        "lbl_cert_img": "Image du badge",
        "ph_cert_name": "ex. IT Essentials",
        "ph_cert_issuer": "ex. Cisco Networking Academy",
        "ph_cert_date": "ex. 2024",
        "ph_cert_url": "ex. https://www.credly.com/... (vide = pas de lien)",
        "frm_colors": "Couleurs", "frm_sizes": "Tailles",
        "color_sidebar": "Fond de la colonne latérale", "color_header": "Titres de sections",
        "color_item": "Titres des entrées", "color_text": "Texte principal",
        "size_photo": "Taille de la photo (mm)", "size_name": "Taille du nom",
        "size_header": "Taille des titres de sections", "size_body": "Taille du texte",
        "size_sidebar_w": "Largeur de la colonne (%)",
        "style_hint": ("Les couleurs et tailles ci-dessous remplacent le style par défaut. "
                       "« Importer un style JSON... » permet de charger un cv_style.json "
                       "complet avec tous les paramètres avancés."),
        "msg_missing_title": "Des champs potentiellement importants sont vides",
        "msg_missing_intro": ("Les champs suivants sont vides. Les ATS et outils d'IA "
                              "des recruteurs s'appuient souvent dessus : il pourrait "
                              "être important de les remplir :"),
        "msg_missing_outro": "Générer le CV quand même ?",
        "f_education": "Au moins une formation",
        "f_experience": "Au moins une expérience",
        "f_skills": "Au moins une catégorie de compétences",
        "f_dates": "Les dates de certaines formations/expériences",
        "msg_done_title": "CV généré",
        "msg_done_body": "Votre CV a été généré :\n{path}",
        "msg_open_pdf": "L'ouvrir maintenant ?",
        "msg_err_title": "Échec de la génération",
        "msg_err_body": ("Le CV n'a pas pu être généré. Si vous avez utilisé des "
                         "caractères hors alphabet latin, ajoutez une police Unicode "
                         "via un style JSON personnalisé (voir README)."),
        "msg_style_loaded": "Style importé avec succès.",
        "msg_style_reset": "Style par défaut rétabli.",
        "msg_data_saved": "Données du CV enregistrées :\n{path}",
        "msg_data_loaded": "Données du CV chargées.",
        "msg_invalid_json": "Ce fichier n'est pas un fichier JSON valide.",
        "dlg_images": "Images", "dlg_json": "Fichiers JSON", "dlg_pdf": "Fichiers PDF",
        "about_text": (APP_NAME + " v" + APP_VERSION + "\n\n"
                       "Créateur de CV par formulaire produisant un PDF deux colonnes "
                       "compatible ATS.\nOpen source : https://github.com/In-Veritas/cv-generator"),
    },
    "es": {
        "lang_name": "Español",
        "choose_lang": "Elija su idioma",
        "tab_personal": "Personal", "tab_education": "Formación",
        "tab_experience": "Experiencia", "tab_skills": "Competencias",
        "tab_certifications": "Certificaciones", "tab_style": "Estilo",
        "menu_file": "Archivo", "menu_load_data": "Cargar datos del CV (.json)...",
        "menu_save_data": "Guardar datos del CV (.json)...",
        "menu_import_style": "Importar estilo (.json)...",
        "menu_reset_style": "Restablecer estilo por defecto", "menu_exit": "Salir",
        "menu_language": "Idioma", "menu_help": "Ayuda", "menu_about": "Acerca de",
        "menu_presets": "Preajustes", "preset_academic": "Académico",
        "preset_professional": "Profesional",
        "lbl_name": "Nombre completo", "lbl_title": "Subtítulo",
        "lbl_photo": "Foto", "lbl_objective": "Objetivo",
        "lbl_about": "Sobre mí", "lbl_email": "Email", "lbl_phone": "Teléfono",
        "lbl_address": "Dirección", "lbl_github": "URL de GitHub",
        "lbl_linkedin": "URL de LinkedIn",
        "ph_name": "ej. María López",
        "ph_title": "Línea bajo su nombre — ej. Candidatura a Máster, Ingeniera de software",
        "ph_objective": "1–2 frases con su objetivo profesional — se muestra en un recuadro",
        "ph_about": "Un párrafo corto sobre usted: su pasión, su trayectoria y lo que busca",
        "ph_email": "ej. maria.lopez@mail.com",
        "ph_phone": "ej. 612345678",
        "ph_address": "Una línea por fila: calle, luego código postal + ciudad, luego país",
        "ph_github": "ej. https://github.com/usuario (vacío para ocultar)",
        "ph_linkedin": "ej. https://www.linkedin.com/in/usuario (vacío para ocultar)",
        "btn_browse": "Examinar...", "btn_add": "Añadir", "btn_update": "Modificar",
        "btn_remove": "Eliminar", "btn_up": "Subir", "btn_down": "Bajar",
        "btn_generate": "Generar CV", "btn_import_style": "Importar estilo JSON...",
        "btn_reset_style": "Estilo por defecto", "btn_choose": "Elegir...",
        "lbl_entries": "Entradas (seleccione una para editarla)",
        "lbl_entry_title": "Título", "lbl_entry_subtitle": "Institución / Empresa",
        "lbl_entry_date": "Fechas", "lbl_entry_desc": "Descripción",
        "ph_edu_title": "ej. Grado en Informática",
        "ph_edu_subtitle": "ej. Universidad de Lyon 2",
        "ph_edu_date": "ej. Septiembre 2022 a junio 2025",
        "ph_exp_title": "ej. Prácticas en desarrollo de software",
        "ph_exp_subtitle": "ej. ACME Corp",
        "ph_exp_date": "ej. Abril 2025 a junio 2025",
        "ph_desc": "Una frase de contexto y una línea por viñeta empezando por \"- \". Verbos de acción y resultados cuantificados",
        "frm_sidebar_badges": "Insignias de la barra lateral (opcional)",
        "lbl_tech_badges": "Insignias técnicas", "lbl_lang_badges": "Insignias de idiomas",
        "ph_tech_badges": "Separadas por comas, ej. Python, SQL, Git (bajo la foto)",
        "ph_lang_badges": "Separadas por comas, ej. Español (nativo), Inglés C1",
        "frm_skill_cats": "Categorías de competencias (zona principal)",
        "lbl_skill_cat": "Nombre de la categoría", "lbl_skill_items": "Competencias",
        "ph_skill_cat": "ej. Lenguajes de programación",
        "ph_skill_items": "Separadas por comas, ej. Python, Java, SQL",
        "btn_badge_help": "Ayuda",
        "btn_make_badge": "Generar insignia...",
        "badge_help_title": "Cómo añadir insignias",
        "badge_help_text": "1. Descargue la imagen de su insignia (ej. en Credly, abra la página de la insignia y guarde el PNG).\n2. Guárdela en la carpeta 'badges' junto a la aplicación para mantener todo junto.\n3. Complete los campos de la certificación, pulse Examinar... y seleccione la imagen.\n4. Pegue la URL pública de la insignia en 'URL del enlace' para hacerla clicable en el PDF.\n\nCualquier imagen sirve: 'Generar insignia...' la recorta en cuadrado y la ajusta a 300\u00d7300 px.",
        "msg_badge_saved": "Imagen de insignia creada y vinculada al formulario:\n{path}",
        "lbl_cert_name": "Nombre", "lbl_cert_issuer": "Emisor",
        "lbl_cert_date": "Fecha", "lbl_cert_url": "URL del enlace",
        "lbl_cert_img": "Imagen de la insignia",
        "ph_cert_name": "ej. IT Essentials",
        "ph_cert_issuer": "ej. Cisco Networking Academy",
        "ph_cert_date": "ej. 2024",
        "ph_cert_url": "ej. https://www.credly.com/... (vacío = sin enlace)",
        "frm_colors": "Colores", "frm_sizes": "Tamaños",
        "color_sidebar": "Fondo de la barra lateral", "color_header": "Títulos de sección",
        "color_item": "Títulos de entradas", "color_text": "Texto principal",
        "size_photo": "Tamaño de la foto (mm)", "size_name": "Tamaño del nombre",
        "size_header": "Tamaño de títulos de sección", "size_body": "Tamaño del texto",
        "size_sidebar_w": "Ancho de la barra (%)",
        "style_hint": ("Los colores y tamaños siguientes sustituyen el estilo por defecto. "
                       "Use \"Importar estilo JSON...\" para cargar un cv_style.json "
                       "completo con todos los parámetros avanzados."),
        "msg_missing_title": "Hay campos posiblemente importantes vacíos",
        "msg_missing_intro": ("Los siguientes campos están vacíos. Los ATS y las "
                              "herramientas de IA de los reclutadores suelen usarlos, "
                              "por lo que podría ser importante completarlos:"),
        "msg_missing_outro": "¿Generar el CV de todos modos?",
        "f_education": "Al menos una formación",
        "f_experience": "Al menos una experiencia",
        "f_skills": "Al menos una categoría de competencias",
        "f_dates": "Las fechas de algunas formaciones/experiencias",
        "msg_done_title": "CV generado",
        "msg_done_body": "Su CV ha sido generado:\n{path}",
        "msg_open_pdf": "¿Abrirlo ahora?",
        "msg_err_title": "Error de generación",
        "msg_err_body": ("No se pudo generar el CV. Si usó caracteres fuera del "
                         "alfabeto latino, añada una fuente Unicode mediante un "
                         "estilo JSON personalizado (ver README)."),
        "msg_style_loaded": "Estilo importado correctamente.",
        "msg_style_reset": "Estilo por defecto restablecido.",
        "msg_data_saved": "Datos del CV guardados:\n{path}",
        "msg_data_loaded": "Datos del CV cargados.",
        "msg_invalid_json": "Este archivo no es un JSON válido.",
        "dlg_images": "Imágenes", "dlg_json": "Archivos JSON", "dlg_pdf": "Archivos PDF",
        "about_text": (APP_NAME + " v" + APP_VERSION + "\n\n"
                       "Creador de CV por formulario que produce un PDF de dos columnas "
                       "compatible con ATS.\nCódigo abierto: https://github.com/In-Veritas/cv-generator"),
    },
    "pt": {
        "lang_name": "Português",
        "choose_lang": "Escolha o seu idioma",
        "tab_personal": "Pessoal", "tab_education": "Formação",
        "tab_experience": "Experiência", "tab_skills": "Competências",
        "tab_certifications": "Certificações", "tab_style": "Estilo",
        "menu_file": "Arquivo", "menu_load_data": "Carregar dados do CV (.json)...",
        "menu_save_data": "Salvar dados do CV (.json)...",
        "menu_import_style": "Importar estilo (.json)...",
        "menu_reset_style": "Restaurar estilo padrão", "menu_exit": "Sair",
        "menu_language": "Idioma", "menu_help": "Ajuda", "menu_about": "Sobre",
        "menu_presets": "Predefinições", "preset_academic": "Acadêmico",
        "preset_professional": "Profissional",
        "lbl_name": "Nome completo", "lbl_title": "Subtítulo",
        "lbl_photo": "Foto", "lbl_objective": "Objetivo",
        "lbl_about": "Sobre mim", "lbl_email": "Email", "lbl_phone": "Telefone",
        "lbl_address": "Endereço", "lbl_github": "URL do GitHub",
        "lbl_linkedin": "URL do LinkedIn",
        "ph_name": "ex. Maria Silva",
        "ph_title": "Linha abaixo do seu nome — ex. Candidatura a Mestrado, Engenheira de software",
        "ph_objective": "1–2 frases com o seu objetivo profissional — exibido em um quadro destacado",
        "ph_about": "Um parágrafo curto sobre você: sua paixão, sua trajetória e o que procura",
        "ph_email": "ex. maria.silva@mail.com",
        "ph_phone": "ex. 11912345678",
        "ph_address": "Uma linha por fileira: rua, depois CEP + cidade, depois país",
        "ph_github": "ex. https://github.com/usuario (vazio para ocultar)",
        "ph_linkedin": "ex. https://www.linkedin.com/in/usuario (vazio para ocultar)",
        "btn_browse": "Procurar...", "btn_add": "Adicionar", "btn_update": "Modificar",
        "btn_remove": "Remover", "btn_up": "Subir", "btn_down": "Descer",
        "btn_generate": "Gerar CV", "btn_import_style": "Importar estilo JSON...",
        "btn_reset_style": "Estilo padrão", "btn_choose": "Escolher...",
        "lbl_entries": "Entradas (selecione uma para editar)",
        "lbl_entry_title": "Título", "lbl_entry_subtitle": "Instituição / Empresa",
        "lbl_entry_date": "Datas", "lbl_entry_desc": "Descrição",
        "ph_edu_title": "ex. Bacharelado em Ciência da Computação",
        "ph_edu_subtitle": "ex. Universidade de Lyon 2",
        "ph_edu_date": "ex. Setembro 2022 a junho 2025",
        "ph_exp_title": "ex. Estágio em desenvolvimento de software",
        "ph_exp_subtitle": "ex. ACME Corp",
        "ph_exp_date": "ex. Abril 2025 a junho 2025",
        "ph_desc": "Uma frase de contexto e uma linha por marcador começando com \"- \". Verbos de ação e resultados quantificados",
        "frm_sidebar_badges": "Selos da barra lateral (opcional)",
        "lbl_tech_badges": "Selos técnicos", "lbl_lang_badges": "Selos de idiomas",
        "ph_tech_badges": "Separados por vírgulas, ex. Python, SQL, Git (abaixo da foto)",
        "ph_lang_badges": "Separados por vírgulas, ex. Português (nativo), Inglês C1",
        "frm_skill_cats": "Categorias de competências (área principal)",
        "lbl_skill_cat": "Nome da categoria", "lbl_skill_items": "Competências",
        "ph_skill_cat": "ex. Linguagens de programação",
        "ph_skill_items": "Separadas por vírgulas, ex. Python, Java, SQL",
        "btn_badge_help": "Ajuda",
        "btn_make_badge": "Gerar selo...",
        "badge_help_title": "Como adicionar selos",
        "badge_help_text": "1. Baixe a imagem do seu selo (ex. no Credly, abra a página do selo e salve o PNG).\n2. Guarde-a na pasta 'badges' ao lado do aplicativo para manter tudo junto.\n3. Preencha os campos da certificação, clique em Procurar... e selecione a imagem.\n4. Cole a URL pública do selo em 'URL do link' para torná-lo clicável no PDF.\n\nQualquer imagem serve: 'Gerar selo...' recorta em quadrado e ajusta para 300\u00d7300 px.",
        "msg_badge_saved": "Imagem de selo criada e vinculada ao formulário:\n{path}",
        "lbl_cert_name": "Nome", "lbl_cert_issuer": "Emissor",
        "lbl_cert_date": "Data", "lbl_cert_url": "URL do link",
        "lbl_cert_img": "Imagem do selo",
        "ph_cert_name": "ex. IT Essentials",
        "ph_cert_issuer": "ex. Cisco Networking Academy",
        "ph_cert_date": "ex. 2024",
        "ph_cert_url": "ex. https://www.credly.com/... (vazio = sem link)",
        "frm_colors": "Cores", "frm_sizes": "Tamanhos",
        "color_sidebar": "Fundo da barra lateral", "color_header": "Títulos de seção",
        "color_item": "Títulos das entradas", "color_text": "Texto principal",
        "size_photo": "Tamanho da foto (mm)", "size_name": "Tamanho do nome",
        "size_header": "Tamanho dos títulos de seção", "size_body": "Tamanho do texto",
        "size_sidebar_w": "Largura da barra (%)",
        "style_hint": ("As cores e tamanhos abaixo substituem o estilo padrão. "
                       "Use \"Importar estilo JSON...\" para carregar um cv_style.json "
                       "completo com todos os parâmetros avançados."),
        "msg_missing_title": "Campos possivelmente importantes estão vazios",
        "msg_missing_intro": ("Os campos a seguir estão vazios. Os ATS e as ferramentas "
                              "de IA dos recrutadores costumam usá-los, então pode ser "
                              "importante preenchê-los:"),
        "msg_missing_outro": "Gerar o CV mesmo assim?",
        "f_education": "Pelo menos uma formação",
        "f_experience": "Pelo menos uma experiência",
        "f_skills": "Pelo menos uma categoria de competências",
        "f_dates": "As datas de algumas formações/experiências",
        "msg_done_title": "CV gerado",
        "msg_done_body": "Seu CV foi gerado:\n{path}",
        "msg_open_pdf": "Abrir agora?",
        "msg_err_title": "Falha na geração",
        "msg_err_body": ("Não foi possível gerar o CV. Se você usou caracteres fora "
                         "do alfabeto latino, adicione uma fonte Unicode por meio de "
                         "um estilo JSON personalizado (ver README)."),
        "msg_style_loaded": "Estilo importado com sucesso.",
        "msg_style_reset": "Estilo padrão restaurado.",
        "msg_data_saved": "Dados do CV salvos:\n{path}",
        "msg_data_loaded": "Dados do CV carregados.",
        "msg_invalid_json": "Este arquivo não é um JSON válido.",
        "dlg_images": "Imagens", "dlg_json": "Arquivos JSON", "dlg_pdf": "Arquivos PDF",
        "about_text": (APP_NAME + " v" + APP_VERSION + "\n\n"
                       "Criador de CV por formulário que produz um PDF de duas colunas "
                       "compatível com ATS.\nCódigo aberto: https://github.com/In-Veritas/cv-generator"),
    },
}

PLACEHOLDER_FG = "#8a8a8a"
NORMAL_FG = "#1a1a1a"


# ── widgets with instructional placeholder text ────────────────────────

class PlaceholderEntry(tk.Entry):

    def __init__(self, master, placeholder="", **kw):
        kw.setdefault("fg", NORMAL_FG)
        super().__init__(master, **kw)
        self.placeholder = placeholder
        self._showing_ph = False
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self._show_placeholder()

    def _show_placeholder(self):
        if not super().get():
            self._showing_ph = True
            self.config(fg=PLACEHOLDER_FG)
            self.insert(0, self.placeholder)

    def _on_focus_in(self, _):
        if self._showing_ph:
            self.delete(0, "end")
            self.config(fg=NORMAL_FG)
            self._showing_ph = False

    def _on_focus_out(self, _):
        if not super().get():
            self._show_placeholder()

    def get_value(self):
        return "" if self._showing_ph else super().get().strip()

    def set_value(self, value):
        self._showing_ph = False
        self.config(fg=NORMAL_FG)
        self.delete(0, "end")
        if value:
            self.insert(0, value)
        else:
            self._show_placeholder()


class PlaceholderText(tk.Text):

    def __init__(self, master, placeholder="", **kw):
        kw.setdefault("fg", NORMAL_FG)
        kw.setdefault("wrap", "word")
        kw.setdefault("undo", True)
        super().__init__(master, **kw)
        self.placeholder = placeholder
        self._showing_ph = False
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
        self._show_placeholder()

    def _content(self):
        return self.get("1.0", "end-1c")

    def _show_placeholder(self):
        if not self._content():
            self._showing_ph = True
            self.config(fg=PLACEHOLDER_FG)
            self.insert("1.0", self.placeholder)

    def _on_focus_in(self, _):
        if self._showing_ph:
            self.delete("1.0", "end")
            self.config(fg=NORMAL_FG)
            self._showing_ph = False

    def _on_focus_out(self, _):
        if not self._content():
            self._show_placeholder()

    def get_value(self):
        return "" if self._showing_ph else self._content().strip()

    def set_value(self, value):
        self._showing_ph = False
        self.config(fg=NORMAL_FG)
        self.delete("1.0", "end")
        if value:
            self.insert("1.0", value)
        else:
            self._show_placeholder()


# ── generic list editor (education, experience, certifications, skills) ─

class ListEditor(ttk.Frame):
    """A listbox of dict items plus an edit form with Add/Update/Remove."""

    def __init__(self, master, app, items, fields, display):
        super().__init__(master, padding=8)
        self.app = app
        self.items = items          # list of dicts, shared with app.model
        self.fields = fields        # [{key, label, ph, kind, height?}]
        self.display = display      # item dict -> listbox line
        t = app.t

        left = ttk.Frame(self)
        left.pack(side="left", fill="both", padx=(0, 10))
        ttk.Label(left, text=t["lbl_entries"]).pack(anchor="w")
        box_frame = ttk.Frame(left)
        box_frame.pack(fill="both", expand=True)
        self.listbox = tk.Listbox(box_frame, width=34, height=14, exportselection=False)
        sb = ttk.Scrollbar(box_frame, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=sb.set)
        self.listbox.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        move = ttk.Frame(left)
        move.pack(fill="x", pady=(4, 0))
        ttk.Button(move, text="↑ " + t["btn_up"], width=10,
                   command=lambda: self._move(-1)).pack(side="left", padx=(0, 4))
        ttk.Button(move, text="↓ " + t["btn_down"], width=10,
                   command=lambda: self._move(1)).pack(side="left")

        right = ttk.Frame(self)
        right.pack(side="left", fill="both", expand=True)
        self.widgets = {}
        for f in self.fields:
            ttk.Label(right, text=f["label"]).pack(anchor="w", pady=(4, 0))
            if f["kind"] == "text":
                w = PlaceholderText(right, placeholder=f["ph"], height=f.get("height", 5))
                w.pack(fill="both", expand=True)
            elif f["kind"] == "file":
                row = ttk.Frame(right)
                row.pack(fill="x")
                w = PlaceholderEntry(row, placeholder=f["ph"])
                w.pack(side="left", fill="x", expand=True)
                ttk.Button(row, text=t["btn_browse"],
                           command=lambda w=w, f=f: self._browse(w, f)).pack(side="left", padx=(4, 0))
            else:
                w = PlaceholderEntry(right, placeholder=f["ph"])
                w.pack(fill="x")
            self.widgets[f["key"]] = w
            # edits to a selected entry are saved automatically
            w.bind("<KeyRelease>", self._auto_apply, add="+")
            w.bind("<FocusOut>", self._auto_apply, add="+")

        btns = ttk.Frame(right)
        btns.pack(fill="x", pady=(8, 0))
        ttk.Button(btns, text=t["btn_add"], command=self._add).pack(side="left", padx=(0, 4))
        ttk.Button(btns, text=t["btn_remove"], command=self._remove).pack(side="left")

        self.refresh()

    def _browse(self, widget, field):
        t = self.app.t
        path = filedialog.askopenfilename(
            filetypes=[(t["dlg_images"], "*.png *.jpg *.jpeg *.bmp *.gif")])
        if path:
            widget.set_value(path)
            self._auto_apply()

    def _harvest_form(self):
        return {f["key"]: self.widgets[f["key"]].get_value() for f in self.fields}

    def _fill_form(self, item):
        for f in self.fields:
            self.widgets[f["key"]].set_value(item.get(f["key"], ""))

    def _selected_index(self):
        sel = self.listbox.curselection()
        return sel[0] if sel else None

    def _on_select(self, _):
        i = self._selected_index()
        if i is not None:
            self._fill_form(self.items[i])

    def _auto_apply(self, _event=None):
        """Write the form into the selected entry as the user types."""
        i = self._selected_index()
        if i is None:
            return
        item = self._harvest_form()
        if item == self.items[i]:
            return
        self.items[i] = item
        self.listbox.delete(i)
        self.listbox.insert(i, self.display(item))
        self.listbox.selection_set(i)

    def _add(self):
        if self._selected_index() is not None:
            # an entry is selected (edits already saved automatically):
            # deselect and clear the form so a fresh entry can be typed
            self.listbox.selection_clear(0, "end")
            for f in self.fields:
                self.widgets[f["key"]].set_value("")
            return
        item = self._harvest_form()
        if not any(item.values()):
            return
        self.items.append(item)
        self.refresh()
        for f in self.fields:
            self.widgets[f["key"]].set_value("")

    def _remove(self):
        i = self._selected_index()
        if i is None:
            return
        del self.items[i]
        self.refresh()
        for f in self.fields:
            self.widgets[f["key"]].set_value("")

    def _move(self, delta):
        i = self._selected_index()
        if i is None:
            return
        j = i + delta
        if not (0 <= j < len(self.items)):
            return
        self.items[i], self.items[j] = self.items[j], self.items[i]
        self.refresh(select=j)

    def refresh(self, select=None):
        self.listbox.delete(0, "end")
        for it in self.items:
            self.listbox.insert("end", self.display(it))
        if select is not None:
            self.listbox.selection_set(select)
            self.listbox.see(select)


# ── main application ───────────────────────────────────────────────────

def empty_model():
    return {
        "name": "", "title": "", "photo": "", "objective": "", "about": "",
        "email": "", "phone": "", "address": "", "github": "", "linkedin": "",
        "tech_badges": "", "lang_badges": "",
        "formations": [], "experiences": [], "skill_cats": [], "certifications": [],
    }


class CVApp(tk.Tk):

    def __init__(self, lang="en"):
        super().__init__()
        self.lang = lang
        self.model = empty_model()
        self.style_dict = load_default_style()
        self.section_order = list(PRESETS[DEFAULT_PRESET])
        try:
            ttk.Style(self).theme_use("vista")
        except tk.TclError:
            pass
        self.minsize(860, 640)
        set_window_icon(self)
        self._build_ui()

    @property
    def t(self):
        return TR[self.lang]

    # ── UI construction ────────────────────────────────────────────────

    def _build_ui(self):
        t = self.t
        self.title(WINDOW_TITLE)
        self._build_menu()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=8, pady=(8, 0))

        # Personal is always first and Style always last; the four section
        # tabs are created in self.section_order and can be dragged around.
        self._tab_keys = {}
        builders = {"formations": self._build_education_tab,
                    "experiences": self._build_experience_tab,
                    "skills": self._build_skills_tab,
                    "certifications": self._build_certifications_tab}
        self._build_personal_tab()
        for key in self.section_order:
            self._tab_keys[str(builders[key]())] = key
        self._build_style_tab()
        self._drag_tab = None
        self.notebook.bind("<ButtonPress-1>", self._tab_press)
        self.notebook.bind("<B1-Motion>", self._tab_drag)

        bottom = ttk.Frame(self, padding=8)
        bottom.pack(fill="x")
        self._add_whale(bottom)
        gen = ttk.Button(bottom, text="⚙  " + t["btn_generate"], command=self.on_generate)
        gen.pack(side="right")

    # ── tab reordering (drag a section tab to move it) ─────────────────

    def _movable(self, index):
        return 0 < index < self.notebook.index("end") - 1

    def _tab_press(self, event):
        try:
            i = self.notebook.index(f"@{event.x},{event.y}")
        except tk.TclError:
            self._drag_tab = None
            return
        self._drag_tab = i if self._movable(i) else None

    def _tab_drag(self, event):
        if self._drag_tab is None:
            return
        try:
            target = self.notebook.index(f"@{event.x},{event.y}")
        except tk.TclError:
            return
        if target == self._drag_tab or not self._movable(target):
            return
        self.notebook.insert(target, self.notebook.tabs()[self._drag_tab])
        self._drag_tab = target
        self._sync_order_from_tabs()

    def _sync_order_from_tabs(self):
        self.section_order = [self._tab_keys[w] for w in self.notebook.tabs()
                              if w in self._tab_keys]
        self.preset_var.set(self._preset_name())

    def _preset_name(self):
        for name, order in PRESETS.items():
            if list(self.section_order) == order:
                return name
        return ""

    def apply_preset(self, name):
        self.section_order = list(PRESETS[name])
        self._apply_tab_order()
        self.preset_var.set(name)

    def _apply_tab_order(self):
        widgets = {key: w for w, key in self._tab_keys.items()}
        for pos, key in enumerate(self.section_order, start=1):
            self.notebook.insert(pos, widgets[key])

    def _add_whale(self, parent):
        """Dark-blue whale mascot in the bottom-left corner, visible on every tab."""
        path = os.path.join(base_dir(), "whale.png")
        if not _HAS_PIL or not os.path.exists(path):
            return
        try:
            img = Image.open(path).convert("RGBA").resize((26, 26), Image.LANCZOS)
            tinted = Image.new("RGBA", img.size, WHALE_TINT + (0,))
            tinted.putalpha(img.getchannel("A"))
            self._whale_img = ImageTk.PhotoImage(tinted)
            lbl = ttk.Label(parent, image=self._whale_img, cursor="hand2")
            lbl.pack(side="left")
            lbl.bind("<Button-1>", lambda _e: webbrowser.open(GITHUB_URL))
        except Exception:
            pass

    def _build_menu(self):
        t = self.t
        menubar = tk.Menu(self)

        m_file = tk.Menu(menubar, tearoff=0)
        m_file.add_command(label=t["menu_load_data"], command=self.load_data)
        m_file.add_command(label=t["menu_save_data"], command=self.save_data)
        m_file.add_separator()
        m_file.add_command(label=t["menu_import_style"], command=self.import_style)
        m_file.add_command(label=t["menu_reset_style"], command=self.reset_style)
        m_file.add_separator()
        m_file.add_command(label=t["menu_exit"], command=self.destroy)
        menubar.add_cascade(label=t["menu_file"], menu=m_file)

        self.preset_var = tk.StringVar(self, value=self._preset_name())
        m_preset = tk.Menu(menubar, tearoff=0)
        for name in ("professional", "academic"):
            m_preset.add_radiobutton(label=t["preset_" + name], value=name,
                                     variable=self.preset_var,
                                     command=lambda n=name: self.apply_preset(n))
        menubar.add_cascade(label=t["menu_presets"], menu=m_preset)

        m_lang = tk.Menu(menubar, tearoff=0)
        for code in ("fr", "en", "es", "pt"):
            m_lang.add_command(label=TR[code]["lang_name"],
                               command=lambda c=code: self.change_language(c))
        menubar.add_cascade(label=t["menu_language"], menu=m_lang)

        m_help = tk.Menu(menubar, tearoff=0)
        m_help.add_command(label=t["menu_about"],
                           command=lambda: messagebox.showinfo(t["menu_about"], t["about_text"]))
        menubar.add_cascade(label=t["menu_help"], menu=m_help)

        self.config(menu=menubar)

    def _build_personal_tab(self):
        t = self.t
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text=t["tab_personal"])
        tab.columnconfigure(1, weight=1)
        self.p_widgets = {}

        def row(r, key, label_key, ph_key, kind="entry", height=3):
            ttk.Label(tab, text=t[label_key]).grid(row=r, column=0, sticky="nw",
                                                   padx=(0, 8), pady=3)
            if kind == "text":
                w = PlaceholderText(tab, placeholder=t[ph_key], height=height)
                w.grid(row=r, column=1, sticky="nsew", pady=3)
            else:
                w = PlaceholderEntry(tab, placeholder=t[ph_key])
                w.grid(row=r, column=1, sticky="ew", pady=3)
            self.p_widgets[key] = w

        row(0, "name", "lbl_name", "ph_name")
        row(1, "title", "lbl_title", "ph_title")

        # photo picker
        ttk.Label(tab, text=t["lbl_photo"]).grid(row=2, column=0, sticky="nw",
                                                 padx=(0, 8), pady=3)
        photo_row = ttk.Frame(tab)
        photo_row.grid(row=2, column=1, sticky="ew", pady=3)
        w = PlaceholderEntry(photo_row, placeholder=t["btn_browse"])
        w.pack(side="left", fill="x", expand=True)
        ttk.Button(photo_row, text=t["btn_browse"], command=self._pick_photo).pack(
            side="left", padx=(4, 0))
        self.p_widgets["photo"] = w

        row(3, "objective", "lbl_objective", "ph_objective", kind="text", height=3)
        row(4, "about", "lbl_about", "ph_about", kind="text", height=5)
        row(5, "email", "lbl_email", "ph_email")
        row(6, "phone", "lbl_phone", "ph_phone")
        row(7, "address", "lbl_address", "ph_address", kind="text", height=3)
        row(8, "github", "lbl_github", "ph_github")
        row(9, "linkedin", "lbl_linkedin", "ph_linkedin")
        tab.rowconfigure(4, weight=1)

    def _pick_photo(self):
        t = self.t
        path = filedialog.askopenfilename(
            filetypes=[(t["dlg_images"], "*.png *.jpg *.jpeg *.bmp *.gif")])
        if path:
            self.p_widgets["photo"].set_value(path)

    def _build_education_tab(self):
        t = self.t
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=t["tab_education"])
        self.edu_editor = ListEditor(
            tab, self, self.model["formations"],
            fields=[
                {"key": "title", "label": t["lbl_entry_title"], "ph": t["ph_edu_title"], "kind": "entry"},
                {"key": "subtitle", "label": t["lbl_entry_subtitle"], "ph": t["ph_edu_subtitle"], "kind": "entry"},
                {"key": "date", "label": t["lbl_entry_date"], "ph": t["ph_edu_date"], "kind": "entry"},
                {"key": "description", "label": t["lbl_entry_desc"], "ph": t["ph_desc"], "kind": "text", "height": 6},
            ],
            display=lambda it: it.get("title", "") or "—")
        self.edu_editor.pack(fill="both", expand=True)
        return tab

    def _build_experience_tab(self):
        t = self.t
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=t["tab_experience"])
        self.exp_editor = ListEditor(
            tab, self, self.model["experiences"],
            fields=[
                {"key": "title", "label": t["lbl_entry_title"], "ph": t["ph_exp_title"], "kind": "entry"},
                {"key": "subtitle", "label": t["lbl_entry_subtitle"], "ph": t["ph_exp_subtitle"], "kind": "entry"},
                {"key": "date", "label": t["lbl_entry_date"], "ph": t["ph_exp_date"], "kind": "entry"},
                {"key": "description", "label": t["lbl_entry_desc"], "ph": t["ph_desc"], "kind": "text", "height": 6},
            ],
            display=lambda it: it.get("title", "") or "—")
        self.exp_editor.pack(fill="both", expand=True)
        return tab

    def _build_skills_tab(self):
        t = self.t
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text=t["tab_skills"])

        side = ttk.LabelFrame(tab, text=t["frm_sidebar_badges"], padding=8)
        side.pack(fill="x")
        side.columnconfigure(1, weight=1)
        ttk.Label(side, text=t["lbl_tech_badges"]).grid(row=0, column=0, sticky="w",
                                                        padx=(0, 8), pady=3)
        self.w_tech = PlaceholderEntry(side, placeholder=t["ph_tech_badges"])
        self.w_tech.grid(row=0, column=1, sticky="ew", pady=3)
        ttk.Label(side, text=t["lbl_lang_badges"]).grid(row=1, column=0, sticky="w",
                                                        padx=(0, 8), pady=3)
        self.w_langb = PlaceholderEntry(side, placeholder=t["ph_lang_badges"])
        self.w_langb.grid(row=1, column=1, sticky="ew", pady=3)

        cats = ttk.LabelFrame(tab, text=t["frm_skill_cats"], padding=0)
        cats.pack(fill="both", expand=True, pady=(10, 0))
        self.skill_editor = ListEditor(
            cats, self, self.model["skill_cats"],
            fields=[
                {"key": "category", "label": t["lbl_skill_cat"], "ph": t["ph_skill_cat"], "kind": "entry"},
                {"key": "items", "label": t["lbl_skill_items"], "ph": t["ph_skill_items"], "kind": "text", "height": 3},
            ],
            display=lambda it: it.get("category", "") or "—")
        self.skill_editor.pack(fill="both", expand=True)
        return tab

    def _build_certifications_tab(self):
        t = self.t
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=t["tab_certifications"])
        self.cert_editor = ListEditor(
            tab, self, self.model["certifications"],
            fields=[
                {"key": "name", "label": t["lbl_cert_name"], "ph": t["ph_cert_name"], "kind": "entry"},
                {"key": "issuer", "label": t["lbl_cert_issuer"], "ph": t["ph_cert_issuer"], "kind": "entry"},
                {"key": "date", "label": t["lbl_cert_date"], "ph": t["ph_cert_date"], "kind": "entry"},
                {"key": "url", "label": t["lbl_cert_url"], "ph": t["ph_cert_url"], "kind": "entry"},
                {"key": "image", "label": t["lbl_cert_img"], "ph": t["btn_browse"], "kind": "file"},
            ],
            display=lambda it: it.get("name", "") or "—")
        self.cert_editor.pack(fill="both", expand=True)

        bar = ttk.Frame(tab, padding=(8, 0, 8, 8))
        bar.pack(fill="x")
        ttk.Button(bar, text="🛈  " + t["btn_badge_help"],
                   command=self._show_badge_help).pack(side="left")
        ttk.Button(bar, text=t["btn_make_badge"],
                   command=self._generate_badge).pack(side="left", padx=(6, 0))
        return tab

    def _show_badge_help(self):
        t = self.t
        messagebox.showinfo(t["badge_help_title"], t["badge_help_text"])

    def _generate_badge(self):
        t = self.t
        src = filedialog.askopenfilename(
            filetypes=[(t["dlg_images"], "*.png *.jpg *.jpeg *.bmp *.gif")])
        if not src:
            return
        badges_dir = os.path.join(base_dir(), "badges")
        initial = os.path.splitext(os.path.basename(src))[0] + "_badge.png"
        dst = filedialog.asksaveasfilename(
            defaultextension=".png", initialfile=initial,
            initialdir=badges_dir if os.path.isdir(badges_dir) else None,
            filetypes=[("PNG", "*.png")])
        if not dst:
            return
        try:
            make_badge_image(src, dst)
        except Exception as exc:
            messagebox.showerror(t["msg_err_title"],
                                 f"[{type(exc).__name__}] {exc}")
            return
        self.cert_editor.widgets["image"].set_value(dst)
        messagebox.showinfo(WINDOW_TITLE, t["msg_badge_saved"].format(path=dst))

    # style tab: color pickers write straight into self.style_dict; sizes
    # are held in DoubleVars and applied at generation time.
    STYLE_COLORS = [
        ("color_sidebar", [("sidebar", "bg_color")]),
        ("color_header", [("colors", "section_header"), ("colors", "section_underline")]),
        ("color_item", [("colors", "item_title"), ("certifications", "link_icon_color")]),
        ("color_text", [("colors", "text"), ("colors", "item_subtitle")]),
    ]
    STYLE_SIZES = [
        ("size_photo", ("sidebar", "photo_size"), 20, 60, 1),
        ("size_name", ("font_sizes", "name"), 10, 24, 0.5),
        ("size_header", ("font_sizes", "section_header"), 10, 20, 0.5),
        ("size_body", ("font_sizes", "item_description"), 6, 11, 0.5),
        ("size_sidebar_w", ("sidebar", "width_ratio"), 20, 40, 1),
    ]

    def _build_style_tab(self):
        t = self.t
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text=t["tab_style"])

        ttk.Label(tab, text=t["style_hint"], wraplength=760, foreground="#555").pack(
            anchor="w", pady=(0, 8))

        colors = ttk.LabelFrame(tab, text=t["frm_colors"], padding=8)
        colors.pack(fill="x")
        self.color_buttons = {}
        for i, (label_key, paths) in enumerate(self.STYLE_COLORS):
            ttk.Label(colors, text=t[label_key]).grid(row=i, column=0, sticky="w",
                                                      padx=(0, 10), pady=3)
            btn = tk.Button(colors, text=t["btn_choose"], width=14,
                            command=lambda lk=label_key: self._pick_color(lk))
            btn.grid(row=i, column=1, sticky="w", pady=3)
            self.color_buttons[label_key] = btn

        sizes = ttk.LabelFrame(tab, text=t["frm_sizes"], padding=8)
        sizes.pack(fill="x", pady=(10, 0))
        self.size_vars = {}
        for i, (label_key, path, lo, hi, step) in enumerate(self.STYLE_SIZES):
            ttk.Label(sizes, text=t[label_key]).grid(row=i, column=0, sticky="w",
                                                     padx=(0, 10), pady=3)
            var = tk.DoubleVar()
            ttk.Spinbox(sizes, from_=lo, to=hi, increment=step, textvariable=var,
                        width=8).grid(row=i, column=1, sticky="w", pady=3)
            self.size_vars[label_key] = var

        btns = ttk.Frame(tab)
        btns.pack(fill="x", pady=(12, 0))
        ttk.Button(btns, text=t["btn_import_style"], command=self.import_style).pack(
            side="left", padx=(0, 6))
        ttk.Button(btns, text=t["btn_reset_style"], command=self.reset_style).pack(side="left")

        self._refresh_style_controls()

    def _style_get(self, path):
        node = self.style_dict
        for k in path[:-1]:
            node = node.setdefault(k, {})
        return node.get(path[-1])

    def _style_set(self, path, value):
        node = self.style_dict
        for k in path[:-1]:
            node = node.setdefault(k, {})
        node[path[-1]] = value

    def _refresh_style_controls(self):
        for label_key, paths in self.STYLE_COLORS:
            rgb = self._style_get(paths[0]) or [0, 0, 0]
            self._paint_color_button(label_key, rgb)
        for label_key, path, lo, hi, step in self.STYLE_SIZES:
            val = self._style_get(path)
            if label_key == "size_sidebar_w":
                val = round((val or 0.30) * 100)
            self.size_vars[label_key].set(val)

    def _paint_color_button(self, label_key, rgb):
        r, g, b = (int(c) for c in rgb)
        hexc = f"#{r:02x}{g:02x}{b:02x}"
        fg = "#ffffff" if (r * 299 + g * 587 + b * 114) / 1000 < 128 else "#000000"
        self.color_buttons[label_key].config(bg=hexc, fg=fg, activebackground=hexc)

    def _pick_color(self, label_key):
        paths = dict(self.STYLE_COLORS)[label_key]
        current = self._style_get(paths[0]) or [0, 0, 0]
        r, g, b = (int(c) for c in current)
        rgb, _ = colorchooser.askcolor(color=f"#{r:02x}{g:02x}{b:02x}", parent=self)
        if rgb is None:
            return
        rgb = [int(round(c)) for c in rgb]
        for p in paths:
            self._style_set(p, rgb)
        self._paint_color_button(label_key, rgb)

    def _apply_size_vars(self):
        for label_key, path, lo, hi, step in self.STYLE_SIZES:
            try:
                val = float(self.size_vars[label_key].get())
            except (tk.TclError, ValueError):
                continue
            val = max(lo, min(hi, val))
            if label_key == "size_sidebar_w":
                val = val / 100.0
            self._style_set(path, val)

    # ── model <-> widgets ──────────────────────────────────────────────

    def harvest(self):
        m = self.model
        for key, w in self.p_widgets.items():
            m[key] = w.get_value()
        m["tech_badges"] = self.w_tech.get_value()
        m["lang_badges"] = self.w_langb.get_value()
        # list editors mutate the model lists directly
        self._apply_size_vars()

    def populate(self):
        m = self.model
        for key, w in self.p_widgets.items():
            w.set_value(m.get(key, ""))
        self.w_tech.set_value(m.get("tech_badges", ""))
        self.w_langb.set_value(m.get("lang_badges", ""))
        self.edu_editor.refresh()
        self.exp_editor.refresh()
        self.skill_editor.refresh()
        self.cert_editor.refresh()
        self._refresh_style_controls()

    def change_language(self, code):
        if code == self.lang:
            return
        self.harvest()
        self.lang = code
        for w in self.winfo_children():
            w.destroy()
        self.config(menu="")
        self._build_ui()
        self.populate()

    # ── data mapping (model <-> cv_data.json format) ───────────────────

    @staticmethod
    def _csv(text):
        return [s.strip() for s in text.replace("\n", ",").split(",") if s.strip()]

    def build_data(self):
        m = self.model
        links = []
        if m["github"]:
            links.append({"label": "Github", "icon": "",
                          "icon_font": "fa-brands", "url": m["github"]})
        if m["linkedin"]:
            links.append({"label": "LinkedIn", "icon": "",
                          "icon_font": "fa-brands", "url": m["linkedin"]})
        address = [ln.strip() for ln in m["address"].splitlines() if ln.strip()]
        certs = []
        for c in m["certifications"]:
            cert = {"name": c.get("name", ""), "issuer": c.get("issuer", "")}
            if c.get("date"):
                cert["date"] = c["date"]
            if c.get("url"):
                cert["url"] = c["url"]
            if c.get("image"):
                cert["image"] = c["image"]
            certs.append(cert)
        return {
            "personal": {
                "name": m["name"], "title": m["title"], "photo": m["photo"],
                "objective": m["objective"], "about": m["about"],
                "contact": {"email": m["email"], "phone": m["phone"],
                            "address": address},
                "links": links,
            },
            "skills": {"technical": self._csv(m["tech_badges"]),
                       "languages": [{"name": s, "style": "accent"}
                                     for s in self._csv(m["lang_badges"])]},
            "formations": copy.deepcopy(m["formations"]),
            "experiences": copy.deepcopy(m["experiences"]),
            "skills_section": [{"category": c.get("category", ""),
                                "items": self._csv(c.get("items", ""))}
                               for c in m["skill_cats"]],
            "certifications": certs,
            "section_order": list(self.section_order),
        }

    def apply_data(self, data):
        m = empty_model()
        p = data.get("personal", {})
        m["name"] = p.get("name", "")
        m["title"] = p.get("title", "")
        photo = p.get("photo", "")
        if photo and not os.path.isabs(photo):
            candidate = os.path.join(base_dir(), photo)
            photo = candidate if os.path.exists(candidate) else photo
        m["photo"] = photo
        m["objective"] = p.get("objective", "")
        m["about"] = p.get("about", "")
        contact = p.get("contact", {})
        m["email"] = contact.get("email", "")
        m["phone"] = str(contact.get("phone", ""))
        addr = contact.get("address", "")
        m["address"] = "\n".join(addr) if isinstance(addr, list) else str(addr)
        for lnk in p.get("links", []):
            label = lnk.get("label", "").lower()
            if "git" in label:
                m["github"] = lnk.get("url", "")
            elif "linked" in label:
                m["linkedin"] = lnk.get("url", "")

        def badge_names(lst):
            return ", ".join(b["name"] if isinstance(b, dict) else str(b) for b in lst)

        skills = data.get("skills", {})
        m["tech_badges"] = badge_names(skills.get("technical", []))
        m["lang_badges"] = badge_names(skills.get("languages", []))
        for key in ("formations", "experiences"):
            for it in data.get(key, []):
                m[key].append({"title": it.get("title", ""),
                               "subtitle": it.get("subtitle", ""),
                               "date": it.get("date", ""),
                               "description": it.get("description", "")})
        for cat in data.get("skills_section", []):
            m["skill_cats"].append({"category": cat.get("category", ""),
                                    "items": ", ".join(cat.get("items", []))})
        for c in data.get("certifications", []):
            m["certifications"].append({"name": c.get("name", ""),
                                        "issuer": c.get("issuer", ""),
                                        "date": c.get("date", ""),
                                        "url": c.get("url", ""),
                                        "image": c.get("image", "")})
        self.model = m
        # rebind editors to the new lists
        self.edu_editor.items = m["formations"]
        self.exp_editor.items = m["experiences"]
        self.skill_editor.items = m["skill_cats"]
        self.cert_editor.items = m["certifications"]
        order = data.get("section_order", [])
        if sorted(order) == sorted(SECTION_KEYS):
            self.section_order = list(order)
            self._apply_tab_order()
            self.preset_var.set(self._preset_name())
        self.populate()

    # ── file actions ───────────────────────────────────────────────────

    def load_data(self):
        t = self.t
        path = filedialog.askopenfilename(filetypes=[(t["dlg_json"], "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            messagebox.showerror(t["msg_err_title"], t["msg_invalid_json"])
            return
        self.apply_data(data)
        messagebox.showinfo(WINDOW_TITLE, t["msg_data_loaded"])

    def save_data(self):
        t = self.t
        self.harvest()
        path = filedialog.asksaveasfilename(defaultextension=".json",
                                            initialfile="cv_data.json",
                                            filetypes=[(t["dlg_json"], "*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.build_data(), f, ensure_ascii=False, indent=2)
        messagebox.showinfo(WINDOW_TITLE, t["msg_data_saved"].format(path=path))

    def import_style(self):
        t = self.t
        path = filedialog.askopenfilename(filetypes=[(t["dlg_json"], "*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                imported = json.load(f)
        except (json.JSONDecodeError, OSError):
            messagebox.showerror(t["msg_err_title"], t["msg_invalid_json"])
            return
        self.style_dict = deep_merge(EMBEDDED_STYLE, imported)
        self._refresh_style_controls()
        messagebox.showinfo(WINDOW_TITLE, t["msg_style_loaded"])

    def reset_style(self):
        self.style_dict = load_default_style()
        self._refresh_style_controls()
        messagebox.showinfo(WINDOW_TITLE, self.t["msg_style_reset"])

    # ── generation ─────────────────────────────────────────────────────

    def check_missing(self):
        t, m = self.t, self.model
        missing = []
        for key, label_key in [("name", "lbl_name"), ("title", "lbl_title"),
                               ("email", "lbl_email"), ("phone", "lbl_phone"),
                               ("objective", "lbl_objective"), ("about", "lbl_about")]:
            if not m[key]:
                missing.append(t[label_key])
        if not m["formations"]:
            missing.append(t["f_education"])
        if not m["experiences"]:
            missing.append(t["f_experience"])
        if not m["skill_cats"]:
            missing.append(t["f_skills"])
        if any(not e.get("date") for e in m["formations"] + m["experiences"]):
            missing.append(t["f_dates"])
        return missing

    def on_generate(self):
        t = self.t
        self.harvest()

        missing = self.check_missing()
        if missing:
            msg = (t["msg_missing_intro"] + "\n\n"
                   + "\n".join("• " + f for f in missing)
                   + "\n\n" + t["msg_missing_outro"])
            if not messagebox.askyesno(t["msg_missing_title"], msg, icon="warning"):
                return

        path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                            initialfile="cv_output.pdf",
                                            filetypes=[(t["dlg_pdf"], "*.pdf")])
        if not path:
            return

        data = self.build_data()
        style = copy.deepcopy(self.style_dict)
        lang = {"lang": self.lang, self.lang: CV_LABELS[self.lang]}
        try:
            gen = CVGenerator(data, style, lang)
            gen.generate()
            gen.output(path)
        except Exception as exc:
            messagebox.showerror(t["msg_err_title"],
                                 t["msg_err_body"] + f"\n\n[{type(exc).__name__}] {exc}")
            return

        if messagebox.askyesno(t["msg_done_title"],
                               t["msg_done_body"].format(path=path)
                               + "\n\n" + t["msg_open_pdf"]):
            open_in_viewer(path)


# ── startup language chooser ───────────────────────────────────────────

def choose_language():
    chosen = {"code": None}
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    set_window_icon(root)
    root.resizable(False, False)
    frame = ttk.Frame(root, padding=24)
    frame.pack()
    ttk.Label(frame, text=" / ".join(TR[c]["choose_lang"] for c in ("fr", "en")),
              font=("Segoe UI", 11, "bold")).pack(pady=(0, 14))

    def pick(code):
        chosen["code"] = code
        root.destroy()

    for code in ("fr", "en", "es", "pt"):
        ttk.Button(frame, text=TR[code]["lang_name"], width=26,
                   command=lambda c=code: pick(c)).pack(pady=3)

    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) // 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) // 3
    root.geometry(f"+{x}+{y}")
    root.mainloop()
    return chosen["code"]


# ── headless smoke test (used to verify the frozen exe) ────────────────

def selftest():
    out = os.path.join(base_dir(), "selftest_output.pdf")
    data = {
        "personal": {
            "name": "Jane Doe", "title": "Master's Applicant",
            "photo": "", "objective": "Selftest objective.",
            "about": "Selftest about paragraph.",
            "contact": {"email": "jane@doe.dev", "phone": "0600000000",
                        "address": ["1 Test Street", "69000 Lyon"]},
            "links": [{"label": "Github", "icon": "",
                       "icon_font": "fa-brands", "url": "https://github.com"}],
        },
        "skills": {"technical": ["Python"], "languages": [{"name": "English C2", "style": "accent"}]},
        "formations": [{"title": "BSc Computer Science", "subtitle": "Test University",
                        "date": "2022-2025",
                        "description": "Context.\n- Bullet one\n- Bullet two"}],
        "experiences": [{"title": "Intern", "subtitle": "ACME", "date": "2025",
                         "description": "Did things.\n- Achieved X"}],
        "skills_section": [{"category": "Programming", "items": ["Python", "SQL"]}],
        "certifications": [{"name": "Cert", "issuer": "Issuer", "date": "2024"}],
        "section_order": PRESETS[DEFAULT_PRESET],
    }
    lang = {"lang": "en", "en": CV_LABELS["en"]}
    gen = CVGenerator(data, load_default_style(), lang)
    gen.generate()
    gen.output(out)
    print("SELFTEST OK ->", out)


def main():
    if "--selftest" in sys.argv:
        selftest()
        return
    set_app_user_model_id()
    code = choose_language()
    if not code:
        return
    app = CVApp(code)
    app.mainloop()


if __name__ == "__main__":
    main()
