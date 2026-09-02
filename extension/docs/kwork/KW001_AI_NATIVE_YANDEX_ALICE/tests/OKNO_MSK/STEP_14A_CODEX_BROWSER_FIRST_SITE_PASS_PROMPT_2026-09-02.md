# Codex prompt — OKNO_MSK Step 14A browser-first site pass

Execute ONLY the independent current-site pass required to finish Step 14A for OKNO_MSK.

Repository:
`MaksimUnimax/Yandex_direct`

Branch:
`roadmap/kwork-productization-2026-08-28`

Public site:
`https://okno-msk.ru/`

## Main instruction

**Use the Codex browser as the PRIMARY tool. Do not build, debug or qualify a custom crawler.**

The goal is to actually inspect the current public site and return current-site evidence for Step 14.

Read first:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_14_CODEX_BROWSER_FIRST_DISCOVERY_CORRECTION_2026-09-02.md`

Then perform the site pass.

## What to do in the browser

1. Open `https://okno-msk.ru/`.
2. Inspect the rendered homepage, main navigation, mega-menu, footer and visible same-site links.
3. Follow same-site public links systematically.
4. Open discovered pages and record at minimum:
   - current URL;
   - final URL after navigation/redirect;
   - page title;
   - H1;
   - how the page was discovered (homepage nav, footer, page link, sitemap, upstream known URL, etc.);
   - source page/path that led to it where useful.
5. Continue discovery through newly opened same-site pages so the pass is not limited to the already-known Step-12/13/14 URL set.
6. If a public sitemap is available, inspect it as an ADDITIONAL discovery route and open/materially reconcile URLs that are not already represented by browser navigation.
7. Load the known Step-12/13/14 URL inputs only for reconciliation. Do NOT use them as the discovery universe.

## Important discovery goal

Surface every current public URL found by the browser/sitemap that is absent from the known Step-12/13/14 set.

For each such URL, record enough current page evidence for ChatGPT to decide later whether it is architecture-material.

Do NOT make page-ownership or structural decisions yourself.

## Verify the 15 planned Step-14 internal links

Read:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_14_INTERNAL_LINK_ARCHITECTURE.tsv`

Identify the 15 rows with the Step-14 IMPLEMENT recommendation.

For EACH of the 15:

1. open the current source page in the browser;
2. inspect the current page DOM/links or browser-visible link target evidence;
3. determine whether the source currently contains a real link to the planned target;
4. classify exactly once:

```text
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
```

`AS_IS_PRESENT` requires actual current source-page link evidence. Do not infer it merely because both pages exist or are semantically related.

Account for all 15 exactly once.

## Expected outputs

Create/persist under:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/`

at minimum:

1. `STEP_14A_CODEX_BROWSER_DISCOVERED_URLS.tsv`
2. `STEP_14A_CODEX_BROWSER_PAGE_PROFILE_LEDGER.tsv`
3. `STEP_14A_CODEX_BROWSER_NEW_URL_RECONCILIATION.tsv`
4. `STEP_14A_CODEX_BROWSER_REQUIRED_EDGE_VERIFICATION.tsv`
5. `STEP_14A_CODEX_BROWSER_PASS_REPORT.md`

Recommended fields for discovered URLs:

```text
url
final_url
title
h1
discovery_origin
discovery_source_url
known_upstream_yes_no
browser_read_state
notes
```

Recommended fields for 15-edge verification:

```text
edge_id
source_url
target_url
source_opened
target_opened
current_link_present
observed_link_target
anchor_or_context
as_is_state
notes
```

## Use of code

Code is allowed ONLY as a helper after browser evidence is collected, for example to:

- deduplicate URLs;
- normalize URLs;
- compare browser-collected URLs with Step-12/13/14 TSV inputs;
- generate TSV/JSON/Markdown files;
- count rows.

Do NOT build or run another custom site crawler.

## Boundaries

Do NOT:

- execute Step 15;
- use GenSearch/Alice;
- make paid provider/API calls;
- mutate the public website;
- create/delete/merge target pages;
- add redirects/canonical decisions;
- change keyword/page ownership;
- claim final Step-14 acceptance.

## Git discipline

After the browser pass is complete:

1. commit the browser evidence artifacts;
2. fetch current remote if necessary;
3. integrate safely if remote advanced;
4. NORMAL-PUSH to `origin roadmap/kwork-productization-2026-08-28`;
5. no force-push.

## Final report

Return:

```text
FINAL_COMMIT_SHA
PUSH_STATUS

BROWSER_PASS_EXECUTED = true
TOTAL_BROWSER_DISCOVERED_URLS
TOTAL_BROWSER_OPENED_READ_URLS
SITEMAP_URLS_RECONCILED
CURRENT_URLS_NOT_IN_UPSTREAM
UNREAD_OR_BLOCKED_URLS

PLANNED_IMPLEMENT_EDGE_BASELINE = 15
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
EDGE_ACCOUNTING = 15/15

ARTIFACTS_CREATED
BLOCKERS_OR_LIMITATIONS
STEP15_EXECUTED = false
```

Do not return another "ready to run" report. Perform the browser pass and return the actual collected results.
