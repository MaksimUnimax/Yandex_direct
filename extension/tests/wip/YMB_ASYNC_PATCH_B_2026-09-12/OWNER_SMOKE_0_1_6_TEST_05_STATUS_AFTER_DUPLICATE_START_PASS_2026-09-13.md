# Owner smoke 0.1.6 — TEST-05 PASS

Date: 2026-09-13
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`

## Purpose

Verify that the rejected duplicate `start` from TEST-04 did not mutate the existing deferred Search job.

## Observed owner-profile result

```text
SEARCH_ASYNC_BATCH_RESULT_V1
{"action":"status","job_id":"owner-smoke-016-01","ok":true,"request_executed":false,"provider_calls":0,"progress":{"job_id":"owner-smoke-016-01","control":"RUNNING","total":1,"counts":{"PENDING":1,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":0,"operations_accepted":0,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":0}}
```

## Acceptance

- existing job still present: PASS
- control remains `RUNNING`: PASS
- total remains `1`: PASS
- `PENDING=1`: PASS
- `requests_started=0`: PASS
- `operations_accepted=0`: PASS
- `polls_started=0`: PASS
- `provider_calls=0`: PASS
- `request_executed=false`: PASS
- `revision=0`: PASS
- duplicate-start rejection caused no observable state mutation: PASS

`OWNER_SMOKE_0_1_6_TEST_05 = PASS`
