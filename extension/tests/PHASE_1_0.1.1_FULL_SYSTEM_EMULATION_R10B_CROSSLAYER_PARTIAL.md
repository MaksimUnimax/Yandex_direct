# FSE R10B — cross-layer Manual sync / worker hard gate

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

This batch contains one PASS and one TEST ERROR; they are classified separately.

## R10B-1 — stale content click while authoritative worker Manual is OFF

Status: **PASS**.

Controlled worker input:

- valid bound ChatGPT sender/tab;
- valid `WORDSTAT_API_V1` command;
- API credentials present;
- content is treated as if a stale click handler still emitted `WS_EXECUTE_COMMAND`;
- persisted conversation-scoped Manual state is OFF.

Actual:

```text
executeManualCommand → MANUAL_MODE_OFF
mocked fetch calls: 0
durable manual operation created: no
```

Conclusion: the R9D stale-content UI/listener divergence does not bypass the worker hard gate or reach the Yandex request boundary while authoritative Manual is OFF.

## R10B-2 — persisted worker Manual ON during content startup sync

Status: **TEST ERROR — decoration assertion used the wrong fake-style accessor.**

Actual production state before the bad assertion:

```text
WS_CONTENT_READY manual_mode:true
content manualEnabled:true
observer startup path executed
```

The test then incorrectly asserted `copy.style.backgroundColor`. Production sets the decoration through `style.setProperty("background-color", "rgba(255, 204, 0, 0.22)", "important")`, and the package's FakeStyle implementation exposes it through `style.getPropertyValue("background-color")`. The existing content regression tests use that accessor.

Therefore the failed CSS assertion is harness error, not extension evidence. Corrected rerun must use the package's established style API and also verify authoritative OFF resync removes both Manual state and decoration.

No production patch was made. No real/external Yandex request occurred.
