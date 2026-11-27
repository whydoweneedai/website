#!/usr/bin/env python3
"""
Check scheduled posts before you commit, and print the release calendar.

Fails when:
- a future-dated post's page is in blog/ (it would be live at once), or missing
  from docs/scheduled-posts/<slug>/index.html (nothing to release);
- a live post has no page in either place;
- a served page links to a post that is still scheduled (a broken link until then).

  python3 scripts/check-schedule.py
  SITE_TODAY=2026-12-10 python3 scripts/check-schedule.py   # as of another day
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_data import ROOT, SCHEDULED_DIR, SITE_PATH, is_published, site_today  # noqa: E402

UNSERVED = ("docs/", ".git/", "scripts/", "node_modules/")


def main():
    today = site_today()
    articles = json.loads(SITE_PATH.read_text())["articles"]
    errors, waiting_release, scheduled = [], [], []
    for a in articles:
        slug, live_page = a["slug"], ROOT / "blog" / a["slug"] / "index.html"
        waiting = SCHEDULED_DIR / slug / "index.html"
        if is_published(a, today):
            if not live_page.exists():
                if waiting.exists():
                    waiting_release.append(a)
                else:
                    errors.append(f"{slug}: live since {a['date']} but has no page in blog/ or docs/scheduled-posts/.")
            continue
        scheduled.append(a)
        if live_page.exists() or (ROOT / "blog" / slug).exists():
            errors.append(f"{slug}: dated {a['date']} but its folder is in blog/, so it would go live at once. "
                          f"Move it to docs/scheduled-posts/{slug}/.")
        if not waiting.exists():
            errors.append(f"{slug}: dated {a['date']} but docs/scheduled-posts/{slug}/index.html is missing.")

    hidden = {a["slug"] for a in scheduled + waiting_release}
    if hidden:
        pattern = re.compile(r'href="(?:https://whydoweneedai\.com)?/blog/(' + "|".join(map(re.escape, hidden)) + r')/?["#]')
        for page in ROOT.rglob("*.html"):
            rel = page.relative_to(ROOT).as_posix()
            if rel.startswith(UNSERVED):
                continue
            for slug in sorted(set(pattern.findall(page.read_text(errors="ignore")))):
                errors.append(f"{rel}: links to /blog/{slug}/, which is not live yet.")

    print(f"Schedule as of {today} (America/New_York):")
    for a in sorted(waiting_release + scheduled, key=lambda x: x["date"]):
        note = "due, goes out on the next daily run" if a in waiting_release else "scheduled"
        print(f"  {a['date']}  {a['slug']}  ({note})")
    if not waiting_release and not scheduled:
        print("  nothing scheduled")
    if errors:
        print("\nProblems:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
