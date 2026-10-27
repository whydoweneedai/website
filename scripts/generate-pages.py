#!/usr/bin/env python3
"""Generate topic pages, search page shell, and update sitemap entries."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = json.loads((ROOT / "scripts/articles.json").read_text())

TOPICS = {
    "tested": {
        "title": "Tested",
        "intro": "Documented experiments on invented data—what passed, what failed, and what still needs a person.",
    },
    "choosing-ai-tools": {
        "title": "Choosing AI tools",
        "intro": "Plain comparisons and decision tests so the right subscription matches the job you need done.",
    },
    "automation-workflows": {
        "title": "Automation & workflows",
        "intro": "Lifecycle maps, scorecards, and blueprints for follow-up, handoff, and repetitive work.",
    },
    "roi-planning": {
        "title": "ROI & planning",
        "intro": "Readiness checklists, pilot reviews, and conservative math before you scale a workflow.",
    },
    "risk-data": {
        "title": "Risk, data & permissions",
        "intro": "What to upload, what to keep out, and how to set rules before agents act in your apps.",
    },
}

HEAD = """  <!-- Google tag (gtag.js) -->
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

FONT = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet"></noscript>
  <link rel="stylesheet" href="/blog/styles.css">
"""

HEADER = """
  <header class="site-header">
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
  </header>
"""

FOOTER = """
  <footer class="site-footer">
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
  <script src="/blog/site.js" defer></script>
"""


def card_html(a, lazy=True):
    slug = a["slug"]
    loading = 'loading="lazy" decoding="async"' if lazy else 'loading="eager" fetchpriority="high"'
    return f"""<article class="card card--standard">
  <a class="card-link" href="/blog/{slug}/">
    <div class="card-media">
      <picture>
        <source type="image/webp" srcset="/images/hero/{slug}-480.webp 480w, /images/hero/{slug}-960.webp 960w" sizes="(min-width: 640px) 320px, 100vw">
        <img src="/images/hero/{slug}-960.webp" alt="{a['imageAlt']}" width="960" height="540" {loading}>
      </picture>
    </div>
    <div class="card-body">
      <div class="post-meta"><time datetime="{a['date']}">{a['date']}</time></div>
      <h2 class="card-title">{a['searchTitle']}</h2>
      <p class="card-dek">{a['searchDek']}</p>
    </div>
  </a>
</article>"""


def topic_page(slug, info):
    articles = [a for a in META if a["topic"] == slug]
    articles.sort(key=lambda x: x["date"], reverse=True)
    cards = "\n".join(card_html(a) for a in articles)
    url = f"https://whydoweneedai.com/topics/{slug}/"
    title = info["title"]
    intro = info["intro"]
    current = f' aria-current="page"' if slug else ""
    nav = HEADER.replace(
        f'href="/topics/{slug}/"',
        f'href="/topics/{slug}/"{current}',
        1,
    )
    ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": intro,
        "url": url,
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://whydoweneedai.com/"},
                {"@type": "ListItem", "position": 2, "name": title, "item": url},
            ],
        },
    }
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="google-adsense-account" content="ca-pub-3631010450044967">
  <title>{title} | Why Do We Need AI?</title>
  <meta name="description" content="{intro}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{intro}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://whydoweneedai.com/website_logo.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@whydoweneedai">
  <script type="application/ld+json">{json.dumps(ld)}</script>
{FONT}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
{nav}
  <main class="page-main" id="main-content">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true"> / </span><span>{title}</span></nav>
    <header class="topic-hero">
      <h1>{title}</h1>
      <p>{intro}</p>
    </header>
    <section class="home-section" aria-label="Articles">
      <div class="card-grid">
{cards}
      </div>
    </section>
  </main>
{FOOTER}
</body>
</html>
"""
    out = ROOT / "topics" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("topic", slug)


def main():
    for slug, info in TOPICS.items():
        topic_page(slug, info)


if __name__ == "__main__":
    main()
