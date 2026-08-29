# KW-001 / OKNO-MSK — STEP 03R S11 PRE-PROVIDER FAILURE

Date: 2026-08-29
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`
Target seed: `S11 алюминиевые окна`
Status: **PRE-PROVIDER FAILURE / SAFE UNCHANGED RETRY**

## Delivered YMB error

```text
bridge = yandex-marketing-bridge
version = 0.1.1
status = ERROR
service = wordstat
channel = manual
stage = COMMAND_DISCOVERY
code = NO_SUPPORTED_COMMAND
message = В выбранном блоке нет поддерживаемой команды Yandex Marketing Bridge.
recoverable = true
request_executed = false
automatic_retry = false
run_id = null
operation = null
autorun_continues = false
timestamp = 2026-08-29T03:25:17.176Z
operation_id = manual-064894a3-4111-46ec-8ea3-687955576234
```

## Provider-execution truth

```text
provider request executed = false
provider outcome = NOT_STARTED
Wordstat request count increment = 0
provider cost increment = 0 RUB
S11 completed = false
S11 batch item consumed = false
```

The failure happened at local `COMMAND_DISCOVERY` before a supported YMB command was identified, so no Wordstat provider call was initiated.

## Recovery decision

The unchanged S11 command may be presented again because `request_executed=false` is explicit. This is not an automatic replay of an uncertain provider request.

Required recovery:

```text
present a clean standalone supported WORDSTAT_BATCH_API_V1 batch.next command
keep ACTIVE SERVICE = Wordstat
keep EXECUTION MODE = Manual
keep MANUAL = ON
keep AUTORUN = OFF
execute only S11
then require full raw + TSV preservation before S12
```

## Non-repeat control

```text
OUTCOME_UNKNOWN = 0
BLIND_PROVIDER_RETRY = false
SAFE_UNCHANGED_RETRY = true
STEP_03R_COMPLETED_ITEMS = 10/18
NEXT_PROVIDER_ITEM = S11 `алюминиевые окна`
NEXT_PROVIDER_ITEM_ALLOWED = true
FORWARD_ANALYTICAL_STEP = BLOCKED
```
