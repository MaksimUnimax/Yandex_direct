# Phase 2 Search owner functional run checklist

Date: 2026-08-25  
Status: **ACTIVE — completed runs recorded; continuation plan pinned**

## Authority

```text
LIVE_HEAD_BEFORE_WRITE = e43918296fcafa31c154d1c9fcc0e9161af0a334
PRODUCT_SOURCE = b7869180c229356a6b3d51ac980ec3da5df4c23c
ARTIFACT_SHA256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
OWNER_LIVE_SEARCH = PASS / CLOSED
```

This file is the durable continuation ledger for the sequential owner functional checks performed in the real ChatGPT profile. Secrets are intentionally not recorded.

## Resume rule after any chat/session interruption

1. Read this file from live `main`.
2. Continue from the first row whose verdict is `PENDING`.
3. Keep the owner cadence: **1 run = 1 command/testable function**.
4. Wait until the previous Manual operation is visibly complete before starting the next run.
5. Never blind-retry after any provider initiation with ambiguous outcome.
6. Tests marked `DEFERRED / CONTROLLED QA` must not be reproduced against the real provider unless the owner explicitly decides to do so.

## Completed run ledger

| Run | Check | Observed result | Provider request | Verdict |
|---:|---|---|---|---|
| 1 | Search command while active service = Wordstat | `SERVICE_NOT_ACTIVE` at `MANUAL_ADMISSION` | No | **PASS** |
| 2 | Missing required `queryText` | `MISSING_FIELD` at `COMMAND_VALIDATION` | No | **PASS** |
| 3 | `groupsOnPage=999` | `INVALID_FIELD`; allowed 1–100 | No | **PASS** |
| 4 | Unsupported method `searchAsync` | `UNSUPPORTED_METHOD` | No | **PASS** |
| 5 | Valid Search command with no runtime credentials | `SEARCH_RESULT_V1 / SKIPPED / NO_CREDENTIALS` | No | **PASS — credential guard** |
| 6A | Manual-policy attempt after importing legacy backup | still `NO_CREDENTIALS`; legacy import did not populate current runtime credentials | No | **DIAGNOSTIC / exposed legacy-backup incompatibility** |
| 6B | Convert/import valid V2 settings, then valid Search | `SEARCH_RESULT_V1`, `status=OK`, HTTP 200, `FORMAT_XML`, 5 normalized results, `request_executed=true`, `automatic_retry=false` | **Exactly one confirmed real Search request** | **PASS — owner live Search** |
| 7 | Search Manual permission OFF | `SKIPPED / MANUAL_DISABLED`, HTTP 0 | No | **PASS** |
| 8 | Search cost cap below one-request estimate | `SKIPPED / COST_LIMIT`, HTTP 0 | No | **PASS** |
| 9 | `SEARCH_TYPE_COM` with `region=225` | `REGION_NOT_SUPPORTED` | No | **PASS** |
| 10 | `SEARCH_TYPE_COM` with `LOCALIZATION_RU` | `LOCALIZATION_NOT_SUPPORTED` | No | **PASS** |
| 11 | Unsupported field `device` | `UNSUPPORTED_FIELD` | No | **PASS** |
| 12 | `queryText` with 41 words | `QUERY_TOO_MANY_WORDS` | No | **PASS** |
| 13 | `maxPassages=6` | `INVALID_FIELD`; allowed 1–5 | No | **PASS** |
| 14 | `docsInGroup=4` | first attempt hit `MANUAL_OPERATION_ACTIVE`; retry returned `INVALID_FIELD`, allowed 1–3 | No | **PASS on retry** |
| 15 | `page=-1` | first attempt hit `MANUAL_OPERATION_ACTIVE`; retry returned `INVALID_FIELD`, allowed 0–1000000 | No | **PASS on retry** |
| 16 | `familyMode=FAMILY_MODE_UNKNOWN` | `INVALID_ENUM` | No | **PASS** |
| 17 | `sortMode=SORT_MODE_RANDOM` | `INVALID_ENUM` at `COMMAND_VALIDATION`; `request_executed=false`, `automatic_retry=false` | No | **PASS** |

## Incidental lifecycle evidence

The owner started the next command too quickly after runs 14 and 15. The Bridge correctly returned:

```text
stage = MANUAL_ADMISSION
code = MANUAL_OPERATION_ACTIVE
request_executed = false
automatic_retry = false
```

These are recorded as lifecycle safety observations, not failures of the intended validation checks. Both intended checks passed on retry after the prior Manual operation completed.

## Current next run

### Run 18 — invalid `sortOrder` enum — PENDING

Execute exactly one command after the previous Manual operation is complete:

```text
SEARCH_API_V1
{
  "method": "search",
  "queryText": "купить ноутбук",
  "searchType": "SEARCH_TYPE_RU",
  "region": "225",
  "page": 0,
  "groupsOnPage": 5,
  "sortOrder": "SORT_ORDER_RANDOM"
}
```

Expected:

```text
YMB_ERROR_V1
stage = COMMAND_VALIDATION
code = INVALID_ENUM
request_executed = false
automatic_retry = false
```

## Planned owner checks after Run 17

| Planned run | Check | Expected boundary | Real provider request? | Status |
|---:|---|---|---|---|
| 17 | Invalid `sortMode` | `INVALID_ENUM` / local validation | No | **PASS** |
| 18 | Invalid `sortOrder` | `INVALID_ENUM` / local validation | No | **PENDING — NEXT** |
| 19 | Invalid `groupMode` | `INVALID_ENUM` / local validation | No | **PENDING** |
| 20 | Invalid `fixTypoMode` | `INVALID_ENUM` / local validation | No | **PENDING** |
| 21 | Invalid `searchType` | `INVALID_ENUM` / local validation | No | **PENDING** |
| 22 | Malformed JSON after `SEARCH_API_V1` | `INVALID_JSON` / local parsing | No | **PENDING** |
| 23 | Conversation Manual mode OFF, valid Search command | `MANUAL_MODE_DISABLED` at Manual admission | No | **PENDING** |
| 24 | Close/reopen popup and verify imported credentials/settings still present in public state | persistence only | No | **PENDING** |
| 25 | Export current settings as V2 and verify structure/checksum/search policy/credential presence without exposing secret values | settings transport only | No | **PENDING** |
| 26 | Re-import the freshly exported V2 settings after all Manual operations are idle; verify no credential loss and no active-runtime corruption | settings import only | No | **PENDING** |
| 27 | Reverse service isolation: active Search + `WORDSTAT_API_V1` command | `SERVICE_NOT_ACTIVE` before provider | No | **PENDING** |
| 28 | Search Autorun permission OFF, attempt Autorun start | `AUTORUN_DISABLED` before provider | No | **PENDING** |
| 29 | Search Autorun happy-path with one real Search request | end-to-end Autorun provider path | **Yes** | **OPTIONAL / PAID — only after fresh official tariff check and explicit owner decision** |
| 30 | Request-count limit inside shared RUN budget | `REQUEST_LIMIT` with no extra provider call after limit | Potentially | **DEFERRED / CONTROLLED QA already covered; do not spend live requests by default** |
| 31 | Provider HTTP/authentication error handling | definite provider error, no automatic second call | Yes | **DEFERRED / CONTROLLED QA already covered** |
| 32 | Timeout/ambiguous provider outcome | `UNKNOWN` / no blind retry | Ambiguous | **DEFERRED / CONTROLLED QA already covered; do not induce live** |

## Notes on budget/request-limit testing

Standalone Manual operations do not accumulate request totals across separate independent button presses. The request-count guard is meaningful when Manual shares an active paused RUN budget or in Autorun. Therefore it is intentionally not tested by repeatedly clicking standalone Manual Search.

## Credential/import finding

The owner possessed a real API key and Folder ID in a legacy settings backup. The legacy backup used old credential nesting and was not compatible with the current V2 import envelope. A V2-compatible backup was generated locally from the owner's file, preserving the secret values without recording them here. After V2 import, Search credentials became available and the real owner-live Search request passed.

## Existing primary live acceptance evidence

The governed Phase-2 provider boundary is already closed by:

```text
extension/tests/PHASE_2_REAL_PROFILE_OWNER_LIVE_SEARCH_PASS_2026-08-25.md
```

This checklist is additional functional owner evidence and a continuation plan; it does not reopen the already accepted Phase-2 live boundary unless a later run exposes a real product defect.
