#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_chrome import (
    FONT,
    head_scripts,
    HEAD_ICONS,
    footer_html,
    header_nav,
    html_newsletter_attr,
    mascot_img,
)
from site_data import load_site

ROOT = Path(__file__).resolve().parents[1]


def main():
    site = load_site()
    nl = html_newsletter_attr(site["newsletter_active"])
    html = f"""<!DOCTYPE html>
<html lang="en"{nl}>
<head>
{head_scripts(False)}
{HEAD_ICONS}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex,follow">
  <title>Page not found | Why Do We Need AI?</title>
{FONT}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
{header_nav()}
  <main class="page-main error-page" id="main-content">
    {mascot_img("lg")}
    <h1>Page not found</h1>
    <p class="article-dek">That URL doesn’t match anything on WhyDoWeNeedAI. Try the front page or search the archive.</p>
    <p><a class="button" href="/">Back to home</a> <a class="button button--secondary" href="/search/">Search articles</a></p>
  </main>
{footer_html()}
</body>
</html>
"""
    (ROOT / "404.html").write_text(html)
    print("404 ok")


if __name__ == "__main__":
    main()
