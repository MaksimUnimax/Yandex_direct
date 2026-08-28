# AI-native GenSearch proxy validation — G01

Date: 2026-08-28

Root: `печать велеса`

## Provider execution

Valid observation:

```text
protocol = SEARCH_API_V1
method = genSearch
request_id = search-fe9bbf81-5e2f-40ce-b403-12af9094c497
status = OK
http_status = 200
elapsed_ms = 3558
request_executed = true
automatic_retry = false
transport.wire_format = json_array
transport.frame_count = 1
estimated_rub = 5.08
```

There was one earlier paid-boundary G01 attempt that returned HTTP-success JSON but failed in the pre-R3 local response parser with `INVALID_SEARCH_RESPONSE`. It is not used as semantic evidence, but it is conservatively counted as an additional provider request for economics. Therefore:

```text
valid_proxy_observations = 1
provider_requests_for_G01 = 2
conservative_estimated_provider_cost_rub_for_G01 = 10.16
```

No automatic retry occurred.

## GenSearch observation

Answer orientation is strongly meaning/explanation-first. The answer covers:

- Velес-related symbolic meaning and mythology;
- visual/form interpretation;
- bear-paw vs wolf-paw forms;
- suitability/claimed protective meanings;
- an explicit caveat that magical properties are not scientifically established.

Structured sources returned 5 entries. Four were marked `used=true`; one Yandex Market category was `used=false`. Used source types include specialist explanatory commerce-content, a general marketplace/listings surface, and another specialist product/content page.

Observed GenSearch query expansion was conservative:

```text
searchQueries = ["печать велеса"]
```

Hints expanded into usage, related Veles amulets and legends, but hints are not relabeled as consumer-Alice fan-out.

## Canonical consumer-Alice comparator

Frozen Pass B records the same unmodified root as meaning/explanation-first and explicitly notes forms, symbolism, historical/ritual use, bear-vs-wolf distinctions, wearing caveats and modern use. Pass B also records informational plus independent commerce-content source participation and consumer fan-out around historical use, related Veles symbols and legends.

Canonical reference:

`extension/tests/AI_NATIVE_BLOOD_SAND_AI_NATIVE_PASS_B_2026-08-27.md`

## Comparison

```text
answer_job_orientation = SAME_OR_STRONGLY_ALIGNED
commercial_vs_explanatory_orientation = SAME_OR_STRONGLY_ALIGNED
source_type_orientation = SAME_OR_STRONGLY_ALIGNED
exact_source_url_overlap = NOT_ASSERTED_FROM_CURRENT_ACCESSIBLE_EVIDENCE
consumer_fanout_vs_genSearch_searchQueries = PARTIALLY_ALIGNED / GEN_SEARCH_NARROWER
material_page_job_implication = SAME
```

The decision-relevant implication is preserved: `печать велеса` requires a commercial symbol-family landing paired with a substantial meaning/use/history asset; AI/source-worthiness is real, not merely transactional SERP behavior.

GenSearch does **not** reproduce the richer consumer-Alice fan-out on this root via `searchQueries[]`; therefore `searchQueries[]` must remain separate provenance and is not a substitute for Alice fan-out.

## G01 verdict

```text
classification = SAME_OR_STRONGLY_ALIGNED
comparable = true
systematic_contradiction = false
proxy_signal_useful = true
source_auditability = sufficient_for_this_root
```

G01 supports continuing the bounded five-root validation. It does not by itself authorize a claim of exact consumer-Alice equivalence.
