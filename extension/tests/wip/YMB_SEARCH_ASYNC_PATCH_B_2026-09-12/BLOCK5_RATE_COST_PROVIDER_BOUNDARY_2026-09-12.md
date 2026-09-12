# YMB Deferred Search Patch B — rate / cost / provider-boundary block 5

Date: 2026-09-12
Branch: `wip/ymb-search-async-patch-b-2026-09-12`
Candidate: exact Patch B candidate1; production bytes unchanged.
Real Yandex traffic: 0. Provider requests were intercepted/stubbed in controlled Node/browser QA.

## Deterministic runtime rate/cost tests

Node executable assertions: `5/5 PASS`.

Proved:

- `submitN` sleeps exactly 150 ms between provider submit boundaries;
- `collectN` sleeps exactly 150 ms between Operation GET boundaries;
- unknown submit outcome stops `submitN` immediately: one provider call, no hidden retry, no later-item progression;
- transient collect failure performs one GET per selected item per command, no hidden retry;
- policy/admission rejection happens before provider submit and before cost/request reservation mutation;
- accepted submits reserve exactly `0.0305 RUB` each in the deferred estimate;
- collection GET increments collection counters but does not add Search submit cost.

## Browser worker provider-boundary test

Browser: Chrome/Chromium 144.0.7559.96 controlled QA profile.

Captured async submit request:

```text
POST https://searchapi.api.cloud.yandex.net/v2/web/searchAsync
Authorization: Api-Key <fake QA key>
Content-Type: application/json
folderId = qa-folder
responseFormat = FORMAT_XML
```

Captured Operation request:

```text
GET https://operation.api.cloud.yandex.net/operations/op%2Fa%2Bb
Authorization: Api-Key <fake QA key>
Accept: application/json
```

Captured ordinary sync Search regression:

```text
POST https://searchapi.api.cloud.yandex.net/v2/web/search
```

The ordinary Search endpoint/body semantics remained unchanged.

Additional browser assertions:

```text
async_submit_url = PASS
async_submit_method = PASS
async_submit_auth = PASS
async_folder_id = PASS
operation_get_fixed_host = PASS
operation_get_encoded_id = PASS
operation_get_auth = PASS
sync_search_unchanged_endpoint = PASS
global_policy_one_fetch_only = PASS
second_submit_blocked_before_fetch = PASS
autorun_async_manual_only = PASS
autorun_async_fetch_count = 0
operation_id_mismatch_fail_closed = PASS
```

The global Search policy was set to one request; first deferred submit executed, second was rejected with `REQUEST_LIMIT` and no second fetch.

Operation GET returning another operation id raised `ASYNC_OPERATION_ID_MISMATCH` with no automatic retry.

Managed Chromium policy was restored exactly after browser QA:

`3b740260e337305aaef268e6c63af8fa2796057ce46f43df5ae5a3949e085e86`

## Verdict

```text
PATCH_B_RATE_LIMIT = PASS
PATCH_B_COST_GUARD = PASS
PATCH_B_PROVIDER_BOUNDARY = PASS
SYNC_SEARCH_PROVIDER_REGRESSION = PASS
HIDDEN_RETRY = 0
PRODUCTION_BYTES_CHANGED = NO
PATCH_B_ACCEPTED_FOR_INTEGRATION = NOT_YET
RELEASE_ALLOWED = NO
```

Shared-service/manual/content dependency regression and exact-candidate identity still remain before Patch-B acceptance-for-integration.
