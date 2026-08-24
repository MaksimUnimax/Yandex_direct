# Codex Phase 2 Stage 4 — final rerun handoff

Date: 2026-08-24  
Status: **CURRENT PRIMARY HANDOFF / START ONE NEW COMPLETE CAMPAIGN FROM THE BEGINNING**

This file integrates the exact frozen candidate, Windows-safe transport reconciliation and current browser-harness reconciliation into one execution authority. It does not weaken or replace the living PD/Manual/Search gates; it removes stale candidate-specific ambiguity from older handoff text.

## Role

You are the independent QA executor. Do not develop fixes during this campaign.

Forbidden during the campaign:

```text
production edits
package-test edits
acceptance weakening
candidate substitution
refreeze
real Yandex credentials
real Yandex requests
patching a failure to continue
```

If an assertion fails, preserve evidence, classify the failing layer and continue unrelated safe sections when possible. No enabled mandatory `NOT_RUN` is allowed in a PASS verdict.

Allowed final verdicts only:

```text
PASS
FAIL_PRODUCT
FAIL_ARTIFACT
FAIL_HARNESS
```

## Repository

```text
MaksimUnimax/Yandex_direct
```

## Step 0 — connect to live authority first

1. Fetch current `origin/main`.
2. Read the current live `main` HEAD and commit metadata.
3. Do not assume the expected SHA below is still the newest commit; if `main` legitimately advanced, inspect the newer metadata and continue only if the authority below remains in force.
4. Read these files from current `main` before execution:

```text
extension/docs/README.md
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CURRENT_STATE.md
extension/docs/PROJECT_PURPOSE.md
extension/docs/SPECIFICATION.md
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
extension/docs/ROADMAP.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
extension/docs/PHASE_2_STAGE_4_CODEX_EXECUTION_MAP_2026-08-24.md
extension/tests/PHASE_2_STAGE_4_PACKAGED_SUITE_ADAPTER_2026-08-24.md
extension/tests/PHASE_2_STAGE_4_REFROZEN_CANDIDATE_CHECKPOINT_2026-08-24.md
extension/docs/CODEX_PHASE2_STAGE4_WINDOWS_TRANSPORT_RECONCILIATION_2026-08-24.md
extension/docs/CODEX_PHASE2_STAGE4_BROWSER_HARNESS_RECONCILIATION_2026-08-24.md
this file
```

Candidate-specific precedence is mandatory:

```text
Windows transport reconciliation
→ supersedes every stale reference to transport commit 9dedf7bf...

Browser-harness reconciliation
→ supersedes stale/missing B-01/B-02/B-03 browser venue references

This final-rerun handoff
→ is the primary candidate-specific execution entry point

All other living PD / Manual / Search / package / cleanliness requirements
→ remain mandatory
```

## Exact frozen candidate — unchanged

```text
source commit:
0ee1d38f8d28cfccceb5a07f9606fa715261bc27

artifact:
yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip

artifact SHA-256:
d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16

artifact bytes:
170734

files:
65

ZIP entries:
68

payload manifest bytes:
11421

payload manifest SHA-256:
0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
```

Do not use the superseded `1869d17... / 0f0b035c...` freeze.

No product or package-test bytes changed during the transport/browser QA repairs. **No refreeze is required.**

## Step 1 — consume only the current Windows-safe exact transport

Current transport authority:

```text
branch:
qa/phase2-stage4-final-b64-transport-0ee1d38-2026-08-24

commit:
bc7754cff6416ff59942ff6f1052d450792888d5

path:
extension/tests/qa_transport/phase2-stage4-final-b64/
```

The historical transport commit `9dedf7bf624174996fae7efa7a4bdbff6904d348` is superseded for a new Windows checkout. Do not use it.

After fresh checkout of `bc7754...`, verify the raw working-tree bytes of:

```text
extension/tests/qa_transport/phase2-stage4-final-b64/EXACT_CANDIDATE_MANIFEST_2026-08-24.json
```

Require exactly:

```text
bytes: 11421
SHA-256: 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
```

Also require `git check-attr text` to show text conversion disabled/unset for that file.

Then run:

```text
python extension/tests/qa_transport/phase2-stage4-final-b64/verify_exact_b64_transport.py
```

Require:

```text
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
REAL_YANDEX_REQUESTS=0
```

Known independent Windows consumer proof:

```text
run: 32717179084
job: 97400791303
OS: Microsoft Windows Server 2025
Git: 2.55.0.windows.4
core.autocrlf: true
WINDOWS_RAW_MANIFEST_IDENTITY_PASS
WINDOWS_FROZEN_AUTHORITY_MATCH_PASS
WINDOWS_TRANSPORT_CLEAN_PASS
REAL_YANDEX_REQUESTS=0
```

You must still verify your own consumed checkout.

Materialize the exact ZIP from the published chunks into a fresh QA temp directory. Hash it again and require `d58b5bd... / 170734` before any product PASS credit.

## Step 2 — complete exact source suite

Checkout exact frozen source:

```text
git checkout 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
cd extension/src
npm test
```

Require:

```text
231/231 PASS
0 fail
0 skipped
0 cancelled
```

Do not edit tests if a failure appears.

## Step 3 — static / syntax / manifest integrity

Against exact frozen source and exact package bytes:

- parse/check every JS/MJS;
- parse governed JSON;
- verify manifest entrypoints/resources;
- verify expected permissions/host permissions;
- verify no accidental production surface;
- retain exact artifact identity.

Use the execution map for the concrete PD mapping.

## Step 4 — complete exact packaged suite

Do not run the package tests directly from the installable ZIP root with an invalid repository-relative layout.

Use the governed packaged-suite adapter:

```text
python extension/tests/qa_transport/phase2-candidate/run_packaged_suite.py \
  --archive <EXACT_D58B5BD_ZIP> \
  --manifest <EXACT_CANDIDATE_MANIFEST_2026-08-24.json> \
  --work-dir <FRESH_QA_TEMP>/packaged-suite-work
```

Require:

```text
PACKAGE_EXACT_IDENTITY_PASS
PACKAGED_SUITE_LAYOUT_IDENTITY_PASS
PACKAGED_SYNTAX_PASS count=59
PACKAGED_JSON_PASS count=2
231/231 packaged tests PASS
PACKAGED_SUITE_PASS files=38
PACKAGED_PREDELIVERY_PREFLIGHT_PASS
```

The adapter may only create a temporary QA execution layout. It must not change ZIP/source/test bytes.

## Step 5 — current browser-owned B-01/B-02/B-03 authority

Use exact harness commit:

```text
667fda2f9a0e4197c4873ea96f27862c8453f2f0
```

Current harness files:

```text
extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_gate.mjs
extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.key.pem
extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.cert.pem
```

The key/cert are local-only self-signed loopback QA fixture material, not Yandex credentials and not frozen product payload.

Create a clean detached harness worktree at exact commit `667fda2...`.

Install only the external driver dependency without saving tracked package state:

```text
npm install --prefix extension/tests/qa_browser/phase2-stage4 --no-save --package-lock=false puppeteer-core@25.4.0
```

Use:

```text
Chrome for Testing 151.0.7922.47
Puppeteer 25.4.0
headful isolated QA profile
exact extracted d58b5bd... extension root
controlled local HTTPS ChatGPT fixture
controlled local Search stub
```

Execute:

```text
node extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_gate.mjs \
  <CHROME_PATH> \
  <EXACT_EXTRACTED_D58B5BD_EXTENSION_ROOT> \
  extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.key.pem \
  extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.cert.pem
```

Require all markers:

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
```

After cleanup also require a clean harness checkout.

Known independent browser proof already completed:

```text
QA PR #10 — closed without merge
run: 32720334374
job: 97410193364
conclusion: SUCCESS
B01_PROJECT_WORK_PASS
B02_MANUAL_ON_TRANSACTION_PASS
B03_SEARCH_AUTORUN_PASS
BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1
BROWSER_GATE_REAL_YANDEX_REQUESTS=0
PHASE2_STAGE4_BROWSER_GATE_PASS
BROWSER_HARNESS_CLEAN_PASS
```

You must still execute the browser gate yourself as part of the complete campaign; the preflight is capability/harness proof, not a substitute for this campaign's browser evidence.

### B-01

Prove installed exact extension / Project-Work route / MV3 worker / real popup initialization and controlled local fixture behavior.

### B-02 — mandatory Manual-ON transaction

This harness is the current executable venue for the mandatory real-popup Manual-ON addendum. It must use the real popup, not an internal shortcut, and prove worker/content/action behavior including reopen, OFF removal and second ON re-arm.

### B-03 — Search Autorun/operator lifecycle

Use the real popup plus controlled Search stub. Prove Search settings, Start, WAITING_COMMAND, one controlled provider-stub initiation, real result-delivery path, popup reopen truth, Pause, owner/non-owner isolation, Resume and Finish.

Use deterministic integration tests from the execution map for crash/recovery states assigned outside browser manufacture.

## Step 6 — execute the complete governed matrix

Execute **all** enabled sections:

```text
PD-00 through PD-17
+
mandatory Manual-ON real-popup transaction
+
S-00 through S-17 Search Phase-2 addendum
```

Do not stop after one ordinary assertion failure when unrelated safe sections can still run. Collect the complete failure set.

No mandatory enabled section may remain `NOT_RUN` in a PASS verdict.

### Enabled Search surface

```text
SEARCH_API_V1
service: search
method: search
POST https://searchapi.api.cloud.yandex.net/v2/web/search
FORMAT_XML
SEARCH_RESULT_V1
synchronous text Search only
```

### Surfaces that remain zero-provider locked

```text
Search async/deferred
Search image
Search generative
Webmaster
Metrika
Direct
arbitrary assistant-selected URLs/methods/headers
```

All network behavior in controlled QA must be local stub/fault-injection only. No real Yandex request is allowed.

## Step 7 — final exactness / cleanliness

At the end:

1. rerun the exact transport verifier;
2. re-hash exact ZIP and require `d58b5bd... / 170734`;
3. re-check the full 65-row manifest;
4. prove production bytes were not changed during gate;
5. prove package-test bytes were not changed during gate;
6. remove temporary browser/driver/worktree files;
7. require controlled real Yandex requests exactly `0`;
8. require no real credentials/secrets in evidence;
9. make every PD/S section explicit;
10. emit one Markdown report and one JSON report.

## Required final result

Return a complete:

```text
CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT

candidate:
  source_commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
  artifact: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
  artifact_sha256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
  artifact_bytes: 170734
  files: 65
  zip_entries: 68
  payload_manifest_sha256: 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
  payload_manifest_bytes: 11421
  transport_commit: bc7754cff6416ff59942ff6f1052d450792888d5
  browser_harness_commit: 667fda2f9a0e4197c4873ea96f27862c8453f2f0

live_main_head: <actual SHA at start>
step_0_authority: PASS|FAIL
transport: PASS|FAIL
source_suite: <pass>/<total>
packaged_suite: <pass>/<total>
packaged_syntax: <pass>/<total>
packaged_json: <pass>/<total>
browser_project_work: PASS|FAIL
browser_manual_on_transaction: PASS|FAIL
browser_search_autorun: PASS|FAIL
controlled_search_stub_requests: <integer>
real_yandex_requests: <integer>
real_credentials_used: YES|NO
production_modified_during_gate: YES|NO
tests_modified_during_gate: YES|NO
final_cleanliness: PASS|FAIL
not_run_enabled_sections: <integer>

sections:
  PD-00: PASS|FAIL
  PD-01: PASS|FAIL
  PD-02: PASS|FAIL
  PD-03: PASS|FAIL
  PD-04: PASS|FAIL
  PD-05: PASS|FAIL
  PD-06: PASS|FAIL
  PD-07: PASS|FAIL
  PD-08: PASS|FAIL
  PD-09: PASS|FAIL
  PD-10: PASS|FAIL
  PD-11: PASS|FAIL
  PD-12: PASS|FAIL
  PD-13: PASS|FAIL
  PD-14: PASS|FAIL
  PD-15: PASS|FAIL
  PD-16: PASS|FAIL
  PD-17: PASS|FAIL

manual_on_transaction: PASS|FAIL

search_sections:
  S-00: PASS|FAIL
  S-01: PASS|FAIL
  S-02: PASS|FAIL
  S-03: PASS|FAIL
  S-04: PASS|FAIL
  S-05: PASS|FAIL
  S-06: PASS|FAIL
  S-07: PASS|FAIL
  S-08: PASS|FAIL
  S-09: PASS|FAIL
  S-10: PASS|FAIL
  S-11: PASS|FAIL
  S-12: PASS|FAIL
  S-13: PASS|FAIL
  S-14: PASS|FAIL
  S-15: PASS|FAIL
  S-16: PASS|FAIL
  S-17: PASS|FAIL

search_phase2:
  protocol_registry: PASS|FAIL
  parser_validation: PASS|FAIL
  provider_request_exactly_once: PASS|FAIL
  credential_policy: PASS|FAIL
  cost_guard: PASS|FAIL
  base64_xml_decode: PASS|FAIL
  xml_normalization: PASS|FAIL
  manual_path: PASS|FAIL
  autorun_path: PASS|FAIL
  wordstat_search_isolation: PASS|FAIL
  http_unknown_no_retry: PASS|FAIL
  future_search_modes_locked: PASS|FAIL
  real_yandex_requests: <integer>
  verdict: PASS|FAIL

failures:
  <complete list with gate id, classification, expected, actual and evidence>

verdict: PASS|FAIL_PRODUCT|FAIL_ARTIFACT|FAIL_HARNESS
```

`PASS` is valid only when every mandatory PD section, every S section, mandatory Manual-ON transaction, source/package suites, current browser gate and final exactness/cleanliness all pass; `not_run_enabled_sections=0`; `real_yandex_requests=0`; `real_credentials_used=NO`; production/tests were not mutated.

## Historical stopped attempts — do not repeat them

```text
Attempt 1:
FAIL_HARNESS at PD-00
cause: packaged-suite adapter authority missing from main
reconciled by: 5fe4201c8fa62331efb3dec30a08b99f0f2aaa13
product bytes involved: NO

Attempt 2:
FAIL_ARTIFACT at PD-00
cause: Windows LF→CRLF conversion of exact transport manifest
reconciled by: bc7754cff6416ff59942ff6f1052d450792888d5
product bytes involved: NO

Attempt 3:
FAIL_HARNESS after exact transport/source/package PASS
cause: current B-01/B-02/B-03 browser venue not yet published
reconciled by: 667fda2f9a0e4197c4873ea96f27862c8453f2f0 + Windows browser PASS run 32720334374/job 97410193364
product bytes involved: NO
```

Do not stop merely because these historical failures exist. Their exact QA-process causes are reconciled.

## Start rule

Start a **new clean complete campaign from Step 0**. Do not resume an old stopped workspace state. Do not patch failures during the campaign. Return the complete result above.
