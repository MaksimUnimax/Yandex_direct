# KW-002 Step06 — S06Q001 REACQUISITION R1 COLLECT PASS EVIDENCE

Date: 2026-09-15
Status: **OPERATION RESULT RECEIVED / NORMALIZATION SUCCEEDED / LOCAL RESULT SAVED / EXPORT REQUIRED BEFORE S06Q002**

## Scope

```text
QUERY_ID = S06Q001
QUERY_TEXT = амулет
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q001-r1-20260915
OPERATION_ID = spr9hlddpfp9al2grrfl
```

The original failed job `kw002-s06q001-20260914` and old operation `spr2q2fbfldmt6poichd` remain frozen.

## Exact Bridge collect result received in owner chat

```json
{"action":"collectN","job_id":"kw002-s06q001-r1-20260915","ok":true,"request_executed":true,"provider_calls":1,"processed":1,"normalized":1,"bounded_stop":false,"last":{"outcome":"received","code":null,"index":0,"operation_id":"spr9hlddpfp9al2grrfl"},"progress":{"job_id":"kw002-s06q001-r1-20260915","control":"RUNNING","total":1,"counts":{"PENDING":0,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":1,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":1,"operations_accepted":1,"polls_started":1,"unresolved":0,"all_successful":true,"busy":false,"revision":5}}
```

## Reconciled execution truth

```text
COLLECT_OK = true
REQUEST_EXECUTED = true
PROVIDER_CALLS = 1
PROCESSED = 1
NORMALIZED_ITEMS = 1
BOUNDED_STOP = false
OUTCOME = received
ERROR_CODE = null
ITEM_INDEX = 0
OPERATION_ID = spr9hlddpfp9al2grrfl
ITEM_STATE = SUCCEEDED
REQUESTS_STARTED = 1
OPERATIONS_ACCEPTED = 1
POLLS_STARTED = 1
UNRESOLVED = 0
ALL_SUCCESSFUL = true
BUSY = false
REVISION = 5
```

This closes the provider lifecycle for the controlled replacement operation. It proves that a deferred Search result was received and normalized locally. The compact collect envelope does **not** expose the actual normalized SERP rows, therefore it is not yet sufficient durable Step06 evidence by itself.

## Required local evidence export

Accepted Yandex Marketing Bridge v0.1.6 exposes local-only `exportPage` for the async job. The export code reads the already-persisted item and result and includes:
- item lifecycle state and operation identity;
- preserved `raw_text`;
- complete `result.normalized.results` array;
- page-level result row count and integrity metadata.

The export action performs no provider fetch and reports `request_executed=false`, `provider_calls=0`.

Required exact export command after remote readback of this collect evidence and cursor:

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"exportPage","jobId":"kw002-s06q001-r1-20260915","after":-1,"limit":1,"revision":5}
```

## Hard boundaries

```text
SECOND_SUBMIT = FORBIDDEN
FURTHER_COLLECT = FORBIDDEN UNLESS LATER EVIDENCE PROVES EXPORT/LOCAL RESULT DEFECT REQUIRING A SEPARATE DECISION
PROVIDER_CALLS_ALLOWED_NOW = 0
LOCAL_EXPORT_ALLOWED_AFTER_REMOTE_READBACK = 1
S06Q002_RELEASED = false
STEP07_STARTED = false
```

Do not release S06Q002 until the exact exported result file has been received, durably persisted, remotely read back, and its normalized row count/required fields reconciled.