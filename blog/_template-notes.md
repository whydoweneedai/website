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

## Hero image modes (`data/site.json` → `hero`)

| Value | Use |
|-------|-----|
| `illustration` | Conceptual 16:9 art in `/images/hero/` |
| `typographic` | Brand title card (comparisons awaiting real screenshots) |
| `screenshot` | Real product UI — use honest caption in `figcaption` |

### Illustration hero

1. Files: `/images/hero/<slug>-{480,960,1280}.webp` and `<slug>-1280.jpg` (16:9).
2. In `data/site.json`: `"hero": "illustration"`, `"imageAlt": "Illustration: …"` (literal, not a real product or person).
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

Set `"hero": "typographic"` — no image files required. OG/Twitter image falls back to `website_logo.png`.

## Newsletter (end of article)

Inactive by default. See **Newsletter** section in `docs/design-system.md`. Do not enable until privacy copy and provider are ready.
