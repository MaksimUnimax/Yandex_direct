# KW-002 Step06 — S06Q002 CONTROLLED REACQUISITION R1 COLLECTION RELEASE R2

Date: 2026-09-16
Status: **PUBLISHED FOR EXACTLY ONE DUE COLLECTION ATTEMPT / ACTIVATION REQUIRES REMOTE READBACK / NO RESUBMIT**

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

## 2. Why this is R2

The first released `collectN count=1` command returned locally:

```text
request_executed = false
provider_calls = 0
last.code = NO_DUE_OPERATIONS
polls_started = 0
revision = 2
```

Therefore it did not claim the item and did not execute a provider poll. Its exact truth is preserved under:

- `STEP_06_S06Q002_REACQUISITION_R1_COLLECT_NO_DUE_EVIDENCE_2026-09-16.md`
- `STEP_06_S06Q002_REACQUISITION_R1_COLLECT_NO_DUE_REMOTE_READBACK_2026-09-16.md`

## 3. Corrected timing basis

The previous external approximation `12:16 +05:00` was too early and is superseded for scheduling.

Repository evidence establishes:

```text
SUBMIT_ACCEPTED_EVIDENCE_COMMIT = 14078e3b7ad5910506680def01a12565eef5221b
SUBMIT_ACCEPTED_EVIDENCE_COMMIT_TIME = 2026-09-16T07:31:32Z = 2026-09-16T12:31:32+05:00
V46_CONSERVATIVE_NOT_BEFORE = 2026-09-16T12:36:54+05:00
LIVE_TIME_CHECK = 2026-09-16T12:36:57+05:00
V46_CONSERVATIVE_GUARD_ELAPSED = true
```

YMB 0.1.8 runtime sets `nextPollAt = clock() + 300000` at durable submit completion and the store admits collection only when `next_poll_at <= now`. The runtime due check remains authoritative at execution.

## 4. Exact command

After this release and its successor cursor are remote-read back, exactly one collection command may be executed:

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"collectN","jobId":"kw002-s06q002-r1-20260916","count":1}
```

## 5. Hard boundary

```text
EXACT_COLLECTION_COMMANDS_TO_AUTHORIZE_AFTER_REMOTE_READBACK = 1
PROVIDER_SUBMIT_CALLS = 1
PROVIDER_COLLECT_CALLS_SO_FAR = 0
LOCAL_NO_DUE_COLLECT_COMMANDS_SO_FAR = 1
SECOND_PROVIDER_SUBMIT_ALLOWED = false
AUTOMATIC_RETRY = false
SYNCHRONOUS_SEARCH_FALLBACK = false
GENSEARCH_FALLBACK = false
WORDSTAT_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
STEP07_STARTED = false
STEP08_STARTED = false
```

If runtime again returns `NO_DUE_OPERATIONS`, preserve that exact truth and do not count it as a provider collect. If a provider poll executes, preserve its exact returned envelope before any further action.

## 6. Required handling of result

1. preserve exact Bridge envelope;
2. preserve `request_executed`, `provider_calls`, `processed`, `normalized`, `last`, `progress`, operation id and revision;
3. no resubmit;
4. no automatic second collect;
5. if result is received, preserve raw and normalized evidence without truncation;
6. persist collection evidence and remote-readback it before any export release;
7. do not release S06Q003 until exact export and closure are durably completed.

## 7. Verdict

```text
S06Q002_R1_COLLECTION_RELEASE_R2_PUBLICATION = PASS
REMOTE_READBACK_REQUIRED_BEFORE_COLLECT = true
PROVIDER_COLLECTION_CALLS_EXECUTED_BY_THIS_RELEASE = 0
SECOND_PROVIDER_SUBMIT_ALLOWED = false
S06Q003_RELEASED = false
```
