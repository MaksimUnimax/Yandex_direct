# KW-002 — LEVEL 2 STEP 02 SEED / ACQUISITION QUALITY GATE

Status: **ACTIVE / REQUIRED / OVERRIDES EARLIER STEP-02 TEXT WHERE CONFLICT EXISTS**  
Owner correction: 2026-09-08

## 1. Purpose

Step 02 does **not** merely prove that every catalog row has some seed.

It must build a search-discovery probe set that is likely to reveal relevant Yandex demand without being dominated by avoidable ambiguity/noise.

```text
CATALOG ROUTE COVERAGE != SEARCH-PROBE QUALITY COVERAGE
SEED != FINAL KEYWORD
SEED != SEO CLUSTER
SEED != PAGE
```

## 2. Failure history that this gate prevents

The first Blood & Sand Step-02 execution produced 97 probes and achieved 76/76 catalog-route coverage, but a later external-method audit found substantive defects:

```text
1. any primary route was counted as quality coverage;
2. high-noise bare names could remain PRIMARY without a refinement route;
3. use-context synonym coverage was unsystematic;
4. every distinct seller name tended to become PRIMARY by default;
5. expected_information_gain was often boilerplate rather than discriminating;
6. PRIMARY/DEFERRED rationale could over-emphasize request count/cost instead of information gain.
```

These are permanent non-repeat controls for Step 02.

## 3. External method basis

### OFFICIAL_YANDEX

Yandex Webmaster — query selection / market analysis:

https://yandex.ru/support/webmaster/ru/service/queries-selection

Yandex Direct — building keyword lists:

https://yandex.ru/support/direct/ru/keywords/building-keyword-list

Yandex Wordstat GetTop:

https://aistudio.yandex.ru/en/docs/search-api/api-ref/grpc/Wordstat/getTop

Yandex Wordstat operators:

https://yandex.ru/support2/wordstat/ru/content/operators

Supported principles:

```text
- start from words describing the real business/offer;
- discover additional and non-obvious user formulations;
- overly broad/ambiguous formulations should be qualified/refined;
- relevant synonyms/alternative wording matter;
- Wordstat seed is an acquisition input, not a final-keyword verdict;
- operators may be used deliberately to control a concrete measurement question.
```

### INDUSTRY_PRACTICE

Ahrefs seed keywords:
https://ahrefs.com/blog/seed-keywords/

Semrush seed keywords / ecommerce keyword research:
https://www.semrush.com/blog/seed-keywords/
https://www.semrush.com/blog/ecommerce-keyword-research/

Supported principles:

```text
- seed quality and diversity affect discovered keyword universe;
- exact seller vocabulary is only one source of seeds;
- related terminology/variations matter;
- relevance/volume/intent are validated after discovery;
- competitor-derived expansion is a valid later source of new seeds.
```

## 4. Required seed classes

Use only classes with a named discovery purpose. Typical classes:

```text
CLIENT_HEAD_CLASS
EXPLICIT_USE_OR_FORM
ANALYST_COMPOSED_USE_DIAGNOSTIC
EXACT_NAMED_PRODUCT_OR_SYMBOL
EXPLICIT_ALIAS_OR_ALTERNATE_WRITING
FAMILY_SCOPED
QUALIFIED_NAME_REFINEMENT
VARIANT_MARKER_DIAGNOSTIC
BRAND_CONTROL
```

No class is automatically PRIMARY.

## 5. Ambiguity/noise classification is mandatory

Every candidate seed must receive:

```text
ambiguity_noise_class = LOW | MEDIUM | HIGH
```

HIGH means the bare phrase is likely to have substantial unrelated/non-product interpretations or homonymy.

Examples can include broad concepts, religious/informational phrases, common names/words, brands/media titles or ambiguous abbreviations.

## 6. High-noise bare seed rule

A HIGH-noise bare seed may not be treated as sufficient quality coverage by itself.

It must be one of:

```text
A. BROAD_CONTROL_PRIMARY
   deliberately broad root used to discover vocabulary, with separate qualified routes elsewhere;

B. CONTROL_DEFERRED
   preserved for later/control use but not counted as main quality coverage;

C. PRIMARY_WITH_REFINEMENT
   bare control may run, but at least one explicit qualified/refinement route is also PRIMARY.
```

Required fields:

```text
refinement_strategy
paired_refinement_seed_ids
quality_coverage_role
```

For a named product where exact physical class is unknown, qualification may use explicitly labelled analyst-composed business-class context without pretending the class is a client fact.

## 7. Qualified probe must not become invented product truth

Allowed:

```text
client says business sells amulets/oberegs/talismans
+
client catalog contains name X
→ analyst may compose diagnostic qualified probes around X
```

But:

```text
ANALYST-COMPOSED QUALIFIER != PROOF PRODUCT X IS THAT CLASS
```

The seed must say it is a diagnostic composition.

When useful, Wordstat OR grouping may be used as a measurement construction if supported by current Wordstat operator semantics, e.g. a business-class OR group around an ambiguous name. Such operator use must be labelled and preserved.

## 8. Search-probe quality coverage is separate from catalog coverage

Step 02 must maintain two different QA views:

```text
CATALOG_LINEAGE_COVERAGE
= every material client offer/name has a traceable discovery route

SEARCH_PROBE_QUALITY_COVERAGE
= every material direction has at least one route whose ambiguity/noise/refinement plan is acceptable
```

PASS requires both.

A row cannot be counted as quality-covered merely because one bare noisy name points to it.

## 9. Use-context synonym coverage must be systematic but bounded

When client facts establish a material use context, Step 02 must identify a small justified synonym/formulation axis rather than rely on one wording only.

Example job-level pattern:

```text
машина
автомобиль
авто
в машину
для машины
для автомобиля
для авто
```

This is NOT a universal requirement to multiply every noun by every synonym.

Required procedure:

```text
1. identify confirmed use context;
2. identify the smallest distinct wording set likely to reveal different user formulations;
3. compose only information-gaining combinations;
4. explain why each chosen form is distinct;
5. avoid combinatorial padding.
```

## 10. Exact seller names cannot automatically become PRIMARY

Forbidden default:

```text
EVERY DISTINCT SELLER TITLE/NAME -> PRIMARY
```

For each exact name decide:

```text
PRIMARY
CONTROL_PRIMARY
CONTROL_DEFERRED
QUALIFIED_PRIMARY
DEFERRED_TARGETED
```

based on:

```text
ambiguity/noise
distinct discovery value
availability of broader/qualified routes
redundancy with aliases/family probes
expected information gain
```

## 11. Information-gain rationale must discriminate

Forbidden boilerplate:

```text
"high because it covers this product name"
```

Each PRIMARY/DEFERRED decision must explain why this probe is useful **now** versus later/never.

At minimum distinguish:

```text
UNIQUE_DISCOVERY_BRANCH
BROAD_CONTROL
QUALIFIED_REFINEMENT
SYNONYM_COVERAGE
REDUNDANT_ALIAS_CONTROL
VARIANT_ONLY_AFTER_BASE_DEMAND
BRAND_CONTROL
HIGH_NOISE_LOW_VALUE
```

## 12. Provider cost is secondary to quality

Do not defer a distinct useful probe merely to save trivial request cost.

```text
INFORMATION_GAIN / COVERAGE / RELIABILITY
>
TRIVIAL REQUEST-COUNT SAVING
```

This does not mean run every possible combination. Redundancy/noise can still justify deferral.

## 13. Required Step-02 fields

Every final seed record must preserve at minimum:

```text
seed_id
seed_phrase
seed_class
seed_source_type
source_lineage
seed_purpose
question_to_resolve
expected_information_gain
ambiguity_noise_class
quality_coverage_role
refinement_strategy
paired_refinement_seed_ids
synonym_axis
region
planned_wordstat_mode
operator_mode
execution_priority
claim_boundary
status
```

## 14. Primary acquisition manifest

Step 02 must materialize a deterministic primary acquisition manifest for Step 03.

The manifest must not require Step 03 to infer which seeds are current.

It must explicitly enumerate every executable primary probe and its source/version.

## 15. QA requirements

At minimum:

```text
ALL_SEEDS_HAVE_SOURCE_LINEAGE = true
ALL_SEEDS_HAVE_EXPLICIT_PURPOSE = true
ALL_SEEDS_HAVE_DISCRIMINATING_INFO_GAIN = true
ALL_SEEDS_HAVE_NOISE_CLASS = true
HIGH_NOISE_PRIMARY_WITHOUT_REFINEMENT_OR_CONTROL_JUSTIFICATION = 0
MATERIAL_DIRECTIONS_WITHOUT_CATALOG_LINEAGE_ROUTE = 0
MATERIAL_DIRECTIONS_WITHOUT_SEARCH_QUALITY_ROUTE = 0
MATERIAL_USE_CONTEXT_WITHOUT_BOUNDED_SYNONYM_PLAN = 0
SELLER_NAMES_PROMOTED_TO_PRIMARY_BY_DEFAULT = 0
ANALYST_COMPOSED_PROBES_UNLABELLED = 0
STEP01_BUCKETS_USED_AS_SEO_TAXONOMY = 0
REDUNDANT_PROBES_WITHOUT_REASON = 0
COST_ONLY_DEFER_DECISIONS = 0
WORDSTAT_CALLS_IN_STEP02 = 0
SEARCH_CALLS_IN_STEP02 = 0
AI_SEARCH_CALLS_IN_STEP02 = 0
OLD_RESEARCH_CONTAMINATION = 0
```

## 16. 10-point quality scoring for Step 02

Apply Level-1 `RESULT_QUALITY_SCORING_RULE.md`.

Step-specific quality focus:

```text
- probe quality, not just row coverage;
- ambiguity/refinement governance;
- synonym/use-context coverage;
- seller-vocabulary dependence;
- discriminating information-gain logic;
- deterministic readiness for Step 03.
```

Step 02 cannot PASS below **9.0/10** or with any open substantive defect.

## 17. PASS

```text
CATALOG_LINEAGE_COVERAGE = PASS
SEARCH_PROBE_QUALITY_COVERAGE = PASS
HIGH_NOISE_PRIMARY_WITHOUT_GOVERNED_ROUTE = 0
USE_CONTEXT_SYNONYM_PLAN = PASS
INFO_GAIN_RATIONALE = PASS
PRIMARY_ACQUISITION_MANIFEST = MATERIALIZED
STEP02_QUALITY_SCORE >= 9.0/10
ALL HARD GATES = PASS
REMOTE_READBACK = PASS
```

Only then:

```text
STEP_02 = COMPLETE / PASS
NEXT_STEP_ALLOWED = true
NEXT_STEP = STEP_03_PRIMARY_WORDSTAT_ACQUISITION
```
