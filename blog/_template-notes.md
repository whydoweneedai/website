# Article template notes

Styles live in [`blog/styles.css`](styles.css). Design tokens are documented in [`docs/design-system.md`](../docs/design-system.md).

## Short answer (factual summary)

```html
<div class="short-answer">
  <p><strong>The short answer:</strong> One or two sentences that state what the test or guide supports, with limits.</p>
</div>
```

You may also use `class="verdict short-answer"` on a leading paragraph when the article already uses that pattern.

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
  <img src="…" width="…" height="…" alt="…" loading="lazy" decoding="async">
  <figcaption>Caption text.</figcaption>
</figure>
```

**Table of contents** — add `id` attributes to `h2` elements; `blog/site.js` builds a TOC when there are three or more `h2[id]`.

## Hero image for a new post

1. Export **16:9** images at **480**, **960**, and **1280** px wide (WebP) plus **1280×720 JPG** for Open Graph.
2. Save as `/images/hero/<slug>-480.webp`, `-960.webp`, `-1280.webp`, and `-1280.jpg`.
3. Place this block after `</header>` and before `<article class="article-body">`:

```html
<figure class="article-hero">
  <picture>
    <source type="image/webp" srcset="/images/hero/your-slug-480.webp 480w, /images/hero/your-slug-960.webp 960w, /images/hero/your-slug-1280.webp 1280w" sizes="(min-width: 960px) 860px, 100vw">
    <img src="/images/hero/your-slug-1280.jpg" srcset="/images/hero/your-slug-480.webp 480w, /images/hero/your-slug-960.webp 960w, /images/hero/your-slug-1280.jpg 1280w" sizes="(min-width: 960px) 860px, 100vw" width="1280" height="720" alt="Short literal description." loading="eager" fetchpriority="high">
  </picture>
</figure>
```

4. Set `og:image`, `twitter:image`, and JSON-LD `image` to `https://whydoweneedai.com/images/hero/your-slug-1280.jpg`.

**Fallback** (no image yet): use a typographic placeholder:

```html
<div class="hero-fallback" role="img" aria-label="Article title">Article title</div>
```

## Topic label

```html
<a class="topic-label" href="/topics/choosing-ai-tools/">Choosing AI tools</a>
```

Topic slugs: `tested`, `choosing-ai-tools`, `automation-workflows`, `roi-planning`, `risk-data`.

## Newsletter (end of article)

Use the compact Netlify form pattern from any redesigned article (`newsletter-compact` + `newsletter-form--compact`).
