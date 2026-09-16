# KW-002 Step06 — S06Q002 CONTROLLED REACQUISITION R1 SUBMIT ACCEPTED EVIDENCE

Date: 2026-09-16
Status: **PASS / EXACTLY ONE PROVIDER SUBMIT EXECUTED / WAITING / NO COLLECT RELEASED**

## 1. Scope

```text
QUERY_ID = S06Q002
QUERY_TEXT = оберег
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q002-r1-20260916
YMB_VERSION = 0.1.8
```

## 2. Exact returned Bridge envelope

```json
{"action":"submitN","job_id":"kw002-s06q002-r1-20260916","ok":true,"request_executed":true,"provider_calls":1,"processed":1,"normalized":0,"bounded_stop":false,"last":{"outcome":"accepted","code":null,"index":0,"operation_id":"sprriom53ppme5q13epe"},"progress":{"job_id":"kw002-s06q002-r1-20260916","control":"RUNNING","total":1,"counts":{"PENDING":0,"SUBMITTING":0,"WAITING":1,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":1,"operations_accepted":1,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":2}}
```

## 3. Verified invariants

```text
ok = true
request_executed = true
provider_calls = 1
processed = 1
normalized = 0
bounded_stop = false
outcome = accepted
operation_id = sprriom53ppme5q13epe
control = RUNNING
WAITING = 1
requests_started = 1
operations_accepted = 1
polls_started = 0
unresolved = 1
all_successful = false
busy = false
revision = 2
```

Exactly one Search provider submission was executed and accepted. The provider operation is now durable under `sprriom53ppme5q13epe`.

## 4. Poll guard

The Bridge deferred Search protocol requires a minimum first-poll delay of five minutes. The submit result was observed in the current execution session at approximately:

```text
SUBMIT_RESULT_OBSERVED_AT = 2026-09-16T12:16:00+05:00
CONSERVATIVE_COLLECTION_NOT_BEFORE = 2026-09-16T12:21:00+05:00
```

Provider-side `createdAt` was not exposed in this submit envelope, so the observed submit-result time is used conservatively for the external release gate. The runtime's own persisted `next_poll_at` remains authoritative when `collectN` is eventually attempted.

## 5. Hard boundary after submit

```text
SECOND_PROVIDER_SUBMIT_ALLOWED = false
AUTOMATIC_RETRY = false
PROVIDER_COLLECTIONS_ALLOWED_NOW = 0
LOCAL_START_ALLOWED_NOW = 0
SYNCHRONOUS_SEARCH_CALLS_ALLOWED = 0
WORDSTAT_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
```

No `collectN` may be released until this evidence and its successor cursor are remote-read back and the conservative first-poll guard has elapsed.

## 6. Verdict

```text
S06Q002_R1_PROVIDER_SUBMIT = ACCEPTED
PROVIDER_SUBMIT_CALLS = 1
PROVIDER_OPERATION_ID = sprriom53ppme5q13epe
CURRENT_ITEM_STATE = WAITING
PROVIDER_COLLECT_CALLS = 0
SECOND_PROVIDER_SUBMIT_ALLOWED = false
S06Q003_RELEASED = false
```
