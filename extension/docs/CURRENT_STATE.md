# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH = LIVE PASS / CLOSED — LIFECYCLE BUTTON PATCH = FROZEN / PRE-CODEX — PHASE 3 WEBMASTER QUEUED AFTER PATCH GATE**  
Updated: 2026-08-26

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_THIS_STATE_WRITE = bc0f43c49e3e9e15a908ddacba5f2ebcc1533734
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
LIFECYCLE_PATCH_DEV_PREFLIGHT = PASS / NOT INDEPENDENT CODEX EVIDENCE
LIFECYCLE_PATCH_FULL_CODEX_GATE = PENDING
PRODUCTION_BYTES_CHANGED_SINCE_ACCEPTED_GATE = YES
PACKAGE_TEST_BYTES_CHANGED_SINCE_ACCEPTED_GATE = YES
OWNER_HANDOFF_AUTHORIZED = NO
OWNER_LIVE_AUTHORIZED = NO
OPEN_BLOCKERS = exact-artifact transport round-trip + independent Codex complete applicable gate
AUTHORIZED_NEXT_STAGE = EXACT_ARTIFACT_TRANSPORT_ROUND_TRIP_THEN_CODEX_COMPLETE_PRE_DELIVERY_FULL_GATE
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

Development/preflight evidence:

```text
fail-first = 11 PASS / 3 expected FAIL on old content bytes
focused patched test = 14/14 PASS
complete source suite = 247/247 PASS
syntax = PASS
GitHub Actions dev run 32919302492 = SUCCESS
real Yandex requests = 0
real credentials = NO
```

The GitHub Actions run is development/preflight only and is **not** independent Codex evidence.

## Mandatory gate authority

Before Codex execution, use the living authority including:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_NATIVE_ACTION_POPUP_GEOMETRY_ADDENDUM_2026-08-24.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

The Manual-ON authority is now consistently:

```text
Manual ON: content acknowledgement first -> worker hard-gate authorization second
Manual OFF: worker OFF first -> content cleanup second
```

The current patch additionally requires the browser/runtime regression:

```text
blocked -> action disabled/non-clickable -> no dispatch -> lifecycle clears -> action enabled again
```

Controlled QA must use zero real credentials and make zero real Yandex requests.

## Current authorized next action

```text
1. Publish the exact frozen 0430463e... ZIP through the proven byte-safe transport.
2. Read/reassemble it back as a fresh consumer.
3. Require exact SHA-256, byte count, ZIP integrity, file count and entry count.
4. Only after round-trip PASS authorize the independent Codex complete applicable gate.
5. Owner receives no new artifact before Codex PASS.
6. After patch PASS/closure, begin Phase 3 Webmaster governed requirement reconstruction.
```

Do not mutate or substitute the frozen `0430463e...` candidate while its gate chain is active. Any product or package-test byte change invalidates this freeze and requires a new exact candidate/full applicable gate.
