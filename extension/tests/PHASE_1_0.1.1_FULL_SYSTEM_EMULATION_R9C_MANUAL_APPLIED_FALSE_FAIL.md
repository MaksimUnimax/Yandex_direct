# FSE R9C — Manual ON when content explicitly reports `applied:false`

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **FAIL — popup/backend claim Manual ON although current content explicitly says the mode was not applied.**

This is distinct from R9B. Here popup context resolution succeeds, `WS_SET_MANUAL_MODE` succeeds and persists Manual ON, and `WS_APPLY_MANUAL_MODE` reaches the tab successfully. The content-side acknowledgement is deliberately:

```json
{
  "ok": true,
  "applied": false
}
```

Observed final state after the real production popup change handler returns:

```json
{
  "backend_manual_mode": true,
  "popup_checked": true,
  "status": "Ручной режим включён для этого диалога.",
  "tab_apply_attempts": 1
}
```

Runner summary including unchanged popup regressions:

```text
12 tests
11 PASS
1 FAIL
```

Acceptance violation:

- worker desired/persisted state is ON;
- current content runtime explicitly reports that Manual was not applied;
- popup nevertheless presents ON as successful current-runtime truth;
- therefore popup Manual ON is not a reliable proof that local Copy listeners/decorations are active in the content script.

Production cause is the same unchecked acknowledgement boundary demonstrated by R9B: `popup.js` awaits `tabMessage(... WS_APPLY_MANUAL_MODE ...)` but discards its return value and unconditionally renders the successful worker response/status. No check requires `ok === true && applied === true`; there is no rollback or reconciliation after the worker-side state has already been committed.

R9B proves the transport-failure version of this divergence. R9C proves the successful-transport/negative-content-acknowledgement version. Together they establish the defect independently of any DOM-selector hypothesis.

This defect is consistent with the owner's real patched-candidate evidence (popup Manual ON while the local Copy remains gray), but the current live logs do not contain the missing content apply acknowledgement, so this campaign does not claim which of the two R9 paths occurred in that specific live instance.

No production patch was made. No real/external Yandex request occurred.
