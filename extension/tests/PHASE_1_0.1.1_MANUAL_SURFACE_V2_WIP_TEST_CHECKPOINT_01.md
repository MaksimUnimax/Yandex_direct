# Phase 1 0.1.1 — Manual Surface v2 WIP test checkpoint 01

Date: 2026-08-17
Base governed artifact: `yandex-marketing-bridge-0.1.1-phase1-fse-manual-popup-patch-candidate.zip`
Base SHA-256: `f06a16780bed8a1aedb6726c25baaa0667145d4adb14553868b294f95e807cc3`
Live DOM authority: `PHASE_1_0.1.1_LIVE_CHATGPT_DOM_EVIDENCE_2026-08-17.md`.

Status: **WIP / NOT A CANDIDATE / NOT LIVE PASS.**

## Work state tested

The test object is the local refactor worktree derived byte-for-byte from the governed base ZIP before the Manual Surface v2 implementation is complete.

Current production-file SHA-256 values at this checkpoint:

```text
content_script.js                    ee28ae2555cae591381e9f68f092869ce9a2814068092547879ee7137a75ebe6
service_worker.js                    d6b0f094b684350cf6ff063b74c842a175391edc873da570b5b39d7c8b3cc494
shared/block_command_discovery.js    583f95e536a754316e39ec4928e26c9960018fcac31bba4704286008dc3
shared/manual_controls.js            01882215246e8ff5239fec438ef608220161008054a4ea6f5f6bbf1864ecc3b3
shared/wordstat_protocol.js          044f2fb2733a48e915eacc9da01f004c24d083d6a1899812b2074a0d19e7cd85
```

This checkpoint is evidence only; these WIP production bytes are not yet committed as an accepted patch.

## New structural discovery test

A new generic block-command discovery module was executed independently before the full suite.

Result:

```text
9/9 PASS
```

Covered:

- adjacent commands;
- comma/whitespace/prose separators;
- nested objects/arrays;
- braces and marker-like strings inside JSON strings;
- malformed earlier marker followed by a later valid marker;
- missing JSON recovery at a later marker;
- U+00A0/U+200B/U+2060/U+00AD/U+FEFF separators;
- unknown future service marker recognition only when followed structurally by a JSON object;
- marker token boundaries;
- prose-only/no-command input.

## First full-suite run against incomplete refactor

Command:

```text
npm test
```

Actual:

```text
tests:      330
pass:       298
fail:        32
cancelled:    0
skipped:      0
```

This result is intentionally retained rather than rewriting tests until green.

The 32 failures include known superseded expectations from the old Manual contract and current-DOM model, including old `latest five` history/tail semantics, old non-command visual expectations, old generic `<pre><code>` assumptions, old Manual parser/message names, old reference/hash guards and old single-command rejection behavior. They also include worker/content recovery and lifecycle assertions that must be re-proven against the new common block-owned execution engine before release.

No FAIL is being classified as fixed merely by changing an assertion. Each affected behavior must be replaced with an executable test of the owner-directed v2 contract and retained safety invariants.

## Safety

No real Yandex request was issued by this WIP test run. Provider behavior used controlled mocks/emulation.

Phase 1 remains NOT LIVE PASS and Phase 2 remains blocked.
