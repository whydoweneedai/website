
## Adding news to the homepage

1. Add an entry to `data/news.json` with `title`, `source`, `sourceUrl`, `date` (YYYY-MM-DD), `takeaway`, and `image`. Write an original headline and one sentence about what the news means for a small business. Use the original article’s URL and publication date.
2. Add a licensed photo thumbnail in `images/news/` and use its root-relative path in `image`. Credit the photographer and license in `data/image-sources.md`, and set `imageCredit` (for example, `Photo: Photographer / Pexels`) for the small on-card credit. Use only licensed photos, never publisher images. The homepage adds “via <Publisher>” automatically.
3. Run `python3 scripts/regenerate-site.py`. The generator includes feed items from the last 21 days and sorts them newest first. Regenerate to refresh the window on the deployed static site.
4. Review the News tab and click through to the original source. Commit the JSON, thumbnail, and regenerated output together.

For blog cards, set the optional `takeaway` and `cardImage` fields in `data/site.json`. Use a licensed photo in `images/posts/cards/<slug>.jpg` and record its credit in `data/image-sources.md`. Keep the separate article hero and OG images unchanged.

## Retiring a post

1. Move its entry from `articles` to `retiredArticles` in `data/site.json`, with `redirectTo` set to the closest live page.
2. `git mv blog/<slug> docs/retired-posts/<slug>` so the files are kept but never served (`/docs/*` returns 404).
3. Add 301 redirects in `netlify.toml` for `/blog/<slug>`, `/blog/<slug>/`, `/blog/<slug>/index.html` and `/blog/<slug>/*`.
4. Remove links to it from live pages, then run `python3 scripts/regenerate-site.py` and the `scripts/check-*.py` checks.

To bring one back, reverse those steps.

## Scheduling a post

Posts can be committed ahead of time and go live on their own date, with no deploy until then.

1. Add the post to `articles` in `data/site.json` with `date` set to the day it should go live (YYYY-MM-DD, New York time). You can also name it in `homepage.featuredSlugs` or `homepage.leadSlug` now; it appears there on its day.
2. Put its page at `docs/scheduled-posts/<slug>/index.html`, not in `blog/`. `/docs/*` is never served, so the page stays private on the site until its date. The repository is public, so the file can be read on GitHub before then.
3. Run `python3 scripts/regenerate-site.py` and `python3 scripts/check-schedule.py`, which prints the release calendar and fails if a scheduled post would leak or a live page links to one early. Commit and merge as usual.

Every generated page, the sitemap, the RSS feed and search leave out posts dated after today. Each morning at about 6 AM New York time, the "Release scheduled posts" GitHub Action runs `scripts/release-due-posts.py`. On a day with nothing due it changes nothing, so there is no commit and no Netlify deploy. When a post is due it moves the page into `blog/`, regenerates the site and pushes one commit to `main`, which Netlify deploys. Posts due the same day ship in that one deploy.

To preview a day, run `SITE_TODAY=2026-12-02 python3 scripts/check-schedule.py`. To release early, change the post's `date` to today and run the workflow from the Actions tab ("Run workflow"). GitHub pauses scheduled workflows after 60 days with no commits to the repository; if that happens, turn it back on from the Actions tab.

