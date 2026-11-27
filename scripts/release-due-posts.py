#!/usr/bin/env python3
"""
Publish scheduled posts whose date has arrived.

A scheduled post is an entry in data/site.json `articles` with a future `date`,
and its page kept at docs/scheduled-posts/<slug>/index.html (never served).
On or after that date (America/New_York), this script moves the page to
blog/<slug>/ and regenerates the site, so the post shows up on the blog index,
homepage, topic pages, sitemap, RSS feed and search.

  python3 scripts/release-due-posts.py           # release what is due, then regenerate
  python3 scripts/release-due-posts.py --check   # only report; change nothing

With nothing due it changes nothing, so the daily workflow makes no commit and
Netlify does not deploy. Set SITE_TODAY=YYYY-MM-DD to preview another day.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_data import ROOT, SCHEDULED_DIR, SITE_PATH, is_published, site_today  # noqa: E402


def due_posts(today):
    articles = json.loads(SITE_PATH.read_text())["articles"]
    due = []
    for article in articles:
        slug = article["slug"]
        waiting = SCHEDULED_DIR / slug / "index.html"
        live = ROOT / "blog" / slug / "index.html"
        if not is_published(article, today) or not waiting.exists():
            continue
        if live.exists():
            raise SystemExit(f"{slug}: page exists in both blog/ and docs/scheduled-posts/. Keep one.")
        due.append(article)
    return due


def set_output(name, value):
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a") as fh:
            fh.write(f"{name}={value}\n")


def main():
    check_only = "--check" in sys.argv[1:]
    today = site_today()
    due = due_posts(today)
    slugs = [a["slug"] for a in due]
    set_output("due", "true" if due else "false")
    set_output("slugs", " ".join(slugs))
    if not due:
        print(f"{today}: nothing due.")
        return
    print(f"{today}: due -> " + ", ".join(slugs))
    if check_only:
        return
    for slug in slugs:
        shutil.move(str(SCHEDULED_DIR / slug), str(ROOT / "blog" / slug))
        print("released", slug)
    if SCHEDULED_DIR.exists() and not any(SCHEDULED_DIR.iterdir()):
        SCHEDULED_DIR.rmdir()
    subprocess.check_call([sys.executable, str(ROOT / "scripts/regenerate-site.py")])


if __name__ == "__main__":
    main()
