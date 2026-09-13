# B19 — owner smoke tests of new 0.1.6 functionality

Date: 2026-09-13
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Candidate: `Yandex-Marketing-Bridge-0.1.6.zip`
Candidate SHA-256: `81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2`

This file records owner-run smoke tests after the owner explicitly waived the independent Codex gate. These results do not retroactively constitute Codex PASS.

## TEST-01 — deferred Search start is local-only

Command:

```text
SEARCH_ASYNC_BATCH_API_V1
{"action":"start","jobId":"owner-smoke-016-01","queries":["тестовый запрос bridge 0.1.6"],"confirmBillable":true,"maxRequests":1,"maxCostRub":1}
```

Observed result:

```text
SEARCH_ASYNC_BATCH_RESULT_V1 {"action":"start","job_id":"owner-smoke-016-01","ok":true,"request_executed":false,"provider_calls":0,"progress":{"job_id":"owner-smoke-016-01","control":"RUNNING","total":1,"counts":{"PENDING":1,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":0,"operations_accepted":0,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":0}}
```

Verdict: **PASS**

Acceptance facts:

- `ok=true`;
- `request_executed=false`;
- `provider_calls=0`;
- exactly one item created in `PENDING`;
- `requests_started=0`;
- `operations_accepted=0`;
- `polls_started=0`;
- no `UNKNOWN` / `FAILED` / `CANCELLED` state;
- no provider request was initiated by `start`.

Next test: local `status` readback of the same persisted job; expected provider calls = 0.
