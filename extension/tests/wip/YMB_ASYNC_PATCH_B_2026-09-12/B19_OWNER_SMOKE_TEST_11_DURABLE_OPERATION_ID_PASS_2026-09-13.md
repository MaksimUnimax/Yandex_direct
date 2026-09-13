# B19 owner smoke TEST-11 — durable operation id readback PASS

Date: 2026-09-13
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Version: `0.1.6`
Job: `owner-smoke-016-01`

Observed owner result:

```json
{"action":"itemsPage","job_id":"owner-smoke-016-01","ok":true,"request_executed":false,"provider_calls":0,"page":{"rows":[{"index":0,"state":"WAITING","operation_id":"sprnnhjulgb8ofo593bc","poll_count":0,"error_code":null,"parse_error":null}],"next_after":0}}
```

Verdict: PASS.

Confirmed:
- provider calls for readback: 0;
- item index 0 is durably persisted in state `WAITING`;
- durable operation id is `sprnnhjulgb8ofo593bc`;
- poll count remains 0 before collect;
- no item/provider/parse errors are recorded.

This proves the accepted Yandex Search async operation identity is persisted locally and is not dependent on the prior submit response text.
