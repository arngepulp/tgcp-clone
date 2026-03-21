from tcgdexsdk import TCGdex
from tcgdexsdk.enums import Quality, Extension
from PIL import Image, ImageDraw, ImageFont
from consts import ENERGY_NAMES_TO_SYMBOLS
import asyncio
import textwrap

def draw_wrapped_text(draw, text, x, y, max_width, font, fill=(0,0,0)):
    lines = textwrap.wrap(text, width=max_width)
    for line in lines:
        draw.text((x, y), line, fill=fill, font=font)
        y += font.size + 4
    return y

def format_types(types):
    if not types:
        return "N/A"
    return ", ".join(types)

def format_cost(cost):
    if not cost:
        return ""
    return " ".join([ENERGY_NAMES_TO_SYMBOLS.get(c, c) for c in cost])

def save_placeholder_image(card, filepath):
    img = Image.new('RGB', (400, 700), color=(200, 200, 200))
    draw = ImageDraw.Draw(img)
    
    try:
        font_large = ImageFont.truetype("arial.ttf", 22)
        font_medium = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 13)
    except:
        font_large = ImageFont.load_default()
        font_medium = font_large
        font_small = font_large
    
    y = 20
    
    draw.text((20, y), card.name, fill=(0, 0, 0), font=font_large); y += 35
    types_str = format_types(getattr(card, 'types', None))
    draw.text((20, y), f"HP: {getattr(card, 'hp', 'N/A')}  Type: {types_str}", fill=(0, 0, 0), font=font_medium); y += 25
    draw.text((20, y), f"Stage: {getattr(card, 'stage', 'N/A')}", fill=(0, 0, 0), font=font_medium); y += 35

    abilities = getattr(card, 'abilities', []) or []
    for ab in abilities:
        draw.text((20, y), f"[ABILITY] {ab.name}", fill=(100, 0, 150), font=font_medium); y += 25
        y = draw_wrapped_text(draw, getattr(ab, 'effect', ''), 20, y, 45, font_small, fill=(0,0,0))
        y += 10

    attacks = getattr(card, 'attacks', []) or []
    for atk in attacks:
        cost_str = format_cost(getattr(atk, 'cost', []))
        damage = getattr(atk, 'damage', '0')
        effect = getattr(atk, 'effect', None)
        draw.text((20, y), f"[ATK] {atk.name}  Cost: {cost_str}  Dmg: {damage}", fill=(0, 0, 100), font=font_medium); y += 25
        if effect:
            y = draw_wrapped_text(draw, effect, 20, y, 45, font_small, fill=(0,0,0))
        y += 10

    y += 10
    weakness = getattr(card, 'weaknesses', []) or []
    for w in weakness:
        draw.text((20, y), f"Weakness: {w.type} {w.value}", fill=(150, 0, 0), font=font_medium); y += 25
    draw.text((20, y), f"Retreat: {getattr(card, 'retreat', 0)}", fill=(0, 0, 0), font=font_medium)

    img.save(filepath)