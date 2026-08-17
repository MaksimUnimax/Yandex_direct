# Phase 1 0.1.1 — Manual Surface v2 refactor plan

Date: 2026-08-17
Status: **AUTHORIZED BY OWNER; PLAN FROZEN BEFORE PRODUCTION CHANGE**
Base artifact: `yandex-marketing-bridge-0.1.1-phase1-fse-manual-popup-patch-candidate.zip`
Base SHA-256: `f06a16780bed8a1aedb6726c25baaa0667145d4adb14553868b294f95e807cc3`
Base files: 42

Owner contract authority: `extension/docs/MANUAL_CODE_BLOCK_ACTION_CONTRACT_V2_2026-08-17.md`.

## 1. Why this refactor is authorized

The exact base artifact remains a real-current-Chrome K-02/C-01 FAIL: Manual is enabled, content runtime/conversation are present, but local Copy controls remain gray. The owner then explicitly changed/finalized the desired Manual UX and ordered a clean Ozon-reference-aligned refactor rather than more selector patches.

This owner authorization supersedes the previous FSE defect-register restriction against additional DOM changes. It also supersedes earlier test expectations that non-command local code-block Copy remains gray while Manual ON.

## 2. Reference behavior to preserve/adapt

From live `MaksimUnimax/blood_sand`, branch `work/ozon-data-collection-2026-08-11`, HEAD observed during planning: `50afcc835c5dc374d320dbaeda27062fd5c0f848`.

Reference lessons:

- v0.1.5: Manual content path must not own parser/validation failures that should become observable worker-owned result/error delivery;
- v0.1.9: Manual/Autorun command discovery uses ordered queue semantics, strict serial provider execution, one combined delivery, recovery/no replay;
- v0.1.11: current generic code-block binding, rescanning and decorated-button diagnostics were required after an analogous live gray-Copy failure.

Yandex intentional difference: Ozon v0.1.10 used worker readiness as the blue-state gate; owner requires Yandex Manual visual arming whenever Manual ON + local code-block binding succeeds. Text/protocol validity is not a visual gate.

## 3. Production architecture target

### 3.1 Content Manual surface

Refactor the Manual/Copy portion of `content_script.js` as a generic local-code-block action adapter.

Required behavior:

1. Resolve assistant message/container without looking at command text.
2. Resolve code/writing block bodies structurally.
3. Resolve one unique local Copy control for one block, including toolbar-sibling layouts.
4. Exclude generic assistant response Copy.
5. On Manual ON, decorate every currently eligible local code-block Copy and future eligible controls.
6. Add visible bridge-owned label `Яндекс` while preserving the native Copy icon/content/listener.
7. On Manual OFF/dispose, restore exact native styles/title and remove only bridge-owned label/listener state.
8. On click, do not prevent native Copy; capture the complete block text and submit it to worker/core.
9. No `WordstatProtocol.isCommandText()`/`parseCommand()` gate in the content Manual click path.
10. Emit explicit diagnostics for scan/bind/decorate state and failure counts.

Implementation preference: remove/rewrite obsolete duplicated root-first/manual-tail logic if it obstructs the generic adapter. Do not layer another one-off selector branch on top of the existing K-02 patch.

### 3.2 Worker Manual block processing

Refactor Manual admission so worker receives `block_text` as the authority input.

Required behavior:

1. trusted sender/conversation/binding/manual gates remain first;
2. worker performs command discovery and service routing;
3. no supported command → controlled chat-visible `YMB_ERROR_V1`, `request_executed:false`, zero provider fetch;
4. malformed/invalid command material → controlled worker-owned error/result, zero provider fetch for that item;
5. valid commands execute in source order, max provider concurrency 1;
6. existing policy/credential/cost gates remain per command;
7. completed provider work is persisted before continuing and is not blindly replayed;
8. one clicked block produces one final Manual delivery transaction;
9. Phase 1 executes Wordstat only; future service prefixes cannot cause network side effects.

### 3.3 Wordstat protocol/core

Add structural full-block discovery helpers modeled on the Ozon balanced-object approach:

- find each literal registered marker;
- allow comma/whitespace/prose/Markdown/adjacency as irrelevant separators;
- parse one balanced JSON object after the marker, honoring JSON strings and escapes;
- continue safely to later markers after malformed material;
- keep strict `normalizeCommand()` validation;
- preserve existing single-command parser for Autorun compatibility unless the common batch migration deliberately replaces it with equivalent tested behavior.

### 3.4 Result/error format

Preserve existing `WORDSTAT_RESULT_V1` for one valid command where compatibility permits.

For a clicked block with multiple discovered items, add one structured combined batch delivery format and test it explicitly. Batch format must expose per-item status/request identity/`request_executed` and retain no secrets.

No provider result is sent to ChatGPT between individual requests.

## 4. Explicit non-goals / safety boundaries

Do not:

- add Search/Webmaster/Metrika/Direct provider code in Phase 1;
- add arbitrary URL/method/header execution;
- weaken owner-tab/conversation binding;
- let assistant text enable Manual, raise policy limits or switch Autorun service;
- create provider parallelism;
- introduce blind retry;
- weaken durable delivery/reconciliation;
- expose credentials to content or ChatGPT;
- change manifest permissions/host permissions unless a separately proven requirement exists.

## 5. Mandatory test matrix before candidate release

### A. DOM/action-surface matrix

At minimum test:

- current writing block + internal Copy;
- legacy `#code-block-viewer` + local Copy;
- generic `<pre><code>` + sibling toolbar Copy;
- wrapper with header toolbar + code body;
- code body and Copy appearing in either mutation order;
- multiple code blocks in one assistant turn;
- multiple Copy-like controls where locality is ambiguous → fail closed;
- generic whole-response Copy exclusion;
- non-assistant code/control exclusion;
- Manual OFF → no decoration/bridge handler;
- Manual ON → every unambiguous local code-block Copy decorated regardless of contents;
- `Яндекс` label exactly once per decorated button;
- repeated rescans/rerenders do not duplicate labels/listeners;
- Manual OFF/dispose restores exact native button state;
- native Copy event is not prevented;
- rapid double click creates at most one Manual admission for one armed block while busy.

Content cases while Manual ON must include:

- empty block;
- ordinary prose;
- unrelated JSON;
- malformed Wordstat JSON;
- one valid Wordstat command;
- several valid Wordstat commands;
- valid/malformed/valid sequence;
- marker-like text inside JSON string;
- nested objects/arrays/braces inside strings;
- Unicode separators;
- adjacent commands;
- comma-separated commands.

### B. Worker/block discovery and provider matrix

For each test, assert input, resulting queue, provider fetch count/order/concurrency, durable state and final output.

Required:

- no marker → zero fetch + chat-visible error;
- unknown/future service only → zero fetch + controlled error;
- malformed marker → zero fetch for malformed item;
- valid one command → exactly one logical request;
- valid N commands → exactly N logical requests, strict source order, max concurrency 1;
- identical commands are distinct queue items when deliberately emitted twice;
- validation failure does not execute provider for that item;
- missing credentials/policy denial → zero fetch for denied item;
- HTTP 4xx/5xx → one request, no retry;
- network/timeout unknown outcome → no blind retry;
- recovery after completed item → completed provider request not replayed;
- delivery failure → no provider replay;
- paused RUN Manual budget semantics preserved per accepted command;
- future service prefixes cannot execute during Wordstat-only Phase 1.

### C. Popup/state/recovery regressions

Re-run the complete existing popup Manual transaction/error matrix, content authoritative ON/OFF sync, stale-content worker OFF hard gate, Start/Autorun, delivery recovery and diagnostics.

### D. Full package regression

Required final gates:

- all existing package tests plus new tests PASS;
- every changed production line/function is executed by meaningful runtime tests or explicitly justified unreachable defensive code;
- production JS/MJS syntax PASS;
- JSON parse PASS;
- manifest entrypoints PASS;
- no permission/host-permission expansion;
- deterministic ZIP rebuild byte-identical;
- fresh ZIP extraction byte-identical to staged source;
- complete relevant suite rerun against fresh extracted ZIP;
- Chromium pack smoke PASS where environment permits;
- zero real Yandex requests during controlled patch/testing.

## 6. Live acceptance boundary

Controlled/package PASS cannot close K-02. After the final fresh ZIP passes all gates, the only first owner check required is zero-Yandex-request visual acceptance:

- Manual OFF: local code-block Copy ordinary;
- Manual ON: every local code-block Copy in the supplied test response becomes yellow and visibly says `Яндекс`;
- generic whole-response Copy remains ordinary.

No API command should be clicked until that visual prerequisite passes.
