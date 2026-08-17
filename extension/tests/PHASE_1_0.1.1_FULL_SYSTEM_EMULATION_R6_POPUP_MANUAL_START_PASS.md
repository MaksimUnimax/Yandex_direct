# FSE R6 — popup / Manual / Start / prefix / reference-UI regression

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **PASS — 41/41**.

```text
41 tests
41 PASS
0 FAIL
```

Covered:

- Manual exists, defaults OFF and is conversation-scoped;
- worker rejects Manual execution while OFF;
- initial five-block tail and content-agnostic arming;
- Yandex-yellow Manual Copy visual contract;
- whole-response Copy excluded while local code/writing Copy supported;
- native Copy preserved;
- Manual OFF disconnects observer/restores styling;
- popup boot/current binding/state rendering;
- runtime/tab transport success, empty-response, runtime-error and missing-context branches;
- global/conversation save-refresh-status-busy paths;
- every popup button/change/input handler invoked;
- diagnostics filters, copy/download paths;
- confirmation-negative destructive-action fences;
- popup context transport failures;
- durable Manual operation blocks Start/Resume independently of the toggle;
- Manual handler failures;
- Bind/Test/Start backend rejection branches;
- PR-02/PR-03 immediate toggle persistence and Start availability before full Save;
- exact reference toast renderer and no invented YMB plaque label;
- configurable/default Start prompt requirements;
- fresh-price / one-command-one-request / no-batching start-prompt contract;
- report-prefix excluded from Start and retained only for API results;
- Start content commit → click-until-empty boundary;
- Start worker confirmation and composer-empty completion gate.

No real/external Yandex request occurred.
