# PHASE 2 — YANDEX SEARCH / SERP REQUIREMENTS AND IMPLEMENTATION PLAN

Status: **CURRENT PHASE-2 REQUIREMENT AUTHORITY / IMPLEMENTATION ACTIVE**  
Updated: 2026-08-20

This document records the Phase-2 service contract reconstructed from current project authority and current official Yandex Search API documentation. It must be read before Search product changes.

## 1. Phase boundary

Phase 1 Wordstat is LIVE PASS and closed.

Phase 2 adds the second adapter to the same extension:

```text
Yandex Marketing Bridge
├─ Wordstat [accepted]
└─ Search   [Phase 2]
```

Runtime remains:

```text
ChatGPT conversation ↔ Yandex Marketing Bridge ↔ official Yandex Search API
```

GitHub/job concepts remain outside extension runtime.

The Search protocol prefix is already reserved by the product specification:

```text
SEARCH_API_V1
```

Result signature:

```text
SEARCH_RESULT_V1
```

## 2. Current official Yandex Search API facts

Primary official documentation checked 2026-08-19:

```text
https://aistudio.yandex.ru/docs/ru/search-api/concepts/index.html
https://aistudio.yandex.ru/docs/ru/search-api/concepts/web-search.html
https://aistudio.yandex.ru/docs/ru/search-api/api-ref/WebSearch/search.html
https://aistudio.yandex.ru/docs/ru/search-api/api-ref/WebSearchAsync/search.html
https://aistudio.yandex.ru/docs/ru/search-api/api-ref/authentication.html
https://aistudio.yandex.ru/docs/ru/search-api/concepts/limits.html
https://aistudio.yandex.ru/docs/ru/search-api/pricing.html
https://aistudio.yandex.ru/docs/ru/search-api/operations/web-search-sync.html
```

Current text-search REST service:

```text
POST https://searchapi.api.cloud.yandex.net/v2/web/search
```

Deferred endpoint also exists:

```text
POST https://searchapi.api.cloud.yandex.net/v2/web/searchAsync
```

Text search is available in synchronous and deferred modes and can return XML or HTML. The REST response contains Base64 `rawData` holding the selected XML/HTML representation.

Current authentication supports:

```text
Authorization: Api-Key <API key>
```

or:

```text
Authorization: Bearer <IAM token>
```

The documented access role is:

```text
search-api.webSearch.user
```

AI Studio API-key examples use scope/access corresponding to:

```text
yc.search-api.execute
```

`folderId` identifies the Yandex Cloud folder where required.

## 3. Current official pricing relevant to Phase 2

Official RUB tariff checked 2026-08-19:

```text
daytime synchronous: 488 RUB / 1000 requests = 0.488 RUB/request
night synchronous:    366 RUB / 1000 requests = 0.366 RUB/request

daytime deferred:     30.5 RUB / 1000 requests = 0.0305 RUB/request
night deferred:       25.41 RUB / 1000 requests = 0.02541 RUB/request
```

Night window documented by Yandex:

```text
00:00:00–07:59:59 UTC+3
```

Requests ending in an internal server error or authentication error are documented as non-billable; Bridge must still truthfully distinguish request initiation from billing estimate and must not invent a guaranteed charge outcome from HTTP status alone.

Phase-2 policy must retain a tariff snapshot/source and must be conservative. If runtime tariff-window logic is not implemented in the first slice, the safe default cost reservation for a synchronous request is the higher daytime value:

```text
0.488 RUB per accepted sync initiation
```

ChatGPT must freshly verify official pricing before any owner-live paid Search command.

## 4. Current official quotas and hard limits

Current documented Search quotas/limits include:

```text
synchronous requests/hour: 10000
synchronous requests/second: 10

deferred requests/hour: 35000
deferred requests/second: 10
result polling requests/second: 10

maximum returned results per search query: 250
maximum query length: 400 characters
maximum query words: 40

deferred minimum processing time: 5 minutes
deferred result retention: 12 hours
```

Product validation must enforce deterministic local limits where possible before provider initiation. Provider quotas remain provider authority.

## 5. Phase-2 first implementation slice

Phase 2 will be incremental.

### 5.1 First slice — synchronous text SERP only

The first product slice implements only:

```text
SEARCH_API_V1
method = search
mode = synchronous text web search
endpoint = /v2/web/search
response format = FORMAT_XML
```

Deferred search, image search and generative search are NOT part of the first slice.

Reason:

- synchronous text search is the smallest complete SERP collection path;
- it reuses existing exactly-once Manual/Autorun provider initiation semantics;
- deferred search introduces a separate durable operation/polling lifecycle and should be added only after synchronous Search is accepted;
- image and generative Search are distinct operation/cost classes and must not silently enter the text SERP phase.

### 5.2 Why XML is canonical for the first slice

Use:

```text
responseFormat = FORMAT_XML
```

XML contains the search results proper and supports the detailed SERP controls needed for normalized collection, including grouping/sorting/typo/localization parameters. HTML may include ads, quick answers and other changing presentation elements and is not the canonical first-slice normalized data source.

## 6. SEARCH_API_V1 command contract — first slice

Canonical command shape:

```text
SEARCH_API_V1
{
  "method": "search",
  "queryText": "...",
  "searchType": "SEARCH_TYPE_RU",
  "region": "225",
  "page": 0,
  "groupsOnPage": 10,
  "familyMode": "FAMILY_MODE_MODERATE",
  "fixTypoMode": "FIX_TYPO_MODE_ON",
  "sortMode": "SORT_MODE_BY_RELEVANCE",
  "sortOrder": "SORT_ORDER_DESC",
  "groupMode": "GROUP_MODE_FLAT",
  "docsInGroup": 1,
  "maxPassages": 4,
  "l10n": "LOCALIZATION_RU"
}
```

Required field:

```text
queryText
```

Defaults for omitted fields:

```text
method          = search
searchType      = SEARCH_TYPE_RU
region          = 225 for SEARCH_TYPE_RU
page            = 0
groupsOnPage    = 10
familyMode      = FAMILY_MODE_MODERATE
fixTypoMode     = FIX_TYPO_MODE_ON
sortMode        = SORT_MODE_BY_RELEVANCE
sortOrder       = SORT_ORDER_DESC
groupMode       = GROUP_MODE_FLAT
docsInGroup     = 1
maxPassages     = 4
l10n            = LOCALIZATION_RU
responseFormat  = FORMAT_XML (internal fixed first-slice value)
```

`folderId` and credentials are operator-owned local settings and MUST NOT be required in assistant commands.

Supported `searchType` values from current official REST reference:

```text
SEARCH_TYPE_RU
SEARCH_TYPE_TR
SEARCH_TYPE_COM
SEARCH_TYPE_KK
SEARCH_TYPE_BE
SEARCH_TYPE_UZ
```

First-slice implementation must validate compatibility of region/localization parameters with the selected search type rather than blindly emitting invalid combinations.

## 7. Search validation rules

Before network initiation:

```text
queryText non-empty
queryText <= 400 characters
queryText <= 40 words
page integer >= 0
groupsOnPage integer 1..100 for canonical XML
docsInGroup integer 1..3
maxPassages integer 1..5
known enums only
known service/method only
credential capability present
operator permission allows Search
request/cost budget admits next request
owner tab + conversation binding valid
single-flight/irreversible fences clear
```

Validation/policy/credential rejection:

```text
request_executed = false
provider initiation = 0
automatic_retry = false
```

## 8. Provider request body

First-slice REST body maps normalized command to current API fields:

```text
{
  "query": {
    "searchType": "...",
    "queryText": "...",
    "familyMode": "...",
    "page": "...",
    "fixTypoMode": "..."
  },
  "sortSpec": {
    "sortMode": "...",
    "sortOrder": "..."
  },
  "groupSpec": {
    "groupMode": "...",
    "groupsOnPage": "...",
    "docsInGroup": "..."
  },
  "maxPassages": "...",
  "region": "...",
  "l10n": "...",
  "folderId": "<operator local setting>",
  "responseFormat": "FORMAT_XML"
}
```

The Bridge uses the existing local Yandex Search API credential/folder settings when compatible. It must not duplicate or expose the API key in command/result/debug/GitHub surfaces.

If the stored credential does not have Search access, return controlled `NO_ACCESS`/provider authorization evidence according to the existing credential/error contract; do not mutate or discard working Wordstat credentials.

## 9. Response handling and normalization

Yandex REST returns:

```text
{"rawData":"<Base64 XML bytes>"}
```

Bridge must:

1. validate the HTTP response;
2. decode Base64 to UTF-8 XML;
3. preserve provider truth without fabricating missing fields;
4. normalize available organic SERP documents into a stable Bridge result shape;
5. tolerate optional/missing provider fields because Yandex explicitly documents Search response fields/content as mutable and optional;
6. never treat an optional missing snippet/title/date as a whole-request failure if the result document remains identifiable.

First-slice normalized document target:

```text
{
  "rank": 1,
  "url": "...",
  "domain": "... | null",
  "title": "... | null",
  "snippet": "... | null",
  "modtime": "... | null"
}
```

The implementation may preserve a bounded decoded raw XML field for diagnostics/forward compatibility, but must not dump credential-bearing request headers and must respect composer/result size safety.

Parser tests must cover missing optional tags, XML entities, nested highlight markup, repeated passages and unexpected-but-ignorable tags.

## 10. SEARCH_RESULT_V1 envelope

First-slice common result:

```text
SEARCH_RESULT_V1
{
  "bridge": "yandex-marketing-bridge",
  "version": "...",
  "service": "search",
  "operation": "search",
  "request_id": "...",
  "run_id": null,
  "status": "OK | ERROR | SKIPPED",
  "reason": null,
  "cost_estimate": {...},
  "policy": {...},
  "command": {...},
  "http_status": 200,
  "elapsed_ms": 0,
  "result": {
    "results": [...],
    "result_count": 0,
    "response_format": "FORMAT_XML"
  },
  "request_executed": true,
  "automatic_retry": false
}
```

No `job_id` runtime requirement.

## 11. Cost/policy semantics

Search is paid from the first successful provider initiation class.

Operator controls must include at minimum:

```text
Search Manual allowed
Search Autorun allowed
allowed Search methods
max Search requests per RUN
max estimated Search RUB per RUN
current tariff snapshot/source
```

One accepted Search command = at most one external initiation.

Budget is reserved before provider initiation. Conservative over-count after an uncertain crash is acceptable; under-count that could permit duplicate/over-budget initiation is not.

Manual on a PAUSED Search RUN uses the same RUN budget and cannot bypass it.

## 12. Failure/no-retry semantics

Preserve global Bridge rules:

```text
HTTP 2xx
→ normal result

HTTP 4xx/5xx after one initiation
→ ERROR evidence
→ request_executed = true
→ automatic_retry = false

validation / credentials / policy rejection before fetch
→ request_executed = false
→ zero provider initiation

timeout/network/session loss after initiation may have occurred
→ request_executed = UNKNOWN
→ automatic_retry = false
→ identical blind retry forbidden
```

## 13. Manual and Autorun integration

Search must use the already accepted common core, not fork a second DOM/composer implementation.

Required reuse:

```text
external Yandex action
native Copy independence
real popup Manual state
conversation binding
owner-tab fence
single-flight Manual admission
worker-owned outbox
composer occupied protection
committed Send at most once
ready/Microphone completion
watch-only committed recovery
always-on YMB_ERROR_V1
Debug redaction
Export/Import
```

The core router detects `SEARCH_API_V1` only after the Search service is registered for Phase 2.

One Autorun RUN remains one immutable service. A Wordstat RUN cannot execute Search and a Search RUN cannot execute Wordstat.

## 14. First-slice implementation map

Expected changed/new product surfaces:

```text
extension/src/shared/service_registry.js
  register search / SEARCH_API_V1

new Search protocol module
  parse/normalize/build request
  cost metadata helpers
  SEARCH_RESULT_V1 formatting

new Search XML normalization module
  Base64 UTF-8 decode
  tolerant XML result normalization

worker/core routing
  Search credential/policy/budget/provider execution

popup/operator policy
  expose Search as Phase-2 active service
  Search request/cost limits

manifest/import order if required
```

Do not duplicate common Manual/content delivery logic unless a proven service-specific need exists.

## 15. Mandatory focused development tests

Before any frozen candidate:

```text
SEARCH_API_V1 parse/validation/defaults
all supported enums
query 400-char and 40-word boundaries
invalid page/group/passages boundaries
folder/credential omission from assistant command
build exact /v2/web/search request
Authorization redaction
no request on validation/NO_CREDENTIALS/policy limit
one request exactly on accepted command
HTTP error no retry
UNKNOWN outcome no retry
Base64/XML decode
normalized ranks/order
optional/missing XML fields
XML entities/highlights/passages
Search/Wordstat router separation
one RUN = one service
Manual paused-RUN Search budget
cost reservation before initiation
Search result/error delivery through existing outbox
```

No real Yandex request during development/Codex controlled tests.

## 16. Full-gate additions required before implementation handoff

The living Codex gate must be expanded before a Phase-2 candidate is handed off to cover:

```text
Search protocol and service registry
Search credential capability
Search policy/cost guard
Search sync request exactly-once
Search HTTP/UNKNOWN no-retry behavior
Search XML decode/normalization
Search Manual path
Search Autorun path
Wordstat/Search service isolation
packaged Search behavior
zero real Yandex traffic in controlled gate
```

Production-byte changes invalidate the previous Phase-1 package gate for the new combined candidate; Phase 1 regressions must remain in the complete gate.

## 17. Owner-live Phase-2 policy

After a new combined Wordstat+Search exact candidate passes the complete Codex gate, owner-live should remain minimal and functional.

At least one real synchronous Search request will be paid. Immediately before the executable owner command:

1. freshly check official Yandex Search API pricing;
2. state exact expected per-request cost for the current time/tariff class;
3. use one useful low-volume query;
4. click Yandex once;
5. no blind retry if outcome is ambiguous;
6. verify the returned `SEARCH_RESULT_V1` is usable.

UI-only cases already covered by controlled gate are observed naturally rather than repeated as a separate checklist unless a new live UI defect appears.

## 18. Explicitly out of first slice

Not authorized in the first Search implementation slice:

```text
/v2/web/searchAsync deferred lifecycle
Operation polling/cancel
image search
generative search
HTML SERP normalization
browser scraping of yandex.ru
Direct/Webmaster/Metrika changes
```

These require separate contract/gate expansion after synchronous Search is accepted.

## 19. Requirement-reconstruction verdict

```text
PHASE 1 WORDSTAT = LIVE PASS / CLOSED
PHASE 2 SEARCH REQUIREMENTS = RECONSTRUCTED
PHASE 2 FOUNDATION = IMPLEMENTED ON dev/phase2-search-foundation-2026-08-19
PHASE 2 FOUNDATION LOCAL VERIFICATION = 393/393 PASS; SYNTAX PASS; JSON PASS; REAL YANDEX REQUESTS 0
```

## 20. Four active engineering stages — binding execution plan

The remaining implementation is now governed by:

```text
extension/docs/PHASE_2_SEARCH_ACTIVE_ENGINEERING_STAGES.md
```

The four ordered stages are:

```text
STAGE 1 — Search policy / cost / admission
STAGE 2 — Worker / provider execution integration
STAGE 3 — Operator settings / popup / load wiring
STAGE 4 — Manual Search end-to-end integration / local regression / freeze prep
```

Foundation is already complete and is not one of these remaining four stages.

Execution rule:

```text
ChatGPT continues through the four stages without micro-confirmations.
Unknown browser/DOM/runtime fact → concrete Codex measurement, never guess.
Completed exact candidate → Codex complete pre-delivery gate.
Codex PASS → owner minimal paid real-Yandex Search acceptance.
Owner explicit pause/scope change → stop/adjust.
```

Current authorized next stage:

```text
PHASE_2_STAGE_1_SEARCH_POLICY_COST_ADMISSION
```
