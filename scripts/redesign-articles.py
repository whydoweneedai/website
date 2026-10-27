#!/usr/bin/env python3
"""Rebuild article page chrome without changing article-body HTML."""
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "scripts/articles.json").read_text())
BY_SLUG = {a["slug"]: a for a in META}
ORDERED = sorted(META, key=lambda a: a["date"], reverse=True)

FONT = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&amp;display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&amp;display=swap" rel="stylesheet"></noscript>"""

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


def header_nav():
    return """<header class="site-header">
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


def footer_html():
    return """<footer class="site-footer">
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


def hero_picture(slug: str, alt: str, eager: bool = True):
    base = f"/images/hero/{slug}"
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f"""<figure class="article-hero">
  <picture>
    <source type="image/webp" srcset="{base}-480.webp 480w, {base}-960.webp 960w, {base}-1280.webp 1280w" sizes="(min-width: 960px) 860px, 100vw">
    <img src="{base}-1280.jpg" srcset="{base}-480.webp 480w, {base}-960.webp 960w, {base}-1280.jpg 1280w" sizes="(min-width: 960px) 860px, 100vw" width="1280" height="720" alt="{alt}" {loading}>
  </picture>
</figure>"""


def read_next_cards(slug: str):
    art = BY_SLUG[slug]
    topic = art["topic"]
    same = [a for a in ORDERED if a["slug"] != slug and a["topic"] == topic]
    other = [a for a in ORDERED if a["slug"] != slug and a["topic"] != topic]
    picks = (same + other)[:3]
    cards = []
    for p in picks:
        cards.append(
            f"""<article class="card card--compact read-next-card">
  <a class="card-link" href="/blog/{p['slug']}/">
    <span class="topic-label">{p['topicLabel']}</span>
    <h3 class="card-title">{p['searchTitle']}</h3>
    <p class="card-dek">{p['searchDek']}</p>
  </a>
</article>"""
        )
    return "\n".join(cards)


def article_extras(slug: str, topic: str, topic_label: str):
    url = f"https://whydoweneedai.com/blog/{slug}/"
    enc = quote(url, safe="")
    return f"""
<aside class="article-share" aria-label="Share this article">
  <p class="article-share-label">Share</p>
  <div class="share-actions">
    <button type="button" class="share-btn" data-share-copy data-share-url="{url}">Copy link</button>
    <a class="share-btn" href="https://twitter.com/intent/tweet?url={enc}" rel="noopener noreferrer" target="_blank">X</a>
    <a class="share-btn" href="https://www.linkedin.com/sharing/share-offsite/?url={enc}" rel="noopener noreferrer" target="_blank">LinkedIn</a>
    <a class="share-btn" href="mailto:?subject=Why%20Do%20We%20Need%20AI&amp;body={enc}">Email</a>
  </div>
</aside>
<section class="read-next" aria-labelledby="read-next-{slug}">
  <h2 id="read-next-{slug}" class="section-title">Read next</h2>
  <div class="read-next-grid">
{read_next_cards(slug)}
  </div>
  <p class="topic-more"><a href="/topics/{topic}/">More in {topic_label} →</a></p>
</section>
<div class="article-end-modules">
  <aside class="module-readyscore" aria-labelledby="rs-{slug}">
    <h2 id="rs-{slug}" class="module-title">AI ReadyScore</h2>
    <p>Take the free 3-minute self-assessment to see where AI fits your business today.</p>
    <a class="button button--secondary" href="/ai-readyscore/">Take AI ReadyScore</a>
  </aside>
  <aside class="newsletter-compact" aria-labelledby="nl-{slug}">
    <h2 id="nl-{slug}" class="module-title">Newsletter</h2>
    <p>One useful email when we publish: what we tested, what worked, and which AI is worth paying for. No hype. Unsubscribe anytime.</p>
    <form name="newsletter" method="POST" action="/subscribe/thanks/" data-netlify="true" netlify-honeypot="bot-field" class="newsletter-form newsletter-form--compact">
      <input type="hidden" name="form-name" value="newsletter">
      <p class="hidden-field" hidden><label>Leave blank <input name="bot-field"></label></p>
      <label class="newsletter-label" for="email-{slug}">Email</label>
      <div class="newsletter-row">
        <input id="email-{slug}" type="email" name="email" required autocomplete="email" placeholder="you@company.com">
        <button type="submit" class="button">Subscribe</button>
      </div>
    </form>
  </aside>
</div>"""


def replace_images(html: str, slug: str) -> str:
    img_url = f"https://whydoweneedai.com/images/hero/{slug}-1280.jpg"
    html = re.sub(
        r'<meta property="og:image" content="[^"]*">',
        f'<meta property="og:image" content="{img_url}">',
        html,
    )
    html = re.sub(
        r'<meta name="twitter:image" content="[^"]*">',
        f'<meta name="twitter:image" content="{img_url}">',
        html,
    )
    html = re.sub(
        r'"image": "https://whydoweneedai.com/website_logo.png"',
        f'"image": "{img_url}"',
        html,
    )
    return html


def replace_eyebrow(header: str, topic: str, label: str) -> str:
    return re.sub(
        r'<span class="eyebrow">[^<]*</span>',
        f'<a class="topic-label" href="/topics/{topic}/">{label}</a>',
        header,
        count=1,
    )


def process_file(path: Path):
    slug = path.parent.name
    art = BY_SLUG.get(slug)
    if not art:
        print("skip", slug)
        return
    html = path.read_text()
    m_body = re.search(r"(<article class=\"article-body\">.*?</article>)", html, re.DOTALL)
    m_header = re.search(r"(<header class=\"article-header\">.*?</header>)", html, re.DOTALL)
    m_nav = re.search(r"<nav class=\"article-nav\".*?</nav>", html, re.DOTALL)
    m_title = re.search(r"<title>([^<]+)</title>", html)
    if not m_body or not m_header or not m_title:
        print("parse fail", slug)
        return

    article_body = m_body.group(1)
    article_header = replace_eyebrow(m_header.group(1), art["topic"], art["topicLabel"])
    article_nav = m_nav.group(0) if m_nav else ""

    # Preserve everything in head except fonts
    head = re.search(r"<head>(.*?)</head>", html, re.DOTALL).group(1)
    head = re.sub(r"<link rel=\"preconnect\".*?<noscript>.*?</noscript>", FONT, head, flags=re.DOTALL)
    head = replace_images(head, slug)

    breadcrumb_short = art["searchTitle"][:40] + ("…" if len(art["searchTitle"]) > 40 else "")
    hero = hero_picture(slug, art["imageAlt"])
    extras = article_extras(slug, art["topic"], art["topicLabel"])

    out = f"""<!DOCTYPE html><html lang="en"><head>
{HEAD_ANALYTICS}{head}</head><body>
<a class="skip-link" href="#main-content">Skip to content</a>
{header_nav()}
<main class="article-main" id="main-content">
<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true"> / </span><a href="/blog/">Archive</a><span aria-hidden="true"> / </span><a href="/topics/{art['topic']}/">{art['topicLabel']}</a><span aria-hidden="true"> / </span><span>{breadcrumb_short}</span></nav>
{article_header}
{hero}
<nav class="article-toc" id="article-toc" aria-label="Table of contents" hidden></nav>
{article_body}
{extras}
{article_nav}
</main>
{footer_html()}
</body></html>"""

    path.write_text(out)
    print("ok", slug)


def main():
    for art in META:
        p = ROOT / "blog" / art["slug"] / "index.html"
        if p.exists():
            process_file(p)


if __name__ == "__main__":
    main()
