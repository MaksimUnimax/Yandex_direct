# FSE R13 — popup `busy()` negative error-boundary matrix

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **FAIL — 9/9 tested negative actions escape the popup event boundary instead of being rendered as controlled user-visible error state.**

Formal matrix:

```text
9 tests
0 PASS
9 FAIL
```

Failing actions / injected failure:

1. Pause Autorun — current ChatGPT context resolution throws.
2. Resume Autorun — current ChatGPT context resolution throws.
3. Finish Autorun — current ChatGPT context resolution throws after operator confirmation.
4. Clear Send profile — backend returns `ok:false`.
5. Clear Copy profiles — backend returns `ok:false`.
6. Export settings — backend returns `ok:false`.
7. Import settings — backend/validation path rejects.
8. Clear diagnostics — backend returns `ok:false`.
9. Copy diagnostics — clipboard write rejects.

For each case the production async event callback rejected to its caller instead of completing normally with a controlled popup error/status. The representative escaped errors include `forced tabs query error`, `clear send rejected`, `clear copy rejected`, `export rejected`, `import rejected`, `diag clear rejected`, and `clipboard denied`.

Production common cause:

```javascript
async function busy(button, fn) {
  const old = button.textContent;
  button.disabled = true;
  try { return await fn(); }
  finally {
    button.textContent = old;
    button.disabled = false;
    if (lastState) renderState(lastState);
  }
}
```

`busy()` restores the button/UI in `finally` but has no common `catch`. Several handlers intentionally throw when their backend/content action fails and also have no local catch, so those errors become rejected async event callbacks. Handlers that already contain their own `try/catch` (Bind, Save, Test, Start, Reset prompt, toggle handlers, Manual handler) are not this defect class; `loadDiagnostics` also has its own explicit `ok:false` handling.

R12 Send/Copy picker failures are the same common `busy()` error-boundary class and can be repaired by the same governed change. The separate R9 Manual state-commit/content-ack divergence requires its own transactional/reconciliation correction.

No production patch was made. No real/external Yandex request occurred.
