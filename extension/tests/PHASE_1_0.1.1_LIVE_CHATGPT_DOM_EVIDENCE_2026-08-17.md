# Phase 1 0.1.1 — live ChatGPT DOM evidence for Manual Surface v2

Date: 2026-08-17
Source: owner-supplied report produced by browser agent against authenticated built-in ChatGPT browser.
Probe ID: `YMB-CHATGPT-DOM-001`.

Status: **FACTUAL DOM EVIDENCE — governs the current ChatGPT code-block adapter implementation.**

## Environment

Observed page:

```text
https://chatgpt.com/c/6a82924e-5ed0-83eb-84a2-851ddad40c88
```

CDP/full DevTools was unavailable. Browser-evaluate DOM inspection was used. No Copy or Send control was clicked.

## Assistant container facts

The selected assistant turn is a `SECTION` with:

```html
<section
  class="text-token-text-primary w-full ..."
  dir="auto"
  data-turn-id="0542a941-eacf-4760-a8b5-7efaa8854b3c"
  data-turn-id-container="0542a941-eacf-4760-a8b5-7efaa8854b3c"
  data-testid="conversation-turn-74"
  data-turn="assistant">
```

Inside it is a message container:

```html
<div
  data-message-author-role="assistant"
  data-message-id="f48b96ab-2c9c-4e52-a549-2f8cb2e76ac3"
  dir="auto"
  data-message-model-slug="gpt-5-6-thinking"
  class="min-h-8 text-message relative flex w-full flex-col items-end ...">
```

For both code-block roots and their local Copy controls, these exact ancestor lookups were observed as FOUND:

```js
el.closest('section[data-turn="assistant"][data-turn-id]')
el.closest('[data-message-author-role="assistant"]')
```

## Current code-block family

Nine structural code blocks were observed in DOM order. The current family is **not** generic `<pre><code>`.

Each block root is:

```text
PRE
class="overflow-visible! px-0!"
data-start="..."
data-end="..."
```

The final observed block additionally had `data-is-last-node=""`.

Facts common to the nine blocks:

- `<pre>` exists and is the block root;
- `<code>` was not observed;
- `#code-block-viewer` was not observed;
- displayed block text is hosted by a CodeMirror `.cm-content` element;
- the `.cm-content` element has `role="textbox"`, `aria-multiline="true"`, `aria-readonly="true"`, `contenteditable="false"`;
- the local Copy control is structurally inside the same `PRE`;
- the minimum common ancestor of the block and local Copy is the `PRE` itself;
- each observed `PRE` contained exactly one button.

This factual family supersedes the previous current-DOM hypothesis that required `<pre><code>`.

## Current local Copy facts

Representative observed local Copy:

```html
<button type="button"
  class="flex gap-1 items-center select-none pointer-events-auto py-2 text-sm font-medium hover:bg-black/5 dark:hover:bg-white/10 size-9 rounded-full px-2"
  aria-label="Копировать"
  data-state="closed">
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
       aria-hidden="true" class="icon-md">
    <use href="/cdn/assets/sprites-core-0beb1f83.svg#7fccfb"
         fill="currentColor"></use>
  </svg>
</button>
```

Observed fields:

```text
tagName       BUTTON
id            absent
role          absent
aria-label    Копировать
title         absent
data-testid   absent
name          absent
data-state    closed
textContent   empty
SVG count      1
size           36 x 36 px
```

The observed sprite reference was:

```text
/cdn/assets/sprites-core-0beb1f83.svg#7fccfb
```

Two toolbar layout variants were observed inside the `PRE`:

```text
DIV.pointer-events-none.absolute.end-1.5.top-1.z-2...
```

and

```text
DIV.flex.flex-row.items-center.gap-0.5.justify-self-end
```

The Copy remains a descendant of the same `PRE` in both cases.

## Generic response Copy observation

For the selected assistant turn:

```text
local Copy controls inside <pre>: 9
Copy controls outside <pre>:      0
generic response Copy:            not observed
```

Therefore generic-response Copy exclusion remains required by contract, but this particular probe did not provide a live instance of that control.

## Exact selector facts

For every observed block root and its local Copy:

```text
closest('section[data-turn="assistant"][data-turn-id]') => FOUND
closest('[data-message-author-role="assistant"]')      => FOUND
```

For each local Copy:

```text
data-testid  NULL
aria-label   Копировать
title        NULL
name         NULL
textContent  empty
svg count    1
```

`instanceof HTMLButtonElement` could not be tested in that browser-evaluate environment because its isolated constructor lookup failed; this is an environment limitation, not a DOM conclusion.

## Implementation consequences frozen from observed facts

These are direct consequences of the owner contract plus observed DOM, not speculative selector guesses:

1. Current ChatGPT adapter must support a `PRE` root with no `<code>` descendant.
2. Current displayed text must be captured from the block structure/CodeMirror body rather than requiring `<code>` or `#code-block-viewer`.
3. Current local Copy can be resolved structurally inside the same `PRE`; a sibling-toolbar assumption is unnecessary for this family.
4. The current local Copy can be recognized from block-local structure plus its Copy semantics (`aria-label="Копировать"`) without inspecting block text.
5. Manual ON decoration must not depend on protocol/content validity.
6. The old K-02 current-DOM model `<pre><code>` is not factual for this observed production ChatGPT family and must not remain the primary current adapter.
7. Legacy/writing-block adapters may remain only as compatibility families and must not complicate or override the direct current `PRE` family.

## Safety / side effects

The probe did not click local Copy, generic Copy, or Send. No Yandex command or Yandex API initiation was intentionally performed by the probe.

No production code was changed by this evidence record itself.
