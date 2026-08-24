# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH / STAGE 4 ACTIVE — EXACT CANDIDATE FROZEN / CODEX FULL GATE PENDING**  
Updated: 2026-08-24

Always fetch live `main` HEAD before any transition or control write.

## Current owner instruction

The owner requires focused development and a single governed Stage-4 closure:

- ChatGPT owns product/test/packaging changes;
- do not reopen Stage 3 to search hypothetical adjacent edge cases after its exit criteria passed;
- the complete broad regression campaign belongs to the exact frozen candidate, not to every intermediate edit;
- Codex is QA executor for the full pre-delivery gate and must not design/patch product fixes during that campaign;
- zero real Yandex requests during controlled QA;
- owner-live paid Search acceptance starts only after exact Codex PASS and a fresh pricing check;
- no blind retry after an ambiguous or executed provider request.

## Authoritative transition snapshot

```text
LIVE_MAIN_HEAD = 21a2c351437df2cba0dc04003a788c352e6732c0
PRODUCT_BRANCH = candidate/phase2-search-reconstruction-2026-08-23
PR = #5 Phase 2 Search reconstruction candidate
STAGE3_PRODUCT_HEAD = 75d18291224069a6ae67c110498481ec7320d3c0
STAGE3_WORKER_BLOB = 87b90dcb0a1ecca8afc5587d8ab7f6ddfd2c241a
STAGE4_FROZEN_SOURCE_COMMIT = 1869d17f3cb64417a07088de18dafa5687c83840
HANDOFF_ARTIFACT_SHA256 = 0f0b035c6bc04da841d549182c3dcea6e7cf10074eddebafdf1c3a4c21c98411
HANDOFF_ARTIFACT_BYTES = 170726
HANDOFF_FILES = 65
HANDOFF_ZIP_ENTRIES = 68
CODEX_FULL_GATE = PENDING
OWNER_LIVE_SEARCH = BLOCKED UNTIL CODEX PASS
```

Later branch commits may update CI/docs/evidence only. They do **not** redefine the frozen candidate. The frozen package builder and every Stage-4 QA handoff are pinned to `1869d17...`.

## Exact frozen Stage-4 candidate

```text
filename:
yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip

root:
yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate/

SHA-256:
0f0b035c6bc04da841d549182c3dcea6e7cf10074eddebafdf1c3a4c21c98411

bytes: 170726
files: 65
ZIP entries: 68
ZIP integrity: PASS
source commit: 1869d17f3cb64417a07088de18dafa5687c83840
```

Package payload follows the established Phase-2 layout:

```text
all extension/src/** files
+ root-level extension/tests/*.test.mjs
```

Repository docs, historical evidence trees, `.github/**`, nested QA transport inputs and other non-package files are excluded from the ZIP payload.

## Full target manifest

The freeze generated `EXACT_CANDIDATE_MANIFEST_2026-08-24.json` containing all 65 package file paths with exact byte counts and SHA-256 hashes.

```text
manifest bytes: 11421
manifest SHA-256: 1acda380ef8fee4aca255014cdacf48a50059037113ff121bd86c738e4fceea9
format: YMB_PHASE2_EXACT_CANDIDATE_V1
source commit: 1869d17f3cb64417a07088de18dafa5687c83840
```

Durable freeze checkpoint:

```text
extension/tests/PHASE_2_STAGE_4_FROZEN_CANDIDATE_CHECKPOINT_2026-08-24.md
```

## Freeze / transport proof

Dedicated read-only Stage-4 workflow:

```text
workflow: phase2-stage4-freeze
run: 32705402373
job: 97365293002
conclusion: SUCCESS
permission: contents: read
```

The exact source commit was checked out and the package was independently built twice. Both builds returned exactly:

```text
SHA-256 0f0b035c6bc04da841d549182c3dcea6e7cf10074eddebafdf1c3a4c21c98411
bytes 170726
files 65
entries 68
ZIP PASS
SOURCE_PACKAGE_IDENTITY_PASS
```

Byte-for-byte `cmp` between the two independently generated ZIPs passed.

Published Actions transport:

```text
artifact name: phase2-stage4-frozen-candidate-1869d17
artifact ID: 9512033721
wrapper bytes: 182577
wrapper SHA-256: b5ba907514c2a417c537fcce82ddfe5ca6605df6fb71ea309942700605fb4e33
```

A fresh consumer downloaded artifact ID `9512033721` and independently verified:

```text
wrapper SHA-256 = b5ba907514c2a417c537fcce82ddfe5ca6605df6fb71ea309942700605fb4e33
inner ZIP SHA-256 = 0f0b035c6bc04da841d549182c3dcea6e7cf10074eddebafdf1c3a4c21c98411
inner bytes = 170726
files = 65
entries = 68
ZIP integrity = PASS
all 65 file path/byte/SHA-256 rows match downloaded manifest = PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
```

Therefore the Stage-4 transport is consumer-conformance proven; upload/API success alone is not being treated as artifact proof.

## Current focused sanity state

Combined read-only PR workflow after CI-only synchronization:

```text
workflow: phase2-focused-development
run: 32705402326
focused job: 97365292925
freeze job: 97365292591
focused Stage-3 regression set: 77/77 PASS
fail: 0
service_worker.js syntax: PASS
popup.js syntax: PASS
freeze job: SUCCESS
```

This is **not** the complete Codex pre-delivery gate and does not replace it.

## Accepted Phase 1 baseline

Phase 1 Wordstat remains **LIVE PASS / CLOSED**.

```text
accepted artifact SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes: 209505
files: 45
ZIP entries: 48
version: 0.1.1
historical complete full gate: PASS
owner-live Wordstat: PASS for getTop, getDynamics, getRegionsDistribution, getRegionsTree
```

Those are historical accepted Phase-1 bytes; the combined Wordstat+Search frozen candidate above requires its own complete Stage-4 gate.

## Phase 2 Search boundary

```text
protocol: SEARCH_API_V1
service: search
method: search
endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
mode: synchronous text web search only
response format: FORMAT_XML
normalized result: SEARCH_RESULT_V1
```

Out of scope remains async polling Search, image Search, generative Search, HTML SERP normalization, yandex.ru scraping, Webmaster, Metrika and Direct implementation.

## Stage status

```text
STAGE 1 — exact base + Search foundation = PASS / COMPLETED
STAGE 2 — worker/provider/credential/policy execution = PASS / COMPLETED
STAGE 3 — Manual/Autorun/operator/delivery integration = PASS / COMPLETED
STAGE 4 — exact frozen candidate = PASS
STAGE 4 — transport consumer-conformance = PASS
STAGE 4 — complete Codex pre-delivery full gate = PENDING
STAGE 4 — owner-live Search = BLOCKED UNTIL CODEX PASS
```

## Stage 3 preserved invariants

The frozen candidate preserves the common unified runtime rather than a parallel Search-specific implementation, including:

- Project/Work nested ChatGPT conversation identity;
- Search Manual via Bridge-owned external `Яндекс` action;
- Search Autorun through the common RUN lifecycle;
- immutable service per RUN and Wordstat/Search isolation;
- owner-tab/live-conversation fences;
- service-context and Manual-mode runtime locks;
- single-flight/outbox admission;
- committed Send at most once and watch-only recovery;
- durable `YMB_ERROR_V1` delivery;
- UNKNOWN/no-blind-retry semantics;
- Manual abandoned `REQUESTING` restart recovery;
- Autorun abandoned `REQUESTING` restart recovery;
- Autorun `STARTING` restart recovery that restores one missing `autorun_start` without provider initiation and does not duplicate an existing outbox;
- Search request/cost/credential policy;
- settings export/import runtime safety and diagnostic redaction.

Final Stage-3 production commit:

```text
75d18291224069a6ae67c110498481ec7320d3c0
fix: recover missing Autorun start delivery
```

## Current authorized action

```text
AUTHORIZED_NEXT_STAGE = CODEX_COMPLETE_PRE_DELIVERY_FULL_GATE
```

Use:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
extension/tests/PHASE_2_STAGE_4_FROZEN_CANDIDATE_CHECKPOINT_2026-08-24.md
```

Codex must consume the exact frozen artifact identified above and execute the complete enabled PD-00…PD-17 matrix, including required browser/CfT/Puppeteer surfaces, source suite, packaged suite, syntax/JSON, source-package identity and zero-real-Yandex assertions. No enabled section may silently remain `NOT_RUN` in a PASS verdict.

If the complete Codex campaign finds a product defect, classify it `FAIL_PRODUCT` and return it to ChatGPT. Any production-byte fix creates a new candidate and invalidates this frozen identity. Transport/harness/process defects must not mutate frozen production bytes.
