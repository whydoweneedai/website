#!/usr/bin/env python3
"""
Generate 1200×630 social share PNGs (logo + headline + topic).

Requires: fonts/Nunito-ExtraBold.ttf (pinned via fontsource API).
Outputs: images/og/<slug>.png, images/og/home.png, images/og/topic-<slug>.png

Run after editing data/site.json or article titles:
  python3 scripts/make-og-images.py
"""
from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OG_DIR = ROOT / "images" / "og"
BRAND = ROOT / "images" / "brand"
FONT_HEAD = ROOT / "fonts" / "Nunito-ExtraBold.ttf"
FONT_LABEL = ROOT / "fonts" / "Nunito-Bold.ttf"

W, H = 1200, 630
INK = (30, 58, 92)  # #1e3a5c
ACCENT = (24, 89, 169)  # sampled robot blue #1859a9
SKY = (216, 238, 248)
SKY_DEEP = (159, 211, 230)
GOLD = (242, 169, 59)
WHITE = (255, 255, 255)


def load_fonts():
    if not FONT_HEAD.exists():
        raise SystemExit(f"Missing {FONT_HEAD} — see docs/design-system.md")
    head = ImageFont.truetype(str(FONT_HEAD), 56)
    head_sm = ImageFont.truetype(str(FONT_HEAD), 48)
    label = ImageFont.truetype(str(FONT_LABEL), 28)
    return head, head_sm, label


def canvas() -> Image.Image:
    im = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(im)
    draw.rectangle((0, 0, W, 220), fill=SKY)
    draw.polygon([(0, 180), (W, 120), (W, 280), (0, 320)], fill=SKY_DEEP)
    draw.rectangle((0, 280, W, H), fill=WHITE)
    draw.line((72, 248, W - 72, 248), fill=(200, 220, 235), width=2)
    return im


def paste_rgba(base: Image.Image, overlay: Image.Image, xy: tuple[int, int], max_width: int | None = None):
    overlay = overlay.convert("RGBA")
    if max_width and overlay.width > max_width:
        ratio = max_width / overlay.width
        overlay = overlay.resize((max_width, int(overlay.height * ratio)), Image.Resampling.LANCZOS)
    base.paste(overlay, xy, overlay)


def draw_topic_pill(draw: ImageDraw.ImageDraw, text: str, font, xy: tuple[int, int]) -> int:
    pad_x, pad_y = 18, 10
    bbox = draw.textbbox((0, 0), text.upper(), font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = xy
    draw.rounded_rectangle(
        (x, y, x + tw + pad_x * 2, y + th + pad_y * 2),
        radius=999,
        fill=SKY,
        outline=ACCENT,
        width=2,
    )
    draw.text((x + pad_x, y + pad_y), text.upper(), font=font, fill=ACCENT)
    return y + th + pad_y * 2 + 24


def wrap_headline(draw: ImageDraw.ImageDraw, text: str, font, x: int, y: int, max_width: int) -> int:
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
    if len(lines) > 4:
        lines = lines[:4]
        lines[-1] = lines[-1][:80] + "…"
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=INK)
        bbox = draw.textbbox((x, y), ln, font=font)
        y = bbox[3] + 12
    return y


def render_article(title: str, topic: str, out: Path, head_font, label_font):
    im = canvas()
    draw = ImageDraw.Draw(im)
    lockup = Image.open(BRAND / "lockup-128.png")
    paste_rgba(im, lockup, (72, 56), max_width=520)
    y = draw_topic_pill(draw, topic, label_font, (72, 200))
    wrap_headline(draw, title, head_font, 72, y, W - 144)
    draw.ellipse((W - 120, H - 100, W - 40, H - 20), fill=GOLD)
    im.save(out, "PNG", optimize=True)
    print("og", out.relative_to(ROOT))


def render_home(out: Path, head_font, label_font):
    im = canvas()
    draw = ImageDraw.Draw(im)
    logo = Image.open(ROOT / "website_logo.png")
    paste_rgba(im, logo, (72, 48), max_width=420)
    draw.text((72, 360), "Practical AI for small business", font=label_font, fill=ACCENT)
    wrap_headline(
        draw,
        "Which AI is worth it for your business—researched and plainly answered.",
        head_font,
        72,
        410,
        W - 144,
    )
    im.save(out, "PNG", optimize=True)
    print("og", out.relative_to(ROOT))


def render_topic(name: str, out: Path, head_font, label_font):
    im = canvas()
    draw = ImageDraw.Draw(im)
    logo = Image.open(ROOT / "website_logo.png")
    paste_rgba(im, logo, (72, 40), max_width=320)
    y = draw_topic_pill(draw, "Topic", label_font, (72, 260))
    wrap_headline(draw, name, head_font, 72, y, W - 144)
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
