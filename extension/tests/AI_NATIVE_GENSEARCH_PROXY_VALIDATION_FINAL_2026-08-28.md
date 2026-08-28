# AI-native GenSearch proxy validation — final

Date: 2026-08-28

Status: **COMPLETE**

```text
AI_NATIVE_GENSEARCH_PROXY_VALIDATION_PASS
representative_roots = 5
valid_observations = 5
systematic_contradictions = 0
production_claim_exact_consumer_alice_equivalence = FORBIDDEN
```

## Purpose

Determine whether official Yandex GenSearch preserves enough decision-relevant behavior from the frozen canonical consumer-Alice evidence to serve as the repeatable structured AI-search hand for O-001 AI-Native Semantic Rebuild.

This validation does **not** test text equivalence. It tests page-job orientation, commercial-vs-explanatory behavior, source usefulness/auditability, contamination behavior and semantic decision implications.

## Evidence set

| ID | Root | Classification | Decision-relevant result |
|---|---|---|---|
| G01 | `печать велеса` | SAME_OR_STRONGLY_ALIGNED | meaning/explanation-first behavior, forms/symbolism and specialist source-worthiness preserved; GenSearch query expansion narrower than consumer fan-out |
| G02 | `оберег в машину` | PARTIALLY_ALIGNED | GenSearch is more shopping/product-list oriented than consumer Alice, but the same hybrid automotive-protection commerce job remains valid; no contradictory architecture action |
| G03 | `вегвизир` | SAME_OR_STRONGLY_ALIGNED | history/meaning/correction-first behavior preserved, including Huld 1860 and absence of confirmed Viking-age provenance |
| G04 | `алатырь оберег` | SAME_OR_STRONGLY_ALIGNED | meaning/mythology/suitability-first behavior and hybrid content-commerce implication preserved |
| G05 | `подарок мужчине в машину` | SAME_OR_STRONGLY_ALIGNED | clean practical-gift behavior preserved; no amulet/Veles/Vegvisir injection; contamination-control conclusion confirmed |

Per-root evidence:

- `extension/tests/AI_NATIVE_GENSEARCH_PROXY_G01_2026-08-28.md`
- `extension/tests/AI_NATIVE_GENSEARCH_PROXY_G02_2026-08-28.md`
- `extension/tests/AI_NATIVE_GENSEARCH_PROXY_G03_2026-08-28.md`
- `extension/tests/AI_NATIVE_GENSEARCH_PROXY_G04_2026-08-28.md`
- `extension/tests/AI_NATIVE_GENSEARCH_PROXY_G05_2026-08-28.md`

Canonical consumer-Alice comparator remains frozen in:

`extension/tests/AI_NATIVE_BLOOD_SAND_AI_NATIVE_PASS_B_2026-08-27.md`

## Aggregate result

```text
SAME_OR_STRONGLY_ALIGNED = 4
PARTIALLY_ALIGNED = 1
MATERIALLY_DIFFERENT = 0
NOT_COMPARABLE = 0
systematic_contradiction = false
material_wrong-way_page_job_change = false
structured_source_auditability = sufficient
contamination_control = pass
```

The only partial-alignment case is G02 `оберег в машину`: GenSearch overweights direct product/shopping presentation relative to the richer consumer-Alice choice/use-case layer. This difference is useful and explainable, not a contradiction. It does not reverse the owned-site action because the existing hybrid choice/use-case commerce page remains required by the broader evidence stack.

## Important non-equivalence

Across the bounded set, GenSearch `searchQueries[]` was consistently conservative and usually repeated only the root query. Consumer-Alice fan-out can be materially richer.

Therefore:

```text
GEN_SEARCH_QUERY_OBSERVED != ALICE_FANOUT_OBSERVED
GEN_SEARCH_ANSWER != CONSUMER_ALICE_ANSWER
GEN_SEARCH_SOURCE != CONSUMER_ALICE_SOURCE
```

GenSearch is accepted as a distinct structured AI-search evidence surface, not as a hidden relabeling of consumer Alice.

## Provider/runtime behavior observed

The final R3 validation candidate returned successful live GenSearch observations with:

```text
HTTP 200
request_executed = true
automatic_retry = false
transport.wire_format = json_array
transport.frame_count = 1
```

The R3 parser was designed after checking the official GenSearch contract and accepts the observed response framing while preserving ordinary Search behavior separately.

## Economics

Five valid observations required five successful paid provider requests. G01 also had one earlier paid-boundary request whose valid provider JSON could not be consumed by the pre-R3 parser; it is excluded from semantic evidence but counted conservatively in cost.

```text
valid_successful_requests = 5
additional_paid_parser_failure_request = 1
total_provider_requests_crossing_paid_boundary = 6
estimated_rub_per_request = 5.08
conservative_total_estimated_rub = 30.48
automatic_retries = 0
```

Admission/delivery failures and `OPERATION_DISABLED` attempts had `request_executed=false` and are not counted as provider requests.

## Acceptance logic

The bounded set satisfies the previously defined acceptance conditions:

1. no unexplained systematic contradiction with canonical consumer-Alice jobs;
2. material page-job implications are aligned or differences are explicitly useful under separate provenance;
3. structured source evidence is sufficient for audit on every root;
4. `searchQueries[]` remain GenSearch provenance and are not relabeled as Alice fan-out;
5. cost/request boundary is explicit;
6. provider errors are fail-closed and paid requests have no automatic retry.

## Final verdict

```text
AI_NATIVE_GENSEARCH_PROXY_VALIDATION_PASS
```

Official Yandex GenSearch preserves enough decision-relevant AI-search signal to be promoted as the repeatable structured AI-search hand for O-001, subject to strict provenance separation and the normal production delivery gates.

This verdict authorizes freezing the production GenSearch provider/protocol contract inside the existing Search service family. It does **not** authorize claims of exact consumer-Alice equivalence, deterministic citation behavior, consumer-visible ranking equivalence, or guaranteed traffic/revenue outcomes.

## Next product action

```text
proxy validation = PASS
→ freeze GenSearch production protocol/provenance contract
→ run complete pre-delivery regression on exact product source
→ controlled owner-live acceptance / product delivery gate
→ only after those gates, promote into main
```
