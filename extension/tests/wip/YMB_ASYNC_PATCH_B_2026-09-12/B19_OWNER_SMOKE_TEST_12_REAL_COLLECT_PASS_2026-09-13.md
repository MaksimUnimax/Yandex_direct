# B19 owner smoke TEST-12 — real deferred Search collect PASS

Date: 2026-09-13
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Installed build: `Yandex-Marketing-Bridge-0.1.6.zip`
Job: `owner-smoke-016-01`

Observed result:

```json
{"action":"collectN","job_id":"owner-smoke-016-01","ok":true,"request_executed":true,"provider_calls":1,"processed":1,"normalized":1,"bounded_stop":false,"last":{"outcome":"received","code":null,"index":0,"operation_id":"sprnnhjulgb8ofo593bc"},"progress":{"job_id":"owner-smoke-016-01","control":"RUNNING","total":1,"counts":{"PENDING":0,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":1,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":1,"operations_accepted":1,"polls_started":1,"unresolved":0,"all_successful":true,"busy":false,"revision":7}}
```

Verdict: **PASS**.

Confirmed live owner-installed end-to-end behavior:
- one real Operation API collect call executed;
- persisted operation id matched `sprnnhjulgb8ofo593bc`;
- provider result was received;
- raw result was durably persisted before normalization;
- automatic normalization succeeded (`normalized=1`);
- final durable item state is `SUCCEEDED`;
- no parse failure, provider failure, UNKNOWN, or unresolved work remains;
- `all_successful=true`;
- no automatic retry was required.

This owner smoke test is execution evidence only and does not rewrite the earlier independent Codex waiver classification.
