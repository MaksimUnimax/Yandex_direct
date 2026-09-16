# KW-002 Step06 — S06Q003..S06Q022 ASYNC QUEUE CONTROL PASS REMOTE READBACK

Date: 2026-09-16
Status: **PASS / CONTROL AUTHORITY + CURSOR V54 EXACT REMOTE READBACK VERIFIED / LOCAL START MAY BE RELEASED**

## 1. Read back commit

```text
BRANCH = roadmap/kwork-productization-2026-08-28
COMMIT = 62f60e1a8139e96cf7db7cdede26b1486a34aa16
MESSAGE = docs(kw002): establish Step06 async queue control pass
TREE = 0014e686b50b1c080b12629a291df11be069ea60
PARENT = 1f56a5ad3d7086c0930882c49b105e6cafe5b8d4
```

The branch update was a normal fast-forward; force-push was not used.

## 2. Exact control authority readback

```text
FILE = STEP_06_S06Q003_Q022_ASYNC_QUEUE_CONTROL_PASS_2026-09-16.md
EXPECTED_GIT_BLOB_SHA = 7ec5dc62d3af1d2b014d30044cec10a1c33b6cd6
REMOTE_GIT_BLOB_SHA = 7ec5dc62d3af1d2b014d30044cec10a1c33b6cd6
MATCH = true
```

The remote file contains the complete provider-free control decision selecting one durable `SEARCH_ASYNC_BATCH_API_V1` job for S06Q003..S06Q022, one independently attributable item per query, transactional local durability between provider operations, conservative UNKNOWN freeze, and one final exact export + Git remote-readback barrier before Step07.

## 3. Exact cursor V54 readback

```text
FILE = KW002_EXECUTION_CURSOR_2026-09-11.json
SCHEMA = KW002_CURRENT_EXECUTION_CURSOR_V54
EXPECTED_GIT_BLOB_SHA = 7b2429b6bedd368ee2b95e331aab42d056971470
REMOTE_GIT_BLOB_SHA = 7b2429b6bedd368ee2b95e331aab42d056971470
MATCH = true
```

V54 correctly kept all provider permissions at zero and required this readback before any queue release.

## 4. Source-contract confirmation used by the control pass

Live YMB 0.1.9 authority remains:

```text
BRANCH = hotfix/ymb-file-delivery-p0-2026-09-14
HEAD = b218afb0187bd26af1d7ada3590b02edc2d4a2de
search_protocol.js = 49ca9a6f3a2786a3107f03d0724dfca7578cd096
search_async_protocol.js = 91df9051f4cf52d51ee73af9c66a196411a966d7
search_async_store.js = 1de12e529141649eb4a0f94cac155ab32f38b0dd
search_async_runtime.js = 571debe536e634aad1ed280f215c4e35b19925ae
search_async_policy.js = e18de13b36a617fc8fa78203459d8947869687f9
search_async_worker_transport.js = 75c5349531d7fb77641991d648cfb8b40a490bdc
```

The ordinary Search protocol hardcodes `responseFormat = FORMAT_XML`; the async protocol builds each deferred submit through that ordinary Search request builder. Therefore the multi-item start command does not need, and must not add, a separate unsupported `responseFormat` field.

## 5. Release boundary after successful readback

The successor cursor may release exactly one provider-free local start:

```text
JOB_ID = kw002-s06q003-q022-20260916
QUERY_COUNT = 20
MAX_REQUESTS = 20
MAX_COST_RUB = 0.61
LOCAL_STARTS_ALLOWED = 1
PROVIDER_SUBMITS_ALLOWED = 0
PROVIDER_COLLECTIONS_ALLOWED = 0
LOCAL_EXPORTS_ALLOWED = 0
SYNCHRONOUS_SEARCH_ALLOWED = 0
WORDSTAT_ALLOWED = 0
GENSEARCH_ALLOWED = 0
AI_SEARCH_ALLOWED = 0
STEP07_STARTED = false
```

The local start must create the durable 20-item job only. Expected provider accounting for the start itself is:

```text
request_executed = false
provider_calls = 0
```

Only after that local start result is observed and durably recorded may a later successor release bounded `submitN`.

## 6. Verdict

```text
CONTROL_AUTHORITY_REMOTE_READBACK = PASS
CURSOR_V54_REMOTE_READBACK = PASS
CONTROL_PASS_DURABLY_VERIFIED = true
ONE_PROVIDER_FREE_LOCAL_START_MAY_BE_RELEASED = true
PROVIDER_CALLS_DURING_CONTROL_AND_READBACK = 0
STEP07_STARTED = false
```
