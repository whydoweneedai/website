#!/usr/bin/env python3
"""Generate /terms/ from site chrome."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_chrome import FONT, HEAD_ICONS, footer_html, head_scripts, header_nav, html_newsletter_attr
from site_data import load_site

ROOT = Path(__file__).resolve().parents[1]
EFFECTIVE = "2026-11-04"
EFFECTIVE_DISPLAY = "November 4, 2026"
URL = "https://whydoweneedai.com/terms/"


def main():
    site = load_site()
    nl = html_newsletter_attr(site["newsletter_active"])
    ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Terms of use",
        "url": URL,
        "dateModified": EFFECTIVE,
    }
    html = f"""<!DOCTYPE html>
<html lang="en"{nl}>
<head>
{head_scripts(False)}
{HEAD_ICONS}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Terms of use | Why Do We Need AI</title>
  <meta name="description" content="Terms of use for whydoweneedai.com: how you may use the site, our informational content, third-party links and ads, and the AI ReadyScore self-assessment.">
  <meta name="robots" content="index, follow">
  <meta name="twitter:site" content="@whydoweneedai">
  <meta name="theme-color" content="#2563eb">
  <link rel="canonical" href="{URL}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Why Do We Need AI">
  <meta property="og:title" content="Terms of use | Why Do We Need AI">
  <meta property="og:url" content="{URL}">
  <script type="application/ld+json">{json.dumps(ld)}</script>
{FONT}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
{header_nav()}
  <main class="article-main" id="main-content">
    <header class="article-header">
      <span class="eyebrow">Legal</span>
      <h1>Terms of use</h1>
      <p class="article-dek">Plain terms for using whydoweneedai.com and the tools we publish here.</p>
      <div class="article-meta"><span>Effective {EFFECTIVE_DISPLAY}</span></div>
    </header>
    <article class="article-body">
      <h2>Using this site</h2>
      <p>Why Do We Need AI (whydoweneedai.com) is an informational publication. By using the site, you agree to these terms. If you do not agree, please do not use the site.</p>

      <h2>Informational content only</h2>
      <p>Articles, guides, tests, and tools on this site are for general information. They are not legal, financial, tax, medical, or other professional advice. You are responsible for your own decisions and for verifying anything that matters to your business or situation.</p>

      <h2>AI-assisted content</h2>
      <p>Some research, drafting, or editing may use AI tools under human review. We aim for accuracy and practical usefulness; see our <a href="/editorial-policy/">editorial policy</a> for how we work.</p>

      <h2>Accuracy and corrections</h2>
      <p>We update content when we learn something is wrong or outdated. If you spot an error, please <a href="/contact/">contact us</a>.</p>

      <h2>Third-party links and advertising</h2>
      <p>The site may link to other websites or show ads served by third parties, including Google AdSense. We do not control those sites or services and are not responsible for their content, policies, or practices.</p>

      <h2>AI ReadyScore</h2>
      <p>The AI ReadyScore quiz is a self-assessment for your own planning. Results are suggestions, not guarantees. Submitting the quiz may send the information you provide to us as described in our <a href="/privacy/">privacy policy</a>.</p>

      <h2>Intellectual property</h2>
      <p>Unless we say otherwise, Why Do We Need AI owns the site’s branding, layout, and original content. You may link to our pages and quote short excerpts with attribution. You may not scrape, republish, or resell our content without permission.</p>

      <h2>Limitation of liability</h2>
      <p>The site is provided “as is.” To the fullest extent permitted by law, Why Do We Need AI is not liable for any loss or damage arising from your use of the site, reliance on its content, or issues with linked or third-party services.</p>

      <h2>Changes</h2>
      <p>We may update these terms. The effective date above will change when we publish material updates.</p>

      <h2>Contact</h2>
      <p>Questions about these terms: use the <a href="/contact/">contact page</a>.</p>
    </article>
  </main>
{footer_html()}
</body>
</html>
"""
    out = ROOT / "terms/index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("terms ok")


if __name__ == "__main__":
    main()
