#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hero_markup import LOGO_OG, card_media, lead_media_link, og_image_url
from datetime import date

from site_data import format_display_date, load_site, topic_href
from site_chrome import (
    FONT,
    HEAD_ICONS,
    footer_html,
    head_scripts,
    header_nav,
    html_newsletter_attr,
    masthead_logo,
    newsletter_home_block,
    readyscore_module,
)

ROOT = Path(__file__).resolve().parents[1]


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
        pick_cards.append(
            f"""<article class="card card--standard">
          <a class="card-link" href="/blog/{slug}/">
            {card_media(a)}
            <div class="card-body"><h3 class="card-title">{a['searchTitle']}</h3><p class="card-dek">{a['searchDek']}</p></div>
          </a>
        </article>"""
        )

    topic_cards = "\n        ".join(
        topic_card(t, topic_pages) for t in site["raw"]["topics"] if t["slug"] in topic_pages
    )
    og_image = og_image_url(slug="home")
    built_dateline = f"{format_display_date(date.today().isoformat())} · Practical AI for small business"

    html = f"""<!DOCTYPE html>
<html lang="en"{nl_attr}>
<head>
{head_scripts(True)}
{HEAD_ICONS}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="google-adsense-account" content="ca-pub-3631010450044967">
  <title>Why Do We Need AI? | Practical AI for small business</title>
  <meta name="description" content="Which AI is worth it for your business—researched and plainly answered. Practical guides, documented tests, and decision tools for small-business owners.">
  <meta name="author" content="whydoweneedai.com">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#1f66b8">
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
      "logo": {{ "@type": "ImageObject", "url": "{LOGO_OG}" }}
    }}
  }}
  </script>
{FONT}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
{header_nav("/")}
  <div class="pub-dateline-bar" aria-hidden="false">
    <p class="pub-dateline" id="pub-dateline">{built_dateline}</p>
  </div>
  <main class="page-main" id="main-content">
    <header class="masthead">
      <div class="masthead-inner">
        {masthead_logo()}
        <div class="masthead-copy">
          <h1 class="masthead-tagline">Which AI is worth it for your business, researched and plainly answered.</h1>
          <p class="masthead-sub">Practical AI. No jargon required.</p>
        </div>
      </div>
    </header>

    <section class="home-section" aria-labelledby="lead-title">
      <div class="section-header">
        <h2 id="lead-title" class="section-title">Lead story</h2>
      </div>
      <article class="lead-story">
        {lead_media_link(lead)}
        <div>
          <a class="topic-label" href="{lead_href}">{lead['topicLabel']}</a>
          <h2 class="lead-story-headline"><a href="/blog/{lead['slug']}/">{lead['searchTitle']}</a></h2>
          <p class="lead-dek">{lead['searchDek']}</p>
          <p class="post-meta"><time datetime="{lead['date']}">{lead['dateDisplay']}</time></p>
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

    <section class="home-section home-section--editors-picks" aria-labelledby="picks-title">
      <div class="section-header">
        <h2 id="picks-title" class="section-title">Editor's picks</h2>
        <p class="section-intro">Good places to start.</p>
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
      {readyscore_module("readyscore-title")}
    </section>

{newsletter_home_block()}
  </main>

{footer_html()}
  <script>
  (function () {{
    var el = document.getElementById("pub-dateline");
    if (!el) return;
    var d = new Date();
    var months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
    el.textContent = months[d.getMonth()] + " " + d.getDate() + ", " + d.getFullYear() + " · Practical AI for small business";
  }})();
  </script>
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
