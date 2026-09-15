# KW-002 Step06 — S06Q001 COLLECT READ ERROR EVIDENCE

Date: 2026-09-15
Status: **COLLECT ATTEMPT SETTLED AS READ_ERROR / NETWORK OUTCOME UNKNOWN / SAME OPERATION PRESERVED / WAITING**

## Query and operation identity

```text
QUERY_ID = S06Q001
QUERY_TEXT = амулет
JOB_ID = kw002-s06q001-20260914
TRANSPORT = DEFERRED_ASYNC
OPERATION_ID = spr2q2fbfldmt6poichd
```

Upstream authorities:
- `STEP_06_S06Q001_EXECUTION_RELEASE_2026-09-14.md`
- `STEP_06_S06Q001_SUBMIT_ACCEPTED_EVIDENCE_2026-09-14.md`
- `STEP_06_S06Q001_COLLECTION_RELEASE_2026-09-14.md`

## Exact Bridge result returned after collectN

```json
{"action":"collectN","job_id":"kw002-s06q001-20260914","ok":false,"request_executed":"UNKNOWN","provider_calls":0,"processed":1,"normalized":0,"bounded_stop":false,"last":{"outcome":"read_error","code":"ASYNC_NETWORK_OUTCOME_UNKNOWN","index":0,"operation_id":"spr2q2fbfldmt6poichd"},"progress":{"job_id":"kw002-s06q001-20260914","control":"RUNNING","total":1,"counts":{"PENDING":0,"SUBMITTING":0,"WAITING":1,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":1,"operations_accepted":1,"polls_started":1,"unresolved":1,"all_successful":false,"busy":false,"revision":4}}
```

## Reconciled execution truth

```text
COLLECT_OK = false
REQUEST_EXECUTED = UNKNOWN
BRIDGE_REPORTED_PROVIDER_CALLS = 0
PROCESSED = 1
NORMALIZED = 0
OUTCOME = read_error
ERROR_CODE = ASYNC_NETWORK_OUTCOME_UNKNOWN
ITEM_INDEX = 0
OPERATION_ID = spr2q2fbfldmt6poichd
ITEM_STATE_AFTER_SETTLEMENT = WAITING
REQUESTS_STARTED = 1
OPERATIONS_ACCEPTED = 1
POLLS_STARTED = 1
UNRESOLVED = 1
REVISION = 4
RESULT_SAVED = 0
SUCCEEDED = 0
FAILED = 0
UNKNOWN_ITEM_STATE_COUNT = 0
CANCELLED = 0
```

`provider_calls=0` MUST NOT be interpreted as proof that no HTTP GET reached the provider, because the transport contract itself reports `request_executed="UNKNOWN"`. The correct evidence state is network outcome unknown.

This is NOT:
- a provider zero-result response;
- a provider rejection;
- a completed Search result;
- permission to resubmit the Search query;
- permission to create another job;
- permission to release S06Q002.

## Code-level lifecycle interpretation

Accepted v0.1.6 `search_async_transport.js` classifies an unrecognized exception after durable admission/fetch entry as `ASYNC_NETWORK_OUTCOME_UNKNOWN` and returns `request_executed="UNKNOWN"`; no automatic retry is performed.

Accepted v0.1.6 `search_async_store.js` handles `finishCollect(outcome=read_error)` by:
1. recording `last_polled_at`;
2. recording `last_read_error`;
3. assigning a new `next_poll_at`;
4. moving the item from `COLLECTING` back to `WAITING`;
5. settling the attempt and clearing the lease.

Therefore the current item is durably settled and does not require runtime `recover`. A later explicit collect may continue the same saved provider operation lifecycle only after a new bounded release/current-state check.

## Anti-duplicate boundary

- DO NOT call `start` again.
- DO NOT call `submit` or `submitN` again.
- DO NOT create a replacement job for S06Q001.
- DO NOT release S06Q002.
- DO NOT infer whether the uncertain GET reached the provider.
- DO NOT count this as Search evidence.
- DO NOT automatically retry collect.

## Conservative next-read timing gate

The exact internal `next_poll_at` timestamp is not exposed in the Bridge result. At 2026-09-15T06:37:25+05:00 the result was being reconciled. To avoid an immediate blind retry, the chat-side control gate sets:

```text
NEXT_COLLECT_RECHECK_NOT_BEFORE = 2026-09-15T06:42:25+05:00
```

This is a conservative orchestration gate, not a claim about the exact internal store timestamp. After that time, current state must be rechecked and one new explicit collect attempt may be released for the SAME job/operation if no contradictory evidence appears.
