# Owner smoke test 03 — itemsPage durable item readback

Date: 2026-09-13
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Candidate: Yandex Marketing Bridge 0.1.6
Job: `owner-smoke-016-01`

Owner-observed result:

`SEARCH_ASYNC_BATCH_RESULT_V1 {"action":"itemsPage","job_id":"owner-smoke-016-01","ok":true,"request_executed":false,"provider_calls":0,"page":{"rows":[{"index":0,"state":"PENDING","operation_id":null,"poll_count":0,"error_code":null,"parse_error":null}],"next_after":0}}`

Verdict: PASS.

Verified from the owner-installed candidate:
- the job contains one durable item at index 0;
- item state is `PENDING`;
- no operation id exists yet;
- poll count is 0;
- no item error or parse error is present;
- `request_executed=false`;
- `provider_calls=0`.

This confirms that `start` persisted the deferred Search item locally and `itemsPage` can read it without provider traffic.
