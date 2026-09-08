# STEP 05A.8 INFORMATION GAIN + FIRST-EXECUTION VALIDATION ASSESSMENT — WORK HANDOFF — 2026-09-08

## 0. Task type

This is an **EXECUTION task** for ChatGPT Work.

Do not stop after review, planning, or a prose-only opinion.
Execute the complete Step 5A.8 measurement and validation-assessment scope below, materialize durable evidence artifacts, run deterministic QA, commit completed checkpoints, and perform remote GitHub readback before reporting completion.

Repository:

`MaksimUnimax/Yandex_direct`

Branch:

`roadmap/kwork-productization-2026-08-28`

Level-1 methodology workspace:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE`

Current Level-2 job workspace:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK`

Step 5A execution workspace:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_05A_FIRST_EXECUTION_2026-09-08`

Expected current remote HEAD before this handoff materialization:

`d8c730607e8297a5183a0f9302a31dd4a5c1af7a`

The launch prompt from Main ChatGPT will provide the actual handoff commit. Verify live branch/HEAD before substantive work.

---

# 1. Current verified state

Main ChatGPT independently read back the Step 5A.6–5A.7 remote artifacts and accepted them as materially consistent.

Verified current facts include:

```text
SEARCH_REQUIREMENTS = 9 / 9
SEARCH_SUCCEEDED = 7
SEARCH_OUTCOME_UNKNOWN = 2
SEARCH_SERP_ROWS = 70
VISIBILITY_MATRIX_ROWS = 81
SELECTED_COMPETITOR_VISIBILITY_CELLS = 11
SELECTED_COMPETITOR_RANKING_ROWS = 12
FINAL_ADD_TO_PIPELINE = 7
FINAL_HOLD_EVIDENCE = 2
POTENTIALLY_NEW_WORDSTAT_OCCURRENCES_RECONCILED = 20
MERGE_ACCEPTED = 16
SUPPRESSED_AS_CLOSE_VARIANT_DUPLICATE = 3
RETAIN_HOLD = 1
SEMANTIC_PIPELINE_DELTA_ROWS = 16
UNKNOWN_RETRIES = 0
DETERMINISTIC_QA = PASS 65/65
PROJECT_TEST_VALIDATED = false
LEVEL1_METHOD_PROMOTED = false
PROPAGATION_STATE = PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE
```

The two Search holds are:

- `OLD_HOUSING_WINDOWS` / `окна для старого фонда`
- `BALCONY_AS_STORAGE` / `кладовая на балконе`

No further Yandex provider calls are authorized in this Work task.

---

# 2. Mandatory authorities to read

Read live remote versions, not stale local assumptions.

At minimum read:

## 2.1 Level-1 method authority

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md`

Mandatory sections:

- purpose / client-facing meaning;
- claim boundary;
- Step 5A.8 diminishing-information-gain rule;
- required outputs;
- failure classes;
- Section 11 first-execution validation gate.

## 2.2 Step 5A.1–5A.7 execution authorities

At minimum:

- `STEP_05A_FIRST_EXECUTION_REPORT.md`
- `STEP_05A_COMPETITOR_PAGE_INSPECTION_REPORT.md` or equivalent live report/checkpoints for page inspection
- `STEP_05A_DERIVED_SEED_CANDIDATES.tsv`
- `STEP_05A_SEED_DECISIONS.json`
- `STEP_05A_WORDSTAT_SEED_ACQUISITION_LEDGER.tsv`
- `STEP_05A_WORDSTAT_RETURNED_PHRASE_LEDGER.tsv`
- `STEP_05A_WORDSTAT_SEMANTIC_RECONCILIATION.tsv`
- `STEP_05A_SEARCH_RECHECK_REQUIREMENT_PACKAGE.tsv`
- `STEP_05A_WORDSTAT_RECONCILIATION_REPORT.md`
- `STEP_05A_SEARCH_REQUIREMENT_ACQUISITION_LEDGER.tsv`
- `STEP_05A_SEARCH_SERP_LEDGER.tsv`
- `STEP_05A_SEARCH_RESULT_INTENT_CLASSIFICATION.tsv`
- `STEP_05A_COMPETITOR_QUERY_VISIBILITY_MATRIX.tsv`
- `STEP_05A_FINAL_GAP_DECISION_REGISTER.tsv`
- `STEP_05A_ACCEPTED_PHRASE_MERGE_RECONCILIATION.tsv`
- `STEP_05A_ACCEPTED_SEMANTIC_PIPELINE_DELTA.tsv`
- `STEP_05A_SEARCH_DECISION_MERGE_REPORT.md`
- `STEP_05A_SEARCH_DECISION_MERGE_QA.json`
- `STEP_05A_INFORMATION_GAIN_INPUT.json`
- `CHECKPOINT_07_SEARCH_DECISION_MERGE_REMOTE_READBACK.md`

Resolve equivalent exact filenames from the live execution workspace if any report name differs. Do not substitute stale snapshots.

## 2.3 Current frozen project authority for denominator/context only

Read the current completed OKNO_MSK semantic authority and the already-corrected release state only to establish baseline denominators and protection checks.

Do not modify them.

Relevant frozen counts already established in the project include:

```text
UNIQUE_SEMANTIC_PHRASES = 2840
ACTIVE = 2332
ASSIGNED = 2313
SEARCH_REQUIRED = 19
CANONICAL_STRUCTURAL_UNITS = 168
```

Verify these against live authority before using them in final calculations.

---

# 3. Hard boundaries

## 3.1 No new acquisition

DO NOT perform:

- new Yandex Search;
- new Wordstat;
- Alice/GenSearch/Webmaster/Metrika/Direct calls;
- substitute web search;
- new competitor-page crawling or inspection.

Step 5A.8 measures the evidence already acquired.

## 3.2 No automatic Level-1 promotion

Do not edit the Level-1 method status to `PROJECT_TEST_VALIDATED`, `APPROVED ACTIVE`, or equivalent.

Do not set a persistent project-wide `PROJECT_TEST_VALIDATED=true` merely because deterministic QA passes.

This task must distinguish:

```text
DETERMINISTIC_TECHNICAL_GATE_RESULT
OWNER_REVIEW_REQUIRED_GATE
RECOMMENDED_PROJECT_TEST_VALIDATION_VERDICT
ACTUAL_LEVEL1_PROMOTION_STATE
```

The actual Level-1 promotion state remains unchanged unless the owner separately authorizes it after reviewing this assessment.

## 3.3 Client-usefulness gate cannot be self-certified

The Level-1 first-execution gate includes:

`client-facing competitor-gap result is understandable and materially useful`

Work may produce a client-facing **preview/prototype** in the Step 5A execution workspace and may run deterministic language/completeness QA on it.

Work must NOT mark the owner usefulness/understandability gate as final PASS on its own.

Use a state such as:

`OWNER_REVIEW_REQUIRED`

unless an already-preserved explicit owner acceptance exists in the repository. Do not infer owner acceptance from deterministic QA.

## 3.4 Accepted delta is not frozen truth yet

The 16 accepted delta rows are acquisition-pipeline additions only.

Do not:

- rewrite frozen Stage-5 master;
- rewrite canonical structural-unit authority;
- assign final page ownership;
- create/delete/merge/split pages;
- modify corrected client release;
- mutate Documents №01–03 or semantic-core XLSX.

Preserve:

`PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE`.

---

# 4. Required Step 5A.8 measurements

Create a reproducible information-gain funnel from the preserved evidence.

At minimum measure and reconcile:

```text
75 preserved discovery Search queries
750 preserved discovery TOP10 rows
9 selected competitor domains
44 competitor target URLs
43 directly accessible + 1 redirected-accessible + 0 inaccessible
92 candidate occurrences
43 deduplicated candidate directions
22 already covered after page-level reconciliation
14 potentially new Wordstat seeds
3 off-scope
4 hold/review
14 Wordstat executions
160 actually returned Wordstat phrase rows
20 potentially-new Wordstat occurrences entering Search reconciliation
9 deduplicated Search recheck requirements
7 successful Search-confirmed ADD_TO_PIPELINE directions
2 Search OUTCOME_UNKNOWN -> HOLD_EVIDENCE directions
16 accepted semantic-pipeline delta rows
3 close-variant suppressions
1 retained occurrence hold
```

## 4.1 Required conversion/yield rates

Calculate exact rates with numerator/denominator explicitly named. At minimum:

- candidate-occurrence -> deduplicated-direction consolidation rate;
- deduplicated-direction -> Wordstat-seed rate;
- Wordstat returned rows -> potentially-new Search-recheck occurrence rate;
- Wordstat seeds -> Search-recheck direction rate;
- Search-recheck requirements -> ADD_TO_PIPELINE direction rate;
- successful Search requirements -> ADD_TO_PIPELINE rate;
- 20 potentially-new occurrences -> 16 accepted delta row rate;
- accepted delta rows -> current 2,840 unique semantic phrase baseline expansion ratio;
- accepted delta rows -> current 2,332 active phrase baseline ratio;
- hold rate at Search decision layer;
- selected-competitor visibility density = observed visible cells / 81 possible direction-domain cells;
- unique selected competitor domains actually visible in successful rechecks / 9 selected domains.

Do not use percentages without also preserving raw counts.

## 4.2 Provider-cost efficiency

Use only already-preserved provider-cost evidence.

Known bounded Step 5A acquisition costs to verify:

- Wordstat: `0.28 RUB`
- Step 5A.6 Search: `4.392 RUB`

Compute total incremental provider cost and descriptive efficiency metrics such as:

- RUB per final ADD_TO_PIPELINE direction;
- RUB per accepted delta row;
- RUB per successfully resolved Search requirement.

These are descriptive COGS measures, not quality targets and not reasons to reject useful evidence.

## 4.3 Novelty and filtering value

Measure not only additions but also filtering/de-risking value.

At minimum preserve:

- directions already covered before new provider work;
- off-scope directions filtered before provider work;
- HOLD directions preserved rather than fabricated;
- close variants suppressed rather than inflating delta;
- website-text-as-ranking overclaims prevented;
- exact-query competitor visibility confirmed only where current Search rows exist.

## 4.4 Competitor visibility gain

Use the 9x9 matrix and successful Search rows to report:

- visible selected-competitor cells;
- ranking rows;
- unique selected competitors actually observed in the seven successful rechecks;
- selected competitors not observed in those rechecks;
- query directions with zero selected competitors visible but still ADD_TO_PIPELINE because Wordstat + Search intent + business scope + novelty supported addition;
- exact previously inspected URL matches vs same-domain/different-URL visibility.

Do not reinterpret `competitor page supplied topic` as `competitor ranked for new query`.

## 4.5 Information-gain stop assessment

Assess Step 5A.8's diminishing-information-gain rule from preserved evidence only.

Do not invent a universal numeric threshold.

Required questions:

1. Did the bounded competitor pass produce material new semantic information? Quantify.
2. Did it mostly repeat existing semantics, mostly add noise, or still produce substantial new in-scope directions?
3. Does this single execution empirically prove a reusable saturation threshold? Expected answer may be `NO` if the evidence does not support one.
4. Is there enough evidence to stop this *bounded rehearsal* without recursively expanding competitors/seeds further? Explain from scope control, existing additions, remaining holds and absence of authorization for recursive acquisition.
5. What observation in a future varied rehearsal would justify extending or stopping earlier?

Distinguish:

`STOP_THIS_REHEARSAL`
from
`PERMANENT_DIMINISHING_GAIN_THRESHOLD_VALIDATED`.

They are not the same.

---

# 5. First-execution validation gate register

Materialize one row per Level-1 Section 11 gate.

At minimum evaluate these ten gates exactly:

1. `REAL_SEARCH_COMPETITOR_DISCOVERY_WORKS_IN_TARGET_REGION`
2. `COMPETITOR_PAGE_TO_SEED_LINEAGE_IS_DURABLE`
3. `WORDSTAT_EXPANSION_ADDS_MEASURABLE_COVERAGE_OR_PROVES_NO_MATERIAL_GAP`
4. `RETURNED_WORDSTAT_ROWS_FULLY_PRESERVED_UNDER_STEP3_STEP5_SCHEMA`
5. `MATERIAL_NEW_CANDIDATES_RECEIVE_CORRECT_SEARCH_CONFIRMATION_OR_HOLD_ROUTING`
6. `WEBSITE_TEXT_AS_RANKING_OVERCLAIM_EQUALS_0`
7. `FULL_COMPETITOR_KEYWORD_UNIVERSE_OVERCLAIM_EQUALS_0`
8. `MERGE_COUNTS_RECONCILE`
9. `EXTERNAL_REVERSE_DOMAIN_PROVIDER_REQUIRED_FOR_BASE_EXECUTION_EQUALS_FALSE`
10. `CLIENT_FACING_COMPETITOR_GAP_RESULT_IS_UNDERSTANDABLE_AND_MATERIALLY_USEFUL`

Each gate row must contain:

- gate ID;
- gate statement;
- evidence files;
- exact supporting counts/facts;
- deterministic status (`PASS`, `FAIL`, `PARTIAL`, `NOT_APPLICABLE`, or `OWNER_REVIEW_REQUIRED`);
- unresolved evidence;
- whether Work is authorized to close the gate;
- recommended owner action if needed.

Do not collapse gate 10 into deterministic PASS.

---

# 6. Validation verdict model

Produce separate verdict fields. Do not conflate them.

Required fields:

```text
FIRST_EXECUTION_TECHNICAL_VALIDATION
FIRST_EXECUTION_INFORMATION_GAIN_VERDICT
CLIENT_FACING_USEFULNESS_GATE
RECOMMENDED_PROJECT_TEST_VALIDATION
ACTUAL_PROJECT_TEST_VALIDATED_STATE
LEVEL1_METHOD_PROMOTION_STATE
PERMANENT_DIMINISHING_GAIN_THRESHOLD_STATE
```

Allowed recommended project-test verdicts:

```text
RECOMMEND_VALIDATE_AFTER_OWNER_REVIEW
RECOMMEND_REMAIN_PENDING
RECOMMEND_FAIL_AND_REWORK
```

Unless explicit preserved owner acceptance already exists, actual state must remain:

```text
ACTUAL_PROJECT_TEST_VALIDATED_STATE = false / PENDING_OWNER_REVIEW
LEVEL1_METHOD_PROMOTION_STATE = NOT_PROMOTED
```

A technically strong run may justify `RECOMMEND_VALIDATE_AFTER_OWNER_REVIEW`; that still does not itself promote Level-1.

---

# 7. Client-facing preview for owner review

Create a concise plain-Russian preview in the Step 5A execution workspace only.

Suggested filename:

`STEP_05A_CLIENT_FACING_COMPETITOR_GAP_PREVIEW_RU.md`

It must be understandable to a client who knows Yandex, Wordstat, competitors, Search, Alice/AI, but does not know internal project enum names.

Explain in plain Russian:

- зачем проверяли конкурентов;
- сколько реальных поисковых конкурентов/страниц исследовали;
- сколько дополнительных тем нашли;
- как Wordstat отфильтровал/раскрыл их;
- какие новые направления подтвердились в текущей выдаче Яндекса;
- какие два направления остались неопределёнными и почему;
- сколько новых поисковых фраз подготовлено к включению в общее ядро;
- что это пока не означает создание новых страниц;
- что должно произойти перед следующим реальным релизом.

Do not leak internal IDs, filenames, QA enums or developer jargon into the client-facing prose.

This preview is for owner review only and must not be inserted into the corrected client release in this task.

---

# 8. Required artifacts

Create at minimum in:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_05A_FIRST_EXECUTION_2026-09-08/`

1. `STEP_05A_INFORMATION_GAIN_METRICS.json`
2. `STEP_05A_INFORMATION_GAIN_FUNNEL.tsv`
3. `STEP_05A_FIRST_EXECUTION_VALIDATION_GATE_REGISTER.tsv`
4. `STEP_05A_FIRST_EXECUTION_VALIDATION_REPORT.md`
5. `STEP_05A_FIRST_EXECUTION_VALIDATION_QA.json`
6. `STEP_05A_CLIENT_FACING_COMPETITOR_GAP_PREVIEW_RU.md`
7. checkpoint/execution log sufficient to prove Work lifecycle and remote readback.

You may add deterministic builder/validator scripts.

Do not overwrite raw provider evidence.

---

# 9. Required QA

QA must fail if any of the following occurs:

- any funnel count does not reconcile to preserved evidence;
- any rate lacks its raw numerator/denominator;
- Wordstat or Search cost is invented or altered;
- accepted delta count differs from 16 without explicit source correction;
- 2 unknown Search directions are converted to success/failure/empty SERP;
- a competitor ranking claim lacks current Search evidence;
- a page/topic observation is used as exact-query ranking proof;
- final page ownership or implementation action is created;
- frozen Stage-5/client release is modified;
- Level-1 method is automatically promoted;
- `PROJECT_TEST_VALIDATED=true` is persisted without explicit owner authorization;
- gate 10 is self-certified by Work without preserved owner acceptance;
- permanent diminishing-gain threshold is claimed from a single execution without evidence;
- new provider or substitute web calls are made.

Also require exact QA assertions for:

```text
GATE_ROWS = 10
SEARCH_REQUIREMENTS = 9
SEARCH_SUCCEEDED = 7
SEARCH_UNKNOWN = 2
SERP_ROWS = 70
WORDSTAT_ROWS = 160
POTENTIALLY_NEW_OCCURRENCES = 20
ADD_DIRECTIONS = 7
HOLD_DIRECTIONS = 2
ACCEPTED_DELTA_ROWS = 16
UNKNOWN_RETRIES = 0
LEVEL1_PROMOTED = false
PROJECT_TEST_VALIDATED_PERSISTED_TRUE = false
```

---

# 10. Git lifecycle

Use:

`WORK -> SAVE -> COMMIT -> REMOTE GITHUB READBACK -> CONTINUE`

At completion:

1. working tree clean;
2. required artifacts exist remotely;
3. remote-read back all final validation artifacts;
4. verify protected frozen/client paths unchanged;
5. persist final readback receipt;
6. report final remote HEAD.

---

# 11. Completion condition

This Work task is complete only when:

- information gain is quantitatively measured from preserved Step 5A.1–5A.7 evidence;
- the diminishing-gain stopping question is explicitly assessed without inventing a permanent threshold;
- all ten first-execution validation gates have evidence-backed statuses;
- deterministic/owner-only gates are separated;
- a project-validation recommendation is produced without changing Level-1 promotion state;
- a plain-Russian client-facing preview exists for owner review but is not inserted into the corrected release;
- QA passes;
- remote GitHub readback passes.

Expected next action after completion is one of:

```text
OWNER_REVIEW_STEP_5A_FIRST_EXECUTION_VALIDATION_AND_CLIENT_FACING_PREVIEW
```

and, independently for the actual semantic dataset before any next real release:

```text
PROPAGATE_STEP_5A_ACCEPTED_SEMANTIC_PIPELINE_DELTA_THROUGH_NORMAL_DOWNSTREAM_PIPELINE
```

Do not execute either owner approval or downstream release propagation inside this Work task.
