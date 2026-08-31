# Step 12 — evidence-derived confidence acceptance

Date: 2026-08-31
Scope: D12-04 only. Step 12 remains in correction.

## What failed in the first run

`confidence='HIGH'` was the default constructor value. That made confidence describe whether the analyst remembered to downgrade a row, not how strong the evidence was.

## Corrected implementation

`STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv` derives every row from explicit dimensions:

```text
TASK_COHERENCE
BUSINESS_TRUTH
CURRENT_PAGE_FIT
DEMAND_SUPPORT
SEARCH_BOUNDARY_SUPPORT
HIERARCHY_CLARITY
RECOMMENDATION_MATURITY
```

The confidence field is generated only after these fields exist. No action is assigned HIGH as a constructor/default value.

## Mechanical QA readback

```text
STRUCTURAL_UNITS = 160
DEFAULT_HIGH_CONFIDENCE_USED = false
ROWS_WITHOUT_EVIDENCE_DIMENSIONS = 0
HIGH = 71
MEDIUM = 80
LOW = 9
NEW_PAGE_HIGH_WITH_MATERIAL_SEARCH_GAP = 0
CONDITIONAL_BUSINESS_HIGH_COMMERCIAL_CREATE = 0
UNRESOLVED_ACTION_ROWS = 0
```

The distribution itself is not the proof; the important checks are the absence of default HIGH and the inability of a row with a material missing boundary to become HIGH.

## Manual challenge examples

### Panoramic commercial candidate

Result: `MEDIUM`.

Why:
- coherent corrected commercial core;
- strong direct Wordstat support;
- broad product offer is still conditional rather than fully proven as a standalone family;
- no direct Step-9 core page-boundary probe;
- hierarchy was still pending at this stage.

This is the expected behavior: strong demand does not erase missing page-boundary/business evidence.

### Window replacement service candidate

Result: `MEDIUM`.

Why:
- coherent service task and strong demand;
- current installation workflow supports replacement activity;
- standalone replacement-service role is conditional;
- direct Search page boundary is not probed;
- proposed page hierarchy was pending.

### Hardware guide candidate

Result: `MEDIUM`.

Why:
- corrected guide core has only partial direct demand support compared with other candidates;
- generic reviews were removed from the core;
- no direct Step-9 core query remains;
- proposed hierarchy was pending.

### Existing exact product/service pages

Rows such as existing balcony/PVC-door/product/service pages may receive `HIGH` when:
- the task is coherent;
- current business/page fit is strong;
- the action is simply to preserve the already verified page;
- no material unresolved Search boundary is needed for that exact structural role.

This explains why lack of a fresh Search probe does not mechanically cap every existing-page KEEP at MEDIUM: direct Search is required when it can change the page boundary, not as ritual evidence for every obvious current owner.

### Deferred ambiguity

Ambiguous/deferred tasks receive `LOW` because their terminal task is not resolved. High phrase frequency cannot override unresolved meaning.

## Verdict

**D12-04 DEFAULT_HIGH_CONFIDENCE = VERIFIED_FIXED.**

Reason: confidence now represents evidence strength/dependency, not a default display label. Future hierarchy work may legitimately upgrade/downgrade individual rows, but it must use the same explicit dimensions; it cannot reintroduce a default HIGH.

## Next

D12-07: materialize site hierarchy/internal-link role for every accepted/provisional new-page candidate. Until that file exists, proposed new-page rows keep `hierarchy_clarity = PENDING_FOR_PROPOSED_PAGE` and cannot receive HIGH solely from demand.

## Простыми словами

Раньше почти всё автоматически считалось «очень уверенным», если я специально не написал обратное. Теперь это невозможно: уверенность складывается из конкретных доказательств. Если мы не проверили важную вещь — например, нужен ли в Яндексе отдельный тип страницы, — рекомендация так и остаётся средней/предварительной, даже если спрос большой.
