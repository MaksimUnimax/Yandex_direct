# Step 12 — D12-13 new-page action target disconnect

Date: 2026-08-31
Status: OPEN / discovered by fail-closed D12-11+D12-06 graph build

## What failed

The first deterministic Step-13 pair-graph run stopped before persistence with:

`RuntimeError: Hierarchy candidate page has no structural action owner: https://okno-msk.ru/uslugi/zamena-okon/`

The failure was not a harmless URL-format mismatch. Readback of `STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv` showed an internally contradictory row:

- structural unit: `WINDOW_REPLACEMENT_SERVICE`;
- action: `NEW_COMMERCIAL_PAGE`;
- primary page candidate: `https://okno-msk.ru/uslugi/ustanovka-okon/`;
- hierarchy state: `PENDING_FOR_PROPOSED_PAGE`;
- canonical new-page evidence/hierarchy candidate: `PROPOSED_NEW:/uslugi/zamena-okon/` / `https://okno-msk.ru/uslugi/zamena-okon/`.

So the action said “create a new page” while the primary destination still pointed to the existing installation page. The graph correctly refused to invent ownership for the proposed replacement page.

## Root cause

`step12_build_evidence_derived_actions_v1.py` derived `structural_action=NEW_COMMERCIAL_PAGE` from the canonical new-page evidence mapping, but copied `primary_page_candidate` from the pre-action structural-unit record. For `WINDOW_REPLACEMENT_SERVICE`, that upstream record still contained the current installation page as the best existing alternative.

The builder therefore combined two different concepts in one field:

1. the new page being proposed as the structural owner;
2. the current existing page that is the fallback/alternative today.

For most other new-page candidates, the structural-unit candidate already happened to contain `PROPOSED_NEW:...`, so the bug was latent. Replacement service exposed it.

## Why this matters

This is not only a graph-building problem. An implementation reader could see `NEW_COMMERCIAL_PAGE` but deploy changes to the wrong URL. It also disconnects the hierarchy plan from the action graph and makes downstream Step-13 pair derivation incomplete.

## Correct rule

For every structural action `NEW_COMMERCIAL_PAGE` or `NEW_INFORMATIONAL_PAGE`:

- `primary_page_candidate` MUST equal the canonical proposed page from `STEP_12_NEW_PAGE_EVIDENCE_V2.tsv`;
- the existing alternative MUST remain separate as supporting/current alternative evidence;
- the hierarchy candidate MUST resolve to at least one structural-action owner after canonical URL normalization.

Hard invariant:

```text
NEW_PAGE_ACTION
→ CANONICAL_PROPOSED_PRIMARY_TARGET
→ HIERARCHY_OWNER_EXISTS
```

and never:

```text
NEW_PAGE_ACTION
→ EXISTING_FALLBACK_PAGE_AS_PRIMARY_TARGET
```

## Required verification

The correction is not accepted until all of the following pass from saved GitHub data:

- all new-page action rows have a canonical proposed primary target;
- all five hierarchy candidate pages resolve to at least one structural-action owner;
- `WINDOW_REPLACEMENT_SERVICE` resolves to `/uslugi/zamena-okon/` rather than `/uslugi/ustanovka-okon/`;
- D12-04 evidence-derived confidence invariants still pass;
- the D12-11/D12-06 pair graph can proceed past hierarchy ownership validation;
- saved results are read back from GitHub.

## Boundary

This defect does not approve the replacement page or any other proposed page. It only restores internal consistency between the structural action, canonical proposed page, and hierarchy graph. Search-boundary/business uncertainty remains unchanged.
