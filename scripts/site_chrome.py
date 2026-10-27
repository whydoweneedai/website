#!/usr/bin/env python3
"""Shared HTML chrome fragments driven by data/site.json."""
from site_data import load_site, topic_href

HEAD_ANALYTICS = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-GLNJLNSFEL"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-GLNJLNSFEL');
  </script>

  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3631010450044967" crossorigin="anonymous"></script>
"""

HEAD_ICONS = """  <link rel="icon" href="/favicon.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">"""

FONT = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Nunito:wght@800;900&amp;display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Nunito:wght@800;900&amp;display=swap" rel="stylesheet"></noscript>
  <link rel="stylesheet" href="/blog/styles.css">"""


def html_newsletter_attr(active: bool) -> str:
    return ' data-newsletter="on"' if active else ' data-newsletter="off"'


def wordmark_img(css_class: str = "brand-wordmark") -> str:
    return f"""<picture>
      <source type="image/webp" srcset="/images/brand/logo-wordmark.webp 1x, /images/brand/logo-wordmark@2x.webp 2x">
      <img class="{css_class}" src="/images/brand/logo-wordmark.png" srcset="/images/brand/logo-wordmark.png 1x, /images/brand/logo-wordmark@2x.png 2x" width="907" height="166" alt="WhyDoWeNeedAI" decoding="async">
    </picture>"""


def mascot_img(size: str = "md", decorative: bool = True) -> str:
    """size: sm | md | lg"""
    cls = f"brand-mascot brand-mascot--{size}"
    hidden = ' aria-hidden="true"' if decorative else ""
    return f"""<img class="{cls}" src="/images/brand/logo-mascot.webp" srcset="/images/brand/logo-mascot.webp 1x, /images/brand/logo-mascot@2x.webp 2x" width="531" height="522" alt=""{hidden} loading="lazy" decoding="async">"""


def header_nav(current_path: str = "") -> str:
    site = load_site()
    topic_pages = site["topic_pages"]
    links = []
    for t in site["raw"]["topics"]:
        href = topic_href(t["slug"], topic_pages)
        label = t["name"]
        if t["slug"] == "choosing-ai-tools":
            label = "Choosing tools"
        elif t["slug"] == "automation-workflows":
            label = "Automation"
        elif t["slug"] == "roi-planning":
            label = "ROI &amp; planning"
        elif t["slug"] == "risk-data":
            label = "Risk &amp; data"
        cur = ' aria-current="page"' if current_path == href else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    nav_topics = "\n        ".join(links)
    return f"""<header class="site-header">
  <nav class="nav-inner" aria-label="Primary navigation">
    <a class="brand" href="/">{wordmark_img()}</a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-nav-panel">Menu</button>
    <div class="nav-panel" id="site-nav-panel">
      <div class="nav-links">
        {nav_topics}
        <a href="/search/">Search</a>
        <a href="/about/">About</a>
        <a class="nav-cta" href="/ai-readyscore/">AI ReadyScore</a>
      </div>
    </div>
  </nav>
</header>"""


def footer_html() -> str:
    site = load_site()
    topic_pages = site["topic_pages"]
    topic_links = []
    for t in site["raw"]["topics"]:
        href = topic_href(t["slug"], topic_pages)
        topic_links.append(f'<a href="{href}">{t["name"]}</a>')
    topics_col = "\n        ".join(topic_links)
    return f"""<footer class="site-footer">
  <div class="footer-inner">
    <div class="footer-brand">
      {mascot_img("sm")}
      <p class="footer-tagline">Practical AI for small business — researched and plainly answered.</p>
      <p class="footer-copy">© WhyDoWeNeedAI</p>
    </div>
    <nav class="footer-nav" aria-label="Footer">
      <div class="footer-col">
        <p class="footer-col-title">Topics</p>
        {topics_col}
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


NEWSLETTER_COPY = "One useful email when we publish: what we tested, what worked, and which AI is worth paying for. No hype. Unsubscribe anytime."


def newsletter_home_block() -> str:
    return f"""    <section class="home-section newsletter-block" aria-labelledby="newsletter-title">
      <div class="newsletter-block-inner">
        {mascot_img("md")}
        <div>
          <h2 id="newsletter-title" class="section-title">Newsletter</h2>
          <p>{NEWSLETTER_COPY}</p>
          <p class="newsletter-soon" role="status">Newsletter launching soon.</p>
          <form class="newsletter-form" name="newsletter" aria-hidden="true">
            <label class="newsletter-label" for="newsletter-email">Email address</label>
            <div class="newsletter-row">
              <input id="newsletter-email" type="email" name="email" disabled autocomplete="email" placeholder="you@company.com">
              <button type="button" class="button" disabled>Subscribe</button>
            </div>
          </form>
        </div>
      </div>
    </section>"""


def newsletter_article_block(slug: str) -> str:
    return f"""  <aside class="newsletter-compact" aria-labelledby="nl-{slug}">
    {mascot_img("sm")}
    <h2 id="nl-{slug}" class="module-title">Newsletter</h2>
    <p>{NEWSLETTER_COPY}</p>
    <p class="newsletter-soon" role="status">Newsletter launching soon.</p>
    <form class="newsletter-form newsletter-form--compact" name="newsletter" aria-hidden="true">
      <label class="newsletter-label" for="email-{slug}">Email</label>
      <div class="newsletter-row">
        <input id="email-{slug}" type="email" name="email" disabled autocomplete="email" placeholder="you@company.com">
        <button type="button" class="button" disabled>Subscribe</button>
      </div>
    </form>
  </aside>"""


def readyscore_module(title_id: str = "readyscore-title", compact: bool = False) -> str:
    cls = "module-readyscore"
    if compact:
        cls += " module-readyscore--compact"
    return f"""<aside class="{cls}" aria-labelledby="{title_id}">
  {mascot_img("md")}
  <div class="module-readyscore-copy">
    <h2 id="{title_id}" class="module-title">Take the 3-minute AI ReadyScore</h2>
    <p>A short self-assessment to see where AI fits your business today—before another subscription or pilot.</p>
    <a class="button button--secondary" href="/ai-readyscore/">Start AI ReadyScore</a>
  </div>
</aside>"""
