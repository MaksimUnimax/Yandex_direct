# Step 12 — Structural actions report

Date: 2026-08-31
Status: **PASS AFTER SECOND EXTERNAL METHOD AUDIT + OWNER-GOAL / CURRENT-SITE FRESHNESS / CONTENT-REUSE CORRECTION + INDEPENDENT QA**

## Plain-language result

Step 12 answers what the site should actually change. The second audit materially changed the answer: the previous corrected pass was still too SEO-centric. It could prove search demand and page structure while missing a current existing page or recommending informational content that works against a paid service.

The live site was therefore rechecked for all five former new-page concepts. All five CREATE concepts were withdrawn. Current architecture now reuses/expands current pages and content instead of proposing new URLs.

## Why the previous corrected pass was still wrong

The analyst had read correct external sources before the step, but some findings remained narrative guidance instead of executable gates. In particular, the workflow did not fail when a CREATE lacked a fresh immediately-before-CREATE current-site check, and it did not have explicit owner-goal/business-potential/content-role fields. Therefore `correct research` did not guarantee `correct execution`.

Permanent lesson:

```text
CORRECT_RESEARCH != EXECUTABLE_CONTROL
BUSINESS_TRUTH != OWNER_BUSINESS_GOAL_ALIGNMENT
PAGE_OWNERSHIP_GAP != CURRENT_CONTENT_GAP
OLD_INVENTORY_ABSENCE != CURRENT_PAGE_ABSENCE
```

The reusable method now converts these principles into mandatory stages, evidence fields and fail-closed QA.

## Second-audit defects

- **D12-16** — false panoramic CREATE; exact live commercial panoramic page existed.
- **D12-17** — neutral DIY-installation article conflicted with the site's professional-installation business outcome and explicit anti-DIY positioning.
- **D12-18** — broad DIY repair/adjustment CREATE ignored existing self-help content plus the paid repair handoff.
- **D12-19** — second false CREATE: current replacement-in-apartment commercial page already existed.
- **D12-20** — broad hardware guide confused lack of one exact owner with lack of content; existing choose-windows guide already contains substantive hardware selection plus specialist pages.

All tracked defects D12-01..D12-20 are now VERIFIED_FIXED.

## Recommendation delta

```text
STRUCTURAL_UNITS = 160
CHANGED_UNITS_VS_PREVIOUS_V2 = 16
ACTION_CHANGED_UNITS = 12
PRIMARY_TARGET_CHANGED_UNITS = 11
SUPPORTING_TARGET_CHANGED_UNITS = 9
MATURITY_CHANGED_UNITS = 2
CONFIDENCE_CHANGED_UNITS = 0
FORMER_UNIQUE_PROPOSED_NEW_PAGES = 5
CURRENT_UNIQUE_PROPOSED_NEW_PAGES = 0
FORMER_NEW_COMMERCIAL_ACTION_ROWS = 2
CURRENT_NEW_COMMERCIAL_ACTION_ROWS = 0
FORMER_NEW_INFORMATIONAL_ACTION_ROWS = 4
CURRENT_NEW_INFORMATIONAL_ACTION_ROWS = 0
FORMER_PROPOSED_NEW_REFERENCE_ROWS = 14
CURRENT_PROPOSED_NEW_REFERENCE_ROWS = 0
```

Current action distribution:

```text
{
  "ADD_SECTION_OR_FAQ_TO_EXISTING": 12,
  "DEFER_PENDING_EVIDENCE": 10,
  "EXPAND_EXISTING_PAGE": 14,
  "KEEP_EXISTING_STRUCTURE": 58,
  "NO_STANDALONE_PAGE": 13,
  "OUTSIDE_SCOPE_NO_ACTION": 7,
  "ROUTE_TO_EXISTING_PAGE_AS_SUBTASK": 46
}
```

## Five former new-page concepts — final current recommendation

1. **Panoramic windows** — no new `/panoramnye-okna/`. Use current `https://okno-msk.ru/okna-rehau/panoramnoe-osteklenie/`; related article/object pages remain supporting/current owners.
2. **Window replacement** — no new `/uslugi/zamena-okon/`. Expand/use current `https://okno-msk.ru/okna-rehau/po-tipu-doma/zamena-okon-v-kvartire/`; installation remains supporting.
3. **DIY installation** — no neutral step-by-step DIY article. Expand professional installation page with requirements, risks, preparation, common errors and reasons to use qualified installation.
4. **DIY repair + adjustment** — no broad new article. Keep current adjustment/operation self-help for low-risk cases and connect complex issues to paid repair.
5. **Hardware guide** — no new broad guide. Expand current `kak-vybrat-plastikovye-okna` hardware section and route specialist component needs to existing accessory/service pages.

## Current-site freshness control and tools

Universal authority: `../../CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`.

- A small named **positive existence** check can be done by ChatGPT public web: open/read the current first-party page.
- A material **negative existence** claim on a large site should use broad Codex/browser discovery plus targeted ChatGPT current-page read/cross-check.
- If broad discovery is unavailable and absence cannot be proved, use DEFER/ABSENCE_NOT_PROVEN instead of confident CREATE/no-page truth.

This gate now applies to Steps 1, 11, 12, 13, 14 and 20 at different depths.

## Final current accounting

```text
SOURCE_ACTIVE_PHRASES = 2332
FINAL_PHRASE_ACTION_ROWS = 2332
ASSIGNED = 2313
SEARCH_REQUIRED = 19
STRUCTURAL_UNITS = 160
STRUCTURAL_ACTION_ROWS = 160
CURRENT_NEW_PAGES = 0
CURRENT_STEP13_CANDIDATE_PAIRS = 178
PAIRS_REQUIRING_FUTURE_SEARCH_CHECK = 160
STEP13_DEPENDENCY_UNITS = 105
INDEPENDENT_SECOND_AUDIT_FINDINGS = 0
PAIR_MISSING_EXTRA_DUPLICATE = 0/0/0
BUSINESS_FRESHNESS_MISSING_ROWS = 0
STEP13_EXECUTED = false
NEW_BRIDGE_REQUESTS = 0
NEW_BRIDGE_COST_RUB = 0.0
```

## Canonical current artifacts

```text
STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv
STEP_12_STRUCTURAL_UNITS_V5.tsv
STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V3.tsv
STEP_12_PHRASE_ACTION_MAP_FINAL_V3.tsv
STEP_12_SECOND_AUDIT_FRESHNESS_EVIDENCE.tsv
STEP_12_POST_CLOSE_CURRENT_SITE_BUSINESS_CORRECTIONS.tsv
STEP_12_FORMER_NEW_PAGE_CONCEPTS_SECOND_AUDIT.tsv
STEP_12_SECOND_AUDIT_ACTION_DELTA.tsv
STEP_12_STEP13_CANDIDATE_PAIRS_V3.tsv
STEP_12_MATURITY_DEPENDENCY_LEDGER_V3.tsv
STEP_12_SECOND_AUDIT_INDEPENDENT_QA.json
STEP_12_SECOND_AUDIT_QA_FINDINGS.tsv
STEP_12_QA.json
STEP_12_REPORT.md
STEP_12_SECOND_AUDIT_FINAL_ACCEPTANCE_2026-08-31.md
STEP_12_CORRECTION_DEFECT_LEDGER.tsv
STEP_12_CORRECTION_CURRENT_STATE.json
```

Historical V1/V2/new-page evidence/hierarchy artifacts remain as provenance and are superseded where they conflict with V3.

**Step 12 is complete as a closure candidate. Step 13 has not been started. Durable closure requires GitHub readback and final status synchronization.**
