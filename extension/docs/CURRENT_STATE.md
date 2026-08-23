# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH RECONSTRUCTION CANDIDATE PREPARED / FULL QA PENDING**  
Updated: 2026-08-23

Always fetch live `main` HEAD before any transition or control write.

## Current owner instruction

The owner explicitly corrected the prior recovery loop:

- ChatGPT is the developer and reconstructs/reimplements lost product changes itself;
- Codex is only independent QA/measurement after the candidate is complete;
- do not represent the lost final historical patch as recovered;
- do not keep splitting development into endless micro-tests;
- use focused development checks while code changes, then freeze one candidate and run the complete pre-delivery gate on that exact candidate;
- do not perform real Yandex requests during development or controlled QA.

## Repository pointers

```text
repo: MaksimUnimax/Yandex_direct
control branch: main
historical recovery branch: dev/phase2-recovery-work-2026-08-20
clean candidate branch: candidate/phase2-search-reconstruction-2026-08-23
candidate source snapshot commit: 07accfa96aeb1b38d4e882235163bdc136d16a01
```

The historical recovery PR is not a delivery PR and must not be merged blindly. The clean candidate was created directly on top of live `main` from the reconstructed source/test tree, without the temporary recovery workflow or the five old `patch.gz.b64` transport chunks.

## Accepted Phase 1 baseline

Phase 1 Wordstat remains LIVE PASS / CLOSED.

```text
accepted artifact SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes: 209505
files: 45
ZIP entries: 48
version: 0.1.1
latest complete historical full gate: PD-00..PD-17 PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
real Yandex requests during controlled gate: 0
owner-live Wordstat: PASS for all four supported operations
```

## Phase 2 Search protocol

```text
protocol: SEARCH_API_V1
service: search
method: search
endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
response: FORMAT_XML
result: SEARCH_RESULT_V1
scope: synchronous text web search only
```

Out of scope remains asynchronous/polling Search, image Search, generative Search, HTML normalization and yandex.ru scraping.

## Historical lost final integration

The old final integrated Search tree had historical PASS evidence:

```text
focused integration: 38/38 PASS
popup runtime: 13/13 PASS
full source suite: 382/382 PASS
syntax: 46/46 PASS
JSON: 2/2 PASS
real Yandex requests: 0
```

Those results are historical evidence only. The exact old final source bytes are lost and are not the current candidate.

Recorded lost patch identity:

```text
raw patch SHA-256: d2338b7d1f233e3622fdc1da49038df0e96afe0785b2addfbab4f961fda9cee6
raw bytes: 81690
gzip SHA-256: 5c32e7a16f0102cc0c54cb59fb15a1b815795462822a8338692adef2d1487ec5
base64 SHA-256: edc73c040de67310a03c284728d45589b7a901721ff7b4b4df52d5f363b113de
```

The surviving combined patch with raw SHA-256 `91751cd720dba23282be69d75c921331dab83bbe6076bffd464519297a80c0ca` is useful historical source material but is **not** that lost final patch.

## Reconstructed candidate functionality

The current candidate reconstructs the required lost product behavior with new source bytes:

- shared Wordstat + synchronous Search service registry;
- Search Manual execution through the Bridge-owned external `Яндекс` action;
- full-block capture and serial execution of supported commands;
- wrong-service rejection before durable claim/provider execution;
- Manual single-flight and provider-outcome UNKNOWN no-retry fence;
- Search Autorun through the existing RUN lifecycle;
- immutable service and Wordstat/Search isolation;
- owner-tab and conversation binding checks before execution/delivery;
- separate Wordstat/Search policy, request/cost guards and local credentials;
- service-aware Autorun start prompt;
- durable result/error queues and correct-chat delivery;
- occupied-composer protection;
- Send commit before click and watch-only committed recovery, preventing double Send;
- manual-send behavior when auto-send is disabled;
- content transport retry only before worker acceptance;
- durable `YMB_ERROR_V1` delivery with redacted diagnostics;
- settings export/import SHA-256 validation;
- rollback backup before settings import;
- compatible settings merge that preserves active Autorun/Manual runtime state;
- legacy report-prefix and Send/Copy profile compatibility;
- popup confirmation for secret export/import and 5 MiB import limit;
- host permissions limited to ChatGPT and the official Yandex Search API host.

## Current development verification

The current source was checked after reconstruction with the repository candidate gate using the actual PR merge with live `main`:

```text
current Node regression: 156/156 PASS
fail: 0
syntax checks: PASS
manifest/package JSON: PASS
candidate package-reference checks: PASS
real Yandex requests: 0
```

This 156-test reconstructed suite is broader than the earlier focused recovery suite, but it must **not** be described as equivalent to the lost historical 382/382 or the accepted Phase-1 435-check full-system campaign.

The candidate gate also records SHA-256 for every file under `extension/src`. These hashes identify the reconstructed source bytes and intentionally differ from the lost historical final hashes.

## Testing / delivery rule

While production source bytes change, focused/current regression is used. Once the clean candidate is frozen, run the complete mandatory pre-delivery QA against that exact candidate. Any later production-byte change invalidates that candidate QA and requires a new freeze.

Search-specific full-gate requirements remain governed by:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
```

Codex may be used only as an independent executor/measurement layer for that final QA; it does not design or fix the product.

## Current pointer

```text
PRODUCT_SOURCE = reconstructed source on candidate/phase2-search-reconstruction-2026-08-23
CANDIDATE_SOURCE_SNAPSHOT = 07accfa96aeb1b38d4e882235163bdc136d16a01
HANDOFF_ARTIFACT = NONE
CURRENT_RECONSTRUCTED_GATE = 156/156 PASS + syntax/JSON PASS
LATEST_HISTORICAL_FULL_GATE = Phase-1 e13a PASS; historical lost Phase-2 382/382 evidence retained
OWNER_LIVE = Phase 1 PASS; Phase 2 Search PENDING
NEXT_RELEASE_ACTION = run complete mandatory QA against the clean frozen candidate, then prepare owner-live Search acceptance only after fresh official pricing verification
REAL_YANDEX_REQUESTS_AUTHORIZED_NOW = NO
```
