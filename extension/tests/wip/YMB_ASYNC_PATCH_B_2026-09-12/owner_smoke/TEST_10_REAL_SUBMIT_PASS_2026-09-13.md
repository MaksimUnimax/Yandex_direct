# OWNER SMOKE TEST-10 — REAL deferred Search submit

Date: 2026-09-13
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Version: `0.1.6`
Job: `owner-smoke-016-01`

Result supplied by owner from installed extension:

```json
{"action":"submitN","job_id":"owner-smoke-016-01","ok":true,"request_executed":true,"provider_calls":1,"processed":1,"normalized":0,"bounded_stop":false,"last":{"outcome":"accepted","code":null,"index":0,"operation_id":"sprnnhjulgb8ofo593bc"},"progress":{"job_id":"owner-smoke-016-01","control":"RUNNING","total":1,"counts":{"PENDING":0,"SUBMITTING":0,"WAITING":1,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":1,"operations_accepted":1,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":4}}
```

Verdict: **PASS**.

Confirmed:
- one real Yandex Search API submit executed;
- provider_calls=1;
- operation accepted with id `sprnnhjulgb8ofo593bc`;
- durable state moved PENDING -> WAITING;
- requests_started=1;
- operations_accepted=1;
- no UNKNOWN/FAILED state;
- no collect/poll performed yet.
