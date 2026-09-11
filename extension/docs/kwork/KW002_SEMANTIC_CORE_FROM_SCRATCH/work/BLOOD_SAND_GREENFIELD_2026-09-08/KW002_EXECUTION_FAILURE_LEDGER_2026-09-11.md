# KW-002 Blood & Sand — execution failure ledger

Date: 2026-09-11
Status: **ACTIVE JOB-SPECIFIC LESSONS / MUST BE READ BEFORE CONTINUATION**

Universal authority:

`LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`

This file records concrete failures observed in this rehearsal so they remain part of the permanent provenance chain. It is not a blame log; it exists to stop the same failure class from recurring.

## Current accepted cursor

```text
STEP00 = PASS after source-boundary correction
STEP01 = PASS / 76 of 76 Ozon rows
STEP02 = V2 PASS / V1 SUPERSEDED
STEP03 = PASS / 79 of 79 durable feed-forward
STEP03A = PASS / BYTE UNCHANGED
STEP03B_ORIGINAL = SUPERSEDED
STEP03B_CORRECTED = ACCEPTED / REMOTE READBACK PASS
HISTORICAL_STEP04 = PRESENT
POST_SANITATION_STEP04 = REQUIRED / NOT YET EXECUTED
STEP05 = BLOCKED / NOT STARTED
```

## Failure 1 — Step00 source boundary was initially too broad

Observed:

```text
EARLY_IN_SCOPE = WB + Ozon
EARLY_IN_SCOPE_ROWS = 164
CORRECTED_AUTHORITY = Ozon only
CORRECTED_ROWS = 76
```

Consequence:

Dependent Step01 planning based on mixed-source/cross-platform reconciliation became invalid and had to be rebuilt.

Permanent lesson:

- sales-channel fact is not automatically an authorized assortment evidence source;
- source mutation must invalidate dependent work;
- never preserve superseded inputs just because processing already happened.

Regression gate:

```text
ACTIVE_ASSORTMENT_SOURCE = Ozon only
WB_ROWS_USED_AS_ACTIVE_STEP01_02_ASSORTMENT = 0
```

## Failure 2 — Step02 V1 passed accounting better than search usefulness

Observed V1 quality:

```text
QUALITY_SCORE = 65/100
STATUS = REWORK_REQUIRED
```

Concrete defects:

- bare ambiguous names were treated as sufficient quality routes;
- HIGH-noise names lacked mandatory refinement strategy;
- automobile synonym/use-context coverage was not systematic;
- exact seller names were too automatically promoted to PRIMARY;
- information-gain rationales were repetitive and weakly discriminative;
- provider-cost economy influenced deferral too strongly;
- Step03 was opened before dedicated search-probe-quality QA.

Correction:

Step02 V2 separated catalog-lineage coverage from search-quality coverage, introduced refinement/control logic, and reached 93/100.

Permanent lesson:

```text
76/76 CATALOG COVERAGE != GOOD WORDSTAT PROBE SET
```

## Failure 3 — Step03 provider/acquisition completion was not sufficient persistence proof

Observed late defect:

```text
PROVIDER/CURRENT OUTCOMES = 79/79
LOSSLESS_GITHUB_FEED_FORWARD_AT_LATE_QA = 60/79
AFFECTED_RUN_ORDERS = 32-48,50,51
```

Recovery eventually restored:

```text
DURABLE_FEED_FORWARD = 79/79
REMOTE_READBACK = PASS
```

Permanent lesson:

A provider result does not exist for downstream analysis until complete required payload, provenance and durable readback are proven.

`OUTCOME_UNKNOWN` must not be blindly replayed or overwritten under the old identity.

Regression gate:

```text
PROVIDER_TERMINAL = 79/79
DURABLE_LOSSLESS = 79/79
REMOTE_READBACK = PASS
```

## Failure 4 — original Step04 lacked occurrence-level reproducibility

Accepted external audit found:

```text
AUDIT_VERDICT = REWORK_REQUIRED
QUALITY_SCORE = 87/100
GLOBAL_DEFECT = D14 QA_OR_REPRODUCIBILITY_DEFECT
```

Aggregate family totals reconciled, but the result lacked a durable deterministic ledger proving which exact occurrence belonged to which family.

Correction required and later produced:

`STEP_04_OCCURRENCE_FAMILY_LEDGER_CORRECTED_2026-09-10.tsv`

Permanent lesson:

Family summary rows are not sufficient authority. Every full-volume family pass requires occurrence identity -> family mapping and zero unassigned/duplicate occurrence identities.

## Failure 5 — Step04 examples demonstrated rule defects; examples themselves were not the correction target

Affected historical examples included F011/F015/F017/F022/F025/F032 and queue duplications E004/E017 and E007/E014.

The accepted correction contract explicitly required:

```text
FIX UNDERLYING DETERMINISTIC RULE
RERUN COMPLETE FROZEN CORPUS
DO NOT PATCH ONLY DEMONSTRATED EXAMPLES
```

Permanent lesson:

A representative defect is a regression test and evidence of a rule failure. Any sibling rows affected by the same rule must be reprocessed.

## Failure 6 — original Step03B broad regex/stem logic caused semantic false exclusions

Independent full-volume audit result:

```text
STEP03B_FULL_VOLUME_AUDIT = FAIL
FINAL_VERDICT = CRITICAL_REWORK_REQUIRED
QUALITY_SCORE = 75/100
```

Unsafe exclusions:

```text
CURRENT_AUTO_EXCLUDED = 6752
UNSAFE_EXCLUSIONS = 758
EXCLUDE -> KEEP = 14
EXCLUDE -> HOLD = 744
```

Observed collision classes:

- zodiac/astrology product-vs-information collisions;
- `футбол*` versus `футболка`;
- `банк*` collisions;
- `четк*` versus possible `чётки` morphology/typo;
- `купить ... дом` versus `оберег дома купить`;
- generic media verbs without explicit media referent;
- vehicle/model rules firing before supported car-use/catalog collisions;
- generic game/model tokens treated as conclusive.

Permanent lesson:

```text
SUBSTRING MATCH != REFERENT PROOF
TOKEN MATCH != INTENT PROOF
AMBIGUITY -> HOLD
```

## Failure 7 — original Step03B positive business fallback caused semantic false KEEP

Unsafe KEEP audit:

```text
CURRENT_KEEP = 5074
UNSAFE_KEEP = 286
KEEP -> EXCLUDE = 79
KEEP -> HOLD = 207
```

Cause:

Recognized business/product vocabulary could override incomplete foreign-context guards.

Permanent lesson:

```text
POSITIVE BUSINESS TOKEN DOES NOT OVERRIDE EXPLICIT FOREIGN CONTEXT
```

Before KEEP, independently test named games, media works, vehicle parts/models, foreign entities, places/persons/organizations and unsupported products.

## Failure 8 — original Step03B HOLD contained deterministically resolvable rows

Audit found:

```text
HOLD -> KEEP = 298
HOLD -> EXCLUDE = 368
TOTAL_RESOLVABLE_HOLD = 666
```

Permanent lesson:

Conservative HOLD is correct when evidence is insufficient, but clear frozen catalog/business evidence or explicit foreign context should resolve rows deterministically rather than accumulate avoidable HOLD debt.

## Failure 9 — mechanical QA/self-score masked Step03B semantic defects

Original Step03B had complete accounting and high self-scoring, but later independent semantic audit changed state for 1,710 normalized identities.

Corrected transition total:

```text
CHANGED_IDENTITIES = 1710
CHANGED_RAW_OCCURRENCES = 1761
```

Permanent lesson:

```text
ACCOUNTING_QA != SEMANTIC_QA
SELF_SCORE != INDEPENDENT ACCEPTANCE
```

A full-volume semantic pre-filter must receive adversarial collision-class QA before Main ChatGPT acceptance.

## Failure 10 — downstream Step04 became stale after upstream Step03B correction

Corrected Step03B final accepted partition:

```text
KEEP = 5100
HOLD = 13035
EXCLUDE = 6441
TOTAL = 24576
OVERLAY_STATE_MISMATCHES = 0
RAW_LINEAGE_LOSS = 0
QUALITY_SCORE = 98.23/100
```

Mechanical reconciliation with historical corrected Step04:

```text
STEP04_OCCURRENCES = 25979
KEEP_OCCURRENCES = 5263
HOLD_OCCURRENCES = 13823
EXCLUDE_OCCURRENCES = 6893
STEP04_FAMILIES = 25
FAMILIES_WITH_STATE_TRANSITIONS = 23
```

Consequence:

Historical Step04 family and expansion-queue conclusions cannot be treated as current semantic authority without a dedicated post-sanitation semantic pass.

Permanent lesson:

```text
UPSTREAM PASS CHANGE CAN REVOKE DOWNSTREAM PASS
```

Step05 remains blocked until post-sanitation Step04 is independently accepted.

## Required regression matrix for the next Step04 pass

The next post-sanitation Step04 execution must explicitly test:

| failure | required regression |
|---|---|
| F03B broad regex collisions | no family decision may treat old pre-correction sanitation state as current truth |
| F03B ambiguity destruction | HOLD remains explicit unless family context provides a high-confidence family decision; Step04 must not perform final row intent cleanup |
| F04 missing occurrence ledger | complete deterministic mapping over all 25,979 occurrences |
| F04 example-only patching | full affected universe rerun; examples are tests only |
| upstream invalidation | use corrected Step03B authorities, not original Step03B or historical family totals as input truth |
| frequency bias | no family exclusion/priority solely from low/high frequency |
| sealed-source contamination | zero sealed historical Blood & Sand research used |
| provider contamination | zero new Wordstat/Search/GenSearch/AI calls |
| scope creep | no final row cleanup, SERP clustering, query->page mapping or IA |

## Current next action

```text
NEXT_STEP = POST_SANITATION STEP04 FULL-VOLUME SEMANTIC REWRITE
INPUT_AUTHORITY = CORRECTED STEP03B + FROZEN CLIENT SCOPE + PRESERVED RAW LINEAGE
STEP05_ALLOWED = false
```
