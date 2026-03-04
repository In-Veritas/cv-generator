#!/usr/bin/env python3
"""
CV Generator
Generates a two-column PDF CV from JSON data and style configuration.
Uses Font Awesome icons for links, contact markers, and certifications.

Usage:
    python generate_cv.py
    python generate_cv.py --data my_data.json --style my_style.json -o output.pdf
"""

import json
import argparse
import os
import sys
import tempfile
from fpdf import FPDF

try:
    from PIL import Image
    _HAS_PIL = True
except ImportError:
    _HAS_PIL = False


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class CVGenerator(FPDF):

    def __init__(self, data, style, lang=None):
        super().__init__(format="A4")
        self.data = data
        self.st = style
        self._lang = lang or {}
        self.W = 210   # A4 width  (mm)
        self.H = 297   # A4 height (mm)
        self.sidebar_w = self.W * self.st["sidebar"]["width_ratio"]
        self.set_auto_page_break(auto=False)
        if getattr(sys, 'frozen', False):
            self._base_dir = os.path.dirname(sys.executable)
        else:
            self._base_dir = os.path.dirname(os.path.abspath(__file__))
        self._load_icon_fonts()
        self._load_custom_fonts()

    # ── font registration ──────────────────────────────────────────────

    def _load_icon_fonts(self):
        fonts_dir = os.path.join(self._base_dir, "fonts")
        self._has_fa_brands = False
        self._has_fa_solid = False

        if not os.path.isdir(fonts_dir):
            return

        for fname in os.listdir(fonts_dir):
            lower = fname.lower()
            full = os.path.join(fonts_dir, fname)

            if "brands" in lower and (lower.endswith(".otf") or lower.endswith(".ttf")):
                self.add_font("fa-brands", "", full)
                self._has_fa_brands = True
            elif "solid" in lower and (lower.endswith(".otf") or lower.endswith(".ttf")):
                self.add_font("fa-solid", "", full)
                self._has_fa_solid = True

    def _load_custom_fonts(self):
        custom = self.st.get("fonts", {}).get("custom", {})
        for family, variants in custom.items():
            if isinstance(variants, str) and os.path.exists(variants):
                self.add_font(family, "", variants)
            elif isinstance(variants, dict):
                for sty, path in variants.items():
                    if os.path.exists(path):
                        self.add_font(family, sty, path)

    # ── photo resolution (supports jpg, jpeg, png, bmp, gif) ─────────

    def _resolve_photo(self, photo):
        photo_path = photo if os.path.isabs(photo) else os.path.join(self._base_dir, photo)
        if os.path.exists(photo_path):
            return photo_path
        root, _ = os.path.splitext(photo_path)
        for ext in (".png", ".jpg", ".jpeg", ".bmp", ".gif"):
            candidate = root + ext
            if os.path.exists(candidate):
                return candidate
        return None

    # ── style helpers ──────────────────────────────────────────────────

    def _font(self, key):
        return self.st.get("fonts", {}).get(key, "Helvetica")

    def _size(self, key):
        return self.st.get("font_sizes", {}).get(key, 10)

    def _color(self, key, fallback=(0, 0, 0)):
        return tuple(self.st.get("colors", {}).get(key, list(fallback)))

    def _gap(self, key):
        return self.st.get("spacing", {}).get(key, 4)

    def _lh(self, font_size):
        ratio = self.st.get("spacing", {}).get("line_height_ratio", 0.44)
        return font_size * ratio

    def _label(self, key, fallback=""):
        code = self._lang.get("lang", "fr")
        strings = self._lang.get(code, {})
        return strings.get(key, fallback)

    # ── icon helper ────────────────────────────────────────────────────

    def _draw_icon(self, x, y, icon_char, font_family, size, color=None):
        if color:
            self.set_text_color(*color)
        self.set_font(font_family, "", size)
        self.set_xy(x, y)
        w = self.get_string_width(icon_char)
        self.cell(w, self._lh(size), icon_char)
        return w

    def _tint_image(self, path, rgb):
        """Return path to a tinted copy of the image (or original if Pillow unavailable)."""
        if not _HAS_PIL:
            return path
        img = Image.open(path).convert("RGBA")
        r, g, b = rgb
        pixels = img.load()
        for y in range(img.height):
            for x in range(img.width):
                _, _, _, a = pixels[x, y]
                if a > 0:
                    pixels[x, y] = (r, g, b, a)
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tmp.name)
        return tmp.name

    def _has_icon_font(self, font_name):
        if font_name == "fa-brands":
            return self._has_fa_brands
        if font_name == "fa-solid":
            return self._has_fa_solid
        return font_name.lower() in [f.lower() for f in self.fonts]

    # ── public API ─────────────────────────────────────────────────────

    def generate(self):
        self.add_page()
        self._draw_sidebar()
        self._draw_main()
        self._draw_footer()
        return self

    # ══════════════════════════════════════════════════════════════════
    #  SIDEBAR
    # ══════════════════════════════════════════════════════════════════

    def _draw_sidebar(self):
        cfg = self.st["sidebar"]
        pad = cfg["padding"]
        x, w = pad, self.sidebar_w - 2 * pad
        y = cfg.get("top_margin", 12)

        # background
        self.set_fill_color(*cfg["bg_color"])
        self.rect(0, 0, self.sidebar_w, self.H, "F")

        p = self.data["personal"]

        # ── name (centred) ────────────────────────────────────────────
        self.set_font(self._font("heading"), "B", self._size("name"))
        self.set_text_color(*self._color("sidebar_name"))
        self.set_xy(x, y)
        self.multi_cell(w, self._lh(self._size("name")), p["name"], align="C")
        y = self.get_y() + self._gap("after_name")

        # ── title (centred) ───────────────────────────────────────────
        self.set_font(self._font("heading"), "I", self._size("subtitle"))
        self.set_text_color(*self._color("sidebar_title"))
        self.set_xy(x, y)
        self.multi_cell(w, self._lh(self._size("subtitle")), p.get("title", ""), align="C")
        y = self.get_y() + self._gap("after_title")

        # ── photo (centred) ───────────────────────────────────────────
        photo = p.get("photo", "")
        if photo:
            photo_path = self._resolve_photo(photo)
            if photo_path and os.path.exists(photo_path):
                sz = cfg.get("photo_size", 35)
                self.image(photo_path, x + (w - sz) / 2, y, sz, sz)
                y += sz + self._gap("after_photo")

        # ── technical badges (optional) ───────────────────────────────
        tech = self.data.get("skills", {}).get("technical", [])
        if tech:
            y = self._draw_badges(x, y, w, tech)
            y += self._gap("after_tech_badges")

        # ── language badges (optional) ────────────────────────────────
        langs = self.data.get("skills", {}).get("languages", [])
        if langs:
            y = self._draw_badges(x, y, w, langs)
            y += self._gap("after_lang_badges")

        # ── Everything below photo: LEFT-ALIGNED ──────────────────────

        # ── social links (left-aligned) ───────────────────────────────
        links = p.get("links", [])
        if links:
            y = self._draw_links(x, y, w, links)
            y += self._gap("after_links")

        # ── objective box (highlighted) ───────────────────────────────
        objective = p.get("objective", "")
        if objective:
            y = self._draw_objective(x, y, w, objective)
            y += self._gap("after_objective")

        # ── about (left-aligned) ─────────────────────────────────────
        about = p.get("about", "")
        if about:
            self.set_font(self._font("body"), "", self._size("about"))
            self.set_text_color(*self._color("sidebar_text"))
            self.set_xy(x, y)
            self.multi_cell(w, self._lh(self._size("about")), about, align="L")
            y = self.get_y() + self._gap("after_about")

        # ── contact ───────────────────────────────────────────────────
        contact = p.get("contact", {})
        if contact:
            self._draw_contact(x, y, w, contact)

    # ── sidebar: badges ────────────────────────────────────────────────

    def _draw_badges(self, x, y, available_w, badges):
        bc = self.st.get("badges", {})
        px  = bc.get("padding_x", 7)
        py  = bc.get("padding_y", 2.5)
        gap = bc.get("gap", 3)
        fs  = bc.get("font_size", 8)
        r   = bc.get("radius", 2)
        bw  = bc.get("border_width", 0.4)

        self.set_font(self._font("body"), "", fs)

        items = []
        for b in badges:
            name  = b["name"]  if isinstance(b, dict) else b
            style = b.get("style", "outlined") if isinstance(b, dict) else "outlined"
            tw = self.get_string_width(name) + 2 * px
            th = fs * 0.35 + 2 * py
            items.append({"name": name, "style": style, "w": tw, "h": th})

        rows, row, rw = [], [], 0
        for it in items:
            need = it["w"] + (gap if row else 0)
            if rw + need > available_w and row:
                rows.append(row)
                row, rw = [it], it["w"]
            else:
                rw += need
                row.append(it)
        if row:
            rows.append(row)

        STYLE_MAP = {
            "filled":   ("filled_bg",   "filled_text",   "filled_bg"),
            "accent":   ("accent_bg",   "accent_text",   "accent_bg"),
            "outlined": ("outlined_bg", "outlined_text", "outlined_border"),
        }

        for row in rows:
            total = sum(it["w"] for it in row) + gap * (len(row) - 1)
            bx = x + (available_w - total) / 2
            mh = max(it["h"] for it in row)

            for it in row:
                bg_key, txt_key, brd_key = STYLE_MAP.get(it["style"], STYLE_MAP["outlined"])
                self.set_fill_color(*bc.get(bg_key, [255, 255, 255]))
                self.set_draw_color(*bc.get(brd_key, [0, 0, 0]))
                self.set_line_width(bw)

                by = y + (mh - it["h"]) / 2
                try:
                    self.rounded_rect(bx, by, it["w"], it["h"], r, style="DF")
                except (AttributeError, TypeError):
                    self.rect(bx, by, it["w"], it["h"], "DF")

                self.set_text_color(*bc.get(txt_key, [0, 0, 0]))
                self.set_font(self._font("body"), "", fs)
                self.set_xy(bx, by + (it["h"] - fs * 0.35) / 2)
                self.cell(it["w"], fs * 0.35, it["name"], align="C")
                bx += it["w"] + gap

            y += mh + gap

        return y

    # ── sidebar: objective box ─────────────────────────────────────────

    def _draw_objective(self, x, y, w, text):
        oc     = self.st.get("objective", {})
        fs     = oc.get("font_size", 8.5)
        pad    = oc.get("padding", 5)
        radius = oc.get("radius", 2)
        bg     = tuple(oc.get("bg_color", [40, 62, 100]))
        border = tuple(oc.get("border_color", [70, 110, 170]))
        title_color = tuple(oc.get("title_color", [130, 175, 230]))
        text_color  = tuple(oc.get("text_color", [220, 230, 245]))
        title  = self._label("objective", oc.get("title", "Objectif"))
        fs_t   = oc.get("title_font_size", 9)
        title_gap = 2
        inner_w = w - 2 * pad
        lh = self._lh(fs)

        # render title + text first, then measure real height and draw box behind
        text_start_y = y + pad + self._lh(fs_t) + title_gap

        # title
        self.set_font(self._font("body"), "B", fs_t)
        self.set_text_color(*title_color)
        self.set_xy(x + pad, y + pad)
        self.cell(inner_w, self._lh(fs_t), title)

        # text
        self.set_font(self._font("body"), "", fs)
        self.set_text_color(*text_color)
        self.set_xy(x + pad, text_start_y)
        self.multi_cell(inner_w, lh, text, align="L")
        text_end_y = self.get_y()

        # now we know the real height — draw box behind everything
        box_h = (text_end_y - y) + pad
        self.set_fill_color(*bg)
        self.set_draw_color(*border)
        self.set_line_width(0.4)
        try:
            self.rounded_rect(x, y, w, box_h, radius, style="DF")
        except (AttributeError, TypeError):
            self.rect(x, y, w, box_h, "DF")

        # re-render title + text on top of the box
        self.set_font(self._font("body"), "B", fs_t)
        self.set_text_color(*title_color)
        self.set_xy(x + pad, y + pad)
        self.cell(inner_w, self._lh(fs_t), title)

        self.set_font(self._font("body"), "", fs)
        self.set_text_color(*text_color)
        self.set_xy(x + pad, text_start_y)
        self.multi_cell(inner_w, lh, text, align="L")

        return y + box_h

    # ── sidebar: links (centred, with FA icons) ────────────────────────

    def _draw_links(self, x, y, w, links):
        fs       = self._size("link")
        gap      = self.st.get("links", {}).get("gap", 10)
        icon_gap = self.st.get("links", {}).get("icon_gap", 2)
        lh       = self._lh(fs)
        color    = self._color("sidebar_link")

        # measure total width to centre the row
        items = []
        for lnk in links:
            icon      = lnk.get("icon", "")
            icon_font = lnk.get("icon_font", "")
            label     = lnk.get("label", "")
            iw = 0
            if icon and icon_font and self._has_icon_font(icon_font):
                self.set_font(icon_font, "", fs)
                iw = self.get_string_width(icon) + icon_gap
            self.set_font(self._font("body"), "B", fs)
            lw = self.get_string_width(label)
            items.append({"icon": icon, "icon_font": icon_font,
                          "label": label, "iw": iw, "lw": lw,
                          "total": iw + lw, "url": lnk.get("url", "")})

        total_w = sum(it["total"] for it in items) + gap * (len(items) - 1)
        bx = x + (w - total_w) / 2  # centred

        for it in items:
            if it["iw"] > 0:
                self._draw_icon(bx, y, it["icon"], it["icon_font"], fs, color)
            self.set_font(self._font("body"), "B", fs)
            self.set_text_color(*color)
            self.set_xy(bx + it["iw"], y)
            if it["url"]:
                self.cell(it["lw"], lh, it["label"], link=it["url"])
            else:
                self.cell(it["lw"], lh, it["label"])
            bx += it["total"] + gap

        return y + lh

    # ── sidebar: contact (with FA icons) ───────────────────────────────

    def _draw_contact(self, x, y, w, contact):
        cc    = self.st.get("contact", {})
        fs_l  = self._size("contact_label")
        fs_v  = self._size("contact_value")
        lh    = cc.get("line_height", 4.2)
        marks = cc.get("markers", {})

        fields = [
            ("email",   contact.get("email", "")),
            ("phone",   contact.get("phone", "")),
            ("address", contact.get("address", "")),
        ]

        for key, value in fields:
            if not value:
                continue
            marker_cfg = marks.get(key, {})

            marker_w = 0
            if marker_cfg:
                icon      = marker_cfg.get("icon", "")  if isinstance(marker_cfg, dict) else ""
                icon_font = marker_cfg.get("font", "")  if isinstance(marker_cfg, dict) else ""
                text      = marker_cfg.get("text", marker_cfg) if isinstance(marker_cfg, dict) else marker_cfg

                if icon and icon_font and self._has_icon_font(icon_font):
                    self.set_text_color(*self._color("sidebar_text"))
                    self.set_font(icon_font, "", fs_l)
                    self.set_xy(x, y)
                    marker_w = self.get_string_width(icon) + 2.5
                    self.cell(marker_w, lh, icon)
                elif text:
                    self.set_font(self._font("body"), "B", fs_l)
                    self.set_text_color(*self._color("sidebar_text"))
                    self.set_xy(x, y)
                    marker_w = self.get_string_width(str(text)) + 2
                    self.cell(marker_w, lh, str(text))

            self.set_font(self._font("body"), "", fs_v)
            self.set_text_color(*self._color("sidebar_text"))
            vx = x + marker_w

            if isinstance(value, list):
                for i, line in enumerate(value):
                    self.set_xy(vx, y + i * lh)
                    self.cell(w - marker_w, lh, line)
                y += len(value) * lh + 1.5
            else:
                self.set_xy(vx, y)
                self.cell(w - marker_w, lh, str(value))
                y += lh + 1.5

    # ══════════════════════════════════════════════════════════════════
    #  MAIN CONTENT (right column)
    # ══════════════════════════════════════════════════════════════════

    def _draw_main(self):
        cfg = self.st.get("main", {})
        pad = cfg.get("padding", 10)
        x = self.sidebar_w + pad
        w = self.W - self.sidebar_w - 2 * pad
        y = cfg.get("top_margin", 10)

        # ── Formations ─────────────────────────────────────────────────
        formations = self.data.get("formations", [])
        if formations:
            y = self._section_header(x, y, w, self._label("formations", "Formations"))
            for item in formations:
                y = self._entry(x, y, w, item)
                y += self._gap("between_items")
            y += self._gap("between_sections")

        # ── Expériences ────────────────────────────────────────────────
        experiences = self.data.get("experiences", [])
        if experiences:
            y = self._section_header(x, y, w, self._label("experiences", "Expériences"))
            for item in experiences:
                y = self._entry(x, y, w, item)
                y += self._gap("between_items")
            y += self._gap("between_sections")

        # ── Compétences (flashy badge-style) ───────────────────────────
        skills_section = self.data.get("skills_section", [])
        if skills_section:
            y = self._section_header(x, y, w, self._label("skills", "Compétences"))
            for i, cat in enumerate(skills_section):
                y = self._skill_category(x, y, w, cat, i)
            y += self._gap("between_sections")

        # ── Certifications ─────────────────────────────────────────────
        certifications = self.data.get("certifications", [])
        if certifications:
            y = self._section_header(x, y, w, self._label("certifications", "Certifications"))
            self._certifications_grid(x, y, w, certifications)

    # ── main: section header ───────────────────────────────────────────

    def _section_header(self, x, y, w, title):
        hc = self.st.get("section_header", {})
        fs = self._size("section_header")

        self.set_font(self._font("heading"), "", fs)
        self.set_text_color(*self._color("section_header"))
        self.set_xy(x, y)
        self.cell(w, self._lh(fs), title)
        y += self._lh(fs) + 1

        self.set_draw_color(*self._color("section_underline"))
        self.set_line_width(hc.get("underline_thickness", 0.3))
        self.line(x, y, x + w, y)
        y += hc.get("gap_after", 5)
        return y

    # ── main: formation / experience entry ─────────────────────────────

    def _entry(self, x, y, w, item):
        fs = self._size("item_title")
        self.set_font(self._font("heading"), "B", fs)
        self.set_text_color(*self._color("item_title"))
        self.set_xy(x, y)
        self.multi_cell(w, self._lh(fs), item.get("title", ""))
        y = self.get_y()

        sub = item.get("subtitle", "")
        if sub:
            fs_s = self._size("item_subtitle")
            self.set_font(self._font("body"), "B", fs_s)
            self.set_text_color(*self._color("item_subtitle"))
            self.set_xy(x, y)
            self.cell(w, self._lh(fs_s), sub)
            y += self._lh(fs_s) + 0.5

        date = item.get("date", "")
        if date:
            fs_d = self._size("item_date")
            self.set_font(self._font("body"), "I", fs_d)
            self.set_text_color(*self._color("item_date"))
            self.set_xy(x, y)
            self.cell(w, self._lh(fs_d), date)
            y += self._lh(fs_d) + 1

        desc = item.get("description", "")
        if desc:
            fs_desc = self._size("item_description")
            lh = self._lh(fs_desc)
            indent = 4
            bullet_r = 0.5

            lines = desc.split("\n")
            for line in lines:
                is_bullet = line.startswith("-")
                text = line.lstrip("- ") if is_bullet else line
                self.set_font(self._font("body"), "", fs_desc)
                self.set_text_color(*self._color("text"))

                if is_bullet:
                    # draw small filled circle as bullet
                    bullet_y = y + lh / 2
                    self.set_fill_color(*self._color("item_title"))
                    self.ellipse(x + indent / 2 - bullet_r, bullet_y - bullet_r,
                                 bullet_r * 2, bullet_r * 2, "F")
                    self.set_xy(x + indent, y)
                    self.multi_cell(w - indent, lh, text)
                else:
                    self.set_xy(x, y)
                    self.multi_cell(w, lh, text)
                y = self.get_y()

        return y

    # ── main: skills category with colored badges ──────────────────────

    def _skill_category(self, x, y, w, category, color_idx):
        sc = self.st.get("skills_section", {})
        colors = sc.get("category_colors", [[0, 121, 150]])
        color = tuple(colors[color_idx % len(colors)])
        fs_cat = sc.get("category_font_size", 9)

        # small colored square + bold category name
        sq = 3
        self.set_fill_color(*color)
        self.rect(x, y + 0.3, sq, sq, "F")

        self.set_font(self._font("body"), "B", fs_cat)
        self.set_text_color(*color)
        self.set_xy(x + sq + 2, y)
        self.cell(w - sq - 2, self._lh(fs_cat), category.get("category", ""))
        y += self._lh(fs_cat) + 1.5

        # skill items as pill badges
        items = category.get("items", [])
        y = self._draw_pill_badges(x, y, w, items, color)
        y += sc.get("category_gap", 4)

        return y

    def _draw_pill_badges(self, x, y, w, items, color):
        sc   = self.st.get("skills_section", {})
        fs   = sc.get("badge_font_size", 7.5)
        px   = sc.get("badge_padding_x", 5)
        py   = sc.get("badge_padding_y", 2)
        gap  = sc.get("badge_gap", 2.5)
        r    = sc.get("badge_radius", 2)

        self.set_font(self._font("body"), "", fs)

        # measure
        badges = []
        for item in items:
            tw = self.get_string_width(item) + 2 * px
            th = fs * 0.35 + 2 * py
            badges.append({"name": item, "w": tw, "h": th})

        # split into left-aligned rows
        rows, row, rw = [], [], 0
        for b in badges:
            need = b["w"] + (gap if row else 0)
            if rw + need > w and row:
                rows.append(row)
                row, rw = [b], b["w"]
            else:
                rw += need
                row.append(b)
        if row:
            rows.append(row)

        for row in rows:
            bx = x
            mh = max(b["h"] for b in row)

            for b in row:
                by = y + (mh - b["h"]) / 2

                self.set_fill_color(*color)
                self.set_draw_color(*color)
                self.set_line_width(0.3)
                try:
                    self.rounded_rect(bx, by, b["w"], b["h"], r, style="DF")
                except (AttributeError, TypeError):
                    self.rect(bx, by, b["w"], b["h"], "DF")

                self.set_text_color(255, 255, 255)
                self.set_font(self._font("body"), "", fs)
                self.set_xy(bx, by + (b["h"] - fs * 0.35) / 2)
                self.cell(b["w"], fs * 0.35, b["name"], align="C")

                bx += b["w"] + gap

            y += mh + gap

        return y

    # ── main: certifications grid (with optional link icons) ───────────

    def _certifications_grid(self, x, y, w, certs):
        cc       = self.st.get("certifications", {})
        cols     = cc.get("columns", 2)
        row_h    = cc.get("row_height", 10)
        col_gap  = cc.get("col_gap", 4)
        fs_n     = cc.get("name_font_size", 9)
        fs_i     = cc.get("issuer_font_size", 8)
        fs_icon  = cc.get("link_icon_size", 8)
        img_sz   = cc.get("image_size", 8)
        img_gap  = cc.get("image_gap", 2)
        col_w    = (w - col_gap * (cols - 1)) / cols

        link_icon      = cc.get("link_icon", "\uf0c1")
        link_icon_font = cc.get("link_icon_font", "fa-solid")
        link_color     = tuple(cc.get("link_icon_color", self._color("item_title")))

        for idx, cert in enumerate(certs):
            col = idx % cols
            row = idx // cols
            cx = x + col * (col_w + col_gap)
            cy = y + row * (row_h + col_gap)

            # badge image (clickable)
            url = cert.get("url", "")
            img = cert.get("image", "")
            text_x = cx
            if img:
                img_path = img if os.path.isabs(img) else os.path.join(self._base_dir, img)
                if os.path.exists(img_path):
                    self.image(img_path, cx, cy, img_sz, img_sz, link=url if url else "")
                    text_x = cx + img_sz + img_gap

            self.set_font(self._font("body"), "B", fs_n)
            self.set_text_color(*self._color("item_subtitle"))
            self.set_xy(text_x, cy)
            name = cert.get("name", "")
            name_w = self.get_string_width(name)
            self.cell(name_w, self._lh(fs_n), name)

            if url and self._has_icon_font(link_icon_font):
                icon_x = text_x + name_w + 1.5
                self.set_font(link_icon_font, "", fs_icon)
                self.set_text_color(*link_color)
                self.set_xy(icon_x, cy)
                icon_w = self.get_string_width(link_icon)
                self.cell(icon_w, self._lh(fs_n), link_icon, link=url)

            self.set_font(self._font("body"), "", fs_i)
            self.set_text_color(*self._color("item_date"))
            issuer_y = cy + self._lh(fs_n) + 0.5
            self.set_xy(text_x, issuer_y)
            self.cell(col_w - (text_x - cx), self._lh(fs_i), cert.get("issuer", ""))

            date = cert.get("date", "")
            if date:
                fs_d = cc.get("date_font_size", 6.5)
                self.set_font(self._font("body"), "I", fs_d)
                self.set_text_color(*self._color("item_date"))
                self.set_xy(text_x, issuer_y + self._lh(fs_i) + 0.3)
                self.cell(col_w - (text_x - cx), self._lh(fs_d), date)

    # ── footer (inside sidebar, bottom) ──────────────────────────────

    def _draw_footer(self):
        fc = self.st.get("footer", {})
        name = self.data.get("personal", {}).get("name", "")
        is_author = name == "Gabriel Vérité"

        text = fc.get("text", "") if is_author else fc.get("text_other", "CV generated with In:Veritas CV Generator")
        if not text:
            return

        fs       = fc.get("font_size", 6.5)
        color    = tuple(fc.get("color", [160, 180, 210]))
        pad      = self.st["sidebar"]["padding"]
        w        = self.sidebar_w - 2 * pad
        link_url = fc.get("link_url", "")

        icon_left  = fc.get("icon_left", fc.get("icon", ""))
        icon_font  = fc.get("icon_font", "")
        has_icons  = icon_font and self._has_icon_font(icon_font)
        img_right  = fc.get("image_right", "")

        self.set_font(self._font("body"), "", fs)
        self.set_text_color(*color)

        # measure widths
        text_w = self.get_string_width(text)
        icon_gap = 2
        lw = 0
        if has_icons and icon_left:
            self.set_font(icon_font, "", fs)
            lw = self.get_string_width(icon_left)

        # resolve right-side image
        img_path = None
        img_sz = fc.get("image_size", 3.5)
        if img_right:
            candidate = img_right if os.path.isabs(img_right) else os.path.join(self._base_dir, img_right)
            if os.path.exists(candidate):
                img_path = candidate

        ty = self.H - 12

        # line 1: plain text (centred)
        self.set_font(self._font("body"), "", fs)
        self.set_text_color(*color)
        self.set_xy(pad, ty)
        self.cell(w, self._lh(fs) + 1, text, align="C")

        # line 2: icon_left + link + image_right (centred)
        if link_url:
            link_y = ty + self._lh(fs) + 2
            display = link_url.replace("https://", "").replace("http://", "").rstrip("/")
            self.set_font(self._font("body"), "B", fs)
            self.set_text_color(*color)
            link_w = self.get_string_width(display)

            rw = (icon_gap + img_sz) if img_path else 0
            total_w = (lw + icon_gap if lw else 0) + link_w + rw
            cx = pad + (w - total_w) / 2

            if lw:
                self._draw_icon(cx, link_y, icon_left, icon_font, fs, color)
                cx += lw + icon_gap

            self.set_font(self._font("body"), "B", fs)
            self.set_text_color(*color)
            self.set_xy(cx, link_y)
            self.cell(link_w, self._lh(fs), display, link=link_url)
            cx += link_w + icon_gap

            if img_path:
                tinted = self._tint_image(img_path, color)
                img_y = link_y - (img_sz - self._lh(fs)) / 2
                self.image(tinted, cx, img_y, img_sz, img_sz)


# ══════════════════════════════════════════════════════════════════════
#  CLI
# ══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Generate a PDF CV from JSON data.")
    parser.add_argument("--data",   default="cv_data.json",   help="Path to CV data JSON")
    parser.add_argument("--style",  default="cv_style.json",  help="Path to style JSON")
    parser.add_argument("--lang",   default="cv_lang.json",   help="Path to language JSON")
    parser.add_argument("-o", "--output", default="cv_output.pdf", help="Output PDF path")
    args = parser.parse_args()

    # When running as a PyInstaller exe, use the exe's directory, not the temp dir
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    def resolve(p):
        return p if os.path.isabs(p) else os.path.join(script_dir, p)

    data  = load_json(resolve(args.data))
    style = load_json(resolve(args.style))
    lang_path = resolve(args.lang)
    lang = load_json(lang_path) if os.path.exists(lang_path) else {}

    gen = CVGenerator(data, style, lang)
    gen.generate()
    gen.output(resolve(args.output))
    print(f"CV generated -> {resolve(args.output)}")


if __name__ == "__main__":
    main()
