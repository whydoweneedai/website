"""Original editorial vector art. Illustrations, never evidence screenshots."""
from html import escape
MEDIA = {
    "can-ai-enter-invoices-spreadsheet-test": ("invoice", "Illustration of an invoice and spreadsheet with a $12.20 difference marked for review."),
    "ai-vs-rules-appointment-payment-reminders": ("reminders", "Illustration of scheduled appointments and a reminder message."),
    "chatgpt-vs-claude-vs-gemini-vs-copilot": ("choose", "Illustration of choosing a tool to fit a task."),
    "ai-agents-business-app-permissions": ("permissions", "Illustration of permissions with reading and drafting enabled, and sending disabled."),
}
def editorial_image(art, eager=False):
    media = MEDIA.get(art["slug"])
    if not media:
        return ""
    name, alt = media
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img class="editorial-image" src="/images/editorial/{name}.svg" width="1200" height="720" alt="{escape(alt, quote=True)}" {loading} decoding="async">'

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_CREDIT_ROW = re.compile(r"^\| `([^`]+)\.jpg` \| ([^|]+) \| \[([^\]]+)\]\(([^)]+)\)", re.M)


def photo_credits():
    """Pexels credits keyed by file stem, read from data/image-sources.md."""
    text = (ROOT / "data/image-sources.md").read_text()
    return {m[1]: {"photographer": m[2].strip(), "title": m[3].strip(), "url": m[4].strip()} for m in _CREDIT_ROW.finditer(text)}


def article_photo(slug):
    """Licensed Pexels hero photo for an article, or None."""
    path = ROOT / "images/posts/cards" / f"{slug}.jpg"
    return f"/images/posts/cards/{slug}.jpg" if path.exists() else None


def article_cover(art):
    src = article_photo(art["slug"])
    if not src:
        return ""
    credit = photo_credits().get(art["slug"], {})
    who = credit.get("photographer", "")
    who = "" if not who or who.lower().startswith("not listed") else f"{escape(who)} / "
    link = credit.get("url", "https://www.pexels.com/")
    alt = escape(credit.get("title", ""), quote=True)
    return (
        f'<figure class="editorial-article-cover"><img class="editorial-image editorial-photo" src="{src}" width="1200" height="675" alt="{alt}" loading="eager" fetchpriority="high" decoding="async">'
        f'<figcaption>Photo: {who}<a href="{link}" rel="noopener" target="_blank">Pexels</a></figcaption></figure>'
    )
