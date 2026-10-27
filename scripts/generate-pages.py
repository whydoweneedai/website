#!/usr/bin/env python3
"""Generate topic hub pages (only topics with 3+ articles)."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hero_markup import card_media
from site_data import load_site
from site_chrome import FONT, HEAD_ICONS, footer_html, head_scripts, header_nav, html_newsletter_attr

ROOT = Path(__file__).resolve().parents[1]


def card_html(a):
    slug = a["slug"]
    return f"""<article class="card card--standard">
  <a class="card-link" href="/blog/{slug}/">
    {card_media(a)}
    <div class="card-body">
      <div class="post-meta"><time datetime="{a['date']}">{a['dateDisplay']}</time></div>
      <h2 class="card-title">{a['searchTitle']}</h2>
      <p class="card-dek">{a['searchDek']}</p>
    </div>
  </a>
</article>"""


def topic_page(slug, topic, articles, nl_attr):
    cards = "\n".join(card_html(a) for a in articles)
    url = f"https://whydoweneedai.com/topics/{slug}/"
    title = topic["name"]
    intro = topic["intro"]
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
    nav = header_nav(f"/topics/{slug}/")
    return f"""<!DOCTYPE html>
<html lang="en"{nl_attr}>
<head>
{head_scripts(True)}
{HEAD_ICONS}
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
  <meta property="og:image" content="https://whydoweneedai.com/images/og/topic-{slug}.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://whydoweneedai.com/images/og/topic-{slug}.png">
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
{footer_html()}
</body>
</html>
"""


def main():
    site = load_site()
    nl_attr = html_newsletter_attr(site["newsletter_active"])
    topics_root = ROOT / "topics"
    published = set()

    for t in site["raw"]["topics"]:
        slug = t["slug"]
        if slug not in site["topic_pages"]:
            thin = topics_root / slug
            if thin.exists():
                shutil.rmtree(thin)
                print("removed thin topic", slug)
            continue
        arts = [a for a in site["articles"] if a["topic"] == slug]
        arts.sort(key=lambda x: x["date"], reverse=True)
        out = topics_root / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(topic_page(slug, t, arts, nl_attr))
        published.add(slug)
        print("topic", slug)

    if topics_root.exists():
        for child in topics_root.iterdir():
            if child.is_dir() and child.name not in published:
                shutil.rmtree(child)
                print("removed stale", child.name)


if __name__ == "__main__":
    main()
