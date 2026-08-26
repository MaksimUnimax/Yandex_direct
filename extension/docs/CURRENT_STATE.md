# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH = LIVE PASS / CLOSED — LIFECYCLE BUTTON PATCH = CODEX PASS / OWNER LIVE PENDING — PHASE 3 WEBMASTER QUEUED AFTER OWNER ACCEPTANCE**  
Updated: 2026-08-26

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_THIS_STATE_WRITE = b220c4b70bf1c6cf4eae0449c102c39eeb09f58c

ACCEPTED_PHASE2_SOURCE = b7869180c229356a6b3d51ac980ec3da5df4c23c
ACCEPTED_PHASE2_ARTIFACT = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa / 179013 bytes / 69 files / 72 ZIP entries
ACCEPTED_PHASE2_FULL_GATE = PASS
ACCEPTED_PHASE2_OWNER_LIVE = PASS

LIFECYCLE_PATCH_BRANCH = candidate/lifecycle-button-gating-2026-08-25
LIFECYCLE_PATCH_SOURCE = 939e880f820e52beae9dcbcedc86d5cd9e13b075
LIFECYCLE_PATCH_PARENT = b7869180c229356a6b3d51ac980ec3da5df4c23c
LIFECYCLE_PATCH_ARTIFACT = yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
LIFECYCLE_PATCH_SHA256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
LIFECYCLE_PATCH_BYTES = 179877
LIFECYCLE_PATCH_FILES = 69
LIFECYCLE_PATCH_ZIP_ENTRIES = 72
LIFECYCLE_PATCH_EXACT_TRANSPORT = PASS
LIFECYCLE_PATCH_FULL_CODEX_GATE = PASS
LIFECYCLE_PATCH_OWNER_HANDOFF_AUTHORIZED = YES
LIFECYCLE_PATCH_OWNER_LIVE = PENDING

PRODUCTION_BYTES_CHANGED_SINCE_LATEST_GATE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_LATEST_GATE = NO
OPEN_BLOCKERS = owner real-profile lifecycle-button acceptance only
AUTHORIZED_NEXT_STAGE = OWNER_REAL_PROFILE_LIFECYCLE_BUTTON_ACCEPTANCE_ON_EXACT_0430463E_ARTIFACT
AFTER_OWNER_PASS = PHASE_3_WEBMASTER_GOVERNED_REQUIREMENT_RECONSTRUCTION
```

## Accepted Phase-2 baseline

Phase 2 synchronous Search first slice remains **LIVE PASS / CLOSED** on:

```text
yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes = 179013
files = 69
ZIP entries = 72
```

Durable evidence:

```text
extension/tests/PHASE_2_REAL_PROFILE_BINDING_CODEX_COMPLETE_PASS_2026-08-25.md
extension/tests/PHASE_2_REAL_PROFILE_OWNER_LIVE_SEARCH_PASS_2026-08-25.md
extension/tests/PHASE_2_OWNER_FUNCTIONAL_LATEST_CHECKPOINT.md
```

Owner Manual Search functional testing is complete. No repetitive Search API validation is required.

## Lifecycle guard button patch — exact tested candidate

Owner Search functional testing exposed that backend admission correctly rejected a new Manual action during:

```text
MANUAL_OPERATION_ACTIVE
DELIVERY_IN_PROGRESS
```

while the Bridge-owned `Яндекс` action could still be clicked.

The patch contract is:

```text
blocking lifecycle active
-> existing action stays present
-> action is disabled/non-clickable before user input
-> blocked click cannot dispatch WS_EXECUTE_MANUAL_BLOCK
-> backend admission guards remain fail-closed
-> lifecycle/outbox clear is positively observed
-> action becomes clickable again
```

The patch must not reset worker/delivery timers, Manual mode, binding, Autorun state, provider state or popup geometry.

Exact source delta from accepted Phase-2 source is one commit and exactly two files:

```text
extension/src/content_script.js
extension/tests/content_phase2_runtime.test.mjs
```

Exact candidate:

```text
branch = candidate/lifecycle-button-gating-2026-08-25
source = 939e880f820e52beae9dcbcedc86d5cd9e13b075
parent = b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact = yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
SHA-256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
bytes = 179877
files = 69
ZIP entries = 72
ZIP integrity = PASS
deterministic rebuild = BYTE_IDENTICAL PASS
```

## Development / transport / browser preflight

```text
fail-first old bytes = 11 PASS / 3 expected FAIL
focused patched runtime = 14/14 PASS
complete source suite = 247/247 PASS
syntax = PASS
exact B64 transport fresh-consumer round-trip = PASS
installed-extension lifecycle browser preflight = PASS
preflight real Yandex requests = 0
preflight real credentials = NO
```

Transport authority:

```text
branch = qa/lifecycle-button-gating-exact-transport-2026-08-26
commit = e11b4f9d5dfb9f5b1bd01bd885151aefdcddc797
format = YMB_EXACT_ZIP_B64_TRANSPORT_V1
chunk_count = 69
base64_sha256 = a226f87c626659ba16b9f992fc526019c3d3d98702d5655659846b5a8f74e359
fresh_consumer_artifact_sha256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
byte_identical = PASS
```

Lifecycle browser harness authority:

```text
branch = qa/lifecycle-button-gating-browser-harness-939e880-2026-08-26
commit = 1009b224d1cfe389f6f041a16cd2a8d53657284a
path = extension/tests/qa_browser/lifecycle_button_gating_gate.mjs
blob = 43739af40d50c35d910752c0cdb1371487393e9a
product_bytes_in_harness_delta = 0
package_test_bytes_in_harness_delta = 0
```

## Independent Codex complete applicable gate — PASS

Codex executed the complete governed campaign against the exact transported `0430463e...` artifact and returned:

```text
campaign = LIFECYCLE_BUTTON_GATING_COMPLETE_APPLICABLE_GATE
step_0_authority = PASS
transport = PASS
source_suite = 247/247
packaged_suite = 247/247
focused_lifecycle_runtime = 14/14
source_syntax = 22/22
packaged_syntax = 63/63
source_json = 2/2
packaged_json = 2/2
B01/B02/B03 = PASS
PD-00..PD-17 = ALL PASS
manual_on_transaction = PASS
S-00..S-17 = ALL PASS
repair_real_id_late_install = PASS
repair_canonical_live_receiver = PASS
native_popup_geometry_430x560 = PASS
lifecycle installed-extension gate = PASS
controlled_search_stub_requests = 1
lifecycle_provider_hits = 0
real_yandex_requests = 0
real_credentials_used = NO
final_cleanliness = PASS
enabled_not_run_sections = 0
failures = []
verdict = PASS
```

Mutation audit:

```text
production_modified_during_gate = NO
package_tests_modified_during_gate = NO
historical_stage4_harness_modified_during_gate = NO
current_stage4_wrapper_modified_during_gate = NO
real_profile_binding_harness_modified_during_gate = NO
lifecycle_button_harness_modified_during_gate = NO
```

Durable evidence:

```text
extension/tests/LIFECYCLE_BUTTON_GATING_FREEZE_2026-08-26.md
extension/tests/LIFECYCLE_BUTTON_GATING_EXACT_TRANSPORT_PASS_2026-08-26.md
extension/tests/LIFECYCLE_BUTTON_GATING_BROWSER_PREFLIGHT_2026-08-26.md
extension/tests/CODEX_LIFECYCLE_BUTTON_GATING_COMPLETE_GATE_HANDOFF_2026-08-26.md
extension/tests/LIFECYCLE_BUTTON_GATING_CODEX_COMPLETE_PASS_2026-08-26.md
```

## Owner real-profile acceptance — pending

The operating contract requires the exact Codex-PASS artifact to be handed to the owner before any irreducible real-profile acceptance.

Owner acceptance is intentionally narrow and should not create extra paid Search traffic solely for testing:

```text
1. Install/use exact 0430463e... artifact.
2. During the next natural Manual lifecycle, observe the Bridge-owned Yandex action.
3. While MANUAL_OPERATION_ACTIVE or DELIVERY_IN_PROGRESS is active, the action must remain visible but disabled/non-clickable.
4. A blocked click must not dispatch another Manual operation.
5. After lifecycle/outbox completion is positively observed, the action must become clickable again without toggling Manual mode or resetting worker timers.
```

If this passes:

```text
LIFECYCLE_BUTTON_PATCH = OWNER LIVE PASS / CLOSED
PHASE_3_WEBMASTER = AUTHORIZED
```

If it fails, preserve exact evidence and reopen only the proven layer.

## Current authorized next action

```text
OWNER HANDOFF exact artifact:
yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
SHA-256 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
179877 bytes / 69 files / 72 ZIP entries

Then perform only the narrow owner real-profile lifecycle-button acceptance above.
```

Do not mutate or substitute the exact `0430463e...` artifact. After owner PASS, update control plane and begin Phase 3 Webmaster governed requirement reconstruction.
