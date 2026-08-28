# AI-native GenSearch production contract

Date: 2026-08-28
Status: **FROZEN FOR PRODUCTION DELIVERY GATE**

Applies to: O-001 AI-Native Semantic Rebuild.

## Authority

This contract is frozen only after the bounded five-root proxy validation passed:

`extension/tests/AI_NATIVE_GENSEARCH_PROXY_VALIDATION_FINAL_2026-08-28.md`

Verdict:

```text
AI_NATIVE_GENSEARCH_PROXY_VALIDATION_PASS
representative_roots = 5
valid_observations = 5
MATERIALLY_DIFFERENT = 0
systematic_contradictions = 0
```

Exact product source authority already exercised in owner-live GenSearch validation:

```text
source_commit = 0fdcd0704c0d86f6bc6b915a340494ae456cd3e8
extension_src_tree = 354230e8d68bf4759d98cdba55ec6ba0e0796c63
product_version = 0.1.1
```

No production-byte change is authorized merely to freeze this document. The live-tested R3 product bytes remain the candidate authority.

## Service / protocol boundary

GenSearch remains a bounded method of the existing Search service.

```text
service = search
command_prefix = SEARCH_API_V1
result_prefix = SEARCH_RESULT_V1
method = genSearch
provider_endpoint = POST https://searchapi.api.cloud.yandex.net/v2/gen/search
```

The service registry remains exactly:

```text
wordstat
search
webmaster
metrika
direct
```

No sixth GenSearch service is permitted.

## Command contract

One paid GenSearch request is admitted only by an explicit command of the form:

```text
SEARCH_API_V1 {"method":"genSearch","queryText":"...","confirmBillable":true}
```

Allowed GenSearch command fields are exactly:

```text
method
queryText
confirmBillable
```

`confirmBillable` must be literal boolean `true`. Ordinary Search-only fields such as `searchType` and `region` are rejected for `genSearch` rather than being mapped to invented provider semantics.

Current bridge safety bounds remain:

```text
queryText <= 400 Unicode characters
queryText <= 40 whitespace-delimited words
```

## Provider request contract

For `genSearch`, the bridge builds one synchronous provider request:

```json
{
  "messages": [
    {"content": "<queryText>", "role": "ROLE_USER"}
  ],
  "folderId": "<configured Search folder id>",
  "fixMisspell": true,
  "getPartialResults": false
}
```

Credentials are injected by the existing Search credential runtime and are not placed in the JSON body or returned in result evidence.

There is no hidden provider loop and no automatic paid retry.

## Response / transport contract

The normalized result remains explicitly generative:

```text
result.mode = generative
```

Preserved provider evidence includes:

```text
message.content
message.role
sources[].url
sources[].title
sources[].used
searchQueries[].text
searchQueries[].reqId
fixedMisspellQuery
isAnswerRejected
isBulletAnswer
hints[]
problematicAnswer
transport.wire_format
transport.frame_count
```

The response decoder accepts the provider shapes already governed by the official-contract tests and live R3 evidence:

```text
single JSON GenSearchResponse object
JSON array/server-stream framing -> final snapshot
JSON Lines framing -> final snapshot
```

An official response may omit optional semantic fields. An empty object is therefore not rejected merely because no optional field is present.

Ordinary Search remains on its existing `/v2/web/search` + XML-normalizer path and does not inherit GenSearch stream-framing behavior.

## Provenance contract

GenSearch is a distinct structured AI-search evidence surface. Consumers must interpret the result using the following provenance labels:

```text
GEN_SEARCH_INPUT
GEN_SEARCH_ANSWER
GEN_SEARCH_SOURCE
GEN_SEARCH_SOURCE_USED
GEN_SEARCH_QUERY_OBSERVED
```

The normalized wire result itself remains backward-compatible and is distinguished mechanically by:

```text
service = search
operation = genSearch
result.mode = generative
```

The following mappings are forbidden:

```text
GEN_SEARCH_QUERY_OBSERVED -> ALICE_FANOUT_OBSERVED
GEN_SEARCH_ANSWER -> CONSUMER_ALICE_ANSWER
GEN_SEARCH_SOURCE -> CONSUMER_ALICE_SOURCE
```

`searchQueries[]` proved materially narrower than consumer-Alice fan-out in the bounded validation and must remain separate provenance.

## Cost / admission contract

Recorded synchronous GenSearch estimate used by the bridge:

```text
5.08 RUB / request
```

The Search policy model owns this cost. A legacy stored Search policy may be migrated once to recognize the new method, while a later explicit method disable remains fail-closed.

A command may be skipped before the provider boundary for policy/admission reasons. Such a skip must retain:

```text
request_executed = false
automatic_retry = false
```

A request that crosses the provider boundary must report execution truth and is never automatically repeated after an unknown/error outcome.

## Acceptance evidence already observed

Five valid live observations were collected on the exact R3 product bytes:

```text
G01 печать велеса        = SAME_OR_STRONGLY_ALIGNED
G02 оберег в машину      = PARTIALLY_ALIGNED
G03 вегвизир             = SAME_OR_STRONGLY_ALIGNED
G04 алатырь оберег       = SAME_OR_STRONGLY_ALIGNED
G05 подарок мужчине...   = SAME_OR_STRONGLY_ALIGNED
```

All five successful observations returned HTTP 200, `request_executed=true`, `automatic_retry=false`, and real provider framing `json_array` with one frame.

There was one earlier paid-boundary G01 request that failed only in the superseded pre-R3 parser. It is counted in economics but is not semantic evidence.

## Production claim boundary

Permitted claim:

> Official Yandex GenSearch is a repeatable structured AI-search evidence hand that preserved enough decision-relevant signal in the bounded O-001 validation to be used selectively in the workflow.

Forbidden claims include:

- exact equivalence to consumer Alice;
- guaranteed Alice citation/indexing;
- deterministic source inclusion;
- consumer-visible source/ranking equivalence;
- `searchQueries[]` equivalence to Alice fan-out;
- guaranteed traffic, ranking or revenue uplift.

## Freeze statement

```text
GENSEARCH_PRODUCTION_CONTRACT_FROZEN = true
PROXY_VALIDATION = PASS
PRODUCT_SOURCE_COMMIT = 0fdcd0704c0d86f6bc6b915a340494ae456cd3e8
PRODUCT_SRC_TREE = 354230e8d68bf4759d98cdba55ec6ba0e0796c63
PRODUCT_BYTES_CHANGED_BY_CONTRACT_FREEZE = false
REAL_PROVIDER_REQUESTS_REQUIRED_FOR_NEXT_GATE = 0
```

Next gate: complete controlled pre-delivery regression against these exact product bytes, then main promotion only if the gate is fully green and exact product identity is preserved.
