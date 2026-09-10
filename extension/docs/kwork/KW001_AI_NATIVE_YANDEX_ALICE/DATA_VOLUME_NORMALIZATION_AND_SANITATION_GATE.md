# KW-001 — DATA VOLUME, NORMALIZATION AND SANITATION GATE

Status: **OWNER-APPROVED / ACTIVE / PERMANENT UNIVERSAL AUTHORITY**  
Decision date: 2026-09-10  
Applies to: every KW-001 job, especially large catalog/e-commerce cases.

## 1. Why this gate exists

KW-001 must distinguish complete provider evidence from the compact analytical set used by Work/LLM/Search/Alice.

```text
RAW_OCCURRENCE_POOL
!= NORMALIZED_UNIQUE_POOL
!= SANITIZED_CANDIDATE_POOL
!= STEP7_CLEANED_ACTIVE_SET
!= SEARCH_STAGE_SET
```

A provider may legitimately return tens or hundreds of thousands of raw occurrences. That does not authorize treating every occurrence as an equally expensive semantic-analysis unit.

This gate is a scalability correction. It does **not** impose the KW-002 commercial ceiling of 1500 phrases on KW-001.

## 2. Step 2 — acquisition probe design for large catalogs

Canonical rule:

```text
SKU != AUTOMATIC WORDSTAT SEED
PAGE != AUTOMATIC WORDSTAT SEED
SEED = BOUNDED INFORMATION-GAIN PROBE
```

For a large catalog, first model search-relevant entities:

```text
category
subcategory
product type
use case
attribute/material/form factor
brand family
model/SKU only when it has a distinct search identity or decision value
```

A SKU/model deserves its own probe only when at least one is true:

```text
observable/expected standalone search identity
material commercial importance
material ambiguity/boundary to resolve
current page role that cannot be represented by the broader family
brand/model naming is itself how users search
```

Do not multiply provider calls merely because the catalog contains many rows.

## 3. Step 3 — preserve RAW losslessly, then compact analytically

Step 3 still preserves every authorized provider occurrence with full provenance under `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md`.

After Step 3 acquisition is complete, two mandatory sub-gates run before Step 4:

```text
STEP 3A — NORMALIZATION / DEDUPLICATION
STEP 3B — HIGH-CONFIDENCE SANITATION
```

### Step 3A — normalization / deduplication

Create one analytical phrase identity while preserving all raw occurrence lineage.

Mandatory operations:

```text
preserve complete RAW occurrences
normalize whitespace/case/technical punctuation conservatively
collapse exact duplicates analytically
retain every duplicate's seed/run/request/provider lineage
detect safe implicit duplicate groups
use word-order/inflection equivalence only when meaning is demonstrably preserved
never delete the underlying RAW evidence
```

Canonical example:

```text
same phrase returned by 12 runs
= 12 RAW occurrences
= potentially 1 normalized analytical phrase + 12 provenance links
```

### Step 3B — high-confidence sanitation

Apply only conservative rules that can remove obvious noise without destroying ambiguous useful demand.

Allowed early classes include:

```text
frozen business exclusions
unsupported geography when explicit
explicit foreign brands/entities/models with proven foreign referent
explicit media/game/book/person/place/organization contexts
technical/lexical/morphological garbage
empty/malformed rows
safe implicit duplicates already resolved by Step3A
high-confidence stop-topic patterns derived from evidence
```

Asymmetric rule:

```text
CLEAR OFF-TOPIC -> AUTO_EXCLUDED + reason + lineage
CLEAR DUPLICATE -> COLLAPSED_TO canonical phrase
AMBIGUOUS / MULTI-MEANING -> HOLD / REVIEW
DIRECT BUSINESS-SUPPORTED -> KEEP_CANDIDATE
LOW FREQUENCY ALONE -> NEVER AUTO_EXCLUDE
HIGH FREQUENCY ALONE -> NEVER KEEP
```

## 4. Step 4 — family triage input boundary

Step 4 must work on:

```text
SANITIZED_CANDIDATE_POOL
+ HOLD/AMBIGUOUS rows when family context is needed
+ aggregate provenance locators
```

Step 4 must **not** semantically partition every RAW occurrence independently by default.

The full RAW ledger remains machine/audit evidence.

```text
FAMILY TRIAGE != RAW OCCURRENCE PARTITION
FAMILY TRIAGE != FINAL STEP7 CLEANUP
```

If Step 4 finds an obvious recurring off-topic family that Step3B missed, record it as sanitation feedback and improve the deterministic rule before future expansion is unioned.

## 5. Step 5 and Step 5A — every expansion re-enters the same filter

Every new Wordstat acquisition from Step 5 or Step 5A must follow:

```text
NEW RAW OCCURRENCES
-> STEP3A NORMALIZATION
-> STEP3B SANITATION
-> UNION ONLY NEW SANITIZED/HOLD ANALYTICAL PHRASES
```

Never append raw expansion rows directly to the semantic working set.

Competitor-derived seeds remain probes. Competitor presence/page text does not exempt their Wordstat output from the same duplicate/noise/business-fit controls.

## 6. Step 6 / 6A acquisition extensions

If Step6/6A later acquire new query rows, those rows are governed by the same Step3A/3B transformation before entering the common semantic set.

## 7. Step 7 remains mandatory and changes purpose only by input scale

Step7 is still the deep row-level semantic cleanup authority.

It now receives the compact post-sanitation analytical universe rather than the complete RAW occurrence universe.

Step7 performs the expensive judgments that early sanitation must not fake:

```text
positive business relevance
KEEP / REJECT / REVIEW
intent / user task where applicable
ambiguous referent resolution
commercial/informational fit
semantic edge cases
adversarial semantic QA
```

Canonical distinction:

```text
STEP3B EARLY SANITATION
= cheap / conservative / mass / deterministic where possible

STEP7 FINAL SEMANTIC CLEANUP
= nuanced / semantic / business-aware / uncertainty-preserving
```

## 8. Work / LLM context rule

Large RAW occurrence ledgers are machine evidence, not default Work input.

```text
WORK SHOULD RECEIVE:
normalized/sanitized candidate rows
family summaries
reason codes
provenance locators
count reconciliation
only targeted RAW slices needed for disputed cases
```

Do not paste/serialize full multi-megabyte RAW ledgers into a Work conversation merely because they exist.

For very large sanitized sets, deterministic processing may run in stable chunks keyed by IDs, with lossless merge reconciliation. Sampling must never be presented as full processing.

## 9. Search and Alice downstream volume rule

Step8/9 Search-stage work operates on the cleaned/frozen semantic set required for actual decisions, not on RAW occurrences.

Step15/16 Alice remains a bounded diagnostic/control design; the full semantic core is not bulk-run through Alice by default.

```text
RAW_OCCURRENCE_COUNT != SEARCH_REQUEST_COUNT
RAW_OCCURRENCE_COUNT != ALICE_REQUEST_COUNT
ACTIVE_PHRASE_COUNT != ALICE_REQUEST_COUNT
```

## 10. Mandatory data funnel QA

Every materially large acquisition job must publish a funnel equivalent to:

```text
raw_occurrence_rows
normalized_unique_rows
exact_duplicate_occurrences_collapsed
implicit_duplicate_groups
collapsed_implicit_rows
auto_excluded_rows by reason
hold_ambiguous_rows
sanitized_candidate_rows
step7_keep_rows
step7_reject_rows
step7_review_rows
search_stage_rows
```

PASS requires:

```text
RAW accounting = lossless
normalized rows = 100% traceable to RAW
no silent drops
every excluded/collapsed row has reason + target/state
every HOLD remains visible
working analytical set is not inflated by provider duplicates
```

## 11. Frequency boundary

Frequency is a signal, not a universal relevance rule.

It may help:

```text
choose a canonical variant inside a proven duplicate group
prioritize review
identify potential low-value tails under a job-specific strategy
```

It may not by itself prove:

```text
business relevance
irrelevance
page ownership
intent
need for a new page
```

## 12. Large-site stopping discipline

Acquisition must stop on information gain/coverage logic, not because every catalog row has been individually probed.

For large e-commerce sites, category/subcategory/product-type/use/attribute families normally carry the initial discovery burden. SKU/model probes are selective.

The method must report why additional probes are still expected to add new search-language coverage.

## 13. Commercial scope boundary

This gate does **not** set a fixed KW-001 final phrase cap.

```text
KW002 STANDARD DELIVERY CEILING = separate product rule
KW001 FINAL ACTIVE CORE = evidence/scope dependent
```

A current KW-001 job may legitimately retain more than 1500 active phrases if they are relevant and auditable.

Any future commercial package cap for KW-001 must be set through its own productization/economics process, not copied from KW-002.

## 14. Existing accepted jobs

This gate is mandatory for future KW-001 acquisition and for any job that reopens Steps2–7 materially.

Previously accepted outputs are not invalidated solely because they were produced before this gate. A historical job only requires backfill when the owner reopens upstream acquisition/cleanup or when a scalability/quality defect is independently demonstrated.

## 15. Method sources

Official Yandex Webmaster:
https://yandex.ru/support/webmaster/ru/service/queries-selection

Topvisor — progressive cleanup:
https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/

Topvisor — tens of thousands of queries:
https://journal.topvisor.com/ru/seo-kitchen/how-to-clean-queries/

Key Collector — implicit duplicates:
https://www.key-collector.ru/docs/tools/implicit-duplicates/

Ahrefs — ecommerce keyword research:
https://ahrefs.com/blog/ecommerce-seo/

Ahrefs — large product-page keyword research:
https://ahrefs.com/blog/ecommerce-product-page-seo/

These sources support progressive filtering, duplicate normalization, category/subcategory-oriented e-commerce research and bulk processing. Project/provider evidence still decides each concrete job.