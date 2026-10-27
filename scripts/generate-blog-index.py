#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = sorted(json.loads((ROOT / "scripts/articles.json").read_text()), key=lambda a: a["date"], reverse=True)

filters = [
    ("all", "All topics", None),
    ("tested", "Tested", "tested"),
    ("choosing-ai-tools", "Choosing AI tools", "choosing-ai-tools"),
    ("automation-workflows", "Automation & workflows", "automation-workflows"),
    ("roi-planning", "ROI & planning", "roi-planning"),
    ("risk-data", "Risk, data & permissions", "risk-data"),
]

filter_links = []
for slug, label, topic in filters:
    if slug == "all":
        filter_links.append(f'<a href="/blog/" aria-current="true">{label}</a>')
    else:
        filter_links.append(f'<a href="/topics/{slug}/">{label}</a>')

items = []
for a in META:
    s = a["slug"]
    items.append(f"""        <article class="archive-item" data-topic="{a['topic']}">
          <a class="archive-item-thumb" href="/blog/{s}/" tabindex="-1" aria-hidden="true">
            <picture>
              <source type="image/webp" srcset="/images/hero/{s}-480.webp 480w, /images/hero/{s}-960.webp 960w" sizes="160px">
              <img src="/images/hero/{s}-960.webp" width="960" height="540" alt="" loading="lazy" decoding="async">
            </picture>
          </a>
          <div>
            <a class="topic-label" href="/topics/{a['topic']}/">{a['topicLabel']}</a>
            <h2><a href="/blog/{s}/">{a['searchTitle']}</a></h2>
            <p class="post-meta"><time datetime="{a['date']}">{a['date']}</time> · {a['readMin']}-min read</p>
            <p>{a['searchDek']}</p>
          </div>
        </article>""")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-GLNJLNSFEL"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-GLNJLNSFEL');
  </script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3631010450044967" crossorigin="anonymous"></script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="google-adsense-account" content="ca-pub-3631010450044967">
  <title>Archive | Why Do We Need AI?</title>
  <meta name="description" content="Full archive of practical AI guides and documented tests for small-business owners.">
  <link rel="canonical" href="https://whydoweneedai.com/blog/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Archive | Why Do We Need AI?">
  <meta property="og:url" content="https://whydoweneedai.com/blog/">
  <meta property="og:image" content="https://whydoweneedai.com/website_logo.png">
  <meta name="twitter:site" content="@whydoweneedai">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet"></noscript>
  <link rel="stylesheet" href="/blog/styles.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
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
  <main class="page-main" id="main-content">
    <header class="topic-hero">
      <p class="eyebrow">Archive</p>
      <h1>Practical AI. No jargon required.</h1>
      <p>Every guide and documented test, newest first. Filter by topic or <a href="/search/">search the archive</a>.</p>
    </header>
    <nav class="archive-filters" aria-label="Filter by topic">
      {' '.join(filter_links)}
    </nav>
    <div class="archive-list">
{chr(10).join(items)}
    </div>
    <aside class="module-readyscore" style="margin:2rem 0 3rem">
      <h2 class="module-title">AI ReadyScore</h2>
      <p>Free 3-minute self-assessment—see where AI fits your business before another subscription.</p>
      <a class="button button--secondary" href="/ai-readyscore/">Take AI ReadyScore</a>
    </aside>
  </main>
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
          <a href="/blog/" aria-current="page">Archive</a>
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
</body>
</html>
"""

(ROOT / "blog/index.html").write_text(html)
print("blog index ok")
