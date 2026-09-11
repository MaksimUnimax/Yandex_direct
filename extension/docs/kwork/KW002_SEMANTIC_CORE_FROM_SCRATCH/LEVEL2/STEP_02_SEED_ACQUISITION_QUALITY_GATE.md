# KW-002 — LEVEL 2 STEP 02 SEED / ACQUISITION QUALITY GATE

Status: **ACTIVE / UNIVERSAL / REQUIRED / APPLIES TO ANY KW-002 SITE**

Companion universal authorities:

- `../LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`
- `../LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`

## 1. Purpose

Step 02 builds a **search-discovery probe set**, not a catalog checklist and not a final keyword list.

```text
BUSINESS/CATALOG ROUTE COVERAGE != SEARCH-PROBE QUALITY COVERAGE
SEED != FINAL KEYWORD
SEED != SEO CLUSTER
SEED != PAGE
```

The step must create probes likely to reveal how users actually search for the current business while controlling avoidable ambiguity and redundancy.

## 2. Universal failure mechanisms this step prevents

### 2.1 Business-accounting completeness mistaken for search completeness

Root cause:

A project proves that every product/service/entity has at least one seed and treats that accounting result as evidence that market vocabulary is adequately discoverable.

Why this fails:

Client/business vocabulary can differ materially from user vocabulary. Users search with synonyms, use cases, problems, attributes, colloquial forms and alternative names.

Control:

```text
BUSINESS_LINEAGE_COVERAGE
AND
SEARCH_PROBE_QUALITY_COVERAGE
must be separate QA dimensions.
```

### 2.2 Ambiguous bare names treated as sufficient primary probes

Root cause:

Exact names look authoritative because they came from the client, but many names are homonyms, brands, concepts or terms with unrelated meanings.

Why this fails:

A broad ambiguous probe can return a large noisy universe and still fail to expose the intended business meaning.

Control:

High-noise bare probes require a refinement/control strategy.

### 2.3 Client taxonomy copied directly into acquisition taxonomy

Root cause:

The analyst assumes that every distinct seller title/category/label deserves its own primary acquisition route.

Why this fails:

Several business labels can map to one user vocabulary branch; conversely, one business label can require several search formulations.

Control:

Each probe must justify distinct discovery value and incremental information gain.

### 2.4 Request-count/cost minimization overrides information gain

Root cause:

Provider cost or execution convenience becomes the dominant criterion for probe selection.

Why this fails:

A cheap but under-informative probe plan can systematically miss vocabulary and create false confidence downstream.

Control:

```text
INFORMATION_GAIN / COVERAGE / RELIABILITY
>
TRIVIAL REQUEST-COUNT SAVING
```

## 3. External method basis

Official Yandex:

- Yandex Webmaster — query selection / market analysis: https://yandex.ru/support/webmaster/ru/service/queries-selection
- Yandex Direct — building keyword lists: https://yandex.ru/support/direct/ru/keywords/building-keyword-list
- Yandex Wordstat GetTop: https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop
- Yandex Wordstat operators: https://yandex.ru/support2/wordstat/ru/content/operators

Industry corroboration:

- Ahrefs — seed keywords: https://ahrefs.com/blog/seed-keywords/
- Semrush — seed keywords: https://www.semrush.com/blog/seed-keywords/
- Semrush — ecommerce keyword research: https://www.semrush.com/blog/ecommerce-keyword-research/

These sources support the general principles that seed diversity affects discovery, ambiguous/broad formulations may need refinement, and seed relevance is not final keyword/page relevance.

## 4. Required seed dimensions

Use only dimensions with a named discovery purpose. Depending on business type, candidates may include:

```text
HEAD_PRODUCT_OR_SERVICE
SYNONYM_OR_COMMON_NAMING_VARIANT
CATEGORY_OR_FAMILY_TERM
USE_CASE
PROBLEM_OR_NEED
ATTRIBUTE_OR_FORM_FACTOR
COMMERCIAL_MODIFIER
EXACT_NAMED_PRODUCT_OR_SERVICE
QUALIFIED_NAME_REFINEMENT
BRAND_CONTROL
REGIONAL_OR_CONTEXTUAL_VARIANT
```

No class is automatically PRIMARY.

## 5. Ambiguity/noise classification

Every candidate seed receives:

```text
ambiguity_noise_class = LOW | MEDIUM | HIGH
```

HIGH means the bare phrase is likely to contain substantial unrelated interpretations, homonymy or category ambiguity.

This classification is about expected acquisition noise, not final relevance.

## 6. High-noise bare seed rule

A HIGH-noise bare seed cannot alone satisfy search-quality coverage.

It must be governed as one of:

```text
BROAD_CONTROL_PRIMARY
CONTROL_DEFERRED
PRIMARY_WITH_REFINEMENT
```

Required fields:

```text
refinement_strategy
paired_refinement_seed_ids
quality_coverage_role
```

A qualified probe may combine a confirmed business class with an ambiguous exact name, but must be labelled as analyst-composed measurement logic rather than client product truth.

## 7. Analyst-composed qualifier boundary

Allowed generic pattern:

```text
client/business confirms class C
+
client/business confirms name/entity X
→ analyst may compose a diagnostic probe C + X
```

But:

```text
ANALYST-COMPOSED QUALIFIER != PROOF THAT X IS SOLD/DEFINED EXACTLY AS C
```

The measurement construction and factual business claim remain separate.

## 8. Two independent coverage views

Step02 must maintain:

```text
BUSINESS_LINEAGE_COVERAGE
= every material offer/direction has at least one traceable discovery route

SEARCH_PROBE_QUALITY_COVERAGE
= every material direction has at least one probe whose ambiguity/refinement/information-gain plan is acceptable
```

PASS requires both.

## 9. Synonym/use-context coverage

When client facts establish a material use context or naming axis, define the smallest justified set of distinct formulations likely to reveal different search language.

Procedure:

```text
1. identify confirmed business/use context;
2. identify plausible materially distinct wording variants;
3. keep only information-gaining formulations;
4. document why each variant is not redundant;
5. avoid combinatorial multiplication.
```

No fixed synonym list is universal.

## 10. Exact business names cannot automatically become PRIMARY

Forbidden default:

```text
EVERY DISTINCT CLIENT TITLE/NAME -> PRIMARY
```

For each exact name choose, with rationale:

```text
PRIMARY
CONTROL_PRIMARY
CONTROL_DEFERRED
QUALIFIED_PRIMARY
DEFERRED_TARGETED
```

based on ambiguity, distinct discovery value, redundancy, refinement availability and expected information gain.

## 11. Information-gain rationale

Each PRIMARY/DEFERRED decision must explain why the probe is useful now versus later or never.

Useful generic reason classes:

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

Boilerplate such as “covers this product/service name” is insufficient.

## 12. Provider cost is secondary

Do not run every possible combination. But do not defer a distinct useful probe merely to save trivial provider cost.

Redundancy, low expected information gain or unresolved business facts are valid reasons to defer.

## 13. Required Step02 fields

Every final seed record preserves at minimum:

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
planned_provider_mode
operator_mode
execution_priority
claim_boundary
status
```

## 14. Primary acquisition manifest

Step02 must materialize a deterministic primary acquisition manifest for Step03. Step03 must not infer which probes are current.

## 15. QA requirements

```text
ALL_SEEDS_HAVE_SOURCE_LINEAGE = true
ALL_SEEDS_HAVE_EXPLICIT_PURPOSE = true
ALL_SEEDS_HAVE_DISCRIMINATING_INFO_GAIN = true
ALL_SEEDS_HAVE_NOISE_CLASS = true
HIGH_NOISE_PRIMARY_WITHOUT_REFINEMENT_OR_CONTROL_JUSTIFICATION = 0
MATERIAL_DIRECTIONS_WITHOUT_BUSINESS_LINEAGE_ROUTE = 0
MATERIAL_DIRECTIONS_WITHOUT_SEARCH_QUALITY_ROUTE = 0
MATERIAL_USE_CONTEXT_WITHOUT_BOUNDED_SYNONYM_PLAN = 0
CLIENT_NAMES_PROMOTED_TO_PRIMARY_BY_DEFAULT = 0
ANALYST_COMPOSED_PROBES_UNLABELLED = 0
BUSINESS_TAXONOMY_USED_AS_FINAL_SEO_TAXONOMY = 0
REDUNDANT_PROBES_WITHOUT_REASON = 0
COST_ONLY_DEFER_DECISIONS = 0
PROVIDER_CALLS_IN_STEP02 = 0
ORDINARY_SEARCH_CALLS_IN_STEP02 = 0
AI_SEARCH_CALLS_IN_STEP02 = 0
JOB_SPECIFIC_RULES_IN_LEVEL2 = 0
```

## 16. Quality scoring

Apply Level-1 `RESULT_QUALITY_SCORING_RULE.md`.

Step-specific focus:

```text
probe quality
ambiguity/refinement governance
synonym/use-context coverage
client-vocabulary dependence
information-gain quality
deterministic readiness for Step03
```

No numeric score can override a failed hard gate.

## 17. PASS

```text
BUSINESS_LINEAGE_COVERAGE = PASS
SEARCH_PROBE_QUALITY_COVERAGE = PASS
HIGH_NOISE_PRIMARY_WITHOUT_GOVERNED_ROUTE = 0
USE_CONTEXT_SYNONYM_PLAN = PASS
INFO_GAIN_RATIONALE = PASS
PRIMARY_ACQUISITION_MANIFEST = MATERIALIZED
ALL HARD GATES = PASS
REMOTE_READBACK = PASS
```

Only then may Step03 primary acquisition begin.
