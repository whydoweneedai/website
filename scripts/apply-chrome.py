#!/usr/bin/env python3
"""Replace legacy header/footer/fonts on static pages (not articles, not assessment, not quiz)."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_chrome import FONT, HEAD_GA, HEAD_ICONS, footer_html, header_nav, html_newsletter_attr
from site_data import load_site

ROOT = Path(__file__).resolve().parents[1]

FONT_OLD = re.compile(
    r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?<link rel="stylesheet" href="/blog/styles.css">',
    re.DOTALL,
)

HEADER_OLD = re.compile(r'<header class="site-header">.*?</header>', re.DOTALL)
FOOTER_OLD = re.compile(r'<footer class="site-footer">.*?</footer>\s*(<script src="/blog/site.js" defer></script>)?', re.DOTALL)

ADSENSE_BLOCK = re.compile(
    r"\s*<!-- Google AdSense -->.*?pagead2\.googlesyndication\.com.*?</script>",
    re.DOTALL,
)
ADSENSE_SCRIPT = re.compile(
    r'<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^"]*"[^>]*></script>\s*',
    re.DOTALL,
)
ADSENSE_META = re.compile(r'\s*<meta name="google-adsense-account"[^>]*>\s*')

PATHS = [
    "about/index.html",
    "contact/index.html",
    "contact/thanks/index.html",
    "editorial-policy/index.html",
    "privacy/index.html",
]


def strip_adsense(html: str) -> str:
    html = ADSENSE_BLOCK.sub("", html)
    html = ADSENSE_SCRIPT.sub("", html)
    html = ADSENSE_META.sub("\n", html)
    return html


def ensure_ga_only(html: str) -> str:
    html = strip_adsense(html)
    if "G-GLNJLNSFEL" not in html:
        html = html.replace("<head>", f"<head>\n{HEAD_GA}", 1)
    return html


def ensure_newsletter_attr(html: str) -> str:
    site = load_site()
    attr = html_newsletter_attr(site["newsletter_active"])
    if "data-newsletter" in html[:300]:
        return html
    return re.sub(r'<html lang="en">', f'<html lang="en"{attr}>', html, count=1)


def inject_icons(html: str) -> str:
    if "favicon.png" not in html:
        return html.replace("<head>", f"<head>\n{HEAD_ICONS}", 1)
    if "site.webmanifest" not in html:
        html = html.replace(
            'rel="apple-touch-icon"',
            'rel="apple-touch-icon" sizes="180x180"',
            1,
        )
        html = html.replace(
            "/apple-touch-icon.png\">",
            '/apple-touch-icon.png">\n  <link rel="manifest" href="/site.webmanifest">',
            1,
        )
    return html


def process(path: Path):
    html = path.read_text()
    html = ensure_ga_only(html)
    html = FONT_OLD.sub(FONT, html)
    html = inject_icons(html)
    html = HEADER_OLD.sub(header_nav(), html)
    html = FOOTER_OLD.sub(footer_html(), html)
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
