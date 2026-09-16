# KW-002 Step06 — S06Q002 CONTROLLED REACQUISITION R1 EXACT EXPORT CLOSURE

Date: 2026-09-16
Status: **EXACT EXPORT PERSISTED / BYTE IDENTITY VERIFIED / REMOTE CLOSURE READBACK REQUIRED**

## 1. Scope

```text
QUERY_ID = S06Q002
QUERY_TEXT = оберег
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q002-r1-20260916
PROVIDER_OPERATION_ID = sprriom53ppme5q13epe
YMB_VERSION = 0.1.8
JOB_REVISION = 5
```

## 2. Exact exported authority

```text
FILE = search-kw002-s06q002-r1-20260916-r5-0-0.json
SIZE_BYTES = 58270
SHA256 = 58a4788534511e7319185ead2b097522aefcf485f5130b1dea1b028eaafa8596
GIT_BLOB_SHA = 7a77cd154b582fac1a5893f4ce5b1c06bcd42f07
PERSIST_COMMIT = 3d9d9bbb0e547c0f120a7c4d06dd63986ffbadc2
```

The GitHub commit adding the exact export reports the same Git blob SHA as the original Bridge file. The file therefore reached the research branch byte-for-byte, without JSON reserialization.

## 3. Export envelope invariants

```text
schema = YMB_SEARCH_ASYNC_EXPORT_PAGE_V1
job_id = kw002-s06q002-r1-20260916
revision = 5
total_items = 1
item_count = 1
items_with_raw = 1
items_with_normalized = 1
result_row_count = 20
all_job_items_in_this_file = true
has_more = false
item_index = 0
item_state = SUCCEEDED
operation_id = sprriom53ppme5q13epe
parse_error = null
```

Job summary in the export:

```text
requests_started = 1
operations_accepted = 1
polls_started = 1
SUCCEEDED = 1
all other item states = 0
unresolved = 0
all_successful = true
busy = false
revision = 5
reserved_microrub = 30500
max_requests = 1
max_cost_microrub = 30500
```

## 4. Raw + normalized completeness

The exact exported item contains both:

- the complete stored raw provider operation response (`raw_text`), including the provider `rawData` XML payload;
- the complete normalized SERP object.

Normalized validation:

```text
schema = YMB_ASYNC_XML_GUARD_V1
document_count = 20
result_count = 20
response_format = FORMAT_XML
empty_proven = false
xml_error_code = null
usable_for_url_comparison = true
missing_url_ranks = []
unsafe_url_ranks = []
```

Ranks are exactly `1..20`. There are 20 unique URLs and no missing rank/URL positions.

## 5. Domain distribution in the exact 20-result SERP

```text
www.ozon.ru = 8
www.wildberries.ru = 8
slavyanskieoberegi.ru = 1
blog.beregy.ru = 1
market.yandex.ru = 1
dzen.ru = 1
UNIQUE_DOMAINS = 6
UNIQUE_URLS = 20
```

This distribution is evidence from this exact bounded SERP only. It is not yet a final competitor ranking or final site-architecture conclusion.

## 6. Provider lifecycle accounting

```text
provider_submit_calls = 1
provider_collect_calls = 1
local_no_due_collect_commands = 1
local_no_due_provider_calls = 0
operation_id = sprriom53ppme5q13epe
result_received = true
normalized_items = 1
```

The earlier `NO_DUE_OPERATIONS` command was a local timing no-op and is not counted as a provider collection.

## 7. Hard boundary

```text
EXACT_EXPORT_PERSISTED = true
EXACT_EXPORT_REMOTE_READBACK_PASS = false
CURRENT_EVIDENCE_DURABLY_CLOSED = false
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
```

S06Q002 may be marked durably closed only after remote readback of the exact persisted JSON, this closure file, and successor canonical cursor.

## 8. Verdict

```text
S06Q002_R1_EXACT_EXPORT_PERSISTENCE = PASS
BYTE_IDENTITY = PASS
NORMALIZED_SERP_ROWS = 20
UNIQUE_URLS = 20
UNIQUE_DOMAINS = 6
REMOTE_READBACK_REQUIRED_FOR_DURABLE_CLOSURE = true
S06Q003_RELEASED = false
PROVIDER_CALLS_DURING_EXPORT_PERSISTENCE = 0
```
