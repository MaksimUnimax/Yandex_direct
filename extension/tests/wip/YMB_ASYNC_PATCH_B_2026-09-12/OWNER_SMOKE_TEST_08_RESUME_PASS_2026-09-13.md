# OWNER SMOKE TEST 08 — RESUME PASS

Date: 2026-09-13
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Product: Yandex Marketing Bridge 0.1.6
Job: `owner-smoke-016-01`

Observed owner-profile result:

```text
SEARCH_ASYNC_BATCH_RESULT_V1 {"action":"resume","job_id":"owner-smoke-016-01","ok":true,"request_executed":false,"provider_calls":0,"progress":{"job_id":"owner-smoke-016-01","control":"RUNNING","total":1,"counts":{"PENDING":1,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":0,"operations_accepted":0,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":2}}
```

Classification: **PASS**

Verified:
- `PAUSED -> RUNNING` transition succeeds;
- no provider request executed;
- `provider_calls=0`;
- item remains `PENDING`;
- request/operation/poll counters remain zero;
- revision advances from 1 to 2;
- no state corruption after prior paused-submit denial.

No production changes were made by this test.
