#!/usr/bin/env python3
"""Set og:image and twitter:image on static marketing pages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://whydoweneedai.com"

PAGES = {
    "about/index.html": f"{ORIGIN}/images/og/about.png",
    "ai-readyscore/index.html": f"{ORIGIN}/images/og/ai-readyscore.png",
}


def patch(path: Path, image_url: str):
    html = path.read_text()
    html = re.sub(
        r'<meta property="og:image" content="[^"]*">',
        f'<meta property="og:image" content="{image_url}">',
        html,
        count=1,
    )
    if 'name="twitter:image"' in html:
        html = re.sub(
            r'<meta name="twitter:image" content="[^"]*">',
            f'<meta name="twitter:image" content="{image_url}">',
            html,
            count=1,
        )
    elif 'name="twitter:card"' in html:
        html = html.replace(
            '<meta name="twitter:card"',
            f'<meta name="twitter:image" content="{image_url}">\n<meta name="twitter:card"',
            1,
        )
    else:
        html = html.replace(
            '<meta name="twitter:site"',
            f'<meta name="twitter:image" content="{image_url}">\n<meta name="twitter:site"',
            1,
        )
    path.write_text(html)
    print("og meta", path.relative_to(ROOT))


def main():
    for rel, url in PAGES.items():
        p = ROOT / rel
        if p.exists():
            patch(p, url)


if __name__ == "__main__":
    main()
