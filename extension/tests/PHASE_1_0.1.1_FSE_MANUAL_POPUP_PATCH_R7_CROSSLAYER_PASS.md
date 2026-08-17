# FSE Manual/popup patch R7 — cross-layer safety and reconciliation rerun

Date: 2026-08-17
Base candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`
Patched `popup.js` SHA-256: `7286ea024033293110ad10ebc16856de0beacf512f6f86a229ac0271ac20c28c`

Status: **PASS — 45/45** in a disposable full copy of the patched package tree with the two targeted cross-layer tests added without altering production bytes.

Key mandatory results:

1. **Worker hard gate** — a stale content-side Manual click while authoritative persisted Manual is OFF returns `MANUAL_MODE_OFF`, creates no durable Manual operation, and produces **0 mocked fetches**.
2. **Content authoritative pull/reload reconciliation** — persisted worker Manual ON delivered through content-ready sync sets content Manual active and applies the governed yellow local-Copy decoration; a later authoritative worker OFF resync sets content Manual inactive and removes the decoration/observer state.

The remaining 43 passing tests in this targeted run are the worker/content exhaustive helper regressions imported by the cross-layer harnesses, confirming the same worker/content production bytes remain green around the focused checks.

Conclusion:

- the revised popup transaction order keeps worker authorization OFF until content ON is positively acknowledged;
- if content becomes stale after an OFF cleanup failure, the worker hard gate still blocks request execution;
- the existing `WS_CONTENT_READY`/authoritative pull path remains a valid eventual reconciliation mechanism.

No real/external Yandex request occurred.
