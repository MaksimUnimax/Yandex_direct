# STEP 04 — WORK PRE-HANDOFF MANIFEST

Date: 2026-09-09
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Step: `04 — first family triage`
Status: `PREPARED / EXECUTION GATED BY LEVEL2 DRAFT STATUS`

## Why Work is required

Step03 closed with 79/79 primary acquisition probes and a large preserved Wordstat corpus. The owner explicitly required that semantic processing of this large corpus not be performed in normal chat. Row/family-scale processing must therefore use the Level-1 Work handoff path.

## Allowed input files / sources

Repository: `MaksimUnimax/Yandex_direct`
Branch: `roadmap/kwork-productization-2026-08-28`

Current-job authority only:

- `extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08/CLIENT_SUPPLIED_BRIEF.md`
- `.../CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md`
- `.../CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv`
- `.../ALLOWED_INPUTS_AND_SEALED_SOURCES.md`
- `.../STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`
- `.../STEP_03_COLLECTION_CLOSURE_2026-09-09.md`
- `.../STEP_03_WORDSTAT_RAW_PERSISTENCE_STATE_2026-09-09.md`
- complete current-job `STEP_03_WORDSTAT_RAW/` evidence tree, including reconstructable compressed carrier manifests
- `extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/LEVEL1/WORK_HANDOFF_RULE.md`
- `extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`
- `extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/LEVEL2/STEP_RULES_INDEX.md`
- `.../STEP_04_PRE_STEP_SOURCE_TRACE_2026-09-09.md`

## Prohibited inputs

- all sealed prior Blood & Sand SEO/Wordstat/Search/Alice/GenSearch/competitor/cluster/IA/Page Job research not explicitly whitelisted by the current job authority;
- conclusions from KW001/OKNO_MSK as evidence for Blood & Sand demand;
- new provider calls of any kind;
- unsourced assumptions about assortment, materials, meanings, buyer intent, or business claims.

## Current authoritative upstream facts

```text
STEP03_PRIMARY_MANIFEST_ROWS = 79
STEP03_CURRENT_ACQUISITION_COVERAGE = 79/79
STEP03_PERSISTENCE = PASS
FINAL_S001_RESULTS_ROWS = 2000
FINAL_S001_ASSOCIATIONS_ROWS = 20
FINAL_S001_TOTALCOUNT = 478857
```

Historical missing-original request bodies and current-provider re-query bodies must remain distinct provenance classes.

## Execution gate

Before doing any Step04 semantic classification, re-read `LEVEL2/STEP_RULES_INDEX.md` from the live branch.

If it still says:

`Status: DRAFT FOR OWNER REVIEW / DO NOT EXECUTE YET`

then STOP before semantic triage. Do not bypass or reinterpret that status. Return only a gate/readiness report identifying that the frozen corpus and handoff are ready but Step04 execution is blocked pending owner acceptance of Level2.

If the owner has explicitly changed/accepted the Level2 gate so Step04 is executable, continue with the canonical prompt below.

## Exact execution goal once gate is open

Perform Step04 `first family triage` over the complete Step03 acquisition corpus. Build a traceable family-level inventory before row-level cleanup. This is not final keyword cleanup and not clustering/page design.

Classify observed demand/expansion families using the Level2 authority categories:

- `strong in-scope`
- `plausible in-scope`
- `mixed/ambiguous`
- `obvious out-of-scope`
- `coverage gap / requires expansion`

Every decision must preserve provenance and have an explicit reason code. Never reject a family solely because frequency is low.

## Required outputs once gate is open

Materialize under the current job workspace:

1. `STEP_04_FAMILY_TRIAGE_2026-09-09.tsv`
2. `STEP_04_TARGETED_EXPANSION_QUEUE_2026-09-09.tsv`
3. `STEP_04_TRIAGE_QA_2026-09-09.md`
4. `STEP_04_WORK_RETURN_RECEIPT_2026-09-09.md`

Minimum fields for `STEP_04_FAMILY_TRIAGE`:

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

Minimum fields for targeted expansion queue:

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

## Mandatory processing rules

- Read the full corpus programmatically; do not rely on snippets or sample rows.
- Reconstruct compressed lossless carriers when required by their manifests.
- Preserve every raw occurrence in the source evidence; Step04 output may summarize families but must retain locators back to source evidence.
- Do not silently deduplicate away provenance.
- Do not convert Wordstat `count` or `totalCount` into business relevance.
- Distinguish entity collisions, automotive Chery Amulet noise, media/book/game queries, morphology noise and other off-topic families from actual in-scope demand only on evidence, not token heuristics alone.
- Genuine uncertainty must remain `mixed/ambiguous`; do not force a binary answer.
- Do not create final clusters, URLs, page types, IA, Page Jobs, titles, headings, or content recommendations.
- Do not run Wordstat, Search, GenSearch, Alice, or any other provider.
- Do not use sealed prior research.

## QA / acceptance checks

At minimum verify:

```text
INPUT_PRIMARY_PROBES_ACCOUNTED = 79/79
SOURCE_CARRIERS_READ_OR_RECONSTRUCTED = PASS
SILENT_SOURCE_DROPS = 0
FAMILY_ROWS_WITH_REASON_CODE = 100%
FAMILY_ROWS_WITH_PROVENANCE = 100%
LOW_FREQUENCY_ONLY_REJECTIONS = 0
FORCED_AMBIGUITY_DECISIONS = 0
SEALED_SOURCE_VIOLATIONS = 0
NEW_PROVIDER_CALLS = 0
FINAL_CLUSTERING_PERFORMED = false
PAGE_DESIGN_PERFORMED = false
```

## Canonical Work prompt

```text
You are taking over the large-data processing portion of the active KW-002 Blood & Sand greenfield semantic-core rehearsal.

Repository: MaksimUnimax/Yandex_direct
Branch: roadmap/kwork-productization-2026-08-28
Job: extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08

THIS IS NOT A NEW PROJECT. DO NOT RESTART STEPS 00-03. DO NOT MAKE PROVIDER CALLS.

First read, in full, the job's ALLOWED_INPUTS_AND_SEALED_SOURCES.md, STEP_03_COLLECTION_CLOSURE_2026-09-09.md, STEP_03_WORDSTAT_RAW_PERSISTENCE_STATE_2026-09-09.md, STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv, LEVEL1/WORK_HANDOFF_RULE.md, LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md, LEVEL2/STEP_RULES_INDEX.md, and STEP_04_PRE_STEP_SOURCE_TRACE_2026-09-09.md.

Before semantic processing, check the live Level2 status. If it is still 'DRAFT FOR OWNER REVIEW / DO NOT EXECUTE YET', do not perform Step04 triage. Materialize only STEP_04_WORK_RETURN_RECEIPT_2026-09-09.md stating the exact blocking gate and confirming that the 79/79 corpus is readable; then stop.

Only if Level2 is explicitly executable/owner-accepted: process the complete Step03 Wordstat raw corpus programmatically and execute Step04 first-family triage exactly as defined by the current Level2 authority. Account for all 79 primary acquisition probes. Reconstruct lossless compressed carriers where needed. Never use only snippets. Preserve provenance to run_order, seed, request/carrier and raw evidence.

Classify observed families as strong in-scope, plausible in-scope, mixed/ambiguous, obvious out-of-scope, or coverage gap/requires expansion. Give every family an explicit reason code and reason text. Frequency alone is never a reject rule. Keep genuine ambiguity unresolved. Distinguish provider morphology/entity collisions and unrelated topics from business demand using business/assortment authority and observed query meaning, not superficial token rules.

Materialize:
- STEP_04_FAMILY_TRIAGE_2026-09-09.tsv
- STEP_04_TARGETED_EXPANSION_QUEUE_2026-09-09.tsv
- STEP_04_TRIAGE_QA_2026-09-09.md
- STEP_04_WORK_RETURN_RECEIPT_2026-09-09.md

Do not perform final row cleanup, clustering, intent-to-page mapping, page creation, IA, Page Jobs, content recommendations or any Wordstat/Search/AI provider call. Do not use sealed prior Blood & Sand analytical research. Do not silently drop source rows/provenance.

QA must prove 79/79 primary probes accounted, zero silent source drops, 100% reason-code coverage, 100% provenance coverage, zero low-frequency-only rejections, zero forced ambiguity decisions, zero sealed-source violations, zero new provider calls, and no clustering/page-design work.

Commit only intended KW002 job artifacts on top of the CURRENT live shared branch without reset/rebase/force-push. If the branch advances concurrently, re-read live HEAD and preserve unrelated work. Return commit SHA, output counts, QA results, and exact blockers/uncertainties.
```
