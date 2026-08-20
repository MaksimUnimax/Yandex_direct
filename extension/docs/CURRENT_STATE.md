# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY / PHASE 2 STAGE 3 ACTIVE**  
Updated: 2026-08-20

This file applies immediately in the current conversation and every new/resumed conversation. Always fetch live `main` HEAD before action.

## Repository

```text
repo: MaksimUnimax/Yandex_direct
control branch: main
Phase-2 development branch: dev/phase2-search-foundation-2026-08-19
```

## Mandatory workflow authorities

Before any future Codex handoff, read and execute:

```text
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

Phase-2 engineering is governed by:

```text
extension/docs/PHASE_2_FOUR_STAGE_EXECUTION_CONTROL.md
```

Stage reporting rule:

```text
work continuously inside a stage without micro-step chatter
→ preserve product/test/evidence in GitHub
→ at stage PASS, write durable checkpoint + update CURRENT_STATE
→ send one concise owner report
→ continue automatically unless owner/Codex/real blocker is required
```

Unknown browser/DOM/runtime facts MUST NOT be guessed. Stop at the exact uncertainty and request a concrete Codex measurement.

## Phase 1 accepted authority

```text
artifact SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes: 209505
files: 45
ZIP entries: 48
version: 0.1.1

content_script.js: ddf9ed51c60ab90dcdeb1fcd5a1b955c3dd88dfc53a0ddfd5842d66ebe9a02cc
popup.js: ac87ad973e8b673bf0c235a43b3dc29dfb67865594ea62e085f943660f0a7ab2
service_worker.js: 2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

Latest complete Codex full gate remains the exact Phase-1 e13a gate:

```text
PD-00..PD-17: ALL PASS
Manual-ON transaction regression: PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source/package identity: PASS
real Yandex requests: 0
verdict: PASS
```

Owner real-profile Phase-1 acceptance:

```text
getRegionsTree PASS
getTop PASS
getDynamics PASS
getRegionsDistribution PASS
```

Phase 1 Wordstat is LIVE PASS / CLOSED.

## Phase 2 Search authority

```text
protocol: SEARCH_API_V1
service: search
method: search
mode: synchronous text web search
endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
response format: FORMAT_XML
result signature: SEARCH_RESULT_V1
```

Outside the first slice:

```text
searchAsync / Operation polling
image search
generative search
HTML normalization
browser scraping of yandex.ru
```

Canonical Phase-2 docs:

```text
extension/docs/PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/PHASE_2_FOUR_STAGE_EXECUTION_CONTROL.md
```

Search must reuse the accepted common Manual/Autorun/outbox/conversation/owner-tab/no-blind-retry core.

## Phase 2 four-stage execution status

### STAGE 1 — exact base + Search foundation

```text
STATUS = PASS / COMPLETED
```

Evidence:

```text
exact Phase-1 e13a base: 45/45 exact; mismatches 0; missing 0; extras 0
Stage-1 target files: 50
Stage-1 target manifest SHA-256: 62bd5846c8f7d6ade7f788d4394d79e02e802611144a4249761ccbb07397b98b
focused Search: 32/32 PASS
affected suite: 86/86 PASS
full suite: 393/393 PASS
syntax: PASS
JSON: PASS
real Yandex requests: 0
```

Durable Stage-1 evidence:

```text
extension/tests/phase2/search-foundation/FOUNDATION_EVIDENCE_2026-08-19.json
extension/tests/phase2/search-foundation/target-tree-sha256.tsv
extension/tests/phase2/search-foundation/phase2-search-foundation.patch.gz.b64
```

### STAGE 2 — worker/provider/credential/policy execution

```text
STATUS = PASS / COMPLETED
```

Canonical Stage-2 target is exact Stage-1 target plus the preserved Stage-2 patch. Target identity:

```text
target files: 51
target manifest SHA-256: a274600440461cc7ac4669e959d3b84ee6dfaa9dffb26219ee7e1dd0086f8236
fresh git apply --check: PASS
fresh target identity: 51/51 exact; mismatches 0; missing 0; extras 0
```

Stage-2 production hashes:

```text
service_worker.js def73ebb44243b57d0be98ad21fec6ccf230cc2dfe1b29f8ee3588e17fe80282 / 190920 bytes
shared/credential_registry.js 506aafca071522c7dc110dd72feec4d7fbee36119849abac69158c9be232a311 / 1413 bytes
shared/policy_model.js c97c2b8dd600091f894d2c7c5c0fb91a6408d5cc848bc579ec3acc6cb59d99bf / 6086 bytes
```

Stage-2 verified behavior:

```text
Search protocol/XML loaded in worker
service-aware Search/Wordstat routing
local API-key + folderId Search capability without exposing credentials in command/result
one POST /v2/web/search exactly per admitted Search command
validation/credential/policy rejection before provider -> zero initiation
HTTP error after initiation -> ERROR / request_executed=true / automatic_retry=false
ambiguous initiated network failure -> request_executed=UNKNOWN / automatic_retry=false / no retry
XML normalization failure after HTTP success -> executed=true / no retry
conservative Search cost guard = 0.488 RUB/request
request and RUB run-budget enforcement
reservation computed before provider initiation
Authorization/API-key redaction
Search/Wordstat protocol isolation
```

Verification:

```text
focused Search Stage 2: 10/10 PASS
full source suite: 377/377 PASS
syntax: 46/46 PASS
JSON: 2/2 PASS
real Yandex requests: 0
```

Exact Stage-2 transport evidence:

```text
patch SHA-256: 6b9c7f55fd736261ce794f818f66ea066dc1256c3ae05e849c97373c7b4ccedc
patch bytes: 32357
gzip SHA-256: 4f9bac5de1e658c40e14305d9dbe6fca17b58718a562e6e546e26328a8285a54
base64 SHA-256: 717d8b1c76450949053c33bfeff1921401f433076f0f8b0c9c3c78f5539f662d
base64 chars: 10676
```

Durable Stage-2 evidence on the development branch:

```text
extension/tests/phase2/search-worker-provider/STAGE2_EVIDENCE_2026-08-20.json
extension/tests/phase2/search-worker-provider/target-tree-sha256.tsv
extension/tests/phase2/search-worker-provider/phase2-stage2-worker-provider.patch.gz.b64
```

No browser/DOM fact was required in Stage 2, so no Codex measurement was needed.

### STAGE 3 — Manual/Autorun/operator/delivery integration

```text
STATUS = ACTIVE / IN WORK
```

Authorized Stage-3 scope:

```text
popup Search active-service/operator controls
Search Manual + Autorun policy/limits
eligible SEARCH_API_V1 external `Яндекс` action through the common Manual surface
native Copy independence
owner-tab + conversation binding + single-flight reuse
one immutable service per Autorun RUN
Wordstat/Search RUN isolation
worker-owned outbox/result/error delivery
composer occupied protection
committed Send at most once
ready/Microphone completion + watch-only recovery
YMB_ERROR_V1 + Debug redaction
Export/Import compatibility
full regression, syntax/JSON, zero real Yandex requests
```

If any Stage-3 decision depends on an unknown current ChatGPT DOM/browser/runtime fact, do not infer it; request a concrete Codex measurement.

### STAGE 4 — frozen candidate / exact transport / Codex / owner live

```text
STATUS = PENDING STAGE 3 PASS
```

## Current control-plane reconstruction

```text
LIVE_HEAD = fetch live main before every control-plane write
PRODUCT_SOURCE = exact Stage-2 target: Stage-1 foundation + Stage-2 patch; 51 files; manifest a274600440461cc7ac4669e959d3b84ee6dfaa9dffb26219ee7e1dd0086f8236
HANDOFF_ARTIFACT = NONE for Phase 2; no frozen combined candidate yet
LATEST_FULL_GATE = Phase-1 exact e13a PASS only; no Phase-2 combined full gate yet
PRODUCTION_BYTES_CHANGED_SINCE_GATE = YES in Phase-2 development lineage
OWNER_LIVE = Phase 1 PASS; Phase 2 PENDING
OPEN_BLOCKERS = NONE for Stage 3
AUTHORIZED_NEXT_STAGE = PHASE_2_STAGE_3_MANUAL_AUTORUN_OPERATOR_DELIVERY_INTEGRATION
CODEX_MEASUREMENT_PENDING = NO
OWNER_ACTION_PENDING = NO
```

## Phase status

```text
PHASE 0 = PASS
PHASE 1 WORDSTAT = LIVE PASS / CLOSED
PHASE 2 YANDEX SEARCH / SERP = ACTIVE / STAGE 1 PASS / STAGE 2 PASS / STAGE 3 IN WORK / STAGE 4 PENDING
PHASE 3 WEBMASTER = BLOCKED
PHASE 4 METRIKA = BLOCKED
PHASE 5 DIRECT READ = BLOCKED
PHASE 6 DIRECT DRAFT/PRE-LIVE WRITE = BLOCKED
PHASE 7 DIRECT LIVE WRITE = BLOCKED
PHASE 8 FULL ORDER E2E = BLOCKED
```
