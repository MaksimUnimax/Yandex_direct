# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH RECONSTRUCTION CANDIDATE / FOCUSED DEVELOPMENT MODE**  
Updated: 2026-08-23

Always fetch live `main` HEAD before any transition or control write.

## Current owner instruction

The owner explicitly corrected the prior QA/recovery workflow and restored focused development mode:

- ChatGPT is the developer and reconstructs/reimplements product changes itself;
- Codex is used only for targeted QA/measurement when needed;
- do not represent the lost final historical patch as recovered;
- do not keep splitting development into endless full-suite/full-gate campaigns;
- while production code is changing, test **only the changed behavior and directly affected dependencies**, plus the syntax/static checks required by that changed surface;
- the historical `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` remains historical/pre-delivery QA documentation, but it is **not an active requirement for current Phase-2 development or every candidate change**;
- do not perform real Yandex requests during development unless the owner explicitly starts an owner-live acceptance step.

This owner instruction supersedes any later/current pointer that treated the complete PD-00…PD-17 gate, package freeze or whole-suite regression as the mandatory next step before continuing development.

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
historical complete full gate: PD-00..PD-17 PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
real Yandex requests during controlled gate: 0
owner-live Wordstat: PASS for all four supported operations
```

## Phase 2 Search protocol

```text
protocol: SEARCH_API_V1
service: search
method: search
endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
request format: synchronous text web search
provider response requested: FORMAT_XML
normalized result: SEARCH_RESULT_V1
scope: synchronous text web search only
```

Out of scope remains asynchronous/polling Search, image Search, generative Search, HTML normalization and yandex.ru scraping.

## Historical lost final integration

The old final integrated Search tree had historical PASS evidence:

```text
focused integration: 38/38 PASS
full source suite: 382/382 PASS
syntax: 46/46 PASS
JSON: 2/2 PASS
real Yandex requests: 0
```

Those results are historical evidence only. The exact old final source bytes are lost and are not the current candidate.

Recorded lost patch identity:

```text
raw patch SHA-256: d2338b7d1f233e3622fdc1da49038df0e96afe0785b2addfbab4f961fda9cee6
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

## Project/Work popup repair after reconstructed candidate failed in owner use

The first reconstructed candidate incorrectly recognized only direct ChatGPT `/c/<uuid>` routes. In current ChatGPT Project/Work URLs the conversation is nested under `/g/.../c/<uuid>`, so conversation identity remained unavailable and the popup/settings controls were effectively unusable in the owner's actual route.

Production repair:

```text
8483b52acee7981f2ef50eaa0d62ec4c655006cf
fix: recognize ChatGPT project conversation routes
```

The repair changes `extension/src/shared/conversation_identity.js` so a valid `/c/<uuid>` conversation segment can be recognized inside an allowed ChatGPT pathname while foreign origins and roots without a concrete conversation remain fail-closed.

Focused regressions added for this repair:

```text
fbb1710bc907c00b210f145e5e5edd3871364b6b
test: cover ChatGPT project conversation identity

dc0c39f5609a10e85de809677574efa698678df8
test: cover popup initialization on ChatGPT project route
```

This Project/Work popup compatibility is now a preserved product invariant for all later changes.

## Current development verification policy

Active rule from the owner:

```text
change one product surface
→ add/update focused tests for exactly that behavior
→ run those focused tests
→ run only directly affected dependency/regression checks
→ run syntax/static checks required by the changed files
→ continue development when green
```

Do not run the full historical PD-00…PD-17 gate, deterministic package-freeze campaign, whole source regression suite or packaged whole-suite regression merely because one development change was made.

If a future owner handoff explicitly requires a broad release audit, that is a separate owner-directed activity and not an automatic development blocker.

## Current development objective

Continue Phase 2 from the repaired Project/Work-compatible candidate. Preserve existing Wordstat behavior and the Project/Work popup repair while finishing/validating Search functionality incrementally.

For every product edit:

1. identify the smallest changed runtime surface;
2. make the production change without unrelated refactors;
3. add/update focused regression coverage for that surface;
4. run only that coverage plus directly affected dependencies and required syntax/static checks;
5. record the exact change and result;
6. continue to the next Phase-2 item.

No owner-live Search request has been executed yet. A real Search request is a separate explicit owner-live acceptance step and must not be initiated as a side effect of development QA.
