# KW-002 Step06 — S06Q001 COLLECT HTTP 404 EVIDENCE

Date: 2026-09-15
Status: **OPERATION.GET EXECUTED / HTTP 404 / RESULT NOT RECOVERED / OLD OPERATION FROZEN**

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
- `STEP_06_S06Q001_COLLECT_READ_ERROR_EVIDENCE_2026-09-15.md`

## Exact Bridge result returned after the second collectN

```json
{"action":"collectN","job_id":"kw002-s06q001-20260914","ok":false,"request_executed":true,"provider_calls":1,"processed":1,"normalized":0,"bounded_stop":false,"last":{"outcome":"read_error","code":"ASYNC_HTTP_404","index":0,"operation_id":"spr2q2fbfldmt6poichd"},"progress":{"job_id":"kw002-s06q001-20260914","control":"RUNNING","total":1,"counts":{"PENDING":0,"SUBMITTING":0,"WAITING":1,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":1,"operations_accepted":1,"polls_started":2,"unresolved":1,"all_successful":false,"busy":false,"revision":6}}
```

## Reconciled execution truth

```text
COLLECT_OK = false
REQUEST_EXECUTED = true
BRIDGE_REPORTED_PROVIDER_CALLS = 1
PROCESSED = 1
NORMALIZED = 0
OUTCOME = read_error
ERROR_CODE = ASYNC_HTTP_404
ITEM_INDEX = 0
OPERATION_ID = spr2q2fbfldmt6poichd
LOCAL_ITEM_STATE_AFTER_SETTLEMENT = WAITING
REQUESTS_STARTED = 1
OPERATIONS_ACCEPTED = 1
POLLS_STARTED = 2
UNRESOLVED = 1
REVISION = 6
RESULT_SAVED = 0
SUCCEEDED = 0
FAILED = 0
UNKNOWN_ITEM_STATE_COUNT = 0
CANCELLED = 0
```

The second Operation.Get attempt definitely crossed the Bridge network boundary and received an HTTP 404 response. This is not a Search zero-result response, not completed Search evidence, and not a successful deferred result.

The local `WAITING` state is only the Bridge lifecycle state after `finishCollect(read_error)`. It does not prove that the provider still retains the operation.

## Endpoint and Bridge qualification recheck

Accepted v0.1.6 `search_async_protocol.js` builds the collect request as:

`GET https://operation.api.cloud.yandex.net/operations/{operationId}`

Current official Yandex Operation.Get documentation specifies the same endpoint.

A prior owner-installed v0.1.6 live smoke test on 2026-09-13 (`B19_OWNER_SMOKE_TEST_12_REAL_COLLECT_PASS_2026-09-13.md`) demonstrated that the same product path can execute a real Operation API collect and receive a deferred result successfully:

```text
request_executed = true
provider_calls = 1
outcome = received
normalized = 1
final state = SUCCEEDED
```

Therefore this S06Q001 404 must not be generalized into a claim that the v0.1.6 Operation.Get route is categorically nonfunctional.

## Provider-limit recheck

Current official Yandex Search API limits state:
- minimum deferred processing time: 5 minutes;
- maximum retention time of deferred request results: 12 hours.

Official sources rechecked 2026-09-15:
- https://aistudio.yandex.ru/ru/docs/search-api/api-ref/Operation/get
- https://aistudio.yandex.ru/en/docs/search-api/concepts/limits
- https://aistudio.yandex.ru/ru/docs/search-api/operations/web-search

## Cause classification

```text
OBSERVED_PROVIDER_FACT = Operation.Get returned HTTP 404 for spr2q2fbfldmt6poichd
EXACT_CAUSE = UNRESOLVED_FROM_AVAILABLE_EVIDENCE
ROUTE_TYPO_PROVEN = false
BRIDGE_OPERATION_GET_CATEGORICALLY_BROKEN = false
RESULT_EXPIRED_PROVEN = false
ACCESS_CONTEXT_MISMATCH_PROVEN = false
PROVIDER_SIDE_OPERATION_DISAPPEARANCE_PROVEN = false
```

The 12-hour retention limit makes retention expiry a plausible explanation when the operation is old, but the exact provider creation timestamp needed to prove expiry is not present in the Bridge result currently preserved in the KW-002 evidence chain. No exact-cause claim is made without that evidence.

## Hard lifecycle decision

The old operation is now frozen from further blind collection attempts:

```text
OLD_OPERATION_FURTHER_COLLECT_ALLOWED = false
OLD_JOB_RESUBMIT_ALLOWED = false
S06Q002_RELEASED = false
STEP07_STARTED = false
```

Repeated GET of the same 404 operation would be an ungrounded retry and is not authorized.

## Next admissible recovery path

Before any new provider call, a separate bounded recovery/replay authority must decide whether S06Q001 may be reacquired as a controlled replacement under a new job identity. Such a replacement, if authorized, is not an automatic retry and must preserve this failed lifecycle as provenance.

Until that release is published and remotely read back:
- no new `start`;
- no new `submit`/`submitN`;
- no new `collect`/`collectN`;
- no S06Q002;
- no Step07.
