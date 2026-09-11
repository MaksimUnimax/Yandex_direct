# KW-002 — W09 Step04 current-authority rerun execution release

Date: 2026-09-11
Status: **RELEASED TO WORK / CURRENT REMOTE AUTHORITY REQUIRED / STEP05 BLOCKED**

## Why this rerun exists

The owner-uploaded W08 correction materially improved the Step04 data and passed remote publication presence checks, but Main ChatGPT found that Work had executed from a stale repository base and froze the superseded W08 prompt/release rather than the current universal-cause V2 authority.

Therefore W08 is preserved as historical correction evidence but is not accepted as the current Step04 authority.

Main review:

`STEP_04_POST_AUDIT_CORRECTED_MAIN_CHATGPT_REMOTE_REVIEW_2026-09-11.md`

## Canonical prompt

Execute exactly:

`STEP_04_CURRENT_UNIVERSAL_CAUSE_CORRECTION_RERUN_WORK_PROMPT_2026-09-11.md`

## Mandatory universal authorities

Read IN FULL:

- `LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`
- `LEVEL1/WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md`
- `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`
- `LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md`
- `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`
- `LEVEL1/RESULT_QUALITY_SCORING_RULE.md`
- `LEVEL1/WORK_HANDOFF_RULE.md`
- `LEVEL2/README.md`
- `LEVEL2/STEP_RULES_INDEX.md`
- `LEVEL2/STEP_04_PRELIMINARY_FAMILY_TRIAGE_QUALITY_GATE.md`

## Execution identity

```text
HANDOFF_ID = KW002-BS-W09
STEP_ID = STEP04_CURRENT_AUTHORITY_FULL_VOLUME_UNIVERSAL_CAUSE_RERUN
```

The exact remote HEAD must be fetched by Work at execution start. Do not use a hard-coded historical base as a substitute for that live check.

## Hard start gate

```text
REMOTE_FETCH_PERFORMED = true
WORK_START_REMOTE_HEAD = REMOTE_BRANCH_HEAD_AT_START
CURRENT_W09_PROMPT_PRESENT = true
CURRENT_W09_RELEASE_PRESENT = true
CURRENT_UNIVERSAL_LEVEL1_LEVEL2_PRESENT = true
```

Fail closed if not true.

## Analytical boundaries

```text
NORMALIZED_IDENTITIES_EXPECTED = 24576
RAW_OCCURRENCES_EXPECTED = 25979
STEP03A_MUTATION_ALLOWED = false
STEP03B_MUTATION_ALLOWED = false
WORDSTAT_CALLS_ALLOWED = 0
ORDINARY_SEARCH_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
STEP05_ADVANCEMENT_ALLOWED = false
STEP06_ADVANCEMENT_ALLOWED = false
FINAL_INTENT_ALLOWED = false
SERP_CLUSTERING_ALLOWED = false
QUERY_TO_PAGE_ALLOWED = false
```

## Current universal hard gates

```text
UNBOUNDED_PREFIX_OR_SUBSTRING_AS_SEMANTIC_PROOF = 0
EXPLICIT_TASK_HIDDEN_BY_BROADER_TOPIC = 0
RULE_PRECEDENCE_CONTRACT = PRESENT
REPEATED_EXPLICIT_TASK_PATTERN_HIDDEN_IN_GENERIC = 0
UNKNOWN_TASK_DISCOVERY_ROUTE = PRESENT
INDEPENDENT_DIAGNOSTIC_DEFECT_LOGIC_NOT_LIMITED_TO_KNOWN_PSF_IDS = true
LARGE_GENERIC_FAMILY_HETEROGENEITY_AUDIT = PASS
PROVIDER_READY_WITH_EQUIVALENT_DURABLE_EVIDENCE = 0
OWNER_FACT_GAP_SENT_TO_PROVIDER = 0
RAW_LINEAGE_LOSS = 0
STEP03B_MUTATIONS = 0
STALE_BASE_MUTABLE_STATE_FILE_OVERWRITE = 0
```

Known W07/W08 defects are regression fixtures only and do not define the method.

## Pre-publication authority gate

Immediately before push/owner-relay:

```text
REMOTE_HEAD_RECHECKED = true
WORK_PRE_PUBLICATION_REMOTE_HEAD = recorded
REMOTE_ADVANCED_AFTER_START = true|false
```

If remote advanced and governing authorities changed, Work must reconcile/revalidate before publication.

Mutable current-state files must not be blindly uploaded from a stale workspace.

## PASS candidate

A Work return may be only `PASS_CANDIDATE`. Main ChatGPT must independently remote-read and accept it.

PASS candidate requires all prompt gates plus:

```text
FULL_VOLUME_ACCOUNTING = PASS
CURRENT_AUTHORITY_SIGNAL_LEDGER = COMPLETE
INDEPENDENT_POST_CORRECTION_TAXONOMY_AUDIT = PASS
ALL_JOB_FIXTURE_REGRESSIONS = PASS
OPEN_CRITICAL_DEFECTS = 0
PROVIDER_CALLS = 0
STEP05_ADVANCEMENT = false
STEP06_ADVANCEMENT = false
```

## Stop

Stop after W09 analytical artifacts, QA, manifest and publication/owner-relay preparation.

Do not resume Step05 in the same run.
