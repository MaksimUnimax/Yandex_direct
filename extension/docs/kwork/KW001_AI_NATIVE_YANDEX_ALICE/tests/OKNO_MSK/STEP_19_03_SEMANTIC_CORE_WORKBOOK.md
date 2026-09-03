# 03 — Semantic core workbook

Status: **CLIENT PHYSICAL DELIVERABLE / MATERIALIZED DERIVED VIEW / CANONICAL SOURCES PRESERVED**  
Date: 2026-09-03  
Post-external-audit correction: **APPLIED**

## What changed after the external method audit

The first Step19 pass made a correct data-governance decision — do not create a second hand-maintained semantic truth — but implemented that principle incorrectly. It left this deliverable as a join guide that required the recipient to combine internal Step8/10/11 files manually.

That implementation is superseded.

The corrected client deliverable is the physical workbook:

```text
STEP_19_CLIENT_WORKBOOK_CORRECTED.xlsx
sheet: 03_Semantic_Core
```

The sheet contains the actual **2332 active phrase rows** materialized mechanically from the accepted canonical authorities. The client no longer needs to perform a manual JOIN to see the promised phrase → task → page map.

The canonical authorities remain:

1. `STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv` — demand/provenance lineage;
2. `STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv` — task/cluster assignment lineage;
3. `STEP_11_PHRASE_PAGE_MAP.tsv` — current accepted phrase → page/state authority.

The XLSX is explicitly a **DERIVED / MATERIALIZED client view**, not a competing source of truth. Corrections must be made upstream and the workbook regenerated.

## Correct canonicality rule

```text
DO NOT HAND-MAINTAIN A SECOND TRUTH
!=
DO NOT MATERIALIZE A CLIENT VIEW
```

Correct implementation:

```text
CANONICAL SOURCES
-> DETERMINISTIC MATERIALIZATION
-> CLIENT XLSX
-> ROW/ID/HASH QA
```

The deterministic builder is persisted as:

`step19_materialize_client_data.py`

The correction data build was independently checked in GitHub Actions run `33752050742` and persisted to the roadmap branch.

## Accounting

```text
MASTER EXACT PHRASE KEYS UPSTREAM = 2840
ACTIVE PHRASE ROWS MATERIALIZED IN XLSX = 2332
CURRENT PHRASE→PAGE ROWS MATERIALIZED = 2332
PRESERVED UNRESOLVED / SEARCH_REQUIRED = 19
SILENT ACTIVE PHRASE DROPS = 0
```

The inactive/excluded Step08 rows remain preserved upstream for auditability; they are not silently converted into active client rows.

## Materialized fields

The physical `03_Semantic_Core` sheet includes, in one filterable row-level view:

- phrase;
- observed Wordstat/provider result/association counts;
- explicit demand-semantics boundary;
- source occurrences and provenance;
- Step08 Search-stage disposition;
- Step10 assignment status/cluster/confidence/evidence lineage;
- current Step11 assignment status and cluster;
- user task / intent / business fit;
- current target URL;
- ownership state and confidence;
- mapping applicability and reason;
- correction/evidence provenance;
- explicit materialized-view status.

## Demand semantics

Provider counts remain labelled as observed counts.

```text
WORDSTAT OBSERVED COUNT
!= GUARANTEED EXACT QUERY FREQUENCY
```

They are not relabelled as exact-match frequency unless the underlying provider request actually used the required exact operator semantics.

## Page mapping semantics

`current_target_url` means the current intended SEO/page owner selected by the accepted analytical workflow. It does **not** automatically mean that Yandex Webmaster or current organic ranking has proved that same URL for every phrase.

Private Webmaster/Metrika evidence was not used in the base-public rehearsal. Where a phrase remains unresolved, the workbook preserves `SEARCH_REQUIRED` instead of manufacturing a target.

## Current architecture overlay

Implementation should be read together with:

- workbook sheet `02_Page_Model`;
- workbook sheet `05_Page_Actions`;
- workbook sheet `07_Priority_Plan`;
- workbook sheet `Execution_Calibration`;
- workbook sheet `Measurement`;
- canonical Step14/Step14A authorities for exact affected page boundaries.

Later explicit Step14A discoveries override only the governed boundaries they actually affect. Unaffected accepted decisions remain inherited.

## Client usage

The corrected usage is now:

1. Open `STEP_19_CLIENT_WORKBOOK_CORRECTED.xlsx`.
2. Use `03_Semantic_Core` directly; filter/sort the materialized rows — **no manual repo join is required**.
3. Use `02_Page_Model` for the 15-direction page-role view.
4. Use `05_Page_Actions` for the exact supported page/action changes and do-not-do boundaries.
5. Use `07_Priority_Plan` for analytical importance.
6. Use `Execution_Calibration` for the 112 exact work packages and real owner/effort/capacity calibration.
7. Use `Measurement` for implementation acceptance and future measurement routes.

## Claim boundary

This workbook is an evidence-backed semantic/page/action implementation interface. It is not a ranking guarantee, traffic forecast, revenue forecast or committed development schedule.

The implementation sequence remains `PENDING_CALIBRATION` until real owner/effort/capacity/dependency inputs are supplied.
