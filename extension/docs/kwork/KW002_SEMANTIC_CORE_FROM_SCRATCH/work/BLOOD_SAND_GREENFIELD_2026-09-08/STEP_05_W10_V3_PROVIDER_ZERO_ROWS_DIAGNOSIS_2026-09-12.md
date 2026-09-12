# KW-002 Blood & Sand — Step05 W10 V3 provider result diagnosis

Date: 2026-09-12
Status: **DIAGNOSIS PASS — VALID SUCCESS_WITH_ZERO_ROWS / NO BRIDGE DATA-LOSS DEFECT / NO REPLAY**

## Scope

Candidate: `W10C001`

Request ID: `wordstat-b3fbe6dd-121b-4e67-81ca-0b03bdc53358`

Exact released request:

```text
getTop
phrase=(амулет|оберег|талисман) Аум
numPhrases=2000
regions=[225]
devices=[DEVICE_ALL]
```

Returned provider/Bridge result:

```json
{
  "totalCount": "3"
}
```

No second provider request was made.

## Initial conservative classification and correction

Immediately after the owner returned the response, the missing JSON keys `results` and `associations` were conservatively classified as `SUCCESS_BUT_EVIDENCE_INCOMPLETE` until the current Bridge code and provider serialization contract could be checked.

That provisional classification is now superseded.

Final classification:

`SUCCESS_WITH_ZERO_ROWS`

Reason: `results` and `associations` are protobuf repeated fields. Empty repeated fields are valid default values and ProtoJSON omits default-valued fields by default. Therefore a valid response with empty `results=[]` and `associations=[]` can serialize as a JSON object containing only the non-default `totalCount`.

## Current official/provider schema evidence

Yandex AI Studio REST reference for `Wordstat.GetTop` defines the success response as:

```text
totalCount: int64 string
results[]: PhraseInfo
associations[]: PhraseInfo
```

Source:
`https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop`

The current Yandex Cloud generated protobuf bindings define `GetTopResponse.Results` and `GetTopResponse.Associations` as repeated fields and expose them with `omitempty` JSON tags.

Source package:
`https://pkg.go.dev/github.com/yandex-cloud/go-genproto/yandex/cloud/searchapi/v2`

Protocol Buffers ProtoJSON specifies that fields without presence whose value is the default — explicitly including an empty repeated field — are omitted from generated JSON output by default.

Source:
`https://protobuf.dev/programming-guides/json/`

## Current Bridge code trace

Current branch code was read after the provider result was persisted.

### 1. Provider HTTP layer

`extension/src/service_worker.js`

`executeWordstatCommand()`:

- executes the HTTP request;
- reads the complete response body with `response.text()`;
- parses it with `parseJsonMaybe(text)`;
- on HTTP success passes `result: parsed` directly into `WordstatProtocol.buildResultEnvelope()`.

There is no Wordstat result normalization/projection that could remove `results` or `associations`.

### 2. Wordstat envelope layer

`extension/src/shared/wordstat_protocol.js`

`buildResultEnvelope()` stores `result` unchanged.

`formatResultEnvelope()` serializes the complete envelope using `JSON.stringify(envelope, null, 2)`.

No row trimming, sampling, compact projection or whitelist of result fields exists here.

### 3. Manual delivery layer

`extension/src/service_worker.js`

Manual execution pushes `result.report_text` directly into the report list and stores that report text in the outbox. `putOutbox()` stores the entry as supplied and contains no truncation/projection logic.

### 4. Content delivery layer

`extension/src/content_script.js` passes `entry.report_text` to `BB2ComposerSend.setComposerText()`.

`extension/src/shared/composer_send.js` assigns the complete string to the composer and contains no payload truncation logic.

## Root-cause verdict

```text
PROVIDER_HTTP_BODY_LOSS = false
BRIDGE_WORDSTAT_NORMALIZER_LOSS = false
BRIDGE_ENVELOPE_FORMATTER_LOSS = false
BRIDGE_OUTBOX_LOSS = false
BRIDGE_CONTENT_DELIVERY_LOSS = false
VALID_PROTOJSON_EMPTY_REPEATED_OMISSION = true
```

There is no evidence of a Bridge 0.1.4 data-loss bug in this execution.

There is also no hidden missing row set to recover from Bridge storage: the provider HTTP JSON parsed by the worker already had the empty repeated fields omitted; later layers preserve that parsed object losslessly.

## Semantic meaning of the result

The facts are:

```text
totalCount = 3
returned results rows = 0
returned association rows = 0
```

Do NOT rewrite this as either:

- `three keywords were found`; or
- `demand is zero`.

Bounded interpretation:

- Yandex reported aggregate `totalCount=3` for this exact GetTop configuration/current snapshot;
- Yandex returned no phrase-level `results` vocabulary and no `associations` vocabulary;
- therefore this probe produced no extractable distinct Cyrillic-Аум physical-product-qualified vocabulary rows for the current research snapshot;
- the zero-row observation may close W10C001 for the current snapshot only;
- it does not prove permanent/universal zero demand and does not authorize a claim that no such demand can ever exist.

## Step03A / Step03B consequence

No new provider rows exist.

Therefore:

```text
STEP03A_ROWS_TO_PROCESS = 0
STEP03B_ROWS_TO_PROCESS = 0
UPSTREAM_MUTATIONS_REQUIRED = 0
```

There is nothing to normalize/sanitize or union from this request.

## Provider/replay consequence

The one-call release was consumed by the successful request.

```text
CURRENT_W10C001_RELEASE = CONSUMED
BLIND_REPLAY = FORBIDDEN
SECOND_PROVIDER_CALL = NOT_AUTHORIZED
```

No replay is necessary for the current snapshot because this is now a valid semantic zero-row outcome, not incomplete evidence.

## Final diagnosis verdict

```text
W10C001_PROVIDER_EXECUTION = EXECUTED
HTTP_STATUS = 200
PROVIDER_STATUS = OK
OUTCOME = SUCCESS_WITH_ZERO_ROWS
TOTAL_COUNT = 3
RESULT_ROWS = 0
ASSOCIATION_ROWS = 0
RAW_REMOTE_READBACK = PASS
BRIDGE_DATA_LOSS_BUG = NO
W10C001_CURRENT_SNAPSHOT_STATE = CLOSED_FOR_CURRENT_RESEARCH_SNAPSHOT
REPLAY_REQUIRED = NO
REPLAY_ALLOWED = NO
STEP06_STARTED = false
```
