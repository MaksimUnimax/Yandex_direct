# Phase 1 0.1.1 — Manual Surface v2 source-tree PASS checkpoint

Date: 2026-08-17
Status: **SOURCE-TREE PASS; PACKAGE/COVERAGE/LIVE GATES STILL PENDING.**

Governed base artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-fse-manual-popup-patch-candidate.zip
SHA-256: f06a16780bed8a1aedb6726c25baaa0667145d4adb14553868b294f95e807cc3
files: 42
```

Authorities:

- `extension/docs/MANUAL_CODE_BLOCK_ACTION_CONTRACT_V2_2026-08-17.md`
- `extension/tests/PHASE_1_0.1.1_MANUAL_SURFACE_V2_PATCH_PLAN.md`
- `extension/tests/PHASE_1_0.1.1_LIVE_CHATGPT_DOM_EVIDENCE_2026-08-17.md`

## Live-DOM implementation target now tested

The current ChatGPT Manual adapter is based on the factual observed family:

```text
assistant SECTION / assistant role container
→ PRE
→ readonly CodeMirror body: [role="textbox"][aria-readonly="true"][contenteditable="false"]
→ one unique local Copy BUTTON inside that PRE
```

Manual visual arming is independent of block text. All unambiguous local code-block Copy controls are Yandex-yellow and receive one bridge-owned `Яндекс` label while Manual is ON. The content script captures the complete clicked block and sends it to worker/core as `WS_EXECUTE_MANUAL_BLOCK`; it does not pre-parse Wordstat commands.

## WIP failure preservation and closure

The first incomplete-refactor full suite was intentionally recorded as:

```text
330 tests
298 PASS
32 FAIL
```

After the full v2 worker/content implementation and after replacing the superseded legacy assertions with executable checks of the same safety responsibilities under the new architecture, the complete source-tree suite now reports:

```text
346 tests
346 PASS
0 FAIL
0 skipped
0 cancelled
```

The old 32 failures were not hidden by deleting their responsibilities. Coverage was transferred to the v2 boundaries, including:

- current PRE/CodeMirror binding plus current-writing/legacy/generic compatibility adapters;
- all-block Manual decoration independent of contents;
- native Copy not prevented;
- complete block capture and worker-owned parsing;
- generic whole-response Copy exclusion;
- ambiguous locality fail-closed;
- full-surface mutation rescan with no arbitrary latest-five tail;
- exact native state restoration on Manual OFF;
- duplicate content admission fence;
- conversation/binding gates before Manual durable claim/provider work;
- chat-visible Manual-OFF/Autorun-active errors instead of unobservable throw-only behavior;
- missing credentials/policy skip with zero provider request;
- paused-RUN request/cost budget sharing;
- invalid credential/provider error semantics;
- Manual operation ownership until delivery completes;
- duplicate/concurrent Manual operation fencing;
- legacy pre-v2 unknown-outcome recovery with no replay;
- v2 checkpointed safe resume versus `request_in_flight` UNKNOWN fencing;
- delivery recovery without provider replay;
- prefix/delivery/source/security guards.

## Current WIP production hashes at this checkpoint

```text
content_script.js
03826461d0f8bd7a00ddf653b505d333755002d22a827d9ee286103321f746f4

service_worker.js
25f6acb35a766016b99f8fdc03ba64485aa004b7e8a894922a8d0243aa8c5e9e

shared/block_command_discovery.js
583f95e536a754316e39ec492fc4928e26c9960018fcac31bba4704286008dc3

shared/manual_controls.js
01882215246e8ff5239fec438ef608220161008054a4ea6f5f6bbf1864ecc3b3

shared/wordstat_protocol.js
044f2fb2733a48e915eacc9da01f004c24d083d6a1899812b2074a0d19e7cd85
```

These are WIP source hashes, not yet a final release identity.

## New explicit v2 test surfaces

Generic structural block-command discovery:

```text
9/9 PASS
```

Dedicated worker Manual Surface v2 matrix:

```text
12/12 PASS
```

Dedicated factual current-ChatGPT content tests cover:

- four arbitrary PRE/CodeMirror blocks all decorated while Manual ON;
- `Яндекс` label exactly once;
- ordinary prose captured whole and submitted to worker without content parse gate;
- generic-response Copy excluded;
- ambiguous PRE Copy fail-closed;
- mutation-added PRE rescanned/decorated;
- repeated rescans do not duplicate labels/listeners;
- Manual OFF restores native inline state exactly.

## Safety

No real/external Yandex request was issued during this implementation/test run. Provider behavior was mocked/emulated.

This checkpoint does **not** declare K-02 or Phase 1 LIVE PASS. Required next work is changed-production execution/coverage audit, syntax/static/security/package identity, deterministic fresh ZIP build, complete suite rerun from fresh extraction, then real-current-Chrome zero-request visual acceptance.
