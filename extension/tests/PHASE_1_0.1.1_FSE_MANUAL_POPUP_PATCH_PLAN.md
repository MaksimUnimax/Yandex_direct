# Phase 1 0.1.1 — FSE Manual/popup error-boundary patch plan

Date: 2026-08-17
Status: PLAN AMENDMENT — committed before implementation.
Authority: owner explicitly ordered exhaustive whole-function testing and correction of demonstrated defects.
Source defect register: `PHASE_1_0.1.1_FULL_SYSTEM_EMULATION_DEFECT_REGISTER.md`.

## Exact base

```text
yandex-marketing-bridge-0.1.1-phase1-k02-generic-dom-patch-candidate.zip
SHA-256: 46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c
files: 42
```

## Authorized production scope

Only `popup.js` may change in this patch.

### PATCH-FSE-01 — Manual transition acknowledgement/reconciliation

For a popup Manual toggle:

1. resolve and confirm the current ChatGPT context as before;
2. persist worker desired state through `WS_SET_MANUAL_MODE` as before;
3. send `WS_APPLY_MANUAL_MODE` to the same tab/conversation;
4. treat apply success as true only when the returned object has both:
   - `ok === true`;
   - `applied === true`;
5. ON failure after worker commit:
   - roll worker desired state back to OFF;
   - best-effort apply OFF to the current content runtime;
   - render safe OFF state;
   - show explicit error; never display ON success;
6. OFF failure after worker commit:
   - keep worker desired state OFF (hard safety gate remains authoritative);
   - do not claim that content observer/listeners/decorations were removed;
   - show explicit reconciliation error while keeping the checkbox/backend OFF;
7. successful ON/OFF retains existing immediate-persistence UX and exact conversation scoping;
8. no Yandex request or provider action is introduced by state reconciliation.

No worker API hard-gate, content DOM adapter, request, delivery, Autorun, policy, pricing, credential or permission semantic may change.

### PATCH-FSE-02 — common popup async error boundary

`busy(button, fn)` must:

- keep current disable/restore/render-state `finally` behavior;
- catch otherwise-uncaught errors from popup async actions;
- render a user-visible error status instead of leaving an unhandled rejected event callback;
- preserve handlers that already catch/format their own errors;
- never turn a failed action into success;
- include a useful error code when one exists without exposing secrets.

## Mandatory focused regressions

### Manual transition matrix

- ON + apply success → worker ON, content ON, popup ON, success status;
- ON + tab transport failure → worker rolled back OFF, popup OFF, error status;
- ON + `ok:true, applied:false` → worker rolled back OFF, popup OFF, error status;
- OFF + apply success → worker OFF, content OFF, popup OFF, success status;
- OFF + tab transport failure → worker stays OFF, content may remain stale ON, popup OFF, explicit reconciliation error rather than false cleanup-success text;
- OFF + `ok:true, applied:false` → same safe/error behavior;
- stale content click while worker OFF → `MANUAL_MODE_OFF`, zero mocked fetch;
- content authoritative startup/resync ON/OFF remains green.

### Popup error-boundary matrix

Negative failures for all demonstrated actions must complete without rejected event callbacks and show controlled error status:

- Send picker;
- Copy picker;
- Pause;
- Resume;
- Finish;
- Clear Send profile;
- Clear Copy profiles;
- Export settings;
- Import settings;
- Clear diagnostics;
- Copy diagnostics clipboard failure.

Positive action paths must remain green.

## Dependency regression

After focused tests:

- complete existing popup suite;
- worker Manual/binding/concurrency/recovery suites;
- content runtime/Manual DOM suites;
- transport/protocol/security suites;
- export/import/diagnostic suites;
- complete built-in source package suite;
- every changed `popup.js` line executed in controlled runtime or explicitly source-asserted;
- JS/MJS syntax and JSON parsing;
- production file/path inventory unchanged;
- exactly `popup.js` differs from base production bytes;
- fresh deterministic ZIP extraction byte identity;
- Chromium pack succeeds;
- zero real/external Yandex requests.

## Acceptance boundary

A controlled/package PASS does not close K-02. The final candidate must still be installed in real current Chrome and visually prove that Manual ON results in an armed supported local Copy in the owner's actual ChatGPT DOM. If Manual apply cannot be confirmed there, popup must now report a controlled error/OFF state rather than falsely claiming ON.
