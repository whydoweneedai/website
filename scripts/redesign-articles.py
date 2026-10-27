#!/usr/bin/env python3
"""Rebuild article page chrome without changing article-body HTML."""
import re
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_data import load_site, topic_href
from hero_markup import hero_markup, og_image_url
from site_chrome import (
    FONT,
    HEAD_ICONS,
    footer_html,
    head_scripts,
    header_nav,
    html_newsletter_attr,
    newsletter_article_block,
    readyscore_module,
)

ROOT = Path(__file__).resolve().parents[1]


def read_next_cards(slug: str, site):
    art = site["by_slug"][slug]
    topic = art["topic"]
    ordered = site["ordered"]
    same = [a for a in ordered if a["slug"] != slug and a["topic"] == topic]
    other = [a for a in ordered if a["slug"] != slug and a["topic"] != topic]
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


def article_extras(slug: str, site):
    art = site["by_slug"][slug]
    topic = art["topic"]
    topic_label = art["topicLabel"]
    url = f"https://whydoweneedai.com/blog/{slug}/"
    enc = quote(url, safe="")
    more_topic = ""
    if topic in site["topic_pages"]:
        more_topic = f'  <p class="topic-more"><a href="/topics/{topic}/">More in {topic_label} →</a></p>\n'
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
{read_next_cards(slug, site)}
  </div>
{more_topic}</section>
<div class="article-end-modules">
{readyscore_module(f"rs-{slug}", compact=True)}
{newsletter_article_block(slug)}
</div>"""


def replace_images(html: str, art: dict) -> str:
    img_url = og_image_url(art)
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
        r'"image"\s*:\s*"https://whydoweneedai\.com/[^"]+"',
        f'"image": "{img_url}"',
        html,
    )
    return html


def topic_label_link(topic: str, label: str, topic_pages: set) -> str:
    href = topic_href(topic, topic_pages)
    return f'<a class="topic-label" href="{href}">{label}</a>'


def refresh_article_meta(header: str, art: dict) -> str:
    pub_iso = art["date"]
    pub = art["dateDisplay"]
    mod_iso = art.get("dateModified") or art["date"]
    mod_disp = art["dateModifiedDisplay"]
    read = art.get("readMin", 8)
    updated = ""
    if mod_iso != art["date"]:
        updated = f'<span>•</span><span>Updated <time datetime="{mod_iso}">{mod_disp}</time></span>'
    meta = (
        f'<div class="article-meta"><time datetime="{pub_iso}">{pub}</time>'
        f"{updated}<span>•</span><span>{read}-minute read</span>"
        f'<span>•</span><span>By <a href="/about/">Ross C</a>, editor</span></div>'
    )
    if re.search(r'<div class="article-meta">', header):
        return re.sub(r'<div class="article-meta">.*?</div>', meta, header, count=1, flags=re.DOTALL)
    return header.replace("</header>", f"{meta}</header>", 1)


def replace_eyebrow(header: str, topic: str, label: str, topic_pages: set) -> str:
    link = topic_label_link(topic, label, topic_pages)
    return re.sub(
        r'<span class="eyebrow">[^<]*</span>|<a class="topic-label" href="[^"]*">[^<]*</a>',
        link,
        header,
        count=1,
    )


def clean_article_head(head: str) -> str:
    """Strip chrome duplicates; keep page metadata and schema."""
    head = re.sub(r"<!-- Google tag \(gtag\.js\) -->.*?crossorigin=\"anonymous\"></script>\s*", "", head, flags=re.DOTALL)
    head = re.sub(r"<link rel=\"icon\"[^>]*>\s*", "", head)
    head = re.sub(r"<link rel=\"apple-touch-icon\"[^>]*>\s*", "", head)
    head = re.sub(r"<link rel=\"preconnect\"[^>]*>\s*", "", head)
    head = re.sub(
        r"<link rel=\"preload\" as=\"style\" href=\"https://fonts.googleapis.com[^\"]*\"[^>]*>\s*",
        "",
        head,
    )
    head = re.sub(r"<noscript><link href=\"https://fonts.googleapis.com[^\"]*\"[^>]*></noscript>\s*", "", head)
    head = re.sub(r"<link rel=\"stylesheet\" href=\"(?:\.\./)?styles\.css\">\s*", "", head)
    head = re.sub(r"<link rel=\"stylesheet\" href=\"/blog/styles\.css\">\s*", "", head)
    head = head.strip()
    return f"{head}\n{FONT.strip()}"


def process_file(path: Path, site):
    slug = path.parent.name
    art = site["by_slug"].get(slug)
    if not art:
        print("skip", slug)
        return
    html = path.read_text()
    m_body = re.search(r"(<article class=\"article-body\">.*?</article>)", html, re.DOTALL)
    m_header = re.search(r"(<header class=\"article-header\">.*?</header>)", html, re.DOTALL)
    m_nav = re.search(r"<nav class=\"article-nav\".*?</nav>", html, re.DOTALL)
    if not m_body or not m_header:
        print("parse fail", slug)
        return

    article_body = m_body.group(1)
    article_header = replace_eyebrow(
        m_header.group(1), art["topic"], art["topicLabel"], site["topic_pages"]
    )
    article_header = refresh_article_meta(article_header, art)
    article_nav = m_nav.group(0) if m_nav else ""

    head = re.search(r"<head>(.*?)</head>", html, re.DOTALL).group(1)
    head = clean_article_head(head)
    head = replace_images(head, art)

    breadcrumb_short = art["searchTitle"][:40] + ("…" if len(art["searchTitle"]) > 40 else "")
    thref = topic_href(art["topic"], site["topic_pages"])
    hero = hero_markup(art)
    extras = article_extras(slug, site)
    nl_attr = html_newsletter_attr(site["newsletter_active"])

    out = f"""<!DOCTYPE html><html lang="en"{nl_attr}><head>
{head_scripts(True)}{HEAD_ICONS}{head}</head><body>
<a class="skip-link" href="#main-content">Skip to content</a>
{header_nav()}
<main class="article-main" id="main-content">
<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true"> / </span><a href="/blog/">Archive</a><span aria-hidden="true"> / </span><a href="{thref}">{art['topicLabel']}</a><span aria-hidden="true"> / </span><span>{breadcrumb_short}</span></nav>
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
    site = load_site()
    for art in site["articles"]:
        p = ROOT / "blog" / art["slug"] / "index.html"
        if p.exists():
            process_file(p, site)


if __name__ == "__main__":
    main()
