# Yandex Marketing Bridge — Wordstat MV3 long-fetch repair handoff

Date: 2026-09-09

Status: **BLOCKING PRODUCTION DEFECT / FOCUSED ENGINEERING REPAIR REQUIRED**

## 0. Why this repair exists

A real KW-002 Wordstat acquisition on Bridge runtime `0.1.4` exposed a production transport defect.

A broad `getTop` request with `numPhrases=2000` for `амулет` entered the provider boundary at:

```text
2026-09-09T02:02:05.072Z
```

and was converted to `OUTCOME_UNKNOWN` at:

```text
2026-09-09T02:02:35.728Z
```

Observed duration:

```text
30.656 s
```

The batch correctly refused automatic replay.

Project evidence:

`extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_03_BRIDGE_MV3_30S_FETCH_BLOCKER_2026-09-09.md`

## 1. External platform authority

Official Chrome extension service worker lifecycle:

https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle

Chrome explicitly documents service-worker termination when a `fetch()` response takes more than 30 seconds to arrive.

Official Offscreen API reference:

https://developer.chrome.com/docs/extensions/reference/api/offscreen

Offscreen documents are extension-owned hidden documents in MV3. Extension permissions carry over, while communication is through `chrome.runtime`. This is a candidate primitive, not a preselected final architecture.

Official cross-origin extension request guidance:

https://developer.chrome.com/docs/extensions/develop/concepts/network-requests

Official Yandex GetTop:

https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop

Yandex documents synchronous GetTop and result depth up to 2000. No current official Yandex GetTop 30-second client timeout was found during the incident investigation.

## 2. Exact source family

Observed runtime:

```text
Yandex Marketing Bridge = 0.1.4
```

Repository v0.1.4 branch:

```text
bridge/webmaster-readiness-gzip-v0.1.4
```

Known exact commit containing `VERSION: "0.1.4"`:

```text
8bb1365a9905df8a6d7e09917e81444a9b7f1024
```

Important provenance boundary:

The live result did not expose installed artifact SHA. Do not claim byte identity between the user's installed package and this commit unless a package/source fingerprint is obtained. The repository commit is the current reproducible v0.1.4 engineering authority to repair/test.

## 3. Current faulty transport pattern

In the v0.1.4 source family, Wordstat provider execution is performed directly from the MV3 service worker:

```js
await fetch(req.url, ...)
```

The catch boundary intentionally maps a thrown fetch to:

```text
REQUEST_OUTCOME_UNKNOWN_NO_RETRY
```

That no-retry behavior is correct and must remain.

The defect is hosting potentially >30s synchronous provider requests on the service-worker fetch-response path.

## 4. Repair goal

Create a production-safe provider network transport for potentially long Wordstat calls that does not depend on the service worker receiving the HTTP response within Chrome's 30-second fetch-response limit.

This is a transport repair only.

Do not change SEO methodology, seed strategy, Wordstat provider semantics or batch accounting merely to mask the defect.

## 5. Mandatory preservation invariants

Preserve all accepted Bridge behavior:

```text
WORDSTAT_API_V1
WORDSTAT_BATCH_API_V1
WORDSTAT_RESULT_V1
WORDSTAT_BATCH_RESULT_V1

one batch.next = at most one provider initiation
no hidden retry
OUTCOME_UNKNOWN => no automatic replay
stable batch item fingerprint
request_id persisted before/at provider boundary
cost/request accounting
pause/resume/cancel/status semantics
Manual/Autorun ownership fences
active_service isolation
credential isolation
complete provider payload delivery
Search/Webmaster/Metrika/Direct regressions
```

No credential may be exposed to page DOM, ChatGPT content or untrusted web context.

## 6. Forbidden shortcut fixes

Do not solve by:

```text
- globally reducing numPhrases from 2000 to 100/500;
- blindly retrying after 30s;
- increasing an application timeout inside the same service-worker fetch;
- calling chrome APIs as a heartbeat while leaving provider fetch in the service worker and claiming that fixes the distinct fetch-response 30s limit;
- silently converting OUTCOME_UNKNOWN to FAILED or SUCCEEDED;
- removing durable batch protections;
- running provider requests from a page content script subject to web-origin/CORS/security boundaries;
- leaking API key/folder credentials into ChatGPT/page-visible data.
```

## 7. Required design investigation before implementation

Evaluate at least these architectures against Chrome documentation and project security/lifecycle rules:

### Option A — extension-owned offscreen document / dedicated worker transport

Potential model:

```text
service worker
→ durably marks REQUEST_STARTED
→ ensures extension-owned offscreen transport exists
→ sends trusted provider request spec to transport
→ long network call executes outside service-worker fetch-response 30s boundary
→ transport returns/wakes service worker with result
→ result is committed to durable batch state
→ normal delivery proceeds
```

Must prove:

```text
correct permitted offscreen reason/justification
credential handling remains trusted
cross-origin host permission works
service-worker restart during request does not lose completion
result cannot be delivered twice
request cannot be replayed after restart
only exact intended provider call occurs
```

A dedicated Web Worker spawned from the offscreen document may be considered if it provides a cleaner long-running network context. Do not assume this is required before tests.

### Option B — another extension-owned persistent document context

Evaluate only if it is less intrusive and more policy-correct than offscreen.

Do not create visible hidden-tab hacks as the default production architecture without explicit owner approval.

## 8. Durability requirement is stronger than simply avoiding 30s

The correct design must survive:

```text
service-worker termination while provider request is still pending
service-worker restart before result arrives
popup close
tab refresh
ChatGPT delivery delay
manual/autorun mode transitions allowed by existing rules
```

If the service worker dies after request initiation, provider completion must not be lost or replayed blindly.

A design that merely keeps one Promise alive in RAM is not sufficient.

## 9. Required test-first cases

Before production implementation, add failing tests/harness coverage for:

```text
T1: simulated provider response at 1s -> one request -> success
T2: simulated provider response at 35s -> one request -> success, NOT OUTCOME_UNKNOWN solely because of Chrome SW fetch timeout
T3: service-worker restart during >30s in-flight request -> no duplicate provider initiation
T4: completion after restart -> durable result reconciled once
T5: transport/result message duplicate -> exactly-once settlement
T6: transport context disappears before outcome known -> OUTCOME_UNKNOWN, no auto retry
T7: HTTP 4xx/5xx -> known provider error, not unknown
T8: network failure after initiation -> OUTCOME_UNKNOWN
T9: complete Wordstat response body preserved
T10: empty successful JSON object remains raw `{}` and is not silently rewritten
T11: request/cost totals reconcile
T12: batch pause/resume/cancel/status remain zero-provider actions
T13: prior Wordstat single-request regression
T14: Search/Webmaster/Metrika/Direct prior-service regression
T15: secret/redaction audit
```

## 10. Browser acceptance requirement

A Node-only fake is not enough because the defect is a Chrome MV3 lifecycle boundary.

Exact-package browser QA must include a controlled long-response endpoint/harness that exceeds 30 seconds and proves the final transport survives without duplicate provider execution.

The exact built package tested in browser must be the package handed to the owner.

## 11. Live provider acceptance after synthetic browser gate

Only after the long-response browser gate passes:

```text
load exact accepted package
active_service = wordstat
run one bounded real Wordstat GetTop request
verify request_id / result / no replay / cost
then run a broad request expected to exercise the long-response path
```

Do not use the unresolved historical `амулет` request as an automatic retry. A new real request is a deliberate new observation with new request identity.

## 12. Versioning

Do not overwrite `0.1.4` while shipping different product bytes.

The repair should receive a new product version (expected next patch version such as `0.1.5`, unless the repository's current version authority has moved by implementation time).

Version must reconcile across:

```text
manifest.json
package.json
shared/product.js
runtime envelopes
artifact name/manifest
QA evidence
```

## 13. Required final handoff evidence

Provide:

```text
base commit
repair branch
final source commit
exact extension/src tree SHA
exact artifact SHA256
all changed files
focused tests
full source regression
full packaged regression
long-response browser test evidence
prior-service regression
secret scan
real provider acceptance request IDs
no-auto-retry proof
owner install instructions
```

## 14. Stop condition

Do not return to KW-002 Step 03 provider acquisition until:

```text
LONG_WORDSTAT_FETCH_TRANSPORT = PASS
>30S_BROWSER_TEST = PASS
NO_DUPLICATE_INITIATION = PASS
DURABLE_COMPLETION = PASS
PRIOR_SERVICE_REGRESSION = PASS
EXACT_PACKAGE_IDENTITY = PASS
OWNER_LOADED_ACCEPTED_PACKAGE = true
```

Then KW-002 creates a new Step-03 acquisition revision and resumes from preserved upstream seed authority.
