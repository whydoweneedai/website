#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hero_markup import card_media
from site_data import load_site, topic_href
from site_chrome import FONT, HEAD_ANALYTICS, footer_html, header_nav, html_newsletter_attr

ROOT = Path(__file__).resolve().parents[1]


def archive_item(a, topic_pages):
    s = a["slug"]
    thumb = f'<a class="archive-item-thumb archive-item-thumb--typographic" href="/blog/{s}/" tabindex="-1" aria-hidden="true">{card_media(a)}</a>'
    thref = topic_href(a["topic"], topic_pages)
    return f"""        <article class="archive-item" data-topic="{a['topic']}">
          {thumb}
          <div>
            <a class="topic-label" href="{thref}">{a['topicLabel']}</a>
            <h2><a href="/blog/{s}/">{a['searchTitle']}</a></h2>
            <p class="post-meta"><time datetime="{a['date']}">{a['date']}</time> · {a['readMin']}-min read</p>
            <p>{a['searchDek']}</p>
          </div>
        </article>"""


def main():
    site = load_site()
    topic_pages = site["topic_pages"]
    nl_attr = html_newsletter_attr(site["newsletter_active"])
    filter_links = ['<a href="/blog/" aria-current="true">All topics</a>']
    for t in site["raw"]["topics"]:
        if t["slug"] in topic_pages:
            filter_links.append(f'<a href="/topics/{t["slug"]}/">{t["name"]}</a>')
    items = "\n".join(archive_item(a, topic_pages) for a in site["ordered"])

    html = f"""<!DOCTYPE html>
<html lang="en"{nl_attr}>
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
{FONT}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
{header_nav("/blog/")}
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
{items}
    </div>
    <aside class="module-readyscore" style="margin:2rem 0 3rem">
      <h2 class="module-title">AI ReadyScore</h2>
      <p>Free 3-minute self-assessment—see where AI fits your business before another subscription.</p>
      <a class="button button--secondary" href="/ai-readyscore/">Take AI ReadyScore</a>
    </aside>
  </main>
{footer_html()}
</body>
</html>
"""
    (ROOT / "blog/index.html").write_text(html)
    print("blog index ok")


if __name__ == "__main__":
    main()
