# KW-002 / BLOOD & SAND — STEP07 RANKING-QUERY SOURCE LIMITATION ACCEPTANCE

Status: **CURRENT ACCEPTANCE AUTHORITY**
Date: 2026-09-18

## 1. Decision

Step07 is accepted as:

`PASS_ACCEPTED_WITH_EXTERNAL_SOURCE_LIMITATION`

The ranking-query lane is recorded as:

`SOURCE_UNAVAILABLE_DECLARED_LIMITATION`

This is not a zero-query result and is not a claim of full competitor ranking-query recall.

## 2. Preserved accepted evidence

```text
SOURCE_URL_ROWS = 1976
AUTHORIZED_COMPETITORS = 32
CANDIDATE_IDENTITIES = 2172
PAGE_PROVENANCE_ROWS = 3948
STEP08_ELIGIBLE = 794
RANKING_QUERY_OBSERVATIONS = 0
```

The full-volume access-state correction remains accepted, including:

```text
SOURCE_URL_ROWS_REVALIDATED = 1976/1976
OZON_ROWS_CORRECTED = 27/27
BLOCK_OR_ERROR_EVIDENCE_MISCLASSIFIED_AS_INSPECTED = 0
```

No semantic candidate or immutable page-provenance rewrite is introduced by this acceptance.

## 3. Source-recovery evidence

The ranking-query source blocker was tested independently in two materially different execution environments:

1. ChatGPT Work during the Step07 post-acceptance correction;
2. Codex Windows during `KW002_STEP07_RANKING_QUERY_SOURCE_RECOVERY_CODEX_WINDOWS_2026-09-18`.

Both concluded that no legitimately accessible source was available that simultaneously supplied real competitor domain/URL -> raw query -> Yandex organic ranking evidence under the allowed access policy.

The Codex Windows recovery checked serious candidates including Keys.so, SpyWords, Topvisor, MegaIndex, Yandex Webmaster and additional alternatives. Observed paths were authenticated/paid, masked/demo-only, owned-site-only, wrong-lane, Google-oriented, inaccessible, or otherwise insufficient for admissible competitor ranking-query evidence.

No purchase, credential extraction, CAPTCHA bypass, paywall bypass, cookie/session theft or evidence fabrication was performed.

## 4. Methodological interpretation

```text
SOURCE_UNAVAILABLE != ZERO RANKING QUERIES
SOURCE_UNAVAILABLE != COMPLETE COMPETITOR RECALL
SOURCE_UNAVAILABLE != PERMISSION TO FABRICATE
```

The page-surface Step07 lane remains valid evidence. The absent reverse-index ranking-query lane remains a known recall limitation.

A commercial/external enrichment source is not an unconditional baseline dependency unless access to that source is part of the frozen execution scope or is legitimately available.

## 5. Persistent known limitation

The accepted Step07 candidate universe does not contain a reverse-index portfolio of all Yandex organic queries for the 32 authorized competitor domains.

Therefore later artifacts MUST NOT claim exhaustive competitor ranking-query coverage.

The limitation remains active through downstream work unless later superseded by legitimate ranking-query acquisition.

## 6. Reopen condition

If a legitimate approved Yandex organic domain/URL→query source or owner-provided admissible export becomes available later, the ranking-query lane may be reopened as enrichment.

Such enrichment must preserve existing immutable evidence, run the authorized competitor universe under the then-current rule, reconcile new candidates, and re-evaluate downstream dependency impact before accepted results are changed.

## 7. Forward gate

Step07 is no longer blocked by the unavailable external source.

Step08 execution is still NOT started.

Forward state:

```text
STEP07 = PASS_ACCEPTED_WITH_EXTERNAL_SOURCE_LIMITATION
STEP07_RANKING_QUERY_LANE = SOURCE_UNAVAILABLE_DECLARED_LIMITATION
KNOWN_RECALL_LIMITATION = ACTIVE
STEP08 = NOT_STARTED_PREPARATION_REQUIRED
WORDSTAT_CALLS_ALLOWED_NOW = 0
YMB_SEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
NEXT = STEP08_PREPARATION
```

Step08 requires its own preparation/release and provider gates before any Wordstat execution.

## 8. Acceptance

```text
MAIN_CHAT_ACCEPTANCE = ACCEPTED
HISTORICAL_DEFECT_LINEAGE_PRESERVED = true
PAGE_SURFACE_RESULT_PRESERVED = true
ACCESS_STATE_CORRECTION_PRESERVED = true
RANKING_QUERY_DATA_FABRICATED = false
FULL_COMPETITOR_RANKING_QUERY_RECALL_CLAIM = false
```
