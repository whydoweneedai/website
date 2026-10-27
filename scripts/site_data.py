#!/usr/bin/env python3
"""Load data/site.json and derived editorial helpers."""
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_PATH = ROOT / "data/site.json"

HERO_CAPTION = "Illustration: WhyDoWeNeedAI"
LOGO_OG = "https://whydoweneedai.com/website_logo.png"

# Short labels for tight cover plates / archive thumbs
TOPIC_PLATE_LABELS = {
    "tested": "Tested",
    "choosing-ai-tools": "Choosing tools",
    "automation-workflows": "Automation",
    "roi-planning": "ROI & planning",
    "risk-data": "Risk & data",
}


def topic_plate_label(topic_slug: str, fallback: str) -> str:
    return TOPIC_PLATE_LABELS.get(topic_slug, fallback)


def format_display_date(iso: str) -> str:
    """e.g. 2026-10-29 -> Oct 29, 2026"""
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d.strftime('%b')} {d.day}, {d.year}"


def load_site():
    data = json.loads(SITE_PATH.read_text())
    topics_by_slug = {t["slug"]: t for t in data["topics"]}
    articles = data["articles"]
    for a in articles:
        t = topics_by_slug[a["topic"]]
        a["topicLabel"] = t["name"]
        a["topicPlateLabel"] = topic_plate_label(a["topic"], t["name"])
        a["dateDisplay"] = format_display_date(a["date"])
        mod = a.get("dateModified") or a["date"]
        a["dateModifiedDisplay"] = format_display_date(mod)
    by_slug = {a["slug"]: a for a in articles}
    ordered = sorted(articles, key=lambda x: x["date"], reverse=True)
    counts = {}
    for a in articles:
        counts[a["topic"]] = counts.get(a["topic"], 0) + 1
    topic_pages = {slug for slug, n in counts.items() if n >= 3}
    return {
        "raw": data,
        "topics_by_slug": topics_by_slug,
        "articles": articles,
        "by_slug": by_slug,
        "ordered": ordered,
        "topic_counts": counts,
        "topic_pages": topic_pages,
        "newsletter_active": bool(data.get("newsletter", {}).get("active")),
    }


def topic_href(slug: str, topic_pages: set) -> str:
    if slug in topic_pages:
        return f"/topics/{slug}/"
    return "/blog/"


def enrich_article(a, topic_pages):
    return {**a, "topicHref": topic_href(a["topic"], topic_pages)}
