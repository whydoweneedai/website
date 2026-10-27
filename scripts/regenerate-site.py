#!/usr/bin/env python3
"""
Regenerate generated pages from data/site.json.

Edit data/site.json (topics, article topics, homepage lead & editor's picks),
then run:  python3 scripts/regenerate-site.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(name):
    path = SCRIPTS / name
    print("==>", name)
    subprocess.check_call([sys.executable, str(path)])


def main():
    run("build-brand-assets.py")
    run("make-og-images.py")
    run("generate-styles.py")
    run("generate-homepage.py")
    run("generate-blog-index.py")
    run("generate-pages.py")
    run("generate-404.py")
    run("generate-subscribe-thanks.py")
    run("redesign-articles.py")
    subprocess.check_call(["node", str(SCRIPTS / "build-search-index.js")])
    run("generate-search.py")
    run("apply-chrome.py")
    run("patch-static-og.py")
    print("Done. Review data/site.json and commit outputs.")


if __name__ == "__main__":
    main()
