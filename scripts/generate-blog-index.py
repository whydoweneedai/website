#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_data import load_site, topic_href

ARCHIVE_MARK = """<img class="archive-mark" src="/images/brand/robot-head.png" width="262" height="174" alt="" aria-hidden="true" loading="lazy" decoding="async">"""
from site_chrome import FONT, HEAD_ICONS, footer_html, head_scripts, header_nav, html_newsletter_attr, readyscore_module

ROOT = Path(__file__).resolve().parents[1]


def archive_item(a, topic_pages):
    s = a["slug"]
    thref = topic_href(a["topic"], topic_pages)
    return f"""        <article class="archive-item archive-item--text" data-topic="{a['topic']}">
          <a class="archive-item-mark-link" href="/blog/{s}/" tabindex="-1" aria-hidden="true">{ARCHIVE_MARK}</a>
          <div class="archive-item-body">
            <a class="topic-label" href="{thref}">{a['topicLabel']}</a>
            <h2><a href="/blog/{s}/">{a['searchTitle']}</a></h2>
            <p class="archive-dek">{a['searchDek']}</p>
            <p class="post-meta"><time datetime="{a['date']}">{a['dateDisplay']}</time> · {a['readMin']}-min read</p>
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
{head_scripts(True)}
{HEAD_ICONS}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="google-adsense-account" content="ca-pub-3631010450044967">
  <title>Archive | Why Do We Need AI?</title>
  <meta name="description" content="Full archive of practical AI guides and documented tests for small-business owners.">
  <link rel="canonical" href="https://whydoweneedai.com/blog/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Archive | Why Do We Need AI?">
  <meta property="og:url" content="https://whydoweneedai.com/blog/">
  <meta property="og:image" content="https://whydoweneedai.com/images/og/home.png">
  <meta name="twitter:image" content="https://whydoweneedai.com/images/og/home.png">
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
    {readyscore_module("archive-readyscore", compact=True)}
  </main>
{footer_html()}
</body>
</html>
"""
    (ROOT / "blog/index.html").write_text(html)
    print("blog index ok")


if __name__ == "__main__":
    main()
