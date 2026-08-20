# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT / PHASE 2 SEARCH DEVELOPMENT ACTIVE**  
Updated: 2026-08-20

Always fetch live `main` HEAD before any control-plane write.

## Current owner instruction

The owner explicitly corrected the prior recovery loop and authorized continued development on 2026-08-20:

- do not keep sending artifact-recovery work to Codex;
- ChatGPT is the developer and must reconstruct/reimplement the lost product changes itself;
- the exact final Stage-3 patch is lost and is not to be falsely represented as recovered;
- restore the lost Search integration from surviving requirements, evidence, earlier exact modules/patches, and tests;
- reintroduce changes under the established testing policy: focused development tests while code is changing, then one complete mandatory pre-delivery regression gate after the exact candidate is finished and frozen.

This owner instruction supersedes the earlier `exact Stage-2 recovery only / Codex recovery prompt` pointer that was introduced during the mistaken recovery loop.

## Repository

```text
repo: MaksimUnimax/Yandex_direct
control branch: main
active recovery/development branch: dev/phase2-recovery-work-2026-08-20
```

## Accepted Phase 1 baseline

Phase 1 Wordstat remains LIVE PASS / CLOSED.

```text
accepted artifact SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes: 209505
files: 45
ZIP entries: 48
version: 0.1.1
latest complete full gate: PD-00..PD-17 PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
real Yandex requests during controlled gate: 0
owner-live Wordstat: PASS for all four supported operations
```

## Phase 2 Search — surviving accepted work

First Search slice remains:

```text
protocol: SEARCH_API_V1
service: search
method: search
endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
response: FORMAT_XML
result: SEARCH_RESULT_V1
scope: synchronous text web search only
```

Provider-independent Search foundation was completed and tested.
Worker/provider/credential/policy Search execution was completed and tested.
Historical accepted evidence records focused Search worker tests 10/10 PASS, full suite 377/377 PASS, syntax 46/46 PASS, JSON 2/2 PASS, and zero real Yandex requests.

The final lost integration work had also reached functional/test PASS before its exact bytes were lost. Historical evidence records:

```text
focused integration: 38/38 PASS
popup runtime: 13/13 PASS
full source suite: 382/382 PASS
syntax: 46/46 PASS
JSON: 2/2 PASS
real Yandex requests: 0
```

Known final production hashes from that lost working tree are historical evidence only:

```text
content_script.js a789b7ec586632d2dde287b59ccaee11d8de010ae9a474cdcd9a68a0b252e688
manifest.json ac48a2399f7f77d1382958231038a999e8c7dfd37e4cdc60a9b9241a62c0c96f
popup.html 778c5d2068a2cccd7648f4cef16f649870878e114baa43e4eabf43a628b34cc0
popup.js 03b13ad6af722ea9cc92d26e7e299519fbd500e43d71f2c9c225a903bfe6c274
service_worker.js 87a4022b7273618ac4df343cff50f7fd155d03c26dc17b68169a569dd0a43c3b
```

The exact final patch itself is lost. Recorded identity:

```text
raw patch SHA-256: d2338b7d1f233e3622fdc1da49038df0e96afe0785b2addfbab4f961fda9cee6
raw bytes: 81690
gzip SHA-256: 5c32e7a16f0102cc0c54cb59fb15a1b815795462822a8338692adef2d1487ec5
base64 SHA-256: edc73c040de67310a03c284728d45589b7a901721ff7b4b4df52d5f363b113de
```

`STAGE3_EXACT_RECOVERY_RESULT_V1` proved that these exact final bytes were not found in the searched recovery locations. That result is preserved as evidence; it does not establish a product defect.

A separate surviving combined Search patch with raw SHA-256 `91751cd720dba23282be69d75c921331dab83bbe6076bffd464519297a80c0ca` / 142186 bytes is useful development evidence, but it is **not** the lost final patch above and must not be represented as such.

## Testing policy for the restoration

The mandatory pre-delivery regression gate was adopted on 2026-08-18. Its intended two-mode rule remains authoritative:

```text
while product code is changing:
  run focused tests for changed behavior + directly affected dependencies + syntax/static checks

when the complete working candidate is finished:
  freeze the exact candidate and handoff artifact
  run one complete mandatory regression campaign against that exact candidate
  any mandatory FAIL blocks handoff
  any later production-byte change invalidates that candidate's product gate
```

Search-specific full-gate coverage is governed by:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
```

No real Yandex requests or real credentials are used during controlled development/gate testing.

## Current development objective

Reimplement the lost Search user/runtime integration without inventing new product scope:

- Search Manual path through the shared external `Яндекс` action;
- service mismatch rejection before claim/provider execution;
- Search Autorun through the existing RUN lifecycle;
- immutable service / Wordstat↔Search isolation;
- active-service propagation worker→content;
- popup service selector and separate Search policy/credentials;
- service-aware start prompt;
- Search settings/credentials Export/Import separation;
- reuse of owner-tab binding, conversation binding, single-flight admission, durable outbox, composer protection, Send-at-most-once and no-blind-retry behavior.

The current implementation must be committed as normal source/test files so it cannot be lost as another local-only candidate.

## Current pointer

```text
PRODUCT_SOURCE = development reconstruction/reimplementation in progress on dev/phase2-recovery-work-2026-08-20
HANDOFF_ARTIFACT = NONE
LATEST_FULL_GATE = Phase-1 e13a PASS only; no Phase-2 combined full-gate PASS yet
OWNER_LIVE = Phase 1 PASS; Phase 2 Search PENDING
CURRENT_WORK = restore lost Search integration with focused tests
NEXT_RELEASE_ACTION = only after complete restoration + development verification: freeze exact candidate and run complete mandatory pre-delivery gate
REAL_YANDEX_REQUESTS_AUTHORIZED_NOW = NO
```
