# KW-002 Step06 — S06Q001 REACQUISITION R1 SUBMIT ACCEPTED EVIDENCE

Date: 2026-09-15
Status: **PROVIDER SUBMIT ACCEPTED / OPERATION ID DURABLY RECORDED / WAITING / NO COLLECTION RELEASED YET**

## Scope

This evidence belongs only to the controlled reacquisition of the already-released Step06 representative query:

```text
QUERY_ID = S06Q001
QUERY_TEXT = амулет
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q001-r1-20260915
```

The original failed job `kw002-s06q001-20260914` and old operation `spr2q2fbfldmt6poichd` remain frozen and are not reopened.

Upstream authorities:
- `STEP_06_S06Q001_CONTROLLED_REACQUISITION_RELEASE_2026-09-15.md`
- `STEP_06_S06Q001_REACQUISITION_R1_START_PASS_AND_SUBMIT_RELEASE_2026-09-15.md`

## Exact Bridge submit result received in owner chat

```json
{"action":"submitN","job_id":"kw002-s06q001-r1-20260915","ok":true,"request_executed":true,"provider_calls":1,"processed":1,"normalized":0,"bounded_stop":false,"last":{"outcome":"accepted","code":null,"index":0,"operation_id":"spr9hlddpfp9al2grrfl"},"progress":{"job_id":"kw002-s06q001-r1-20260915","control":"RUNNING","total":1,"counts":{"PENDING":0,"SUBMITTING":0,"WAITING":1,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":1,"operations_accepted":1,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":2}}
```

## Reconciled execution truth

```text
SUBMIT_OK = true
REQUEST_EXECUTED = true
PROVIDER_CALLS = 1
PROCESSED = 1
NORMALIZED = 0
OUTCOME = accepted
ERROR_CODE = null
ITEM_INDEX = 0
OPERATION_ID = spr9hlddpfp9al2grrfl
ITEM_STATE = WAITING
REQUESTS_STARTED = 1
OPERATIONS_ACCEPTED = 1
POLLS_STARTED = 0
UNRESOLVED = 1
RESULT_SAVED = 0
SUCCEEDED = 0
PARSE_FAILED = 0
FAILED = 0
UNKNOWN = 0
CANCELLED = 0
REVISION = 2
```

This is a successful deferred submission only. It is not Search-result evidence yet and it does not prove any SERP row, domain, title, snippet or zero-result outcome.

## Timing guard

The Bridge result does not expose an authoritative provider-side operation creation timestamp in this chat envelope. The owner-chat observation time was checked immediately after receipt as:

```text
OBSERVED_AT = 2026-09-15T07:20:59+05:00
```

To avoid polling earlier than the documented deferred minimum processing window, use a conservative external guard:

```text
COLLECTION_NOT_BEFORE = 2026-09-15T07:25:59+05:00
```

This guard is later than five minutes after the result was observed, so it cannot be earlier than five minutes after the provider submit itself. The Bridge's own durable `next_poll_at` remains the runtime authority when collection is attempted.

## Hard boundaries

```text
SECOND_SUBMIT = FORBIDDEN
AUTOMATIC_RETRY = false
NEW_OPERATION_ID_MUST_BE_PRESERVED = spr9hlddpfp9al2grrfl
COLLECTION_RELEASED_NOW = false
COLLECTION_BEFORE_2026-09-15T07:25:59+05:00 = FORBIDDEN
OLD_OPERATION_COLLECT = FORBIDDEN
OLD_JOB_RESUBMIT = FORBIDDEN
S06Q002_RELEASED = false
STEP07_STARTED = false
```

Before any collection command:
1. persist this accepted operation identity;
2. publish/update the execution cursor;
3. remote-read both artifacts;
4. re-check current time against the conservative guard;
5. publish a bounded collection release for at most one `collectN count=1` on this same new job.
