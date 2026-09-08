# KW-001 / OKNO_MSK — Step 5A first execution Work handoff

Status: **READY FOR WORK EXECUTION**

## 1. Purpose

Run the **first project validation of existing Level-1 Step 5A** using preserved OKNO_MSK evidence.

This is **not** a new methodology design task and **not** a post-release client-document correction task.

Canonical Level-1 authority:

- `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md`
- `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_RULES_INDEX.md`

The current method status is:

```text
ROADMAP_STAGE_EXISTS = true
OWNER_AUTHORIZED_ROADMAP_INSERTION = true
PROJECT_TEST_VALIDATED = false
```

The purpose of this execution is to produce the first real project evidence for that validation.

## 2. Starting branch / base

Repository:

`MaksimUnimax/Yandex_direct`

Branch:

`roadmap/kwork-productization-2026-08-28`

Expected handoff base HEAD:

`5d5e38c380042702979dd6f6a80bc59bc69083cd`

Before any write, Work must re-read live HEAD and preserve any legitimate later commits if HEAD moved.

## 3. Role boundary

This task is intentionally assigned to **Work** because it requires bulk processing of preserved SERP evidence.

Main ChatGPT must not manually iterate the 750 SERP rows in chat.

Work must perform the bulk analysis, persist durable artifacts, commit them, and perform remote GitHub readback.

Yandex Bridge is **not** controlled by Work for this task.

## 4. Hard acquisition boundary

For this first execution block:

```text
NEW_YANDEX_SEARCH_CALLS = 0
NEW_WORDSTAT_CALLS = 0
NEW_ALICE_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_WEBMASTER_CALLS = 0
NEW_METRIKA_CALLS = 0
NEW_DIRECT_CALLS = 0
NEW_PAID_PROVIDER_COST_RUB = 0
```

Use preserved evidence first.

Do not launch any new provider acquisition.

If later Step 5A execution truly requires new Wordstat/Search evidence, materialize the exact evidence requirement and stop before the provider call so Main ChatGPT can control the Yandex Bridge separately.

## 5. Preserved Step 9 SERP authority

The normalized ordinary-Yandex evidence is complete for the initial tranche:

- query 1 canary: `STEP_09_SERP_RESULTS.tsv`
- queries 2–20: `STEP_09_SERP_R2_PROJECTION_RAW_PART_01.tsv`
- queries 21–39: `STEP_09_SERP_R2_PROJECTION_RAW_PART_02.tsv`
- queries 40–58: `STEP_09_SERP_R2_PROJECTION_RAW_PART_03.tsv`
- queries 59–75: `STEP_09_SERP_R2_PROJECTION_RAW_PART_04.tsv`
- persistence index: `STEP_09_SERP_R2_PROJECTION_INDEX.md`
- Step 9 analytical decisions: `STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv`

Expected source accounting:

```text
queries = 75
ranked_rows = 750
region = 213
ranks_per_query = 1..10
```

Do not invent unavailable raw fields. The R2 projection does not contain snippets, raw provider XML, per-item provider request IDs, or HTTP status fields.

## 6. Downstream authorities for tracing impact

Use preserved downstream truth to determine what Search evidence later influenced or confirmed.

Read as needed:

- `STEP_10_CLUSTER_ASSIGNMENTS.tsv`
- `STEP_10_CLUSTER_SUMMARY.tsv`
- corrected/final Step 10 authorities where applicable
- `STEP_11_PAGE_OWNERSHIP_CORRECTED.tsv`
- `STEP_11_PHRASE_PAGE_MAP.tsv`
- `RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv`
- `RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv`
- `RESEARCH_REBUILD_STAGE_07_SEARCH_CASE_EXPLANATION_2026-09-05.tsv`
- `STEP_19_06_SOURCE_COMPETITOR_OBSERVATIONS.tsv`

Use the latest applicable canonical authority when early and corrected artifacts disagree.

Do not rewrite historical completed client decisions.

## 7. Required execution — Phase A: reconstruct the full 75-query SERP dataset

Materialize one deterministic combined ledger from the five preserved Step 9 sources.

Required columns where supported:

```text
query_index
query_text
item_id
region
rank
url
domain
normalized_domain
title
source_file
```

Required QA:

```text
SOURCE_QUERIES = 75
SOURCE_RANKED_ROWS = 750
ACCOUNTED_QUERIES = 75
ACCOUNTED_RANKED_ROWS = 750
SILENT_ROW_DROPS = 0
DUPLICATE_ROW_INFLATION = 0
```

## 8. Required execution — Phase B: identify real recurring Yandex competitors

From the preserved 750 rows:

1. Normalize domains deterministically.
2. Count recurrence by:
   - total TOP-10 appearances;
   - distinct queries;
   - TOP-1 / TOP-3 / TOP-5 appearances;
   - best rank;
   - median rank where useful.
3. Classify domains at minimum into:
   - `DIRECT_BUSINESS_COMPETITOR`
   - `ORGANIC_COMPETITOR_OTHER_MODEL`
   - `AGGREGATOR_DIRECTORY`
   - `MARKETPLACE`
   - `MANUFACTURER_OR_BRAND_SOURCE`
   - `INFORMATIONAL_PUBLISHER`
   - `YANDEX_PLATFORM`
   - `OTHER_REVIEW`
   - `UNKNOWN`
4. Do not equate recurrence with business comparability.
5. Identify the recurring domains that are actually useful as Step 5A competitor candidates.

## 9. Required execution — Phase C: trace what ordinary Yandex Search changed or confirmed

For all 75 queries, where the preserved downstream authorities allow a trustworthy join, build a trace:

```text
query
→ preserved SERP observation
→ Step 9 decision
→ downstream user-task / cluster decision
→ page-ownership / structural decision
→ impact classification
```

Use explicit impact classes:

```text
CHANGED_DECISION
DE_RISKED_DECISION
CONFIRMED_EXISTING_DECISION
NO_MATERIAL_DOWNSTREAM_EFFECT
UNRESOLVED_TRACE
```

The core question is:

**What exactly did the Yandex TOP analysis influence in OKNO_MSK, and what did it merely confirm?**

Do not assign causal impact unless it can be traced to preserved project evidence.

## 10. Required execution — Phase D: Step 5A competitor candidate selection

Using recurrence + business comparability + semantic/task diversity, select a bounded set of real search competitors for the next Step 5A phase.

For each selected competitor record:

- domain;
- number of distinct Step 9 queries;
- strongest ranks;
- relevant query/task areas;
- competitor class;
- why this domain is a useful semantic-gap source;
- exact ranking URLs from preserved evidence that should be inspected next.

Do not yet perform new Wordstat/Search acquisition.

If public competitor-page inspection can be done within Work without new Yandex provider calls, it may inspect only the selected evidence-bearing public URLs needed to derive candidate themes/seeds and must preserve URL-level provenance. Do not broaden into a full technical competitor SEO audit.

## 11. Required artifacts

Create an isolated directory under:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_05A_FIRST_EXECUTION_2026-09-08/`

Materialize at least:

```text
CHECKPOINT_00_BASELINE_AND_REUSE_INVENTORY.md
STEP_05A_SERP_COMBINED_750.tsv
STEP_05A_DOMAIN_FREQUENCY.tsv
STEP_05A_QUERY_IMPACT_TRACE.tsv
STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv
STEP_05A_FIRST_EXECUTION_QA.json
STEP_05A_FIRST_EXECUTION_REPORT.md
EXECUTION_LOG.md
```

If public competitor pages are inspected in this execution, also create:

```text
STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv
STEP_05A_DERIVED_SEED_CANDIDATES.tsv
```

## 12. Scope protection

Do not modify:

- corrected client release;
- Document 01;
- Document 02;
- Document 03;
- standalone semantic-core XLSX;
- historical Step 0–20 canonical outputs.

The new Step 5A execution must remain an isolated methodology-validation layer.

## 13. Persistence discipline

Do not do the whole execution only in Work memory.

After each material block:

```text
WORK
→ SAVE
→ COMMIT
→ REMOTE GITHUB READBACK
→ CONTINUE
```

At minimum persist and read back:

1. baseline/reuse checkpoint;
2. combined 750-row SERP ledger + QA;
3. domain-frequency / competitor inventory;
4. query-impact trace;
5. candidate selection + first-execution report.

## 14. Completion boundary

This Work task is complete when:

- all 75 queries and 750 rows are accounted for;
- recurring real Yandex competitors are identified;
- the impact of Step 9 Search evidence on later OKNO_MSK decisions is traced as far as evidence supports;
- a bounded real-competitor candidate set is selected for Step 5A;
- all artifacts are committed;
- remote GitHub readback passes;
- no new governed provider calls were made.

If the next Step 5A subphase requires new Wordstat or new Yandex Search evidence, do **not** perform it. Record the exact required seeds/queries and return control to Main ChatGPT, which controls the Yandex Bridge.

## 15. Final Work response

Return only an execution summary containing:

- starting HEAD;
- final HEAD;
- commit SHAs;
- source accounting 75 / 750;
- number of normalized domains;
- top recurring direct competitors;
- impact counts by class;
- selected competitor candidates;
- whether public competitor-page inspection was completed;
- exact new Wordstat/Search evidence required next, if any;
- provider calls = 0 confirmation;
- remote readback = PASS/FAIL.
