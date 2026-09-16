# KW-002 Step06 — S06Q002 CONTROLLED REACQUISITION R1 EXACT-ONE SUBMIT RELEASE

Date: 2026-09-16
Status: **PUBLISHED FOR EXACTLY ONE DEFERRED PROVIDER SUBMISSION / ACTIVATION REQUIRES REMOTE READBACK**

## 1. Scope

```text
QUERY_ID = S06Q002
QUERY_TEXT = оберег
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q002-r1-20260916
TRANSPORT = DEFERRED_ASYNC
YMB_VERSION = 0.1.8
```

The fresh local job has already passed and was remote-read back under:

- `STEP_06_S06Q002_REACQUISITION_R1_LOCAL_START_PASS_EVIDENCE_2026-09-16.md`
- `STEP_06_S06Q002_REACQUISITION_R1_LOCAL_START_REMOTE_READBACK_2026-09-16.md`

Current job truth before provider execution:

```text
control = RUNNING
total = 1
PENDING = 1
requests_started = 0
operations_accepted = 0
polls_started = 0
unresolved = 1
revision = 0
provider_calls_so_far = 0
```

## 2. Exact provider command

After this release and its successor cursor are remote-read back, exactly one provider submission may be executed:

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"submitN","jobId":"kw002-s06q002-r1-20260916","count":1}
```

The existing job caps are authoritative:

```text
maxRequests = 1
maxCostRub = 0.0305
```

Therefore this release authorizes at most one Search provider request for the one preserved query `оберег`.

## 3. Hard execution boundary

```text
EXACT_PROVIDER_SUBMISSIONS_TO_AUTHORIZE_AFTER_REMOTE_READBACK = 1
SECOND_PROVIDER_SUBMIT_ALLOWED = false
PROVIDER_COLLECTIONS_ALLOWED_NOW = 0
AUTOMATIC_RETRY = false
SYNCHRONOUS_SEARCH_FALLBACK = false
GENSEARCH_FALLBACK = false
WORDSTAT_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
STEP07_STARTED = false
STEP08_STARTED = false
```

## 4. Required handling of submit result

Immediately after the one `submitN`:

1. preserve the exact returned Bridge envelope;
2. preserve `request_executed`, `provider_calls`, `progress`, item state and provider operation ID if returned;
3. persist that evidence to GitHub before any collect;
4. remote-readback the persisted evidence;
5. if the item is `WAITING`, do not resubmit and do not collect until a separate due-time collection release is published and remote-read back;
6. if the submission itself fails or becomes unknown, preserve failure truth and stop; do not blind retry.

## 5. Publication-time boundary

This file does not itself execute the provider request.

```text
PROVIDER_SUBMISSIONS_ALLOWED_BEFORE_RELEASE_READBACK = 0
PROVIDER_COLLECTIONS_ALLOWED = 0
PROVIDER_CALLS_EXECUTED_BY_THIS_RELEASE = 0
S06Q003_RELEASED = false
```

## 6. Verdict

```text
S06Q002_R1_EXACT_ONE_SUBMIT_RELEASE_PUBLICATION = PASS
REMOTE_READBACK_REQUIRED_BEFORE_SUBMIT = true
SECOND_PROVIDER_SUBMIT_ALLOWED = false
S06Q003_RELEASED = false
```
