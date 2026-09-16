# KW-002 Step06 — S06Q002 CONTROLLED REACQUISITION R1 COLLECTION RELEASE

Date: 2026-09-16
Status: **PUBLISHED FOR EXACTLY ONE COLLECTION ATTEMPT / ACTIVATION REQUIRES REMOTE READBACK / NO RESUBMIT**

## 1. Scope

```text
QUERY_ID = S06Q002
QUERY_TEXT = оберег
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q002-r1-20260916
PROVIDER_OPERATION_ID = sprriom53ppme5q13epe
CURRENT_ITEM_STATE = WAITING
SUBMIT_REVISION = 2
```

## 2. Release basis

The exact provider submit was accepted once and persisted under:

- `STEP_06_S06Q002_REACQUISITION_R1_SUBMIT_ACCEPTED_EVIDENCE_2026-09-16.md`
- `STEP_06_S06Q002_REACQUISITION_R1_SUBMIT_ACCEPTED_REMOTE_READBACK_2026-09-16.md`

Verified state before collection:

```text
provider_submit_calls = 1
provider_collect_calls = 0
requests_started = 1
operations_accepted = 1
polls_started = 0
WAITING = 1
unresolved = 1
operation_id = sprriom53ppme5q13epe
revision = 2
```

## 3. Due-time guard

```text
SUBMIT_RESULT_OBSERVED_AT = 2026-09-16T12:16:00+05:00
CONSERVATIVE_COLLECTION_NOT_BEFORE = 2026-09-16T12:21:00+05:00
LIVE_TIME_CHECK = 2026-09-16T12:32:34+05:00
CONSERVATIVE_GUARD_ELAPSED = true
```

The external five-minute guard has elapsed. The Bridge runtime's persisted due state remains authoritative at execution; if runtime reports not-due or otherwise refuses collection, preserve that exact truth and do not retry automatically.

## 4. Exact command

After this release and its successor cursor are remote-read back, exactly one collection attempt may be executed:

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"collectN","jobId":"kw002-s06q002-r1-20260916","count":1}
```

## 5. Hard boundary

```text
EXACT_COLLECTION_ATTEMPTS_TO_AUTHORIZE_AFTER_REMOTE_READBACK = 1
SECOND_COLLECTION_ATTEMPT_PREAUTHORIZED = false
SECOND_PROVIDER_SUBMIT_ALLOWED = false
LOCAL_START_ALLOWED = false
AUTOMATIC_RETRY = false
SYNCHRONOUS_SEARCH_FALLBACK = false
GENSEARCH_FALLBACK = false
WORDSTAT_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
STEP07_STARTED = false
STEP08_STARTED = false
```

## 6. Required handling of collection result

Immediately after the one `collectN`:

1. preserve the exact returned Bridge envelope;
2. preserve `request_executed`, `provider_calls`, `processed`, `normalized`, `last`, `progress`, operation id and revision;
3. do not collect again automatically if the operation is still waiting;
4. if a result is received, preserve raw result and normalized result without truncation;
5. persist collection evidence before any export or next query;
6. remote-readback the evidence before any export release;
7. do not release S06Q003 until exact export and closure are durably completed.

## 7. Publication verdict

```text
S06Q002_R1_COLLECTION_RELEASE_PUBLICATION = PASS
REMOTE_READBACK_REQUIRED_BEFORE_COLLECT = true
PROVIDER_COLLECTION_CALLS_EXECUTED_BY_THIS_RELEASE = 0
SECOND_PROVIDER_SUBMIT_ALLOWED = false
S06Q003_RELEASED = false
```
