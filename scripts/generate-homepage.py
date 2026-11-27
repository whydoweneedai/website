#!/usr/bin/env python3
"""Build the publication homepage from the article catalog and news desk."""
from html import escape

from hero_markup import LOGO_OG, og_image_url
from editorial_media import MEDIA
from site_chrome import FONT, HEAD_ICONS, X_URL, XSVG, footer_html, header_nav, head_scripts
from site_data import ROOT, load_site, format_display_date


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


def tags(article):
    primary = article["topic"] or "everyday"
    return [primary, "tests"] if is_test(article) else [primary]


def guide_card(article, index):
    topic = article["topicLabel"] if article["topic"] else "Everyday ChatGPT"
    state = " hidden" if index >= 8 else ""
    return f'''<a class="guide" data-tags="{escape(" ".join(tags(article)))}" href="{article_url(article)}"{state}>
  <div class="ph">{image_markup(card_image(article))}</div>
  <div class="body"><h3>{escape(article["searchTitle"])}</h3><p>{escape(takeaway(article))}</p>
  <div class="meta"><span class="t{ " ours" if is_test(article) else ""}">{escape("Our test" if is_test(article) else topic)}</span> · {article["readMin"]} min read</div></div>
</a>'''


def main():
    site = load_site()
    posts = site["ordered"]
    config = site["raw"]["homepage"]
    # A scheduled post may already be named here; it appears on its publish day.
    picks = [site["by_slug"][slug] for slug in config["featuredSlugs"] if slug in site["by_slug"]]
    lead = site["by_slug"].get(config["leadSlug"]) or posts[0]
    picks = [article for article in picks if article["slug"] != lead["slug"]]
    featured = featured_card(lead, lead=True)
    featured += "".join(featured_card(article) for article in picks)

    topics = {topic["slug"]: topic["name"] for topic in site["raw"]["topics"]}
    topics.update(tests="Our tests", everyday="Everyday ChatGPT")
    chips = f'<button class="on" aria-pressed="true" data-f="all">All <small>{len(posts)}</small></button>'
    for slug, label in topics.items():
        count = sum(slug in tags(article) for article in posts)
        if count:
            chips += f'<button aria-pressed="false" data-f="{escape(slug)}">{escape(label)} <small>{count}</small></button>'
    guides = "".join(guide_card(article, index) for index, article in enumerate(posts))
    n_tests = sum(is_test(article) for article in posts)
    tests_proof = f"<b>{n_tests}</b> published tests · " if n_tests else ""
    og_image = og_image_url(slug="home")
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
{head_scripts(True)}
{HEAD_ICONS}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="google-adsense-account" content="ca-pub-3631010450044967">
  <title>Why Do We Need AI? | Plain-English AI for work and everyday life</title>
  <meta name="description" content="What AI is actually good for at work and at home. Plain-English guides and tested walkthroughs that show what worked, what didn’t, and how to try it yourself.">
  <meta name="author" content="whydoweneedai.com">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#0f1d30">
  <link rel="canonical" href="https://whydoweneedai.com/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Why Do We Need AI">
  <meta property="og:title" content="Why Do We Need AI? | Plain-English AI for work and everyday life">
  <meta property="og:description" content="What AI is actually good for at work and at home, tested and plainly explained.">
  <meta property="og:url" content="https://whydoweneedai.com/">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:site" content="@whydoweneedai">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Why Do We Need AI?">
  <meta name="twitter:description" content="What AI is actually good for at work and at home, tested and plainly explained.">
  <meta name="twitter:image" content="{og_image}">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Why Do We Need AI?",
    "url": "https://whydoweneedai.com/",
    "description": "A plain-English AI publication for working people, with tested walkthroughs and practical guides.",
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
<section class="hero"><h1>Honest, <em>tested</em> AI for<br> work and everyday life.</h1>
<p>We try AI on real tasks, from a household budget to a busy workweek, and publish what worked, what didn’t, and how to do it yourself.</p>
<div class="cta"><a class="btn btn-white" href="/blog/">Read the blog →</a><a class="btn btn-ghost" href="{X_URL}">{XSVG} Follow @whydoweneedai</a></div>
<p class="proof">{tests_proof}<b>{len(posts)}</b> guides · corrections shown in the open</p></section>
</div></div>
<div class="sheet"><div class="wrap">
<section class="sec"><div class="head"><h2>Latest posts</h2><p>Plain-English guides to getting real use out of AI.</p></div>
<div class="feat">{featured}</div><div class="more"><a class="btn btn-outline" href="/blog/">View all posts →</a></div></section>

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
