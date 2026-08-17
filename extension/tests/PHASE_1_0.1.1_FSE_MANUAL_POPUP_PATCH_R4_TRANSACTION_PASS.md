# FSE Manual/popup patch R4 — transaction-order revision focused result

Date: 2026-08-17
Base candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`
Plan amendment: `PHASE_1_0.1.1_FSE_MANUAL_POPUP_PATCH_PLAN_AMENDMENT_1.md`

Production scope remains only `popup.js`.

## First revision-2 focused execution

Status: **12/13 PASS, 1 FAIL in the intermediate patch.**

The transaction-order cases themselves reached the new ON content-first / OFF worker-first paths. The single failure was the synchronous worker-commit exception case after content ON had already been applied. The production catch correctly best-effort disarmed content and kept the worker state OFF, but it executed:

```text
status(error)
→ refresh()
```

`refresh()` then replaced the explicit failure text with the ordinary bound-dialog popup status. This was a real error-rendering flaw in the intermediate patch, not a test-harness error.

No external/Yandex request occurred.

## Correction

The Manual catch ordering was changed to:

```text
best-effort content OFF if needed
→ refresh authoritative state
→ render the original failure status last
```

No other production file changed.

## Corrected focused execution

Status: **PASS — 13/13**.

```text
13 tests
13 PASS
0 FAIL
```

The focused Manual transaction matrix now proves:

- ON success: content `applied:true` first, worker ON commit second, popup ON only after both;
- ON content transport failure: worker receives no ON commit, popup OFF/error;
- ON `applied:false`: worker receives no ON commit, popup OFF/error;
- ON content success + worker ON rejection: content is disarmed best-effort, worker stays OFF, popup OFF/error;
- same worker rejection + content cleanup failure: worker remains OFF and popup reports that content OFF is not confirmed;
- synchronous worker-send exception after content ON: content is disarmed, authoritative state refreshed, original error remains visible;
- OFF success: worker OFF first, content OFF second, normal OFF success;
- OFF worker commit rejection: popup returns to ON and does not disarm content or claim OFF;
- OFF content transport failure after worker OFF: popup/worker stay OFF and report reconciliation failure;
- OFF `applied:false` after worker OFF: same safe/truthful state;
- the 11 demonstrated common popup negative actions remain caught by the `busy()` error boundary.

No external/Yandex request occurred.
