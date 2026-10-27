#!/usr/bin/env python3
"""Hero and card media markup (typographic default; image modes for future assets)."""
from site_data import HERO_CAPTION, load_site

LOGO_OG = "https://whydoweneedai.com/website_logo.png"


def _ship_typographic_only() -> bool:
    return load_site()["raw"].get("settings", {}).get("shipTypographicHeroes", True)


MASCOT_MINI = """<img class="hero-plate-mascot" src="/images/brand/logo-mascot.webp" srcset="/images/brand/logo-mascot.webp 1x, /images/brand/logo-mascot@2x.webp 2x" width="531" height="522" alt="" aria-hidden="true" loading="lazy" decoding="async">"""


def typographic_plate(art: dict, variant: str = "article") -> str:
    """Premium typographic field: topic, headline, brand mascot motif."""
    topic = art["topicLabel"]
    title = art["searchTitle"]
    if variant == "card":
        return f"""<div class="hero-plate hero-plate--card" aria-hidden="true">
  {MASCOT_MINI}
  <span class="hero-plate-topic">{topic}</span>
  <span class="hero-plate-title">{title}</span>
</div>"""
    if variant == "lead":
        return f"""<div class="hero-plate hero-plate--lead" aria-hidden="true">
  {MASCOT_MINI}
  <span class="hero-plate-topic">{topic}</span>
  <span class="hero-plate-title">{title}</span>
  <span class="hero-plate-brand">WhyDoWeNeedAI</span>
</div>"""
    alt = art.get("imageAlt") or title
    return f"""<figure class="article-hero article-hero--typographic">
  <div class="hero-plate hero-plate--article" role="img" aria-label="{alt}">
    {MASCOT_MINI}
    <span class="hero-plate-topic">{topic}</span>
    <span class="hero-plate-title">{title}</span>
    <span class="hero-plate-brand">WhyDoWeNeedAI</span>
  </div>
</figure>"""


def hero_markup(art: dict, eager: bool = True) -> str:
    if _ship_typographic_only():
        return typographic_plate(art, "article")

    slug = art["slug"]
    alt = art.get("imageAlt", art["searchTitle"])
    mode = art.get("hero", "typographic")
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    caption = f'<figcaption class="article-hero-caption">{HERO_CAPTION}</figcaption>'

    if mode == "typographic":
        return typographic_plate(art, "article")

    if mode == "screenshot":
        base = f"/images/hero/{slug}"
        return f"""<figure class="article-hero article-hero--screenshot">
  <picture>
    <source type="image/webp" srcset="{base}-480.webp 480w, {base}-960.webp 960w, {base}-1280.webp 1280w" sizes="(min-width: 960px) 860px, 100vw">
    <img src="{base}-1280.jpg" srcset="{base}-480.webp 480w, {base}-960.webp 960w, {base}-1280.jpg 1280w" sizes="(min-width: 960px) 860px, 100vw" width="1280" height="720" alt="{alt}" {loading}>
  </picture>
  {caption}
</figure>"""

    base = f"/images/hero/{slug}"
    return f"""<figure class="article-hero article-hero--illustration">
  <picture>
    <source type="image/webp" srcset="{base}-480.webp 480w, {base}-960.webp 960w, {base}-1280.webp 1280w" sizes="(min-width: 960px) 860px, 100vw">
    <img src="{base}-1280.jpg" srcset="{base}-480.webp 480w, {base}-960.webp 960w, {base}-1280.jpg 1280w" sizes="(min-width: 960px) 860px, 100vw" width="1280" height="720" alt="{alt}" {loading}>
  </picture>
  {caption}
</figure>"""


def card_media(art: dict, lazy: bool = True) -> str:
    if _ship_typographic_only() or art.get("hero", "typographic") == "typographic":
        return f'<div class="card-media card-media--typographic">{typographic_plate(art, "card")}</div>'
    slug = art["slug"]
    alt = art.get("imageAlt", "")
    loading = 'loading="lazy" decoding="async"' if lazy else 'loading="eager" fetchpriority="high"'
    return f"""<div class="card-media"><picture><source type="image/webp" srcset="/images/hero/{slug}-480.webp 480w, /images/hero/{slug}-960.webp 960w" sizes="320px"><img src="/images/hero/{slug}-960.webp" width="960" height="540" alt="{alt}" {loading}></picture></div>"""


def lead_media_link(art: dict) -> str:
    slug = art["slug"]
    inner = typographic_plate(art, "lead")
    return f'<div class="lead-story-media lead-story-media--typographic"><a href="/blog/{slug}/" class="hero-plate-link">{inner}</a></div>'


def og_image_url(art: dict) -> str:
    if _ship_typographic_only():
        return LOGO_OG
    mode = art.get("hero", "typographic")
    if mode == "typographic":
        return LOGO_OG
    return f"https://whydoweneedai.com/images/hero/{art['slug']}-1280.jpg"
