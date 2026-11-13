
## Adding news to the homepage

1. Add an entry to `data/news.json` with `title`, `source`, `sourceUrl`, `date` (YYYY-MM-DD), `takeaway`, and `image`. Write an original headline and one sentence about what the news means for a small business. Use the original article’s URL and publication date.
2. Create a WhyDoWeNeedAI thumbnail in `images/news/` and use its root-relative path in `image`. Use original art for every news item. The homepage adds the publisher credit automatically.
3. Run `python3 scripts/regenerate-site.py`. The generator includes feed items from the last 21 days and sorts them newest first. Regenerate to refresh the window on the deployed static site.
4. Review the News tab and click through to the original source. Commit the JSON, thumbnail, and regenerated output together.

For blog cards, set the optional `takeaway` and `cardImage` fields in `data/site.json`. Reuse existing editorial art when available. Save new post art to `images/posts/`.
