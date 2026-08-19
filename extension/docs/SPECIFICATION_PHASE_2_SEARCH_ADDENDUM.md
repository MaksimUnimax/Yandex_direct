# SPECIFICATION ADDENDUM — PHASE 2 YANDEX SEARCH / SERP

Status: **MANDATORY CURRENT COMPANION TO `SPECIFICATION.md`**  
Updated: 2026-08-19

This addendum activates the Phase-2 Search adapter after Phase-1 Wordstat LIVE PASS. Where older `SPECIFICATION.md` text still says Search is blocked, this addendum plus `CURRENT_STATE.md` supersede that stale phase-lock wording for Phase 2 only.

Full Phase-2 requirement authority:

```text
extension/docs/PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
```

## A. Enabled services

Current combined product target:

```text
Wordstat [accepted Phase 1]
Search   [Phase 2 development]
```

Still blocked:

```text
Webmaster
Metrika
Direct
```

## B. Protocol routing

Phase-2 registered protocols:

```text
WORDSTAT_API_V1 → Wordstat adapter
SEARCH_API_V1   → Search adapter
```

Unknown/future prefixes remain zero-provider/no-side-effect.

One Autorun RUN still has exactly one immutable `active_service`. Wordstat and Search commands cannot cross-execute in the other service's RUN.

## C. Search first-slice operation

Only the following Search operation is enabled initially:

```text
SEARCH_API_V1
method = search
mode = synchronous text search
REST = POST https://searchapi.api.cloud.yandex.net/v2/web/search
responseFormat = FORMAT_XML
result = SEARCH_RESULT_V1
```

Not enabled in the first slice:

```text
searchAsync / operation polling
image search
generative search
HTML normalization
browser scraping
```

## D. Search command

Canonical command:

```text
SEARCH_API_V1
{
  "method":"search",
  "queryText":"...",
  "searchType":"SEARCH_TYPE_RU",
  "region":"225",
  "page":0,
  "groupsOnPage":10,
  "familyMode":"FAMILY_MODE_MODERATE",
  "fixTypoMode":"FIX_TYPO_MODE_ON",
  "sortMode":"SORT_MODE_BY_RELEVANCE",
  "sortOrder":"SORT_ORDER_DESC",
  "groupMode":"GROUP_MODE_FLAT",
  "docsInGroup":1,
  "maxPassages":4,
  "l10n":"LOCALIZATION_RU"
}
```

`folderId`, API key, IAM token and other secrets are operator-local and never assistant-command fields.

Validation must enforce the current official API bounds recorded in the Phase-2 requirements document before provider initiation.

## E. Search credentials

Search reuses the trusted local Yandex Search API credential/folder storage where compatible. A working Wordstat credential must not be destroyed or rewritten merely because Search access is unavailable.

Credential/access outcomes retain the common capability model:

```text
PRESENT
MISSING
INVALID_OR_EXPIRED
NO_ACCESS
```

Pre-network credential failure:

```text
request_executed = false
automatic_retry = false
provider requests = 0
```

## F. Search cost policy

Search is a paid service operation.

Current 2026-08-19 tariff snapshot is recorded in the Phase-2 requirements document. Operator policy must contain a tariff source/snapshot and Search request/RUB ceilings.

Unless explicit tariff-window logic is implemented, reserve the conservative higher synchronous tariff per accepted initiation.

Budget reservation happens before irreversible provider initiation.

Manual on a PAUSED Search RUN uses the same RUN request/cost counters and cannot bypass them.

## G. Search result normalization

Provider `rawData` is Base64 XML. Bridge must decode it and produce `SEARCH_RESULT_V1` with stable common metadata and tolerant organic-result normalization.

Normalized document target:

```text
rank
url
domain | null
title | null
snippet | null
modtime | null
```

Yandex documents Search response fields as optional/mutable. Missing optional fields therefore must not fabricate values or fail a whole request when an identifiable document/result can still be preserved.

## H. Search safety invariants

All accepted common-core invariants remain mandatory:

```text
external Yandex Manual action
native Copy independence
conversation binding fail-closed
owner-tab fence
one accepted command → at most one provider initiation
no silent composer overwrite
worker-owned durable outbox
Send at most once after commit
ready/Microphone completion
watch-only committed recovery
UNKNOWN provider outcome → no blind retry
always-on YMB_ERROR_V1
Debug adds redacted diagnostics only
no secrets in command/result/error/debug/GitHub
```

Search must reuse this core rather than introduce a parallel delivery FSM.

## I. SEARCH_RESULT_V1 common envelope

```text
SEARCH_RESULT_V1
{
  bridge,
  version,
  service:"search",
  operation:"search",
  request_id,
  run_id,
  status,
  reason,
  cost_estimate,
  policy,
  command,
  http_status,
  elapsed_ms,
  result:{
    results:[...],
    result_count,
    response_format:"FORMAT_XML"
  },
  request_executed,
  automatic_retry
}
```

No runtime `job_id` requirement.

## J. Search failure semantics

```text
2xx → normal result
4xx/5xx after request → ERROR, request_executed:true, no auto retry
validation/policy/credential rejection before fetch → request_executed:false
uncertain timeout/network boundary → request_executed:"UNKNOWN", automatic_retry:false
```

Identical blind retry after an UNKNOWN outcome is forbidden.

## K. Phase-2 acceptance

Before owner handoff of any combined Wordstat+Search candidate:

```text
focused Search development tests PASS
all affected existing Wordstat/core tests PASS
new exact candidate frozen
mandatory QA transport runbook PASS before Codex prompt
complete living full gate + mandatory Search addendum PASS
zero real Yandex requests during controlled gate
then minimal owner-live real Search functional acceptance
```

A Search production-byte change creates a new combined candidate; the previous Phase-1 `e13a…` full-gate result remains historical evidence for those bytes and is not a PASS for the new combined candidate.