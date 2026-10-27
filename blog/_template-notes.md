# Article template notes

Styles: [`blog/styles.css`](styles.css). Tokens: [`docs/design-system.md`](../docs/design-system.md). **Editorial mapping:** [`data/site.json`](../data/site.json) — then `python3 scripts/regenerate-site.py`.

## Short answer (factual summary)

```html
<div class="short-answer">
  <p><strong>The short answer:</strong> One or two sentences that state what the test or guide supports, with limits.</p>
</div>
```

## Our take (editor opinion)

```html
<div class="our-take">
  <p class="our-take-label">Our take</p>
  <p>Your opinion here—clearly labeled, separate from reporting and from the short answer.</p>
</div>
```

## Optional components (new posts)

**Pull quote**

```html
<blockquote class="pull-quote">A single standout sentence from the piece.</blockquote>
```

**Callouts**

```html
<div class="callout callout--info"><p>Neutral context or definition.</p></div>
<div class="callout callout--warning"><p>Risk or limitation.</p></div>
<div class="callout callout--tip"><p>Practical next step.</p></div>
```

**Key takeaways**

```html
<div class="key-takeaways">
  <h3>Key takeaways</h3>
  <ul><li>…</li></ul>
</div>
```

**Figure with caption**

```html
<figure class="article-figure">
  <img src="…" width="…" height="…" alt="Illustration: …" loading="lazy" decoding="async">
  <figcaption>Illustration: WhyDoWeNeedAI</figcaption>
</figure>
```

**Table of contents** — add `id` on `h2`; `blog/site.js` builds a TOC when there are three or more `h2[id]`.

## Hero image modes (`data/site.json`)

**Shipping now:** `settings.shipTypographicHeroes: true` — text-and-color covers with the **robot-head** mark; **no** illustrations or AI art. **Do not commit** files under `/images/hero/` until real screenshots are ready. OG/Twitter/JSON-LD use generated `/images/og/<slug>.png` (see `scripts/make-og-images.py`).

When ready for real art: set `shipTypographicHeroes` to `false`, add files locally, set per-article `hero`, run `python3 scripts/regenerate-site.py`.

| `hero` value | Use |
|-------|-----|
| `typographic` | Topic + headline + robot-head mark (current default) |
| `illustration` | Conceptual 16:9 art in `/images/hero/` (not in repo until chosen) |
| `screenshot` | Real product UI with honest `figcaption` |

### Illustration hero (when assets exist)

1. Add files: `/images/hero/<slug>-{480,960,1280}.webp` and `<slug>-1280.jpg` (16:9).
2. In `data/site.json`: `"hero": "illustration"`, `"imageAlt": "Illustration: …"`.
3. Regenerate. Markup includes:

```html
<figure class="article-hero article-hero--illustration">
  <picture>…</picture>
  <figcaption class="article-hero-caption">Illustration: WhyDoWeNeedAI</figcaption>
</figure>
```

### Screenshot hero (tool reviews)

1. Add screenshot files at the same paths (or update generator paths if you use a `-screenshot-` suffix later).
2. Set `"hero": "screenshot"` and alt text that describes the UI literally (not marketing).
3. Optional longer `figcaption` under the credit line for what the screenshot shows.

### Typographic fallback

Set `"hero": "typographic"` — no hero image files required. Run `python3 scripts/make-og-images.py` after adding the article to regenerate `/images/og/<slug>.png`.

## Newsletter (end of article)

Inactive by default. See **Newsletter** section in `docs/design-system.md`. Do not enable until privacy copy and provider are ready.
