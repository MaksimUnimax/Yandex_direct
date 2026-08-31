# Step 12 — Structural actions report

Date: 2026-08-31
Status: **PASS AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA**

## Executive result

Step 12 is complete. The historical first-pass `PASS_AFTER_FULL_STRUCTURAL_ACTION_AUDIT` is preserved only as superseded provenance and is **not** the current acceptance authority.

The corrected final authority is based on explicit structural units, phrase-level materialization, evidence-derived confidence/maturity, implementable hierarchy, a deterministic Step-13 candidate-pair handoff, and independent QA that is computed from persisted source artifacts rather than self-asserted constants.

Step 13 is **NOT STARTED**. It is only the next allowed major step and still requires its own pre-step methodology research/review before execution.

## Final accounting

```text
SOURCE_ACTIVE_PHRASES = 2332
FINAL_PHRASE_ACTION_MAP_ROWS = 2332
ASSIGNED_TO_STRUCTURAL_UNITS = 2313
SEARCH_REQUIRED / DEFER_UNRESOLVED = 19
FINAL_STRUCTURAL_UNITS = 160
FINAL_STRUCTURAL_ACTION_ROWS = 160
UNIQUE_PROPOSED_NEW_PAGES = 5
HIERARCHY_CANDIDATE_PAGES_MATERIALIZED = 5/5
CURRENT_DERIVED_STEP13_CANDIDATE_PAIRS = 189
PAIRS_REQUIRING_FUTURE_DIRECT_STEP13_SEARCH_CHECK = 171
STRUCTURAL_UNITS_WITH_STEP13_DEPENDENCY = 107
INDEPENDENT_QA_CHECKS = 46/46 PASS
INDEPENDENT_QA_FINDINGS = 0
MANUAL_SEMANTIC_REVIEW_CASES = 10/10 PASS
SPLIT_MERGE_REGRESSION_CASES = 4/4 PASS
ACTUAL_SPLIT_ROWS = 0
ACTUAL_MERGE_ROWS = 0
UNSUPPORTED_SPLIT_ROWS = 0
UNSUPPORTED_MERGE_ROWS = 0
QA_SELF_ASSERTED_PASS_FIELDS = 0
IMPLEMENTABLE_ACTIONS_WITH_BLANK_PRIMARY_TARGET = 0
STALE_MATERIALIZED_HIERARCHY_REASONS = 0
STEP13_EXECUTED = false
NEW_BRIDGE_REQUESTS_DURING_FINAL_CORRECTION = 0
NEW_BRIDGE_COST_RUB_DURING_FINAL_CORRECTION = 0.0
```

The current `189` pair count is a **derived property of this corrected routing graph**, not a hard-coded target or reusable threshold. Independent QA rebuilds the expected pair universe from V1 routing inputs and hierarchy edges and checks missing/extra/duplicate pairs.

## Why the historical Step-12 pass was withdrawn

The first pass produced useful broad structural ideas but overclaimed certainty. The external audit and fail-closed correction sequence identified fifteen tracked defects (`D12-01` through `D12-15`). All are now `VERIFIED_FIXED` in `STEP_12_CORRECTION_DEFECT_LEDGER.tsv`.

The most important corrected failure classes were:

- hidden lexical routing overrides instead of explicit user-task structural units;
- mixed semantic units surviving a phrase-list review;
- new-page recommendations without a dedicated demand/Search evidence matrix;
- default HIGH confidence;
- QA that self-certified desired constants and incorrectly treated all SPLIT/MERGE as errors;
- manually selected Step-13 follow-up instead of a complete derived routing graph;
- incomplete new-page hierarchy;
- useful phrases stranded inside rejected/no-page/outside groups;
- phrase count used as a demand proxy;
- Step-13 dependencies hidden behind final-looking recommendations;
- new-page action targets disconnected from the canonical proposed page;
- implementable actions with no primary target;
- stale confidence explanations after hierarchy was already materialized.

Several correction workflows intentionally failed before persistence or before acceptance. Those failures were not bypassed; they exposed the next inconsistency and the method was corrected before rerun.

## Final structural action model

The final action table is `STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv`. Every row exposes explicit evidence dimensions, current hierarchy state, recommendation maturity, confidence, and any derived Step-13 dependency.

Current action counts by structural unit:

```text
{
  "ADD_SECTION_OR_FAQ_TO_EXISTING": 8,
  "DEFER_PENDING_EVIDENCE": 10,
  "EXPAND_EXISTING_PAGE": 12,
  "INCLUDE_AS_SECTION_IN_PROPOSED_PAGE": 5,
  "KEEP_EXISTING_STRUCTURE": 55,
  "NEW_COMMERCIAL_PAGE": 2,
  "NEW_INFORMATIONAL_PAGE": 4,
  "NO_STANDALONE_PAGE": 13,
  "OUTSIDE_SCOPE_NO_ACTION": 7,
  "ROUTE_TO_EXISTING_PAGE_AS_SUBTASK": 44
}
```

Current confidence distribution:

```text
{
  "HIGH": 29,
  "LOW": 12,
  "MEDIUM": 119
}
```

Current maturity distribution:

```text
{
  "DEFERRED_PENDING_MISSING_EVIDENCE": 12,
  "FINAL_WITHIN_STEP12_EVIDENCE": 43,
  "PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK": 105
}
```

A Step-13 dependency cannot remain `HIGH` or `FINAL_WITHIN_STEP12_EVIDENCE`. Independent QA found both contradiction counts equal to zero.

## Proposed new-page concepts

The correction preserves five unique proposed page concepts, but Step 12 does **not** pretend that all five are final architecture. Their current evidence/gap state remains explicit:

- `PANORAMIC_WINDOWS_COMMERCIAL` → `PROPOSED_NEW:/panoramnye-okna/` — evidence maturity `PROVISIONAL_PENDING_SEARCH_BOUNDARY`; Search boundary: `MATERIAL_SEARCH_PAGE_BOUNDARY_NOT_DIRECTLY_PROBED`.
- `WINDOW_HARDWARE_GUIDE` → `PROPOSED_NEW:/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/` — evidence maturity `PROVISIONAL_PENDING_SEARCH_BOUNDARY`; Search boundary: `MATERIAL_SEARCH_PAGE_BOUNDARY_NOT_DIRECTLY_PROBED`.
- `PVC_WINDOW_INSTALLATION_DIY_GUIDE` → `PROPOSED_NEW:/stati/ustanovka-plastikovyh-okon-svoimi-rukami/` — evidence maturity `EVIDENCE_SUPPORTED_PENDING_ACTION_REEVALUATION`; Search boundary: `NO_GAP_FOR_OBSERVED_CORE_QUERIES__DO_NOT_TRANSFER_TO_UNPROBED_PHRASES`.
- `PVC_WINDOW_REPAIR_DIY_GUIDE` → `PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/` — evidence maturity `PROVISIONAL_PENDING_SEARCH_BOUNDARY`; Search boundary: `MATERIAL_SEARCH_PAGE_BOUNDARY_NOT_DIRECTLY_PROBED`.
- `WINDOW_REPLACEMENT_SERVICE` → `PROPOSED_NEW:/uslugi/zamena-okon/` — evidence maturity `PROVISIONAL_PENDING_SEARCH_BOUNDARY`; Search boundary: `MATERIAL_SEARCH_PAGE_BOUNDARY_NOT_DIRECTLY_PROBED`.

The hierarchy plan materializes parent/navigation placement plus mandatory inbound/outbound routes for all five. A good hierarchy does not erase a Search/business boundary gap.

## D12-14 — four missing-target actions resolved from evidence

The first independent D12-05 audit found four implementable actions with blank primary targets. They were not repaired by copying the nearest supporting URL. A dedicated phrase/page evidence packet was built first, then each case was resolved:

- `PVC_DOOR_INSTALLATION_SERVICE` → `ADD_SECTION_OR_FAQ_TO_EXISTING` → `https://okno-msk.ru/dveri-rehau/`. No standalone PVC-door-installation owner is verified, but Step11 explicitly records that current door pages bundle installation with product purchase. The implementable recommendation is therefore a clear installation/price section or FAQ on the existing door hub, not a new service landing.
- `PVC_WINDOW_OPERATION_DIY` → `INCLUDE_AS_SECTION_IN_PROPOSED_PAGE` → `PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/`. The single operation question “как открыть пластиковое окно” is adjacent to troubleshooting but Step11 found no current owner. It belongs as a narrow section in the already evidenced DIY repair/adjustment guide; the professional repair page is supporting/fallback, not the primary informational answer.
- `REHAU_OTHER_BRAND_COMPARISON_INFO` → `DEFER_PENDING_EVIDENCE` → `NO TARGET / DEFERRED`. Step11 explicitly says no current KBE/Melke-vs-Rehau owner was verified and not to force these queries onto the generic Rehau hub. With zero direct Step09 member queries, neither an existing-section target nor a new standalone comparison page is evidence-backed yet.
- `WINDOW_DEMOLITION_SERVICE` → `ADD_SECTION_OR_FAQ_TO_EXISTING` → `https://okno-msk.ru/uslugi/ustanovka-okon/`. Step11 explicitly records demolition as a sub-step of installation rather than a standalone service owner. The installation service page is therefore the truthful implementation destination for dismantling/demolition scope and price/process explanation.

The notable deliberate non-target is `REHAU_OTHER_BRAND_COMPARISON_INFO`: because Step 11 explicitly warned not to force KBE/Melke-vs-Rehau queries onto the generic Rehau hub and there was no direct Step-9 member evidence, the action is `DEFER_PENDING_EVIDENCE`, blank target, LOW confidence.

## D12-15 — confidence explanations regenerated from current state

After hierarchy and pair/dependency overlays, the human-readable confidence reason is regenerated from the **current** evidence dimensions for all 160 rows. Resolved hierarchy is no longer listed as a missing condition. Real Search, business-truth or Step-13 uncertainty remains visible where applicable.

Independent QA result: `stale_materialized_hierarchy_reason_rows = 0`.

## D12-05 — independent QA and correct SPLIT/MERGE semantics

The canonical QA is no longer the builder's own declaration. `step12_independent_final_qa.py` independently recomputes material properties from persisted source artifacts. Every check records one allowed evidence origin:

```text
COMPUTED_FROM_DATA
VERIFIED_FROM_PROVENANCE
MANUAL_REVIEW_LEDGER
```

The four explicit SPLIT/MERGE controls prove both sides of the rule:

- a supported independent logical split must pass;
- a modifier-only split must fail;
- a same-task structurally redundant merge with evidence must pass;
- a merge justified only by suspected cannibalization must fail.

Therefore QA counts **unsupported** SPLIT/MERGE actions, not all SPLIT/MERGE actions. In this current job there are no final SPLIT/MERGE actions, and unsupported counts are `0/0`; the positive controls prove that zero is not forced by the evaluator.

The pair-universe QA was also corrected from a historical literal count to dynamic set recomputation. Structured JSON readback is parsed as JSON rather than validated by grep-count heuristics. Diagnostics are persisted before the final gate, so a failed run cannot erase the evidence that explains the failure.

## Step-13 handoff — candidate universe only

`STEP_12_STEP13_CANDIDATE_PAIRS.tsv` currently contains `189` derived page pairs. `171` require a future direct Step-13 Search check under the current derivation rules, and `107` structural units visibly carry a Step-13 dependency.

These are **candidate overlap/conflict checks, not cannibalization verdicts**. The pair ledger contains no harmful-cannibalization verdict column/cell and no `STEP_13_*` execution artifact exists in the job workspace.

## Canonical final artifacts

```text
STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv
STEP_12_STRUCTURAL_UNITS_V5.tsv
STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv
STEP_12_PHRASE_ACTION_MAP_FINAL.tsv
STEP_12_NEW_PAGE_EVIDENCE_V2.tsv
STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv
STEP_12_STEP13_CANDIDATE_PAIRS.tsv
STEP_12_MATURITY_DEPENDENCY_LEDGER.tsv
STEP_12_D12_14_TARGET_RESOLUTIONS.tsv
STEP_12_QA_REVIEW_LEDGER.tsv
STEP_12_QA_CHECKS.tsv
STEP_12_QA_REVIEW_RESULTS.tsv
STEP_12_SPLIT_MERGE_REGRESSION_RESULTS.tsv
STEP_12_QA_FINDINGS.tsv
STEP_12_QA.json
STEP_12_REPORT.md
STEP_12_CORRECTION_DEFECT_LEDGER.tsv
STEP_12_CORRECTION_CURRENT_STATE.json
```

Historical first-pass artifacts remain for provenance but are superseded where they conflict with these corrected authorities.

## Plain-language result

Step 12 now answers the practical website question without pretending uncertainty has disappeared: which existing page should remain or receive more content, where a new page is justified as a candidate, which ideas should not become standalone URLs, and which unresolved tasks must wait for more evidence.

The correction also changes how trustworthy the output is. Every active phrase is carried through to a final action/unresolved state, page actions have destinations, new pages have a real place in the site, confidence describes current evidence rather than a default, and the next-step overlap universe is generated from the actual routing graph rather than analyst memory.

**Step 12 is complete. Step 13 has not been started.**
