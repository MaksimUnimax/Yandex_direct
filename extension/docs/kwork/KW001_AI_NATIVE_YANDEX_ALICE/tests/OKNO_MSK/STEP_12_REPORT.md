# Step 12 — Structural actions report

Date: 2026-08-31
Status: **PASS AFTER THIRD EXTERNAL METHOD AUDIT + D12-27 PHRASE-LEVEL REVALIDATION + INDEPENDENT QA**

## Plain-language result
Step 12 decides what the site should actually do with current pages: keep their role, expand them, add a section, route a subtask elsewhere, defer, or avoid unsupported pages. The third audit added explicit gap diagnosis, performance-evidence boundaries, intended-vs-Yandex-observed URL state, SERP result-type provenance, owner-goal source strength and implementable internal links. A later evidence-first review then exposed two residual mixed units; all 65 affected phrases were rechecked before final closure.

## D12-27 correction
- reviewed phrases: **65**
- reassigned phrases: **20**
- French commercial core after review: **42** phrases
- generic accessories core after review: **3** phrases
- zero-member active structural units: **0**

## Current action distribution
```text
ADD_SECTION_OR_FAQ_TO_EXISTING = 12
DEFER_PENDING_EVIDENCE = 10
EXPAND_EXISTING_PAGE = 8
KEEP_EXISTING_STRUCTURE = 64
NO_STANDALONE_PAGE = 13
OUTSIDE_SCOPE_NO_ACTION = 7
ROUTE_TO_EXISTING_PAGE_AS_SUBTASK = 46
```

## Evidence boundaries added in the third audit
- gap types: {'NONE': 130, 'QUALITY_GAP': 20, 'EVIDENCE_INSUFFICIENT': 10}
- intended-vs-Yandex relevant state: {'NOT_APPLICABLE_NO_INTENDED_TARGET': 28, 'NOT_DIRECTLY_CHECKED': 110, 'SITE_NOT_OBSERVED': 22}
- direct persisted SERP evidence attached to units: 33
- owner-goal evidence sources: {'UNKNOWN': 23, 'PUBLIC_SITE_INFERRED': 116, 'NOT_APPLICABLE': 7, 'PUBLIC_SITE_EXPLICIT': 14}
- performance evidence missing fields: 0; base package still has no Webmaster/Metrika account-performance evidence
- structural KEEP does **not** mean no optimization is needed
- material existing-page internal-link units: 66; implementable links: 28

## Downstream Step-13 handoff
- candidate page pairs: **189**
- pairs requiring future direct Step-13 Search check: **171**
- structural units with Step-13 dependency: **108**
- pair missing / extra / duplicates: **0 / 0 / 0**
- pair search-flag/reason mismatches: **0 / 0**
- Step 13 executed: **false**

## Final accounting
```text
SOURCE_ACTIVE_PHRASES = 2332
FINAL_PHRASE_ACTION_ROWS = 2332
ASSIGNED = 2313
SEARCH_REQUIRED = 19
STRUCTURAL_UNITS = 160
TRACKED_DEFECTS = 27
VERIFIED_FIXED = 27
OPEN_DEFECTS = 0
NEW_PAGE_ACTIONS = 0
PROPOSED_NEW_REFS = 0
INDEPENDENT_FINDINGS = 0
NEW_BRIDGE_REQUESTS = 0
NEW_BRIDGE_COST_RUB = 0.0
STEP13_EXECUTED = false
```

## Canonical current artifacts
```text
STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V6.tsv
STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V5.tsv
STEP_12_PHRASE_ACTION_MAP_FINAL_V5.tsv
STEP_12_INTERNAL_LINK_ACTIONS_V5.tsv
STEP_12_STEP13_CANDIDATE_PAIRS_V5.tsv
STEP_12_D12_27_PHRASE_RESOLUTIONS.tsv
STEP_12_THIRD_AUDIT_STRONG_FIT_PAGE_RECHECK.tsv
STEP_12_D12_27_INDEPENDENT_QA.json
STEP_12_QA.json
STEP_12_CORRECTION_DEFECT_LEDGER.tsv
STEP_12_CORRECTION_CURRENT_STATE.json
```

Historical V1–V4 outputs remain provenance only where they conflict with V5/V6.
