# Phase 2 Stage 4 — Codex complete-gate execution map

Date: 2026-08-24  
Status: **MANDATORY / QA EXECUTION AUTHORITY FOR THE FROZEN PHASE-2 CANDIDATE**

This file closes the executable-coverage-map requirement in `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`. It does not change product bytes or redefine the frozen artifact.

## Exact candidate authority

```text
frozen source commit: 1869d17f3cb64417a07088de18dafa5687c83840
artifact: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
SHA-256: 0f0b035c6bc04da841d549182c3dcea6e7cf10074eddebafdf1c3a4c21c98411
bytes: 170726
files: 65
ZIP entries: 68
payload manifest SHA-256: 1acda380ef8fee4aca255014cdacf48a50059037113ff121bd86c738e4fceea9
```

Primary direct repository mirror for Codex:

```text
branch: qa/phase2-stage4-exact-transport-2026-08-24
transport commit: eee36ff3c5c3ce13682ff6ddbcd85001f410b810
path: extension/tests/qa_transport/phase2-stage4-frozen/
ZIP Git blob: a775218d43d00ee92f174c127f90a629b3837553
```

The same bytes were independently consumer-verified through Actions artifact `9512033721` before this mirror was published. The repository mirror points to the exact binary blob created from those verified bytes.

Before any product test, run:

```text
python extension/tests/qa_transport/phase2-stage4-frozen/verify_exact_artifact.py
```

Required markers:

```text
EXACT_ZIP_IDENTITY_PASS
ZIP_INTEGRITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
```

No reconstruction is authorized when this exact ZIP is available.

## Governing documents

Codex must read, in this order:

1. `extension/docs/WORKFLOW_OPERATING_RULES.md`
2. `extension/docs/CURRENT_STATE.md`
3. `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`
4. `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md`
5. `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md`
6. `extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md`
7. this execution map

The Search addendum `S-15` supersedes the old generic Search lock in parent `PD-16` only for the governed synchronous text Search surface. Webmaster, Metrika, Direct, Search deferred/async, Search image and Search generative remain locked.

## Execution venues

Use only demonstrated venues:

- source/static inspection;
- Node test runner / VM integration;
- controlled network stubs and fault injection already present in the test suite;
- qualified Chrome for Testing + Puppeteer installed-extension runtime;
- package extraction/identity checks.

Qualified browser baseline:

```text
Chrome: D:\codex\Test\qa-harness\puppeteer-extension-qa\chrome\win64-151.0.7922.47\chrome-win64\chrome.exe
Chrome version: 151.0.7922.47
Puppeteer: 25.4.0
mode: headful
profile: isolated QA profile
```

Browser-owned assertions must not be replaced by source review.

## Common source/package commands

Frozen source checkout:

```text
git checkout 1869d17f3cb64417a07088de18dafa5687c83840
cd extension/src
npm test
```

The complete source suite is the `package.json` command `node --test ../tests/*.test.mjs` and must include every root-level frozen `*.test.mjs` file.

For the exact extracted ZIP, from its package root run:

```text
node --test tests/*.test.mjs
```

Also parse/check every JS/MJS and both `manifest.json` and `package.json`. Do not edit production or tests during the gate.

## Browser scenarios

### B-01 — installed extension / Project-Work route baseline

Use frozen-source script:

```text
extension/tests/qa_transport/phase2-candidate/browser_project_route_smoke.mjs
```

Run it with the qualified Chrome executable, exact extracted extension root, and the controlled local HTTPS key/cert used by the established QA harness. It must prove MV3 worker loading, content identity on `/g/.../c/<uuid>`, real popup initialization, enabled controls and zero Search-provider hits.

### B-02 — mandatory real-popup Manual ON transaction

Execute **exactly** the 12-step installed-extension scenario in `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md`:

```text
worker Manual OFF + content Manual OFF
→ eligible current PRE/readonly-CodeMirror block
→ real popup Manual ON
→ worker authoritative state ON before content apply
→ content re-sync remains ON
→ exactly one external Яндекс action remains connected/ready
→ ordinary mutation/resync does not self-revert
→ popup reopen remains ON
→ real popup OFF removes Bridge action
→ second real popup ON remains armed
→ real Yandex requests = 0
```

Forbidden substitutes: internal `applyManualMode`, preseeded content ON, popup mock, synthetic direct worker/content shortcuts.

### B-03 — installed Autorun/operator lifecycle

With the same controlled ChatGPT fixture and real popup, execute parent `PD-10` plus Search `S-11`: select `search` while idle, create exactly one RUN, verify WAITING_COMMAND, controlled command pickup without native Copy, stubbed provider initiation at most once, exactly-once result/error delivery, popup reopen truth, Pause/Resume/Finish, owner-tab/conversation isolation and worker reload/recovery. Use deterministic integration tests listed below for crash states that are not reliable to manufacture in the browser. Real Yandex requests must remain 0.

## PD-00…PD-17 mapping

### PD-00 — authority/freeze/exact identity

Venue: repository + package identity.  
Evidence: frozen checkpoint, transport manifest, exact ZIP verifier, source commit `1869d17...`, artifact `0f0b...`.

### PD-01 — complete source regression

Venue: Node.  
Execute the complete frozen source suite, all root `extension/tests/*.test.mjs`; require 0 fail/skip/cancel unless explicitly governed.

### PD-02 — syntax/static/manifest integrity

Venue: source/static + Node.  
Primary coverage: `candidate_readiness_recovery.test.mjs`, `permission_scope_recovery.test.mjs`; parse every JS/MJS, `manifest.json`, `package.json`; verify entrypoints/resources and host permissions.

### PD-03 — exact package/reproducibility/package suite

Venue: exact ZIP/package.  
Use `verify_exact_artifact.py`, full 65-row manifest, frozen checkpoint and deterministic freeze evidence; run complete `tests/*.test.mjs` from exact extracted ZIP plus syntax/JSON checks. Do not substitute a rebuilt ZIP for the primary exact artifact.

### PD-04 — MV3 installation/lifecycle

Venue: browser B-01 + deterministic recovery.  
Coverage: B-01, `conversation_identity_project_routes_recovery.test.mjs`, `popup_project_route_integration_recovery.test.mjs`, `autorun_start_restart_recovery.test.mjs`, `manual_request_restart_recovery.test.mjs`.

### PD-05 — popup/settings

Venue: browser B-02/B-03 + Node.  
Coverage: `popup_phase2_runtime.test.mjs`, `popup_error_boundary_recovery.test.mjs`, `settings_backup_integrity_recovery.test.mjs`, `settings_security_recovery.test.mjs`, `button_picker_recovery.test.mjs`, `start_prompt_and_prefix_recovery.test.mjs`, `auto_start_prompt_tab_control_recovery.test.mjs`.

### PD-06 — external Manual action / DOM binding

Venue: browser B-02 mandatory + Node.  
Coverage: B-02, `content_phase2_runtime.test.mjs`, `button_picker_recovery.test.mjs`, `manual_off_safety_recovery.test.mjs`. Verify native Copy independence, same external action identity across Copy lifecycle, mutation discovery, no duplicates and stable top-right plaques.

### PD-07 — Manual full-block content→worker

Venue: deterministic integration + B-02 admission surface.  
Coverage: `content_phase2_runtime.test.mjs`, `manual_block_sequence_recovery.test.mjs`, `search_manual_worker.test.mjs`.

### PD-08 — Wordstat all Phase-1 operations

Venue: controlled Node/network stubs.  
Coverage: `phase1_core_regression_recovery.test.mjs`, `wordstat_core_recovery.test.mjs`; all `getTop`, `getDynamics`, `getRegionsDistribution`, `getRegionsTree` contours.

### PD-09 — policy/credentials/cost/accounting

Venue: controlled Node/network stubs.  
Coverage: `phase1_core_regression_recovery.test.mjs`, `search_worker_stage2.test.mjs`, `search_manual_worker.test.mjs`, `manual_request_restart_recovery.test.mjs`, `autorun_recovery.test.mjs`.

### PD-10 — Autorun lifecycle

Venue: browser B-03 + deterministic integration.  
Coverage: `autorun_recovery.test.mjs`, `autorun_owner_controls_recovery.test.mjs`, `autorun_start_restart_recovery.test.mjs`, `autorun_transport_retry_recovery.test.mjs`, `runtime_outbox_admission_recovery.test.mjs`, `service_context_owner_control_recovery.test.mjs`, `service_context_owner_lock_recovery.test.mjs`, `manual_paused_run_owner_fence_recovery.test.mjs`.

### PD-11 — Manual delivery FSM/durability/duplicate prevention

Venue: deterministic content↔worker integration + B-02.  
Coverage: `manual_delivery_lifecycle_recovery.test.mjs`, `content_phase2_runtime.test.mjs`, `manual_request_restart_recovery.test.mjs`, `manual_off_safety_recovery.test.mjs`, `content_error_delivery_recovery.test.mjs`, `runtime_outbox_admission_recovery.test.mjs`, `search_manual_worker.test.mjs`.

### PD-12 — Debug/error/redaction

Venue: Node/integration.  
Coverage: `diagnostics_popup_recovery.test.mjs`, `settings_security_recovery.test.mjs`, `content_error_delivery_recovery.test.mjs`, `search_manual_worker.test.mjs`.

### PD-13 — conversation/tab/owner isolation

Venue: Node/integration + B-01/B-03.  
Coverage: `binding_recovery.test.mjs`, `conversation_fences_recovery.test.mjs`, `conversation_identity_project_routes_recovery.test.mjs`, `autorun_owner_controls_recovery.test.mjs`, `manual_mode_owner_control_recovery.test.mjs`, `manual_paused_run_owner_fence_recovery.test.mjs`.

### PD-14 — export/import/migration/persistence

Venue: Node + popup.  
Coverage: `settings_backup_integrity_recovery.test.mjs`, `settings_security_recovery.test.mjs`, `legacy_profiles_recovery.test.mjs`, `popup_phase2_runtime.test.mjs`.

### PD-15 — security/provider containment

Venue: source/static + controlled network.  
Coverage: `permission_scope_recovery.test.mjs`, `settings_security_recovery.test.mjs`, `search_protocol.test.mjs`, `search_worker_stage2.test.mjs`, `candidate_readiness_recovery.test.mjs`.

### PD-16 — phase locks after Search enablement

Venue: source/integration.  
Apply Search addendum `S-15`: governed synchronous text Search is enabled and must be functionally tested. `search_protocol.test.mjs`, `permission_scope_recovery.test.mjs`, service registry/core coverage must prove zero provider execution for Webmaster, Metrika, Direct and Search deferred/image/generative surfaces.

### PD-17 — final cleanliness/evidence

Venue: repository + artifact.  
Re-run exact ZIP verifier; re-hash artifact; compare all 65 payload rows; require clean source/test working state; production/tests modified during gate = NO; real Yandex requests = 0; every PD and S section explicit; emit final Markdown + JSON reports.

## Search S-00…S-17 mapping

### S-00
Authority docs: `PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md`, `SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md`, frozen current state.

### S-01
`search_registry.test.mjs`, `search_worker_stage2.test.mjs`, `phase1_core_regression_recovery.test.mjs`, service-context owner/lock tests.

### S-02
`search_protocol.test.mjs` — defaults, enums and validation boundaries.

### S-03
`search_worker_stage2.test.mjs`, `permission_scope_recovery.test.mjs` — exact single POST/provider containment.

### S-04
`search_worker_stage2.test.mjs`, `settings_security_recovery.test.mjs` — credential capability and secret containment.

### S-05
`search_worker_stage2.test.mjs`, `search_manual_worker.test.mjs`, `phase1_core_regression_recovery.test.mjs` — request/RUB policy and conservative accounting.

### S-06
`search_xml.test.mjs`, `search_worker_stage2.test.mjs` — Base64/XML decode and fail-closed contours.

### S-07
`search_xml.test.mjs` — XML normalization fixtures/order/optional fields/entities/highlights/passages.

### S-08
`search_protocol.test.mjs`, `search_worker_stage2.test.mjs`, `search_manual_worker.test.mjs` — `SEARCH_RESULT_V1` truthfulness.

### S-09
`search_worker_stage2.test.mjs`, `search_manual_worker.test.mjs`, `autorun_recovery.test.mjs`, `manual_request_restart_recovery.test.mjs` — HTTP errors, UNKNOWN, no retry, fingerprint fence.

### S-10
`search_manual_worker.test.mjs`, `manual_block_sequence_recovery.test.mjs`, `manual_delivery_lifecycle_recovery.test.mjs`, B-02 — complete Manual Search path through common delivery FSM.

### S-11
B-03 plus `search_worker_stage2.test.mjs`, Autorun owner/recovery/start-restart/transport/outbox tests — complete Search Autorun path.

### S-12
`phase1_core_regression_recovery.test.mjs`, `wordstat_core_recovery.test.mjs` plus common Manual/outbox/settings/owner tests — Phase-1/core preservation.

### S-13
B-03 + `popup_phase2_runtime.test.mjs`, service-context tests, `manual_mode_owner_control_recovery.test.mjs` — operator service controls/persistence.

### S-14
`permission_scope_recovery.test.mjs`, `search_protocol.test.mjs`, `search_worker_stage2.test.mjs` — exact Search provider allowlist and forbidden modes/URLs.

### S-15
`search_protocol.test.mjs` future-method lock plus permission/service-registry coverage. Synchronous text Search enabled; deferred/image/generative Search, Webmaster, Metrika and Direct remain zero-provider locked.

### S-16
PD-03 exact payload manifest + complete source suite + complete packaged suite. Search modules/tests must be byte-identical between source payload and exact ZIP.

### S-17
Final report must include the exact `search_phase2` subsection required by the Search addendum, with every field explicit and `real_yandex_requests: 0`.

## Campaign completion rule

One campaign means:

```text
PD-00..PD-17: every enabled section PASS
S-00..S-17: every mandatory section PASS
Manual-ON addendum: PASS
source suite: 0 failures
packaged suite: 0 failures
real_yandex_requests: 0
production_modified_during_gate: NO
tests_modified_during_gate: NO
```

Any enabled `NOT_RUN` forbids PASS. Continue unrelated safe sections after an ordinary assertion failure so the report contains the complete failure set. Allowed final verdicts only: `PASS`, `FAIL_PRODUCT`, `FAIL_ARTIFACT`, `FAIL_HARNESS`.
