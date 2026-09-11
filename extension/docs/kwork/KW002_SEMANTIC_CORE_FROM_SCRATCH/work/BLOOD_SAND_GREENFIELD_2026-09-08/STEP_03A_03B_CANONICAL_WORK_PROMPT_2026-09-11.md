# KW-002 Blood & Sand — STEP 03A/03B CANONICAL CHATGPT WORK PROMPT

```text
You are executing the mandatory Step03A + Step03B volume-pipeline backfill for the active KW-002 Blood & Sand greenfield semantic-core rehearsal.

Repository:
MaksimUnimax/Yandex_direct

Branch:
roadmap/kwork-productization-2026-08-28

Job:
extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08

THIS IS NOT A NEW RESEARCH RUN.
THIS IS NOT STEP05 ACQUISITION.
THIS IS NOT FINAL KEYWORD CLEANUP.
THIS IS NOT SERP CLUSTERING.
THIS IS NOT QUERY→PAGE OWNERSHIP OR IA DESIGN.

The task is a deterministic large-data migration of already preserved Step03 evidence:

RAW_OCCURRENCE_POOL
→ NORMALIZED_UNIQUE_POOL
→ SANITIZED_CANDIDATE_POOL / HOLD / AUTO_EXCLUDED

Use the COMPLETE dataset.
Do not sample, truncate, use first-N rows, or replace full processing with representative examples.

======================================================================
0. HARD PRECONDITION
======================================================================

Before any transformation, read the live shared branch and verify that the Step04 limited-rework corrected five-file bundle is durably present on remote and readable:

<JOB>/STEP_04_OCCURRENCE_FAMILY_LEDGER_CORRECTED_2026-09-10.tsv
<JOB>/STEP_04_FAMILY_TRIAGE_CORRECTED_2026-09-10.tsv
<JOB>/STEP_04_TARGETED_EXPANSION_QUEUE_CORRECTED_2026-09-10.tsv
<JOB>/STEP_04_LIMITED_REWORK_QA_2026-09-10.md
<JOB>/STEP_04_LIMITED_REWORK_WORK_RETURN_2026-09-10.md

If any of these five files is absent, unreadable, or publication/readback cannot be proven:

STOP.

Return:

STEP03A_03B_WORK_EXECUTION = BLOCKED
BLOCKER = STEP04_LIMITED_REWORK_REMOTE_PUBLICATION_NOT_COMPLETE

Do not execute Step03A/03B in that state.

======================================================================
1. READ AUTHORITIES IN FULL
======================================================================

LEVEL 1:
- LEVEL1/COMMON_RULES.md
- LEVEL1/INHERITED_KW001_UNIVERSAL_RULES.md
- LEVEL1/CLIENT_INTAKE_AND_SCOPE_RULE.md
- LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md
- LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md
- LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md
- LEVEL1/RESULT_QUALITY_SCORING_RULE.md
- LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md
- LEVEL1/WORK_HANDOFF_RULE.md

LEVEL 2:
- LEVEL2/STEP_RULES_INDEX.md
- LEVEL2/INHERITED_KW001_STEP_RULES.md

JOB:
- <JOB>/JOB_MANIFEST.md
- <JOB>/JOB_FLOW.md
- <JOB>/ALLOWED_INPUTS_AND_SEALED_SOURCES.md
- <JOB>/CLIENT_SUPPLIED_BRIEF.md
- <JOB>/CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md
- <JOB>/CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
- <JOB>/STEP_01_BUSINESS_AND_ASSORTMENT_MODEL.md
- <JOB>/STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv
- <JOB>/STEP_03_COLLECTION_CLOSURE_2026-09-09.md
- <JOB>/STEP_03_WORDSTAT_RAW_PERSISTENCE_STATE_2026-09-09.md
- <JOB>/STEP_03_RAW_RECOVERY_AUTHORITY_FINAL_2026-09-10.md
- <JOB>/STEP_03_RAW_RECOVERY_FINAL_RECEIPT_2026-09-10.md
- <JOB>/STEP_03_RAW_RECOVERY_INDEX_FINAL_2026-09-10.md
- <JOB>/STEP_03_RAW_RECOVERY_COMPLETION_STATE_2026-09-10.json
- complete <JOB>/STEP_03_WORDSTAT_RAW evidence tree
- <JOB>/KW002_VOLUME_PIPELINE_MIGRATION_GATE_2026-09-10.md
- <JOB>/STEP_03A_03B_PRE_STEP_REVIEW_AND_WORK_HANDOFF_2026-09-11.md

Read corrected Step04 artifacts only as downstream reconciliation authority.
Do NOT allow corrected Step04 family assignments to rewrite Step03A exact-normalization truth.

======================================================================
2. CLEAN-BASELINE / SOURCE BOUNDARY
======================================================================

Prior Blood & Sand analytical research remains SEALED unless explicitly whitelisted by the active job authority.

Do NOT use prior:
- SEO research
- Wordstat conclusions outside the accepted current Step03 evidence
- Search/SERP conclusions
- Alice/GenSearch conclusions
- competitor research
- cluster decisions
- query→page decisions
- IA / Page Jobs / SEO priorities

Knowing an old conclusion exists does not make it allowed evidence.

Required:
SEALED_SOURCE_VIOLATIONS = 0

======================================================================
3. PROVIDER BOUNDARY
======================================================================

ZERO NEW PROVIDER CALLS.

Do NOT call:
- Wordstat
- ordinary Yandex Search
- Search batch
- GenSearch
- Alice / AI search
- any other external demand provider

This migration uses already persisted evidence only.

Required:
NEW_WORDSTAT_CALLS = 0
NEW_SEARCH_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_AI_SEARCH_CALLS = 0

======================================================================
4. CANONICAL RAW INPUT
======================================================================

Accepted current Step03 feed-forward truth:

CANONICAL_PRIMARY_PROBES = 79
DURABLE_SOURCE_RESOLUTION = 79/79
RESULT_OCCURRENCES = 24722
ASSOCIATION_OCCURRENCES = 1257
TOTAL_RAW_OCCURRENCES = 25979

Reconstruct only the accepted current feed-forward corpus using final Step03 recovery authority/mapping.

Do NOT count obsolete historical payload versions as additional current occurrences.
Do NOT lose empty terminal runs; they remain source-status evidence but generate zero occurrence rows.

Occurrence identity:

occurrence_id = R{run_order:03d}|{channel}|{position:04d}

channel must be exactly:
results
associations

======================================================================
5. STEP03A — NORMALIZATION + DEDUPLICATION
======================================================================

Purpose:
Convert 25,979 lossless RAW occurrences into stable analytical phrase identities without destroying provenance.

Never edit or overwrite RAW evidence.

For matching/comparison only, use conservative normalization:

1. Unicode canonical normalization using NFC.
2. Trim leading/trailing whitespace.
3. Collapse repeated internal whitespace to one space.
4. Create a case-normalized comparison representation.
5. Preserve meaningful digits, lexical hyphens and other characters unless a rule proves they are only technical noise.
6. Preserve all original observed phrase variants in lineage.
7. Do NOT use aggressive compatibility normalization if it can erase meaningful distinctions.
8. Do NOT treat punctuation removal as semantic equivalence by default.

---------------------------------------------------------------------
5A. EXACT DUPLICATES
---------------------------------------------------------------------

Exact duplicates may be analytically collapsed only when they produce the same safe normalized comparison identity.

Repeated identical phrases from different:
- seeds
- runs
- request IDs
- channels

remain distinct RAW occurrences.

They may map to one normalized phrase identity, but every occurrence must remain in lineage.

Do NOT sum repeated provider counts across seeds as though duplicate observations were independent demand.
Preserve observed count values and provenance.

---------------------------------------------------------------------
5B. IMPLICIT DUPLICATES
---------------------------------------------------------------------

Detect candidate groups such as:
- word-order variants
- inflection variants
- variants differing only by potentially non-material stop words

Do NOT collapse merely because tokens/stems are similar.
Word order can change meaning.
Entity names, routes, models, product names and other structured phrases require conservative handling.

For every implicit group use one of:

NONE
CANDIDATE
ACCEPTED_EQUIVALENT
REJECTED_NOT_EQUIVALENT
HOLD_AMBIGUOUS

Collapse only ACCEPTED_EQUIVALENT.
If equivalence is uncertain -> HOLD_AMBIGUOUS.

Frequency may help choose a canonical representative among already-proven equivalent forms.
Frequency must NOT decide business relevance or duplicate truth by itself.

---------------------------------------------------------------------
5C. REQUIRED STEP03A OUTPUTS
---------------------------------------------------------------------

Create:

<JOB>/STEP_03A_NORMALIZED_UNIQUE_POOL_2026-09-11.tsv

Minimum fields:
normalized_phrase_id
canonical_phrase
exact_normalized_key
raw_phrase_variants
raw_occurrence_count
all_raw_occurrence_ids
run_orders
seed_ids
seed_phrases
provider_request_ids
carrier_locators
channels
observed_count_values
exact_duplicate_count
implicit_duplicate_group_id
implicit_duplicate_state
canonicalization_reason
lineage_state
notes

Create:

<JOB>/STEP_03A_NORMALIZATION_LEDGER_2026-09-11.tsv

Exactly one row per RAW occurrence.

Minimum fields:
occurrence_id
run_order
seed_id
seed_phrase
provider_request_id
carrier_locator
channel
position
raw_phrase
raw_count
exact_normalized_key
normalized_phrase_id
implicit_duplicate_group_id
implicit_duplicate_state
collapsed_to_normalized_phrase_id
mapping_reason
notes

Required ledger rows = 25979.

Create:

<JOB>/STEP_03A_NORMALIZATION_QA_2026-09-11.md

Prove at minimum:
RAW_OCCURRENCES = 25979
RESULT_OCCURRENCES = 24722
ASSOCIATION_OCCURRENCES = 1257
NORMALIZATION_LEDGER_ROWS = 25979
UNIQUE_OCCURRENCE_IDS = 25979
UNMAPPED_RAW_OCCURRENCES = 0
DUPLICATE_OCCURRENCE_IDS = 0
NORMALIZED_UNIQUE_ROWS = N
EXACT_DUPLICATE_GROUPS = N
COLLAPSED_EXACT_DUPLICATE_OCCURRENCES = N
IMPLICIT_DUPLICATE_GROUPS = N
IMPLICIT_ACCEPTED_GROUPS = N
IMPLICIT_HOLD_GROUPS = N
RAW_LINEAGE_LOSS = 0

======================================================================
6. STEP03B — HIGH-CONFIDENCE SANITATION
======================================================================

Input:
STEP_03A_NORMALIZED_UNIQUE_POOL_2026-09-11.tsv

Apply frozen client/business scope conservatively.

Every normalized analytical phrase must end in exactly one governed state:

KEEP_CANDIDATE
AUTO_EXCLUDED
HOLD_AMBIGUOUS
COLLAPSED_TO

Allowed AUTO_EXCLUDED classes are only high-confidence cases such as:
- explicit frozen business exclusion
- explicit foreign entity/brand when context proves foreign referent
- explicit media/game/book/song/film/person/place/organization context
- explicit unrelated vehicle/model/product context
- obvious lexical/morphology garbage
- technical noise
- malformed/empty analytical row
- duplicate already safely collapsed at Step03A
- high-confidence stop-topic pattern demonstrated by current evidence

A bare ambiguous phrase must NOT inherit the exclusion of a longer explicit foreign/media/entity phrase.

If a phrase can plausibly describe both client business and a foreign entity/topic:
HOLD_AMBIGUOUS

Do NOT auto-exclude solely because frequency is zero or low.
Do NOT keep solely because frequency is high.

Do NOT perform:
- final intent classification
- final cluster assignment
- page ownership
- IA/Page Jobs

---------------------------------------------------------------------
6A. DETERMINISTIC REASON CODES
---------------------------------------------------------------------

At minimum distinguish:

KEEP_DIRECT_BUSINESS_FIT
KEEP_PLAUSIBLE_BUSINESS_FIT
EXCLUDE_FROZEN_BUSINESS_BOUNDARY
EXCLUDE_EXPLICIT_FOREIGN_ENTITY
EXCLUDE_EXPLICIT_MEDIA
EXCLUDE_EXPLICIT_PERSON
EXCLUDE_EXPLICIT_PLACE
EXCLUDE_EXPLICIT_ORGANIZATION
EXCLUDE_EXPLICIT_VEHICLE_OR_MODEL
EXCLUDE_UNRELATED_PRODUCT
EXCLUDE_LEXICAL_GARBAGE
EXCLUDE_TECHNICAL_NOISE
COLLAPSED_EXACT_DUPLICATE
COLLAPSED_SAFE_IMPLICIT_DUPLICATE
HOLD_MULTI_MEANING
HOLD_ENTITY_COLLISION
HOLD_BUSINESS_FIT_UNCERTAIN

Additional precise reason codes are allowed.
Catch-all reasons that hide different mechanisms are forbidden.

---------------------------------------------------------------------
6B. REQUIRED STEP03B OUTPUTS
---------------------------------------------------------------------

Create:

<JOB>/STEP_03B_SANITIZED_CANDIDATE_POOL_2026-09-11.tsv

Minimum fields:
normalized_phrase_id
canonical_phrase
sanitation_state
sanitation_reason_code
sanitation_rule
business_fit_state
ambiguity_state
raw_occurrence_count
all_raw_occurrence_ids
seed_ids
run_orders
provider_request_ids
observed_count_values
implicit_duplicate_group_id
notes

This file contains retained working candidate rows only.

Create:

<JOB>/STEP_03B_EXCLUDED_HOLD_REGISTER_2026-09-11.tsv

Minimum fields:
normalized_phrase_id
canonical_phrase
sanitation_state
sanitation_reason_code
sanitation_rule
business_fit_state
ambiguity_state
raw_occurrence_count
all_raw_occurrence_ids
evidence_basis
notes

Include AUTO_EXCLUDED, HOLD_AMBIGUOUS and collapsed identities needed for full accounting.

Create:

<JOB>/STEP_03B_SANITATION_QA_2026-09-11.md

Prove:
NORMALIZED_UNIQUE_ROWS = N
KEEP_CANDIDATE_ROWS = N
AUTO_EXCLUDED_ROWS = N
HOLD_AMBIGUOUS_ROWS = N
COLLAPSED_ROWS = N
NORMALIZED_ACCOUNTING_RECONCILIATION = PASS
AUTO_EXCLUDED_WITHOUT_REASON = 0
HOLD_WITHOUT_REASON = 0
LOW_FREQUENCY_ONLY_EXCLUSIONS = 0
HIGH_FREQUENCY_ONLY_KEEPS = 0
AMBIGUOUS_SILENT_EXCLUSIONS = 0
RAW_LINEAGE_LOSS = 0
SEALED_SOURCE_VIOLATIONS = 0

Report AUTO_EXCLUDED counts by reason code.

======================================================================
7. DATA FUNNEL
======================================================================

Create:

<JOB>/KW002_DATA_FUNNEL_2026-09-11.json

At minimum:

{
  "raw_occurrence_rows": 25979,
  "result_occurrence_rows": 24722,
  "association_occurrence_rows": 1257,
  "normalized_unique_rows": N,
  "exact_duplicate_groups": N,
  "implicit_duplicate_groups": N,
  "collapsed_duplicate_rows": N,
  "auto_excluded_rows": N,
  "auto_excluded_rows_by_reason": {},
  "hold_ambiguous_rows": N,
  "sanitized_candidate_rows": N,
  "valid_reserve_rows": null,
  "delivery_selected_rows": null,
  "delivery_cap": null,
  "delivery_cap_state": "OWNER_DECISION_REQUIRED"
}

Do NOT invent the Blood & Sand DELIVERY_KEYWORD_CAP.
STANDARD_KWORK_DELIVERY_CEILING = 1500 is a product ceiling, not proof that this order purchased 1500.

Until owner freezes actual cap:
delivery_cap = null
valid_reserve_rows = null
delivery_selected_rows = null

This does not invalidate Step03A/03B, but it blocks final migration-baseline freeze and Step05 resume.

======================================================================
8. POST-SANITATION STEP04 RECONCILIATION PREPARATION
======================================================================

Do NOT rewrite corrected Step04 during Step03A/03B.

After sanitation, produce a reconciliation-ready summary with:
- normalized candidate count
- HOLD count needing family context
- corrected Step04 occurrences now mapping to AUTO_EXCLUDED rows
- corrected Step04 occurrences remaining active candidates
- corrected Step04 family rows affected by sanitation
- whether a dedicated post-sanitation Step04 Work pass is required

Do NOT advance Step05.

======================================================================
9. ADVERSARIAL QA
======================================================================

Explicitly search for:
- lost RAW occurrences
- same occurrence mapped twice
- missing provenance
- duplicate normalized IDs
- aggressive punctuation stripping
- unsafe word-order collapse
- unsafe inflection collapse
- entity-name collisions
- media-title collisions
- vehicle/model collisions
- low-frequency-only exclusions
- high-frequency-only keeps
- broad-token blacklist false positives
- bare ambiguous phrases inheriting exclusions from longer explicit phrases
- sum-of-duplicate-frequency inflation
- contamination from sealed prior Blood & Sand research

For every defect, fix the underlying deterministic rule, not only the example.

======================================================================
10. QUALITY SCORE
======================================================================

Score Step03A/03B using ten independent 0–10 dimensions:

1. GOAL_AND_OUTPUT_COMPLETENESS
2. METHOD_AND_SOURCE_SUPPORT
3. INPUT_EVIDENCE_AND_PROVENANCE_INTEGRITY
4. COVERAGE_AND_COMPLETENESS
5. ANALYTICAL_CORRECTNESS_AND_CLAIM_BOUNDARIES
6. ADVERSARIAL_QA_QUALITY
7. PERSISTENCE_READBACK_AND_REPRODUCIBILITY
8. OWNER_CLIENT_USABILITY_AND_PLAIN_LANGUAGE
9. INFORMATION_GAIN_COST_AND_EXECUTION_EFFICIENCY
10. DOWNSTREAM_READINESS

Report:
QUALITY_TOTAL_100
QUALITY_SCORE_10

PASS candidate requires:
QUALITY_TOTAL_100 >= 90
QUALITY_SCORE_10 >= 9.0
ALL HARD GATES = PASS
OPEN CRITICAL DEFECTS = 0

Work must NOT declare final Main ChatGPT acceptance.

======================================================================
11. GIT / SHARED BRANCH RULE
======================================================================

Before every material write block:
- read current live HEAD
- continue on top of current shared branch
- preserve unrelated concurrent work
- no reset
- no rebase of shared history
- no force push

Persist only artifacts belonging to this execution unit.

After publication:
- remote-read back every produced artifact
- verify blob SHA
- verify row counts
- verify QA arithmetic
- report final remote HEAD

======================================================================
12. RETURN TO MAIN CHATGPT
======================================================================

Return:

STEP03A = COMPLETE/PASS_CANDIDATE or BLOCKED
STEP03B = COMPLETE/PASS_CANDIDATE or BLOCKED

LIVE_BASE_HEAD = ...
FINAL_REMOTE_HEAD = ...

RAW_OCCURRENCES = 25979
NORMALIZATION_LEDGER_ROWS = 25979
NORMALIZED_UNIQUE_ROWS = N

EXACT_DUPLICATE_GROUPS = N
IMPLICIT_DUPLICATE_GROUPS = N
COLLAPSED_DUPLICATE_ROWS = N

KEEP_CANDIDATE_ROWS = N
AUTO_EXCLUDED_ROWS = N
HOLD_AMBIGUOUS_ROWS = N
SANITIZED_CANDIDATE_ROWS = N

RAW_LINEAGE_LOSS = 0
UNMAPPED_RAW_OCCURRENCES = 0
DUPLICATE_OCCURRENCE_IDS = 0
LOW_FREQUENCY_ONLY_EXCLUSIONS = 0
AMBIGUOUS_SILENT_EXCLUSIONS = 0
SEALED_SOURCE_VIOLATIONS = 0

DELIVERY_KEYWORD_CAP = OWNER_DECISION_REQUIRED

NEW_WORDSTAT_CALLS = 0
NEW_SEARCH_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_AI_SEARCH_CALLS = 0

QUALITY_TOTAL_100 = ...
QUALITY_SCORE_10 = ...

OUTPUT_PATHS
REMOTE_BLOB_SHAS
REMOTE_READBACK = PASS/FAIL

Do not execute Step05.
Do not start Step06.
```
