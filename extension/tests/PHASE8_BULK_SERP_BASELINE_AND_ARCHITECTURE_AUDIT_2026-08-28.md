# Phase 8 — Bulk SERP / TOP / rank baseline + architecture audit

Date: 2026-08-28
Status: **P8-00 BASELINE FROZEN / P8-01 ARCHITECTURE AUDIT COMPLETE / PRODUCT BYTES UNCHANGED**

## 1. Exact production baseline

Phase-8 development branch was created from exact accepted production `main`:

```text
main_commit = 67aeee71a42bdc0edb516341297987c1d1d26972
root_tree = d4e7d4577a54736fb8c3692bed8c5b5137c158e0
extension_tree = 01a735be7a97f095528eece4008224b97d04bf19
extension/src_tree = 04dc6d015977270fb064b669ee03d04f6e130612
extension/tests_tree = 6baf13fb6210d64b25d68dfb665468942eaf9316
```

At P8-00 freeze, `main` still resolves to the same accepted SHA.

Phase-8 branch:

```text
phase8/bulk-serp-top-rank-2026-08-28
base = 67aeee71a42bdc0edb516341297987c1d1d26972
```

Requirements/docs commits before this audit do not modify `extension/src`.

## 2. Relevant frozen implementation identities

```text
extension/src/manifest.json
= 5a23d95010e8ef34623fbe63715155687594d8f6

extension/src/phase3_service_worker_bootstrap.js
= b6be6ee7adee1a6b9c23f267ddb9b50dcfd3b46f

extension/src/content_script.js
= 1190ebda4771118243e179a33e333b8b30a7ad9a

extension/src/shared/service_registry.js
= c247d4d6c1273de38daf5967a83cc3ac2c260923

extension/src/shared/search_protocol.js
= 49ca9a6f3a2786a3107f03d0724dfca7578cd096

extension/src/shared/search_xml.js
= f738aa676ef92f288004aac776f9cb8e0cc2d042

extension/src/shared/policy_model.js
= dc7873bad83bbf319123d96c03d12c4f4b31d1c6

extension/src/shared/provider_batch_job_model.js
= 9d2912090d4523ff029cbe7d77936bdb3995dc53

extension/src/shared/wordstat_batch_protocol.js
= 2846a0bdfeba6a9241b5aced255ed44b06cffcad

extension/src/shared/wordstat_batch_runtime.js
= 6c30afb253a1756c7c40d162a70c289c0e7c28d7

extension/src/shared/wordstat_batch_transport.js
= 82d6b133e437690ce2c488f17cab1f32ce87abce

extension/src/shared/wordstat_batch_content_bridge.js
= 751724c5d1a1091749bc6742723807fbf4c28008
```

## 3. Search provider contract audit

Current ordinary Search already owns the provider behavior required by Phase 8:

```text
protocol = SEARCH_API_V1
method = search
endpoint = POST /v2/web/search
region support = existing SearchProtocol semantics
page = bounded integer
groupsOnPage = 1..100
docsInGroup = 1..3
```

No provider-level protocol extension is required merely to execute a per-key SERP job.

Current ordinary Search response normalization already yields:

```text
results[]
  rank
  url
  domain
  title
  snippet
  modtime
result_count
response_format = FORMAT_XML
```

Therefore TOP/domain/rank projection can be pure deterministic computation over persisted accepted Search results.

GenSearch is a distinct method in the same `SEARCH_API_V1` protocol and must not be selected implicitly by Search batch.

## 4. Batch lifecycle reuse audit

`YMBProviderBatchJobModel` is intentionally service-generic. It already provides the Phase-8 safety-critical lifecycle:

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

Reusable invariants already implemented:

- canonical command fingerprinting and exact duplicate discipline;
- one active/in-flight item per job;
- request and cost bounds before claim/start;
- persisted `REQUEST_STARTED` identity;
- `request_executed` truth;
- `automatic_retry = false`;
- `OUTCOME_UNKNOWN` blocks later automatic paid progression;
- pause/resume/cancel;
- recovery of stale claims and stale started requests;
- durable progress totals.

**Decision:** Phase 8 reuses this model unchanged unless a failing Search-specific contract test proves a generic gap. Do not fork/copy the lifecycle model.

## 5. Wordstat batch runtime audit

Wordstat batch proves the correct service-specific adapter pattern:

```text
service-specific protocol
+ separate service-specific storage key
+ generic provider-batch model
+ service policy admission
+ persist claim
+ persist REQUEST_STARTED
+ exactly one provider executor call on next
+ persist terminal payload before delivery
+ manual/autorun adapter
```

`wordstat_batch_runtime.js` stores each provider result payload on the durable item before returning the result.

**Decision:** Search batch should copy the pattern, not the Wordstat semantics. It gets its own protocol/runtime/storage key and executes only normalized ordinary Search commands.

## 6. Storage decision

Wordstat runtime currently owns:

```text
ymb_wordstat_batch_jobs_v1
```

Phase 8 must not mix service jobs into this map.

Frozen Search-batch storage contract:

```text
ymb_search_batch_jobs_v1
```

The generic model may be shared; the persisted maps remain service-separated.

## 7. Registry and routing decision

The service registry contains exactly five definitions:

```text
wordstat -> WORDSTAT_API_V1
search -> SEARCH_API_V1
webmaster -> WEBMASTER_API_V1
metrika -> METRIKA_API_V1
direct -> DIRECT_API_V1
```

Phase 8 must keep these definitions unchanged.

`SEARCH_BATCH_API_V1` is an orchestration protocol belonging semantically to `search`, analogous to `WORDSTAT_BATCH_API_V1` belonging to `wordstat`.

The batch marker therefore requires explicit transport/discovery handling outside the five-entry ordinary registry, not a new service definition.

## 8. Content-script integration audit

`manifest.json` currently loads Wordstat batch protocol/transport/content bridge before ordinary Search modules and `content_script.js`.

`content_script.js` chooses the protocol by active service:

```text
search -> SearchProtocol
wordstat -> WordstatProtocol
metrika -> MetrikaProtocol
direct -> DirectProtocol
```

Wordstat batch currently extends command recognition through a narrowly scoped content bridge/proxy rather than adding a registry entry.

**Decision:** Phase 8 should use the same bounded pattern for Search:

```text
search_batch_protocol.js
search_batch_transport.js
search_batch_content_bridge.js
```

loaded before `content_script.js`, preserving active-service isolation.

## 9. Worker integration audit

`phase3_service_worker_bootstrap.js` currently imports the generic batch model and Wordstat batch modules before the accepted worker bootstrap, then installs `wordstat_batch_worker_transport.js` before later provider runtimes.

Wordstat worker transport wraps the accepted Manual/Autorun handlers and delegates non-batch traffic back to the previous handlers.

**Decision:** Search batch worker integration must preserve the wrapper chain:

```text
accepted ordinary worker
→ Wordstat batch wrapper
→ Search batch wrapper
→ later provider runtime wrappers
```

Exact placement must be covered by a load-order regression test before product integration.

## 10. Policy/economics audit

Current Search policy owns:

```text
search = 0.488 RUB/request
genSearch = 5.08 RUB/request
```

Phase-8 paid items must call policy admission with:

```text
service = search
method = search
```

Never `genSearch`.

At current bridge estimate:

```text
100 ordinary Search items ≈ 48.8 RUB
500 ordinary Search items ≈ 244 RUB
```

Therefore every start manifest must carry explicit job-level `maxRequests` and `maxCostRub`, and the runtime must also respect any stricter global Search policy.

## 11. Projection placement decision

Rank/domain extraction and pairwise TOP overlap are deterministic transformations of persisted SERP evidence and do not require provider calls.

Frozen implementation boundary:

```text
SearchBatchProjection = pure/local
projection = 0 provider requests
overlapPage = 0 provider requests
```

The projection module may compute:

- ranked rows;
- unique domain sets by first/best observed rank;
- sampled target-domain rank inside observed topN;
- pairwise shared-domain counts;
- Jaccard and containment values;
- bounded/paged output.

It must not assign semantic cluster labels or make page split/merge decisions.

## 12. Minimal file plan

Expected new product modules after test-first contract:

```text
extension/src/shared/search_batch_protocol.js
extension/src/shared/search_batch_runtime.js
extension/src/shared/search_batch_projection.js
extension/src/shared/search_batch_transport.js
extension/src/shared/search_batch_content_bridge.js
extension/src/search_batch_worker_transport.js
```

Expected touched integration files:

```text
extension/src/manifest.json
extension/src/phase3_service_worker_bootstrap.js
```

Other production files should remain unchanged unless a focused failing test proves a required integration point.

Expected first focused tests:

```text
extension/tests/search_batch_protocol.test.mjs
extension/tests/search_batch_runtime.test.mjs
extension/tests/search_batch_projection.test.mjs
```

## 13. P8-01 verdict

```text
SEARCH_PROVIDER_CHANGE_REQUIRED = false
GENERIC_BATCH_MODEL_REUSABLE = true
SEPARATE_SEARCH_BATCH_STORAGE_REQUIRED = true
NEW_SERVICE_REQUIRED = false
ORDINARY_SEARCH_ONLY_FIRST_SLICE = true
LOCAL_PROJECTION_PROVIDER_REQUESTS = 0
LOCAL_OVERLAP_PROVIDER_REQUESTS = 0
TEST_FIRST_RUNTIME_AUTHORIZED = true
```

Next step: P8-02 freeze protocol/storage/projection behavior in focused tests before changing `extension/src`.
