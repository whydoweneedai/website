#!/usr/bin/env python3
"""Generate WebP and @2x brand assets from PNG masters in images/brand/."""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "images" / "brand"

NAMES = ("logo-wordmark", "logo-mascot")


def export(name: str):
    png = BRAND / f"{name}.png"
    if not png.exists():
        raise SystemExit(f"Missing {png}")
    im = Image.open(png).convert("RGBA")
    im.save(BRAND / f"{name}.webp", "WEBP", quality=88, method=6)
    w2 = im.resize((im.width * 2, im.height * 2), Image.Resampling.LANCZOS)
    w2.save(BRAND / f"{name}@2x.png", "PNG")
    w2.save(BRAND / f"{name}@2x.webp", "WEBP", quality=88, method=6)
    print(name, im.size, "-> webp + @2x")


def favicon():
    mascot = Image.open(BRAND / "logo-mascot.png").convert("RGBA")
    # upper-center crop approximating robot head
    w, h = mascot.size
    head = mascot.crop((int(w * 0.22), 0, int(w * 0.78), int(h * 0.42)))
    alpha = head.split()[-1]
    bbox = alpha.getbbox()
    if bbox:
        head = head.crop(bbox)
    for size in (32, 180):
        out = head.resize((size, size), Image.Resampling.LANCZOS)
        if size == 32:
            out.save(ROOT / "favicon.png", "PNG")
        else:
            out.save(ROOT / "apple-touch-icon.png", "PNG")
    print("favicon + apple-touch-icon")


def main():
    BRAND.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        export(name)
    favicon()


if __name__ == "__main__":
    main()
