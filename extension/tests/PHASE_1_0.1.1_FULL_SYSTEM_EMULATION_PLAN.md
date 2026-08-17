# Phase 1 0.1.1 — full-system exhaustive emulation plan

Date: 2026-08-17
Status: PLAN AMENDMENT — define before formal execution.
Authority: owner explicitly ordered a complete functional re-test of the exact final K-02 patched candidate, including every affected dependency, all observable inputs/outputs, environment emulation, failure/race permutations and whole-extension regressions.

## Test object

Exact candidate only:

```text
yandex-marketing-bridge-0.1.1-phase1-k02-generic-dom-patch-candidate.zip
SHA-256: 46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c
files: 42
```

No real Yandex request is permitted in this campaign. Browser tests must map the Yandex API hostname to a local HTTPS mock and record every received request.

## Governing principle

The campaign must not prove only that source lines execute. It must test observable contracts:

```text
input / event / persisted state
→ production extension boundary
→ state transition / side effect
→ exact observable output
```

A PASS requires both the expected positive result and absence of forbidden side effects (duplicate Send, duplicate Yandex request, cross-conversation execution, secret leakage, unexpected persistence, or retry after uncertainty).

Existing 319/319 package tests are a baseline only. New black-box tests must be independent of the production implementation's private expected selector/function assumptions wherever practical.

## FSE-01 Package/runtime identity

- candidate SHA-256 and 42-file inventory;
- manifest/package/runtime version consistency;
- manifest permissions, host permissions, script order and popup/worker/content entrypoints;
- syntax/JSON parsing;
- no missing production file required by manifest.

## FSE-02 Shared-module input/output matrix

Execute exported public functions and boundary values for:

- conversation identity;
- service registry;
- Wordstat protocol parse/validation/build/result formatting;
- autorun model;
- manual controls/locality/profile normalization;
- composer send selection;
- proven writing-block capture;
- cost ledger;
- credential registry;
- policy model;
- run context/product model.

For every accepted input family also test malformed type, missing field, empty value, Unicode/control characters, min/max boundary and over-boundary where meaningful.

## FSE-03 Wordstat protocol/API transport

For all four methods (`getTop`, `getDynamics`, `getRegionsDistribution`, `getRegionsTree`):

- exact valid request URL/method/headers/body;
- Unicode phrase body preservation;
- region/device/result-count filters;
- min/max numeric/date boundaries;
- locally invalid command → zero network;
- missing/invalid credential → zero network;
- HTTP 2xx JSON success;
- HTTP 4xx/5xx error;
- malformed JSON;
- timeout/network failure;
- no automatic retry;
- `request_executed` and `automatic_retry` semantics;
- free vs paid cost/charged semantics;
- result/error envelope secret redaction.

All API calls go to a local HTTPS mock reached by hostname mapping; the mock request counter is the source of truth for exactly-once assertions.

## FSE-04 Worker runtime-message contract

Exercise every `chrome.runtime.onMessage` command exposed by `service_worker.js`, including positive, invalid, missing-context, stale-context, duplicate and race cases. At minimum:

- popup context/binding;
- settings state/global state/toggle patch/save/import/export;
- manual mode/state/execute/delivery complete/fail;
- content ready/sync;
- clear key/test connection;
- report confirmation;
- autorun recovery/start/start commit/start complete/pause/resume/stop/command ready/delivery commit/complete/fail;
- error delivery commit/complete;
- Send/Copy profile get/save/clear;
- diagnostics get/clear/record/content-error.

For each request record exact response object and storage/network/tab-message deltas.

## FSE-05 Popup complete UI contract

In a real Chromium extension popup or equivalent browser runtime:

- every control initializes from storage truth;
- every boolean toggle persists immediately without Save;
- unsaved text/credential fields do not persist;
- Save persists intended text/credential fields only;
- Bind, Test API, clear credential, export/import, picker actions;
- Manual/Autorun mutual exclusion;
- Start/Pause/Resume/Finish and current-run counters/status;
- popup reopen fidelity;
- error/status rendering;
- no popup action can silently issue a Yandex request except explicit Test API / execution paths.

## FSE-06 Content-script DOM black-box matrix

Load the real extension in Chromium and vary DOM structure independently from production selector constants.

Command-body families:

- historical writing-block;
- legacy `#code-block-viewer`;
- generic `<pre><code>`;
- nested wrappers around pre/code;
- assistant role on ancestor at different depths;
- section/role attributes independently present/absent;
- extra non-command code blocks;
- empty and multi-code ambiguous blocks;
- history blocks inserted before current tail;
- dynamically inserted block after runtime start.

Copy-control families:

- button inside block;
- sibling toolbar before/after block;
- nested icon/span target;
- `aria-label`, `title`, `data-testid`, visible text and SVG recognition independently;
- delayed Copy insertion;
- multiple equally local candidates;
- generic whole-response Copy;
- role=button/non-button controls;
- custom saved Copy profile;
- no matching Copy.

For each permutation test Manual OFF and ON, initial scan and MutationObserver, route/conversation change, button replacement, native Copy preservation, exactly one Manual admission on rapid repeated clicks, and zero execution for unsupported/ambiguous/non-command/generic-response Copy.

## FSE-07 Content startup/state-order permutations

Specifically vary the order of:

- content runtime start;
- conversation binding availability;
- imported settings availability;
- Manual persisted ON/OFF;
- popup bind/rebind;
- `WS_CONTENT_READY` response;
- explicit `WS_APPLY_MANUAL_MODE` push;
- Copy block existing before/after state sync;
- extension/page reload.

Acceptance: if authoritative worker state says the current bound conversation has Manual ON, every currently supported eligible command block becomes armed after synchronization regardless of safe ordering; stale/different conversation must fail closed.

## FSE-08 Manual end-to-end

Through real content script + real worker + local API mock:

- local Copy remains native Copy;
- supported valid command generates exactly one request and one delivery;
- non-command and unsupported command behavior;
- double/multi-click in-flight dedup;
- Auto Send ON/OFF;
- Send target delayed/missing/replaced;
- pre-commit delivery failure preserves result without API replay;
- post-commit recovery is reconciliation-only;
- worker/page reload at each durable phase;
- Debug OFF/ON error-to-chat behavior and redaction.

## FSE-09 Autorun end-to-end

Through popup/content/worker/local API mock:

- explicit Start → exactly one committed browser send → waiting state;
- stable assistant block detection;
- exactly one command grant/request/delivery;
- duplicate mutation/watcher events do not duplicate request;
- Pause waiting vs deferred during request/delivery;
- Resume same run/counters;
- Finish immediate/deferred;
- duplicate tab ownership;
- owner-tab disappearance/rebind;
- service-worker restart in waiting/requesting/delivering;
- unknown request outcome no retry;
- report-prefix N=1 and N>1 accounting;
- recoverable error continuation.

## FSE-10 Persistence/import/export/security

- same-install reload;
- cross-install import/export checksum/tamper;
- active run preservation;
- conversation-specific manual/prefix/binding restoration;
- no credentials in diagnostics/result/error/tab messages/ChatGPT-facing text;
- backup contains secrets only where explicitly designed;
- unknown extra import fields cannot mutate execution policy unexpectedly.

## FSE-11 Concurrency/race stress

Run deterministic repeated races (minimum 50 iterations each where applicable):

- concurrent start commits;
- concurrent delivery commits/completions;
- concurrent command-ready events;
- rapid local Copy events;
- worker restart around irreversible boundaries;
- content-ready from owner and duplicate tab concurrently;
- popup toggle/save overlapping state writes.

Acceptance: exactly-once irreversible actions and deterministic persisted state.

## FSE-12 Full-package regression and evidence

After black-box campaign:

- rerun entire built-in suite from fresh extraction;
- record branch/line/function coverage limitations honestly;
- syntax/JSON checks;
- Chromium extension load/pack check;
- deterministic archive comparison if package is rebuilt;
- produce machine-readable result inventory with every FSE case, input, expected, actual, network count and status.

## Stop / patch rule

Do not patch production while this exhaustive campaign is discovering failures. Record every FAIL/BLOCKED/TEST ERROR first. After the campaign, derive one minimal patch set from demonstrated failures only. If a failure is caused by the test harness, classify it TEST ERROR and correct the harness before rerun.
