# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH / STAGE 4 ACTIVE — EXACT CANDIDATE + TRANSPORT + BROWSER HARNESS READY FOR NEW COMPLETE CODEX GATE**  
Updated: 2026-08-24

Always fetch live `main` HEAD and commit metadata before any control-plane write or workflow-stage transition.

## Mandatory reconstruction record

The live control-plane checkpoint inspected immediately before this state update was:

```text
LIVE_HEAD_BEFORE_STATE_UPDATE = aef832c2c543f3c3d36fe45689240896429e9957
PRODUCT_SOURCE = 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
HANDOFF_ARTIFACT = d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16 / 170734 bytes
LATEST_COMPLETE_CODEX_GATE = FAIL_HARNESS on exact candidate; browser blocker subsequently reconciled and independently preflighted PASS
PRODUCTION_BYTES_CHANGED_SINCE_GATE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_GATE = NO
OWNER_LIVE = PENDING / BLOCKED UNTIL COMPLETE CODEX PASS + FRESH OFFICIAL PRICING CHECK
OPEN_BLOCKERS = complete Codex campaign has not yet returned PASS
AUTHORIZED_NEXT_STAGE = CODEX_COMPLETE_PRE_DELIVERY_FULL_GATE
```

The current live `main` HEAD may legitimately be newer than the checkpoint above because this document update itself changes `main`; always read live GitHub before acting.

## Owner / process rule

- ChatGPT owns product, tests, packaging, QA authoring, transport preparation, harness preparation and failure-layer fixes.
- Codex is the independent QA executor only; it must not patch production/tests or weaken assertions.
- Stage 3 is closed; do not resume hypothetical edge-case hunting unless Stage-4 evidence proves a product defect.
- Controlled QA uses zero real Yandex requests and zero real Yandex credentials.
- Owner-live paid Search acceptance is blocked until one complete Codex PASS on the exact frozen candidate and a fresh official pricing check.
- No blind retry after a provider initiation with uncertain outcome.

## Current exact frozen product authority

```text
repo: MaksimUnimax/Yandex_direct
product branch: candidate/phase2-search-reconstruction-2026-08-23
product PR: #5 Phase 2 Search reconstruction candidate
Stage-3 production closure: 75d18291224069a6ae67c110498481ec7320d3c0
Stage-4 refrozen source commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
artifact: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
artifact SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
artifact bytes: 170734
files: 65
ZIP entries: 68
payload manifest bytes: 11421
payload manifest SHA-256: 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
```

The earlier `1869d17... / 0f0b035c...` Stage-4 freeze is superseded historical evidence. No current QA/harness/documentation correction has changed the frozen `0ee1d38... / d58b5bd...` candidate, so **no refreeze is authorized or required**.

The two governed package-test corrections that caused the refreeze remain:

```text
extension/tests/PHASE_2_STAGE_4_PACKAGED_SUITE_ADAPTER_2026-08-24.md
53c415c5f984f004705b401bd788673b0d2064c1 — popup owner-tab test alignment
84a8ea01f815bb5da28da2b5c9bdc1c456739fdc — report-prefix owner-tab test alignment
```

## Exact source/package preflight authority

Permanent read-only freeze/preflight evidence:

```text
workflow: phase2-stage4-freeze
run: 32714268931
job: 97392079851
conclusion: SUCCESS
source suite: 231/231 PASS
packaged suite: 231/231 PASS
packaged syntax: 59 PASS
packaged JSON: 2 PASS
SOURCE_PACKAGE_IDENTITY_PASS
EXACT_ARTIFACT_IDENTITY_PASS
PACKAGE_EXACT_IDENTITY_PASS
PACKAGED_SUITE_LAYOUT_IDENTITY_PASS
PACKAGED_PREDELIVERY_PREFLIGHT_PASS
real Yandex requests: 0
```

## Current Windows-safe exact transport authority

The old transport commit `9dedf7bf624174996fae7efa7a4bdbff6904d348` is **historical Linux consumer evidence only** and must not be used by a new Windows Codex checkout.

Current exact transport:

```text
branch: qa/phase2-stage4-final-b64-transport-0ee1d38-2026-08-24
transport commit: bc7754cff6416ff59942ff6f1052d450792888d5
path: extension/tests/qa_transport/phase2-stage4-final-b64/
.gitattributes: * -text
```

Mandatory transport reconciliation:

```text
extension/docs/CODEX_PHASE2_STAGE4_WINDOWS_TRANSPORT_RECONCILIATION_2026-08-24.md
```

Windows consumer proof:

```text
run: 32717179084
job: 97400791303
OS: Microsoft Windows Server 2025
Git: 2.55.0.windows.4
core.autocrlf: true
raw manifest: 11421 bytes / 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
WINDOWS_RAW_MANIFEST_IDENTITY_PASS
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
WINDOWS_FROZEN_AUTHORITY_MATCH_PASS
WINDOWS_TRANSPORT_CLEAN_PASS
REAL_YANDEX_REQUESTS=0
```

## Current Stage-4 browser-harness authority

Mandatory browser reconciliation:

```text
extension/docs/CODEX_PHASE2_STAGE4_BROWSER_HARNESS_RECONCILIATION_2026-08-24.md
```

Exact browser-harness authority:

```text
harness commit: 667fda2f9a0e4197c4873ea96f27862c8453f2f0
harness: extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_gate.mjs
harness blob: 127e6042037ac0cbb044e81b2a9c554f24b5aa6b
TLS cert blob: d91cb127e8d8f6cfa5a95723a15612fd03478af6
TLS local-only QA key blob: 2d0ab1f091b119d964a7ebdcd15720f6cd9728ad
Chrome for Testing: 151.0.7922.47
Puppeteer: 25.4.0
```

The TLS key is a self-signed loopback fixture key only, not a provider credential and not part of the installable ZIP.

Independent Windows browser preflight:

```text
QA PR: #10 — CLOSED WITHOUT MERGE after evidence
workflow run: 32720334374
job: 97410193364
conclusion: SUCCESS
harness commit: 667fda2f9a0e4197c4873ea96f27862c8453f2f0
transport commit: bc7754cff6416ff59942ff6f1052d450792888d5
exact artifact: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
```

Required observed markers:

```text
B01_PROJECT_WORK_PASS
BROWSER_STEP_BIND_PASS
BROWSER_STEP_SEARCH_SETTINGS_PASS
BROWSER_STEP_MANUAL_FIRST_ON_PASS
BROWSER_STEP_NATIVE_COPY_PASS
B02_MANUAL_ON_TRANSACTION_PASS
BROWSER_STEP_AUTORUN_START_PASS
BROWSER_STEP_SEARCH_DELIVERY_PASS
B03_SEARCH_AUTORUN_PASS
BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1
BROWSER_GATE_REAL_YANDEX_REQUESTS=0
PHASE2_STAGE4_BROWSER_GATE_PASS
BROWSER_HARNESS_CLEAN_PASS
```

The temporary browser verifier workflow was removed from `main` after PASS. The durable harness and reconciliation document remain.

Comparison from transport-reconciliation main (`8fe5a751...`) through final synchronized harness authority (`667fda2...`) changed only QA infrastructure paths under `.github/workflows/...` and `extension/tests/qa_browser/phase2-stage4/...`; frozen production and package-test bytes were not changed.

## Latest complete Codex attempt and failure classification

The most recent complete Codex attempt successfully consumed the exact artifact and established:

```text
transport identity: PASS
source suite: 231/231 PASS
packaged suite: 231/231 PASS
packaged syntax: 59/59 PASS
packaged JSON: 2/2 PASS
production modified during gate: NO
tests modified during gate: NO
real Yandex requests: 0
```

It returned `FAIL_HARNESS` because current executable browser venues were not yet published for B-01/B-02/B-03. That failure is now **RECONCILED** by the browser authority and Windows PASS evidence above. It is not product-failure evidence.

Earlier stopped attempts remain historical QA-process evidence only:

```text
Attempt 1: FAIL_HARNESS at PD-00 — packaged-suite adapter authority missing from main; reconciled by 5fe4201c...
Attempt 2: FAIL_ARTIFACT at PD-00 — Windows LF→CRLF transport conversion; reconciled by bc7754c... and Windows consumer PASS
Attempt 3: FAIL_HARNESS after exact source/package PASS — browser venues missing; reconciled by 667fda2... and run 32720334374 PASS
```

No attempt changed product bytes or used real Yandex requests/credentials.

## Current Phase-2 Search boundary

The current companion specification is mandatory:

```text
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
```

Where older base `SPECIFICATION.md` still says Search is blocked, the Phase-2 addendum plus this `CURRENT_STATE.md` supersede that stale phase-lock wording for Phase 2.

Enabled first slice:

```text
protocol: SEARCH_API_V1
service: search
method: search
endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
mode: synchronous text WebSearch only
response format: FORMAT_XML
normalized result: SEARCH_RESULT_V1
```

Still phase-locked:

```text
Search async/deferred polling
Search image
Search generative
HTML SERP normalization
yandex.ru scraping
Webmaster
Metrika
Direct
```

## Stage status

```text
STAGE 1 — Search foundation = PASS / COMPLETED
STAGE 2 — provider/credentials/policy = PASS / COMPLETED
STAGE 3 — Manual/Autorun/operator/delivery integration = PASS / COMPLETED
STAGE 4 — exact refrozen candidate = PASS
STAGE 4 — complete source preflight = 231/231 PASS
STAGE 4 — deterministic rebuild/source-package identity = PASS
STAGE 4 — complete packaged preflight = 231/231 PASS
STAGE 4 — Windows-safe exact transport consumer proof = PASS
STAGE 4 — current installed-extension B-01/B-02/B-03 browser preflight = PASS
STAGE 4 — complete Codex pre-delivery full gate = PENDING NEW COMPLETE RERUN
STAGE 4 — owner-live paid Search = BLOCKED UNTIL COMPLETE CODEX PASS
```

## Mandatory Codex authority for the next campaign

Read from live `main` before execution:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CURRENT_STATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
extension/docs/PHASE_2_STAGE_4_CODEX_EXECUTION_MAP_2026-08-24.md
extension/tests/PHASE_2_STAGE_4_PACKAGED_SUITE_ADAPTER_2026-08-24.md
extension/tests/PHASE_2_STAGE_4_REFROZEN_CANDIDATE_CHECKPOINT_2026-08-24.md
extension/docs/CODEX_PHASE2_STAGE4_WINDOWS_TRANSPORT_RECONCILIATION_2026-08-24.md
extension/docs/CODEX_PHASE2_STAGE4_BROWSER_HARNESS_RECONCILIATION_2026-08-24.md
extension/docs/CODEX_PHASE2_STAGE4_FINAL_HANDOFF_2026-08-24.md
```

Precedence for candidate-specific stale text:

```text
Windows transport reconciliation supersedes stale 9ded... transport references.
Browser-harness reconciliation supersedes stale B-01/B-02/B-03 venue references.
All other final-handoff / execution-map / PD / Manual / Search requirements remain mandatory.
```

The next Codex execution must be a **new complete campaign from the beginning** against the same exact `d58b5bd...` artifact:

```text
PD-00 … PD-17
+ mandatory Manual-ON real-popup transaction
+ S-00 … S-17 Phase-2 Search addendum
+ complete source suite
+ complete packaged suite
+ browser B-01/B-02/B-03 through exact harness 667fda2...
+ final exact artifact / cleanliness proof
```

No enabled mandatory section may remain `NOT_RUN` in a PASS verdict. Real Yandex requests = exactly 0. Real Yandex credentials = 0.

Allowed final verdicts:

```text
PASS
FAIL_PRODUCT
FAIL_ARTIFACT
FAIL_HARNESS
```

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = CODEX_COMPLETE_PRE_DELIVERY_FULL_GATE
OWNER_LIVE_SEARCH = BLOCKED
```

If Codex finds a real product defect, return evidence to ChatGPT and change only the proven layer. Any production-byte or package-test-byte change creates a new candidate and invalidates the current `d58b5bd...` gate authority. QA/harness/reporting/documentation fixes must not mutate frozen payload bytes.
