# MK03 — STEP RULES INDEX

Status: **ACTIVE / PHASE 3 METHOD EXTRACTION COMPLETE CANDIDATE**

## Canonical execution order

```text
STEP 00  Scope + current-site baseline
STEP 01  Representative Yandex discovery baseline
STEP 02  Real organic competitor discovery
STEP 03  Evidence-bearing competitor-page inspection
STEP 04  Competitor-derived topic/seed hypothesis
STEP 05  Wordstat expansion + normalization/sanitation
STEP 06  Material current-Search confirmation
STEP 07  Client coverage comparison + gap classification
STEP 08  Bounded structural opportunity interpretation
STEP 09  Client materialization + QA
```

## Step map

| Step | Purpose | Main output | Primary source authority |
|---|---|---|---|
| 00 | freeze site/region/scope and current public baseline | scope + current coverage baseline | PRODUCT_SCOPE; CLIENT_INPUT_CONTRACT; current-site freshness gates |
| 01 | create only enough representative query families to discover competitors | discovery query-family manifest | Step5A method + information-gain rules |
| 02 | identify domains that actually compete in Yandex organic results | competitor discovery register | STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD |
| 03 | inspect only evidence-bearing competitor pages | competitor page evidence register | STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD |
| 04 | derive traceable genuinely new demand probes | competitor-derived seed register | Step5A method + scope controls |
| 05 | validate demand and compact data correctly | raw/normalized/sanitized competitor acquisition layer | STEP_05A_VOLUME_SANITATION_ADDENDUM + DATA_VOLUME gate |
| 06 | support exact visibility/intent/page-type claims where material | tested query visibility matrix | SERP_COVERAGE_MODE_DECISION + Search claim controls |
| 07 | compare accepted candidates with current client coverage | gap decision register | Step5A decision/merge + current-site freshness |
| 08 | translate confirmed gaps into bounded next-step opportunities | opportunity register | PRODUCT_SCOPE boundaries + no-automatic-CREATE control |
| 09 | expose inspectable results and verify recipient usefulness | client package + QA receipt | Step19/20 recipient QA authorities |

## Mandatory cross-step invariants

Every step obeys `GENERAL_RULES.md` and `ERRORS_AND_LESSONS.md`.

Hard failures:

```text
PAGE TOPIC AS RANKING EVIDENCE
CLIENT COMPETITOR HINT AS ORGANIC COMPETITOR TRUTH
RAW WORDSTAT APPENDED DIRECTLY
UNPROBED QUERY CALLED SEARCH-CONFIRMED
CONFIRMED GAP AUTO-CONVERTED TO CREATE URL
FULL DOMAIN KEYWORD UNIVERSE CLAIM FROM BOUNDED TESTS
DEEP COMPETITOR AUDIT CREEP
SUMMARY COUNTS WITHOUT INSPECTABLE RESULT
SILENT DROPS
```

## State accounting

Material candidate end states:

```text
CONFIRMED_GAP
ALREADY_COVERED
REJECT_OFF_SCOPE
HOLD_EVIDENCE
```

Every row must be count-reconciled into one visible state or a documented deterministic duplicate collapse with preserved lineage.

## Provider boundary

```text
SEARCH = SELECTIVE_DECISION_SERP
WORDSTAT = ONLY GENUINELY NEW INFORMATION-GAIN PROBES
REUSE PRESERVED CURRENT EVIDENCE BEFORE NEW CALL
NO THIRD-PARTY REVERSE-DOMAIN PROVIDER REQUIRED
```

## Phase-5 activation gate

Phase 5 remains blocked until this index, every local step, GENERAL_RULES, ERRORS_AND_LESSONS, EXECUTION_ROADMAP, DELIVERABLE_SPEC, QA_AND_RELEASE and METHOD_CONSISTENCY_AUDIT agree and remote readback passes.
