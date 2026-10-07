# Why Do We Need AI — Editorial Playbook

This file is the working standard for new and updated blog content. The goal is to build a recognizable publication, not a collection of generic AI articles.

## Editorial promise

Help a small-business owner make a better AI or automation decision in plain English.

Every article should answer a real operational question and leave the reader with something they can use: a framework, scorecard, checklist, calculation, template, test plan, worked example, or documented experiment.

## Content pillars

1. **Foundations** — AI vs. automation, terminology, what AI is and is not useful for.
2. **Operations** — workflows, automation design, ROI, implementation, measurement.
3. **Buying & evaluation** — tool selection, pilots, total cost, vendor questions, exit plans.
4. **Risk & trust** — data handling, review, privacy, reliability, high-stakes use.
5. **Field tests** — first-hand experiments with specific tools or workflows. These must clearly state what was actually tested.

## Article types to rotate

Do not publish the same listicle template repeatedly. Rotate among:
- decision frameworks
- how-to guides
- calculators / ROI walkthroughs
- checklists and scorecards
- worked examples
- comparisons that show tradeoffs rather than declaring a universal winner
- first-hand field tests
- myth / misconception explainers
- interviews or practitioner perspectives when available

## Minimum standard for every article

Before publication, the article must contain:
- one clear reader problem
- one original framework, tool, calculation, or practical artifact
- at least one concrete worked example
- explicit limits, risks, or cases where the advice does not apply
- relevant internal links to other guides
- a visible author/editorial-team link
- published and modified dates
- useful metadata and canonical URL
- no fabricated case study, quote, statistic, customer result, or first-hand testing claim

## Anti-slop rules

Avoid:
- generic introductions about AI “changing the world”
- padding articles to hit a word count
- repeating the same point under multiple headings
- fake urgency
- vague claims like “AI saves businesses countless hours”
- unsupported statistics
- invented experts, customers, or anecdotes
- product recommendations based only on marketing pages
- excessive “top 10” posts that add no original decision support
- calling a workflow “AI” when rules-based automation is sufficient

Prefer:
- specific operating examples
- calculations with assumptions shown
- decision criteria
- examples of when not to use AI
- plain language
- short explanations when a concept is simple
- clear distinction between illustrative examples and real tests

## Field-test standard

When we begin publishing tool tests:
1. State the exact task tested.
2. State the input set and sample size.
3. Use the same test cases for compared products.
4. Define the scoring rubric before discussing results.
5. Record failures and edge cases, not only successful outputs.
6. Disclose plan/pricing context when relevant.
7. Do not generalize beyond what the test supports.
8. Include the test date because AI products change quickly.

## Sourcing standard

Use primary documentation for product features, pricing, privacy, terms, or technical behavior whenever possible.

For factual claims that can change, verify them at publication and make the date visible. Avoid filling articles with citations for obvious operational advice; cite where the source materially supports a claim.

## Publishing cadence

Do not dump a large batch of thin posts at once. Favor a steady cadence of substantial pieces.

Working target:
- 1–2 strong new articles per week
- periodic updates to existing cornerstone guides
- field tests only when we actually have something worth testing

Quality outranks volume.

## Internal-link structure

Each article should link naturally to:
- the prior decision a reader should make
- the next decision after this article
- at least one related cornerstone guide where useful

The intended core journey is:

**What should I automate? → Am I ready? → Do I need AI? → Which tool fits? → Did the pilot create value?**

## Editorial QA before merge

Ask:
1. Would this still be useful if the word “AI” disappeared from the headline?
2. What does the reader get here that they could not get from a generic summary?
3. Is any claim pretending to be first-hand when it is not?
4. Is there a clear method or artifact the reader can use?
5. Did we say when the approach should *not* be used?
6. Does the article connect to the rest of the site?
7. Can a skeptical small-business owner follow the logic without jargon?

If the answer to #2 or #4 is weak, the article is not ready.


## Blog index ordering

When publishing or updating `blog/index.html`:
- list article cards by publication date, newest first
- make the newest article the featured card and number it 01
- renumber the remaining cards sequentially
- keep the `Blog.blogPost` structured-data entries in the same newest-first order
- preserve the existing Google Analytics, Google AdSense, metadata, navigation, and footer code while editing the index
