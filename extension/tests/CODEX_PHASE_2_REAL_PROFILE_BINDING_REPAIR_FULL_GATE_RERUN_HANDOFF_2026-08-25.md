# Codex rerun handoff — Phase 2 real-profile binding repair complete pre-delivery gate

Status: **READY FOR INDEPENDENT CODEX COMPLETE RERUN / SAME FROZEN ARTIFACT / OWNER LIVE BLOCKED**  
Date: 2026-08-25

This document supersedes `CODEX_PHASE_2_REAL_PROFILE_BINDING_REPAIR_FULL_GATE_HANDOFF_2026-08-25.md` for the next independent campaign. The first independent campaign returned `FAIL_HARNESS`; product bytes were not implicated and remain frozen.

Codex is the independent QA executor only. ChatGPT remains owner of product, tests, harnesses, packaging and failure repair.

## 0. Mandatory campaign rule

This is a **new complete campaign from the beginning**.

Do not resume only PD-10/PD-11/PD-13/PD-17 or S-11/S-13/S-17 from the failed campaign. Historical PASS values are evidence, not transferable final credit. Start at Step 0 / PD-00 and execute every enabled section.

Codex MUST NOT:

- edit production code;
- edit package tests;
- edit either pinned browser harness or the current Stage-4 compatibility wrapper;
- weaken, skip, reinterpret or replace assertions;
- substitute a rebuilt/logically-equivalent ZIP for the exact transported artifact;
- use real Yandex credentials;
- make any real Yandex request;
- repair any failure itself.

On failure, classify and report the exact failing layer to ChatGPT.

## 1. Live authority to reconstruct first

Before any test, fetch live `main` and read at minimum:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CURRENT_STATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
extension/tests/PHASE_2_REAL_PROFILE_BINDING_REPAIR_FREEZE_TRANSPORT_CHECKPOINT_2026-08-25.md
extension/tests/PHASE_2_REAL_PROFILE_BINDING_STAGE4_HARNESS_RECONCILIATION_2026-08-25.md
```

Required frozen authority:

```text
PRODUCT_SOURCE = b7869180c229356a6b3d51ac980ec3da5df4c23c
PRODUCT_PARENT = f4aee34c0a3455aa7199f6aa54bd581c71d97337
ARTIFACT_FILENAME = yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
ARTIFACT_SHA256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
ARTIFACT_BYTES = 179013
FILES = 69
ZIP_ENTRIES = 72
PAYLOAD_MANIFEST_SHA256 = ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
PAYLOAD_MANIFEST_BYTES = 12125
TRANSPORT_COMMIT = 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
OWNER_LIVE = BLOCKED
PRODUCTION_BYTES_CHANGED_SINCE_FREEZE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_FREEZE = NO
AUTHORIZED_NEXT_STAGE = INDEPENDENT_CODEX_COMPLETE_RERUN_SAME_EXACT_CE824A9F
```

Verify `PRODUCT_PARENT..PRODUCT_SOURCE` is one commit and exactly these six files:

```text
extension/src/content_script.js
extension/src/popup.js
extension/src/popup_context_bootstrap.js
extension/src/shared/conversation_identity.js
extension/tests/popup_phase2_runtime.test.mjs
extension/tests/real_profile_binding_regression.test.mjs
```

Any authority mismatch is a blocking artifact/control-plane failure. Do not guess.

## 2. Exact artifact acquisition — unchanged from first campaign

Use only the published exact B64 transport:

```text
branch = qa/phase2-real-profile-binding-final-b64-transport-b786918-2026-08-25
commit = 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
dir = extension/tests/qa_transport/phase2-real-profile-binding-final-b64
```

Verify:

```text
git rev-parse HEAD == 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
git rev-parse HEAD^ == b7869180c229356a6b3d51ac980ec3da5df4c23c
```

The transport delta must be exactly five files under the transport directory.

Run:

```text
python extension/tests/qa_transport/phase2-real-profile-binding-final-b64/verify_exact_b64_transport.py
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

Persist the decoded exact ZIP in a fresh QA output directory and independently require SHA-256 `ce824a9f...`, 179013 bytes, 69 files, 72 ZIP entries and ZIP integrity PASS. Fresh-extract it and verify every payload path/byte count/hash against the exact payload manifest.

Do not rebuild another ZIP as the package under test.

## 3. Source/package/static regression — rerun from zero

In a separate clean source workspace at exact `b786918...`:

```text
cd extension/src
npm test
```

Expected frozen baseline is `244/244`, but report actual observed count.

Run all syntax/JSON checks required by the permanent gate. Frozen preflight baseline:

```text
source JS syntax = 22/22
source JSON = 2/2
packaged JS syntax = 63/63
packaged JSON = 2/2
```

Run the complete packaged suite against the fresh extraction of the exact transported ZIP using the canonical package-suite adapter from the exact product source. Frozen baseline is `244/244`; report actual observed count.

## 4. Current Stage-4 B-01/B-02/B-03 venue — mandatory reconciled harness

The first independent campaign failed because it invoked the historical Stage-4 `openPopup()` directly. That invocation is no longer the current governed venue.

The historical assertions themselves remain immutable authority:

```text
HISTORICAL_COMMIT = 667fda2f9a0e4197c4873ea96f27862c8453f2f0
HISTORICAL_HARNESS = extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_gate.mjs
HISTORICAL_HARNESS_BLOB = 127e6042037ac0cbb044e81b2a9c554f24b5aa6b
TLS_KEY = extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.key.pem
TLS_KEY_BLOB = 2d0ab1f091b119d964a7ebdcd15720f6cd9728ad
TLS_CERT = extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.cert.pem
TLS_CERT_BLOB = d91cb127e8d8f6cfa5a95723a15612fd03478af6
```

The current compatibility wrapper is external QA authority:

```text
CURRENT_STAGE4_WRAPPER_BRANCH = qa/phase2-current-stage4-browser-harness-b786918-2026-08-25
CURRENT_STAGE4_WRAPPER_COMMIT = 1babfe66222251e2eb63e6e0d4e3eb726ed898e9
CURRENT_STAGE4_WRAPPER_PATH = extension/tests/qa_browser/phase2-stage4-current/run_current_stage4_gate.mjs
CURRENT_STAGE4_WRAPPER_BLOB = e1763df3cec988c3bee93efcdd6369eb8c12d695
```

Verify the wrapper branch is based on `b786918...` and the full delta from product source is exactly the single wrapper file above. Do not modify it.

Qualified environment:

```text
Windows
Chrome for Testing = 151.0.7922.47
puppeteer-core = 25.4.0
```

Install Puppeteer only in the external harness workspace.

Run the wrapper with five arguments:

```text
node extension/tests/qa_browser/phase2-stage4-current/run_current_stage4_gate.mjs \
  <PATH_TO_HISTORICAL_browser_phase2_stage4_gate.mjs> \
  <CHROME_151_EXECUTABLE> \
  <FRESH_EXTRACTED_EXACT_CE824A9F_PACKAGE_ROOT> \
  <PATH_TO_HISTORICAL_qa-chatgpt-local.key.pem> \
  <PATH_TO_HISTORICAL_qa-chatgpt-local.cert.pem>
```

The wrapper is allowed to modify only a temporary in-memory/on-disk QA copy of the historical harness lifecycle functions. It deletes that temporary file after execution. The historical Git object and frozen artifact stay immutable.

Required Stage-4 markers include:

```text
HISTORICAL_STAGE4_ASSERTIONS_PRESERVED
CURRENT_STAGE4_POPUP_LIFECYCLE_PATCH_READY
CURRENT_POPUP_BOOTSTRAP_VENUE_PASS
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

This is the governed replacement for direct execution of the obsolete historical `openPopup()` lifecycle. The assertions below that lifecycle are intentionally preserved.

A wrapper/environment failure on an otherwise exact package is `FAIL_HARNESS`. A failed historical product assertion after the wrapper reaches the current popup context is `FAIL_PRODUCT`.

## 5. Other permanent browser/integration requirements

Execute every other enabled requirement from the permanent gate and Manual/Search addenda, including native Chrome-151 popup geometry and all deterministic integration/fault-injection coverage. Do not transfer PASS credit from the first failed campaign.

Explicit final coverage still requires:

```text
PD-00..PD-17 = every section PASS
manual_on_transaction = PASS
S-00..S-17 = every section PASS
```

No enabled `NOT_RUN` is permitted in PASS.

## 6. Mandatory repair-specific real-profile browser harness

This remains unchanged and must also be rerun in the new complete campaign:

```text
branch = qa/phase2-real-profile-binding-browser-harness-b786918-2026-08-25
commit = 81625e073d507d70451f1457185a3e906c640c66
path = extension/tests/qa_browser/real_profile_binding_gate.mjs
blob = 790539464d7f72214a3126c6585aac74e1afec39
```

It is one QA-only file above exact product source. Run against the same fresh extraction of exact `ce824a9f...` using Chrome `151.0.7922.47` and Puppeteer `25.4.0`.

Required scenarios/markers:

```text
factual direct conversation id 6a82924e-5ed0-83eb-84a2-851ddad40c88 with late extension install = PASS
trusted canonical direct-conversation identity with live receiver = PASS
Bind = PASS
Manual ON = PASS
ChatGPT DOM stable = PASS
REAL_PROFILE_BINDING_BROWSER_GATE_PASS
REAL_YANDEX_REQUESTS=0
```

## 7. Provider safety / exactly-once requirements

All Search provider activity remains controlled/stubbed. No real credentials and no real Yandex traffic.

The Stage-4 controlled Search scenario must observe exactly:

```text
BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1
```

All governed Search validation, pre-network rejection, cost ledger, XML/Base64 normalization, service isolation, HTTP no-retry, UNKNOWN/no-blind-retry and future-feature locks remain mandatory under the Search addendum.

## 8. Cleanliness / mutation audit

Before final verdict require:

```text
real_credentials_used = NO
real_yandex_requests = 0
production_modified_during_gate = NO
package_tests_modified_during_gate = NO
historical_stage4_harness_modified_during_gate = NO
current_stage4_wrapper_modified_during_gate = NO
repair_browser_harness_modified_during_gate = NO
exact_artifact_modified = NO
source_workspace_clean = PASS
transport_workspace_clean = PASS
historical_harness_workspace_clean = PASS
current_wrapper_workspace_clean = PASS
repair_harness_workspace_clean = PASS
enabled_not_run_sections = 0
```

Installing/removing external QA dependencies must not leave tracked workspace changes at final audit.

## 9. Required complete result

Return exactly one complete report headed:

```text
CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT
```

At minimum include:

```text
campaign: COMPLETE_RERUN_AFTER_STAGE4_HARNESS_RECONCILIATION
live_main_head: <actual>
candidate_source: b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact_sha256: ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
artifact_bytes: 179013
artifact_files: 69
artifact_zip_entries: 72
payload_manifest_sha256: ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
transport_commit: 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
historical_stage4_commit: 667fda2f9a0e4197c4873ea96f27862c8453f2f0
current_stage4_wrapper_commit: 1babfe66222251e2eb63e6e0d4e3eb726ed898e9
current_stage4_wrapper_blob: e1763df3cec988c3bee93efcdd6369eb8c12d695
repair_browser_harness_commit: 81625e073d507d70451f1457185a3e906c640c66
step_0_authority: PASS|FAIL
transport: PASS|FAIL
source_suite: <actual pass>/<total>
packaged_suite: <actual pass>/<total>
source_syntax: <actual pass>/<total>
packaged_syntax: <actual pass>/<total>
source_json: <actual pass>/<total>
packaged_json: <actual pass>/<total>
B01_project_work: PASS|FAIL|NOT_RUN
B02_manual_on_transaction_browser: PASS|FAIL|NOT_RUN
B03_search_autorun: PASS|FAIL|NOT_RUN
PD-00: PASS|FAIL|NOT_RUN
...
PD-17: PASS|FAIL|NOT_RUN
manual_on_transaction: PASS|FAIL|NOT_RUN
S-00: PASS|FAIL|NOT_RUN
...
S-17: PASS|FAIL|NOT_RUN
repair_real_id_late_install: PASS|FAIL|NOT_RUN
repair_canonical_live_receiver: PASS|FAIL|NOT_RUN
controlled_search_stub_requests: <integer>
real_yandex_requests: 0
real_credentials_used: NO
production_modified_during_gate: NO
package_tests_modified_during_gate: NO
historical_stage4_harness_modified_during_gate: NO
current_stage4_wrapper_modified_during_gate: NO
repair_browser_harness_modified_during_gate: NO
final_cleanliness: PASS|FAIL
enabled_not_run_sections: <integer>
failures: [] | [exact failures]
verdict: PASS|FAIL_PRODUCT|FAIL_ARTIFACT|FAIL_HARNESS
```

`PASS` is valid only if the complete campaign from Step 0 passed every enabled section, all three Stage-4 browser scenarios passed through the reconciled venue, both repair-specific browser scenarios passed, the controlled Search stub count is exactly the governed value, no relevant bytes were modified, real credentials were not used, real Yandex requests remained zero, and `enabled_not_run_sections=0`.

On any non-PASS result, return the exact evidence and stop. Do not patch anything.