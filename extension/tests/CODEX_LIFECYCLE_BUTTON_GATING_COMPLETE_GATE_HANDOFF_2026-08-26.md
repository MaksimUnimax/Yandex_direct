# Codex handoff — lifecycle button gating complete applicable pre-delivery gate

Status: **READY FOR INDEPENDENT CODEX COMPLETE APPLICABLE GATE / EXACT FROZEN ARTIFACT / OWNER HANDOFF BLOCKED**  
Date: 2026-08-26

Codex is the independent QA executor only. ChatGPT owns product, tests, harnesses, packaging, transport and failure repair.

This is a new complete campaign against the frozen lifecycle-button candidate. Do not transfer final PASS credit from the earlier accepted `ce824a9f...` artifact because production and package-test bytes changed.

## 0. Mandatory campaign rules

Codex MUST NOT:

- edit production code;
- edit package tests;
- edit any governed browser harness or compatibility wrapper;
- weaken, skip, reinterpret or replace assertions;
- substitute a rebuilt/logically equivalent ZIP for the exact transported artifact under test;
- use real Yandex credentials;
- make any real Yandex request;
- patch a product, test, harness or transport failure itself.

Allowed final verdicts:

```text
PASS
FAIL_PRODUCT
FAIL_ARTIFACT
FAIL_HARNESS
```

A PASS requires every enabled applicable section to execute with `enabled_not_run_sections = 0`.

## 1. Reconstruct live authority first

Before any product test, fetch live `main` and read at minimum:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CURRENT_STATE.md
extension/docs/PROJECT_PURPOSE.md
extension/docs/SPECIFICATION.md
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
extension/docs/PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/ROADMAP.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_NATIVE_ACTION_POPUP_GEOMETRY_ADDENDUM_2026-08-24.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
extension/tests/LIFECYCLE_BUTTON_GATING_FREEZE_2026-08-26.md
extension/tests/LIFECYCLE_BUTTON_GATING_EXACT_TRANSPORT_PASS_2026-08-26.md
extension/tests/LIFECYCLE_BUTTON_GATING_BROWSER_PREFLIGHT_2026-08-26.md
this handoff
```

The current Manual-ON authority is:

```text
Manual ON = content WS_APPLY_MANUAL_MODE(true) acknowledgement first
            -> worker WS_SET_MANUAL_MODE(true) hard-gate authorization second
Manual OFF = worker OFF first -> content cleanup second
```

Any stale historical wording that says worker ON first is not current authority.

Required frozen candidate authority:

```text
candidate branch = candidate/lifecycle-button-gating-2026-08-25
candidate source = 939e880f820e52beae9dcbcedc86d5cd9e13b075
candidate parent = b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact filename = yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
artifact SHA-256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
artifact bytes = 179877
artifact files = 69
artifact ZIP entries = 72
owner handoff = BLOCKED pending this gate
owner live = BLOCKED pending this gate
```

Verify `candidate parent..candidate source` is exactly one commit and exactly these two files:

```text
extension/src/content_script.js
extension/tests/content_phase2_runtime.test.mjs
```

Expected diff statistics:

```text
extension/src/content_script.js                 +40 / -2
extension/tests/content_phase2_runtime.test.mjs +35 / -0
```

Any candidate/source authority mismatch is blocking. Do not guess.

## 2. Acquire the exact frozen artifact only through the published B64 transport

Use:

```text
transport branch = qa/lifecycle-button-gating-exact-transport-2026-08-26
transport commit = e11b4f9d5dfb9f5b1bd01bd885151aefdcddc797
transport dir = extension/tests/qa_transport/lifecycle-button-gating
transport format = YMB_EXACT_ZIP_B64_TRANSPORT_V1
```

Checkout/read the transport at exact commit `e11b4f9...`, not a moving branch tip.

Required manifest authority:

```text
candidate_source = 939e880f820e52beae9dcbcedc86d5cd9e13b075
artifact_sha256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
artifact_bytes = 179877
artifact_files = 69
artifact_entries = 72
chunk_chars = 3500
chunk_count = 69
base64_chars = 239836
base64_sha256 = a226f87c626659ba16b9f992fc526019c3d3d98702d5655659846b5a8f74e359
```

Use `transport_manifest.json` as the exact ordered chunk manifest. Verify every chunk's byte count and SHA-256 before concatenation. Concatenate raw chunk bytes in manifest order with no inserted newline, trimming or normalization.

Then require:

```text
joined base64 chars = 239836
joined base64 SHA-256 = a226f87c626659ba16b9f992fc526019c3d3d98702d5655659846b5a8f74e359
base64 decode = strict PASS
decoded ZIP SHA-256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
decoded ZIP bytes = 179877
ZIP test/integrity = PASS
files = 69
ZIP entries including directories = 72
```

Persist that decoded ZIP as the package under test. Fresh-extract it for package/browser tests.

Do not rebuild another ZIP as a substitute. A deterministic rebuild may be checked additionally for reproducibility, but the exact transported `0430463e...` bytes remain the authoritative package under test and eventual owner handoff candidate.

If exact artifact identity does not match, stop product PASS credit and return `FAIL_ARTIFACT`.

## 3. Source and packaged static/test suites

Use a separate clean source workspace at exact candidate source:

```text
939e880f820e52beae9dcbcedc86d5cd9e13b075
```

Run the complete source suite from the candidate's normal extension test entrypoint.

Expected frozen preflight baseline:

```text
source suite = 247/247 PASS
```

Run the focused lifecycle runtime test and require all lifecycle button-gating assertions to pass. Expected preflight baseline:

```text
focused lifecycle test = 14/14 PASS
```

Run all permanent JS syntax and JSON checks required by the living gate. Report actual counts.

Run the complete packaged suite against the fresh extraction of the exact transported `0430463e...` ZIP using the canonical package-suite adapter from exact candidate source. Expected functional count is the same current candidate suite:

```text
packaged suite = 247/247 PASS
```

If counts differ because the runner reports a different denominator, report actual counts and preserve every governed assertion; do not weaken the gate to force the historical number.

## 4. Permanent Phase-2 browser/integration gate remains applicable

This patch changes `content_script.js`, so all existing browser/runtime regression authority that depends on content/worker/popup interaction remains enabled.

Execute every enabled `PD-00..PD-17` section from the living permanent gate, plus the Manual-ON and Search addenda. No enabled `NOT_RUN` is allowed in PASS.

### 4.1 Stage-4 B-01/B-02/B-03 current popup venue

Historical assertions remain immutable authority:

```text
historical commit = 667fda2f9a0e4197c4873ea96f27862c8453f2f0
historical harness = extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_gate.mjs
historical harness blob = 127e6042037ac0cbb044e81b2a9c554f24b5aa6b
TLS key = extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.key.pem
TLS key blob = 2d0ab1f091b119d964a7ebdcd15720f6cd9728ad
TLS cert = extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.cert.pem
TLS cert blob = d91cb127e8d8f6cfa5a95723a15612fd03478af6
```

Current compatibility wrapper:

```text
branch = qa/phase2-current-stage4-browser-harness-b786918-2026-08-25
commit = 1babfe66222251e2eb63e6e0d4e3eb726ed898e9
path = extension/tests/qa_browser/phase2-stage4-current/run_current_stage4_gate.mjs
blob = e1763df3cec988c3bee93efcdd6369eb8c12d695
```

Do not modify historical harness or wrapper. Run them against the fresh extraction of exact `0430463e...` package.

Qualified environment is Chrome for Testing `151.0.7922.47` + Puppeteer `25.4.0` in an isolated QA profile.

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

A wrapper/environment failure after exact artifact establishment is `FAIL_HARNESS`; a failed governed product assertion reached through the current venue is `FAIL_PRODUCT`.

### 4.2 Real-profile binding repair regression remains applicable

Use immutable QA harness:

```text
branch = qa/phase2-real-profile-binding-browser-harness-b786918-2026-08-25
commit = 81625e073d507d70451f1457185a3e906c640c66
path = extension/tests/qa_browser/real_profile_binding_gate.mjs
blob = 790539464d7f72214a3126c6585aac74e1afec39
```

Run it against the same exact extracted `0430463e...` package with Chrome `151.0.7922.47` and Puppeteer `25.4.0`.

Required scenarios include:

```text
factual direct conversation id 6a82924e-5ed0-83eb-84a2-851ddad40c88 with late extension install = PASS
trusted canonical direct-conversation identity with live receiver = PASS
Bind = PASS
Manual ON = PASS
ChatGPT DOM stable = PASS
REAL_PROFILE_BINDING_BROWSER_GATE_PASS
REAL_YANDEX_REQUESTS=0
```

## 5. New mandatory lifecycle-button installed-extension browser regression

Use exactly this QA-only harness:

```text
branch = qa/lifecycle-button-gating-browser-harness-939e880-2026-08-26
commit = 1009b224d1cfe389f6f041a16cd2a8d53657284a
parent = 939e880f820e52beae9dcbcedc86d5cd9e13b075
path = extension/tests/qa_browser/lifecycle_button_gating_gate.mjs
blob = 43739af40d50c35d910752c0cdb1371487393e9a
```

First verify `candidate source..harness commit` is exactly one commit and exactly that one QA-only file. Product bytes and package-test bytes in the harness delta must be zero.

Run the harness unchanged against the same fresh extraction of exact transported `0430463e...` package, with Chrome for Testing `151.0.7922.47` and Puppeteer `25.4.0` in an isolated QA profile.

Required markers:

```text
LIFECYCLE_BUTTON_INITIAL_ENABLED_PASS
LIFECYCLE_MANUAL_OPERATION_DISABLED_PASS
LIFECYCLE_MANUAL_OPERATION_BLOCKED_CLICK_NO_DISPATCH_PASS
LIFECYCLE_MANUAL_OPERATION_CLEAR_REENABLE_PASS
LIFECYCLE_DELIVERY_DISABLED_PASS
LIFECYCLE_DELIVERY_BLOCKED_CLICK_NO_DISPATCH_PASS
LIFECYCLE_DELIVERY_CLEAR_REENABLE_PASS
LIFECYCLE_GATE_PROVIDER_HITS=0
LIFECYCLE_GATE_REAL_YANDEX_REQUESTS=0
LIFECYCLE_BUTTON_GATING_BROWSER_GATE_PASS
```

The governed invariant is:

```text
MANUAL_OPERATION_ACTIVE or DELIVERY_IN_PROGRESS
-> existing Bridge-owned Яндекс action remains present
-> action is disabled/non-clickable
-> blocked click cannot dispatch WS_EXECUTE_MANUAL_BLOCK
-> backend fail-closed guards remain intact
-> authoritative lifecycle/outbox clear is positively observed
-> same action becomes clickable again
```

The test must not reset worker timers, delivery state, Manual mode, conversation binding or Autorun state merely to refresh the button.

## 6. Native popup geometry remains mandatory

The extension popup must remain:

```text
430 x 560
```

Execute the current governed Chrome-151 popup geometry checks from `CODEX_PRE_DELIVERY_NATIVE_ACTION_POPUP_GEOMETRY_ADDENDUM_2026-08-24.md`. No geometry regression is allowed.

## 7. Search/provider safety and exactly-once requirements

All provider behavior in this gate remains controlled/stubbed.

Required:

```text
real_credentials_used = NO
real_yandex_requests = 0
automatic blind retry after UNKNOWN outcome = forbidden
Stage-4 controlled Search stub requests = exactly 1
lifecycle-button harness provider hits = 0
```

All Search validation, service isolation, budget/cost policy, request-limit behavior, XML/Base64 normalization, HTTP failure no-retry, UNKNOWN/no-blind-retry and future-feature locks from the Search addendum remain enabled where mapped by the living gate.

## 8. Cleanliness and immutability audit

Before final verdict require:

```text
exact_artifact_modified = NO
production_modified_during_gate = NO
package_tests_modified_during_gate = NO
historical_stage4_harness_modified_during_gate = NO
current_stage4_wrapper_modified_during_gate = NO
real_profile_binding_harness_modified_during_gate = NO
lifecycle_button_harness_modified_during_gate = NO
real_credentials_used = NO
real_yandex_requests = 0
source_workspace_clean = PASS
transport_workspace_clean = PASS
browser_harness_workspaces_clean = PASS
enabled_not_run_sections = 0
```

Installing external QA dependencies in an untracked/external harness workspace is allowed, but tracked governed workspaces must be clean at final audit.

## 9. Required final result

Return one complete report headed exactly:

```text
CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT
```

At minimum include:

```text
campaign: LIFECYCLE_BUTTON_GATING_COMPLETE_APPLICABLE_GATE
live_main_head: <actual>
candidate_source: 939e880f820e52beae9dcbcedc86d5cd9e13b075
candidate_parent: b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact_sha256: 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
artifact_bytes: 179877
artifact_files: 69
artifact_zip_entries: 72
transport_commit: e11b4f9d5dfb9f5b1bd01bd885151aefdcddc797
lifecycle_harness_commit: 1009b224d1cfe389f6f041a16cd2a8d53657284a
lifecycle_harness_blob: 43739af40d50c35d910752c0cdb1371487393e9a
step_0_authority: PASS|FAIL
transport: PASS|FAIL
source_suite: <actual pass>/<total>
packaged_suite: <actual pass>/<total>
focused_lifecycle_runtime: <actual pass>/<total>
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
native_popup_geometry_430x560: PASS|FAIL|NOT_RUN
lifecycle_button_initial_enabled: PASS|FAIL|NOT_RUN
lifecycle_manual_operation_disabled: PASS|FAIL|NOT_RUN
lifecycle_manual_blocked_click_no_dispatch: PASS|FAIL|NOT_RUN
lifecycle_manual_clear_reenable: PASS|FAIL|NOT_RUN
lifecycle_delivery_disabled: PASS|FAIL|NOT_RUN
lifecycle_delivery_blocked_click_no_dispatch: PASS|FAIL|NOT_RUN
lifecycle_delivery_clear_reenable: PASS|FAIL|NOT_RUN
lifecycle_browser_gate: PASS|FAIL|NOT_RUN
controlled_search_stub_requests: <integer>
lifecycle_provider_hits: <integer>
real_yandex_requests: 0
real_credentials_used: NO
production_modified_during_gate: NO
package_tests_modified_during_gate: NO
historical_stage4_harness_modified_during_gate: NO
current_stage4_wrapper_modified_during_gate: NO
real_profile_binding_harness_modified_during_gate: NO
lifecycle_button_harness_modified_during_gate: NO
final_cleanliness: PASS|FAIL
enabled_not_run_sections: <integer>
failures: [] | [exact failures]
verdict: PASS|FAIL_PRODUCT|FAIL_ARTIFACT|FAIL_HARNESS
```

`PASS` is valid only when the exact transported `0430463e...` artifact passed the entire enabled applicable campaign, all required browser venues passed, lifecycle button gating passed for both blockers and recovery, popup geometry remained 430x560, real credentials were not used, real Yandex requests remained zero, relevant governed bytes remained immutable and `enabled_not_run_sections = 0`.

On any non-PASS result, return the exact evidence and stop. Do not patch anything.