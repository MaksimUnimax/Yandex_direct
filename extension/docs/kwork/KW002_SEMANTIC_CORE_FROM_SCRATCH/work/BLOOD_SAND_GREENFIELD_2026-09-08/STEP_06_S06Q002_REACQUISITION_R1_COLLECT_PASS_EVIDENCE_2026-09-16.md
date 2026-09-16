# KW-002 Step06 — S06Q002 CONTROLLED REACQUISITION R1 COLLECT PASS EVIDENCE

Date: 2026-09-16
Status: **PASS / PROVIDER RESULT RECEIVED / NORMALIZED / EXACT EXPORT NOT YET RELEASED**

## 1. Scope

```text
QUERY_ID = S06Q002
QUERY_TEXT = оберег
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q002-r1-20260916
PROVIDER_OPERATION_ID = sprriom53ppme5q13epe
YMB_VERSION = 0.1.8
```

## 2. Exact returned Bridge envelope

```json
{"action":"collectN","job_id":"kw002-s06q002-r1-20260916","ok":true,"request_executed":true,"provider_calls":1,"processed":1,"normalized":1,"bounded_stop":false,"last":{"outcome":"received","code":null,"index":0,"operation_id":"sprriom53ppme5q13epe"},"progress":{"job_id":"kw002-s06q002-r1-20260916","control":"RUNNING","total":1,"counts":{"PENDING":0,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":1,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":1,"operations_accepted":1,"polls_started":1,"unresolved":0,"all_successful":true,"busy":false,"revision":5}}
```

## 3. Verified invariants

```text
ok = true
request_executed = true
provider_calls = 1
processed = 1
normalized = 1
bounded_stop = false
last.outcome = received
last.index = 0
operation_id = sprriom53ppme5q13epe
control = RUNNING
SUCCEEDED = 1
WAITING = 0
RESULT_SAVED = 0
PARSE_FAILED = 0
FAILED = 0
UNKNOWN = 0
CANCELLED = 0
requests_started = 1
operations_accepted = 1
polls_started = 1
unresolved = 0
all_successful = true
busy = false
revision = 5
```

This is the first actual provider collection for the R1 reacquisition. The earlier `NO_DUE_OPERATIONS` command was a local no-op and did not increment `provider_calls` or `polls_started`.

## 4. Current evidence state

The provider operation returned a result and YMB normalized the single saved item successfully. The compact collection envelope intentionally does not contain the full raw provider payload or normalized SERP rows; those remain in the durable deferred job store and must be materialized by `exportPage`.

Therefore:

```text
RESULT_RECEIVED = true
NORMALIZED_ITEM_COUNT = 1
JOB_ALL_SUCCESSFUL = true
JOB_UNRESOLVED = 0
EXACT_EXPORT_PERSISTED = false
CURRENT_EVIDENCE_DURABLY_CLOSED = false
```

## 5. Hard boundary

```text
SECOND_PROVIDER_SUBMIT_ALLOWED = false
SECOND_PROVIDER_COLLECT_PREAUTHORIZED = false
AUTOMATIC_RETRY = false
LOCAL_EXPORT_ALLOWED_NOW = 0
SYNCHRONOUS_SEARCH_CALLS_ALLOWED = 0
WORDSTAT_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
STEP07_STARTED = false
STEP08_STARTED = false
```

Before export, this exact collect evidence and successor cursor must be remote-read back. Then a separate exact-one local export release may be published and remote-read back.

## 6. Verdict

```text
S06Q002_R1_COLLECT_PASS = true
PROVIDER_SUBMIT_CALLS = 1
PROVIDER_COLLECT_CALLS = 1
PROVIDER_OPERATION_ID = sprriom53ppme5q13epe
JOB_REVISION = 5
JOB_ALL_SUCCESSFUL = true
EXACT_EXPORT_REQUIRED = true
S06Q003_RELEASED = false
```
