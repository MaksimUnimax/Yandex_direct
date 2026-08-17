# FSE R9B — Manual ON content-apply consistency

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **FAIL — production popup can report Manual ON while content never applied Manual mode.**

Corrected fault injection allowed popup context resolution normally, allowed `WS_SET_MANUAL_MODE` to succeed/persist, and failed only the subsequent tab delivery of `WS_APPLY_MANUAL_MODE`.

Runner summary including the unchanged popup regression cases:

```text
12 tests
11 PASS
1 FAIL
```

Exact observed state after the Manual toggle handler finished:

```json
{
  "backend_manual_mode": true,
  "popup_checked": true,
  "status": "Ручной режим включён для этого диалога.",
  "tab_apply_attempts": 1
}
```

Acceptance violation:

- backend/storage has already persisted Manual ON;
- the content-side apply message did not reach the content runtime;
- popup nevertheless renders Manual ON and explicitly tells the operator that Manual mode is enabled;
- therefore the visible popup state does not prove that the current content runtime has installed observer/listeners or yellow Copy decoration.

Production cause is directly in `popup.js`:

```text
const response = await send("WS_SET_MANUAL_MODE", ...)
...
await tabMessage(... "WS_APPLY_MANUAL_MODE" ...)
renderState(response.state)
status("Ручной режим включён ...")
```

`tabMessage()` resolves transport failures as an object `{ok:false, ...}`; it does not reject. The Manual handler ignores the returned object entirely, never checks `ok`, never checks content `applied`, and has no rollback/reconciliation step after worker persistence succeeds.

This defect was not covered by the prior popup suite: the old isolated tab-transport failure test did not combine a successful `WS_SET_MANUAL_MODE` with a failed `WS_APPLY_MANUAL_MODE`, and the old Manual handler failure test failed context resolution before reaching the apply stage.

This controlled defect is consistent with the owner's real patched-candidate symptom (popup Manual ON while local Copy remains gray), but this result alone does not prove that the owner's specific live occurrence was caused by a transport failure rather than an `applied:false` acknowledgement or a separate DOM-binding miss. The next governed check distinguishes those cases.

No production patch was made. No real/external Yandex request occurred.
