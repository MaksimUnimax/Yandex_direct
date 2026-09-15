# KW-002 Step06 — S06Q001 REACQUISITION R1 START PASS AND SUBMIT RELEASE

Date: 2026-09-15
Status: **LOCAL START PASS / EXACTLY ONE PROVIDER SUBMIT RELEASED / NO COLLECTION YET / NO S06Q002**

## Scope

This authority continues only the controlled reacquisition of the already-released Step06 representative query:

```text
QUERY_ID = S06Q001
QUERY_TEXT = амулет
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q001-r1-20260915
```

The original failed job `kw002-s06q001-20260914` and operation `spr2q2fbfldmt6poichd` remain frozen. This file does not reopen them.

Upstream authority:
- `STEP_06_S06Q001_CONTROLLED_REACQUISITION_RELEASE_2026-09-15.md`
- `STEP_06_S06Q001_COLLECT_HTTP_404_EVIDENCE_2026-09-15.md`

## Exact local start result received in owner chat

```json
{"action":"start","job_id":"kw002-s06q001-r1-20260915","ok":true,"request_executed":false,"provider_calls":0,"progress":{"job_id":"kw002-s06q001-r1-20260915","control":"RUNNING","total":1,"counts":{"PENDING":1,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":0,"operations_accepted":0,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":0}}
```

## Reconciled start truth

```text
START_OK = true
REQUEST_EXECUTED = false
PROVIDER_CALLS = 0
TOTAL = 1
PENDING = 1
REQUESTS_STARTED = 0
OPERATIONS_ACCEPTED = 0
POLLS_STARTED = 0
UNRESOLVED = 1
REVISION = 0
```

This proves the replacement job was created locally without a provider request. It does not prove Search success and does not contain SERP evidence yet.

## Exactly one provider submit released

The local-start gate in the controlled reacquisition release is now satisfied. Exactly one deferred Search submission is authorized for this new job:

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"submitN","jobId":"kw002-s06q001-r1-20260915","count":1}
```

Expected safe outcomes:
- accepted provider operation with a new durable operation ID and item state `WAITING`; or
- an explicit provider/transport failure that must be persisted before any further action; or
- an already-complete provider response if Yandex returns terminal data immediately.

## Hard boundaries

```text
NEW_JOB_PROVIDER_SUBMISSIONS_RELEASED_NOW = 1
NEW_JOB_COLLECTIONS_RELEASED_NOW = 0
SECOND_SUBMIT = FORBIDDEN
AUTOMATIC_RETRY = false
OLD_JOB_RESUBMIT = FORBIDDEN
OLD_OPERATION_COLLECT = FORBIDDEN
S06Q002_RELEASED = false
STEP07_STARTED = false
```

After the submit result is returned, persist the exact provider/operation truth and remote-read it before any collection or next-query release.
