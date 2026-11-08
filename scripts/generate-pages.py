#!/usr/bin/env python3
"""Generate reader-first category hubs and legacy redirects."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hero_markup import card_media
from site_data import load_site
from site_chrome import FONT, HEAD_ICONS, footer_html, head_scripts, header_nav, html_newsletter_attr

ROOT = Path(__file__).resolve().parents[1]


# Reading paths supplement the article cards without imposing a word-count target.
TOPIC_GUIDANCE = {
    "getting-started": """<h2>Start with a task, not a tool</h2>
      <p>The best first step is to choose a small, repeatable piece of work and describe what a correct result looks like. If the steps and decisions are predictable, a checklist or ordinary automation may be enough. AI becomes worth testing when the task involves varied language or inputs that simple rules cannot handle well.</p>
      <ul>
        <li>Not sure where to begin? Use <a href="/blog/what-to-automate-first/">the first-task guide</a> to find a manageable starting point.</li>
        <li>Before choosing software, compare <a href="/blog/ai-vs-automation/">AI with rules-based automation</a>.</li>
        <li>Check the process, data and review arrangements with <a href="/blog/ai-readiness-checklist/">the readiness checklist</a>, then see <a href="/blog/ai-readiness-checklist-test/">how it behaved on 12 made-up workflows</a>.</li>
      </ul>
      <p>A readiness score is a prompt for investigation, not permission to automate. Once the task is clear, move to <a href="/topics/tools-comparisons/">choosing a tool</a> and define a small test before committing.</p>""",
    "using-ai-at-work": """<h2>Choose the workflow you need to improve</h2>
      <p>AI is most useful at work when its role is specific and someone can check the result. Start with one transfer, draft or decision-support step. Keep rules for predictable actions, give the tool only the access it needs, and decide what must stop for human review.</p>
      <ul>
        <li>For repetitive admin, read the <a href="/blog/can-ai-enter-invoices-spreadsheet-test/">invoice-entry experiment</a> and the <a href="/blog/ai-vs-rules-appointment-payment-reminders/">AI-versus-rules reminder test</a>. Their synthetic inputs reveal failure cases, not guaranteed business results.</li>
        <li>For customer inquiries, begin with the <a href="/blog/lead-follow-up-automation/">follow-up blueprint</a> and compare it with <a href="/blog/ai-lead-follow-up-test/">the 30-inquiry experiment</a>.</li>
        <li>Before connecting business systems, check <a href="/blog/data-ai-tools/">what data to share</a> and <a href="/blog/ai-agents-business-app-permissions/">which permissions an agent needs</a>.</li>
      </ul>
      <p>Customer discovery is a different problem: <a href="/blog/how-customers-find-small-business-chatgpt/">the ChatGPT discovery guide</a> explains how to make your business information clearer and easier to find. For any workflow change, use <a href="/topics/costs-results/">Costs &amp; Results</a> to decide whether the effort pays off.</p>""",
    "tools-comparisons": """<h2>Compare tools on your own task</h2>
      <p>There is no single best AI tool for every small business. Shortlist tools by the work you need done, the data you can safely share and the systems you already use. Then compare them on the same small set of realistic tasks, including awkward cases, rather than choosing from a polished demo.</p>
      <ul>
        <li>Use <a href="/blog/choose-first-ai-tool/">the first-tool scorecard and cost test</a> to define requirements, compare options and account for review time.</li>
        <li>Read <a href="/blog/chatgpt-vs-claude-vs-gemini-vs-copilot/">the ChatGPT, Claude, Gemini and Copilot comparison</a> for a starting shortlist. It is a researched guide, not a head-to-head benchmark.</li>
      </ul>
      <p>Features, limits and prices change. Check the vendor's current terms before buying, especially if you plan to upload customer or business data. If you cannot yet describe a successful result, return to <a href="/topics/getting-started/">Getting Started</a>. After a trial, use <a href="/blog/evaluate-ai-pilot/">the keep, fix or stop framework</a> before expanding it.</p>""",
    "costs-results": """<h2>Count the work that remains</h2>
      <p>An automation pays off only if its benefits exceed the time and money needed to set it up, run it and correct it. Compare a pilot with your current process, including human review, exceptions and maintenance. Time saved is useful, but it is not automatically cash saved.</p>
      <ul>
        <li>Before a trial, use <a href="/blog/ai-automation-roi/">the AI automation ROI guide</a> to build a baseline, include recurring costs and make your assumptions visible.</li>
        <li>After a trial, use <a href="/blog/evaluate-ai-pilot/">the pilot evaluation framework</a> to choose whether to keep it, fix a specific problem or stop.</li>
      </ul>
      <p>Agree on acceptable errors and review responsibilities before you start. A fast result that needs frequent correction may be worse than a slower, reliable process. If you need ideas for a bounded test, explore <a href="/topics/using-ai-at-work/">the workflow guides and experiments</a>; if the software itself is the obstacle, revisit <a href="/topics/tools-comparisons/">tool selection</a>.</p>""",
}


def card_html(a):
    slug = a["slug"]
    return f"""<article class="card card--standard">
  <a class="card-link" href="/blog/{slug}/">
    {card_media(a)}
    <div class="card-body">
      <p class="format-label">{a['formatLabel']}</p>
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
    <section class="article-body home-section" aria-label="Reading guide">
{TOPIC_GUIDANCE[slug]}
    </section>
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

    for slug, destination in site["raw"].get("legacyTopicRedirects", {}).items():
        out = topics_root / slug / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0;url={destination}"><link rel="canonical" href="https://whydoweneedai.com{destination}"><meta name="robots" content="noindex,follow"><title>Section moved | Why Do We Need AI?</title></head><body><p>This section has moved. <a href="{destination}">Continue to the articles</a>.</p></body></html>''')
        published.add(slug)

    if topics_root.exists():
        for child in topics_root.iterdir():
            if child.is_dir() and child.name not in published:
                shutil.rmtree(child)
                print("removed stale", child.name)


if __name__ == "__main__":
    main()
