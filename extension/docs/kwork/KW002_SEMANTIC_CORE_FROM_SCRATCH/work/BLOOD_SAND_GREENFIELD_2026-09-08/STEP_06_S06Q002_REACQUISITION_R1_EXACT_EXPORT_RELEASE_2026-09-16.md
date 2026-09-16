# KW-002 Step06 — S06Q002 CONTROLLED REACQUISITION R1 EXACT EXPORT RELEASE

Date: 2026-09-16
Status: **PUBLISHED FOR EXACTLY ONE LOCAL EXPORT / ACTIVATION REQUIRES REMOTE READBACK / ZERO PROVIDER CALLS**

## 1. Scope

```text
QUERY_ID = S06Q002
QUERY_TEXT = оберег
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q002-r1-20260916
PROVIDER_OPERATION_ID = sprriom53ppme5q13epe
JOB_REVISION = 5
```

The provider lifecycle is complete and remote-read back:

```text
provider_submit_calls = 1
provider_collect_calls = 1
SUCCEEDED = 1
unresolved = 0
all_successful = true
revision = 5
```

## 2. Exact local export command

After this release and successor cursor are remote-read back, exactly one local export may be executed:

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"exportPage","jobId":"kw002-s06q002-r1-20260916","after":-1,"limit":1,"revision":5}
```

Expected execution boundary:

```text
request_executed = false
provider_calls = 0
```

The export must materialize the one complete job item with preserved raw provider response and normalized result payload. No summary-only substitute is acceptable.

## 3. Hard boundary

```text
EXACT_LOCAL_EXPORTS_TO_AUTHORIZE_AFTER_REMOTE_READBACK = 1
SECOND_EXPORT_PREAUTHORIZED = false
PROVIDER_SUBMISSIONS_ALLOWED = 0
PROVIDER_COLLECTIONS_ALLOWED = 0
SYNCHRONOUS_SEARCH_CALLS_ALLOWED = 0
WORDSTAT_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
STEP07_STARTED = false
STEP08_STARTED = false
```

## 4. Required handling

Immediately after export:

1. preserve the exact returned export envelope and delivered artifact identity;
2. verify revision remains 5 and exported item identity is index 0 / operation `sprriom53ppme5q13epe`;
3. persist the exact exported JSON into the KW002 job evidence directory without truncation;
4. verify normalized result completeness, rank/URL/domain/title/snippet/modtime fields as actually present;
5. remote-readback the exact persisted export;
6. only after durable closure may S06Q003 be considered separately.

## 5. Verdict

```text
S06Q002_R1_EXACT_EXPORT_RELEASE_PUBLICATION = PASS
REMOTE_READBACK_REQUIRED_BEFORE_EXPORT = true
PROVIDER_CALLS_EXECUTED_BY_THIS_RELEASE = 0
S06Q003_RELEASED = false
```
