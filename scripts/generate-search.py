#!/usr/bin/env python3
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_chrome import FONT, HEAD_ICONS, footer_html, head_scripts, header_nav, html_newsletter_attr

ROOT = Path(__file__).resolve().parents[1]

SEARCH_SCRIPT = """
  <script>
  (function () {
    var input = document.getElementById("search-input");
    var results = document.getElementById("search-results");
    var status = document.getElementById("search-status");
    var data = [];

    function getQuery() {
      var params = new URLSearchParams(window.location.search);
      return params.get("q") || "";
    }

    function render(q) {
      var needle = q.trim().toLowerCase();
      var hits = data.filter(function (item) {
        if (!needle) return true;
        var blob = (item.title + " " + item.dek + " " + item.topic).toLowerCase();
        return blob.indexOf(needle) !== -1;
      });
      if (needle && hits.length === 0) {
        status.textContent = "No results for \\"" + q.trim() + "\\".";
      } else if (!needle) {
        status.textContent = hits.length + " article" + (hits.length === 1 ? "" : "s") + " in the archive";
      } else {
        status.textContent = hits.length + " result" + (hits.length === 1 ? "" : "s");
      }
      results.innerHTML = hits.map(function (item) {
        return '<article class="search-hit"><a href="' + item.url + '"><p class="search-meta">' + item.topic + " · " + item.date + '</p><h2>' + item.title + '</h2><p>' + item.dek + '</p></a></article>';
      }).join("");
    }

    fetch("/search/search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (j) {
        data = j;
        var q = getQuery();
        if (q) input.value = q;
        render(input.value);
      })
      .catch(function () { status.textContent = "Could not load search index."; });

    input.addEventListener("input", function () { render(input.value); });
  })();
  </script>
"""


def main():
    from site_data import load_site

    site = load_site()
    nl = html_newsletter_attr(site["newsletter_active"])
    html = f"""<!DOCTYPE html>
<html lang="en"{nl}>
<head>
{head_scripts(False)}
{HEAD_ICONS}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex,follow">
  <title>Search | Why Do We Need AI?</title>
  <meta name="description" content="Search articles on Why Do We Need AI—tests, guides, and tools for small-business owners.">
  <link rel="canonical" href="https://whydoweneedai.com/search/">
  <meta name="twitter:site" content="@whydoweneedai">
{FONT}
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
{header_nav("/search/")}
  <main class="page-main article-main" id="main-content">
    <header class="article-header">
      <h1>Search</h1>
      <p class="article-dek">Find guides and documented tests by title, topic, or keyword.</p>
    </header>
    <label class="newsletter-label" for="search-input">Search articles</label>
    <input id="search-input" class="search-input" type="search" name="q" autocomplete="off" placeholder="e.g. invoices, ROI, ChatGPT">
    <p id="search-status" class="search-meta" role="status" aria-live="polite"></p>
    <div id="search-results" class="search-results"></div>
  </main>
{footer_html()}
{SEARCH_SCRIPT}
</body>
</html>
"""
    out = ROOT / "search" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    print("search ok")


if __name__ == "__main__":
    main()
