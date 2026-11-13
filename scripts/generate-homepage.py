#!/usr/bin/env python3
"""Build the publication homepage from the article catalog and news desk."""
from html import escape

from hero_markup import LOGO_OG, og_image_url
from editorial_media import MEDIA
from site_chrome import FONT, HEAD_ICONS, X_URL, XSVG, footer_html, header_nav, head_scripts
from site_data import ROOT, load_site, load_recent_news, recent_feed_date, format_display_date


def article_url(article):
    return f'/blog/{article["slug"]}/'


def takeaway(article):
    return article.get("takeaway") or article["searchDek"]


def card_image(article):
    media = MEDIA.get(article["slug"])
    fallback = f"/images/editorial/{media[0]}.svg" if media else "/images/og/home.png"
    return article.get("cardImage") or fallback


def is_test(article):
    return article["format"] == "Our experiment"


def image_markup(url, eager=False):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    if url.endswith(".svg") or url.startswith("/images/posts/"):
        width, height = 1200, 720
    elif url.startswith("/images/news/"):
        width, height = 960, 540
    else:
        width, height = 1200, 630
    return f'<img src="{escape(url)}" alt="" width="{width}" height="{height}" {loading} decoding="async">' 


def date_markup(iso):
    return f'<time datetime="{iso}">{format_display_date(iso)}</time>'


def featured_card(article, lead=False):
    label = "Our test" if is_test(article) else article["format"]
    image = image_markup(card_image(article), eager=lead)
    dek = f"<p>{escape(takeaway(article))}</p>" if lead else ""
    classes = "card lead" if lead else "card"
    return f'''<a class="{classes}" href="{article_url(article)}">
  <div class="ph"><span class="badge">{escape(label)}</span>{image}</div>
  <div><h3>{escape(article["searchTitle"])}</h3>{dek}
  <span class="meta">{date_markup(article["date"])} · {article["readMin"]} min read</span></div>
</a>'''


def feed_card(item):
    label_class = "lab ours" if item["kind"] == "ours" else "lab"
    return f'''<a class="item" data-kind="{item["kind"]}" href="{escape(item["sourceUrl"])}">
  <div class="ph">{image_markup(item["image"])}</div>
  <div><div class="{label_class}">{escape(item["source"])}</div>
  <h3>{escape(item["title"])}</h3>
  <p><b>Why it matters:</b> {escape(item["takeaway"])}</p>
  <span class="meta">{date_markup(item["date"])}</span></div>
</a>'''


def tags(article):
    primary = article["topic"] or "everyday"
    return [primary, "tests"] if is_test(article) else [primary]


def guide_card(article, index):
    topic = article["topicLabel"] if article["topic"] else "Everyday ChatGPT"
    state = " hidden" if index >= 8 else ""
    return f'''<a class="guide" data-tags="{escape(" ".join(tags(article)))}" href="{article_url(article)}"{state}>
  <div class="ph">{image_markup(card_image(article))}</div>
  <div class="body"><h3>{escape(article["searchTitle"])}</h3><p>{escape(takeaway(article))}</p>
  <div class="meta"><span class="t">{escape(topic)}</span> · {article["readMin"]} min read</div></div>
</a>'''


def main():
    site = load_site()
    posts = site["ordered"]
    config = site["raw"]["homepage"]
    featured = featured_card(site["by_slug"][config["leadSlug"]], lead=True)
    featured += "".join(featured_card(site["by_slug"][slug]) for slug in config["featuredSlugs"])

    feed = [{**item, "source": f'via {item["source"]}', "kind": "news"} for item in load_recent_news()]
    feed.extend({
        "kind": "ours", "date": article["date"], "title": article["searchTitle"],
        "source": "WhyDoWeNeedAI", "sourceUrl": article_url(article),
        "takeaway": takeaway(article), "image": card_image(article),
    } for article in posts if recent_feed_date(article["date"]))
    feed.sort(key=lambda item: item["date"], reverse=True)
    feed_html = "".join(feed_card(item) for item in feed)

    topics = {topic["slug"]: topic["name"] for topic in site["raw"]["topics"]}
    topics.update(tests="Our tests", everyday="Everyday ChatGPT")
    chips = f'<button class="on" aria-pressed="true" data-f="all">All <small>{len(posts)}</small></button>'
    for slug, label in topics.items():
        count = sum(slug in tags(article) for article in posts)
        if count:
            chips += f'<button aria-pressed="false" data-f="{escape(slug)}">{escape(label)} <small>{count}</small></button>'
    guides = "".join(guide_card(article, index) for index, article in enumerate(posts))
    n_tests = sum(is_test(article) for article in posts)
    og_image = og_image_url(slug="home")
    page = f'''<!DOCTYPE html>
<html lang="en">
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
  <meta name="theme-color" content="#0f1d30">
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
  <link rel="stylesheet" href="/publication.css">
</head>
<body class="publication-home">
<a class="skip-link" href="#main-content">Skip to content</a>
{header_nav("/")}
<main id="main-content">
<div class="top"><div class="wrap">
<section class="hero"><h1>Honest, <em>tested</em> AI for<br> small-business owners.</h1>
<p>We try AI on real small-business tasks, publish what worked and what didn’t, and explain the week’s AI news in plain English.</p>
<div class="cta"><a class="btn btn-white" href="/ai-readyscore/">Get your ReadyScore →</a><a class="btn btn-ghost" href="{X_URL}">{XSVG} Follow @whydoweneedai</a></div>
<p class="proof"><b>{n_tests}</b> published tests · <b>{len(posts)}</b> guides · corrections shown in the open</p></section>
</div></div>
<div class="sheet"><div class="wrap">
<section class="sec"><div class="head"><h2>Latest from our tests</h2><p>Real tasks, invented data, and the results, good or bad.</p></div>
<div class="feat">{featured}</div><div class="more"><a class="btn btn-outline" href="/blog/">View all posts →</a></div></section>

<section class="sec" id="latest"><div class="head"><h2>Latest</h2><p>Recent AI news and practical posts for small businesses.</p>
<div class="tabs" data-for="feed"><button class="on" aria-pressed="true" data-f="all">All</button><button aria-pressed="false" data-f="news">News</button><button aria-pressed="false" data-f="ours">Our posts</button></div></div>
<div class="feed">{feed_html}</div><p class="feed-empty" hidden>No recent items in this view.</p>

<aside class="ready"><div class="txt"><div class="eyebrow">AI ReadyScore · Free</div>
<h2>Find out where AI fits<br>your business.</h2><p>Answer 8 quick questions about how you work today. Get a score and one practical first step to test.</p>
<div class="facts"><span><i></i>8 questions</span><span><i></i>About 2 minutes</span><span><i></i>No tool to buy</span></div>
<a class="btn btn-gold" href="/ai-readyscore/">Get your ReadyScore →</a></div>
<div class="art"><img src="/images/brand/logo-mascot.png" alt="" width="531" height="522"></div></aside></section>

<section class="sec" id="guides"><div class="head"><h2>Guides</h2><p>Step-by-step playbooks from our tests and research.</p>
<div class="chips">{chips}</div></div>
<div class="guides">{guides}</div><div class="more"><a class="btn btn-outline" href="/blog/">View all guides →</a></div></section>
</div></div></main>
{footer_html()}
<script src="/publication.js" defer></script>
</body></html>
'''
    (ROOT / "index.html").write_text(page)


if __name__ == "__main__":
    main()
