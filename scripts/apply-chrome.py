#!/usr/bin/env python3
"""Replace legacy header/footer/fonts on static pages (not articles, not assessment)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FONT_OLD = re.compile(
    r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?<link rel="stylesheet" href="/blog/styles.css">',
    re.DOTALL,
)
FONT_NEW = """<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet"></noscript>
  <link rel="stylesheet" href="/blog/styles.css">"""

HEADER_OLD = re.compile(r'<header class="site-header">.*?</header>', re.DOTALL)
HEADER_NEW = """<header class="site-header">
    <nav class="nav-inner" aria-label="Primary navigation">
      <a class="brand" href="/"><img class="brand-logo" src="/website_logo.png" alt="WhyDoWeNeedAI" width="1407" height="768" decoding="async"><span class="brand-text">WhyDoWeNeedAI</span></a>
      <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-nav-panel">Menu</button>
      <div class="nav-panel" id="site-nav-panel">
        <div class="nav-links">
          <a href="/topics/tested/">Tested</a>
          <a href="/topics/choosing-ai-tools/">Choosing tools</a>
          <a href="/topics/automation-workflows/">Automation</a>
          <a href="/topics/roi-planning/">ROI &amp; planning</a>
          <a href="/topics/risk-data/">Risk &amp; data</a>
          <a href="/search/">Search</a>
          <a href="/about/">About</a>
          <a class="nav-cta" href="/ai-readyscore/">AI ReadyScore</a>
        </div>
      </div>
    </nav>
  </header>"""

FOOTER_OLD = re.compile(r'<footer class="site-footer">.*?</footer>', re.DOTALL)
FOOTER_NEW = """<footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <p class="footer-tagline">Practical AI for small business — researched and plainly answered.</p>
        <p class="footer-copy">© WhyDoWeNeedAI</p>
      </div>
      <nav class="footer-nav" aria-label="Footer">
        <div class="footer-col">
          <p class="footer-col-title">Topics</p>
          <a href="/topics/tested/">Tested</a>
          <a href="/topics/choosing-ai-tools/">Choosing AI tools</a>
          <a href="/topics/automation-workflows/">Automation &amp; workflows</a>
          <a href="/topics/roi-planning/">ROI &amp; planning</a>
          <a href="/topics/risk-data/">Risk, data &amp; permissions</a>
        </div>
        <div class="footer-col">
          <p class="footer-col-title">Publication</p>
          <a href="/blog/">Archive</a>
          <a href="/about/">About</a>
          <a href="/editorial-policy/">Editorial policy</a>
          <a href="/contact/">Contact</a>
          <a href="/privacy/">Privacy</a>
          <a href="/ai-readyscore/">AI ReadyScore</a>
        </div>
      </nav>
    </div>
  </footer>
  <script src="/blog/site.js" defer></script>"""

PATHS = [
    "about/index.html",
    "contact/index.html",
    "contact/thanks/index.html",
    "editorial-policy/index.html",
    "privacy/index.html",
    "ai-readyscore/index.html",
]

ADSENSE_SNIPPET = """  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3631010450044967" crossorigin="anonymous"></script>
"""


def ensure_adsense(html: str) -> str:
    if "adsbygoogle" in html:
        return html
    return html.replace("</script>\n\n  <meta charset", f"</script>\n\n{ADSENSE_SNIPPET}\n  <meta charset", 1)


def process(path: Path):
    html = path.read_text()
    html = FONT_OLD.sub(FONT_NEW, html)
    html = HEADER_OLD.sub(HEADER_NEW, html)
    html = FOOTER_OLD.sub(FOOTER_NEW, html)
    html = ensure_adsense(html)
    if "/blog/site.js" not in html and "</body>" in html:
        html = html.replace("</body>", "  <script src=\"/blog/site.js\" defer></script>\n</body>")
    path.write_text(html)
    print("chrome", path)


def main():
    for rel in PATHS:
        p = ROOT / rel
        if p.exists():
            process(p)


if __name__ == "__main__":
    main()
