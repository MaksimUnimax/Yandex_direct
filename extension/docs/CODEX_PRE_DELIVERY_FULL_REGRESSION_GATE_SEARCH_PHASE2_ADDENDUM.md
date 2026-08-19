# CODEX PRE-DELIVERY FULL REGRESSION GATE — PHASE 2 SEARCH ADDENDUM

Status: **MANDATORY WHEN SEARCH IS PRESENT/ENABLED**  
Updated: 2026-08-19

This addendum is part of the living pre-delivery gate for every candidate containing the Phase-2 Search adapter. It supplements:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
```

Codex remains QA executor only. ChatGPT owns product/test/gate design and fixes.

Controlled gate rule remains:

```text
real Yandex requests = 0
real credentials = 0
```

Use controlled network stubs/fault injection only.

## S-00 — Phase authority

Require live authority to show:

```text
Phase 1 Wordstat = LIVE PASS historical baseline
Phase 2 Search = enabled in current candidate
SEARCH_API_V1 = registered
first slice = synchronous text WebSearch only
```

Read:

```text
extension/docs/PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
```

Any candidate exposing deferred/image/generative Search without a governed contract is FAIL_PRODUCT/coverage FAIL.

## S-01 — Search service registry isolation

Verify:

- `SEARCH_API_V1` maps only to service `search`;
- `WORDSTAT_API_V1` continues to map only to `wordstat`;
- unknown future prefixes cause zero provider requests;
- Search cannot execute in a Wordstat RUN;
- Wordstat cannot execute in a Search RUN;
- one RUN remains one immutable service.

## S-02 — SEARCH_API_V1 parser/defaults

Test canonical command parsing and defaults for:

```text
method = search
queryText required
searchType
region
page
groupsOnPage
familyMode
fixTypoMode
sortMode
sortOrder
groupMode
docsInGroup
maxPassages
l10n
```

Require deterministic normalization.

Boundary tests must include:

```text
queryText empty → reject
queryText 400 chars → accept when otherwise valid
queryText >400 chars → reject
40 words → accept
>40 words → reject
page <0 / noninteger → reject
groupsOnPage outside 1..100 → reject
docsInGroup outside 1..3 → reject
maxPassages outside 1..5 → reject
unknown enum → reject
```

All parser/validation failures are pre-network:

```text
request_executed:false
provider requests:0
automatic_retry:false
```

## S-03 — Exact provider request

For an accepted canonical Search command require exactly one request to:

```text
POST https://searchapi.api.cloud.yandex.net/v2/web/search
```

Request body must map normalized fields into current REST structure:

```text
query
sortSpec
groupSpec
maxPassages
region
l10n
folderId
responseFormat = FORMAT_XML
```

Assistant text cannot choose another host/path/method or arbitrary headers.

`folderId` comes from operator/local settings, not command text.

Authorization is injected only from trusted local credentials and never appears in result/error/debug evidence.

## S-04 — Search credential capability

Controlled cases:

```text
MISSING
INVALID_OR_EXPIRED
NO_ACCESS
PRESENT
```

Pre-network missing/policy capability must not mutate working Wordstat credential state.

No API key/IAM token/Authorization content may enter page DOM, ChatGPT report, diagnostics, package evidence or GitHub-facing result.

## S-05 — Search cost/request policy

Use governed tariff snapshot from the Phase-2 requirement authority.

Verify:

- Search has explicit allowed-method/operator permission;
- request ceiling blocks before fetch;
- RUB ceiling blocks before fetch;
- accepted paid initiation reserves budget before provider call;
- standalone Manual semantics remain governed;
- Manual on PAUSED Search RUN uses the same RUN budget;
- assistant command cannot raise policy limits;
- unknown outcome accounting is conservative and cannot enable duplicate initiation.

If no tariff-window implementation exists, controlled expectations must use the governed conservative higher synchronous reservation.

## S-06 — Search response Base64/XML decode

Stub a valid Yandex REST JSON response containing Base64 XML.

Require:

```text
HTTP 2xx
rawData decoded as UTF-8 XML
SEARCH_RESULT_V1 generated
response_format = FORMAT_XML
request_executed:true
automatic_retry:false
```

Invalid Base64/malformed provider envelope must produce controlled error evidence without a second provider initiation.

## S-07 — XML normalization

Mandatory parser fixtures:

- one organic document;
- multiple documents preserving provider order/rank;
- missing optional title;
- missing snippet/passages;
- missing modtime/domain where possible;
- XML entities;
- nested/highlight markup inside title/passages;
- multiple passages combined deterministically;
- unexpected ignorable tags;
- empty/no-results response;
- provider field-layout variation that remains within governed tolerant parser assumptions.

Normalized target per document:

```text
rank
url
domain|null
title|null
snippet|null
modtime|null
```

Do not fabricate absent fields.

A missing optional field alone must not fail the full result.

## S-08 — SEARCH_RESULT_V1 truthfulness

Verify common fields:

```text
bridge
version
service = search
operation = search
request_id
run_id
status
reason
cost_estimate
policy
command
http_status
elapsed_ms
result
request_executed
automatic_retry
```

No runtime `job_id` dependency.

Result count and rank ordering must match normalized fixture evidence.

## S-09 — HTTP/error/no-retry contours

Controlled network cases:

```text
2xx valid response
400
401/403
429
500
network reject before response
timeout/connection loss after initiation boundary
```

Require:

- one accepted command causes at most one provider initiation;
- received HTTP error produces ERROR evidence and no hidden replay;
- known pre-network rejection stays `request_executed:false`;
- uncertain post-initiation outcome is `request_executed:"UNKNOWN"` where applicable;
- `automatic_retry:false` always on uncertain irreversible outcome;
- identical fingerprint remains fenced against blind retry.

## S-10 — Manual Search path

Through actual controlled content→worker flow:

```text
eligible Search block
→ external Яндекс action click
→ one Manual admission
→ Search parser/policy
→ one stub provider request
→ SEARCH_RESULT_V1
→ existing worker-owned outbox
→ Send at most once
→ ready/Microphone completion
→ Manual lock release
```

Native Copy must produce zero Search admission.

A later distinct Search Manual action must be admitted normally.

Search must not create a service-specific parallel composer/delivery FSM.

## S-11 — Autorun Search path

With active service `search`:

- exactly one Search RUN;
- WAITING_COMMAND lifecycle;
- Search command pickup;
- one controlled provider initiation;
- result/error delivery exactly once;
- counters/cost update;
- recoverable continuation when safe;
- Pause/Resume/Finish;
- worker reload/recovery safety;
- Wordstat markers cannot execute inside Search RUN.

## S-12 — Common-core regression preservation

The new Search product must not regress accepted Phase-1 core behavior.

Complete candidate gate still includes all existing Wordstat/core PD assertions:

```text
Manual ON transaction ordering
external Yandex action/native Copy independence
owner-tab/conversation binding
composer occupied preservation
committed recovery watch-only
Send at most once
always-on YMB_ERROR_V1
Debug redaction
Export/Import
Wordstat getTop/getDynamics/getRegionsDistribution/getRegionsTree
```

Production-byte change means old `e13a…` full-gate PASS is not transferable to the new combined candidate.

## S-13 — Popup/operator service controls

Browser/runtime verify Search is exposed only according to Phase-2 product contract:

- Search can be selected as active service when no conflicting active RUN prevents it;
- Search Manual/Autorun policy persists;
- Search request/RUB ceilings persist;
- Wordstat settings remain intact;
- service selection cannot mutate credentials unexpectedly;
- popup reopen reflects worker truth.

## S-14 — Security/provider containment

Require explicit Search provider allowlist only:

```text
https://searchapi.api.cloud.yandex.net/v2/web/search
```

First slice must not initiate:

```text
/v2/web/searchAsync
Operation polling
ImageSearch
GenSearch
yandex.ru browser scraping
arbitrary assistant URL
```

Real Yandex traffic count remains zero in controlled gate.

## S-15 — Phase locks after Search enablement

For a candidate with Search enabled, the old generic PD-16 Search lock is superseded only for the governed synchronous text Search surface.

Still require zero provider execution for:

```text
Webmaster
Metrika
Direct
Search deferred
Search image
Search generative
```

Recognizing strings/markers for those surfaces must not activate them.

## S-16 — Source/package parity

Search modules/tests/manifest/import order must be present identically in source and fresh exact package.

Run the complete source and packaged suites including all Search tests.

No Search test may exist only outside the handed-off package when runtime code depends on corresponding product module changes.

## S-17 — Final Search evidence

The complete Codex report must add a Search subsection:

```text
search_phase2:
  protocol_registry:
  parser_validation:
  provider_request_exactly_once:
  credential_policy:
  cost_guard:
  base64_xml_decode:
  xml_normalization:
  manual_path:
  autorun_path:
  wordstat_search_isolation:
  http_unknown_no_retry:
  future_search_modes_locked:
  real_yandex_requests:
  verdict:
```

PASS requires every S-00..S-17 mandatory assertion plus the existing PD-00..PD-17 matrix to pass against the same exact frozen candidate.

## Final addendum verdict rule

```text
Search candidate handoff forbidden if any S-section FAIL/NOT_RUN
real Yandex requests during controlled gate must equal 0
production/tests must not be modified by Codex
```

After complete controlled PASS, owner-live Search acceptance is minimal: one useful real paid synchronous Search request after a fresh official tariff check, no blind retry, and functional result validation.