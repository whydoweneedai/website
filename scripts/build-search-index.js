#!/usr/bin/env node
/**
 * Regenerate /search/search-index.json from data/site.json
 */
const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");
const site = JSON.parse(fs.readFileSync(path.join(root, "data/site.json"), "utf8"));
const topics = Object.fromEntries(site.topics.map((t) => [t.slug, t.name]));

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function formatDisplayDate(iso) {
  const d = new Date(`${iso}T12:00:00`);
  return `${MONTHS[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
}

const index = site.articles
  .map((a) => ({
    title: a.searchTitle,
    dek: a.searchDek,
    topic: topics[a.topic],
    topicSlug: a.topic,
    url: `/blog/${a.slug}/`,
    date: formatDisplayDate(a.date),
    dateIso: a.date,
  }))
  .sort((a, b) => (a.dateIso < b.dateIso ? 1 : -1));

fs.writeFileSync(
  path.join(root, "search/search-index.json"),
  JSON.stringify(index, null, 2) + "\n"
);
console.log("Wrote", index.length, "entries to search/search-index.json");
