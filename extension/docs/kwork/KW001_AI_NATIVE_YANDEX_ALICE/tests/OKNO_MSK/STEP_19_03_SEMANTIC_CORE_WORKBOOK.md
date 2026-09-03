# 03 — Semantic core workbook

Status: **CLIENT LOGICAL DELIVERABLE / LOSSLESS SOURCE-BUNDLE VIEW**  
Date: 2026-09-03

## What this deliverable is

The accepted semantic core is intentionally **not copied into a new manually maintained 2332-row table**. Copying the same phrase decisions into a second hand-built table would create a divergence risk and violate the Step19 canonical-data rule.

The client-facing logical workbook is therefore a lossless three-layer bundle joined by the exact `phrase` key:

1. **Demand + original provenance layer** — `STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv`
2. **Final active task/cluster assignment layer** — `STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv`
3. **Current phrase → page/state layer** — `STEP_11_PHRASE_PAGE_MAP.tsv`

These existing canonical TSVs are part of logical deliverable 03 and remain the row-level authority. This guide explains how to read them together.

## Accounting

```text
MASTER EXACT PHRASE KEYS = 2840
ACTIVE PHRASE ROWS = 2332
CURRENT PHRASE→PAGE ROWS = 2332
PRESERVED UNRESOLVED / SEARCH_REQUIRED = 19
SILENT ACTIVE PHRASE DROPS = 0
```

The inactive/excluded rows remain in the Step08 master table for auditability and are not silently deleted from history.

## Join contract

Canonical key:

```text
phrase
```

Required relationship:

```text
STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv
  phrase
  + corrected_status / corrected_reason
  + source_occurrences
  + result_occurrences / association_occurrences
  + max_result_count / max_association_count
  + source_ids / provenance
  + search_stage_disposition / next_resolution_route

JOIN phrase ->

STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv
  phrase
  + effective_intent_group
  + final_cluster_id
  + status
  + confidence
  + classification_reason / search evidence

JOIN phrase ->

STEP_11_PHRASE_PAGE_MAP.tsv
  phrase
  + effective_status
  + effective_cluster_id
  + target_page_state
  + target_url
  + ownership_confidence
  + phrase_coherence
  + correction_source
  + reason
  + lineage_status
```

For active phrases, the Step11 row is the current page/state authority when an older cluster-level representation conflicts with it.

## Demand semantics

`max_result_count`, `max_association_count` and related fields are preserved as the observed Wordstat/provider counts from the accepted acquisition/cleanup lineage.

They are **not relabelled as exact-match frequency** unless the underlying provider request actually used exact operator semantics. Client interpretation should therefore be:

```text
DEMAND SIGNAL / WORDSTAT OBSERVED COUNT
!= GUARANTEED EXACT QUERY FREQUENCY
```

## Page mapping semantics

`target_url` means the intended current SEO/page owner selected by the accepted analytical workflow. It does **not** automatically mean that Yandex Webmaster or current organic ranking proved the same URL for that phrase.

Where the state is unresolved, the workbook preserves the unresolved state instead of manufacturing a page.

## Current architecture overlay

Page/action implementation should be read together with:

- `STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE.tsv`
- `STEP_14A_ARCHITECTURE_DELTA.tsv`
- `STEP_19_05_PAGE_ACTION_MAP.tsv`

Step14A later current-site discoveries override only the explicitly affected page/task boundaries. Unaffected accepted phrase mappings remain inherited.

## Client usage

For semantic/content implementation:

1. Start with `STEP_11_PHRASE_PAGE_MAP.tsv` to see the current page/state for every active phrase.
2. Join by exact `phrase` to `STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv` for task/cluster context.
3. Join by exact `phrase` to `STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv` for accepted demand/provenance context.
4. Use `STEP_19_05_PAGE_ACTION_MAP.tsv` for what should actually be changed.
5. Use `STEP_19_07_PRIORITY_ACTION_PLAN.tsv` for analytical importance and calibration status.

## Claim boundary

This workbook is an evidence-backed semantic/page map. It is not a ranking guarantee, traffic forecast, revenue forecast, or committed development schedule.
