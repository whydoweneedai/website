#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_chrome import FONT, HEAD_ICONS, footer_html, head_scripts, header_nav, html_newsletter_attr
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
  <title>Subscribed | Why Do We Need AI?</title>
  <link rel="canonical" href="https://whydoweneedai.com/subscribe/thanks/">
  <meta name="twitter:site" content="@whydoweneedai">
{FONT}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
{header_nav()}
  <main class="page-main" id="main-content">
    <header class="article-header">
      <h1>Thanks for subscribing</h1>
      <p class="article-dek">Newsletter signup is not active yet. When we launch, you will hear from us at the email you provided.</p>
    </header>
  </main>
{footer_html()}
</body>
</html>
"""
    (ROOT / "subscribe/thanks/index.html").write_text(html)
    print("subscribe/thanks ok")


if __name__ == "__main__":
    main()
