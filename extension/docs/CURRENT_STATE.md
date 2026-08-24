# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH / STAGE 4 ACTIVE — REFROZEN EXACT CANDIDATE READY FOR COMPLETE CODEX GATE**  
Updated: 2026-08-24

Always fetch live `main` HEAD before any control-plane write.

## Owner / process rule

- ChatGPT owns product, tests, packaging, QA authoring and transport preparation.
- Stage 3 is closed; do not resume hypothetical edge-case hunting unless Stage-4 evidence proves a product defect.
- Codex is QA executor only for the complete frozen-candidate gate; it must not patch product/tests to make failures pass.
- Controlled QA uses zero real Yandex requests and zero real credentials.
- Owner-live paid Search acceptance is blocked until complete Codex PASS and a fresh official pricing check.
- No blind retry after a provider initiation with uncertain outcome.

## Current exact authority

```text
repo: MaksimUnimax/Yandex_direct
product branch: candidate/phase2-search-reconstruction-2026-08-23
product PR: #5 Phase 2 Search reconstruction candidate
Stage-3 production closure: 75d18291224069a6ae67c110498481ec7320d3c0
Stage-4 refrozen source commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
```

The earlier Stage-4 candidate at source `1869d17...` / ZIP `0f0b035c...` is **superseded historical evidence**. It became ineligible for final Codex PASS after two QA test assertions inside the package payload were corrected. Production runtime source did not change, but package bytes did, so the gate authority was correctly refrozen.

The two package-test corrections are governed by:

```text
extension/tests/PHASE_2_STAGE_4_PACKAGED_SUITE_ADAPTER_2026-08-24.md
53c415c5f984f004705b401bd788673b0d2064c1 — popup owner-tab test alignment
84a8ea01f815bb5da28da2b5c9bdc1c456739fdc — report-prefix owner-tab test alignment
```

## Current exact handoff artifact

```text
filename: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
root: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate/
SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
bytes: 170734
files: 65
ZIP entries: 68
ZIP integrity: PASS
source commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
```

Package payload remains the established Phase-2 layout:

```text
all extension/src/** files
+ root-level extension/tests/*.test.mjs
```

Repository docs, evidence trees, `.github/**`, nested QA transport files and the packaged-suite adapter are not handoff payload.

## Exact payload manifest

```text
filename: EXACT_CANDIDATE_MANIFEST_2026-08-24.json
format: YMB_PHASE2_EXACT_CANDIDATE_V1
source commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
manifest bytes: 11421
manifest SHA-256: 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
artifact SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
artifact bytes: 170734
files: 65
entries: 68
zip_test: PASS
```

All 65 package file paths, byte counts and SHA-256 hashes are fixed by this manifest.

## Refreeze / complete preflight evidence

Permanent read-only workflow:

```text
workflow: phase2-stage4-freeze
run: 32714268931
job: 97392079851
conclusion: SUCCESS
```

That single exact-source run checked out `0ee1d38...` and completed:

```text
complete source suite: 231/231 PASS
fail: 0
skipped: 0
cancelled: 0

deterministic build A: PASS
deterministic build B: PASS
byte-for-byte ZIP cmp: PASS
SOURCE_PACKAGE_IDENTITY_PASS
EXACT_ARTIFACT_IDENTITY_PASS

complete packaged suite via governed adapter: 231/231 PASS
packaged JS/MJS syntax: 59 PASS
packaged JSON: 2 PASS
PACKAGE_EXACT_IDENTITY_PASS
PACKAGED_SUITE_LAYOUT_IDENTITY_PASS
PACKAGED_PREDELIVERY_PREFLIGHT_PASS

real Yandex requests: 0
```

The packaged-suite adapter changes only the temporary QA execution layout. It verifies exact ZIP/manifest bytes before staging, copies runtime/test bytes without modification, runs syntax/JSON/full tests, and never mutates the frozen artifact.

## Actions artifact transport / independent consumer round-trip

```text
artifact name: phase2-stage4-frozen-candidate-0ee1d38
artifact ID: 9515289771
wrapper bytes: 182585
wrapper SHA-256: 9936e229e8f080d2a24a06892d4ca231a9f625e1ecc267fba57662b446c45e55
```

A fresh consumer downloaded artifact ID `9515289771` and independently verified:

```text
wrapper SHA-256 = 9936e229e8f080d2a24a06892d4ca231a9f625e1ecc267fba57662b446c45e55
wrapper bytes = 182585
inner ZIP SHA-256 = d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
inner ZIP bytes = 170734
manifest SHA-256 = 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
manifest bytes = 11421
ZIP integrity = PASS
files = 65
entries = 68
all 65 path/byte/SHA-256 rows match manifest = PASS
```

## Final Codex-accessible exact transport

The authorized repository transport for the current refrozen bytes is:

```text
branch: qa/phase2-stage4-final-b64-transport-0ee1d38-2026-08-24
transport commit: 9dedf7bf624174996fae7efa7a4bdbff6904d348
path: extension/tests/qa_transport/phase2-stage4-final-b64/
format: YMB_PHASE2_STAGE4_FINAL_EXACT_B64_TRANSPORT_V1
source Actions run: 32714268931
source Actions artifact ID: 9515289771
base64 length: 227648
chunks: 16 × 14228 bytes
```

Fresh-consumer proof:

```text
QA PR: #9 — closed without merge after evidence
consumer run: 32715052351
consumer job: 97394394286
permission: Contents read
checked-out exact transport head: 9dedf7bf624174996fae7efa7a4bdbff6904d348

B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
FINAL_FROZEN_AUTHORITY_MATCH_PASS
REAL_YANDEX_REQUESTS=0
```

Each published chunk has an independent byte count and SHA-256 in the transport manifest. The verifier reconstructs the ZIP using only the repository text chunks, validates exact artifact identity, opens/tests the ZIP and checks every payload row against the full manifest.

Temporary write-publisher and read-only consumer-verifier workflows were removed from `main` after PASS. The final transport branch remains immutable QA input for Codex.

### Historical rejected transport evidence

Do not use these for final Codex input:

```text
old binary mirror PR #7 / run 32709361187 → EXACT_ZIP_IDENTITY_FAIL
classification: QA transport producer failure, not product failure

old B64 v2 transport d398b290... → exact PASS for superseded ZIP 0f0b035c...
classification: historical transport proof only; artifact superseded by refreeze
```

## Accepted Phase 1 baseline

Phase 1 Wordstat remains **LIVE PASS / CLOSED**.

```text
accepted historical artifact SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
version: 0.1.1
historical complete full gate: PASS
owner-live Wordstat: PASS for getTop, getDynamics, getRegionsDistribution, getRegionsTree
```

Historical Phase-1 PASS does not replace the complete combined Wordstat+Search gate for the current refrozen candidate.

## Phase 2 Search boundary

```text
protocol: SEARCH_API_V1
service: search
method: search
endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
mode: synchronous text WebSearch only
response format: FORMAT_XML
normalized result: SEARCH_RESULT_V1
```

Out of scope / still phase-locked:

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

The Search Phase-2 addendum supersedes the generic parent-gate Search future-service lock only for this governed synchronous text Search surface. Webmaster/Metrika/Direct and deferred/image/generative Search remain locked.

## Stage status

```text
STAGE 1 — Search foundation = PASS / COMPLETED
STAGE 2 — provider/credentials/policy = PASS / COMPLETED
STAGE 3 — Manual/Autorun/operator/delivery integration = PASS / COMPLETED
STAGE 4 — exact refrozen candidate = PASS
STAGE 4 — complete source preflight = 231/231 PASS
STAGE 4 — deterministic rebuild/source-package identity = PASS
STAGE 4 — complete packaged preflight = 231/231 PASS
STAGE 4 — Actions artifact consumer round-trip = PASS
STAGE 4 — Codex-accessible text-safe transport fresh-consumer proof = PASS
STAGE 4 — executable PD/S coverage map = PASS
STAGE 4 — complete Codex pre-delivery full gate = PENDING
STAGE 4 — owner-live paid Search = BLOCKED UNTIL CODEX PASS
```

## Codex authority

The complete campaign must use all of:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
extension/docs/PHASE_2_STAGE_4_CODEX_EXECUTION_MAP_2026-08-24.md
extension/tests/PHASE_2_STAGE_4_PACKAGED_SUITE_ADAPTER_2026-08-24.md
```

Codex exact input is transport commit `9dedf7bf624174996fae7efa7a4bdbff6904d348`. Before any product assertion, Codex must run the published verifier and independently establish ZIP `d58b5bd...`, 170734 bytes, 65 files, 68 entries and full manifest parity.

Then Codex executes **one complete campaign** against that same exact artifact:

```text
PD-00 … PD-17
+ mandatory Manual-ON transaction addendum
+ S-00 … S-17 Phase-2 Search addendum
```

Browser-owned assertions use qualified Chrome for Testing + Puppeteer. Internal crash/recovery states may use deterministic integration. Full source and packaged suites are mandatory. No enabled section may be `NOT_RUN` in a PASS verdict.

Allowed final verdicts:

```text
PASS
FAIL_PRODUCT
FAIL_ARTIFACT
FAIL_HARNESS
```

Real Yandex requests during controlled gate: exactly 0. Real credentials: 0.

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = CODEX_COMPLETE_PRE_DELIVERY_FULL_GATE
OWNER_LIVE_SEARCH = BLOCKED
```

If Codex finds a product defect, return it to ChatGPT. Any production-byte or packaged-test-byte change creates a new candidate and invalidates the current `d58b5bd...` gate authority. QA/harness/reporting fixes must not mutate frozen payload bytes.
