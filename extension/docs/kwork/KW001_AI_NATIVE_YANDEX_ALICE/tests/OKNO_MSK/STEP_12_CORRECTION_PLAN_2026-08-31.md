# OKNO-MSK — Step 12 correction plan after external audit

Date: 2026-08-31  
Status: **CORRECTION REQUIRED / EXECUTION IN PROGRESS**

This job-specific plan is created **before changing the first-pass Step-12 result**. Its purpose is to preserve what went wrong, why it happened and the exact order of repair so the correction is causal rather than a sequence of cosmetic edits.

Canonical reusable method being rewritten in parallel:

```text
../../STEP_12_STRUCTURAL_ACTION_METHOD.md
```

Independent audit authority:

```text
STEP_12_EXTERNAL_METHOD_AUDIT_2026-08-31.md
```

## Why the previous PASS is withdrawn

The first Step-12 run produced useful output and preserved every phrase, but the external audit showed that the final acceptance was stronger than the evidence. Therefore the historical artifacts remain as a first-pass record, but they are no longer the accepted final Step-12 truth until this correction finishes.

```text
HISTORICAL_FIRST_PASS = PRESERVE
HISTORICAL_PASS = WITHDRAWN
CURRENT_STEP12_STATE = CORRECTION_REQUIRED
STEP13 = BLOCKED
```

## Correction item 1 — replace hidden lexical overrides with explicit structural subunits

### First-run behavior

191 phrases were redirected by `route_override()` using substring tests. This included finance, calculator, private-house, P-44, aluminium opening modes, veranda warm/cold, PVC-door subtypes, REHAU models and accessories.

### Why this is insufficient

A token can identify a candidate subtask but does not prove the primary page role. The architecture must expose the subtask itself and its grouped phrases.

### Repair

Build `STEP_12_STRUCTURAL_UNITS.tsv` from the phrase map. Every previous override must either:

```text
become a named structural unit with all member phrases + task + target evidence;
return to its parent unit if the override is not justified;
or become explicit unresolved/deferred evidence work.
```

No final phrase route may depend on a hidden runtime substring rule.

## Correction item 2 — re-audit mixed units before any new-page decision

Mandatory re-audit targets discovered so far:

```text
WINDOW_INSTALLATION_DIY_INFO
PANORAMIC_WINDOWS_COMMERCIAL
GLAZING_PERMISSION_INFO
WOOD_WINDOWS_COMMERCIAL
WINDOW_HARDWARE_INFO
WINDOW_REPAIR_DIY_INFO
```

Additional mixed units discovered during correction must be added rather than ignored because they were absent from this initial list.

### Repair

Create `STEP_12_STRUCTURAL_UNIT_CORRECTIONS.tsv` with original unit, phrase, corrected unit/state, reason and evidence. Preserve the historical Step-11/first-pass Step-12 values.

## Correction item 3 — materialize demand/Search evidence for every new-page candidate

Create `STEP_12_NEW_PAGE_EVIDENCE.tsv` for every surviving candidate. Use already saved Wordstat/Search evidence first.

Required questions:

```text
What demand is actually present?
Which phrases carry it?
What is the representative/aggregate frequency evidence available?
What ordinary Search evidence exists for the page boundary?
What result/page types are observed?
Does current business evidence confirm the offered product/service?
Could an existing page be expanded instead?
```

Only a specifically named unresolved gap may justify another Bridge request, and only after the owner-visible YMB gate.

## Correction item 4 — replace default HIGH confidence

Remove `confidence='HIGH'` as a default decision mechanism.

For every final action derive and preserve:

```text
TASK_COHERENCE
BUSINESS_TRUTH
CURRENT_PAGE_FIT
DEMAND_SUPPORT
SEARCH_BOUNDARY_SUPPORT
HIERARCHY_CLARITY
FINAL_CONFIDENCE
CONFIDENCE_DOWNGRADE_REASON
```

A missing material dimension must lower confidence or make the action provisional.

## Correction item 5 — rebuild QA so it verifies instead of self-certifying

Remove hard-coded pass facts and false proxies.

Every QA item must be marked as:

```text
COMPUTED_FROM_DATA
VERIFIED_FROM_PROVENANCE
MANUAL_REVIEW_LEDGER
```

Create `STEP_12_QA_REVIEW_LEDGER.tsv` for semantic checks that cannot be proven by arithmetic.

SPLIT/MERGE must be allowed when justified; QA counts **unsupported** split/merge rows, not all split/merge rows.

## Correction item 6 — derive Step-13 candidate pairs from the actual routing graph

Generate `STEP_12_STEP13_CANDIDATE_PAIRS.tsv` from final structural units/pages. This file is only a universe of possible overlap checks and must not contain a cannibalization verdict.

## Correction item 7 — finish the hierarchy for accepted new pages

Create `STEP_12_HIERARCHY_PLAN.tsv` with:

```text
new/proposed page
parent page/section
inbound link sources
anchor/link concept
outbound supporting links
commercial handoff for informational content
breadcrumb/navigation role
```

## Correction item 8 — finish routing useful phrases from NO_STANDALONE_PAGE units

For every no-page unit, inspect every member phrase and prove that it is either:

```text
routed to another valid page/section;
placed in another explicit structural unit;
deferred with a named missing evidence reason;
or genuinely outside scope.
```

No useful phrase may remain stranded merely because its original group should not become a page.

## Correction item 9 — rescue misassigned in-scope phrases from rejected groups

Known example:

```text
"пластиковые окна в деревянном доме"
```

must not remain trapped in a rejected wooden-window-product unit. Similar rows must be found systematically, not only by the known example.

## Correction item 10 — separate phrase count from demand

Phrase count remains a coverage statistic only. New-page narratives such as "large task" must cite actual demand evidence rather than row count.

## Correction item 11 — make provisional dependencies explicit

A structural action that still depends on Step-13 conflict testing must be marked provisional rather than presented as final implementation truth.

Allowed recommendation maturity:

```text
FINAL_WITHIN_STEP12_EVIDENCE
PROVISIONAL_PENDING_STEP13_CONFLICT_CHECK
DEFERRED_PENDING_MISSING_EVIDENCE
```

## Correct repair order

The order is deliberately dependency-based:

```text
1. Freeze historical first-pass artifacts.
2. Mark Step12 as correction-required and block Step13.
3. Build complete phrase working view from accepted upstream data.
4. Re-audit mixed units and create explicit semantic/structural corrections.
5. Convert lexical overrides into explicit structural subunits.
6. Verify business truth for all commercial/service units.
7. Re-evaluate existing-page fit after the corrected unit boundaries exist.
8. Attach Wordstat demand evidence to page candidates.
9. Attach ordinary Search evidence where it can change the page boundary.
10. Re-decide structural actions by comparing alternatives.
11. Derive confidence and provisional/final maturity from evidence.
12. Build hierarchy/internal-link plans for accepted new pages.
13. Materialize 2332/2332 phrase -> structural unit -> action/page/state rows.
14. Generate complete Step13 candidate page-pair universe.
15. Run independent arithmetic + semantic QA from real data/review ledgers.
16. Persist all corrected artifacts to GitHub and read them back.
17. Only then restore Step12 COMPLETE and allow Step13.
```

### Why this order cannot be shortened mechanically

Demand should not be aggregated before mixed units are corrected, because otherwise different tasks are measured together. Page selection should not be finalized before business truth and demand are known. Confidence should not be chosen before evidence is assembled. QA should not run before the final map exists. Step 13 should not start before Step 12 supplies the full candidate-pair universe.

## Plain-language summary

### Why this correction exists

The first Step 12 produced a useful draft, but some decisions were made too quickly: matching words were sometimes used as if they proved the right page, some mixed groups were treated as one topic, and the checking script partly certified assumptions that it had itself created.

### What will be done

We will first repair the groups of searches so each one means one understandable user task, then check the real demand and existing pages, and only after that decide whether to keep, improve or create a page. Every new page will have to prove why it is useful and where it belongs on the site.

### What the corrected result must give us

A complete plan for all searches in which every recommendation can be explained from evidence, uncertainty is visible instead of hidden, and the next step receives a complete list of page pairs that genuinely need a separate search-conflict check.

## Correction item 12 — do not blindly inherit OUTSIDE when site evidence contradicts it

### What exposed the problem

The full correction review found phrases marked outside/no-page even though the persisted site inventory shows a matching current offer/page. The clearest example is blinds: the site inventory contains an existing blinds page while the entire curtains/blinds cluster had been inherited as outside scope. Other mixed outside/no-page groups also contain salvageable glazing/window-use-case phrases.

### Why this matters

An upstream status is historical evidence, not permission to ignore newer contradictory evidence. If the site actually offers the thing and the phrase asks for that thing, the current step must surface the contradiction and create a correction overlay instead of preserving a false outside label for convenience.

### Repair

Re-audit every historical OUTSIDE/NO_STANDALONE phrase against the verified site inventory. Preserve the old state for provenance, but materialize every in-scope correction and prove that no verified-offer phrase remains stranded.
