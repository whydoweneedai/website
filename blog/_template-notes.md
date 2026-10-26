# Article callout HTML snippets

Use these inside `<article class="article-body">` (after the header). Do not change wording in published articles without editorial review.

## Short answer (factual summary)

```html
<div class="short-answer">
  <p><strong>The short answer:</strong> One or two sentences that state what the test or guide supports, with limits.</p>
</div>
```

You may also add `short-answer` alongside `verdict` on an existing styled paragraph:

```html
<p class="verdict short-answer"><strong>The short answer:</strong> …</p>
```

## Our take (editor opinion)

```html
<div class="our-take">
  <p class="our-take-label">Our take</p>
  <p>Your opinion here—clearly labeled, separate from reporting and from the short answer.</p>
</div>
```

Styles live in `blog/styles.css` (`.short-answer`, `.our-take`, `.our-take-label`).
