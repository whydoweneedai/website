# WhyDoWeNeedAI design system

Single shared stylesheet: [`blog/styles.css`](../blog/styles.css). Regenerate from tokens with `python3 scripts/generate-styles.py` when editing the generator.

## Typography

| Role | Font | Size (desktop) | Notes |
|------|------|----------------|-------|
| Body & UI | **Inter** (400–700) | 18px (`1.125rem`) | Line-height 1.6 |
| Body (mobile) | Inter | 17px (`1.0625rem`) | |
| Headlines | **Newsreader** (400–600) | H1 `clamp(30–44px)` | Editorial serif |
| Article H1 | Newsreader | ~40–48px desktop, ~30–32px mobile | |
| H2 | Newsreader | ~22–28px | |
| H3 | Inter semibold | ~20px | In-article subheads |
| Dek / lead | Inter | ~19–20px | Muted ink |
| Kicker / topic label | Inter | 12px uppercase | Letter-spacing 0.06em |
| Meta / caption | Inter | 13–14px | |

Reading measure: `--measure` (42rem, ~65–72 characters).

Fonts load via Google Fonts with `preconnect`, `preload`, and `display=swap` (Inter + Newsreader only).

## Color

| Token | Value | Use |
|-------|-------|-----|
| `--color-ink` | `#0f172a` | Text |
| `--color-paper` | `#faf9f7` | Page background |
| `--color-cream` | `#fff8eb` | Highlights, our-take |
| `--color-sand` | `#f3ebe0` | Warm neutrals |
| `--color-accent` | `#2563eb` | Links, buttons, focus |
| `--color-coral` | `#e07a5f` | Sparingly (labels, accents) |

No gradients or glow on chrome. Restrained borders and shadows (`--shadow-sm` / `--shadow-md`).

## Spacing & radius

Scale: `--space-1` (4px) through `--space-9` (64px). Radius: `--radius-sm` 6px, `--radius-md` 10px, `--radius-lg` 14px, `--radius-xl` 20px.

## Imagery

- **Live site:** typographic `.hero-plate` (topic, headline, brand gradient) on all cards and article heroes while `data/site.json` → `settings.shipTypographicHeroes` is `true`. Social/meta images use `website_logo.png`.
- **Future assets:** 16:9 hero (`--ratio-hero`), 3:2 cards (`--ratio-card`), files at `/images/hero/<slug>-{480,960,1280}.webp` and `<slug>-1280.jpg` (add locally; not committed until approved). Generators in `scripts/hero_markup.py` keep `<picture>` / srcset markup for `illustration` and `screenshot` modes.

## Components

- **Header**: sticky, logo + topic nav + Search + About + AI ReadyScore; mobile menu via `blog/site.js`
- **Footer**: two-column editorial footer (topics + publication)
- **Buttons**: `.button`, `.button--secondary`
- **Cards**: `.card`, `.card--standard`, `.card--compact`, `.card--lead`
- **Topic label**: `.topic-label` (linked on articles)
- **Article**: `.article-header`, `.article-hero`, `.article-body`, `.short-answer`, `.our-take`
- **Newsletter**: `.newsletter-block`, `.newsletter-form`, `.newsletter-compact`
- **Discovery**: `.read-next`, topic hubs, `/search/`

Optional article components (documented in `blog/_template-notes.md`): `.pull-quote`, `.callout--info|warning|tip`, `.key-takeaways`, `figure.article-figure`.

## JavaScript

- `blog/site.js` — nav toggle, share copy, optional TOC from `h2[id]` (&lt;10KB)
- Search page — inline filter on `search/search-index.json` (noindex; not in sitemap)
- Regenerate index: `node scripts/build-search-index.js`

## Editorial data (`data/site.json`)

Single source for provisional topics, per-article `topic`, homepage `leadSlug`, `latestSlugs`, `editorsPickSlugs`, and per-article `hero` mode (`illustration`, `typographic`, or `screenshot`).

After editing, run:

```bash
python3 scripts/regenerate-site.py
```

Topic hub pages are generated only when a topic has **3 or more** articles; thinner topics stay as labels linking to `/blog/`.

## Newsletter (inactive by default)

Signup UI is visible but does not collect email until you turn it on.

1. In `data/site.json`, set `"newsletter": { "active": true }`.
2. Run `python3 scripts/regenerate-site.py`.
3. Update `scripts/site_chrome.py` newsletter blocks to match your provider. For **Netlify Forms**, use:
   - `method="POST"` `action="/subscribe/thanks/"` `data-netlify="true"` `netlify-honeypot="bot-field"`
   - hidden `form-name`, enable inputs/button, remove `disabled`
   - Add the privacy-policy sentence for newsletter collection when you go live.
4. Set `data-newsletter="on"` on `<html>` (regenerator does this when `active` is true). CSS hides the form when `data-newsletter="off"` and shows **Newsletter launching soon.**

When `shipTypographicHeroes` is `false` and image files are present: use `Illustration:` alt prefix and figcaption **Illustration: WhyDoWeNeedAI** for art; `hero: "screenshot"` with an honest caption for product UI.
