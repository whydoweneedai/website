#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_data import load_site, topic_href
from site_chrome import (
    FONT,
    HEAD_ANALYTICS,
    footer_html,
    header_nav,
    html_newsletter_attr,
    newsletter_home_block,
)

ROOT = Path(__file__).resolve().parents[1]


def card_media(art, lazy=True):
    slug = art["slug"]
    if art.get("hero") == "typographic":
        return ""
    loading = 'loading="lazy" decoding="async"' if lazy else 'loading="eager" fetchpriority="high"'
    return f"""<div class="card-media"><picture><source type="image/webp" srcset="/images/hero/{slug}-480.webp 480w, /images/hero/{slug}-960.webp 960w" sizes="320px"><img src="/images/hero/{slug}-960.webp" width="960" height="540" alt="{art['imageAlt']}" {loading}></picture></div>"""


def lead_media(art):
    slug = art["slug"]
    if art.get("hero") == "typographic":
        return f"""<div class="lead-story-media lead-story-media--typographic">
          <div class="hero-fallback" role="img" aria-label="{art['imageAlt']}">{art['searchTitle']}</div>
        </div>"""
    return f"""<div class="lead-story-media">
          <a href="/blog/{slug}/">
            <picture>
              <source type="image/webp" srcset="/images/hero/{slug}-480.webp 480w, /images/hero/{slug}-960.webp 960w, /images/hero/{slug}-1280.webp 1280w" sizes="(min-width: 960px) 560px, 100vw">
              <img src="/images/hero/{slug}-1280.jpg" width="1280" height="720" alt="{art['imageAlt']}" loading="eager" fetchpriority="high">
            </picture>
          </a>
        </div>"""


def topic_card(t, topic_pages):
    href = topic_href(t["slug"], topic_pages)
    return f"""<article class="card"><a class="card-link" href="{href}"><h3 class="card-title">{t['name']}</h3><p class="card-dek">{t['intro'].split('.')[0]}.</p></a></article>"""


def main():
    site = load_site()
    hp = site["raw"]["homepage"]
    by = site["by_slug"]
    topic_pages = site["topic_pages"]
    lead = by[hp["leadSlug"]]
    lead_href = topic_href(lead["topic"], topic_pages)
    nl_attr = html_newsletter_attr(site["newsletter_active"])

    latest_cards = []
    for slug in hp["latestSlugs"]:
        a = by[slug]
        latest_cards.append(
            f"""<article class="card card--standard">
          <a class="card-link" href="/blog/{slug}/">
            {card_media(a)}
            <div class="card-body"><span class="topic-label">{a['topicLabel']}</span><h3 class="card-title">{a['searchTitle']}</h3><p class="card-dek">{a['searchDek']}</p></div>
          </a>
        </article>"""
        )

    pick_cards = []
    for slug in hp["editorsPickSlugs"]:
        a = by[slug]
        media = card_media(a)
        body_intro = a["searchDek"] if a.get("hero") != "typographic" else "Which subscription matches which job—screenshot hero coming."
        pick_cards.append(
            f"""<article class="card card--standard">
          <a class="card-link" href="/blog/{slug}/">
            {media}
            <div class="card-body"><h3 class="card-title">{a['searchTitle']}</h3><p class="card-dek">{body_intro}</p></div>
          </a>
        </article>"""
        )

    topic_cards = "\n        ".join(topic_card(t, topic_pages) for t in site["raw"]["topics"])

    og_image = "https://whydoweneedai.com/website_logo.png"
    if lead.get("hero") == "illustration":
        og_image = f"https://whydoweneedai.com/images/hero/{lead['slug']}-1280.jpg"

    html = f"""<!DOCTYPE html>
<html lang="en"{nl_attr}>
<head>
{HEAD_ANALYTICS}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="google-adsense-account" content="ca-pub-3631010450044967">
  <title>Why Do We Need AI? | Practical AI for small business</title>
  <meta name="description" content="Which AI is worth it for your business—researched and plainly answered. Practical guides, documented tests, and decision tools for small-business owners.">
  <meta name="author" content="whydoweneedai.com">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#2563eb">
  <link rel="canonical" href="https://whydoweneedai.com/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Why Do We Need AI">
  <meta property="og:title" content="Why Do We Need AI? | Practical AI for small business">
  <meta property="og:description" content="Which AI is worth it for your business—researched and plainly answered.">
  <meta property="og:url" content="https://whydoweneedai.com/">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:site" content="@whydoweneedai">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Why Do We Need AI?">
  <meta name="twitter:description" content="Practical AI for small business—researched and plainly answered.">
  <meta name="twitter:image" content="{og_image}">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Why Do We Need AI?",
    "url": "https://whydoweneedai.com/",
    "description": "A practical AI publication for small-business owners with documented tests and plain-English guides.",
    "publisher": {{
      "@type": "Organization",
      "name": "Why Do We Need AI",
      "url": "https://whydoweneedai.com/",
      "logo": {{ "@type": "ImageObject", "url": "https://whydoweneedai.com/website_logo.png" }}
    }}
  }}
  </script>
{FONT}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
{header_nav("/")}
  <main class="page-main" id="main-content">
    <header class="masthead">
      <p class="eyebrow">Why Do We Need AI</p>
      <h1 class="masthead-tagline">Which AI is worth it for your business, researched and plainly answered.</h1>
      <p class="masthead-sub">Practical AI. No jargon required.</p>
    </header>

    <section class="home-section" aria-labelledby="lead-title">
      <div class="section-header">
        <h2 id="lead-title" class="section-title">Lead story</h2>
      </div>
      <article class="lead-story">
        {lead_media(lead)}
        <div>
          <a class="topic-label" href="{lead_href}">{lead['topicLabel']}</a>
          <h2><a href="/blog/{lead['slug']}/">{lead['searchTitle']}</a></h2>
          <p class="lead-dek">{lead['searchDek']}</p>
          <p class="post-meta"><time datetime="{lead['date']}">{lead['date']}</time></p>
          <a class="button" href="/blog/{lead['slug']}/">Read the comparison</a>
        </div>
      </article>
    </section>

    <section class="home-section" aria-labelledby="latest-title">
      <div class="section-header">
        <h2 id="latest-title" class="section-title">Latest</h2>
      </div>
      <div class="card-grid">
        {chr(10).join(latest_cards)}
      </div>
    </section>

    <section class="home-section" aria-labelledby="picks-title">
      <div class="section-header">
        <h2 id="picks-title" class="section-title">Editor's picks</h2>
        <p class="section-intro">Start with the pieces readers return to most.</p>
      </div>
      <div class="card-grid card-grid--picks">
        {chr(10).join(pick_cards)}
      </div>
    </section>

    <section class="home-section" aria-labelledby="topics-title">
      <div class="section-header">
        <h2 id="topics-title" class="section-title">Browse by topic</h2>
      </div>
      <div class="card-grid">
        {topic_cards}
      </div>
      <p style="margin-top:1.5rem"><a class="read-link" href="/blog/">Full archive</a></p>
    </section>

    <section class="home-section" aria-labelledby="readyscore-title">
      <aside class="module-readyscore">
        <h2 id="readyscore-title" class="module-title">Take the 3-minute AI ReadyScore</h2>
        <p>A short self-assessment to see where AI fits your business today—before another subscription or pilot.</p>
        <a class="button button--secondary" href="/ai-readyscore/">Start AI ReadyScore</a>
      </aside>
    </section>

{newsletter_home_block()}
  </main>

{footer_html()}
  <script>
  (function () {{
    var hash = window.location.hash;
    if (!hash || hash === "#") return;
    var quizHashes = ["#app", "#quiz", "#assessment"];
    if (quizHashes.indexOf(hash.toLowerCase()) !== -1) {{
      window.location.replace("/ai-readyscore/" + hash);
    }}
  }})();
  </script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html)
    print("homepage ok")


if __name__ == "__main__":
    main()
