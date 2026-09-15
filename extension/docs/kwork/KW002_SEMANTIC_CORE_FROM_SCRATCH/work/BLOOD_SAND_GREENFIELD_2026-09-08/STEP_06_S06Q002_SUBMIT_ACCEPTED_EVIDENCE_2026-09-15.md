# KW-002 Step06 — S06Q002 SUBMIT ACCEPTED EVIDENCE

Date: 2026-09-15
Status: **PROVIDER SUBMIT ACCEPTED / OPERATION ID DURABLY RECORDED / WAITING / NO COLLECTION RELEASED YET**

## 1. Scope

This evidence belongs only to the already-started and separately submit-released Step06 query:

```text
QUERY_ID = S06Q002
QUERY_TEXT = оберег
JOB_ID = kw002-s06q002-20260915
TRANSPORT = DEFERRED_ASYNC
```

Upstream authorities:
- `STEP_06_S06Q002_EXECUTION_RELEASE_2026-09-15.md`
- `STEP_06_S06Q002_RELEASE_REMOTE_READBACK_2026-09-15.md`
- `STEP_06_S06Q002_LOCAL_START_PASS_EVIDENCE_2026-09-15.md`
- `STEP_06_S06Q002_LOCAL_START_REMOTE_READBACK_2026-09-15.md`
- `STEP_06_S06Q002_EXACT_ONE_SUBMIT_RELEASE_2026-09-15.md`
- `STEP_06_S06Q002_EXACT_ONE_SUBMIT_RELEASE_REMOTE_READBACK_2026-09-15.md`

## 2. Exact Bridge submit result received in owner chat

```json
{"action":"submitN","job_id":"kw002-s06q002-20260915","ok":true,"request_executed":true,"provider_calls":1,"processed":1,"normalized":0,"bounded_stop":false,"last":{"outcome":"accepted","code":null,"index":0,"operation_id":"sprridu5n6oqitgg774b"},"progress":{"job_id":"kw002-s06q002-20260915","control":"RUNNING","total":1,"counts":{"PENDING":0,"SUBMITTING":0,"WAITING":1,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":1,"operations_accepted":1,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":2}}
```

## 3. Reconciled execution truth

```text
SUBMIT_OK = true
REQUEST_EXECUTED = true
PROVIDER_CALLS = 1
PROCESSED = 1
NORMALIZED = 0
BOUNDED_STOP = false
OUTCOME = accepted
ERROR_CODE = null
ITEM_INDEX = 0
OPERATION_ID = sprridu5n6oqitgg774b
ITEM_STATE = WAITING
CONTROL = RUNNING
TOTAL = 1
PENDING = 0
SUBMITTING = 0
WAITING = 1
COLLECTING = 0
RESULT_SAVED = 0
SUCCEEDED = 0
PARSE_FAILED = 0
FAILED = 0
UNKNOWN = 0
CANCELLED = 0
REQUESTS_STARTED = 1
OPERATIONS_ACCEPTED = 1
POLLS_STARTED = 0
UNRESOLVED = 1
ALL_SUCCESSFUL = false
BUSY = false
REVISION = 2
```

This is a successful deferred submission only. It is not Search-result evidence yet and proves no SERP row, domain, title, snippet, zero-result outcome, clustering or competitor membership.

## 4. Timing guard

The submit envelope does not expose an authoritative provider-side operation creation timestamp or runtime `next_poll_at` in the owner chat result. The owner-chat observation point for this result is recorded as:

```text
OBSERVED_AT = 2026-09-15T09:41:00+05:00
```

To avoid polling earlier than the same conservative deferred guard used for the accepted S06Q001 lifecycle:

```text
COLLECTION_NOT_BEFORE = 2026-09-15T09:46:00+05:00
```

This external guard is only a lower bound. The Bridge runtime's durable `next_poll_at`, if later, remains authoritative when a collection attempt is actually made.

## 5. Hard boundaries

```text
SECOND_LOCAL_START = FORBIDDEN
SECOND_PROVIDER_SUBMIT = FORBIDDEN
AUTOMATIC_RETRY = false
NEW_OPERATION_ID_MUST_BE_PRESERVED = sprridu5n6oqitgg774b
COLLECTION_RELEASED_NOW = false
COLLECTION_BEFORE_2026-09-15T09:46:00+05:00 = FORBIDDEN
SYNCHRONOUS_SEARCH_FALLBACK = FORBIDDEN
WORDSTAT_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
STEP07_STARTED = false
STEP08_STARTED = false
```

Before any collection command:
1. persist this accepted operation identity and successor cursor;
2. remote-read both artifacts;
3. re-check current time against the conservative guard;
4. preserve the same job and operation identity;
5. publish a bounded collection release for at most one `collectN count=1` on this exact job;
6. remote-read that release before any provider collection call.

## 6. Verdict

```text
S06Q002_PROVIDER_SUBMIT = ACCEPTED
S06Q002_OPERATION_ID = sprridu5n6oqitgg774b
S06Q002_STATE = WAITING
S06Q002_PROVIDER_SUBMIT_CALLS = 1
S06Q002_PROVIDER_COLLECT_CALLS = 0
S06Q002_RESULT_RECEIVED = false
NEXT_PROVIDER_CALL_ALLOWED_NOW = 0
```
