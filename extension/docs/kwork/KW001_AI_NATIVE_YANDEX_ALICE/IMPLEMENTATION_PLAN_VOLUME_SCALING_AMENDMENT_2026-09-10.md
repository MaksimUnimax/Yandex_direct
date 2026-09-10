# KW-001 — IMPLEMENTATION PLAN VOLUME-SCALING AMENDMENT

Date: 2026-09-10  
Status: **OWNER-APPROVED / ACTIVE / UNIVERSAL PRODUCT-PLAN AMENDMENT**

This amendment applies to `IMPLEMENTATION_PLAN.md` and changes only the acquisition-volume/scalability architecture. All existing commercial objective, Alice-native positioning, competitor claim boundaries, implementation-readiness rules and recipient QA requirements remain in force.

## 1. Problem corrected

The previous product flow could preserve a complete Wordstat occurrence corpus and then carry too much of that raw volume through family triage and expansion before Step7 performed the first deep row-level cleanup.

That is acceptable for a small corpus but does not scale to large e-commerce catalogs.

Canonical correction:

```text
COMPLETE PROVIDER EVIDENCE
!= COMPLETE ANALYST/LLM WORKING SET
```

## 2. Corrected product-level flow

```text
scope + existing-site/business model
-> bounded search-entity seed map
-> Step3 Wordstat LOSSLESS RAW
-> Step3A normalization / exact + safe implicit deduplication
-> Step3B conservative high-confidence sanitation
-> compact sanitized candidate pool
-> Step4 family triage
-> Step5 targeted expansion
   -> every new provider result immediately through Step3A/3B
-> Step5A competitor semantic expansion
   -> every competitor-derived Wordstat result immediately through Step3A/3B
-> Step6/6A controls if validated/authorized
-> Step7 nuanced row-level semantic cleanup
-> Step8 Search-stage semantic freeze
-> Step9 ordinary Search only for retained decision-relevant queries/boundaries
-> Step10 clustering
-> Step11+ page/action architecture
-> Step15 bounded AI diagnostic set
-> Step16 bounded AI evidence
-> final reconciliation / prioritization / deliverables
```

## 3. Large catalog acquisition rule

Do not translate catalog size directly into Wordstat probe count.

```text
500 SKU != 500 mandatory broad Wordstat probes
5000 SKU != 5000 mandatory broad Wordstat probes
```

Initial discovery is built around search-relevant categories, subcategories, product types, uses, attributes/materials/form factors and brand/model families.

Individual SKU/model probes are selective and require distinct search identity or decision value.

## 4. Data layers

KW-001 now explicitly separates:

```text
RAW_OCCURRENCE_POOL
NORMALIZED_UNIQUE_POOL
SANITIZED_CANDIDATE_POOL
STEP7_CLEANED_ACTIVE_SET
SEARCH_STAGE_SET
AI_DIAGNOSTIC_SET
```

Every downstream row keeps deterministic lineage to RAW, but downstream tools do not need to carry duplicate RAW rows as separate semantic objects.

## 5. Work/LLM execution rule

The default Work handoff must not contain multi-megabyte raw occurrence ledgers.

Use:

```text
compact candidate table
count funnel
reason codes
family summaries
stable IDs
provenance locators
targeted raw slices only when required
```

For very large candidate sets, deterministic chunked processing is allowed only with complete row-accounting and merge QA. Representative sampling must never be described as full semantic processing.

## 6. Step7 remains the deep cleanup stage

The new early sanitation does not replace Step7.

```text
EARLY SANITATION = obvious/high-confidence mass reduction
STEP7 = nuanced relevance, ambiguity, intent/user-task and semantic QA
```

This preserves the conservative behavior learned from prior KW-001 corrections while preventing obvious duplicates/noise from consuming expensive analytical capacity.

## 7. Search/Alice scale boundary

Ordinary Search is not automatically called for every acquired/raw phrase. It is used for the retained Search-stage set and decision-relevant roots/boundaries under the current Step9 method.

Alice/GenSearch remains a bounded diagnostic/control layer. No rule introduced here bulk-runs all active phrases through Alice.

## 8. No imported KW-002 phrase cap

The KW-002 standard ceiling of 1500 delivered phrases is not a KW-001 rule.

KW-001 is a semantic rebuild/reconciliation product for an existing site. Its final active phrase count is evidence- and scope-dependent until its own commercial packaging is frozen through KW-001 productization/economics.

A final core above 1500 can be valid.

## 9. Existing jobs

A previously accepted KW-001 job is not automatically invalidated by this scalability amendment.

Mandatory application occurs for:

```text
new KW-001 jobs
jobs that materially reopen Step2/3/4/5/5A/7
future large-catalog rehearsals
```

Backfill is required only when upstream work is reopened or an independent defect demonstrates that the old volume path harmed quality/completeness.

## 10. Productization measurement addition

Future KW-001 rehearsals must record at minimum:

```text
catalog/page count relevant to acquisition
seed/probe count
raw occurrence count
normalized unique count
sanitized candidate count
Step7 active/reject/review count
Search-stage count
Search observation count
AI diagnostic count
Work/analyst burden before and after compaction
```

This measurement is required to validate that the service remains commercially executable as site size grows.

Canonical permanent gate:

`DATA_VOLUME_NORMALIZATION_AND_SANITATION_GATE.md`

Current roadmap index:

`STEP_RULES_INDEX.md`