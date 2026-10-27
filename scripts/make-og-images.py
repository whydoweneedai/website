#!/usr/bin/env python3
"""Generate 1200×630 social share PNGs."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OG_DIR = ROOT / "images" / "og"
BRAND = ROOT / "images" / "brand"
FONT_HEAD = ROOT / "fonts" / "Nunito-ExtraBold.ttf"
FONT_LABEL = ROOT / "fonts" / "Nunito-Bold.ttf"

W, H = 1200, 630
INK = (30, 58, 92)
NAVY = (30, 58, 92)
ACCENT = (24, 89, 169)
SKY = (232, 244, 251)
WHITE = (255, 255, 255)
BAND_W = 252
MARGIN_X = 48
TEXT_LEFT = BAND_W + MARGIN_X
LOCKUP_MIN_HEIGHT = 96


def load_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_HEAD), size)


def load_label_font() -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_LABEL), 24)


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit_headline(draw: ImageDraw.ImageDraw, text: str, max_width: int, max_height: int, max_lines: int = 5):
    for size in range(58, 26, -2):
        font = load_font(size)
        lines = wrap_lines(draw, text, font, max_width)
        if len(lines) > max_lines:
            continue
        heights = []
        for ln in lines:
            bb = draw.textbbox((0, 0), ln, font=font)
            heights.append(bb[3] - bb[1] + 14)
        total = sum(heights) - 14 if heights else 0
        if total <= max_height:
            return font, lines, total
    font = load_font(26)
    lines = wrap_lines(draw, text, font, max_width)[:max_lines]
    if lines:
        lines[-1] = (lines[-1][:72] + "…") if len(lines[-1]) > 72 else lines[-1]
    bb = draw.textbbox((0, 0), lines[0] if lines else "", font=font)
    total = (bb[3] - bb[1] + 14) * len(lines)
    return font, lines, total


def paste_band_lockup(im: Image.Image, draw: ImageDraw.ImageDraw):
    lockup = Image.open(BRAND / "lockup-128.png").convert("RGBA")
    lh = LOCKUP_MIN_HEIGHT
    lw = int(lockup.width * (lh / lockup.height))
    max_w = BAND_W - 28
    if lw > max_w:
        lw = max_w
        lh = max(LOCKUP_MIN_HEIGHT, int(lockup.height * (lw / lockup.width)))
    lockup = lockup.resize((lw, lh), Image.Resampling.LANCZOS)
    pad_x = 10
    panel_w = lw + pad_x * 2
    panel_h = lh + pad_x * 2
    panel_x = (BAND_W - panel_w) // 2
    panel_y = (H - panel_h) // 2
    draw.rounded_rectangle(
        (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
        radius=10,
        fill=WHITE,
    )
    x = panel_x + pad_x
    y = panel_y + pad_x
    im.paste(lockup, (x, y), lockup)


def draw_topic_label(draw: ImageDraw.ImageDraw, text: str, font, x: int, y: int) -> int:
    label = text.upper()
    pad_x, pad_y = 16, 10
    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rounded_rectangle(
        (x, y, x + tw + pad_x * 2, y + th + pad_y * 2),
        radius=6,
        fill=WHITE,
        outline=ACCENT,
        width=2,
    )
    draw.text((x + pad_x, y + pad_y), label, font=font, fill=ACCENT)
    return y + th + pad_y * 2


def render_page(title: str, out: Path, topic: str | None = None):
    im = Image.new("RGB", (W, H), SKY)
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, BAND_W, H), fill=NAVY)
    paste_band_lockup(im, draw)
    draw = ImageDraw.Draw(im)

    label_font = load_label_font()
    content_top = 48
    content_bottom = H - 48
    if topic:
        topic_bottom = draw_topic_label(draw, topic, label_font, TEXT_LEFT, content_top) + 28
    else:
        topic_bottom = content_top + 8

    max_w = W - TEXT_LEFT - MARGIN_X
    max_h = content_bottom - topic_bottom
    font, lines, block_h = fit_headline(draw, title, max_w, max_h, max_lines=5)
    # Top-align in the content column so long headlines use the full height.
    y = topic_bottom + 12
    if block_h < max_h * 0.55:
        y = topic_bottom + max(12, (max_h - block_h) // 2)
    for ln in lines:
        draw.text((TEXT_LEFT, y), ln, font=font, fill=INK)
        bb = draw.textbbox((TEXT_LEFT, y), ln, font=font)
        y = bb[3] + 14

    im.save(out, "PNG", optimize=True)
    print("og", out.relative_to(ROOT))


def main():
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from site_data import load_site

    OG_DIR.mkdir(parents=True, exist_ok=True)
    site = load_site()

    render_page(
        "Which AI is worth it for your business—researched and plainly answered.",
        OG_DIR / "home.png",
        topic="Why Do We Need AI",
    )
    render_page(
        "AI ReadyScore: how ready is your business for AI?",
        OG_DIR / "ai-readyscore.png",
        topic="AI ReadyScore",
    )
    render_page(
        "About Why Do We Need AI",
        OG_DIR / "about.png",
        topic="About",
    )

    for art in site["articles"]:
        render_page(
            art["searchTitle"],
            OG_DIR / f"{art['slug']}.png",
            topic=art.get("topicPlateLabel") or art["topicLabel"],
        )

    for slug in site["topic_pages"]:
        topic = next(t for t in site["raw"]["topics"] if t["slug"] == slug)
        render_page(topic["name"], OG_DIR / f"topic-{slug}.png", topic="Topic")


if __name__ == "__main__":
    main()
