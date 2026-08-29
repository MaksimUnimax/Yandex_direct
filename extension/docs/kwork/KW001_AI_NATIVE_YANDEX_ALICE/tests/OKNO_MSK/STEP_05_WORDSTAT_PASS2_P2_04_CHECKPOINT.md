# KW-001 / OKNO-MSK — STEP 05 / P2-04 CHECKPOINT

Date: 2026-08-29
Status: **SUCCEEDED / PROVIDER EVIDENCE CAPTURED**

This file is job-specific and disposable with the OKNO-MSK workspace.

## Probe

```text
probe_id = P2-04
phrase = окна для частного дома
reason = DISTINCT_USER_JOB
method = getTop
regions = ["213"]
devices = ["DEVICE_ALL"]
numPhrases = 200
```

## Provider execution truth

```text
job_id = kw001-okno-msk-wordstat-pass2-20260828
request_id = wordstat-batch-62b19239-14ce-4066-a2b9-1661a1ce63a9
status = SUCCEEDED
http_status = 200
request_executed = true
automatic_retry = false
estimated_cost_rub = 0.02
elapsed_ms = 401
```

Batch progress after completion:

```text
status = COMPLETED
total = 4
pending = 0
succeeded = 4
failed_terminal = 0
outcome_unknown = 0
terminal = 4
requests_started = 4
estimated_cost_rub = 0.08
next_safe_action = NONE
```

## Measured demand observations

Root:

```text
окна для частного дома = 479
```

High-signal direct-result branches include:

```text
размер окон для частного дома = 196
пластиковые окна для частного дома = 115
какие окна для частного дома = 72
стандартные окна для частного дома = 69
стандартные размеры окон для частного дома = 69
размеры пластиковых окон для частного дома = 68
окно для котельной в частном доме = 65
выбираем окна для частного дома = 40
окно для газовой котельной частного дома = 40
окна для частного дома купить = 31
окон в котельной требования для частных домов = 27
какие окна выбрать для частного дома = 27
панорамные окна для частного дома = 16
какой профиль окон лучше для частного дома = 9
окна для частного дома цена = 7
```

Additional observed branches:

```text
sizes / standards
selection / comparison
PVC windows
commercial buy/price intent
boiler-room / gas-boiler technical requirements
panoramic windows
wood / aluminium materials
windows-in-floor / form / room-specific use cases
```

## Associations

Notable vocabulary signal:

```text
остекление коттеджей = 133
оконные конструкции = 1536
```

Other associations include broad/noisy adjacent concepts such as `стеклопакет`, garden/country-house terms, `оконный проем` and unrelated house vocabulary.

Association evidence remains vocabulary evidence only; it is not automatically accepted as final semantics or as another Wordstat expansion seed.

## Analytical boundary

This checkpoint does **not** decide:

```text
final keyword retention
cluster boundaries
separate page requirements
whether boiler-room demand requires standalone content
whether `остекление коттеджей` requires another acquisition probe
SERP intent/page ownership
```

Those decisions belong to later cleanup/SERP/page-mapping stages.

## Probe verdict

```text
P2_04_EXECUTION = PASS
P2_04_INFORMATION_GAIN = CONFIRMED
P2_04_PROVIDER_ERROR = NONE
P2_04_OUTCOME_UNKNOWN = false
```
