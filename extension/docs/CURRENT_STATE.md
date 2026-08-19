# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY / OWNER-REQUESTED PAUSE**  
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

Exact `e13a…` owner-live results:

```text
getRegionsTree            PASS / HTTP 200 / request_executed true / charged false
getTop                    PASS / HTTP 200 / request_executed true / charged true
getDynamics               PASS / HTTP 200 after correcting test-command toDate
getRegionsDistribution    PASS / HTTP 200 / request_executed true / charged true
```

The first `getDynamics` attempt returned HTTP 400 because the test command supplied the first day rather than the required last day of the ending month. Classification: `PROMPT/EXECUTION INSTRUCTION`, not product. The bridge correctly reported `request_executed:true`, `automatic_retry:false`; after the cause was established the corrected command was issued and passed. This was not a blind retry.

Sequential real Manual admissions across `getRegionsTree → getTop → getDynamics error → corrected getDynamics → getRegionsDistribution` prove that completed result/error delivery no longer strands the Manual lock.

Full owner-live evidence authority:

```text
extension/docs/PHASE_1_0.1.1_LIVE_ACCEPTANCE.md
```

Issues #1 and #2 are CLOSED / COMPLETED.

## Phase 2 Search requirements — COMPLETE

Current Phase-2 requirement authority:

```text
extension/docs/PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
```

Mandatory Phase-2 specification companion:

```text
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
```

Mandatory Phase-2 controlled-gate companion:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
```

These two addenda supersede stale pre-Phase-2 `Search blocked` wording only for the governed Search first slice. The existing main `SPECIFICATION.md` and living PD gate remain mandatory for common/Wordstat behavior.

Official Yandex Search API facts were freshly checked on 2026-08-19 against Yandex-owned documentation/source.

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

Explicitly outside the first slice:

```text
searchAsync / Operation polling
image search
generative search
HTML normalization
browser scraping of yandex.ru
```

Current official tariff snapshot relevant to the first slice:

```text
day synchronous:   488 RUB / 1000 = 0.488 RUB/request
night synchronous: 366 RUB / 1000 = 0.366 RUB/request
night window: 00:00:00–07:59:59 UTC+3
```

Unless explicit tariff-window logic is implemented, reserve the conservative higher daytime cost. Owner-live paid Search commands require a fresh official price check immediately before execution.

Search must reuse the accepted common Manual/Autorun/outbox/conversation/owner-tab/no-blind-retry core rather than fork service-specific delivery logic.

## Phase 2 foundation research checkpoint

Append-only checkpoint authority:

```text
extension/docs/DEVELOPMENT_CONTEXT_APPEND_ONLY_CONTINUATION_PHASE2_2026-08-19.md
```

At the pause boundary:

```text
PHASE_2_PRODUCTION_CHANGES = NONE
PHASE_2_TEST_CHANGES = NONE
CODEX_MEASUREMENT_PENDING = NO
OWNER_ACTION_PENDING = NO
```

Repository/product structure needed for the first foundation was re-established from live GitHub. Current Yandex-owned SDK source was inspected to confirm the synchronous `WebSearchRequest` mapping and XML result structure instead of guessing it. Confirmed parser facts include `<response> → <group> → <doc>`, optional `url/domain/title/modtime/lang`, repeated `<passage>` values, UTF-8 XML decode, and tolerant handling of missing/invalid optional fields.

Owner rule is now explicit for continuation:

```text
UNKNOWN BROWSER/DOM/RUNTIME FACT
→ do not guess
→ issue a concrete Codex measurement prompt

REPOSITORY FACT
→ read live GitHub

PUBLIC YANDEX API FACT
→ read current official Yandex source/docs
```

## Owner-requested pause boundary

The owner explicitly ordered work to stop and wait for a continuation command.

No further product, test, QA-transport, Codex or owner-live action is authorized until the owner says to continue.

On resume, first re-fetch live `main` and this file. Then continue from the exact recorded Search foundation point:

```text
service registry registration for search/SEARCH_API_V1
→ Search protocol/defaults/strict validation
→ exact synchronous WebSearch request-body builder
→ Base64 UTF-8 XML normalization
→ focused tests
→ focused/source checks
```

Only after that foundation is green should worker/provider/policy integration proceed. If any browser/DOM/runtime fact becomes unknown, request Codex measurement instead of inventing behavior.

## Current control-plane reconstruction

```text
PRODUCT_SOURCE = accepted Phase-1 e13a source; no Phase-2 production changes yet
HANDOFF_ARTIFACT = e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65 / Phase-1 accepted artifact
LATEST_FULL_GATE = PASS on exact Phase-1 e13a artifact
PRODUCTION_BYTES_CHANGED_SINCE_GATE = NO
OWNER_LIVE = Phase 1 PASS
OPEN_BLOCKERS = OWNER-REQUESTED PAUSE ONLY
AUTHORIZED_NEXT_STAGE = PAUSED_BY_OWNER
RESUME_STAGE = PHASE_2_SEARCH_IMPLEMENTATION_FOUNDATION
```

## Phase status

```text
PHASE 0 = PASS
PHASE 1 WORDSTAT = LIVE PASS / CLOSED
PHASE 2 YANDEX SEARCH / SERP = REQUIREMENTS + SPEC ADDENDUM + GATE ADDENDUM READY; FOUNDATION RESEARCH CHECKPOINTED; PRODUCTION NOT CHANGED; PAUSED BY OWNER
PHASE 3 WEBMASTER = BLOCKED
PHASE 4 METRIKA = BLOCKED
PHASE 5 DIRECT READ = BLOCKED
PHASE 6 DIRECT DRAFT/PRE-LIVE WRITE = BLOCKED
PHASE 7 DIRECT LIVE WRITE = BLOCKED
PHASE 8 FULL ORDER E2E = BLOCKED
```