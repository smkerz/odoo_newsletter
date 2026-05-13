"""Génère les vignettes PNG des templates MC Davidian pour le sélecteur Odoo.

Odoo attend deux fichiers par template :
- <nom>_small.png : vignette dans le sélecteur
- <nom>_large.png : version agrandie au survol
Le `data-img` dans le XML doit être le nom de base SANS extension.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "static" / "src" / "img" / "theme_imgs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Templates : (filename base, category, title)
TEMPLATES = [
    ("mcdavidian_b2c_fr",               "B2C FR", "Newsletter"),
    ("mcdavidian_b2c_en",               "B2C EN", "Newsletter"),
    ("mcdavidian_b2c_guide_tailles_fr", "B2C FR", "Guide des tailles"),
    ("mcdavidian_b2c_guide_tailles_en", "B2C EN", "Size Guide"),
    ("mcdavidian_b2c_nouveautes_fr",    "B2C FR", "Nouveautés + Promo"),
    ("mcdavidian_b2c_nouveautes_en",    "B2C EN", "New Creations + Promo"),
    ("mcdavidian_b2c_matic_fr",         "B2C FR", "Le matic"),
    ("mcdavidian_b2c_matic_en",         "B2C EN", "The matic"),
    ("mcdavidian_b2c_coiffures_ete_fr", "B2C FR", "Idées coiffures été"),
    ("mcdavidian_b2c_coiffures_ete_en", "B2C EN", "Summer hairstyle ideas"),
    ("mcdavidian_b2b_bienvenue",        "B2B",    "Bienvenue / Welcome"),
    ("mcdavidian_b2b_reassort_ete",     "B2B",    "Réassort été / Summer reorder"),
    ("mcd_prospection_fr_fashion",      "PROSPECTION FR", "Fashion & Lifestyle"),
    ("mcd_prospection_fr_bridal",       "PROSPECTION FR", "Bridal & Cérémonie"),
    ("mcd_prospection_fr_hair_beauty",  "PROSPECTION FR", "Hair & Beauty"),
    ("mcd_prospection_fr_wellness",     "PROSPECTION FR", "Wellness & Hospitality"),
    ("mcd_prospection_fr_pharmacie",    "PROSPECTION FR", "Pharmacie"),
    ("mcd_prospection_fr_culture",      "PROSPECTION FR", "Culture & Patrimoine"),
]

ROSE_BG = (245, 225, 220)
GOLD = (201, 169, 110)
DARK = (26, 26, 26)
GRAY = (122, 92, 92)

# Tailles cibles Odoo (aspect 0.72, identique aux thèmes standards)
# Small = taille réelle du conteneur dans le sélecteur (180x250)
# Large = 2x pour le rendu retina/hover
SIZES = {
    "small": (180, 250),
    "large": (360, 500),
}

def get_font(size, italic=False, bold=False):
    candidates = []
    if bold:
        candidates += ["georgiab.ttf"]
    if italic:
        candidates += ["georgiai.ttf"]
    candidates += ["georgia.ttf", "times.ttf", "arial.ttf"]
    for fn in candidates:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_centered(draw, text, font, y, color, width):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((width - w) / 2, y), text, fill=color, font=font)

def make_thumbnail(W, H, title, category, is_large):
    img = Image.new("RGB", (W, H), ROSE_BG)
    draw = ImageDraw.Draw(img)

    # Facteur d'échelle basé sur la largeur (référence = 180px)
    scale = W / 180

    # Liserés or haut/bas
    border = max(1, int(2 * scale))
    draw.rectangle([0, 0, W, border], fill=GOLD)
    draw.rectangle([0, H - border, W, H], fill=GOLD)

    # "MC DAVIDIAN" en haut
    brand_size = max(9, int(13 * scale))
    brand_font = get_font(brand_size, bold=True)
    draw_centered(draw, "MC DAVIDIAN", brand_font, int(25 * scale), DARK, W)

    # Petit trait
    trait_w = int(18 * scale)
    trait_y = int(25 * scale) + brand_size + int(5 * scale)
    draw.rectangle(
        [(W / 2 - trait_w), trait_y, (W / 2 + trait_w), trait_y + max(1, int(1.5 * scale))],
        fill=GOLD,
    )

    # Titre au centre avec word-wrap
    title_size = max(11, int(18 * scale))
    title_font = get_font(title_size, italic=True)

    words = title.split()
    lines = []
    current = []
    max_line_width = W - int(16 * scale)
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=title_font)
        if bbox[2] - bbox[0] <= max_line_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))

    line_height = title_size + int(4 * scale)
    total_h = len(lines) * line_height
    start_y = (H - total_h) / 2 - int(8 * scale)
    for i, line in enumerate(lines):
        draw_centered(draw, line, title_font, int(start_y + i * line_height), DARK, W)

    # Badge catégorie
    cat_size = max(8, int(10 * scale))
    cat_font = get_font(cat_size, bold=True)
    bbox = draw.textbbox((0, 0), category, font=cat_font)
    cw, ch = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_h = max(5, int(9 * scale))
    pad_v = max(2, int(4 * scale))
    badge_w = cw + 2 * pad_h
    badge_h = ch + 2 * pad_v
    badge_x = (W - badge_w) / 2
    badge_y = H - int(55 * scale)
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=max(2, int(4 * scale)),
        fill=GOLD,
    )
    draw.text(
        (badge_x + pad_h, badge_y + pad_v - int(1 * scale)),
        category, fill=(255, 255, 255), font=cat_font,
    )

    # Sous-titre tout en bas
    sub_font = get_font(max(7, int(8 * scale)))
    draw_centered(draw, "Fait main en France depuis 1980", sub_font, H - int(22 * scale), GRAY, W)

    return img

for base, cat, title in TEMPLATES:
    for suffix, (w, h) in SIZES.items():
        img = make_thumbnail(w, h, title, cat, is_large=(suffix == "large"))
        out = OUTPUT_DIR / f"{base}_{suffix}.png"
        img.save(out, "PNG", optimize=True)
        print(f"OK {out.name}")

print(f"\n{len(TEMPLATES) * 2} vignettes dans {OUTPUT_DIR}")
