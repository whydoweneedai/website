#!/usr/bin/env python3
"""Replace legacy header/footer/fonts on static pages (not articles, not assessment)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_chrome import FONT, HEAD_ICONS, footer_html, header_nav
from site_data import load_site
from site_chrome import html_newsletter_attr

ROOT = Path(__file__).resolve().parents[1]

FONT_OLD = re.compile(
    r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?<link rel="stylesheet" href="/blog/styles.css">',
    re.DOTALL,
)

HEADER_OLD = re.compile(r'<header class="site-header">.*?</header>', re.DOTALL)
FOOTER_OLD = re.compile(r'<footer class="site-footer">.*?</footer>\s*(<script src="/blog/site.js" defer></script>)?', re.DOTALL)

ADSENSE_SNIPPET = """  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3631010450044967" crossorigin="anonymous"></script>
"""

PATHS = [
    "about/index.html",
    "contact/index.html",
    "contact/thanks/index.html",
    "editorial-policy/index.html",
    "privacy/index.html",
    "ai-readyscore/index.html",
    "search/index.html",
    "subscribe/thanks/index.html",
]


def ensure_adsense(html: str) -> str:
    if "adsbygoogle" in html:
        return html
    return html.replace("</script>\n\n  <meta charset", f"</script>\n\n{ADSENSE_SNIPPET}\n  <meta charset", 1)


def ensure_newsletter_attr(html: str) -> str:
    site = load_site()
    attr = html_newsletter_attr(site["newsletter_active"])
    if "data-newsletter" in html[:300]:
        return html
    return re.sub(r"<html lang=\"en\">", f"<html lang=\"en\"{attr}>", html, count=1)


def inject_icons(html: str) -> str:
    if "favicon.png" in html:
        return html
    return html.replace("<head>", f"<head>\n{HEAD_ICONS}", 1)


def process(path: Path):
    html = path.read_text()
    html = FONT_OLD.sub(FONT, html)
    html = inject_icons(html)
    html = HEADER_OLD.sub(header_nav(), html)
    html = FOOTER_OLD.sub(footer_html(), html)
    html = ensure_adsense(html)
    html = ensure_newsletter_attr(html)
    path.write_text(html)
    print("chrome", path)


def main():
    for rel in PATHS:
        p = ROOT / rel
        if p.exists():
            process(p)


if __name__ == "__main__":
    main()
