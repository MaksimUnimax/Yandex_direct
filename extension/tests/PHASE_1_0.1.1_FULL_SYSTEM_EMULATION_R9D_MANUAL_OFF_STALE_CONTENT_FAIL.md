# FSE R9D — Manual OFF content-state reconciliation

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **FAIL — two independent OFF paths leave content stale ON while backend/popup report successful OFF.**

The controlled popup/content boundary model starts from a current content runtime with Manual active. The popup then toggles Manual OFF. `WS_SET_MANUAL_MODE` succeeds first, so authoritative worker/storage desired state becomes OFF. Two apply failures were then tested independently.

## R9D-1 — `WS_APPLY_MANUAL_MODE` transport failure

Observed:

```json
{
  "backend_manual_mode": false,
  "content_manual_mode": true,
  "popup_checked": false,
  "status": "Ручной режим выключен; observer/listeners и жёлтая декорация сняты.",
  "tab_apply_attempts": 1
}
```

## R9D-2 — content acknowledgement `ok:true, applied:false`

Observed:

```json
{
  "backend_manual_mode": false,
  "content_manual_mode": true,
  "popup_checked": false,
  "status": "Ручной режим выключен; observer/listeners и жёлтая декорация сняты.",
  "tab_apply_attempts": 1
}
```

Combined runner summary including unchanged popup regressions:

```text
13 tests
11 PASS
2 FAIL
```

Acceptance violation:

- popup claims not only desired OFF state but specifically claims that observer/listeners/yellow decoration were removed;
- current content runtime can remain stale ON when the apply transport fails or when content explicitly reports `applied:false`;
- production popup ignores both failure classes exactly as in R9B/R9C.

Safety boundary retained:

- worker-side `executeManualCommand` independently rechecks the persisted conversation-scoped Manual state before any request boundary;
- therefore a stale content listener after authoritative worker OFF does not by itself authorize a Yandex request;
- this finding is a state-consistency/UI/action-boundary defect, not evidence of a worker hard-gate bypass.

No production patch was made. No real/external Yandex request occurred.
