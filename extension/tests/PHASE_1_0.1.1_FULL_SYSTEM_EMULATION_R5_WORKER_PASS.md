# FSE R5 — worker/runtime/concurrency regression

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **PASS — 112/112**.

Executed the exact packaged production `service_worker.js` with its exact shared dependencies through the worker integration, binding/isolation, single-flight and exhaustive residual-message suites.

```text
112 tests
112 PASS
0 FAIL
```

Covered observable safety and runtime contracts include:

- unbound/manual/Autorun fail-closed paths;
- explicit durable binding, stale popup, cross-conversation isolation and first-bind legacy-manual cleanup;
- owner tab vs conversation identity separation;
- duplicate-tab ownership rejection and dead-owner rebind;
- 2 through 10 concurrent identical command events each collapsing to one Yandex-boundary request and one delivery push;
- concurrent `CONTENT_READY` delivery races;
- manual-operation ownership after Manual OFF, duplicate/concurrent operation handling and restart recovery with no request replay;
- exact worker storage/key/diagnostic/profile primitive success/failure branches;
- settings/manual/prefix/start-prompt state and locking;
- streamed/non-stream response handling, exact Cyrillic transport, API-error/key-error/timeout paths;
- manual execution, watch, owner, start recovery and delivery recovery branches;
- Autorun pause/resume/stop/recoverable-error/test-connection message paths;
- start commit/complete/recovery and command/delivery completion/failure runtime dispatch;
- command grant/ignore/error and delivery attempt/commit/complete matrices;
- binding-corruption guard;
- global popup state/API-key clearing without content context;
- additive Copy-profile fallback, dedup and hard rejection of the 25th unique profile;
- concurrent start commits: exactly one browser-click grant;
- concurrent delivery commits: exactly one browser-click grant;
- concurrent delivery confirmations: sequence/report-prefix advanced exactly once;
- duplicate start confirmation idempotency;
- service-worker session loss during `REQUESTING`: fail closed / no Yandex retry.

This is controlled worker evidence, not a substitute for final real-current-Chrome gates. No real/external Yandex request occurred.
