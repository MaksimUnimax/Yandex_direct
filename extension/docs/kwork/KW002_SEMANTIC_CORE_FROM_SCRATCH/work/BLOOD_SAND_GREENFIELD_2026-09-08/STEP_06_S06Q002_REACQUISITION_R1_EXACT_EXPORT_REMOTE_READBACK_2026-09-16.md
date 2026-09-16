# KW-002 Step06 — S06Q002 CONTROLLED REACQUISITION R1 EXACT EXPORT REMOTE READBACK

Date: 2026-09-16
Status: **PASS / EXACT EXPORT + CLOSURE + CURSOR V52 VERIFIED / S06Q002 MAY BE DURABLY CLOSED**

## 1. Scope

```text
QUERY_ID = S06Q002
QUERY_TEXT = оберег
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q002-r1-20260916
PROVIDER_OPERATION_ID = sprriom53ppme5q13epe
```

## 2. Live remote truth

```text
BRANCH = roadmap/kwork-productization-2026-08-28
HEAD = 258dbdffbddb7c2162d6b95672c6acad16666030
HEAD_MESSAGE = docs(kw002): persist S06Q002 R1 exact export state
EXACT_EXPORT_FILE = search-kw002-s06q002-r1-20260916-r5-0-0.json
EXACT_EXPORT_SIZE_BYTES = 58270
EXACT_EXPORT_SHA256 = 58a4788534511e7319185ead2b097522aefcf485f5130b1dea1b028eaafa8596
EXACT_EXPORT_GIT_BLOB_SHA = 7a77cd154b582fac1a5893f4ce5b1c06bcd42f07
EXACT_EXPORT_PERSIST_COMMIT = 3d9d9bbb0e547c0f120a7c4d06dd63986ffbadc2
CLOSURE_FILE = STEP_06_S06Q002_REACQUISITION_R1_EXACT_EXPORT_CLOSURE_2026-09-16.md
CLOSURE_BLOB_SHA = fa28316dd42ecffffd95290d9be7b7cc466e465a
CURSOR_SCHEMA = KW002_CURRENT_EXECUTION_CURSOR_V52
CURSOR_BLOB_SHA = dfca4a1f1ada2ad71cd1d4e2efe778b43140e3e1
```

The remote exact export blob SHA equals the Git blob SHA independently computed from the original Bridge attachment before publication. This proves byte identity of the persisted JSON.

## 3. Export completeness readback

The remote JSON readback confirms:

```text
schema = YMB_SEARCH_ASYNC_EXPORT_PAGE_V1
job_id = kw002-s06q002-r1-20260916
revision = 5
total_items = 1
item_state = SUCCEEDED
operation_id = sprriom53ppme5q13epe
raw_present = true
normalized_present = true
result_count = 20
document_count = 20
ranks = 1..20
unique_urls = 20
unique_domains = 6
usable_for_url_comparison = true
missing_url_ranks = []
unsafe_url_ranks = []
all_job_items_in_this_file = true
has_more = false
```

Domain distribution read back from the exact normalized SERP:

```text
www.ozon.ru = 8
www.wildberries.ru = 8
slavyanskieoberegi.ru = 1
blog.beregy.ru = 1
market.yandex.ru = 1
dzen.ru = 1
```

## 4. Lifecycle accounting readback

```text
provider_submit_calls = 1
provider_collect_calls = 1
local_no_due_collect_commands = 1
local_no_due_provider_calls = 0
requests_started = 1
operations_accepted = 1
polls_started = 1
unresolved = 0
all_successful = true
revision = 5
```

The historical pre-0.1.8 S06Q002 attempt remains preserved but superseded for current evidence. The R1 attempt is the current exact authority.

## 5. Closure boundary

```text
EXACT_EXPORT_REMOTE_READBACK_PASS = true
S06Q002_R1_CURRENT_EVIDENCE_MAY_BE_DURABLY_CLOSED = true
DEFERRED_SEARCH_LOCAL_STARTS_ALLOWED = 0
DEFERRED_SEARCH_SUBMISSIONS_ALLOWED = 0
DEFERRED_SEARCH_COLLECTIONS_ALLOWED = 0
DEFERRED_SEARCH_EXPORTS_ALLOWED = 0
SYNCHRONOUS_SEARCH_CALLS_ALLOWED = 0
WORDSTAT_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
STEP07_STARTED = false
STEP08_STARTED = false
PROVIDER_CALLS_DURING_THIS_READBACK = 0
```

This readback closes only S06Q002 evidence durability. It does not release S06Q003 or make a new analytical conclusion.

## 6. Verdict

```text
S06Q002_R1_EXACT_EXPORT_REMOTE_READBACK = PASS
BYTE_IDENTITY_REMOTE = PASS
RAW_AND_NORMALIZED_COMPLETENESS = PASS
S06Q002_R1_DURABLE_CLOSURE_ALLOWED = true
S06Q003_RELEASED = false
PROVIDER_CALLS_DURING_READBACK = 0
```
