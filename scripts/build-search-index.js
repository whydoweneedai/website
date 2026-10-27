#!/usr/bin/env node
/**
 * Regenerate /search/search-index.json from scripts/articles.json
 * Usage: node scripts/build-search-index.js
 */
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const articles = JSON.parse(
  fs.readFileSync(path.join(root, "scripts/articles.json"), "utf8")
);

const index = articles
  .map((a) => ({
    title: a.searchTitle,
    dek: a.searchDek,
    topic: a.topicLabel,
    topicSlug: a.topic,
    url: `/blog/${a.slug}/`,
    date: a.date,
  }))
  .sort((a, b) => (a.date < b.date ? 1 : -1));

fs.writeFileSync(
  path.join(root, "search/search-index.json"),
  JSON.stringify(index, null, 2) + "\n"
);
console.log("Wrote", index.length, "entries to search/search-index.json");
