#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hero_markup import LOGO_OG, og_image_url

from site_data import format_display_date, load_site, publication_dateline, topic_href
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

    def text_card(a, show_topic: bool) -> str:
        topic = (
            f'<span class="topic-label">{a["topicLabel"]}</span>'
            if show_topic
            else ""
        )
        return f"""<article class="card card--text">
          <a class="card-link" href="/blog/{a['slug']}/">
            <div class="card-body">{topic}<h3 class="card-title">{a['searchTitle']}</h3><p class="card-dek">{a['searchDek']}</p></div>
          </a>
        </article>"""

    lead_slug = hp["leadSlug"]
    ordered_slugs = [a["slug"] for a in site["ordered"]]
    rail_slugs = [s for s in ordered_slugs if s != lead_slug][:3]
    rail_set = set(rail_slugs)

    latest_slugs = list(hp["latestSlugs"])
    pick_slugs = list(hp["editorsPickSlugs"])
    home_slugs = {lead_slug} | set(rail_slugs) | set(latest_slugs) | set(pick_slugs)
    if len(home_slugs) != len(site["articles"]):
        raise SystemExit(
            f"homepage must list each article once (got {len(home_slugs)}, expected {len(site['articles'])})"
        )

    def latest_row(a) -> str:
        return f"""<li class="home-latest-item">
          <a class="home-latest-link" href="/blog/{a['slug']}/">
            <span class="topic-label">{a['topicLabel']}</span>
            <h3 class="home-latest-title">{a['searchTitle']}</h3>
            <p class="home-latest-dek">{a['searchDek']}</p>
            <p class="post-meta"><time datetime="{a['date']}">{a['dateDisplay']}</time></p>
          </a>
        </li>"""

    latest_rows = "\n".join(latest_row(by[slug]) for slug in latest_slugs)
    pick_cards = [text_card(by[slug], False) for slug in pick_slugs]

    rail_items = []
    for i, slug in enumerate(rail_slugs, start=1):
        a = by[slug]
        rail_items.append(
            f'<li class="lead-rail-item"><span class="lead-rail-num" aria-hidden="true">{i}</span>'
            f'<a href="/blog/{slug}/"><span class="lead-rail-kicker">{a["topicLabel"]}</span>'
            f'<span class="lead-rail-title">{a["searchTitle"]}</span></a></li>'
        )
    lead_rail = "\n          ".join(rail_items)
    lead_rail_block = f"""<ol class="lead-rail-list">
          {lead_rail}
          </ol>"""

    topic_cards = "\n        ".join(
        topic_card(t, topic_pages) for t in site["raw"]["topics"] if t["slug"] in topic_pages
    )
    og_image = og_image_url(slug="home")
    pinned = hp.get("mastheadDatelineDate")
    if pinned:
        built_dateline = (
            f"{format_display_date(pinned)} · Practical AI for small business"
        )
    else:
        built_dateline = publication_dateline()

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
  <main class="page-main" id="main-content">
    <header class="masthead masthead--front">
      <div class="masthead-inner masthead-inner--front">
        {masthead_logo()}
        <div class="masthead-copy">
          <p class="pub-dateline masthead-dateline" id="pub-dateline">{built_dateline}</p>
          <h1 class="masthead-tagline">Which AI is worth it for your business, researched and plainly answered.</h1>
          <p class="masthead-sub">Practical AI. No jargon required.</p>
        </div>
      </div>
    </header>

    <section class="home-section home-section--lead" aria-labelledby="lead-headline">
      <div class="lead-front">
        <article class="lead-story lead-story--front">
          <a class="topic-label" href="{lead_href}">{lead['topicLabel']}</a>
          <h2 id="lead-headline" class="lead-story-headline"><a href="/blog/{lead['slug']}/">{lead['searchTitle']}</a></h2>
          <p class="lead-dek">{lead['searchDek']}</p>
          <p class="lead-byline post-meta"><span>By <a href="/about/">Ross C</a></span><span aria-hidden="true">·</span><time datetime="{lead['date']}">{lead['dateDisplay']}</time></p>
          <p class="lead-cta"><a class="read-link" href="/blog/{lead['slug']}/">Read the story</a></p>
          <div class="lead-story-rail-mobile" aria-labelledby="lead-rail-mobile-title">
            <h2 id="lead-rail-mobile-title" class="lead-rail-heading">Latest headlines</h2>
            {lead_rail_block}
          </div>
        </article>
        <aside class="lead-story-rail" aria-labelledby="lead-rail-title">
          <h2 id="lead-rail-title" class="lead-rail-heading">Latest headlines</h2>
          {lead_rail_block}
        </aside>
      </div>
    </section>

    <section class="home-section" aria-labelledby="latest-title">
      <div class="section-header">
        <h2 id="latest-title" class="section-title">Latest</h2>
      </div>
      <ol class="home-latest-list">
        {latest_rows}
      </ol>
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
