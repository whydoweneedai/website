#!/usr/bin/env python3
"""Shared HTML chrome fragments driven by data/site.json."""
import re

from site_data import load_site

HEAD_GA = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-GLNJLNSFEL"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-GLNJLNSFEL');
  </script>
"""

HEAD_ADSENSE = """
  <!-- Google AdSense -->
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3631010450044967" crossorigin="anonymous"></script>
"""

# Back-compat alias for pages that include both
HEAD_ANALYTICS = HEAD_GA + HEAD_ADSENSE


def head_scripts(include_adsense: bool = False) -> str:
    if include_adsense:
        return HEAD_GA + HEAD_ADSENSE
    return HEAD_GA


HEAD_ICONS = """  <link rel="icon" href="/favicon.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
  <link rel="manifest" href="/site.webmanifest">"""

FONT = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Nunito:wght@800;900&amp;display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Nunito:wght@800;900&amp;display=swap" rel="stylesheet"></noscript>
  <link rel="stylesheet" href="/blog/styles.css">
  <link rel="stylesheet" href="/chrome.css">"""

FONT_BLOCK_RE = re.compile(
    r"\s*<link rel=\"preconnect\" href=\"https://fonts\.googleapis\.com\">"
    r".*?<link rel=\"stylesheet\" href=\"/blog/styles\.css\">",
    re.DOTALL | re.IGNORECASE,
)


def inject_font(html: str) -> str:
    """Idempotent: one canonical FONT block immediately before </head>."""
    html = FONT_BLOCK_RE.sub("", html)
    html = re.sub(
        r'<link rel="stylesheet" href="/blog/styles\.css">\s*',
        "",
        html,
        flags=re.IGNORECASE,
    )
    html = html.replace('<link rel="stylesheet" href="/chrome.css">', "")
    return html.replace("</head>", f"{FONT}\n</head>", 1)


def html_newsletter_attr(active: bool) -> str:
    return ' data-newsletter="on"' if active else ' data-newsletter="off"'


# Match .brand-lockup's 28px / 34px height and max-width constraints.
# The explicit ratio keeps each derivative's rounded pixel height from changing
# the layout while it decodes. Width/height attributes retain the fallback ratio.
HEADER_LOCKUP_SIZES = "(max-width: 640px) min(78vw, 149.625px), min(72vw, 181.6875px)"


def lockup_srcset(extension: str) -> str:
    return ", ".join(
        f"/images/brand/lockup-w{width}.{extension} {width}w"
        for width in (150, 182, 300, 364, 450, 546)
    ) + f", /images/brand/lockup-128.{extension} 684w"


def header_lockup() -> str:
    return f"""<picture>
      <source type="image/webp" srcset="{lockup_srcset('webp')}" sizes="{HEADER_LOCKUP_SIZES}">
      <img class="brand-lockup" src="/images/brand/lockup-w182.png" srcset="{lockup_srcset('png')}" sizes="{HEADER_LOCKUP_SIZES}" width="684" height="128" style="aspect-ratio:171 / 32" alt="WhyDoWeNeedAI" decoding="async">
    </picture>"""


def masthead_logo() -> str:
    return """<img class="masthead-logo" src="/website_logo.png" width="1407" height="768" alt="" aria-hidden="true" decoding="async">"""


def footer_logo() -> str:
    return """<img class="footer-logo" src="/website_logo.png" width="1407" height="768" alt="WhyDoWeNeedAI" loading="lazy" decoding="async">"""


def mascot_img(size: str = "md", decorative: bool = True) -> str:
    cls = f"brand-mascot brand-mascot--{size}"
    hidden = ' aria-hidden="true"' if decorative else ""
    return f"""<img class="{cls}" src="/images/brand/logo-mascot.png" width="531" height="522" alt=""{hidden} loading="lazy" decoding="async">"""


X_URL = "https://x.com/whydoweneedai"
XSVG = '<svg class="xicon" aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2H22l-6.8 7.8L23 22h-6.2l-4.8-6.3L6.4 22H3.3l7.3-8.3L1 2h6.3l4.4 5.8L18.9 2Zm-1.1 18h1.7L6.3 3.9H4.5L17.8 20Z"/></svg>'


def header_nav(current_path: str = "") -> str:
    blog_current = ' aria-current="page"' if current_path == "/blog/" else ""
    score_current = ' aria-current="page"' if current_path == "/ai-readyscore/" else ""
    return f"""<header class="site-header">
  <nav class="publication-nav" aria-label="Primary navigation">
    <a class="publication-brand" href="/"><img src="/images/brand/robot-head.png" width="38" height="38" alt=""><span>whydoweneed<b>ai</b></span></a>
    <div class="publication-links">
      <a href="/blog/"{blog_current}>Blog</a>
      <a href="/ai-readyscore/"{score_current}>ReadyScore</a>
    </div>
    <a class="publication-follow" href="{X_URL}">{XSVG} Follow on X</a>
    <details class="publication-menu">
      <summary aria-label="Menu"><span aria-hidden="true"></span></summary>
      <div>
        <a href="/blog/"{blog_current}>Blog</a>
        <a href="/ai-readyscore/"{score_current}>ReadyScore</a>
        <a href="{X_URL}">{XSVG} Follow on X</a>
      </div>
    </details>
  </nav>
</header>"""


def footer_html() -> str:
    return f"""<footer class="site-footer">
  <div class="publication-footer">
    <p>© WhyDoWeNeedAI · Practical AI for small business</p>
    <nav aria-label="Footer">
      <a href="/blog/">Blog</a>
      <a href="/ai-readyscore/">ReadyScore</a>
      <a href="{X_URL}">X</a>
      <a href="/about/">About</a>
      <a href="/editorial-policy/">Editorial policy</a>
      <a href="/contact/">Contact</a>
      <a href="/privacy/">Privacy</a>
      <a href="/terms/">Terms</a>
    </nav>
  </div>
</footer>
<script src="/blog/site.js" defer></script>"""


NEWSLETTER_COPY = "One useful email when we publish: what we tested, what worked, and which AI is worth paying for. No hype. Unsubscribe anytime."


def newsletter_home_block() -> str:
    if not load_site()["newsletter_active"]:
        return ""
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
    if not load_site()["newsletter_active"]:
        return ""
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
    <h2 id="{title_id}" class="module-title">AI ReadyScore</h2>
    <p>A short self-assessment to see where AI fits your business today—before another subscription or pilot.</p>
    <a class="button button--secondary" href="/ai-readyscore/">Find out where AI fits your business — free 2-minute AI ReadyScore self-assessment.</a>
  </div>
</aside>"""
