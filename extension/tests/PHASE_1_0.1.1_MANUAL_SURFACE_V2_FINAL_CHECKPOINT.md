# Phase 1 0.1.1 — Manual Surface v2 final controlled/package checkpoint

Date: 2026-08-17
Status: **CONTROLLED/PACKAGE PASS; REAL CURRENT-CHROME K-02 STILL REQUIRED. PHASE 1 NOT LIVE PASS.**

## Why this candidate exists

The previous final FSE candidate remained a real-current-Chrome K-02/C-01 FAIL: Manual could be enabled while the visible local code-block Copy stayed native/gray. The owner then froze a new Manual contract and supplied real ChatGPT DOM evidence through the browser agent instead of permitting another selector guess.

The factual current ChatGPT family observed in that probe is:

```text
assistant SECTION
→ assistant message container
→ PRE
→ readonly CodeMirror body ([role="textbox"][aria-readonly="true"][contenteditable="false"])
→ exactly one local Copy BUTTON inside the same PRE
```

The prior current-DOM hypothesis `<pre><code>` was therefore not retained as the primary adapter.

## Final Manual Surface v2 contract implemented

Manual OFF:

- local code-block Copy stays native/ordinary;
- no bridge Manual action is armed.

Manual ON:

- every uniquely bound local assistant code-block Copy is armed regardless of the block text;
- the control is Yandex-yellow and visibly contains the bridge-owned label `Яндекс`;
- native Copy behavior remains intact;
- generic whole-response Copy remains excluded;
- content does not inspect `WORDSTAT_API_V1`, JSON validity, service, credentials, policy or provider state to decide whether to arm the button.

On click:

```text
native Copy
+
whole clicked block capture
→ worker/core
→ structural command discovery
→ service routing
→ strict validation
→ policy / credential / cost gates
→ ordered serial execution
→ durable state / no blind replay
→ one final delivery
```

No supported command and malformed/invalid command cases are worker-owned chat-visible errors/results with zero provider request where no external initiation occurred.

## Main production changes

Production changed only:

```text
content_script.js
service_worker.js
shared/manual_controls.js
shared/wordstat_protocol.js
shared/block_command_discovery.js   (new)
```

`manifest.json` is unchanged. No permission or host-permission expansion occurred.

### Content

- factual PRE/CodeMirror adapter is the primary current ChatGPT code-block family;
- writing-block, legacy `#code-block-viewer`, and generic `<pre><code>` remain compatibility families;
- local Copy mapping is structural and block-local, not command-text-driven;
- all current eligible blocks are rescanned; the old arbitrary latest-five/tail logic is gone;
- `Яндекс` label/style/listener is idempotent and removed/restored exactly on Manual OFF/dispose;
- whole block is sent as `WS_EXECUTE_MANUAL_BLOCK`;
- diagnostics expose scan/binding/decorated counts and reasons.

### Worker/core

- full-block discovery is worker-owned;
- structural marker + balanced JSON extraction supports adjacency, commas, prose/Markdown and Unicode separators without treating a comma as protocol syntax;
- malformed material does not consume later valid markers;
- Phase 1 executes Wordstat only;
- valid items execute strictly serially, max provider concurrency 1;
- identical emitted commands remain distinct queue items;
- completed items are checkpointed and not replayed;
- unknown in-flight outcome stops later initiation and is never blindly retried;
- one clicked block owns one final Manual delivery transaction.

## Dead-code cleanup from execution audit

Changed-line coverage identified and removed four structurally dead/redundant branches rather than retaining untestable defensive clutter:

- impossible negative brace depth after a `{`-anchored balanced-object parse;
- impossible non-object JSON root after successful parsing of a balanced `{...}` object;
- duplicate post-loop UNKNOWN sweep already performed by the serial loop;
- unreachable single-result fallback behind an already-required `single_report_text` condition.

## Verification

Final source-tree regression:

```text
358/358 PASS
0 fail
0 skipped
0 cancelled
```

Changed-production nonblank execution under V8 coverage:

```text
content_script.js                     203/203
service_worker.js                     776/776
shared/block_command_discovery.js     218/218
shared/manual_controls.js               2/2
shared/wordstat_protocol.js            16/16
------------------------------------------------
TOTAL                                1215/1215
uncovered                                      0
```

Fresh deterministic package gates:

```text
deterministic ZIP A == ZIP B:         PASS / byte-identical
source ↔ fresh ZIP:                    45/45 byte-identical
fresh ZIP full suite:                 358/358 PASS
fresh ZIP JS/MJS syntax:               40/40 PASS
fresh ZIP JSON:                          2/2 PASS
manifest required entrypoints:          11/11 present
Chromium --pack-extension:             exit 0
real/external Yandex requests:          0
```

Chromium installed-MV3 acceptance on the assistant machine remains unavailable because of managed browser policy; packing itself passes. Real production ChatGPT acceptance remains an owner-browser gate.

## Final candidate

```text
yandex-marketing-bridge-0.1.1-phase1-manual-surface-v2-candidate.zip
SHA-256: 2f47178892a309f468d3488626b9e1ee6bd9758cbff934d046bf7bd326ce14fe
bytes: 197699
files: 45
```

Production hashes:

```text
content_script.js
03826461d0f8bd7a00ddf653b505d333755002d22a827d9ee286103321f746f4

service_worker.js
4be10f692faf72880fc50abd3f32b97538c14b4c4afc59a9ddd22a48a3ae14c8

shared/block_command_discovery.js
6375736431b06ce7029ea17fae0c64ac35c0adb1972890a97101230473d94434

shared/manual_controls.js
01882215246e8ff5239fec438ef608220161008054a4ea6f5f6bbf1864ecc3b3

shared/wordstat_protocol.js
044f2fb2733a48e915eacc9da01f004c24d083d6a1899812b2074a0d19e7cd85
```

## Reproducible base → final patch

The first patch-materialization attempt was a **TEST ERROR**: ordinary `git diff` omitted the three newly added untracked files. Applying that artifact reconstructed only the original 42 paths and missed:

```text
shared/block_command_discovery.js
tests/block_command_discovery.test.mjs
tests/manual_surface_v2_worker.test.mjs
```

That artifact was discarded.

The corrected patch explicitly includes new files. Applying it to the exact governed base reconstructs the final tree:

```text
45/45 byte-identical PASS
```

Corrected hashes:

```text
raw patch SHA-256:    717b0abb25fc9bbb17ad544ec3eb3ada1eca8d5fe7bf5834fbfde49edaf6f70f
raw bytes:           225938
gzip -n -9 SHA-256:  4b3092a3080fb9c8a3ead7e72af96a4221f231404b8cccc63fa04aeab9820c5a
gzip bytes:           49359
base64 SHA-256:       e0a2483dc6a3a0461a672e95b66b1a68b4ef74b5938c66e7f7da11e44b2dffbc
base64 bytes:         65812
```

Machine evidence:

`extension/tests/PHASE_1_0.1.1_MANUAL_SURFACE_V2_FINAL_EVIDENCE.json`

## Effective gate state

- Controlled/source/package Manual Surface v2: **PASS**.
- K-02 real-current-Chrome visual acceptance on this exact candidate: **NOT RUN**.
- Phase 1: **NOT LIVE PASS**.
- Phase 2 Search: **BLOCKED**.

The next real-browser gate requires **zero Yandex requests**: Manual OFF must show native local Copy; Manual ON must turn every local assistant code-block Copy yellow and visibly label it `Яндекс`, regardless of contents. No Copy click is needed until that visual prerequisite passes.
