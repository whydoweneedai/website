# Homepage and invoice article pilot

Prepared against `main` at `d94c348`. Local review only; nothing published, pushed, merged or deployed.

## What changed
- Homepage: compact editorial masthead, large illustrated lead, a separate recent-story rail, three illustrated featured cards, and a calmer two-column article list.
- Four original SVG illustrations use the existing brand palette without changing logo artwork. They are editorial illustrations, not product screenshots or test evidence.
- Invoice article: concise headline, illustrated cover with disclosure, direct verdict, three result figures, the $12.20 subtotal failure and practical checks before detailed methodology.
- Main visible article reading drops from 2,069 to about 798 words. Six native expandable sections preserve detailed results, failures, costs, input mix, limits, methods and sources.
- Every original section ID and link remains. The evidence ZIP is untouched. Other articles are unchanged.
- Existing analytics, AdSense, navigation, footer and inactive newsletter setting are preserved.
- Generator changes preserve the design when the site is rebuilt.

## Checks
Passed:
- Full `python scripts/regenerate-site.py` build, including search index generation.
- A second full regeneration produced identical output.
- `python scripts/check-editorial-pilot.py`: local links, media files, alt text and dimensions, one H1 per page, unique IDs, retained original section IDs/links, verbatim evidence-detail preservation, six expandable sections, illustration caption and valid SVG XML.
- Python compilation, Node search-builder syntax and `git diff --check`.
- All four SVGs rendered and visually inspected. Removed a filter that did not render reliably in the SVG preview tool.
- Existing prose checker reports only the invoice article changed, as intended; its other 19 checked pages are unchanged.

Not verified:
- Browser layout at desktop/mobile widths, keyboard navigation, menu, expand/collapse interactions and history. Chromium cannot launch because socket creation is restricted, even after an approved escalation. The cloud browser cannot reach the local HTTP server; file URLs are blocked by its URL policy. No attempt was made to bypass that policy.

Before publishing, run browser QA at 1440, 820, 390 and 320 px, check all six expandable sections with keyboard and mouse, inspect the menu, table scrolling, article navigation/back behavior and image loading. The source includes responsive rules, but these are not a substitute for a real browser pass.
