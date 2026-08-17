# Phase 1 0.1.1 — exhaustive full-system campaign defect register

Date: 2026-08-17
Test object: `yandex-marketing-bridge-0.1.1-phase1-k02-generic-dom-patch-candidate.zip`
SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **DISCOVERY COMPLETE — patch scope may now be derived only from the demonstrated FAIL set below.**

## Controlled PASS inventory

Formal independent/affected controlled batches completed before closing discovery:

```text
FSE R2 pure-module I/O matrix:                 80/80 PASS
FSE R4 Chromium DOM/event matrix:              34/34 PASS
FSE R5 worker/runtime/concurrency:             112/112 PASS
FSE R6 popup/Manual/Start/reference UI:         41/41 PASS
FSE R7 transport/protocol/policy/security:      76/76 PASS
FSE R8 content/delivery/shared/source guards:   90/90 PASS
FSE R10B worker Manual-OFF hard gate:            1/1 PASS
FSE R10C content authoritative sync:             1/1 PASS
-----------------------------------------------------------
formal positive checks above:                  435 PASS
```

Supporting exact-package regression:

```text
fresh original candidate built-in suite:       319/319 PASS
JS/MJS syntax:                                   37/37 PASS
manifest/package JSON:                            2/2 PASS
fresh extraction A ↔ B:                         42/42 byte-identical
original exact extraction ↔ fresh A:            42/42 byte-identical
Chromium pack: exit 0
```

No real/external Yandex request was issued by the exhaustive campaign.

## BLOCKED / TEST ERROR inventory retained as evidence

- R3 real installed-MV3 local browser acceptance: **BLOCKED BY MANAGED CHROMIUM POLICY**, not product failure. `ExtensionInstallBlocklist:["*"]` and `URLBlocklist:["*"]` prevent extension load/navigation in the assistant test machine.
- R1 initial pure matrix: TEST ERROR from invalid test IDs/Autorun field assumptions; corrected R2 80/80 PASS.
- R9A initial Manual apply injection: TEST ERROR because the fault was injected too early at `WS_PAGE_CONTEXT`; corrected R9B/R9C isolate the apply stage.
- R10A/R10B content targeted harness placement/style assertions: TEST ERROR; corrected R10C PASS.

## Demonstrated product FAIL set

### FSE-DEF-07 — Manual desired-state/content-active-state divergence

Evidence: R9B, R9C, R9D; supported by R10B/R10C boundary checks.

Two ON failures are independently demonstrated:

1. `WS_SET_MANUAL_MODE` commits worker/storage ON, then `WS_APPLY_MANUAL_MODE` tab transport fails.
2. Transport succeeds, but content explicitly replies `{ok:true, applied:false}`.

In both cases production popup still renders checkbox ON and says `Ручной режим включён для этого диалога.`

Two OFF failures are independently demonstrated:

1. worker/storage commits OFF, then apply transport fails;
2. content explicitly replies `applied:false`.

In both cases popup says `Ручной режим выключен; observer/listeners и жёлтая декорация сняты.` although controlled content remains stale ON.

Exact production cause:

- `popup.js` commits worker desired state first through `WS_SET_MANUAL_MODE`;
- it then `await`s `tabMessage(... WS_APPLY_MANUAL_MODE ...)` but discards the returned acknowledgement;
- `tabMessage` deliberately represents transport errors as resolved `{ok:false,...}` values;
- popup checks neither `ok` nor `applied` and unconditionally renders success from the worker response.

Safety/repair boundaries already proved:

- R10B: authoritative worker Manual OFF rejects a stale content click with `MANUAL_MODE_OFF`, creates no durable manual operation and produces **0 mocked fetches**;
- R10C: content startup/`WS_CONTENT_READY` authoritative pull correctly applies worker ON and a later worker OFF resync removes Manual state/yellow decoration.

Therefore this is a real popup↔content state-consistency/action-boundary defect, not a demonstrated worker API hard-gate bypass.

It is also a source-proven mechanism capable of producing the same externally visible state class as the owner's real patched-candidate K-02 evidence: popup Manual ON while local Copy is not armed. The existing owner logs do not contain the content apply acknowledgement, so this register does not claim which specific R9 branch occurred in that live instance.

### FSE-DEF-08 — popup async action error boundary is incomplete

Evidence: R12 and R13.

`busy(button, fn)` disables/restores controls in `try/finally` but has no `catch`. Handlers that intentionally throw after a failed backend/content action and do not provide their own local catch escape as rejected async event callbacks instead of controlled popup error/status.

Demonstrated negative actions:

```text
Send picker
Copy picker
Pause Autorun
Resume Autorun
Finish Autorun
Clear Send profile
Clear Copy profiles
Export settings
Import settings
Clear diagnostics
Copy diagnostics clipboard write
```

R12: 2/2 FAIL.
R13: 9/9 FAIL.

Handlers that already own explicit error handling (Bind, Save, Test, Start, Reset prompt, immediate boolean toggles, Manual handler) are not included in this defect class. `loadDiagnostics` also handles its own backend `ok:false` path.

## Existing live mandatory FAIL retained

### K-02 — real-current-Chrome Manual action boundary

Owner evidence on the exact patched candidate remains **FAIL**:

- Manual visibly ON in popup;
- runtime current conversation confirmed/bound;
- supported `WORDSTAT_API_V1` visible;
- local Copy remains ordinary/gray;
- no command click / no new Yandex request.

Controlled generic-DOM tests cannot override this real-current-Chrome result. FSE-DEF-07 provides a newly demonstrated state-divergence mechanism that must be repaired before K-02 is rerun, but K-02 itself remains live-pending after any controlled patch.

## Frozen patch scope derived from this campaign

Allowed production scope for the next patch:

1. `popup.js` Manual transition logic:
   - never claim Manual ON unless current content confirms the matching conversation apply;
   - inspect both transport `ok` and content `applied`;
   - on failed ON acknowledgement, roll worker desired state back to safe OFF and best-effort reconcile content OFF;
   - on failed OFF acknowledgement, retain worker OFF hard safety state but report cleanup/reconciliation failure instead of falsely claiming observer/listener removal;
   - preserve immediate persistence semantics when acknowledgement succeeds;
   - preserve current conversation binding and Manual/Autorun mutual exclusion.
2. `popup.js` common busy/error boundary:
   - convert otherwise-uncaught async action errors to user-visible popup error status while still restoring button/UI state;
   - do not duplicate/overwrite successful status from handlers that already catch/return normally.
3. Tests/evidence only as required to prove the exact demonstrated dependency closure.

Not authorized by this defect set:

- Yandex transport/request/result changes;
- worker Manual hard-gate weakening;
- Autorun ownership/replay/delivery semantics changes;
- credential/policy/cost changes;
- manifest permissions or host expansion;
- additional DOM-selector changes merely because K-02 is still live FAIL.

After this patch, rerun every R9/R12/R13 negative case, R10B/R10C safety/reconciliation checks, the complete popup/worker/content affected regressions, full 319-package suite, fresh package/syntax/JSON/identity gates, and real-current-Chrome K-02 last.
