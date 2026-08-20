# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY / PHASE 2 STAGE 4 ACTIVE**  
Updated: 2026-08-20

Always fetch live `main` HEAD before any control-plane write.

## Repository

```text
repo: MaksimUnimax/Yandex_direct
control branch: main
Phase-2 development branch: dev/phase2-search-foundation-2026-08-19
```

## Mandatory workflow authorities

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
extension/docs/PHASE_2_FOUR_STAGE_EXECUTION_CONTROL.md
extension/docs/PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
```

Work continuously inside each four-stage boundary without micro-step chatter. At each stage PASS: preserve exact evidence in GitHub, update this file, report once to owner, then continue automatically unless owner action, Codex action, or a real blocker is required.

Unknown current browser/DOM/runtime facts MUST NOT be guessed. Stop at the exact uncertainty and request a concrete Codex measurement.

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

Latest complete Codex full gate remains the exact Phase-1 e13a gate: PD-00..PD-17 ALL PASS; source 361/361; packaged 361/361; syntax 40/40; JSON 2/2; source/package identity PASS; real Yandex requests 0. Owner real-profile Wordstat acceptance PASS for all four supported operations. Phase 1 is LIVE PASS / CLOSED.

## Phase 2 first Search slice

```text
protocol: SEARCH_API_V1
service: search
method: search
mode: synchronous text web search
endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
response format: FORMAT_XML
result signature: SEARCH_RESULT_V1
```

Outside first slice: async/polling, image search, generative search, HTML normalization, yandex.ru scraping.

## Four-stage execution status

### STAGE 1 — exact base + Search foundation

```text
STATUS = PASS / COMPLETED
base e13a: 45/45 exact
Stage-1 target files: 50
target manifest SHA-256: 62bd5846c8f7d6ade7f788d4394d79e02e802611144a4249761ccbb07397b98b
focused: 32/32 PASS
affected: 86/86 PASS
full suite: 393/393 PASS
syntax: PASS
JSON: PASS
real Yandex requests: 0
```

Durable evidence:

```text
extension/tests/phase2/search-foundation/FOUNDATION_EVIDENCE_2026-08-19.json
extension/tests/phase2/search-foundation/target-tree-sha256.tsv
extension/tests/phase2/search-foundation/phase2-search-foundation.patch.gz.b64
```

### STAGE 2 — worker/provider/credential/policy execution

```text
STATUS = PASS / COMPLETED
target files: 51
target manifest SHA-256: a274600440461cc7ac4669e959d3b84ee6dfaa9dffb26219ee7e1dd0086f8236
fresh apply identity: 51/51 PASS
focused Search Stage 2: 10/10 PASS
full suite: 377/377 PASS
syntax: 46/46 PASS
JSON: 2/2 PASS
real Yandex requests: 0
```

Stage 2 covers Search credential capability, separate Search policy, conservative 0.488 RUB guard, request/RUB limits and reservation, exactly one POST `/v2/web/search`, secret redaction, truthful HTTP/UNKNOWN outcomes, no blind retry, and Search/Wordstat provider isolation.

Durable evidence:

```text
extension/tests/phase2/search-worker-provider/STAGE2_EVIDENCE_2026-08-20.json
extension/tests/phase2/search-worker-provider/target-tree-sha256.tsv
extension/tests/phase2/search-worker-provider/phase2-stage2-worker-provider.patch.gz.b64
```

### STAGE 3 — Manual/Autorun/operator/delivery integration

```text
STATUS = PASS / COMPLETED
Stage-3 target files: 51
target manifest SHA-256: b9806e8f2a9ec172ad90ba343fa7183f7f01121fd1ddc3fb69db80b03dda423f
fresh git apply --check: PASS
fresh target identity: 51/51 PASS
focused Manual + Search worker: 38/38 PASS
popup runtime: 13/13 PASS
full suite: 382/382 PASS
syntax: 46/46 PASS
JSON: 2/2 PASS
real Yandex requests: 0
```

Stage-3 product hashes:

```text
content_script.js a789b7ec586632d2dde287b59ccaee11d8de010ae9a474cdcd9a68a0b252e688
manifest.json ac48a2399f7f77d1382958231038a999e8c7dfd37e4cdc60a9b9241a62c0c96f
popup.html 778c5d2068a2cccd7648f4cef16f649870878e114baa43e4eabf43a628b34cc0
popup.js 03b13ad6af722ea9cc92d26e7e299519fbd500e43d71f2c9c225a903bfe6c274
service_worker.js 87a4022b7273618ac4df343cff50f7fd155d03c26dc17b68169a569dd0a43c3b
```

Verified Stage-3 behavior:

```text
Search Manual uses the same external `Яндекс` action and durable Manual delivery path
registered wrong-service Manual command rejects SERVICE_NOT_ACTIVE before durable claim/fetch
paused Search RUN Manual uses the same immutable service and RUN budgets
Search Autorun uses active_service-specific protocol and provider execution
Search/Wordstat cross-service Autorun commands reject before fetch
Search watcher active_service propagates worker -> content
popup exposes Wordstat/Search service selector and separate Search policy/limits
Search start prompt/default is service-aware
settings export/import includes Search policy while credentials remain separate
common owner-tab/conversation/single-flight/outbox/composer/no-blind-retry machinery remains shared
```

Failure containment retained:

```text
15 initial Stage-3 failures = TEST/HARNESS drift from Wordstat-only assertions/module loading; corrected without weakening equivalent invariants.
One real PRODUCT gap found: Manual service mismatch was only rejected after durable claim. Fixed by registered-service preflight routing check before durable claim; zero provider initiation. Focused + full regression PASS afterward.
```

Exact Stage-3 local transport evidence:

```text
patch SHA-256: d2338b7d1f233e3622fdc1da49038df0e96afe0785b2addfbab4f961fda9cee6
patch bytes: 81690
gzip SHA-256: 5c32e7a16f0102cc0c54cb59fb15a1b815795462822a8338692adef2d1487ec5
base64 SHA-256: edc73c040de67310a03c284728d45589b7a901721ff7b4b4df52d5f363b113de
target manifest SHA-256: b9806e8f2a9ec172ad90ba343fa7183f7f01121fd1ddc3fb69db80b03dda423f
```

Durable Stage-3 evidence on development branch:

```text
extension/tests/phase2/search-runtime-integration/STAGE3_EVIDENCE_2026-08-20.json
extension/tests/phase2/search-runtime-integration/target-tree-sha256.tsv
```

No new browser/DOM fact was required; no Codex measurement was needed in Stage 3.

### STAGE 4 — frozen candidate / exact transport / Codex / owner live

```text
STATUS = ACTIVE / IN WORK
```

Required next work:

```text
freeze the exact Stage-3 target as the Phase-2 combined candidate
build deterministic installable ZIP
verify source/package identity, archive integrity, file/entry counts and exact SHA-256
prepare byte-complete Codex-accessible transport using the mandatory proven transport runbook
round-trip consume that published transport before issuing any Codex prompt
run complete Phase-1 + Phase-2 controlled gate with zero real Yandex traffic
only after Codex PASS: owner real-profile paid Search acceptance, one test at a time with a fresh official price check
```

## Current control-plane reconstruction

```text
LIVE_HEAD = fetch live main before every control-plane write
PRODUCT_SOURCE = exact Stage-3 target; 51 files; manifest b9806e8f2a9ec172ad90ba343fa7183f7f01121fd1ddc3fb69db80b03dda423f
HANDOFF_ARTIFACT = NONE; Phase-2 candidate is not frozen yet
LATEST_FULL_GATE = Phase-1 exact e13a PASS only; Phase-2 combined gate pending
PRODUCTION_BYTES_CHANGED_SINCE_GATE = YES
OWNER_LIVE = Phase 1 PASS; Phase 2 PENDING
OPEN_BLOCKERS = NONE before Stage-4 artifact/transport work
AUTHORIZED_NEXT_STAGE = PHASE_2_STAGE_4_FREEZE_PACKAGE_TRANSPORT_AND_CODEX_GATE
CODEX_MEASUREMENT_PENDING = NO
OWNER_ACTION_PENDING = NO
```

## Phase status

```text
PHASE 0 = PASS
PHASE 1 WORDSTAT = LIVE PASS / CLOSED
PHASE 2 SEARCH = ACTIVE / STAGE 1 PASS / STAGE 2 PASS / STAGE 3 PASS / STAGE 4 IN WORK
PHASE 3 WEBMASTER = BLOCKED
PHASE 4 METRIKA = BLOCKED
PHASE 5 DIRECT READ = BLOCKED
PHASE 6 DIRECT DRAFT/PRE-LIVE WRITE = BLOCKED
PHASE 7 DIRECT LIVE WRITE = BLOCKED
PHASE 8 FULL ORDER E2E = BLOCKED
```
