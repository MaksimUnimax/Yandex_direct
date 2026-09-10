# STEP 04 — CHATGPT WORK PRE-HANDOFF MANIFEST — RERUN

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Step: `04 — first family triage`
Status: **FROZEN / OWNER GATE PASS / STEP03 79/79 PASS / READY FOR CHATGPT WORK**

## Why this is a rerun

The prior Work attempt recorded in `STEP_04_WORK_RETURN_RECEIPT_2026-09-09.md` correctly stopped before semantic triage because, at that time:

```text
LEVEL2 OWNER EXECUTION GATE = BLOCKED
LOSSLESS DURABLE RAW = 60/79
```

Both blockers are now resolved:

```text
STEP03_DURABLE_FEED_FORWARD = 79/79 / PASS
STEP04_OWNER_GATE = PASS / STEP04_ONLY
```

The prior Work receipt is historical evidence only. It must not be overwritten or treated as the current blocker.

## Why Work is required

`LEVEL1/WORK_HANDOFF_RULE.md` is ACTIVE / OWNER-LOCKED. Step04 requires complete semantic processing of a large multi-file Wordstat corpus with provenance. Normal chat must not sample, truncate, first-N, representative-example, or summary-only the corpus.

## Current authority precedence for this rerun

Read the following current authorities in this order when any older statement conflicts:

1. `LEVEL2/STEP04_OWNER_EXECUTION_GATE_2026-09-10.md`
2. `work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_04_EXECUTION_CURSOR_2026-09-10.json`
3. `work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_03_RAW_RECOVERY_PROGRESS_2026-09-09.json`
4. `work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_03_RAW_RECOVERY_FINAL_RECEIPT_2026-09-10.md`
5. `work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_03_WORDSTAT_RAW_PERSISTENCE_STATE_2026-09-09.md` as corrected on 2026-09-10
6. `work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_04_PRE_STEP_SOURCE_TRACE_2026-09-10.md`
7. `LEVEL1/WORK_HANDOFF_RULE.md`
8. `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`
9. the Step04 method body inside `LEVEL2/STEP_RULES_INDEX.md`

For Step04 only, `LEVEL2/STEP04_OWNER_EXECUTION_GATE_2026-09-10.md` is the later owner-specific acceptance that supersedes the old document-wide `DRAFT FOR OWNER REVIEW / DO NOT EXECUTE YET` header. It does not authorize Step05 or later steps.

## Allowed business/job inputs

Repository: `MaksimUnimax/Yandex_direct`
Branch: `roadmap/kwork-productization-2026-08-28`

Use only current KW-002 job/method authorities, including:

- `CLIENT_SUPPLIED_BRIEF.md`
- `CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md`
- `CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv`
- `ALLOWED_INPUTS_AND_SEALED_SOURCES.md`
- `STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`
- `STEP_03_COLLECTION_CLOSURE_2026-09-09.md`, subject to later corrections above
- `STEP_03_RAW_RECOVERY_PROGRESS_2026-09-09.json`
- `STEP_03_RAW_RECOVERY_FINAL_RECEIPT_2026-09-10.md`
- corrected `STEP_03_WORDSTAT_RAW_PERSISTENCE_STATE_2026-09-09.md`
- complete current-job `STEP_03_WORDSTAT_RAW/` evidence tree
- current Level1/Level2 authorities listed above
- `STEP_04_PRE_STEP_SOURCE_TRACE_2026-09-10.md`

## Critical RAW replacement rule

Do **not** make successful reconstruction of the two historically broken manual gzip bundles a current Step04 pass condition.

Those old bundle parts remain historical provenance of the persistence defect. Current downstream feed-forward is supplied by complete durable replacement carriers.

Use `STEP_03_RAW_RECOVERY_PROGRESS_2026-09-09.json` as the mapping authority:

```text
run_orders 32-48 -> RECOVERY_REQUERY__<run_order>__<fresh_request_id>.raw.txt
run_orders 50-51 -> RECOVERED__050/051 complete empty-object outcomes
run_order 49 -> independent readable original carrier
all other run_orders -> their already complete current job RAW carriers
```

Every fresh recovery request ID remains distinct from the historical request ID. Preserve both provenance classes where relevant; never rewrite historical identity.

## Prohibited inputs/actions

- sealed prior Blood & Sand Wordstat/Search/Alice/GenSearch/competitor/cluster/IA/Page Job analysis;
- KW-001/OKNO_MSK conclusions as Blood & Sand demand evidence;
- any new Wordstat/Search/GenSearch/Alice/provider request;
- assumptions not supported by current business/assortment evidence;
- final row cleanup;
- final intent assignment;
- SERP clustering;
- URL/page ownership;
- IA/Page Jobs;
- page titles/headings/content recommendations.

## Exact execution goal

Process the complete current Step03 feed-forward corpus programmatically and build a traceable **family-level preliminary triage** before row-level cleanup.

Classify observed demand/expansion families only as:

```text
strong in-scope
plausible in-scope
mixed/ambiguous
obvious out-of-scope
coverage gap / requires expansion
```

Rules:

```text
FAMILY TRIAGE != FINAL ROW CLEANUP
LOW FREQUENCY ALONE != IRRELEVANCE
WORDSTAT COUNT != BUSINESS RELEVANCE
AMBIGUITY MUST REMAIN EXPLICIT
PROVENANCE MUST SURVIVE FAMILY SUMMARIZATION
```

Evaluate meaning against the actual current Blood & Sand business/assortment authority. Distinguish clear entity collisions, Chery Amulet/automotive noise, unrelated books/media/games, morphology noise and other off-topic families from genuine product/use demand only when evidence supports the distinction. Do not use a superficial token blacklist as a substitute for meaning.

## Required outputs

Materialize under the current job workspace:

1. `STEP_04_FAMILY_TRIAGE_2026-09-10.tsv`
2. `STEP_04_TARGETED_EXPANSION_QUEUE_2026-09-10.tsv`
3. `STEP_04_TRIAGE_QA_2026-09-10.md`
4. `STEP_04_WORK_RETURN_RECEIPT_2026-09-10.md`

Do not overwrite the historical `STEP_04_WORK_RETURN_RECEIPT_2026-09-09.md`.

## Mandatory fields — family triage

```text
family_id
family_label
triage_state
reason_code
reason_text
originating_run_orders
originating_seed_ids
originating_seed_phrases
provider_request_ids_or_carrier_locators
representative_observed_phrases
observed_count_range_or_summary
business_authority_locator
assortment_support_state
ambiguity_state
coverage_state
next_step_action
do_not_infer_boundary
```

## Mandatory fields — targeted expansion queue

```text
queue_id
family_id
expansion_reason
missing_vocabulary_or_boundary
proposed_evidence_route
provider_call_required
owner_clarification_required
priority_basis
source_locators
```

`provider_call_required` is a planning field for Step05. **Do not make the call in Step04.**

## Source/corpus accounting

At minimum prove:

```text
CANONICAL_PRIMARY_MANIFEST_ROWS = 79
UNIQUE_RUN_ORDERS_ACCOUNTED = 79/79
CURRENT_FEED_FORWARD_SOURCE_FOR_EACH_RUN_ORDER = RESOLVED
SILENT_SOURCE_DROPS = 0
```

If a current replacement carrier cannot be read, do not fall back silently to the broken historical gzip bundle or a manifest summary. Record the exact missing current carrier and STOP with a real blocker.

## QA / acceptance

Required:

```text
INPUT_PRIMARY_PROBES_ACCOUNTED = 79/79
CURRENT_SOURCE_CARRIERS_READ = PASS
SILENT_SOURCE_DROPS = 0
FAMILY_ROWS_WITH_REASON_CODE = 100%
FAMILY_ROWS_WITH_PROVENANCE = 100%
LOW_FREQUENCY_ONLY_REJECTIONS = 0
FORCED_AMBIGUITY_DECISIONS = 0
SEALED_SOURCE_VIOLATIONS = 0
NEW_PROVIDER_CALLS = 0
FINAL_ROW_CLEANUP_PERFORMED = false
FINAL_CLUSTERING_PERFORMED = false
PAGE_DESIGN_PERFORMED = false
```

Also report:

```text
family_row_count
triage_state_counts
targeted_expansion_queue_row_count
families_with_owner_clarification_required
families_with_provider_call_required_for_future_step05
any unresolved evidence defects
```

## Git / concurrency rule

Before writing, read live branch HEAD. Commit only intended KW002 Step04 outputs on top of the current live shared branch. Do not reset, rebase, force-push or overwrite concurrent unrelated work. If the branch advances, re-read live HEAD and preserve unrelated changes.

## Stop conditions

Stop Step04 and return an explicit blocker only if:

- a required current feed-forward carrier is actually unreadable/missing after using the recovery mapping;
- the current business/assortment authority needed for a material family decision is missing, in which case keep family ambiguity where possible and only block if the whole step cannot be completed;
- source/provenance accounting cannot reach 79/79;
- repository write/readback cannot be verified.

Do not stop because the old historical gzip bundles still fail their historical checksum. That defect has already been repaired for feed-forward by replacement carriers while historical provenance remains preserved.

Canonical executable prompt: `STEP_04_CANONICAL_WORK_PROMPT_2026-09-10.md`.
