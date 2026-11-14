
## Adding news to the homepage

1. Add an entry to `data/news.json` with `title`, `source`, `sourceUrl`, `date` (YYYY-MM-DD), `takeaway`, and `image`. Write an original headline and one sentence about what the news means for a small business. Use the original article’s URL and publication date.
2. Add a licensed photo thumbnail in `images/news/` and use its root-relative path in `image`. Credit the photographer and license in `data/image-sources.md`, and set `imageCredit` (for example, `Photo: Photographer / Pexels`) for the small on-card credit. Use only licensed photos, never publisher images. The homepage adds “via <Publisher>” automatically.
3. Run `python3 scripts/regenerate-site.py`. The generator includes feed items from the last 21 days and sorts them newest first. Regenerate to refresh the window on the deployed static site.
4. Review the News tab and click through to the original source. Commit the JSON, thumbnail, and regenerated output together.

For blog cards, set the optional `takeaway` and `cardImage` fields in `data/site.json`. Use a licensed photo in `images/posts/cards/<slug>.jpg` and record its credit in `data/image-sources.md`. Keep the separate article hero and OG images unchanged.
