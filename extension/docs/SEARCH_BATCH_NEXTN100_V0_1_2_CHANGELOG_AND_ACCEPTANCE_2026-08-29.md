# Yandex Marketing Bridge 0.1.2 — Search Batch `nextN` bounded chunk execution

Date: 2026-08-29  
Status: **IMPLEMENTED / TESTED / SOURCE SYNCHRONIZED**

## Why this change exists

The original Search Batch runtime exposed only one paid item at a time through `action:"next"`. For a bounded owner-authorized Search acquisition this forced one Manual delivery round-trip per provider request and made larger evidence acquisitions operationally inefficient.

The change adds a bounded Manual-only chunk action without creating a second provider path:

```text
SEARCH_BATCH_API_V1
{"action":"nextN","jobId":"...","count":N}
```

Contract:

```text
1 <= count <= 100
Manual only
one Manual block = exactly one SEARCH_BATCH_API_V1 command
no automatic retry
UNKNOWN => stop immediately
terminal error => stop immediately
budget/pause/completion/no-pending => stop before another provider boundary
```

The value `100` is a hard protocol ceiling, not a recommendation that every live chunk should contain 100 provider requests.

## Production code changed

### `shared/search_batch_protocol.js`

Added:

- `nextN` to the Search Batch action set;
- strict `count` validation, integer `1..100`;
- separate allowed-field set for `nextN`;
- additive `chunk` field in `SEARCH_BATCH_RESULT_V1` envelopes.

Why: the operation needs an explicit bounded contract and a result envelope capable of returning multiple sequential item results.

### `shared/search_batch_runtime.js`

Added `nextN()` implemented by sequentially calling the already-existing `next()` path.

It does **not** bypass or duplicate the existing provider boundary. Every item still passes through the existing sequence:

```text
admission/cost check
-> claimNext
-> persist CLAIMED/REQUEST_STARTED state
-> exactly one existing executeSearch provider boundary
-> terminal/unknown/success state update
-> persist result_payload
-> only then consider the next item
```

The chunk stops immediately on `UNKNOWN`, terminal error, budget limit, paused/completed state or another non-executed step.

Chunk response includes:

```text
requested_count
attempted_steps
confirmed_provider_executions
provider_execution_count_exact
stopped_early
stop_reason
items[]
```

The delivery copy removes duplicated `item.result_payload`; the full returned provider result remains in each chunk entry as `provider_result` while the durable job state keeps the original full `result_payload`.

### `search_batch_worker_transport.js`

Added chunk-aware provider-execution accounting and delivery:

- returns the last available request id for a chunk;
- carries `confirmed_provider_executions`;
- preserves `provider_executions=null` for aggregate `UNKNOWN`;
- applies the report prefix when at least one provider request definitely executed;
- explicitly rejects `nextN` in Autorun with `SEARCH_BATCH_NEXT_N_MANUAL_ONLY`.

The existing `BATCH_SINGLE_COMMAND_REQUIRED` Manual guard remains unchanged.

## Deliberately unchanged dependencies

The patch does not create or modify another Yandex service and does not add a direct fetch path.

Unchanged behavior/contracts include:

- `shared/search_protocol.js` provider command semantics;
- Search endpoint/authentication;
- `shared/provider_batch_job_model.js` claim, cost, terminal and UNKNOWN rules;
- `shared/search_batch_transport.js` service routing;
- service registry: still exactly five services;
- Search Batch Manual single-command rule;
- Wordstat Batch;
- Webmaster;
- Metrika;
- Direct;
- GenSearch;
- generic Manual multi-command contract.

## Compatibility

The persisted Search Batch job schema was not changed. A job created by the prior `0.1.1` runtime can be loaded by the patched runtime and continued without replaying an already succeeded item.

This matters for jobs interrupted between Bridge builds.

## Test evidence

Focused test suite after the change:

```text
16 tests
16 PASS
0 FAIL
```

Covered:

1. `nextN` accepts counts 1 and 100.
2. Rejects 0, 101, fractional, missing count and extra fields.
3. Existing `next` and `status` remain valid.
4. Fingerprint changes when `count` changes.
5. Sequential execution preserves provider order.
6. Every previous item result is durably persisted before the next provider boundary.
7. Cost accounting remains exact.
8. `maxRequests` stops before overrun.
9. `maxCostRub` stops before overrun.
10. Terminal provider error stops the chunk immediately.
11. `UNKNOWN` stops immediately and is never blindly retried.
12. Recovery does not replay an unknown request.
13. `count=100` is bounded by actual remaining work; synthetic test with three remaining items performs exactly three provider calls, not 100.
14. Legacy `next` remains exactly one provider boundary.
15. Service/discovery/content-bridge/bootstrap dependencies remain stable.
16. A persisted old-runtime job resumes on the new runtime without replay.

Whole candidate syntax gate:

```text
47 JavaScript files
47 node --check PASS
```

Chromium native pack-extension smoke:

```text
PASS
```

## Live evidence from KW-001 Step 09

The patched Bridge was then used in the live Step-09 Search acquisition.

Observed R2 job:

```text
job_id = kw001-okno-msk-search-step09-20260829-r2
real ordinary Search provider requests = 74
succeeded = 74
failed_terminal = 0
outcome_unknown = 0
estimated cost = 36.112 RUB
final job status = COMPLETED
```

Together with the earlier one-request canary:

```text
75 real Search probes
75 successes
0 terminal failures
0 unknown outcomes
36.600 RUB estimated cumulative cost
```

Important evidence boundary:

```text
LOCAL count=100 BOUNDED TEST != 100 LIVE PROVIDER REQUESTS IN ONE CHUNK
R2 74/74 LIVE SUCCESS != PROOF OF THE EXACT SIZE OF EACH INDIVIDUAL nextN COMMAND
```

The final R2 projection proves the completed 74-item job and normalized TOP-10 outputs, but it does not encode the history of individual chunk command sizes. Documentation must not invent those chunk sizes.

## Version authority

This functional change advances the Bridge patch version:

```text
Yandex Marketing Bridge = 0.1.2
```

Authoritative source fields:

```text
extension/src/manifest.json -> version 0.1.2
extension/src/shared/product.js -> VERSION 0.1.2
extension/src/package.json -> version 0.1.2
```

`0.1.1` is the predecessor baseline from which this patch was developed and live-tested before repository synchronization.

## Operational persistence lesson exposed by the live run

The Bridge correctly persists Search Batch job state in `chrome.storage.local`, but project evidence must not rely on browser storage or the chat session as the only durable copy.

Canonical rule for any paid or otherwise non-trivial acquisition:

```text
PROVIDER_RESULT_RECEIVED
-> IMMEDIATE_PROJECT_DURABLE_WRITE
-> READ-BACK / ACCOUNTING QA
-> ONLY THEN NEXT PAID CHUNK
```

Why: browser storage, extension identity, tab/session state, conversation delivery, or the connection itself can disappear independently. A successful provider call that is not immediately copied into the project evidence ledger can become paid evidence that must be reconstructed or reacquired.

This project-level persistence discipline is separate from the Bridge's internal job persistence and must be enforced by the workflow using the Bridge.
