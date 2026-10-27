#!/usr/bin/env python3
"""Install favicons from brand pack and optional WebP derivatives."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "images" / "brand"


def install_icons():
    shutil.copy2(BRAND / "robot-head-32.png", ROOT / "favicon.png")
    shutil.copy2(BRAND / "robot-head-180.png", ROOT / "apple-touch-icon.png")
    print("favicon.png + apple-touch-icon.png")


def main():
    BRAND.mkdir(parents=True, exist_ok=True)
    install_icons()


if __name__ == "__main__":
    main()
