# AI-native provider research — Yandex GenSearch / Alice-related evidence

Date: 2026-08-27

Status: **OFFICIAL PROVIDER PATH FOUND / RESEARCH COMPLETE ENOUGH FOR ROADMAP / IMPLEMENTATION GATED**

Applies to: O-001 AI-Native Semantic Rebuild.

## 1. Key finding

A repeatable AI-search evidence hand does not need to begin by scraping the consumer Alice UI.

Yandex exposes an official generative-search method inside Yandex Search API:

```text
POST https://searchapi.api.cloud.yandex.net/v2/gen/search
```

Official REST reference:

`https://aistudio.yandex.ru/docs/en/search-api/api-ref/GenSearch/search.html`

Official operation guide:

`https://aistudio.yandex.ru/docs/en/search-api/operations/generative-search.html`

The official API describes GenSearch as search over Yandex's search database using YandexGPT generative AI.

## 2. Valuable response fields

The current official response contract includes:

```text
message.content
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
```

Particularly important for O-001:

```text
sources[].used
= whether a returned source document was used in the generated answer

searchQueries[]
= search queries refined by the YandexGPT model and used for the generative response
```

This provides machine-readable evidence that is far more stable for our Bridge than DOM parsing of a consumer chat interface.

## 3. Authentication / execution boundary

The official guide currently requires a Yandex Cloud folder plus a service account with the Search API role and an API key with the execution scope; IAM-token authentication is also documented as an option.

This belongs architecturally to the existing Yandex Search provider family, not to the dedicated OAuth credentials for Webmaster, Metrika or Direct.

Permanent credential rule remains:

```text
Search / Yandex Cloud credential = its own credential
Webmaster OAuth = separate
Metrika OAuth = separate
Direct OAuth = separate
```

Do not consolidate credentials as part of GenSearch work.

## 4. Proposed Bridge shape

Do not create a standalone pseudo-provider called `alice` unless later evidence requires it.

Preferred provider architecture:

```text
Yandex Search hand
├── ordinary WebSearch
│   └── /v2/web/search
└── generative GenSearch
    └── /v2/gen/search
```

A future trusted protocol may normalize the generative result to a dedicated result envelope while reusing Search credential/policy infrastructure.

Conceptual normalized evidence:

```text
input query
answer text
sources[]
  url
  title
  used
search_queries[]
  text
  req_id
hints[]
misspell correction
answer status flags
request/cost metadata
```

Exact protocol names are intentionally not frozen before implementation design.

## 5. Provenance rule

Do **not** relabel GenSearch fields as consumer-Alice facts without validation.

Use explicit provenance such as:

```text
GEN_SEARCH_INPUT
GEN_SEARCH_ANSWER
GEN_SEARCH_SOURCE
GEN_SEARCH_SOURCE_USED
GEN_SEARCH_QUERY_OBSERVED
```

Do not automatically write:

```text
ALICE_FANOUT_OBSERVED
```

for `searchQueries[]` until the one-time comparison establishes the relationship between GenSearch behavior and the consumer Alice evidence used in `blood_sand`.

This distinction is central to evidence quality.

## 6. Required validation against blood_sand

The existing `blood_sand` dataset contains canonical consumer-Alice observations for the same research program.

Before GenSearch is accepted as the production proxy/measurement hand for O-001, compare it on a bounded representative set against those existing observations.

Compare at least:

```text
root query
answer/user-job orientation
source domains
used/cited source overlap where comparable
additional/refined query themes
commercial vs explanatory orientation
material semantic/page-job implication
```

The comparison must distinguish:

```text
same / strongly aligned
partially aligned
materially different
not comparable
```

Do not require byte/text equivalence. The decision question is whether GenSearch is a useful repeatable evidence surface for the same semantic research job.

This provider-proxy validation is related to, but distinct from, the broader Pass A vs Pass B methodology gate.

## 7. Economics

Official Yandex Search API pricing snapshot on 2026-08-27:

```text
synchronous requests with generative response = 5,080 RUB / 1,000 requests incl. VAT
≈ 5.08 RUB per request
```

Official pricing:

`https://aistudio.yandex.ru/docs/ru/search-api/pricing.html`

Therefore O-001 must **not** blindly send a complete 500- or 10,000-keyword semantic core to GenSearch.

Correct workflow:

```text
large human-demand set
→ ChatGPT cleans/clusters
→ ordinary Search resolves many questions cheaply
→ ChatGPT selects a small decision-relevant AI test set
→ GenSearch only for material uncertainty / AI-specific measurement
```

This matches the original `blood_sand` research discipline.

## 8. Current product implication

Previous wording `missing hand = repeatable Alice UI capture` is now too narrow.

Updated product hypothesis:

```text
preferred future hand = official GenSearch acquisition inside Search provider family
consumer Alice capture = bounded validation/reference layer, not default bulk transport
```

This reduces implementation risk because the official API gives structured data and avoids dependence on consumer UI DOM/state.

## 9. What GenSearch does NOT prove

Even when the API is implemented, do not claim:

- exact equivalence to the current consumer Alice UI;
- guaranteed Alice citation/indexing;
- deterministic source inclusion;
- a consumer-visible source ranking from `sources[]` order;
- that `searchQueries[]` are necessarily identical to consumer Alice fan-out;
- guaranteed traffic or commercial uplift.

Those require separate evidence.

## 10. Implementation gate

GenSearch-specific `extension/src` changes are **not yet authorized** solely because the endpoint exists.

Order:

```text
Phase 5 Direct = CLOSED
→ valid blood_sand comparative methodology gate
→ evaluate incremental decision uplift
→ if justified, promote GenSearch hand to implementation priority
→ run bounded GenSearch-vs-canonical-Alice proxy validation
→ freeze exact provider/protocol contract
→ implement/test
```

Read-only provider research may continue in parallel.

## 11. Current conclusion

The official API route materially strengthens O-001 feasibility:

```text
AI analysis = ChatGPT can do it
human demand = existing Wordstat hand
ordinary Search = existing Search hand
repeatable AI-search acquisition = official GenSearch path exists
post-launch ordinary search = existing Webmaster hand
post-launch AI visibility = still needs an official/stable acquisition path or controlled import
```

The remaining uncertainty is no longer `how can we collect any AI answer at all?`.

It is:

> Does the additional AI evidence materially improve our decisions, and how faithfully does official GenSearch represent the decision-relevant behavior seen in consumer Alice?

Those questions are now explicitly gated and testable.