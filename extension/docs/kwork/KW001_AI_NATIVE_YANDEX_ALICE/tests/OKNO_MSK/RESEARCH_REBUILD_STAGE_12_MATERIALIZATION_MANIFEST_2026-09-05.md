# Stage 12 — client data materialization manifest

**Date:** 2026-09-05  
**Materializer:** `STAGE12_MATERIALIZER_V1 / build_workbook.mjs`  
**Workbook:** `OKNO_MSK_REBUILT_RESEARCH_WORKBOOK_2026-09-05.xlsx`  
**Workbook SHA-256:** `3a5961d35df8da02b94c18914f35cf58a3c049ae95be7aed2223c32793295e07`  
**Size:** 656,682 bytes

## Canonical sources and precedence

| Authority | Revision | Stable key | Consumers |
|---|---|---|---|
| Stage 05 final semantic master | commit `a505c50b77dce02af105f48d43f30fdc66fd30e6` | `phrase_key` | Semantic Master, Summary, downstream client semantic views |
| Stage 05 canonical unit authority | commit `a505c50b77dce02af105f48d43f30fdc66fd30e6` | `structural_unit_id` | Units, Routes, architecture views |
| Stage 05 canonical action authority | commit `a505c50b77dce02af105f48d43f30fdc66fd30e6` | `action_id` | Actions, Implementation, reports |
| Stage 06 implementation specs | commit `fd6c9ea72cf2982433c4567eff865091902744cf` | `action_id` | Implementation and SEO guide |
| Stage 07 evidence register | commit `f28595830cc0bde2d3d794487d30ca229054b06f` | `evidence_id` | Evidence, AI, client explanation |

Overlay precedence is already resolved inside the Stage 05 authorities: accepted Step14A topology overlays supersede older page assignments; accepted Step20 action overlays supersede their older action descriptions. The materializer does not independently reconstruct these overlays.

## Workbook consumers

- README
- Manifest
- Summary
- Semantic Master
- Units
- Actions
- Implementation
- Evidence
- AI Cases
- Links
- Routes
- Uncertainty

## Materialization invariants

- 2,840 semantic rows are generated from one current master.
- 34 action and 34 implementation rows use one current action authority joined by `action_id`.
- 69 correction-universe rows already reconcile against their target unit contract before materialization.
- Search, AI, positive-retain and uncertainty remain distinguishable.
- 15 link rows and 46 routing rows are materialized from their accepted row-level specifications.
- NOT_READY/HOLD are not converted to READY.
- Historical client files are not overwritten.

## Verification

The workbook opens as Microsoft Excel 2007+; all 12 sheets were rendered, visually inspected, and formula-error scanned. The internal summary reconciles to canonical counts. GitHub blob readback is required before Stage 12 PASS is restored.
