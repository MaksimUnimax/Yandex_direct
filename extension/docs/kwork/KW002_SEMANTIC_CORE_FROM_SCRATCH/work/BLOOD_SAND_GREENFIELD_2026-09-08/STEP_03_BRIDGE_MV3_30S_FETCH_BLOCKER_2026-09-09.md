# KW-002 Blood & Sand — STEP 03 BRIDGE MV3 30-SECOND FETCH BLOCKER

Date: 2026-09-09

Status: **BLOCKER CONFIRMED / STEP 03 PROVIDER PROGRESSION STOPPED / BRIDGE TRANSPORT REPAIR REQUIRED**

## 1. Incident summary

Step 03 started a durable Wordstat batch with 79 authorised primary probes.

Observed executions:

```text
item 1 Q001 = (амулет|оберег|талисман) RSOTM
HTTP 200
batch item = SUCCEEDED
request_id = wordstat-batch-9292c032-e48e-443e-8576-a51ad4b2c8cc
elapsed_ms = 1884
provider result JSON = {}
cost = 0.02 RUB

item 2 S001 = амулет
request_id = wordstat-batch-93be1f25-c5ff-4b43-a992-b286101d5c2a
request_started_at = 2026-09-09T02:02:05.072Z
completed_at = 2026-09-09T02:02:35.728Z
elapsed wall time = 30.656 s
batch item = OUTCOME_UNKNOWN
reason = REQUEST_OUTCOME_UNKNOWN_NO_RETRY
result_ref = null
cost ledger = +0.02 RUB
```

Batch after item 2:

```text
total = 79
pending = 77
succeeded = 1
outcome_unknown = 1
terminal = 2
requests_started = 2
estimated_cost_rub = 0.04
stop_reason = OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION
next_safe_action = RECONCILE_UNKNOWN
```

No third provider request is allowed.

## 2. Exact raw authorities

```text
STEP_03_WORDSTAT_RAW/001__Q001__wordstat-batch-9292c032-e48e-443e-8576-a51ad4b2c8cc.txt
STEP_03_WORDSTAT_RAW/002__S001__OUTCOME_UNKNOWN__wordstat-batch-93be1f25-c5ff-4b43-a992-b286101d5c2a.txt
STEP_03_WORDSTAT_ACQUISITION_RECEIPTS.csv
```

Both raw files were persisted and read back remotely.

## 3. Fresh external evidence

### Chrome extension service worker lifecycle

Official Chrome documentation:

https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle

Checked: 2026-09-09.

Chrome states that an extension service worker is normally terminated when:

```text
- inactive for 30 seconds;
- a single request/event/API call takes longer than 5 minutes;
- a fetch() response takes more than 30 seconds to arrive.
```

The observed S001 lifetime is 30.656 seconds, directly matching the platform fetch-response boundary.

### Yandex Wordstat / Search API

Current GetTop REST authority:

https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop

Current Wordstat concept:

https://aistudio.yandex.ru/en/docs/search-api/concepts/wordstat

Current GetTop operation guide:

https://aistudio.yandex.ru/en/docs/search-api/operations/wordstat-gettop

Yandex documents synchronous GetTop, response fields and result depth, but no 30-second GetTop timeout was found in the current documentation reviewed for this incident.

Therefore the 30-second boundary is attributed to the Chrome MV3 execution context, not to a documented Yandex GetTop contract.

## 4. Exact Bridge source evidence

The observed runtime identifies:

```text
bridge = yandex-marketing-bridge
version = 0.1.4
```

A repository v0.1.4 authority exists:

```text
branch = bridge/webmaster-readiness-gzip-v0.1.4
commit = 8bb1365a9905df8a6d7e09917e81444a9b7f1024
```

`extension/src/shared/product.js` at that commit reports `VERSION: "0.1.4"`.

The exact installed artifact SHA was not supplied by the runtime result, so byte-identity between the installed package and this repository commit is not claimed. This repository authority is used to identify the current v0.1.4 implementation family and transport design, not to fabricate installed-artifact identity.

The v0.1.4 service-worker implementation executes Wordstat as:

```text
await fetch(req.url, ...)
```

directly inside the Manifest V3 extension service worker.

There is no explicit application timeout / AbortController around this provider fetch in the inspected source.

Any exception at that fetch boundary is intentionally mapped to:

```text
REQUEST_OUTCOME_UNKNOWN_NO_RETRY
```

This fail-closed mapping is correct and must be preserved. The defect is that a potentially slow synchronous provider request is hosted in a Chrome execution context with a hard 30-second fetch-response lifetime.

## 5. Root-cause verdict

```text
ROOT_CAUSE_CONFIDENCE = HIGH

S001_OUTCOME_UNKNOWN
≈ Chrome MV3 service-worker fetch response >30s termination
+
Bridge direct service-worker Wordstat fetch architecture
```

Evidence alignment:

```text
Chrome documented boundary = >30s fetch response
Observed S001 duration = 30.656s
Bridge source = direct await fetch() in MV3 service worker
Bridge catch = maps fetch exception to OUTCOME_UNKNOWN
Yandex docs = no matching documented 30s GetTop timeout found
```

Do not claim a lower-level network cause beyond this evidence. The provider may eventually have completed server-side; that is exactly why automatic retry remains forbidden.

## 6. Q001 empty `{}` clarification

Q001 is a separate issue from the S001 timeout.

Current Yandex REST docs show a successful GetTop response model with:

```text
totalCount
results[]
associations[]
```

Q001 returned HTTP 200 with JSON `{}`.

Official ProtoJSON specification states that fields without presence that hold default values are omitted by default; that includes zero scalar values and empty repeated fields:

https://protobuf.dev/programming-guides/json/

Therefore `{}` is technically compatible with a response equivalent to:

```text
totalCount = 0
results = []
associations = []
```

However Yandex documentation reviewed does not explicitly state that its REST GetTop zero-result response is serialized this way. Therefore project state remains:

```text
Q001_HTTP_200 = true
Q001_OPERATOR_ACCEPTED_END_TO_END = true
Q001_EMPTY_RESPONSE_COMPATIBLE_WITH_ZERO_MATCHES = true
Q001_ZERO_RESULT_DIRECTLY_DOCUMENTED_BY_YANDEX = false
```

The Q001 raw payload remains unchanged; no synthetic fields are written into raw evidence.

## 7. Why reducing numPhrases is not accepted as the default fix

A temporary reduction from 2000 to 100/500 may make broad requests return in under 30 seconds, but it changes evidence depth and does not remove the architectural failure mode.

```text
LOWER numPhrases
!=
FIX LONG_PROVIDER_REQUEST_TRANSPORT
```

Step 03 quality rule is to preserve the best supported evidence, not weaken collection merely to fit an implementation bug.

A reduced-depth fallback may only be used later as an explicit owner-authorised degradation with a documented evidence limitation, not as the default repair.

## 8. Required Bridge repair properties

The durable fix must ensure:

```text
1. provider request that may take >30s is not dependent on a service-worker fetch response arriving within 30s;
2. credentials remain inside trusted extension-owned contexts;
3. request-start identity is durably persisted before provider boundary;
4. completion/result is durably recoverable after service-worker restart;
5. no automatic replay after unknown provider outcome;
6. existing batch fingerprints/request IDs/cost accounting remain correct;
7. complete Wordstat response body remains available;
8. existing Search/Webmaster/Metrika/Direct behavior is not regressed;
9. exact source/package identity is frozen and tested;
10. live acceptance includes a deliberately >30s provider-response simulation and a real bounded Wordstat test.
```

Potential implementation direction requiring engineering validation:

- move long provider network execution to a durable extension-owned document/worker context not subject to the service-worker fetch-response 30s limit;
- use extension message transport and durable state to let the service worker recover/receive completion;
- Chrome `offscreen` documents are an available MV3 mechanism for hidden extension documents, but exact permission/reason/security/lifecycle design must be validated rather than assumed.

Official offscreen API:

https://developer.chrome.com/docs/extensions/reference/api/offscreen

Do not use service-worker heartbeat calls alone as the fix: Chrome documents the fetch-response >30s limit separately from the ordinary idle timer.

## 9. Current Step-03 execution decision

```text
STEP_03_PROVIDER_PROGRESSION = BLOCKED
THIRD_BATCH_NEXT_ALLOWED = false
AUTO_RETRY_S001 = forbidden
CURRENT_BATCH_NEXT_SAFE_ACTION = RECONCILE_UNKNOWN
CURRENT_BATCH_REQUESTS_STARTED = 2
CURRENT_BATCH_ESTIMATED_COST_RUB = 0.04
```

Before Step 03 resumes:

```text
Bridge long-fetch repair
→ exact package QA
→ owner installs/loads accepted package
→ reconcile/cancel historical blocked batch without replay
→ start a new Step-03 acquisition revision
→ intentionally re-measure unresolved S001 under the repaired transport with explicit new-observation lineage
→ continue primary acquisition
```

The historical request remains `OUTCOME_UNKNOWN`; repair does not retroactively turn it into success/failure.
