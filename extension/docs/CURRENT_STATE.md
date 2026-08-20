# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY / PHASE 2 STAGE 2 ACTIVE**  
Updated: 2026-08-20

This file applies immediately in the current conversation and every new/resumed conversation. Always fetch live `main` HEAD before action.

## Repository

```text
repo: MaksimUnimax/Yandex_direct
control branch: main
Phase-2 development branch: dev/phase2-search-foundation-2026-08-19
```

## Mandatory workflow authorities

Before future Codex handoff, read and execute:

```text
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

Phase-2 engineering is now governed by the owner-ordered four-stage execution control:

```text
extension/docs/PHASE_2_FOUR_STAGE_EXECUTION_CONTROL.md
```

Mandatory stage reporting rule:

```text
work continuously inside a stage without micro-step chatter
→ preserve product/test/evidence in GitHub
→ when stage exit criteria PASS, write durable checkpoint
→ update CURRENT_STATE
→ send owner one concise completion report
→ continue automatically to next stage unless owner pause/action, Codex action, or real blocker is required
```

Unknown browser/DOM/runtime facts MUST NOT be guessed. Stop at the exact uncertainty and request a concrete Codex measurement.

## Phase 1 accepted authority

Exact accepted artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505
files 45
ZIP entries 48
version 0.1.1
```

Critical accepted production hashes:

```text
content_script.js ddf9ed51c60ab90dcdeb1fcd5a1b955c3dd88dfc53a0ddfd5842d66ebe9a02cc
popup.js ac87ad973e8b673bf0c235a43b3dc29dfb67865594ea62e085f943660f0a7ab2
service_worker.js 2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

Successful exact Phase-1 QA transport authority:

```text
branch: qa/e13a-exact-reconstruction-v3
preimage SHA-256: 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
raw patch SHA-256: 709234433bd446f52a18c95785675d0f5ca3450b82459ce2631d36bdb7269bc2
target manifest: extension/tests/qa_transport/e13a/target-tree-sha256.tsv
canonical packer: extension/tests/qa_transport/e13a/canonical_packer_exact.py
```

Latest complete Codex gate remains the Phase-1 e13a gate:

```text
PD-00..PD-17: ALL PASS
Manual-ON transaction regression: PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source/package identity: PASS
real Yandex requests: 0
production modified during gate: NO
tests modified during gate: NO
failures: NONE
verdict: PASS
```

Owner real-profile Phase-1 functional acceptance:

```text
getRegionsTree            PASS
getTop                    PASS
getDynamics               PASS after corrected test-command toDate
getRegionsDistribution    PASS
```

Issues #1 and #2 are CLOSED / COMPLETED. Phase 1 Wordstat is LIVE PASS / CLOSED.

## Phase 2 Search authority

Requirements/spec/gate documents:

```text
extension/docs/PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/PHASE_2_FOUR_STAGE_EXECUTION_CONTROL.md
```

First implementation slice:

```text
protocol: SEARCH_API_V1
service: search
method: search
mode: synchronous text web search
REST endpoint: POST /v2/web/search
response format: FORMAT_XML
result signature: SEARCH_RESULT_V1
```

Explicitly outside first slice:

```text
searchAsync / Operation polling
image search
generative search
HTML normalization
browser scraping of yandex.ru
```

Search reuses the accepted common Manual/Autorun/outbox/conversation/owner-tab/no-blind-retry core rather than forking delivery logic.

## Phase 2 four-stage execution status

### STAGE 1 — exact base + Search foundation

```text
STATUS = PASS / COMPLETED
```

Exact e13a base materialization was completed and verified:

```text
45/45 exact
identity mismatches: 0
missing: 0
extras: 0
```

Foundation product surfaces on the Phase-2 development lineage:

```text
shared/service_registry.js
shared/search_protocol.js
shared/search_xml.js
```

Foundation verification:

```text
focused Search: 32/32 PASS
affected after registry-test correction: 86/86 PASS
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

Known foundation commits include:

```text
6d0c1c2bdbfb9e2b18b32adb25a0c5885f932f2e  phase2: add SEARCH_API_V1 protocol foundation
01f777c7a1e0e06efcb1338c403ea69c86e3d4e8  phase2: add Search XML normalization foundation
e52f6fae18b53cb90306a5dab643568bfaa00f27  phase2: register Search protocol in service registry
69a92de2841a67bee05f347bc8389d81bc4e51eb  phase2: add exact Search foundation patch transport
```

### STAGE 2 — worker/provider/credential/policy execution

```text
STATUS = ACTIVE / IN WORK
```

Required Stage-2 scope:

```text
Search runtime module loading
worker routing SEARCH_API_V1 -> search
Search credential capability + local folderId
POST /v2/web/search provider execution
Authorization redaction
one provider initiation exactly per accepted command
validation/policy/credential rejection -> zero initiation
HTTP error -> truthful ERROR / no retry
ambiguous initiated outcome -> UNKNOWN / no retry
conservative Search cost reservation before initiation
Search request/RUB budgets
Wordstat/Search routing isolation
focused integration tests + full regression
real Yandex requests = 0
```

Do not advance to Stage 3 until Stage-2 exit criteria in `PHASE_2_FOUR_STAGE_EXECUTION_CONTROL.md` are PASS and a durable Stage-2 checkpoint/report exists.

### STAGE 3 — Manual/Autorun/operator/delivery integration

```text
STATUS = PENDING STAGE 2 PASS
```

This stage integrates Search into popup/operator controls and the accepted common Manual/Autorun/outbox/delivery/browser runtime, with Codex measurement required for any unknown browser/DOM fact.

### STAGE 4 — frozen candidate/Codex/owner-live closure

```text
STATUS = PENDING STAGE 3 PASS
```

This stage freezes the exact candidate, executes the proven artifact transport runbook, obtains complete Codex full-gate PASS, then performs irreducible owner real-profile paid Search acceptance one command at a time after fresh official pricing verification.

## Current control-plane reconstruction

```text
LIVE_HEAD = main docs authority must be fetched live before action
PRODUCT_SOURCE = Phase-2 dev lineage based on exact accepted e13a + completed Search foundation
HANDOFF_ARTIFACT = NONE for Phase 2; Phase-1 e13a remains accepted historical/live artifact only
LATEST_FULL_GATE = PASS on exact Phase-1 e13a; no Phase-2 combined candidate gate yet
PRODUCTION_BYTES_CHANGED_SINCE_GATE = YES in Phase-2 development lineage
OWNER_LIVE = Phase 1 PASS; Phase 2 PENDING
OPEN_BLOCKERS = NONE for beginning Stage 2
AUTHORIZED_NEXT_STAGE = PHASE_2_STAGE_2_WORKER_PROVIDER_CREDENTIAL_POLICY_EXECUTION
CODEX_MEASUREMENT_PENDING = NO
OWNER_ACTION_PENDING = NO
```

## Phase status

```text
PHASE 0 = PASS
PHASE 1 WORDSTAT = LIVE PASS / CLOSED
PHASE 2 YANDEX SEARCH / SERP = ACTIVE / STAGE 1 PASS / STAGE 2 IN WORK / STAGES 3-4 PENDING
PHASE 3 WEBMASTER = BLOCKED
PHASE 4 METRIKA = BLOCKED
PHASE 5 DIRECT READ = BLOCKED
PHASE 6 DIRECT DRAFT/PRE-LIVE WRITE = BLOCKED
PHASE 7 DIRECT LIVE WRITE = BLOCKED
PHASE 8 FULL ORDER E2E = BLOCKED
```
