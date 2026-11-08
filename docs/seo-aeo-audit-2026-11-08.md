# SEO and answer-discovery audit response

Baseline: main de821c99053c02fc172b5a685947f1504aa7fcbd, after PR #45 merged. No production merge or deployment is part of this change.

## Implemented
- Stable Organization and Ross C Person identifiers across indexable pages. Public brand X profile is the only sameAs. No surname, personal profile, photo or invented credentials.
- BlogPosting publisher/author references, visible-H1 headlines and consistent modified-date metadata. Existing visible breadcrumbs retained; article BreadcrumbList added. Existing hub breadcrumbs retained.
- Blog archive CollectionPage/ItemList and hub article lists.
- Removed repetitive brand suffix from article search titles; shortened four unwieldy titles and three descriptions without imposing a character limit or rewriting visible headlines.
- Existing useful verdicts moved forward; concise summaries where needed. All original useful paragraphs, worked examples, evidence, correction history and tables preserved. No automatic FAQ or question-heading quota.
- Shared How we test page linked from all four experiments; distinguishes synthetic inputs, held-out cases, mechanical versus judgment grading and independent review limits.
- Useful hub reading paths, not word-count padding. Personal-use articles remain outside the business hubs.
- Server-rendered ReadyScore explanation: six 0–3 factors, conversion to 100, exact bands, clearly illustrative example, limitations and contact-details disclosure. Quiz behavior unchanged.
- Targeted primary-source links and qualification of a small pilot sample as screening, not statistical validation.
- RSS with 17 articles, discovery links, default social images and optional curated llms.txt. No claimed ranking benefit from llms.txt.
- Explicit sitemap content-change dates; no build-clock freshness. Original publication dates preserved.
- Responsive header-logo assets, preserving the original artwork.

## Verified before changes
29/29 sitemap URLs returned 200 with self-canonicals. All 17 posts had valid BlogPosting JSON. Redirects, real 404, HSTS and robots were working. Spoofed AI user-agent requests received content, which does not prove access from actual crawler IPs.

The About page already contained a Person; articles and hubs already had visible breadcrumbs; invoice/readiness pages already provided clear answers. Desktop/mobile New & noteworthy variants are already mutually hidden with CSS. There is one site AdSense loader; Google's second implementation script is injected by Google, not a duplicate installation.

## Performance evidence and limits
Fresh production PageSpeed lab runs, not field data:
- Homepage: mobile 95, LCP 2.7s, TBT 110ms, CLS .022; desktop 99, LCP .7s, CLS .006.
- Lead-follow-up article: mobile 72, LCP 4.3s, TBT 30ms, CLS 0; desktop 94, LCP .8s, CLS .139.
- Neither page has CrUX field data. The audit's 9.7s homepage observation did not reproduce.
- Article LCP is introductory text with render delay. Desktop shifts flag logo sizing/font swaps. Responsive logo sizing is addressed; broader font/render-path tuning requires repeat measurement after release. No claim that Core Web Vitals are solved.
- Ad and analytics behavior left unchanged: these tests do not establish ads as the cause of slow article LCP.

Reports:
https://pagespeed.web.dev/analysis/https-whydoweneedai-com/yq451vzg40?form_factor=mobile
https://pagespeed.web.dev/analysis/https-whydoweneedai-com-blog-ai-lead-follow-up-test/xmcfl2q2qs?form_factor=mobile

## Requires owner access or a separate decision
- Google Search Console and Bing Webmaster Tools: inspect existing property first, complete any ownership/authentication step with owner approval, submit https://whydoweneedai.com/sitemap.xml, inspect indexing and impression data. No account setup, verification change or submission attempted.
- IndexNow: no key created or endpoint submissions made. Requires approved setup and deployment workflow; it is not a substitute for search-console diagnosis and does not guarantee indexing.
- Author identity expansion, photo, personal LinkedIn and external profile edits: not performed. Current Ross C identity is intentional.
- Outreach, backlinks and third-party AI citation checks: no new accounts, posts or contacts made. A spot-check cannot establish absence from an index or guarantee future citations.
- Production merge/deploy still requires authorization; this is a draft change for review.

## Audit advice not applied mechanically
Google does not impose a 60-character title limit or a magic word count. No compulsory FAQ blocks, synthetic results, unsupported credentials or artificial updated dates were added. SearchAction for Google's sitelinks search box is obsolete. llms.txt is a convenience index, not required AI optimization. Generic decision frameworks do not need arbitrary outbound-link quotas.

https://developers.google.com/search/docs/appearance/title-link
https://developers.google.com/search/docs/fundamentals/seo-starter-guide
https://developers.google.com/search/blog/2024/10/sitelinks-search-box
https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

## Reproduction
Run python3 scripts/regenerate-site.py, python3 scripts/check-discovery.py, python3 scripts/check-seo-content.py, python3 scripts/check-editorial-pilot.py and python3 scripts/check-reader-categories.py. Check Python compilation, JavaScript syntax, whitespace and repeat-build idempotence. The older check-prose-unchanged.py/--check-prose assertions are for no-copy-change work; this intentional editorial change uses the narrower evidence/content-preservation regression instead.
