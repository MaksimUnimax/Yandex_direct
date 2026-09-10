# KW-001 — STEP 5A VOLUME / SANITATION ADDENDUM

Updated: 2026-09-10  
Status: **OWNER-APPROVED / ACTIVE / PERMANENT ADDENDUM**  
Applies with: `STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md`.

This addendum changes only the volume/sanitation path. All existing Step5A claim boundaries, competitor-discovery rules, provenance requirements and project-test validation remain in force.

## 1. Corrected input boundary

Step5A must start from the already normalized/sanitized semantic directions produced after Step3/Step5.

```text
FULL RAW OCCURRENCE UNIVERSE
!= DEFAULT COMPETITOR-DISCOVERY QUERY SET
```

Use representative in-scope candidate families and unresolved coverage boundaries for competitor discovery.

## 2. Competitor seed boundary

A competitor-derived topic remains an acquisition probe, not an accepted keyword.

```text
COMPETITOR PAGE TOPIC
-> candidate seed
-> Wordstat RAW
-> normalization
-> sanitation
-> only then semantic candidate decision
```

Do not create one competitor-derived probe for every heading, product row or lexical variant. Each probe requires an explicit missed-demand/information-gain hypothesis.

## 3. Mandatory post-Wordstat transformation

Every Step5A Wordstat response must be persisted losslessly under Step3/5 acquisition rules and then immediately processed through the current universal gate:

`DATA_VOLUME_NORMALIZATION_AND_SANITATION_GATE.md`

Required path:

```text
COMPETITOR_WORDSTAT_RAW_OCCURRENCES
-> Step3A exact/safe implicit deduplication
-> Step3B high-confidence sanitation
-> compare against existing normalized/sanitized pool
-> NEW_SANITIZED_CANDIDATE / ALREADY_COVERED / REJECT / HOLD
```

Raw competitor-derived occurrences must never be appended directly to Step7 or the Search-stage set.

## 4. Duplicate control across acquisition lineages

If a phrase already exists in the normalized analytical pool and Step5A returns it again, preserve the new competitor/Wordstat occurrence lineage but do not create a duplicate analytical phrase.

```text
NEW PROVENANCE != NEW KEYWORD ID
```

## 5. Business/scope sanitation

Step5A competitor presence does not override the frozen client offer.

Clear foreign products/entities/geographies and other high-confidence off-scope meanings may be auto-excluded with reason. Material ambiguity remains HOLD/REVIEW.

```text
COMPETITOR PRESENCE != CLIENT BUSINESS FIT
```

## 6. Search confirmation volume

Current Yandex Search rechecks in Step5A remain bounded to material new candidate queries/families where the result can affect acceptance, intent, competitor-visibility or page-type interpretation.

Do not bulk-run Search for every raw Wordstat row.

## 7. Stop condition

Stop competitor expansion when additional pages/seeds mostly:

```text
repeat normalized directions
produce already-covered demand
produce off-scope/noise
or add low material decision value
```

The stopping decision is based on diminishing information gain, not a required number of competitor pages, seeds or raw rows.

## 8. Required QA additions

Every future Step5A execution must report:

```text
competitor_derived_seed_count
step5a_raw_occurrence_count
step5a_normalized_unique_count
already_existing_normalized_count
new_normalized_count
auto_excluded_count
hold_count
new_sanitized_candidate_count
search_recheck_count
ADD / ALREADY_COVERED / REJECT / HOLD counts
```

PASS requires exact reconciliation between raw Step5A evidence, normalized identities and the common downstream semantic pool.

## 9. Work/LLM input boundary

Do not send a full multi-megabyte Step5A raw ledger to Work by default. Work receives new normalized/sanitized candidates, family summaries and provenance locators; raw slices are opened only for disputed cases.

## 10. Existing method boundaries preserved

Still mandatory:

```text
COMPETITOR PAGE TOPIC != EXACT QUERY RANKING
COMPETITOR RANKING != AUTOMATIC KEYWORD ACCEPTANCE
COMPETITOR-DERIVED SEED != FINAL KEYWORD
COMPETITOR EXPANSION != DEEP COMPETITOR SEO AUDIT
TESTED QUERY VISIBILITY != FULL COMPETITOR KEYWORD UNIVERSE
```

This addendum prevents Step5A from becoming a second uncontrolled raw-data explosion while preserving its approved semantic-coverage purpose.