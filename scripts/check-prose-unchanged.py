#!/usr/bin/env python3
"""Compare visible article/policy prose against main (tags stripped, whitespace normalized)."""
from __future__ import annotations

import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

POLICY_PAGES = [
    "about/index.html",
    "contact/index.html",
    "editorial-policy/index.html",
    "privacy/index.html",
]


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = False
        if tag in ("p", "li", "h1", "h2", "h3", "h4", "td", "th", "blockquote", "figcaption"):
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skip and data:
            self.parts.append(data)

    def text(self) -> str:
        raw = "".join(self.parts)
        raw = re.sub(r"\s+", " ", raw)
        return raw.strip()


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def prose_from_html(html: str, article_only: bool) -> str:
    if article_only:
        m = re.search(r'<article class="article-body">(.*?)</article>', html, re.DOTALL)
        if not m:
            m = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL)
        chunk = m.group(1) if m else html
    else:
        m = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL)
        chunk = m.group(1) if m else html
    parser = TextExtractor()
    parser.feed(chunk)
    return normalize(parser.text())


def git_show_main(path: str) -> str | None:
    r = subprocess.run(
        ["git", "show", f"main:{path}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return None
    return r.stdout


def main() -> int:
    import json

    site = json.loads((ROOT / "data/site.json").read_text())
    paths = [f"blog/{a['slug']}/index.html" for a in site["articles"]] + POLICY_PAGES

    failures: list[str] = []
    skipped: list[str] = []
    checked = 0
    for rel in paths:
        current_path = ROOT / rel
        if not current_path.exists():
            failures.append(f"MISSING {rel}")
            continue
        main_html = git_show_main(rel)
        if main_html is None:
            skipped.append(rel)
            continue
        article_only = rel.startswith("blog/")
        cur_text = prose_from_html(current_path.read_text(encoding="utf-8"), article_only)
        main_text = prose_from_html(main_html, article_only)
        checked += 1
        if cur_text != main_text:
            failures.append(f"DIFF {rel} (len main={len(main_text)} cur={len(cur_text)})")

    print(f"Checked {checked} pages against main.")
    if skipped:
        print(f"Skipped {len(skipped)} pages not on main:")
        for rel in skipped:
            print(f"  SKIP {rel}")
    if failures:
        print("FAILURES:")
        for line in failures:
            print(line)
        return 1
    print("OK: 0 prose differences (visible text, normalized).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
