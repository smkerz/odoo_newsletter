"""Génère les vignettes PNG des templates MC Davidian pour le sélecteur Odoo."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "static" / "src" / "img" / "theme_imgs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Templates : (filename, category, title)
TEMPLATES = [
    ("mcdavidian_b2c_fr",              "B2C FR", "Newsletter"),
    ("mcdavidian_b2c_en",              "B2C EN", "Newsletter"),
    ("mcdavidian_b2c_guide_tailles_fr","B2C FR", "Guide des tailles"),
    ("mcdavidian_b2c_guide_tailles_en","B2C EN", "Size Guide"),
    ("mcdavidian_b2c_nouveautes_fr",   "B2C FR", "Nouveautés + Promo"),
    ("mcdavidian_b2c_nouveautes_en",   "B2C EN", "New Creations + Promo"),
    ("mcdavidian_b2b_bienvenue",       "B2B",    "Bienvenue / Welcome"),
]

# Couleurs MC Davidian
ROSE_BG = (245, 225, 220)
GOLD = (201, 169, 110)
DARK = (26, 26, 26)
GRAY = (122, 92, 92)

W, H = 640, 360

def get_font(size, italic=False, bold=False):
    candidates = []
    if bold:
        candidates += ["georgiab.ttf", "Georgia Bold.ttf"]
    if italic:
        candidates += ["georgiai.ttf", "Georgia Italic.ttf"]
    candidates += ["georgia.ttf", "Georgia.ttf", "times.ttf", "arial.ttf"]
    for fn in candidates:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_centered(draw, text, font, y, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((W - w) / 2, y), text, fill=color, font=font)

def make_thumbnail(filename, category, title):
    img = Image.new("RGB", (W, H), ROSE_BG)
    draw = ImageDraw.Draw(img)

    # Bordure or en haut et en bas
    draw.rectangle([0, 0, W, 4], fill=GOLD)
    draw.rectangle([0, H - 4, W, H], fill=GOLD)

    # "MC DAVIDIAN" en haut
    brand_font = get_font(22, bold=True)
    bbox = draw.textbbox((0, 0), "MC DAVIDIAN", font=brand_font)
    bw = bbox[2] - bbox[0]
    draw.text(((W - bw) / 2, 35), "MC DAVIDIAN", fill=DARK, font=brand_font)

    # Petit trait sous le nom de marque
    draw.rectangle([(W / 2 - 30), 70, (W / 2 + 30), 72], fill=GOLD)

    # Titre du template au centre
    title_font = get_font(34, italic=True)
    # Split long titles in 2 lines
    if len(title) > 18:
        words = title.split()
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        draw_centered(draw, line1, title_font, 135, DARK)
        draw_centered(draw, line2, title_font, 180, DARK)
    else:
        draw_centered(draw, title, title_font, 155, DARK)

    # Badge catégorie en bas
    cat_font = get_font(18, bold=True)
    bbox = draw.textbbox((0, 0), category, font=cat_font)
    cw, ch = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 14
    badge_w = cw + 2 * pad
    badge_h = ch + 10
    badge_x = (W - badge_w) / 2
    badge_y = 280
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=6, fill=GOLD,
    )
    draw.text((badge_x + pad, badge_y + 3), category, fill=(255, 255, 255), font=cat_font)

    # Sous-titre discret
    sub_font = get_font(11)
    draw_centered(draw, "Faits main en France depuis 1980", sub_font, 330, GRAY)

    out = OUTPUT_DIR / f"{filename}.png"
    img.save(out, "PNG", optimize=True)
    print(f"OK {out.name}")

for fn, cat, title in TEMPLATES:
    make_thumbnail(fn, cat, title)

print(f"\n{len(TEMPLATES)} vignettes dans {OUTPUT_DIR}")
