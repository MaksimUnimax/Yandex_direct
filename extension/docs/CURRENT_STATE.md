# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY**  
Updated: 2026-08-19

This file applies immediately in the current conversation and every new/resumed conversation. Always fetch live `main` HEAD before action.

## Repository

```text
repo: MaksimUnimax/Yandex_direct
branch: main
```

## Mandatory QA transport runbook

Before preparing any future Codex pre-delivery prompt, ChatGPT must read and execute:

```text
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

The runbook preserves the concrete transport/reconstruction/consumer-conformance sequence that actually reached a complete Codex PASS. Do not reconstruct that procedure from memory or invent a replacement while the proven route remains applicable.

## Phase 1 exact accepted artifact

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505
files 45
ZIP entries 48
version 0.1.1
```

Production hashes:

```text
content_script.js ddf9ed51c60ab90dcdeb1fcd5a1b955c3dd88dfc53a0ddfd5842d66ebe9a02cc
popup.js ac87ad973e8b673bf0c235a43b3dc29dfb67865594ea62e085f943660f0a7ab2
service_worker.js 2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

The previous `31cc5f…` artifact is retired after owner-live `FAIL_PRODUCT` on Manual ON self-revert.

## Artifact/transport failure history retained for governance

Two early QA attempts for `e13a…` failed before product testing:

```text
FAIL_ARTIFACT #1
expected e13a… / 209505
received 37d896… / 14999 / not a ZIP

FAIL_ARTIFACT #2
source tree 45/45 exact
reconstructed ZIP 8359c6… / 209505
expected e13a…
```

These failures did not change production bytes. Permanent prevention rules are in:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

## Exact successful QA transport authority

```text
qa transport branch: qa/e13a-exact-reconstruction-v3
exact preimage SHA-256: 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
raw patch SHA-256: 709234433bd446f52a18c95785675d0f5ca3450b82459ce2631d36bdb7269bc2
canonical executable packer: extension/tests/qa_transport/e13a/canonical_packer_exact.py
```

The published executable packer reproduces exact `e13a… / 209505 / 45 files / 48 entries` and was independently consumed by Codex.

## Latest complete Codex pre-delivery full gate — PASS

Gate-start authority:

```text
main HEAD: 7bab312c84877627c3f264ff99c3fe5b4546a5b2
qa transport branch: qa/e13a-exact-reconstruction-v3
```

Result:

```text
artifact SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
artifact bytes: 209505
files: 45
ZIP entries: 48
ZIP integrity: PASS
target tree identity: PASS
canonical packer modified: NO
PD-00..PD-17: ALL PASS
Manual-ON transaction regression: PASS
real installed extension popup used: PASS
worker ON committed before content apply: PASS
content final Manual ON: PASS
popup final Manual ON: PASS
Yandex action after apply/resync: PASS
popup reopen / OFF / second ON transitions: PASS
ON→OFF self-revert observed: NO
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

Codex reports:

```text
D:\codex\Yandex\qa-evidence-ymb-full-gate-20260819-06\CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_2026-08-19.md
D:\codex\Yandex\qa-evidence-ymb-full-gate-20260819-06\CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_2026-08-19.json
```

## Owner real-profile Phase-1 functional acceptance — PASS

Current explicit owner scope for final live acceptance was:

```text
only functional tests involving Yandex
UI observed naturally while those tests execute
one test at a time
fresh official pricing check before each paid executable command
no blind retry
```

Exact `e13a…` owner-live results:

```text
getRegionsTree            PASS / HTTP 200 / request_executed true / charged false
getTop                    PASS / HTTP 200 / request_executed true / charged true
getDynamics               PASS / HTTP 200 after correcting test-command toDate
getRegionsDistribution    PASS / HTTP 200 / request_executed true / charged true
```

The first `getDynamics` attempt returned HTTP 400 because the test command supplied the first day rather than the required last day of the ending month. Classification: `PROMPT/EXECUTION INSTRUCTION`, not product. The bridge correctly reported `request_executed:true`, `automatic_retry:false`; after the cause was established the corrected command was issued and passed. This was not a blind retry.

Sequential real Manual admissions across `getRegionsTree → getTop → getDynamics error → corrected getDynamics → getRegionsDistribution` prove that completed result/error delivery no longer strands the Manual lock; no stale `MANUAL_OPERATION_ACTIVE` blocked the next operation.

Real-profile newly rendered command blocks repeatedly exposed a usable `Яндекс` action and executed the intended operation without requiring native Copy as the execution trigger. No live UI regression was reported during the required functional sequence.

Full owner-live evidence authority:

```text
extension/docs/PHASE_1_0.1.1_LIVE_ACCEPTANCE.md
```

## Issues

```text
Issue #1 external Yandex action / Copy independence: CLOSED / COMPLETED
Issue #2 stale Manual operation lock: CLOSED / COMPLETED
```

## Current control-plane reconstruction

```text
PRODUCT_SOURCE = accepted repaired e13a source; production hashes above
HANDOFF_ARTIFACT = e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65 / 209505 / 45 files / full Codex PASS / owner-live PASS
LATEST_FULL_GATE = PASS on exact e13a artifact; PD-00..PD-17 ALL PASS; Manual-ON addendum PASS
PRODUCTION_BYTES_CHANGED_SINCE_GATE = NO
OWNER_LIVE = PASS on exact e13a
OPEN_BLOCKERS = NONE for Phase 1
AUTHORIZED_NEXT_STAGE = PHASE_2_YANDEX_SEARCH_REQUIREMENT_RECONSTRUCTION
```

## Phase status

```text
PHASE 0 = PASS
PHASE 1 WORDSTAT = LIVE PASS / CLOSED
PHASE 2 YANDEX SEARCH / SERP = UNLOCKED FOR REQUIREMENT RECONSTRUCTION; implementation not started
PHASE 3 WEBMASTER = BLOCKED
PHASE 4 METRIKA = BLOCKED
PHASE 5 DIRECT READ = BLOCKED
PHASE 6 DIRECT DRAFT/PRE-LIVE WRITE = BLOCKED
PHASE 7 DIRECT LIVE WRITE = BLOCKED
PHASE 8 FULL ORDER E2E = BLOCKED
```

Do not start Search implementation from memory. The next Search action is to reconstruct live authority/specification and current Yandex Search API facts before product changes.