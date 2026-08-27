# AI-native provider research — Yandex GenSearch / Alice-related evidence

Date: 2026-08-27

Status: **OFFICIAL PROVIDER PATH FOUND / METHODOLOGY GATE PASSED / BOUNDED PROXY VALIDATION AUTHORIZED**

Applies to: O-001 AI-Native Semantic Rebuild.

## 1. Official path

Yandex exposes generative search inside the existing Yandex Search API family:

```text
POST https://searchapi.api.cloud.yandex.net/v2/gen/search
```

Important structured response fields include:

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

This is architecturally preferable to relying on consumer-UI DOM scraping for repeatable production acquisition.

## 2. Provider / credential boundary

Preferred provider shape:

```text
Yandex Search hand
├── ordinary WebSearch
│   └── /v2/web/search
└── generative GenSearch
    └── /v2/gen/search
```

GenSearch should reuse the Search/Yandex Cloud credential-policy family. Webmaster, Metrika and Direct credentials remain separate.

Do not create a credential-consolidation project as part of this work.

## 3. Provenance contract

GenSearch evidence must never be silently relabeled as consumer-Alice evidence.

Use explicit provenance such as:

```text
GEN_SEARCH_INPUT
GEN_SEARCH_ANSWER
GEN_SEARCH_SOURCE
GEN_SEARCH_SOURCE_USED
GEN_SEARCH_QUERY_OBSERVED
```

Do not automatically map:

```text
searchQueries[] -> ALICE_FANOUT_OBSERVED
```

Consumer Alice and GenSearch remain distinct evidence surfaces until the bounded proxy comparison says how useful/aligned they are for the decision task.

## 4. Why implementation priority is now justified

The broader controlled methodology comparison is complete:

`extension/tests/AI_NATIVE_BLOOD_SAND_COMPARISON_2026-08-27.md`

Verdict:

```text
AI_NATIVE_COMPARATIVE_GATE_PASS
```

Material value was observed in page-job scope, priority, source-worthiness and contamination control. Therefore AI-specific engineering is no longer blocked by "unproven incremental value".

What remains unproven is whether GenSearch is a sufficiently useful structured proxy/reference surface for the decision-relevant behavior observed in consumer Alice.

## 5. Required bounded proxy validation

Use a **small representative set**, not a bulk keyword run.

Recommended roots are chosen to cover materially different uncertainty classes already captured in canonical consumer Alice:

```text
1. печать велеса
   - Search transactional vs Alice meaning/history/use-first
   - observed consumer fan-out exists

2. оберег в машину
   - hybrid choice/use-case + direct shopping/products

3. вегвизир
   - history/meaning/correction-first with factual provenance sensitivity

4. алатырь оберег
   - commercial Search vs mythology/meaning/suitability Alice

5. подарок мужчине в машину
   - contamination-control case; only clean canonical consumer-Alice observation is comparator
```

Five requests are enough for the first bounded decision test unless a specific result is non-comparable and one replacement is justified.

At the recorded 2026-08-27 pricing snapshot of roughly `5.08 RUB/request`, this initial five-root set is approximately `25.40 RUB` of provider cost.

## 6. Comparison fields

For every root compare:

```text
root query
consumer-Alice answer/user-job orientation
GenSearch answer/user-job orientation
consumer-Alice source domains/types
GenSearch sources[].url/title/used
source overlap where exact comparison is possible
consumer observed fan-out, if any
GenSearch searchQueries[] themes
commercial vs explanatory orientation
material semantic/page-job implication
```

Per-root classification:

```text
SAME_OR_STRONGLY_ALIGNED
PARTIALLY_ALIGNED
MATERIALLY_DIFFERENT
NOT_COMPARABLE
```

Do not require text equivalence. The product question is whether the structured provider surface preserves enough decision-relevant signal to serve the premium workflow reliably.

## 7. Acceptance logic

A production GenSearch hand may be promoted when:

1. the bounded set has no unexplained systematic contradiction with canonical consumer-Alice jobs;
2. material page-job implications remain sufficiently aligned or the differences are explicitly usable as separate provenance;
3. structured source evidence is complete enough for audit;
4. `searchQueries[]` are stored as GenSearch-observed queries, not consumer fan-out;
5. cost/request boundaries are explicit;
6. provider errors/unknown outcomes remain fail-closed and do not auto-retry paid requests.

A result may still be useful if some roots are only `PARTIALLY_ALIGNED`; exact consumer-Alice equivalence is not the requirement.

If several representative roots are `MATERIALLY_DIFFERENT` in ways that would change recommendations, GenSearch must remain a separate AI-search surface rather than a consumer-Alice proxy.

## 8. Economics / operating rule

Recorded pricing snapshot:

```text
synchronous generative Search API ≈ 5.08 RUB/request
```

Production workflow must remain selective:

```text
large Wordstat set
→ ChatGPT cleans/clusters
→ ordinary Search resolves most questions
→ ChatGPT selects decision-relevant AI test roots
→ bounded GenSearch calls
→ provenance-preserving analysis
```

No hidden loops and no bulk GenSearch over the whole semantic core by default.

## 9. Implementation sequence

Current authorized order:

```text
methodology comparative gate = PASS
→ bounded GenSearch-vs-canonical-Alice validation
→ if sufficiently useful/aligned:
     freeze provider/protocol contract
     implement inside Search provider family
     add focused tests + full pre-delivery regression
     run controlled owner-live acceptance
→ if materially divergent:
     keep provenance separate
     revise product claim / acquisition design before production hand
```

GenSearch production protocol names are intentionally not frozen before the proxy result.

## 10. What GenSearch does not prove

Even after implementation, never claim:

- exact equivalence to consumer Alice;
- guaranteed Alice citation/indexing;
- deterministic source inclusion;
- consumer-visible ranking from `sources[]` order;
- `searchQueries[]` == consumer Alice fan-out;
- guaranteed traffic, ranking or revenue uplift.

## 11. Current conclusion

```text
AI methodology incremental value = PROVEN ON CONTROLLED REAL DATASET
official structured GenSearch path = FOUND
bounded proxy validation = AUTHORIZED / PENDING
production GenSearch hand = NOT YET FROZEN
```

The next uncertainty is specific and testable:

> On representative roots, does official GenSearch preserve enough of the decision-relevant behavior observed in canonical consumer Alice to be the repeatable structured AI-search hand for O-001?
