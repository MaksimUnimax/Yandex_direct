# Phase 2 Stage 4 — Codex complete-gate execution map

Date: 2026-08-24  
Status: **MANDATORY / FINAL QA EXECUTION AUTHORITY FOR THE REFROZEN PHASE-2 CANDIDATE**

This file closes the executable-coverage-map requirement in the living Codex gate. It is QA authority only and does not redefine product bytes.

## Exact candidate authority

```text
frozen source commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
artifact: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
bytes: 170734
files: 65
ZIP entries: 68
payload manifest SHA-256: 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
payload manifest bytes: 11421
```

The old `1869d17... / 0f0b035c...` freeze is superseded historical evidence and is forbidden as the final candidate.

## Exact Codex transport

```text
branch: qa/phase2-stage4-final-b64-transport-0ee1d38-2026-08-24
transport commit: 9dedf7bf624174996fae7efa7a4bdbff6904d348
path: extension/tests/qa_transport/phase2-stage4-final-b64/
format: YMB_PHASE2_STAGE4_FINAL_EXACT_B64_TRANSPORT_V1
source Actions artifact ID: 9515289771
chunks: 16 × 14228 bytes
base64 length: 227648
```

Before any product assertion Codex must fresh-checkout exact transport commit `9dedf7bf...` and run:

```text
python extension/tests/qa_transport/phase2-stage4-final-b64/verify_exact_b64_transport.py
```

Required markers:

```text
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
REAL_YANDEX_REQUESTS=0
```

This route was already independently fresh-consumer verified by GitHub Actions run `32715052351`, job `97394394286`, with `Contents: read`. Codex must still verify its own consumed input before crediting PD-00/PD-03.

## Governing documents

Read in this order:

1. `extension/docs/WORKFLOW_OPERATING_RULES.md`
2. `extension/docs/CURRENT_STATE.md`
3. `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`
4. `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md`
5. `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md`
6. `extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md`
7. `extension/tests/PHASE_2_STAGE_4_PACKAGED_SUITE_ADAPTER_2026-08-24.md`
8. this execution map

Search addendum `S-15` supersedes the generic Search lock in parent `PD-16` only for governed synchronous text Search. Webmaster, Metrika, Direct and Search deferred/async, image and generative surfaces remain locked.

## Demonstrated execution venues

Use only:

- repository/source/static inspection;
- Node test runner / deterministic VM/integration tests;
- controlled network stubs/fault injection already governed by the suite;
- qualified Chrome for Testing + Puppeteer installed-extension runtime;
- exact package extraction and byte-identity checks;
- governed packaged-suite adapter for repository-layout test imports.

Browser-owned assertions must not be replaced by source review.

Qualified browser baseline previously demonstrated:

```text
Chrome for Testing: 151.0.7922.47
Puppeteer: 25.4.0
mode: headful
profile: isolated QA profile
known Windows harness executable:
D:\codex\Test\qa-harness\puppeteer-extension-qa\chrome\win64-151.0.7922.47\chrome-win64\chrome.exe
```

Codex may use the equivalent already-installed qualified path in its environment, but must not replace browser-required assertions with mocks.

## Common exact-source / exact-package execution

### Complete source suite

```text
git checkout 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
cd extension/src
npm test
```

Expected preflight authority: **231/231 PASS**, 0 fail, 0 skipped, 0 cancelled.

### Exact package

Reconstruct the ZIP from transport commit `9dedf7bf...` and keep those exact bytes as the primary artifact under test. Expected identity:

```text
d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
170734 bytes
65 files
68 entries
```

Do **not** run package tests directly as `node --test tests/*.test.mjs` from the installable ZIP root. Repository tests resolve runtime through `../src`; direct invocation is a known invalid venue that produces ENOENT path failures.

Use the governed adapter from source commit `0ee1d38...`:

```text
python extension/tests/qa_transport/phase2-candidate/run_packaged_suite.py \
  --archive <exact-d58b5bd-zip> \
  --manifest <EXACT_CANDIDATE_MANIFEST_2026-08-24.json> \
  --work-dir <fresh-temp-work-dir>
```

The adapter first re-verifies exact ZIP/manifest identity, extracts the exact package, copies runtime/tests byte-identically into a temporary repository-layout harness, re-verifies every staged byte, checks JS/MJS, parses JSON and executes the complete package test suite. It never rewrites the handoff ZIP.

Expected preflight authority:

```text
PACKAGE_EXACT_IDENTITY_PASS
PACKAGED_SUITE_LAYOUT_IDENTITY_PASS
PACKAGED_SYNTAX_PASS count=59
PACKAGED_JSON_PASS count=2
complete packaged tests: 231/231 PASS
PACKAGED_SUITE_PASS files=38
PACKAGED_PREDELIVERY_PREFLIGHT_PASS
```

## Browser scenarios

### B-01 — installed extension / Project-Work route baseline

QA harness:

```text
extension/tests/qa_transport/phase2-candidate/browser_project_route_smoke.mjs
```

Use qualified CfT/Puppeteer with the **exact extracted `d58b5bd...` extension root**. Require MV3 worker load, content identity on `/g/.../c/<uuid>`, real popup initialization, enabled controls and zero Search provider hits.

### B-02 — mandatory real-popup Manual ON transaction

Execute the exact 12-step scenario in the Manual-ON addendum using the installed exact package:

```text
worker Manual OFF + content Manual OFF
→ eligible current PRE/readonly-CodeMirror block
→ real popup Manual ON
→ worker authoritative state ON before content apply
→ content worker re-sync remains ON
→ exactly one external Яндекс action remains connected/ready
→ ordinary mutation/resync does not self-revert
→ popup reopen remains ON
→ real popup OFF removes Bridge action
→ second real popup ON remains armed
→ real Yandex requests = 0
```

Forbidden substitutes: direct internal `applyManualMode`, preseeded content ON, popup mock, direct worker/content shortcut.

### B-03 — installed Search Autorun/operator lifecycle

Using exact package + real popup + controlled ChatGPT fixture:

- active service `search` selected while idle;
- exactly one RUN;
- WAITING_COMMAND;
- controlled Search command pickup without native Copy;
- stubbed provider initiation at most once;
- exactly-once result/error delivery;
- popup reopen truth;
- Pause/Resume/Finish;
- owner-tab/conversation isolation;
- worker reload/recovery;
- Wordstat markers cannot execute in Search RUN;
- real Yandex requests = 0.

Use deterministic integration tests for crash states that are unsafe/unreliable to manufacture in browser.

# PD-00…PD-17 executable mapping

## PD-00 — authority / freeze / exact identity

Venue: repository + artifact identity.  
Evidence: `CURRENT_STATE.md`, exact transport verifier, manifest, source `0ee1d38...`, artifact `d58b5bd...`, freeze run `32714268931`.

## PD-01 — complete source regression

Venue: Node.  
Run every root `extension/tests/*.test.mjs` through `npm test` from exact source. Require all 231 PASS and zero skipped/cancelled unless an explicit governed skip exists.

## PD-02 — syntax/static/manifest integrity

Venue: source/static + Node.  
Coverage includes `candidate_readiness_recovery.test.mjs`, `permission_scope_recovery.test.mjs`; parse/check every JS/MJS and governed JSON; validate manifest entrypoints/resources/permissions/host permissions and no accidental production surface.

## PD-03 — exact package / deterministic reproduction / packaged suite

Venue: exact artifact + governed adapter.  
First run final B64 verifier. Verify the 65-row manifest, ZIP integrity and source-package identity. Deterministic rebuild is additional evidence only and may not replace exact `d58b5bd...`. Run complete packaged suite only through `run_packaged_suite.py` as specified above.

## PD-04 — MV3 installation / lifecycle

Venue: B-01 + deterministic recovery tests.  
Coverage: `conversation_identity_project_routes_recovery.test.mjs`, `popup_project_route_integration_recovery.test.mjs`, `autorun_start_restart_recovery.test.mjs`, `manual_request_restart_recovery.test.mjs`.

## PD-05 — popup/settings

Venue: B-02/B-03 + Node.  
Coverage: `popup_phase2_runtime.test.mjs`, `popup_error_boundary_recovery.test.mjs`, `settings_backup_integrity_recovery.test.mjs`, `settings_security_recovery.test.mjs`, `button_picker_recovery.test.mjs`, `start_prompt_and_prefix_recovery.test.mjs`, `auto_start_prompt_tab_control_recovery.test.mjs`.

## PD-06 — external Manual action / ChatGPT DOM binding

Venue: B-02 mandatory + Node.  
Coverage: `content_phase2_runtime.test.mjs`, `button_picker_recovery.test.mjs`, `manual_off_safety_recovery.test.mjs`. Verify native Copy independence, external action identity through Copy lifecycle, mutation discovery, no duplicates and stable top-right plaques.

## PD-07 — Manual block content→worker

Venue: deterministic integration + B-02 admission surface.  
Coverage: `content_phase2_runtime.test.mjs`, `manual_block_sequence_recovery.test.mjs`, `search_manual_worker.test.mjs`.

## PD-08 — Wordstat all Phase-1 operations

Venue: controlled Node/network stubs.  
Coverage: `phase1_core_regression_recovery.test.mjs`, `wordstat_core_recovery.test.mjs`; `getTop`, `getDynamics`, `getRegionsDistribution`, `getRegionsTree`.

## PD-09 — policy / credentials / cost / accounting

Venue: controlled Node/network stubs.  
Coverage: `phase1_core_regression_recovery.test.mjs`, `search_worker_stage2.test.mjs`, `search_manual_worker.test.mjs`, `manual_request_restart_recovery.test.mjs`, `autorun_recovery.test.mjs`.

## PD-10 — Autorun lifecycle

Venue: B-03 + deterministic integration.  
Coverage: `autorun_recovery.test.mjs`, `autorun_owner_controls_recovery.test.mjs`, `autorun_start_restart_recovery.test.mjs`, `autorun_transport_retry_recovery.test.mjs`, `runtime_outbox_admission_recovery.test.mjs`, `service_context_owner_control_recovery.test.mjs`, `service_context_owner_lock_recovery.test.mjs`, `manual_paused_run_owner_fence_recovery.test.mjs`.

## PD-11 — Manual delivery FSM / durability / dedupe

Venue: deterministic integration + B-02.  
Coverage: `manual_delivery_lifecycle_recovery.test.mjs`, `content_phase2_runtime.test.mjs`, `manual_request_restart_recovery.test.mjs`, `manual_off_safety_recovery.test.mjs`, `content_error_delivery_recovery.test.mjs`, `runtime_outbox_admission_recovery.test.mjs`, `search_manual_worker.test.mjs`.

## PD-12 — Debug/error/redaction

Venue: Node/integration.  
Coverage: `diagnostics_popup_recovery.test.mjs`, `settings_security_recovery.test.mjs`, `content_error_delivery_recovery.test.mjs`, `search_manual_worker.test.mjs`.

## PD-13 — conversation/tab/owner isolation

Venue: Node/integration + B-01/B-03.  
Coverage: `binding_recovery.test.mjs`, `conversation_fences_recovery.test.mjs`, `conversation_identity_project_routes_recovery.test.mjs`, `autorun_owner_controls_recovery.test.mjs`, `manual_mode_owner_control_recovery.test.mjs`, `manual_paused_run_owner_fence_recovery.test.mjs`.

## PD-14 — export/import/migration/persistence

Venue: Node + popup.  
Coverage: `settings_backup_integrity_recovery.test.mjs`, `settings_security_recovery.test.mjs`, `legacy_profiles_recovery.test.mjs`, `popup_phase2_runtime.test.mjs`.

## PD-15 — security/provider containment

Venue: source/static + controlled network.  
Coverage: `permission_scope_recovery.test.mjs`, `settings_security_recovery.test.mjs`, `search_protocol.test.mjs`, `search_worker_stage2.test.mjs`, `candidate_readiness_recovery.test.mjs`.

## PD-16 — phase locks after Search enablement

Venue: source/integration.  
Apply Search addendum `S-15`: governed synchronous text Search is enabled and must execute under controlled stubs. Webmaster, Metrika, Direct and Search deferred/image/generative surfaces must remain zero-provider locked. Coverage: `search_protocol.test.mjs`, permission/service-registry/core tests.

## PD-17 — final cleanliness/evidence

Venue: repository + exact artifact.  
Re-run final B64 verifier; re-hash exact ZIP; compare all 65 manifest rows; require no production/test mutation during campaign; real Yandex requests exactly 0; every PD/S section explicit; emit final Markdown and JSON reports.

# Search S-00…S-17 executable mapping

- **S-00:** `PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md`, `SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md`, `CURRENT_STATE.md`.
- **S-01:** `search_registry.test.mjs`, `search_worker_stage2.test.mjs`, Phase-1 core and service-context tests.
- **S-02:** `search_protocol.test.mjs` defaults/enums/validation boundaries.
- **S-03:** `search_worker_stage2.test.mjs`, `permission_scope_recovery.test.mjs` exact single POST/provider containment.
- **S-04:** `search_worker_stage2.test.mjs`, `settings_security_recovery.test.mjs` credential capability/secret containment.
- **S-05:** `search_worker_stage2.test.mjs`, `search_manual_worker.test.mjs`, Phase-1 core policy/cost accounting.
- **S-06:** `search_xml.test.mjs`, `search_worker_stage2.test.mjs` Base64/XML decode/error contours.
- **S-07:** `search_xml.test.mjs` normalization/order/optional fields/entities/highlights/passages.
- **S-08:** `search_protocol.test.mjs`, `search_worker_stage2.test.mjs`, `search_manual_worker.test.mjs` `SEARCH_RESULT_V1` truthfulness.
- **S-09:** Search worker/manual + Autorun/Manual restart tests for HTTP/UNKNOWN/no-retry/fingerprint fence.
- **S-10:** Search Manual worker + block sequence + Manual delivery + B-02.
- **S-11:** B-03 + Search worker + Autorun owner/recovery/start-restart/transport/outbox tests.
- **S-12:** Phase-1 core/Wordstat + common Manual/outbox/settings/owner regressions.
- **S-13:** B-03 + popup runtime + service-context/manual-mode tests.
- **S-14:** permission scope + Search protocol/worker exact provider allowlist and forbidden surfaces.
- **S-15:** future-method/permission/service-registry locks: sync text Search enabled; deferred/image/generative Search, Webmaster, Metrika, Direct locked.
- **S-16:** PD-03 exact manifest + 231/231 source + 231/231 packaged suite; Search modules/tests byte-identical in artifact.
- **S-17:** final report contains every required `search_phase2` field and `real_yandex_requests: 0`.

# Campaign completion rule

One campaign means:

```text
PD-00..PD-17: every enabled section PASS
S-00..S-17: every mandatory section PASS
Manual-ON transaction addendum: PASS
source suite: 231/231 PASS (or larger only if exact frozen authority itself says so; do not switch candidates)
packaged suite: 231/231 PASS
real_yandex_requests: 0
real_credentials: 0
production_modified_during_gate: NO
tests_modified_during_gate: NO
```

Any enabled `NOT_RUN` forbids PASS. An ordinary assertion failure does not justify skipping unrelated safe sections; collect the complete failure set when possible. Allowed final verdicts only:

```text
PASS
FAIL_PRODUCT
FAIL_ARTIFACT
FAIL_HARNESS
```
