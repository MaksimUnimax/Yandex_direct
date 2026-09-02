# KW-001 — Step 14 Codex browser-first discovery correction

Date: 2026-09-02
Status: **ACTIVE / STEP-14-SPECIFIC / OWNER-REQUIRED / SUPERSEDES CRAWLER-FIRST EXECUTION DESIGN**

## What was wrong

The Step-14A correction correctly established that a deterministic independent Codex pass is required to discover the current public site and current internal-link topology.

However, the execution design then made an unnecessary and incorrect tool-selection jump:

```text
NEED INDEPENDENT CODEX SITE PASS
-> BUILD CUSTOM CRAWLER
-> QUALIFY CUSTOM CRAWLER
-> DEBUG CRAWLER TERMINATION
```

That was the wrong execution path for this environment because Codex already has a browser capable of opening the public site, navigating links and inspecting current rendered pages.

The result was process drift: instead of collecting the site, work shifted into building and debugging collection infrastructure.

Canonical lesson:

```text
CODEX_PASS_REQUIRED != CUSTOM_CRAWLER_REQUIRED

AVAILABLE_NATIVE_BROWSER_CAPABILITY
-> USE BROWSER FIRST FOR PUBLIC SITE DISCOVERY/READING
-> USE CODE ONLY AS A NARROW HELPER WHEN THE BROWSER CANNOT PRODUCE A REQUIRED MECHANICAL RESULT
```

## Root cause

The method correctly recognized that ChatGPT manual web reads are not a completeness authority by themselves. But that was overgeneralized into the assumption that only a custom crawler could provide the independent Codex pass.

The missing question was:

```text
WHAT IS THE STRONGEST AVAILABLE NATIVE TOOL IN THE ACTUAL CODEX ENVIRONMENT FOR THIS EVIDENCE?
```

Because Codex has a browser, the first execution choice should have been browser-native discovery, not building a new crawler.

## Corrected Step-14 execution rule

For OKNO_MSK Step 14A:

```text
PRIMARY COLLECTION TOOL = CODEX BROWSER
```

Codex must use the browser to:

1. open `https://okno-msk.ru/`;
2. inspect the current rendered homepage/navigation/footer;
3. follow same-site public links systematically;
4. open discovered relevant/public pages;
5. record current URL, final URL, title/H1 and discovery path/source;
6. inspect source pages for the 15 planned Step-14 internal-link recommendations and determine whether the target link actually exists in the current page/link DOM;
7. use public sitemap(s), if available, as an additional discovery route;
8. reconcile browser-discovered URLs against Step 12/13/14 known URLs;
9. surface all newly discovered URLs for ChatGPT semantic review;
10. persist results and normal-push them to GitHub.

## Use of code

Code is allowed only as a narrow helper, for example:

```text
normalizing an already collected URL list;
deduplicating browser-collected URLs;
joining collected results against Step-12/13/14 TSV inputs;
counting rows;
producing final TSV/JSON artifacts from browser evidence.
```

Code must NOT become a new custom site-crawler project when the browser can perform the site pass.

## Required evidence boundary

Browser discovery is still evidence collection, not semantic ownership authority.

Codex must not automatically:

```text
create new pages;
change phrase ownership;
merge/delete pages;
set redirects/canonicals;
change Step-13 conclusions;
execute Step 15.
```

ChatGPT performs the semantic reconciliation after Codex persists the browser-collected evidence.

## Non-repeat control

Before designing an evidence mechanism, ask in this order:

```text
1. WHAT FACT MUST BE OBSERVED?
2. WHICH NATIVE TOOL ALREADY AVAILABLE IN THE EXECUTION ENVIRONMENT CAN OBSERVE IT DIRECTLY?
3. IS CUSTOM CODE ACTUALLY NECESSARY?
```

Do not build infrastructure merely because deterministic evidence is needed.

Canonical marker:

```text
KW001_STEP14_CODEX_BROWSER_FIRST_DISCOVERY_ACTIVE = true
KW001_STEP14_CUSTOM_CRAWLER_NOT_REQUIRED_BY_DEFAULT = true
KW001_STEP14_NATIVE_BROWSER_BEFORE_CUSTOM_COLLECTION_CODE = true
```
