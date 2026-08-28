# AI-native GenSearch proxy validation — G02

Date: 2026-08-28

Root: `оберег в машину`

## Provider execution

```text
protocol = SEARCH_API_V1
method = genSearch
request_id = search-c4a83ad5-848b-4987-a5c8-beb3d6abedc7
status = OK
http_status = 200
elapsed_ms = 3406
request_executed = true
automatic_retry = false
transport.wire_format = json_array
transport.frame_count = 1
estimated_rub = 5.08
```

Exactly one provider request was observed for this root and no automatic retry occurred.

## GenSearch observation

The answer is strongly shopping/product-list oriented. It gives concrete product examples such as road-protection amulets, driver charms and keychain-style products, then explicitly points to Yandex Market, AliExpress and Ozon as purchase surfaces.

Structured sources returned 5 entries. Three marketplace/category sources were marked `used=true` (Yandex Market, AliExpress, Ozon); two specialist commerce sources were present but `used=false`.

Observed GenSearch query evidence is narrow:

```text
searchQueries = ["оберег в машину"]
```

Hints retain useful explanatory/selection themes:

- functions of automotive amulets;
- how to choose one;
- suitable materials.

Hints remain GenSearch hints and are not relabeled as consumer-Alice fan-out.

## Canonical consumer-Alice comparator

Frozen Pass B records canonical consumer Alice for the same root as a hybrid choice/use-case + shopping answer with directly orderable products. It also records a mixed source set including specialist commerce-content, marketplaces, public information and media.

Canonical reference:

`extension/tests/AI_NATIVE_BLOOD_SAND_AI_NATIVE_PASS_B_2026-08-27.md`

## Comparison

```text
answer_job_orientation = PARTIALLY_ALIGNED
commercial_orientation = GEN_SEARCH_MORE_SHOPPING_HEAVY
selection_use_case_orientation = ALICE_STRONGER
source_type_orientation = PARTIALLY_ALIGNED
exact_source_url_overlap = NOT_ASSERTED
consumer_fanout_vs_genSearch_searchQueries = GEN_SEARCH_NARROWER
material_page_job_implication = SAME
```

The material page-job implication remains the same: automotive protection should stay a hybrid choice/use-case commerce category rather than collapse into a pure product grid. GenSearch preserves direct shopping demand very well, while canonical consumer Alice carries more of the explanatory/choice layer in the main answer. GenSearch hints partly recover that layer, but hints are weaker evidence than answer orientation.

## G02 verdict

```text
classification = PARTIALLY_ALIGNED
comparable = true
systematic_contradiction = false
proxy_signal_useful = true
source_auditability = sufficient_for_this_root
```

This is a useful difference rather than a recommendation-changing contradiction. It argues for preserving GenSearch and consumer Alice as distinct provenance surfaces even if GenSearch becomes the repeatable structured acquisition hand.