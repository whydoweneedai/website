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

def article_cover(art):
    if art["slug"] != "can-ai-enter-invoices-spreadsheet-test":
        return ""
    return f'<figure class="editorial-article-cover">{editorial_image(art, eager=True)}<figcaption>Illustration: WhyDoWeNeedAI. The $12.20 discrepancy comes from our invented test invoice; this is not a screenshot.</figcaption></figure>'
