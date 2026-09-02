# KW-001 / OKNO_MSK — Step 14A Run 9 ChatGPT reconciliation

Date: 2026-09-02
Status: **PARTIAL PASS — LINK TOPOLOGY VERIFIED / DISCOVERY COMPLETENESS NOT PROVEN**

## Input evidence

Primary owner-supplied package:

`STEP_14A_CODEX_BROWSER_RESULT_RUN9.md`

Local package SHA-256 supplied to this reconciliation:

`36e4083ca727ac93a0223ae82ec72c08c88e61469db8b4ff184563c899be51d9`

Run identity from package:

```text
RUN_ID = 9
IN_APP_BROWSER_USED = true
BROWSER_PASS_EXECUTED = true
STEP15_EXECUTED = false
LOCAL_COMMIT = eff92ac
```

## Accepted Run-9 evidence

The following Run-9 evidence is accepted as current browser evidence:

```text
browser-discovered normalized candidates = 158
opened/read pages = 8
planned IMPLEMENT edges checked = 15/15
AS_IS_PRESENT = 9
AS_IS_ABSENT_PLANNED = 6
BLOCKED_OR_UNVERIFIED = 0
NOT_APPLICABLE = 0
```

The 15-edge result is implementation/topology evidence and is now stored separately in:

`STEP_14A_RUN9_INTERNAL_LINK_AS_IS_RECONCILIATION.tsv`

The Step-12/14 recommendation dimension remains separate from the current as-is dimension:

```text
RECOMMENDATION_STATE = IMPLEMENT for all 15 accepted recommendations
CURRENT_AS_IS_STATE = 9 PRESENT + 6 ABSENT_PLANNED
```

The six currently absent recommended links are:

```text
IL0021
IL0029
IL0040
IL0041
IL0053
IL0059
```

The nine currently present links are:

```text
IL0008
IL0009
IL0025
IL0038
IL0047
IL0049
IL0062
IL0065
IL0066
```

This closes the prior overclaim that live source + live target + semantic fit proved an implemented current link.

## Discovery reconciliation

Run 9 reports:

```text
CURRENT_URLS_NOT_IN_UPSTREAM = 0
```

That statement is accepted only in its literal forward direction:

```text
RUN9_DISCOVERED_URL -> WAS IT ALREADY REPRESENTED UPSTREAM?
```

It does NOT establish the reverse direction:

```text
UPSTREAM_CURRENT_URL -> WAS IT DISCOVERED BY RUN9?
```

Therefore:

```text
CURRENT_URLS_NOT_IN_UPSTREAM = 0
!=
UPSTREAM_URLS_NOT_DISCOVERED_BY_RUN9 = 0
```

### Direct reverse-coverage counterexamples

Run 9 explicitly excluded the `/calculator` candidate from its 158-row candidate set. The accepted Step-14 current URL recheck had already established `https://okno-msk.ru/calculator` as a live current page.

The accepted Step-14 current URL recheck also established the QF017 specialist:

`https://okno-msk.ru/verandy/panoramnye-okna-na-terrasu`

as live and current. The Run-9 veranda block did not discover that URL.

Additional previously accepted current Step-14 pages, especially informational articles used as implementation targets, were not all represented in the Run-9 candidate set. Run 9 therefore cannot be treated as a complete reverse coverage of even the already-known current Step-14 URL universe.

### Current public-web adversarial check

A fresh independent current-web check after Run 9 surfaced public pages outside the Run-9 158-row main-domain candidate list, including:

`https://okno-msk.ru/o-kompanii/llm-info-page/`

and current public GEO subdomains such as:

```text
https://pushkino.okno-msk.ru/
https://ramenskoe.okno-msk.ru/
https://krasnogorsk.okno-msk.ru/
https://odincovo.okno-msk.ru/
```

The AI/LLM information page is not automatically a Step-14 Search-architecture ownership page; it is architecture-relevant evidence for later AI stages and must not be silently ignored. GEO subdomains likewise require scope classification rather than automatic inclusion or exclusion.

These findings prove that Run 9 was a useful browser sample and link-topology check, not a complete public-site enumeration.

## Sitemap boundary

Run 9 recorded:

```text
SITEMAP_URLS_RECONCILED = false
```

because the browser client blocked the attempted `robots.txt` route.

This is a limitation only. It does not prove absence of a sitemap.

The public site is externally reported as exposing `https://okno-msk.ru/sitemap.xml`, but the sitemap contents were not acquired into Run 9 and are therefore not used here as complete URL-enumeration evidence.

## Semantic impact on frozen architecture

Run 9 produced no newly discovered URL that it itself classified as outside the Step-12/13/14 record set. Therefore Run 9 by itself does not require reopening any semantic ownership unit.

However, because discovery completeness is not proven and current adversarial web checks surfaced additional public pages outside the Run-9 list, Step 14 cannot return to an overall COMPLETE state solely from Run 9.

No Run-9 evidence supports any new destructive action.

Preserve:

```text
supported new-page actions = 0
supported merge/delete/redirect/canonical actions = 0
active phrases = 2332
assigned phrases = 2313
preserved unresolved = 19
structural units = 168
Step-13 effective pairs = 199
Step-13 query-family cases = 21
```

## Corrected Step-14A status

```text
STEP14A_RUN9_BROWSER_EXECUTED = PASS
STEP14A_PLANNED_EDGE_ACCOUNTING = PASS_15_OF_15
STEP14A_AS_IS_LINK_TOPOLOGY = PASS
STEP14A_AS_IS_PRESENT = 9
STEP14A_AS_IS_ABSENT_PLANNED = 6
STEP14A_BROWSER_FORWARD_RECONCILIATION = PASS_WITH_BOUNDARY
STEP14A_REVERSE_UPSTREAM_COVERAGE = FAIL_NOT_PROVEN
STEP14A_SITEMAP_RECONCILIATION = NOT_COMPLETE
STEP14A_PUBLIC_SITE_DISCOVERY_COMPLETENESS = NOT_PROVEN
STEP14_SEMANTIC_BASELINE = PROVISIONAL_PASS_PRESERVED
STEP14_OVERALL = REOPENED_PARTIAL_PASS
STEP15 = BLOCKED
```

## What is now genuinely closed

1. The previous internal-link implementation overclaim is closed.
2. All 15 planned Step-14 IMPLEMENT recommendations now have a literal current as-is state.
3. 9 are already implemented.
4. 6 remain implementation recommendations, not current links.
5. Run history remains preserved; Run 9 is accepted as valid browser evidence within its observed scope.

## What is not closed

1. Complete current public-site discovery.
2. Reverse accounting from the accepted current Step-14 URL universe into Run-9 discovery.
3. Sitemap reconciliation.
4. Scope classification of newly surfaced current public pages outside Run 9, including the AI/LLM page and GEO subdomains.

## Next analytical action

Do NOT reopen the 15-edge topology work.

Do NOT rerun Step 15.

Next work should be limited to closing the discovery-universe gap using current public evidence and then classifying only genuinely newly surfaced pages against the existing frozen Search architecture. No automatic new page, merge, redirect, canonical or ownership action is authorized by discovery alone.
