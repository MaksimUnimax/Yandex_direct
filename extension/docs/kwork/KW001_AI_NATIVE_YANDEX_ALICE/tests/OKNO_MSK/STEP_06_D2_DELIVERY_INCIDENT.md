# KW-001 / OKNO-MSK — STEP 06 D2 DELIVERY INCIDENT

Date: 2026-08-29  
Status: **RECOVERABLE PRE-PROVIDER DELIVERY FAILURE / SAFE TO REPLAY SAME D2 COMMAND**

This file is job-specific and disposable with the OKNO-MSK workspace.

## Attempted frozen request

```text
D2 = остекление балконов
method = getDynamics
period = PERIOD_MONTHLY
fromDate = 2024-08-01T00:00:00Z
toDate = 2026-07-31T23:59:59Z
regions = ["213"]
devices = ["DEVICE_ALL"]
```

## YMB error

```text
status = ERROR
service = wordstat
channel = manual
stage = DELIVERY_SEND_TARGET
code = SEND_BUTTON_NOT_READY
message = Кнопка Send недоступна во время доставки.
recoverable = true
request_executed = false
automatic_retry = false
autorun_continues = false
timestamp = 2026-08-29T01:49:02.431Z
```

## Safety interpretation

The failure occurred before provider execution. Therefore:

```text
Yandex provider request for D2 = NOT EXECUTED
provider cost consumed by this failed delivery = 0
provider outcome uncertainty = NONE
same frozen D2 command may be replayed after the local send-target condition clears
blind replay = FALSE
```

No phrase, date range, region, device or period is changed for the replay.

Marker:

```text
KW001_OKNO_MSK_STEP_06_D2_SEND_BUTTON_NOT_READY = true
KW001_OKNO_MSK_STEP_06_D2_REQUEST_EXECUTED = false
KW001_OKNO_MSK_STEP_06_D2_SAFE_REPLAY = true
```
