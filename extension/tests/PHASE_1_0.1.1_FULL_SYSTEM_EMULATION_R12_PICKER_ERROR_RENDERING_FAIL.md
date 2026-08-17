# FSE R12 — popup Send/Copy picker error rendering

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **FAIL — 2/2 negative picker actions surface as rejected async handlers instead of user-visible popup errors.**

Two independent popup actions were exercised with normal popup context resolution followed by a content/tab transport failure only at the picker request.

## R12-1 — Send picker

Input:

```text
pickSend click
WS_PAGE_CONTEXT succeeds
WS_START_SEND_BUTTON_PICKER tab transport fails
```

Actual:

```text
popup handler rejects with: forced tab send error: WS_START_SEND_BUTTON_PICKER
no normal success status is rendered
error escapes the async event handler
```

## R12-2 — Copy picker

Input:

```text
pickCopy click
WS_PAGE_CONTEXT succeeds
WS_START_COPY_BUTTON_PICKER tab transport fails
```

Actual:

```text
popup handler rejects with: forced tab send error: WS_START_COPY_BUTTON_PICKER
no normal success status is rendered
error escapes the async event handler
```

Runner:

```text
2 tests
0 PASS
2 FAIL
```

Production cause:

- both picker callbacks are wrapped with `busy(button, async () => ...)`;
- both correctly inspect `response.ok` and throw on a failed content acknowledgement;
- however `busy()` has only `try/finally`, no `catch`/status rendering, and the two picker handlers have no local `try/catch`;
- therefore the failure becomes an unhandled rejected async event callback instead of a controlled popup error/status message.

This differs from the R9 Manual defect: picker handlers do not falsely report success after a failed acknowledgement; they fail noisily without proper popup error UX.

No production patch was made. No real/external Yandex request occurred.
