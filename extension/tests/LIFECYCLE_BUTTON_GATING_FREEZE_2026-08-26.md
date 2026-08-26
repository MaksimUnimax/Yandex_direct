# Lifecycle button gating — frozen candidate checkpoint

Date: 2026-08-26  
Status: **FROZEN / PRE-CODEX — independent full gate pending**

## Authority before freeze checkpoint

```text
LIVE_MAIN_HEAD_BEFORE_WRITE = e63fa0a8db63c02cd8025fdc89dfc9bf8795b337
ACCEPTED_PHASE2_SOURCE = b7869180c229356a6b3d51ac980ec3da5df4c23c
CANDIDATE_BRANCH = candidate/lifecycle-button-gating-2026-08-25
CANDIDATE_SOURCE = 939e880f820e52beae9dcbcedc86d5cd9e13b075
CANDIDATE_PARENT = b7869180c229356a6b3d51ac980ec3da5df4c23c
```

The candidate is exactly one commit above the accepted Phase-2 source.

## Exact product delta

GitHub compare `b786918... -> 939e880...` contains exactly two changed files:

```text
extension/src/content_script.js                         +40 / -2
extension/tests/content_phase2_runtime.test.mjs         +35 / -0
```

No service-worker, popup, manifest, policy, protocol, credential, packaging or other product files changed.

Git blob identities:

```text
extension/src/content_script.js
c7ca2f89124359c0f8ea1eb055294692e6c350fd

extension/tests/content_phase2_runtime.test.mjs
e2a50cc89e11bbb0cd9272b76675c838c523fff9
```

SHA-256 / bytes of changed files:

```text
content_script.js
SHA-256 0df23af6ace244c03181486974edef2f8da1a45df469a4b5b7f892c2ecb870d7
bytes 36671

content_phase2_runtime.test.mjs
SHA-256 fdce1098e5da00b36d4936fcbb6b6cc0fd6175e996b8b878a5c755560b13db03
bytes 7157
```

## Patch contract

The existing Bridge-owned `Яндекс` action remains structurally present while Manual mode is ON, but becomes disabled/non-clickable when a new Manual action cannot be admitted because of lifecycle state.

Blocking conditions covered by this patch:

```text
MANUAL_OPERATION_ACTIVE
DELIVERY_IN_PROGRESS
local admission hold between UI click and authoritative worker refresh
```

Required behavior:

```text
blocking lifecycle active
-> existing Yandex action disabled/non-clickable
-> no WS_EXECUTE_MANUAL_BLOCK dispatch from a blocked UI click
-> backend admission guards remain fail-closed
-> authoritative lifecycle/outbox clear is positively observed
-> action becomes clickable again
```

The patch does not reset worker timers, delivery state, Manual mode, conversation binding, Autorun state, popup geometry, credentials or provider policy.

## Development verification

Fail-first regression against the accepted pre-patch content implementation:

```text
11 PASS / 3 EXPECTED FAIL
```

The three new lifecycle-button assertions fail against old bytes as intended.

After patch:

```text
focused content_phase2_runtime.test.mjs = 14/14 PASS
complete source suite = 247/247 PASS
modified JS syntax = PASS
real Yandex requests = 0
real credentials used = NO
```

A GitHub Actions development/preflight run independently applied the exact minimal patch to the accepted source, verified exact expected Git blob identities, ran syntax + focused + complete source tests, and produced the clean candidate commit. This run is **development evidence only, not independent Codex QA evidence**.

```text
dev run id = 32919302492
dev job id = 98029481277
result = SUCCESS
```

## Frozen exact artifact

```text
filename = yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
SHA-256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
bytes = 179877
files = 69
ZIP entries = 72
ZIP integrity = PASS
```

Accepted preimage artifact:

```text
yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes = 179013
files = 69
ZIP entries = 72
```

The archive root name remains the historical Phase-2 package root carried by the accepted artifact; it is intentionally not renamed during this minimal patch freeze.

Archive comparison against the accepted preimage shows exactly two changed payload entries and no added/removed entries:

```text
.../content_script.js
.../tests/content_phase2_runtime.test.mjs
```

Both embedded changed files match the candidate SHA-256 values above.

## Deterministic freeze proof

Two independent local rebuilds using the accepted ZIP as metadata/order authority produced byte-identical output:

```text
rebuild A SHA-256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
rebuild B SHA-256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
bytes identical = YES
ZIP integrity = PASS
files = 69
entries = 72
```

## Gate status

```text
PRODUCTION_BYTES_CHANGED_SINCE_ACCEPTED_GATE = YES
PACKAGE_TEST_BYTES_CHANGED_SINCE_ACCEPTED_GATE = YES
LATEST_FULL_GATE_FOR_THIS_CANDIDATE = PENDING
OWNER_HANDOFF_AUTHORIZED = NO
OWNER_LIVE_AUTHORIZED = NO
AUTHORIZED_NEXT_STAGE = EXACT_ARTIFACT_TRANSPORT_ROUND_TRIP_THEN_INDEPENDENT_CODEX_COMPLETE_GATE
```

The previous `ce824a9f...` Phase-2 PASS remains valid only for the old accepted artifact. It cannot authorize this changed candidate.

Before a Codex prompt is issued, the exact frozen `0430463e...` ZIP must be published through the proven byte-safe transport and read/reassembled back by ChatGPT as a fresh consumer with exact SHA/byte/ZIP proof.
