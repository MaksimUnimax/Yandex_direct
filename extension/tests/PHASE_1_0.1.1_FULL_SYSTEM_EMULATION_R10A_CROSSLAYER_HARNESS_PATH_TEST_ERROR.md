# FSE R10A — cross-layer Manual sync targeted harness

Date: 2026-08-17
Status: **TEST ERROR — no production code executed in the intended package layout.**

Purpose was to add two focused cross-layer checks:

1. persisted worker Manual ON must become content Manual ON during startup/content-ready sync, and a later authoritative OFF sync must remove decoration/listeners;
2. a stale content-side Manual click while authoritative worker Manual is OFF must fail with `MANUAL_MODE_OFF` before the mocked fetch boundary.

The first attempt copied existing package test files into `/mnt/data/ymb_fse_browser/`. Those harnesses derive package root from their own `import.meta.url`. Moving them therefore changed the computed root from the exact extracted candidate to `/mnt/data` and produced only filesystem errors:

```text
ENOENT /mnt/data/shared/product.js
ENOENT /mnt/data/service_worker.js
```

Neither result is extension behavior and no acceptance assertion was reached. Corrected rerun must preserve the original `tests/` → package-root relative layout in a disposable full copy of the exact extraction.

No production patch was made. No real/external Yandex request occurred.
