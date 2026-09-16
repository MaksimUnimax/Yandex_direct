# KW-002 Step06 — S06Q003..S06Q022 ASYNC QUEUE CONTROL PASS

Date: 2026-09-16
Status: **PROVIDER-FREE CONTROL PASS COMPLETE / REMOTE READBACK REQUIRED / NO PROVIDER ACTION RELEASED YET**

## 1. Scope

This pass executes the provider-free control action required by `KW002_CURRENT_EXECUTION_CURSOR_V53` after durable closure of S06Q001 and S06Q002.

It does **not** change the fixed Step06 representative-query set, Search settings, competitor methodology, or the Step07 boundary. It only reconciles the safest execution shape for the remaining Step06 acquisition work.

```text
CLOSED = S06Q001, S06Q002
REMAINING = S06Q003..S06Q022
REMAINING_QUERY_COUNT = 20
PROVIDER_CALLS_DURING_THIS_CONTROL_PASS = 0
STEP07_STARTED = false
```

## 2. Authorities checked

Research authority:

- `STEP_06_PRE_EXECUTION_GATE_V2_2026-09-12.md`
- `STEP_06_22_REPRESENTATIVE_QUERIES_W10_2026-09-12.csv`
- `KW002_EXECUTION_CURSOR_2026-09-11.json` V53

Live Yandex Marketing Bridge authority:

```text
BRANCH = hotfix/ymb-file-delivery-p0-2026-09-14
HEAD = b218afb0187bd26af1d7ada3590b02edc2d4a2de
VERSION = 0.1.9
search_async_protocol.js blob = 91df9051f4cf52d51ee73af9c66a196411a966d7
search_async_store.js blob = 1de12e529141649eb4a0f94cac155ab32f38b0dd
search_async_runtime.js blob = 571debe536e634aad1ed280f215c4e35b19925ae
search_async_policy.js blob = e18de13b36a617fc8fa78203459d8947869687f9
search_async_worker_transport.js blob = 75c5349531d7fb77641991d648cfb8b40a490bdc
```

## 3. Control findings

### 3.1 `submitN` / `collectN` semantics

`SEARCH_ASYNC_BATCH_API_V1` supports one durable job with multiple unique queries. `submitN` and `collectN` are bounded orchestration loops, not provider-side batch requests.

Each loop iteration performs at most one ordinary deferred runtime step. The protocol caps one `submitN` / `collectN` command at 25 items. Therefore the 20 remaining Step06 queries fit inside the bounded slice count, while the worker time-slice may still stop early and return resumable state.

No cost saving is claimed from batching. There remains one paid Search submit per query.

### 3.2 Item isolation

The async store keeps independent items identified by `(job_id, index)` and stores, per item, the exact query, provider operation identity, state, raw result and normalized result.

The remaining 20 queries therefore remain independently attributable even when carried by one durable async job.

### 3.3 Transactional durability before the next provider call

Before a provider submit/collect is entered, the store claims the selected item in a single read-write IndexedDB transaction and persists:

```text
item state = SUBMITTING or COLLECTING
attempt identity
job lease
job counters / reserved budget where applicable
job revision
```

Provider completion is then settled through another transactional item/job update. Raw results are stored before normalization; normalized results are persisted against the same item identity.

This creates a durable local barrier between provider operations. The next item is not just an in-memory chat instruction.

### 3.4 Interrupted/ambiguous submit cannot blind-retry

Store recovery is conservative:

```text
interrupted SUBMITTING -> UNKNOWN
error_code = SUBMIT_INTERRUPTED_NO_RETRY
```

A job containing `UNKNOWN` blocks further submit admission until reconciliation. Interrupted collection is returned to WAITING because collection is a non-billable GET of an already accepted provider operation.

This preserves the earlier anti-regression rule that an ambiguous paid Search boundary must never be blindly repeated.

### 3.5 Cost and admission

The live shared admission guard uses a conservative Search submit ceiling:

```text
PRICE_MICRORUB = 30500
submit = paid
collect = 0 reserved_microrub
```

For the 20 remaining queries:

```text
MAX_PROVIDER_SUBMITS = 20
MAX_RESERVED_COST_MICRORUB = 610000
MAX_RESERVED_COST_RUB = 0.61
```

This is a conservative admission ceiling, not an invoice or a replacement for provider tariff evidence.

Admission is checked per attempt. A denied/held/uncertain attempt stops safe forward progress rather than silently consuming the next query.

## 4. Reconciliation with the old per-query GitHub-readback rule

`STEP_06_PRE_EXECUTION_GATE_V2_2026-09-12.md` required:

```text
one provider request
-> persist evidence
-> remote GitHub readback
-> then next provider request
```

That rule was a conservative compensating control before the now-live deferred runtime proved a durable transactional item store, explicit attempt identity, budget ledger, restart recovery, and no-blind-retry handling for ambiguous submits.

The control-pass decision is therefore:

```text
OLD BETWEEN-QUERY BARRIER
= GitHub commit + remote readback after every provider query

NEW BETWEEN-ITEM BARRIER FOR S06Q003..S06Q022
= transactional durable async item state + attempt/lease identity + shared admission ledger + conservative UNKNOWN freeze

FINAL EXTERNAL DURABILITY BARRIER
= exact export of the completed/closed remaining job + Git persistence + exact remote readback BEFORE Step07
```

This changes only the execution/durability placement. It does not weaken query identity, provider-result retention, normalization QA, or the requirement for exact remote evidence before analytical continuation.

## 5. Selected execution shape

Use **one** deferred async job for all remaining fixed queries, preserving one independent item per query:

```text
JOB_ID = kw002-s06q003-q022-20260916
TRANSPORT = SEARCH_ASYNC_BATCH_API_V1
ITEMS = 20
QUERY_IDS = S06Q003..S06Q022
MAX_REQUESTS = 20
MAX_COST_RUB = 0.61
CONFIRM_BILLABLE = true
```

Queries, in canonical order:

```text
S06Q003 талисман
S06Q004 аум
S06Q005 буддийский символ
S06Q006 ваджра
S06Q007 лотос
S06Q008 мантра
S06Q009 молот тора
S06Q010 мусульманский амулет
S06Q011 ом
S06Q012 подкова
S06Q013 руна
S06Q014 руна альгиз
S06Q015 руна отал
S06Q016 руна феху
S06Q017 славянский оберег
S06Q018 славянский символ
S06Q019 талисман удачи
S06Q020 улитка
S06Q021 фигурка будды
S06Q022 христианский символ
```

Search parameters remain exactly the accepted Step06 V2 contract:

```text
searchType = SEARCH_TYPE_RU
region = 225
page = 0
groupsOnPage = 20
groupMode = GROUP_MODE_FLAT
docsInGroup = 1
sortMode = SORT_MODE_BY_RELEVANCE
sortOrder = SORT_ORDER_DESC
familyMode = FAMILY_MODE_MODERATE
fixTypoMode = FIX_TYPO_MODE_OFF
responseFormat = FORMAT_XML
```

`responseFormat` is enforced by the Search request layer and strict async normalization contract; GenSearch/AI-search remain outside Step06.

## 6. Operator UX

The owner must not repeat the old full persistence/readback ceremony 20 times.

The intended operator flow becomes:

```text
1 local start for the 20-item durable job
-> bounded submitN over remaining pending items
-> bounded collectN over due operations as provider operations mature
-> status/itemsPage as needed
-> one exact final export set for the remaining job
-> Git persistence + exact remote readback
-> only then Step06 analytical reconciliation / eventual Step07 gate
```

The worker may return early because of its bounded time slice or because no operation is due yet. Reissuing the same bounded `submitN`/`collectN` action against the same job is continuation of one queue, not 20 manual per-query workflows.

No hidden background polling and no provider-side parallel burst are introduced.

## 7. Mandatory stop conditions

Stop the remaining queue and do not advance to Step07 if any of the following occurs:

```text
UNKNOWN item
FAILED item
PARSE_FAILED item
shared-admission hold/reconciliation requirement
owner/folder mismatch
revision/stale-attempt violation
provider operation ambiguity
unsafe or invalid normalized URL evidence
raw-result loss
exact-export incompleteness
```

A partial/failed remaining job must be preserved as evidence. Do not overwrite or silently restart it.

## 8. Final evidence requirements before Step07

The remaining-job closure must prove for every S06Q003..S06Q022 item:

```text
canonical query identity
provider submit accounting
provider operation identity
terminal item state
raw provider response retained
normalized SERP retained
result rows/ranks/URLs reconciled
validation/parse status
exact export completeness
Git blob identity / exact remote readback
```

Only after all Step06 query evidence is durably reconciled may domain recurrence / competitor selection proceed and only after Step06 closure may Step07 start.

## 9. Release boundary of this control-pass commit

```text
CONTROL_PASS_COMPLETE = true
CONTROL_PASS_REMOTE_READBACK_PASS = false
LOCAL_ASYNC_STARTS_ALLOWED_NOW = 0
PROVIDER_SUBMITS_ALLOWED_NOW = 0
PROVIDER_COLLECTIONS_ALLOWED_NOW = 0
LOCAL_EXPORTS_ALLOWED_NOW = 0
SYNCHRONOUS_SEARCH_ALLOWED_NOW = 0
WORDSTAT_ALLOWED_NOW = 0
GENSEARCH_ALLOWED_NOW = 0
AI_SEARCH_ALLOWED_NOW = 0
S06Q003_Q022_QUEUE_RELEASED = false
STEP07_STARTED = false
PROVIDER_CALLS_DURING_CONTROL_PASS = 0
```

The next action is exact remote readback of this authority and cursor V54. Only a successor cursor may release the provider-free local `start` for the remaining 20-item job.
