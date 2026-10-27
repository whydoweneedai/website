# WhyDoWeNeedAI design system

Anchored on `/website_logo.png`. Derived assets live in `/images/brand/` (see `scripts/build-brand-assets.py`). Stylesheet: [`blog/styles.css`](../blog/styles.css) — regenerate tokens with `python3 scripts/generate-styles.py`.

## Brand assets

| File | Use |
|------|-----|
| `logo-wordmark.png` (+ webp, @2x) | Header only (~28px tall desktop, ~23px mobile) |
| `logo-mascot.png` (+ webp, @2x) | Masthead, About, footer, 404, ReadyScore, newsletter, typographic hero motif |
| `website_logo.png` | Unchanged; default **og:image** / JSON-LD when no article hero image |
| `favicon.png` | Robot-head crop from mascot |

Masters: `logo-wordmark.png` (907×166), `logo-mascot.png` (531×522). After replacing them, run `python3 scripts/build-brand-assets.py` then `python3 scripts/regenerate-site.py`.

## Color (from logo)

| Token | Hex | Use |
|-------|-----|-----|
| `--color-ink` | `#1e3a5c` | Headlines, body on light backgrounds |
| `--color-accent` | `#1f66b8` | Links, buttons, “ai” blue |
| `--color-sky` | `#9fd3e6` | Accents, tags |
| `--color-accent-soft` | `#e8f4fa` | Soft fills |
| `--color-gold` | `#f2a93b` | Sparingly: Editor’s picks, badges, key takeaways |
| `--color-cream` | `#faf3e6` | Page background |
| `--color-paper` | `#ffffff` | Cards, header |

Contrast targets WCAG AA for text and controls.

## Typography

| Role | Font | Weight |
|------|------|--------|
| Headlines, card titles | **Nunito** | 800–900, letter-spacing −0.01 to −0.02em |
| Body, UI | **Inter** | 400–700 |

Sizes unchanged: body 17px mobile / 18px desktop; article H1 ~30–44px; measure ~42rem (65–72ch).

## Imagery

While `settings.shipTypographicHeroes` is `true`, articles and cards use **typographic hero plates** in the logo palette (topic pill, headline, small mascot). Future illustration/screenshot heroes use the markup in `scripts/hero_markup.py` (picture/srcset, figcaption). See `blog/_template-notes.md`.

## Editorial data

[`data/site.json`](../data/site.json) — run `python3 scripts/regenerate-site.py` after edits.

## Newsletter

Inactive (`newsletter.active: false`). See previous newsletter section in git history; wire-up steps apply when enabling collection.
