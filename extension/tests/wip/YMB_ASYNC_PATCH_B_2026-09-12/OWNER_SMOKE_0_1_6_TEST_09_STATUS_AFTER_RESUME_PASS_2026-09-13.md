# YMB 0.1.6 owner smoke — TEST-09 status after resume

Date: 2026-09-13
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Candidate: exact owner-installed `Yandex-Marketing-Bridge-0.1.6.zip`

## Command

```text
SEARCH_ASYNC_BATCH_API_V1
{"action":"status","jobId":"owner-smoke-016-01"}
```

## Observed owner result

```text
SEARCH_ASYNC_BATCH_RESULT_V1 {"action":"status","job_id":"owner-smoke-016-01","ok":true,"request_executed":false,"provider_calls":0,"progress":{"job_id":"owner-smoke-016-01","control":"RUNNING","total":1,"counts":{"PENDING":1,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":0,"operations_accepted":0,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":2}}
```

## Verdict

`TEST-09 = PASS`

Confirmed:

- control remained `RUNNING` after resume;
- exactly one item remained `PENDING`;
- `request_executed=false`;
- `provider_calls=0`;
- `requests_started=0`;
- `operations_accepted=0`;
- `polls_started=0`;
- `revision=2`;
- no real Yandex provider request occurred in TEST-09.

Cumulative owner smoke through TEST-09: nine local/deferred-control checks passed without a provider call. The next boundary is the first real `submit`; it must not be issued without separate owner authorization for a real Yandex Search API request.
