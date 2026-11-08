#!/usr/bin/env python3
"""Install favicons and build responsive header logos from the original PNG."""
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "images" / "brand"


def install_icons():
    shutil.copy2(BRAND / "robot-head-32.png", ROOT / "favicon.png")
    shutil.copy2(BRAND / "robot-head-180.png", ROOT / "apple-touch-icon.png")
    print("favicon.png + apple-touch-icon.png")


def build_header_logos():
    # CSS displays the original 684:128 lockup at 28px or 34px high.
    # Cover both sizes at 1x, 2x and 3x without sending the full 684px asset.
    with Image.open(BRAND / "lockup-128.png") as original:
        source = original.convert("RGBA")
        for width in (150, 182, 300, 364, 450, 546):
            height = round(width * source.height / source.width)
            resized = source.resize((width, height), Image.Resampling.LANCZOS)
            resized.save(BRAND / f"lockup-w{width}.webp", "WEBP", quality=90, method=6)
            resized.save(BRAND / f"lockup-w{width}.png", "PNG", optimize=True)
    print("responsive header lockups (150–546px, WebP + PNG)")


def main():
    BRAND.mkdir(parents=True, exist_ok=True)
    install_icons()
    build_header_logos()


if __name__ == "__main__":
    main()
