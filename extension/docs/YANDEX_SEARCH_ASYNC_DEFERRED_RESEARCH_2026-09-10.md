# YANDEX SEARCH API — DEFERRED / ASYNC MODE RESEARCH FOR BRIDGE

Date: 2026-09-10
Status: **TECHNICAL RESEARCH COMPLETE / NO CODE CHANGE YET**
Scope: assess whether Yandex Marketing Bridge can use deferred ordinary Web Search and how the lifecycle must work.

## 1. Official provider model

Official docs:

- Concepts: https://aistudio.yandex.ru/ru/docs/search-api/concepts/
- Text search concepts: https://aistudio.yandex.ru/ru/docs/search-api/concepts/web-search
- Deferred execution guide: https://aistudio.yandex.ru/ru/docs/search-api/operations/web-search
- REST async endpoint: https://aistudio.yandex.ru/ru/docs/search-api/api-ref/WebSearchAsync/search
- Operation API: https://aistudio.yandex.ru/ru/docs/search-api/api-ref/Operation/
- Quotas/limits: https://aistudio.yandex.ru/ru/docs/search-api/concepts/limits
- Pricing: https://aistudio.yandex.ru/ru/docs/search-api/pricing

Provider lifecycle:

```text
POST https://searchapi.api.cloud.yandex.net/v2/web/searchAsync
-> returns Operation immediately
-> save operation.id
-> result is NOT immediately available
-> wait / later poll
GET https://operation.api.cloud.yandex.net/operations/<operation_id>
-> done=false: still processing
-> done=true + response.rawData: result ready
-> decode Base64 XML/HTML
-> normalize/persist/query QA
```

Official documentation states processing can take from five minutes to several hours.

## 2. Time and retention

Current official limits:

```text
minimum deferred processing time = 5 minutes
maximum retention time of deferred results = 12 hours
```

Implication:
- this is not an interactive request path;
- do not hold one browser/tool call open waiting;
- operation IDs must be durably persisted immediately;
- collection must occur before provider retention expires.

Safe project rule should treat 12 hours as a hard retrieval deadline and should collect substantially earlier.

## 3. Quotas

Current official quotas:

```text
deferred requests/hour = 35,000
deferred requests/second = 10
operation-result GET requests/second = 10
```

This means a 500/1000/1500-query semantic batch is technically compatible with the provider's published default deferred quotas.

Each query is still a separate billed Search request / operation. `Deferred batch` means orchestrating many asynchronous operations; it is not one POST containing 1500 different query texts.

## 4. Pricing

Current RUB prices incl. VAT per 1000 requests:

```text
day synchronous = 488 RUB
day deferred = 30.5 RUB
night synchronous = 366 RUB
night deferred = 25.41 RUB
```

Night window in current pricing: 00:00:00–07:59:59 UTC+3.

Examples, one Search request per phrase:

```text
500 deferred day = 15.25 RUB
1000 deferred day = 30.50 RUB
1500 deferred day = 45.75 RUB
1500 deferred night = 38.115 RUB
```

Cost savings are material, but provider price alone cannot authorize switching a Kwork method or Bridge transport. The new path requires capability implementation + regression validation.

## 5. Current Bridge truth

Current repository implementation checked at 2026-09-10:

### `extension/src/shared/search_protocol.js`

Current ordinary Search endpoint:

```text
/v2/web/search
```

Current cost constant:

```text
CONSERVATIVE_SYNC_COST_RUB = 0.488
```

No accepted async ordinary-Search method is exposed by the current `SEARCH_API_V1` command schema.

### `extension/src/shared/search_batch_runtime.js`

Strengths already reusable:

```text
batch jobs durably stored in chrome.storage.local
job/item IDs
cost/request admission
pause/resume/cancel/status
recovery through recoverAll()
per-item result payload persistence
```

Current limitation:
The runtime assumes one provider call reaches terminal success/failure in the same `next` execution. An async submission returns only an Operation object and is therefore neither ordinary `SUCCEEDED` nor ordinary synchronous `REQUEST_STARTED` completion.

### `extension/src/shared/provider_batch_job_model.js`

Current item states:

```text
PENDING
CLAIMED
REQUEST_STARTED
SUCCEEDED
FAILED_TERMINAL
OUTCOME_UNKNOWN
SKIPPED
CANCELLED
```

Missing durable state equivalent to:

```text
ASYNC_SUBMITTED / WAITING_PROVIDER_RESULT
```

### `extension/src/manifest.json`

Current host permissions include:

```text
https://searchapi.api.cloud.yandex.net/*
```

But async result collection requires access to:

```text
https://operation.api.cloud.yandex.net/*
```

Current extension permissions do not include `alarms`.

## 6. Can we implement deferred Search in this extension?

**YES — technically feasible.**

The current architecture already has the most important foundation: durable batch state in `chrome.storage.local` and recovery after worker/session interruption.

But this is a real new provider lifecycle, not a one-line endpoint substitution.

## 7. Recommended Bridge design

### 7.1 New ordinary Search transport mode

Add an explicit mode, for example:

```text
transportMode = SYNC | DEFERRED
```

Do not silently change existing `search` semantics.

Existing sync remains backward-compatible.

Deferred submission:

```text
query item
-> POST /v2/web/searchAsync
-> receive operation_id
-> mark request billed/submitted
-> persist operation_id + submitted_at immediately
-> release item from synchronous active lock
-> state = WAITING_PROVIDER_RESULT
```

### 7.2 Required item fields

At minimum:

```text
operation_id
async_submitted_at
last_polled_at
poll_count
provider_done
provider_modified_at
result_collected_at
result_retention_deadline_or_safe_collect_deadline
raw_result_ref
normalized_result_ref
```

### 7.3 Required state-machine change

Add an in-progress asynchronous state such as:

```text
WAITING_PROVIDER_RESULT
```

This state:
- is not terminal;
- must not block submission of the next independent item;
- must count as a provider request already started/billed;
- must survive browser/service-worker restarts;
- becomes SUCCEEDED only after result is actually collected, parsed and persisted;
- becomes explicit terminal/expired/error state only with governed evidence.

### 7.4 Submission and collection are separate actions

Recommended command model:

```text
start
submit
submitN
status
collect
collectN
collectReady
pause
resume
cancel-local
```

Do not overload current sync `next` so heavily that its existing semantics become ambiguous.

### 7.5 Polling strategy

Do NOT poll immediately after submit: provider minimum processing time is 5 minutes.

Suggested conservative lifecycle:

```text
T0: submit many operations under <=10 requests/sec
T0: persist each operation ID immediately
T0+5m or later: first collection sweep
for pending operations:
  poll under <=10 operation GET/sec
  collect all done results
  persist raw + normalized immediately
  leave done=false as WAITING
later: repeat with backoff
stop when all terminal or safe deadline reached
```

A 1500-operation full poll sweep at the provider's 10 GET/sec ceiling takes at least about 150 seconds even before network/processing overhead. Therefore polling every operation every few seconds is wasteful.

## 8. Do we literally wait in one ChatGPT/extension interaction for hours?

**No. That would be the wrong architecture.**

Correct user experience:

```text
1. ChatGPT/owner authorizes deferred batch.
2. Bridge submits operations and stores IDs.
3. Bridge returns immediately: SUBMITTED / WAITING.
4. Chat may continue with independent work or close.
5. Later Bridge checks operations.
6. As results become ready they are stored/normalized.
7. ChatGPT asks status/readback and continues analytical step only after required coverage is complete.
```

The Yandex jobs run provider-side after submission. The ChatGPT conversation does not need to stay open for several hours.

## 9. Manual vs automatic collection options

### Option A — manual deferred collection, smallest patch

No background alarm required.

```text
submitN
-> user/ChatGPT returns after >=5 min
-> collectReady/collectN
-> if some pending, repeat later
```

Advantages:
- simpler implementation/test surface;
- no long-lived background scheduler;
- naturally preserves owner-visible checkpoints.

Disadvantage:
- operator must return before retention expiry.

### Option B — automatic background collection

Use Chrome MV3 `chrome.alarms` or equivalent validated scheduler to wake the service worker periodically while the browser is running.

Required manifest changes include at least:

```text
permission: alarms
host_permission: https://operation.api.cloud.yandex.net/*
```

Advantages:
- results collected without keeping ChatGPT open;
- lower risk of missing the 12-hour retention window.

Disadvantages:
- larger patch/test surface;
- Chrome service-worker suspension/restart behavior must be tested;
- if the entire browser/computer is off, alarms cannot collect until Chrome runs again.

### Recommended first implementation

Build and validate **Option A first**, because it proves provider semantics and persistence with minimal moving parts.

After live acceptance, add Option B only if unattended collection materially improves the product workflow.

## 10. Browser closed / PC off

Yandex operations are provider-side, so submitted operations continue independently of the browser.

The extension cannot poll while Chrome is not running.

On reopen:

```text
recover persisted job
-> identify WAITING_PROVIDER_RESULT items
-> poll operation IDs
-> collect still-retained results
```

Risk:
If the result has already aged beyond the provider's retention window, collection can fail. Therefore a production workflow must surface the retrieval deadline and not rely on the owner returning "sometime tomorrow".

## 11. Result format compatibility

Official async Search returns `response.rawData` containing Base64 XML or HTML, analogous to the ordinary text-search result payload.

Therefore the current XML normalization machinery is likely reusable after extracting `operation.response.rawData`.

This must be proven by tests; do not claim compatibility only because the field name matches.

## 12. Authentication / host boundary

Official deferred guide shows IAM-token authorization for both async submit and Operation GET. Current synchronous docs also support API-key access.

Before implementation, test the exact credential type currently stored by Bridge against BOTH:

```text
POST searchAsync
GET operation
```

Do not assume that existing sync authentication is sufficient until live canary proves the exact path.

## 13. Required tests before product use

At minimum:

```text
ASYNC SUBMIT CANARY PASS
OPERATION ID DURABLY SAVED BEFORE NEXT SUBMIT
DONE=false POLL PASS
DONE=true RESULT COLLECTION PASS
RAW XML NORMALIZATION PARITY PASS
BROWSER/SERVICE-WORKER RESTART RECOVERY PASS
DUPLICATE COLLECT IDEMPOTENCY PASS
PARTIAL BATCH RECOVERY PASS
PROVIDER ERROR / OPERATION ERROR PASS
AUTH FAILURE PASS
RATE-LIMIT HANDLING PASS WITHOUT BLIND AUTO-RETRY
RESULT-RETENTION/EXPIRED STATE PASS
COST ACCOUNTING PASS
SYNC MODE REGRESSION PASS
NO DOUBLE BILLING CAUSED BY RECOVERY PASS
```

Do not switch a Kwork to deferred production until these gates pass.

## 14. Recommended use in Kwork portfolio

Deferred Search is particularly attractive for products whose frozen SERP mode is FULL and whose client does not require instant interactive results.

It can also serve large selective batches.

Do not use it for:
- GenSearch/generative response: current Yandex docs list generative response as synchronous-only;
- interactive one-off checks where low latency is important and sync cost is acceptable;
- a product whose method does not require ordinary Search at all.

## 15. Current decision

```text
PROVIDER_SUPPORTS_DEFERRED_TEXT_SEARCH = true
CURRENT_BRIDGE_SUPPORTS_DEFERRED_SEARCH = false
BRIDGE_PATCH_FEASIBLE = true
CODE_PATCH_AUTHORIZED = false
RECOMMENDED_FIRST_PATCH_SCOPE = MANUAL_ASYNC_SUBMIT + DURABLE OPERATION IDS + LATER COLLECT
AUTOMATIC_BACKGROUND_POLLING = OPTIONAL SECOND PHASE
```

No extension source was modified by this research.