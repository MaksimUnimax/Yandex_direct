# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH = LIVE PASS / CLOSED — LIFECYCLE BUTTON PATCH = FROZEN / CODEX READY — PHASE 3 WEBMASTER QUEUED AFTER PATCH GATE**  
Updated: 2026-08-26

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_THIS_STATE_WRITE = 5edf5a0895f2550d2a9714222986553d66ea4367
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
LIFECYCLE_PATCH_ZIP_INTEGRITY = PASS
LIFECYCLE_PATCH_DETERMINISTIC_REBUILD = PASS / BYTE_IDENTICAL
LIFECYCLE_PATCH_FOCUSED_TESTS = 14/14 PASS
LIFECYCLE_PATCH_SOURCE_SUITE = 247/247 PASS
LIFECYCLE_PATCH_EXACT_TRANSPORT = PASS
LIFECYCLE_PATCH_BROWSER_PREFLIGHT = PASS / NOT INDEPENDENT CODEX EVIDENCE
LIFECYCLE_PATCH_FULL_CODEX_GATE = PENDING
PRODUCTION_BYTES_CHANGED_SINCE_ACCEPTED_GATE = YES
PACKAGE_TEST_BYTES_CHANGED_SINCE_ACCEPTED_GATE = YES
OWNER_HANDOFF_AUTHORIZED = NO
OWNER_LIVE_AUTHORIZED = NO
OPEN_BLOCKERS = independent Codex complete applicable gate only
AUTHORIZED_NEXT_STAGE = INDEPENDENT_CODEX_COMPLETE_APPLICABLE_GATE_ON_EXACT_0430463E_ARTIFACT
AFTER_PATCH_PASS = PHASE_3_WEBMASTER_GOVERNED_REQUIREMENT_RECONSTRUCTION
```

## Accepted Phase-2 baseline

Phase 2 synchronous Search first slice remains **LIVE PASS / CLOSED** on the previously accepted exact artifact:

```text
yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes = 179013
files = 69
ZIP entries = 72
```

Existing Phase-2 evidence remains authoritative for those old bytes:

```text
extension/tests/PHASE_2_REAL_PROFILE_BINDING_CODEX_COMPLETE_PASS_2026-08-25.md
extension/tests/PHASE_2_REAL_PROFILE_OWNER_LIVE_SEARCH_PASS_2026-08-25.md
extension/tests/PHASE_2_OWNER_FUNCTIONAL_LATEST_CHECKPOINT.md
```

Owner Manual Search functional testing is complete. No further repetitive owner Search API validation is required.

## Lifecycle guard button patch — frozen candidate

Owner testing exposed that the backend correctly rejected a new Manual action during:

```text
MANUAL_OPERATION_ACTIVE
DELIVERY_IN_PROGRESS
```

but the Bridge-owned `Яндекс` action could still be clicked. The frozen patch enforces:

```text
blocking lifecycle active
-> existing action stays present but disabled/non-clickable
-> blocked UI click cannot dispatch WS_EXECUTE_MANUAL_BLOCK
-> backend admission guards remain fail-closed
-> authoritative lifecycle/outbox clear is positively observed
-> action becomes clickable again
```

The patch does not reset worker/delivery timers, Manual mode, binding, Autorun state, provider state or popup geometry.

Exact source delta from the accepted Phase-2 source is one commit and exactly two files:

```text
extension/src/content_script.js                         +40 / -2
extension/tests/content_phase2_runtime.test.mjs         +35 / -0
```

Exact candidate source:

```text
branch = candidate/lifecycle-button-gating-2026-08-25
commit = 939e880f820e52beae9dcbcedc86d5cd9e13b075
parent = b7869180c229356a6b3d51ac980ec3da5df4c23c
```

Exact frozen artifact:

```text
yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
SHA-256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
bytes = 179877
files = 69
ZIP entries = 72
ZIP integrity = PASS
deterministic independent rebuild = byte-identical PASS
```

Durable freeze evidence:

```text
extension/tests/LIFECYCLE_BUTTON_GATING_FREEZE_2026-08-26.md
```

## Exact transport — PASS

The frozen ZIP has been published through the proven text-safe exact-ZIP B64 route and consumed again from a fresh clone.

```text
transport branch = qa/lifecycle-button-gating-exact-transport-2026-08-26
transport commit = e11b4f9d5dfb9f5b1bd01bd885151aefdcddc797
transport format = YMB_EXACT_ZIP_B64_TRANSPORT_V1
chunk count = 69
base64 chars = 239836
base64 SHA-256 = a226f87c626659ba16b9f992fc526019c3d3d98702d5655659846b5a8f74e359
fresh consumer artifact SHA-256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
fresh consumer bytes = 179877
fresh consumer files = 69
fresh consumer ZIP entries = 72
ZIP integrity = PASS
byte-identical to frozen target = PASS
```

Durable transport evidence:

```text
extension/tests/LIFECYCLE_BUTTON_GATING_EXACT_TRANSPORT_PASS_2026-08-26.md
```

Transport is therefore no longer an open blocker.

## Installed-extension browser preflight — PASS

A dedicated QA-only harness was added as exactly one file above the frozen candidate source:

```text
branch = qa/lifecycle-button-gating-browser-harness-939e880-2026-08-26
commit = 1009b224d1cfe389f6f041a16cd2a8d53657284a
path = extension/tests/qa_browser/lifecycle_button_gating_gate.mjs
blob = 43739af40d50c35d910752c0cdb1371487393e9a
product bytes in harness delta = 0
package-test bytes in harness delta = 0
```

ChatGPT preflight ran the harness against the exact transported `0430463e...` package using Chrome for Testing `151.0.7922.47` and Puppeteer `25.4.0`.

Required observed markers:

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
CHATGPT_BROWSER_PREFLIGHT_PASS
```

Durable browser preflight evidence:

```text
extension/tests/LIFECYCLE_BUTTON_GATING_BROWSER_PREFLIGHT_2026-08-26.md
```

This is development/preflight evidence only. It proves the mandatory browser venue exists and the frozen candidate reaches the intended behavior, but it does not replace independent Codex execution.

## Development/preflight evidence

```text
fail-first = 11 PASS / 3 expected FAIL on old content bytes
focused patched test = 14/14 PASS
complete source suite = 247/247 PASS
syntax = PASS
GitHub Actions dev run 32919302492 = SUCCESS
exact transport round-trip run 32919877249 = SUCCESS
installed-extension browser preflight run 32920317520 = SUCCESS
real Yandex requests = 0
real credentials = NO
```

GitHub Actions runs are development/preflight only and are **not** independent Codex evidence.

## Mandatory gate authority

Codex must fetch live `main` and use the living authority including:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CURRENT_STATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_NATIVE_ACTION_POPUP_GEOMETRY_ADDENDUM_2026-08-24.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

The Manual-ON authority is consistently:

```text
Manual ON: content acknowledgement first -> worker hard-gate authorization second
Manual OFF: worker OFF first -> content cleanup second
```

The current patch additionally requires the installed-extension browser/runtime regression:

```text
blocked -> action disabled/non-clickable -> no dispatch -> lifecycle clears -> action enabled again
```

Controlled QA must use zero real credentials and make zero real Yandex requests.

## Current authorized next action

```text
1. Independent Codex starts a new complete applicable pre-delivery campaign from Step 0.
2. Codex fetches live main and reconstructs current authority before testing.
3. Codex independently reassembles the exact 0430463e... ZIP from transport commit e11b4f9d...
4. Codex requires exact SHA-256, byte count, ZIP integrity, file count and entry count before product PASS credit.
5. Codex runs source/package/static suites plus every enabled permanent browser/integration section.
6. Codex reruns the dedicated lifecycle_button_gating_gate.mjs against the same exact package.
7. No real credentials and zero real Yandex requests.
8. Owner receives no new artifact before complete Codex PASS with enabled_not_run_sections = 0.
9. After patch PASS/closure, begin Phase 3 Webmaster governed requirement reconstruction.
```

Do not mutate or substitute the frozen `0430463e...` candidate while its gate chain is active. Any product or package-test byte change invalidates this freeze and requires a new exact candidate, exact transport proof and complete applicable gate.