# KW-001 / OKNO-MSK — STEP 10 PROGRESS CHECKPOINT — 2026-08-29

Status: **ACTIVE / NOT ACCEPTED / RESUME FROM V17 SELF-TEST FAILURE**

This file is the end-of-session checkpoint for 2026-08-29. It records the actual Step-10 implementation/QA state and is the required resume point for the next work session.

## Branch and checkpoint base

```text
repository = MaksimUnimax/Yandex_direct
branch = roadmap/kwork-productization-2026-08-28
last implementation HEAD before this checkpoint = 17176c79c6b88527f167600b0cf773dcd3edf865
last implementation commit = step10: fix V17 Moscow morphology guard
last workflow run = 33256165028
last workflow job = 99110144487
last workflow conclusion = FAILURE
failure stage = Build conservative Step10 user-task clusters / self-test
```

The workflow failure occurred **before `runner.main()` and before generated Step-10 artifacts were rewritten/committed**. Therefore the last committed generated candidate artifacts are still the previous V14 outputs. V15/V16/V17 code is present, but no V15+ generated candidate is accepted or authoritative yet.

## Current formal state

```text
STEP10_EXECUTION_STARTED = true
STEP10_IMPLEMENTATION_ITERATION = V17
STEP10_MACHINE_REBUILD_V17 = NOT_REACHED
STEP10_V17_SELF_TEST = FAIL
STEP10_GENERATED_ARTIFACTS_V15_PLUS = NOT_COMMITTED
STEP10_MANUAL_SEMANTIC_QA = IN_PROGRESS / NOT PASS
STEP10_COMPLETE = false
STEP11_ALLOWED = false
```

Do not reinterpret a green older V14 workflow as Step-10 acceptance. Manual QA after V14 found real semantic errors that the then-current automatic audits did not detect.

## Why V15 was introduced

Manual semantic QA of the V14 candidate found a systemic precedence problem: broad material/private-house/product rules could swallow a more specific user object, action, or informational task.

Observed error classes included:

```text
1. private-house generic fallback swallowing specific objects/actions;
2. object-specific glazing being swallowed by material/product rules;
3. French/panoramic product families being confused with architecture/real-estate context;
4. informational types/variants being swallowed by product clusters;
5. material words such as wooden/PVC acting as stronger signals than the actual glazing task;
6. unresolved audit returning zero likely misses while manual QA still found clearly classifiable unresolved phrases.
```

Examples found during manual QA:

```text
дом треугольный как называется с панорамными окнами
    -> should be architecture / house-type context, not window-definition

застекление веранды в частном доме панорамное остекление
    -> glazing-service task, not generic private-house window product

входные двери с окном для частного дома
    -> entrance-door head object, not generic private-house window product

французские окна в частном доме цена
    -> specific French-window product family before generic private-house fallback

цена панорамных окон для дома
    -> specific panoramic-window product family before generic private-house fallback

виды пластиковых окон
    -> informational types/variants task, not generic PVC purchase

деревянное остекление веранды
остекление веранды в деревянном доме
    -> veranda glazing service; material/building wording is a modifier
```

## V15 direction now preserved in code

V15 introduced a stronger precedence model. The intended rule order is conceptually:

```text
specific object / explicit action / explicit information task
-> component/accessory
-> specific product/type/material family
-> contextual use-case modifier
-> generic private-house/product fallback
```

Important non-repeat principles:

```text
SPECIFIC_USER_TASK > GENERIC_USE_CASE
OBJECT_SPECIFIC_GLAZING > MATERIAL_PRODUCT_FALLBACK
EXPLICIT_ACTION > PRODUCT_FAMILY
EXPLICIT_INFORMATION_TASK > PRODUCT_FAMILY
DWELLING_HEADED_CONTEXT != WINDOW_HEADED_PRODUCT_QUERY
MATERIAL_TOKEN != AUTOMATIC_PRODUCT_INTENT
ZERO_AUTOMATIC_AUDIT_FLAGS != MANUAL_SEMANTIC_QA_PASS
```

## Audit strengthening performed

The unresolved adversarial audit was strengthened because the previous audit could report zero likely false unresolved states while the manual sample still contained semantically obvious candidates such as price, repair, glazing, project/context, dimensions, and accessory tasks.

Current required audit stack after a successful rebuild:

```text
machine accounting gate
+ direct Step-09 service/product contradiction gate
+ V15 semantic collision audit
+ V15 unresolved-state adversarial audit
+ manual semantic QA
```

Zero machine/adversarial flags is necessary but **not sufficient** for Step-10 PASS.

## Regression fixes already carried forward

The implementation chain currently includes these corrections:

```text
V15 = systemic specificity/precedence rewrite + stronger unresolved audit
V16 = restore explicit Russian `ПВХ` as PVC material when V15 would otherwise reach generic private-house product fallback
V17 = restore exact-only SP09-011 porch-glazing evidence and add French-window final precedence guard
17176c79 = Russian morphology fix: use `москв` stem instead of literal `москва`
```

Exact Step-09 evidence rule retained:

```text
крыльцо для частного дома окна
-> PORCH_GLAZING
-> exact SP09-011 evidence only
-> no evidence transfer to neighbouring phrases
```

## Exact current failure — start here next session

Run `33256165028` failed on this assertion:

```text
phrase = замена балконного блока на французское окно
expected = WINDOW_REPLACEMENT_SERVICE
actual = FRENCH_WINDOWS_COMMERCIAL
actual reason = Window-headed French-window product/configuration demand has priority over incidental apartment/house context
```

Root cause at checkpoint time:

The V17 final French-product precedence guard is now too broad. It correctly protects window-headed French-product queries from the older real-estate fallback, but it also overrides an **explicit replacement/conversion action**. Replacement/action semantics must outrank the French product/configuration guard.

## Mandatory first action next session

Do **not** jump to Step 11 and do **not** accept Step 10 from V14.

Start with:

```text
1. Open STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V17.py.
2. Fix the French final priority guard systemically so explicit whole-window/balcony-block replacement or conversion wins before FRENCH_WINDOWS_COMMERCIAL.
3. Do not solve only the exact failing string if a general action-precedence rule covers the class.
4. Re-run the complete inherited V15 + V16 + V17 self-test corpus.
5. Continue fixing real precedence regressions until the whole corpus passes without weakening/removing the tests.
6. Only then allow runner.main() and the full 2840-row rebuild.
```

The immediate regression that must pass is:

```text
замена балконного блока на французское окно
-> WINDOW_REPLACEMENT_SERVICE
```

while preserving at least these already-protected boundaries:

```text
французские окна в москве в квартирах
-> FRENCH_WINDOWS_COMMERCIAL

квартира с французскими окнами
-> architecture/real-estate context

крыльцо для частного дома окна
-> PORCH_GLAZING via exact SP09-011

окна пвх для частного дома
-> PVC_WINDOWS_COMMERCIAL

размеры окон пвх для частного дома
-> WINDOW_DIMENSIONS_INFO
```

## Required full rerun after self-tests pass

Run the existing GitHub Actions workflow and require all of the following before manual acceptance review:

```text
2840 total phrase keys
2332 active Search-stage rows
1388 CORE_CANDIDATE
944 REVIEW_SEARCH
174 REVIEW_DEFERRED preserved
334 excluded preserved
75 direct Step-09 probes consumed/accounted
8 duplicate comparisons consumed
0 unprobed rows claiming direct SERP evidence
0 silent drops
0 page-ownership decisions
0 structural-action decisions
0 cannibalization decisions
0 provider requests
```

Then inspect the **bot-generated final HEAD**, not the implementation commit alone.

## Mandatory manual QA after a green workflow

A green workflow is not formal acceptance. Re-check representative and historically failing boundaries including:

```text
PVC / ПВХ vs dimensions vs private-house
French windows: product vs dwelling context vs replacement/action
panoramic windows: product vs architecture/inspiration vs service/action
veranda / terrace / balcony / gazebo glazing
wood/aluminium/PVC material modifiers vs glazing-service object
soft windows
doors and mixed windows+doors
finishing / slopes / ebb
repair / replacement / demolition / installation
hardware/accessories
house-series queries
all direct Step-09 anchors
remaining SEARCH_REQUIRED sample and strengthened unresolved-audit targets
```

Only after this manual review can a Step-10 acceptance artifact be written.

## Stop boundary

```text
STEP10_COMPLETE = false
STEP11_PAGE_OWNERSHIP = BLOCKED
NO_PAGE_OWNERSHIP_DECISIONS_YET = true
NO_STRUCTURAL_ACTION_DECISIONS_YET = true
NO_CANNIBALIZATION_DECISIONS_YET = true
```

Resume Step 10 only. Do not silently advance the roadmap.

## Useful links

- Branch: https://github.com/MaksimUnimax/Yandex_direct/tree/roadmap/kwork-productization-2026-08-28
- Last implementation commit before checkpoint: https://github.com/MaksimUnimax/Yandex_direct/commit/17176c79c6b88527f167600b0cf773dcd3edf865
- Failed workflow run: https://github.com/MaksimUnimax/Yandex_direct/actions/runs/33256165028
- V17 classifier: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V17.py
- Workflow: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/.github/workflows/kw001-okno-step10-user-task-clustering.yml

## Checkpoint marker

```text
KW001_OKNO_STEP10_2026_08_29_CHECKPOINT = RECORDED
RESUME_FROM = V17_FRENCH_REPLACEMENT_PRECEDENCE_REGRESSION
STEP10_ACCEPTED = false
STEP11_BLOCKED = true
```
