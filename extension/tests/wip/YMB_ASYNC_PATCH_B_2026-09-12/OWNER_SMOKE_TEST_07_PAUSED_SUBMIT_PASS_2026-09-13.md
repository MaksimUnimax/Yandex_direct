# Owner smoke TEST-07 — submit while PAUSED

Date: 2026-09-13
Build: Yandex Marketing Bridge 0.1.6
Job: `owner-smoke-016-01`

Observed owner result:

```json
{"action":"submitN","job_id":"owner-smoke-016-01","ok":false,"request_executed":false,"provider_calls":0,"processed":1,"normalized":0,"bounded_stop":false,"last":{"outcome":null,"code":"PAUSED","index":null,"operation_id":null},"progress":{"job_id":"owner-smoke-016-01","control":"PAUSED","total":1,"counts":{"PENDING":1,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":0,"operations_accepted":0,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":1}}
```

Verdict: **PASS**.

The deferred Search submit path was attempted while the job was paused. Durable admission stopped the request before provider transport: `request_executed=false`, `provider_calls=0`, `operation_id=null`. The original item remained `PENDING`; provider/accounting counters remained zero; control remained `PAUSED`; revision remained 1.

`processed=1` records one local orchestration step and is not a provider execution. `submit` normalizes to `submitN` with count 1 by protocol design.
