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
ACCENT = (24, 89, 169)
SKY = (232, 244, 251)
WHITE = (255, 255, 255)
MARGIN_X = 72
BOTTOM_RESERVE = 128


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


def fit_headline(draw: ImageDraw.ImageDraw, text: str, max_width: int, max_height: int, max_lines: int = 3):
    for size in range(54, 26, -2):
        font = load_font(size)
        lines = wrap_lines(draw, text, font, max_width)
        if len(lines) > max_lines:
            continue
        heights = []
        for ln in lines:
            bb = draw.textbbox((0, 0), ln, font=font)
            heights.append(bb[3] - bb[1] + 10)
        total = sum(heights) - 10 if heights else 0
        if total <= max_height:
            if len(lines) == max_lines and len(wrap_lines(draw, text, font, max_width)) > max_lines:
                continue
            return font, lines, total
    font = load_font(26)
    lines = wrap_lines(draw, text, font, max_width)[:max_lines]
    if lines:
        lines[-1] = (lines[-1][:70] + "…") if len(lines[-1]) > 70 else lines[-1]
    bb = draw.textbbox((0, 0), lines[0] if lines else "", font=font)
    total = (bb[3] - bb[1] + 10) * len(lines)
    return font, lines, total


def paste_lockup(im: Image.Image):
    lockup = Image.open(BRAND / "lockup-128.png")
    lw = 480
    ratio = lw / lockup.width
    lh = int(lockup.height * ratio)
    lockup = lockup.resize((lw, lh), Image.Resampling.LANCZOS)
    y = H - lh - 48
    im.paste(lockup.convert("RGBA"), (MARGIN_X, y), lockup.convert("RGBA"))


def draw_pill(draw: ImageDraw.ImageDraw, text: str, font, x: int, y: int) -> int:
    pad_x, pad_y = 18, 10
    label = text.upper()
    bbox = draw.textbbox((0, 0), label, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rounded_rectangle(
        (x, y, x + tw + pad_x * 2, y + th + pad_y * 2),
        radius=999,
        fill=SKY,
        outline=ACCENT,
        width=2,
    )
    draw.text((x + pad_x, y + pad_y), label, font=font, fill=ACCENT)
    return y + th + pad_y * 2


def render_page(title: str, out: Path, topic: str | None = None):
    im = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(im)
    label_font = load_label_font()
    y = 56
    if topic:
        y = draw_pill(draw, topic, label_font, MARGIN_X, y) + 28
    headline_top = y
    headline_bottom = H - BOTTOM_RESERVE - 36
    max_h = headline_bottom - headline_top
    max_w = W - MARGIN_X * 2
    font, lines, block_h = fit_headline(draw, title, max_w, max_h, max_lines=3)
    y = headline_top + max(0, (max_h - block_h) // 2)
    for ln in lines:
        draw.text((MARGIN_X, y), ln, font=font, fill=INK)
        bb = draw.textbbox((MARGIN_X, y), ln, font=font)
        y = bb[3] + 10
    paste_lockup(im)
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
        "Free AI Assessment for Small Business | AI ReadyScore Quiz",
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
