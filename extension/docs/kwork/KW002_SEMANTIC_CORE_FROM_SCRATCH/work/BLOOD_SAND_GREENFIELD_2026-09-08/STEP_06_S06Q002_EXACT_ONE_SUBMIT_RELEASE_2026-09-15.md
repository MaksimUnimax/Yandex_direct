# KW-002 Step06 — S06Q002 EXACT ONE SUBMIT RELEASE

Date: 2026-09-15
Status: **PUBLISHED FOR EXACTLY ONE DEFERRED PROVIDER SUBMISSION / ACTIVATION REQUIRES REMOTE READBACK**

## 1. Scope

This authority covers only the already-started S06Q002 job.

```text
QUERY_ID = S06Q002
QUERY_TEXT = оберег
JOB_ID = kw002-s06q002-20260915
TRANSPORT = DEFERRED_ASYNC
```

The local start has already passed and has been persisted and remote-read back under:

- `STEP_06_S06Q002_LOCAL_START_PASS_EVIDENCE_2026-09-15.md`
- `STEP_06_S06Q002_LOCAL_START_REMOTE_READBACK_2026-09-15.md`

Current local job truth before any provider call:

```text
CONTROL = RUNNING
TOTAL = 1
PENDING = 1
REQUESTS_STARTED = 0
OPERATIONS_ACCEPTED = 0
POLLS_STARTED = 0
REVISION = 0
PROVIDER_CALLS = 0
```

## 2. Exact provider submission contract

After this release and its successor cursor are remote-read back and activation is recorded, exactly one deferred provider submission may be executed:

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"submitN","jobId":"kw002-s06q002-20260915","count":1}
```

This command must operate on the existing local job. No replacement `start`, no different job ID, no second submit and no synchronous fallback are allowed.

The existing job budget remains:

```text
MAX_REQUESTS = 1
MAX_COST_RUB = 0.0305
```

## 3. Publication-time boundary

This release publication itself does not authorize an immediate provider call until its remote readback is complete.

```text
LOCAL_STARTS_ALLOWED_NOW = 0
PROVIDER_SUBMISSIONS_ALLOWED_BEFORE_RELEASE_READBACK = 0
PROVIDER_COLLECTIONS_ALLOWED_NOW = 0
SYNCHRONOUS_SEARCH_CALLS_ALLOWED = 0
WORDSTAT_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
STEP07_STARTED = false
STEP08_STARTED = false
PROVIDER_CALLS_ALREADY_EXECUTED_FOR_S06Q002 = 0
```

## 4. Required handling of the submit result

After the one submit:

1. preserve the exact returned `SEARCH_ASYNC_BATCH_RESULT_V1` envelope;
2. preserve `request_executed`, `provider_calls`, job progress, request accounting and any returned operation identity;
3. if state becomes `WAITING`, persist the exact pending operation before any collection is even considered;
4. if a result is immediately available, preserve the full result truth without truncation;
5. do not call `submitN` again under any outcome;
6. do not call `collectN` until the exact post-submit state has been persisted, remote-read back, and collection is separately admitted when due.

Automatic retry and blind resubmission are forbidden.

## 5. Outcome contract

- `WAITING` with an operation ID → persist exact operation identity and stop provider progression.
- immediate `SUCCEEDED` → persist complete raw + normalized evidence and close under the normal evidence gate.
- validation/provider/unknown failure → preserve failure truth; no retry and no competitor inference.
- evidence incomplete → stop unresolved.

## 6. Interpretation boundary

This one provider submission is only a Step06 competitor-discovery acquisition for the exact query `оберег`. It is not final competitor membership, final intent, final clustering, page ownership, architecture, or Step12 full-SERP coverage.

## 7. Publication verdict

```text
S06Q002_EXACT_ONE_SUBMIT_RELEASE_PUBLICATION = PASS
SUBMIT_RELEASE_REMOTE_READBACK_REQUIRED = true
PROVIDER_SUBMISSION_ALLOWED_BEFORE_READBACK = false
SECOND_LOCAL_START_ALLOWED = false
SECOND_PROVIDER_SUBMIT_ALLOWED = false
S06Q003_RELEASED = false
```
