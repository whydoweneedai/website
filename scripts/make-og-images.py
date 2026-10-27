#!/usr/bin/env python3
"""
Generate 1200×630 social share PNGs (logo + headline + topic).

Requires: fonts/Nunito-ExtraBold.ttf (pinned).
Outputs: images/og/<slug>.png, images/og/home.png, images/og/topic-<slug>.png
"""
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
SKY_BAND = (216, 238, 248)
WHITE = (255, 255, 255)
BAND_H = 200


def load_fonts():
    if not FONT_HEAD.exists():
        raise SystemExit(f"Missing {FONT_HEAD}")
    return (
        ImageFont.truetype(str(FONT_HEAD), 56),
        ImageFont.truetype(str(FONT_HEAD), 48),
        ImageFont.truetype(str(FONT_LABEL), 26),
    )


def base_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, W, BAND_H), fill=SKY_BAND)
    draw.line((0, BAND_H, W, BAND_H), fill=(190, 215, 230), width=3)
    return im, draw


def paste_rgba(base: Image.Image, overlay: Image.Image, xy: tuple[int, int], max_width: int | None = None):
    overlay = overlay.convert("RGBA")
    if max_width and overlay.width > max_width:
        ratio = max_width / overlay.width
        overlay = overlay.resize((max_width, int(overlay.height * ratio)), Image.Resampling.LANCZOS)
    base.paste(overlay, xy, overlay)


def draw_topic_pill(draw: ImageDraw.ImageDraw, text: str, font, x: int, y: int) -> tuple[int, int, int, int]:
    pad_x, pad_y = 22, 14
    bbox = draw.textbbox((0, 0), text.upper(), font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    box = (x, y, x + tw + pad_x * 2, y + th + pad_y * 2)
    draw.rounded_rectangle(box, radius=999, fill=SKY, outline=ACCENT, width=2)
    draw.text((x + pad_x, y + pad_y), text.upper(), font=font, fill=ACCENT)
    return box


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, font, max_width: int, max_lines: int = 4) -> list[str]:
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
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:75] + "…"
    return lines


def draw_headline_centered(draw: ImageDraw.ImageDraw, text: str, font, y_center: int, max_width: int):
    lines = wrap_lines(draw, text, font, max_width)
    line_heights = []
    for ln in lines:
        bb = draw.textbbox((0, 0), ln, font=font)
        line_heights.append(bb[3] - bb[1] + 14)
    total = sum(line_heights) - 14
    y = y_center - total // 2
    for ln in lines:
        draw.text((72, y), ln, font=font, fill=INK)
        bb = draw.textbbox((72, y), ln, font=font)
        y = bb[3] + 14


def draw_bottom_brand(im: Image.Image):
    draw = ImageDraw.Draw(im)
    lockup = Image.open(BRAND / "lockup-128.png")
    head = Image.open(BRAND / "robot-head.png")
    lock_w = 440
    paste_rgba(im, lockup, (72, H - 118), max_width=lock_w)
    paste_rgba(im, head, (W - 200, H - 130), max_width=110)


def render_article(title: str, topic: str, out: Path, head_font, label_font):
    im, draw = base_canvas()
    draw_topic_pill(draw, topic, label_font, 72, 48)
    draw_headline_centered(draw, title, head_font, (BAND_H + H) // 2 + 20, W - 144)
    draw_bottom_brand(im)
    im.save(out, "PNG", optimize=True)
    print("og", out.relative_to(ROOT))


def render_home(out: Path, head_font, label_font):
    im, draw = base_canvas()
    draw_topic_pill(draw, "Why Do We Need AI", label_font, 72, 48)
    draw_headline_centered(
        draw,
        "Which AI is worth it for your business—researched and plainly answered.",
        head_font,
        (BAND_H + H) // 2 + 10,
        W - 144,
    )
    draw_bottom_brand(im)
    im.save(out, "PNG", optimize=True)
    print("og", out.relative_to(ROOT))


def render_topic(name: str, out: Path, head_font, label_font):
    im, draw = base_canvas()
    draw_topic_pill(draw, "Topic", label_font, 72, 48)
    draw_headline_centered(draw, name, head_font, (BAND_H + H) // 2 + 10, W - 144)
    draw_bottom_brand(im)
    im.save(out, "PNG", optimize=True)
    print("og", out.relative_to(ROOT))


def main():
    import sys

    sys.path.insert(0, str(ROOT / "scripts"))
    from site_data import load_site

    OG_DIR.mkdir(parents=True, exist_ok=True)
    head_font, head_sm, label_font = load_fonts()
    site = load_site()

    render_home(OG_DIR / "home.png", head_sm, label_font)

    for art in site["articles"]:
        render_article(
            art["searchTitle"],
            art["topicLabel"],
            OG_DIR / f"{art['slug']}.png",
            head_font,
            label_font,
        )

    for slug in site["topic_pages"]:
        topic = next(t for t in site["raw"]["topics"] if t["slug"] == slug)
        render_topic(topic["name"], OG_DIR / f"topic-{slug}.png", head_font, label_font)


if __name__ == "__main__":
    main()
