# WhyDoWeNeedAI design system

Anchored on `/website_logo.png`. Brand crops live in `/images/brand/` (from `uploads/brand-assets.tar.gz`). Stylesheet: [`blog/styles.css`](../blog/styles.css) — regenerate with `python3 scripts/generate-styles.py`.

## Brand assets

| File | Use |
|------|-----|
| `lockup-128.png` / `.webp` (684×128) | **Header** on every page except `assessment.html` (~34px / ~28px tall) |
| `website_logo.png` | **Homepage masthead** + **footer** (unchanged master file) |
| `robot-head.png` | **Robot mark** on text-and-color story cards and article covers |
| `logo-mascot.png` | Newsletter, ReadyScore modules, 404 |
| `robot-head-32.png` | `favicon.png` |
| `robot-head-180.png` | `apple-touch-icon.png` |
| `robot-head-512.png` | `site.webmanifest` |

Do not recolor, filter, or redraw logo art.

After replacing masters: `python3 scripts/build-brand-assets.py` then `python3 scripts/regenerate-site.py`.

## Color (from logo)

| Token | Hex | Use |
|-------|-----|-----|
| `--color-ink` | `#1e3a5c` | Headlines, body |
| `--color-accent` | `#1859a9` | Links, buttons, “ai” blue (sampled from logo) |
| `--color-sky` / `--color-accent-soft` | light blues | Tags, fills, section contrast |
| `--color-gold` | `#f2a93b` | Sparingly: Editor’s picks, accents |
| `--color-paper` | `#ffffff` | Page background (no cream/beige) |

Section bands use `--color-section` (`#eef6fb`), not warm neutrals.

## Typography

| Role | Font | Weight |
|------|------|--------|
| Headlines | **Nunito** | 800–900, letter-spacing −0.01 to −0.02em |
| Body, UI | **Inter** | 400–700 |

Article column: `max-width: 36em` (~65–75 characters). Body 17px mobile / 18px desktop.

## Covers and heroes

**No article images** ship in this site: cards and article heroes are **text + color only**, with the **robot-head** mark for recognition. `scripts/hero_markup.py` still supports future screenshot/illustration heroes (`<picture>`, srcset, figcaption).

## Social share images (OG)

Generated 1200×630 PNGs in `/images/og/`:

```bash
python3 scripts/make-og-images.py
```

Uses pinned `fonts/Nunito-ExtraBold.ttf` and `fonts/Nunito-Bold.ttf`. Outputs:

- `home.png` — homepage
- `topic-<slug>.png` — topic hubs
- `<article-slug>.png` — each article

`regenerate-site.py` runs this automatically. For a **new article**, add it to `data/site.json`, run `regenerate-site.py`, and commit the new `images/og/<slug>.png`.

Articles set `og:image`, `twitter:image` (summary_large_image), and JSON-LD `image` to the per-slug PNG.

## Editorial data

[`data/site.json`](../data/site.json) — run `python3 scripts/regenerate-site.py` after edits.

## Newsletter

Inactive (`newsletter.active: false`). Wire-up steps apply when enabling collection.
