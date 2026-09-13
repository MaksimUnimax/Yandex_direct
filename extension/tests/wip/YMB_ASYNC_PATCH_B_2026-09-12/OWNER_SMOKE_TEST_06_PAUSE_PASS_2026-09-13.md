# Owner smoke TEST-06 — deferred Search pause

Date: 2026-09-13
Product: Yandex Marketing Bridge 0.1.6
Job: `owner-smoke-016-01`

Observed owner result:

```json
{"action":"pause","job_id":"owner-smoke-016-01","ok":true,"request_executed":false,"provider_calls":0,"progress":{"job_id":"owner-smoke-016-01","control":"PAUSED","total":1,"counts":{"PENDING":1,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":0,"operations_accepted":0,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":1}}
```

Verdict: PASS.

Key assertions:
- local control moved from RUNNING to PAUSED;
- one pending item preserved;
- request_executed=false;
- provider_calls=0;
- requests_started=0;
- operations_accepted=0;
- polls_started=0;
- revision advanced from 0 to 1;
- no provider work was initiated.
