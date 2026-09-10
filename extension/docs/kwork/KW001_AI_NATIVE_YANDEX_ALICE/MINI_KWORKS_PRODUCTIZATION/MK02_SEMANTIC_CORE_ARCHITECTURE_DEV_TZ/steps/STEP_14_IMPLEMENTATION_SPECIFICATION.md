# MK02 STEP 14 — IMPLEMENTATION SPECIFICATION / ANALYTICAL PRIORITY

## PURPOSE
Convert accepted architecture/action authority into concrete implementation-ready work packages where evidence is sufficient, while preserving clarification, mapping-only, no-change and HOLD states where it is not.

## WHY THIS STEP EXISTS
A correct owner/action row is not automatically a task an implementer can execute. Prior work also showed that analytical priority was easily overstated as a production schedule, and generic recommendation templates left the real analysis/placement to the recipient.

## INPUTS
Final Step13 current-vs-target architecture; Step11 actions; Step12 competing-page constraints; current page/content/link evidence; client business/change constraints; optional real implementer/effort/capacity information.

## REQUIRED EVIDENCE
For each material work package: current object/page, as-is state, human-readable evidence meaning, audit locator, implementation mode, exact requested change, exact location/context where material, target state, dependencies, preservation constraints, acceptance condition. Real owner/effort/capacity/timing evidence only when a production schedule is claimed.

## METHOD
Canonicalize one real proposed site change as one action key, even when multiple evidence sources support it. Separate accounting batches from executable work packages. Explicitly classify each item using job-appropriate equivalents:

```text
READY_IMPLEMENTATION_SPEC
PENDING_BUSINESS_DETAIL
PENDING_TECHNICAL_DETAIL
PENDING_PLACEMENT_OR_CONTEXT
RECHECK_ONLY
SEMANTIC_MAPPING_ONLY
NO_SITE_CHANGE
HOLD
```

Every site-change package declares an implementation mode such as:

```text
CONTEXTUAL_LINK
NAVIGATION_CHANGE
CONTENT_BLOCK
METADATA_OR_LABEL_CHANGE
OTHER_EXPLICIT_MECHANISM
```

`SEMANTIC_MAPPING_ONLY` and `NO_SITE_CHANGE` are valid results and never become fake website tasks.

A READY recommendation is action-specific. When exact placement matters, one supported placement is required. “Before X or Y”, “where appropriate”, “choose a category”, “decide which page”, or other analysis left to the implementer means the item is not READY.

Company-specific facts require company evidence. Missing business detail becomes a concrete question plus a statement of what becomes ready after the answer.

Assign analytical importance separately from execution schedule. If real implementation owner/effort/capacity/timing are unavailable:

```text
IDEAL_ANALYTICAL_PRIORITY = ALLOWED
EXPECTED_IMPLEMENTATION_SEQUENCE = PENDING_CALIBRATION
```

Do not invent effort, delivery windows, responsible employee, business value or expected uplift.

For READY items, acceptance tests verify the observable implemented state. Recheck triggers for uncertain decisions remain separate from outcome measurement.

## OUTPUTS
Canonical action/work-package register; READY implementation specifications; clarification/check register; mapping/no-change/HOLD register; dependencies; analytical priority; optional calibration interface; implementation acceptance criteria; QA.

## SOURCE KW-001 AUTHORITY
`STEP_18_PRIORITIZATION_AND_IMPLEMENTATION_READINESS_METHOD.md`; `STEP_18_EXECUTION_TICKET_COMPLETENESS_GATE.md`; corrected Report №02 gate and owner failure classes A–U.

## KNOWN FAILURE CLASSES
E18-01..E18-08; T18-01..T18-05; Report failures A–U in `ERRORS_AND_LESSONS.md`.

## ROOT CAUSES
Analytical rows, accounting completeness, generic templates and unknown implementation variables were allowed to look more executable than they actually were.

## NON-REPEAT CONTROLS
Implementation mode required; real-site-change state explicit; action-specific steps; exact location/context when material; evidence meaning separate from locator; no placeholders; analysis not left to implementer; accounting batches decomposed; dependencies explicit; numbering not schedule; duplicates consolidated; no invented owner/effort/capacity/timing; acceptance tied to implementation mode.

## CLAIM BOUNDARIES
```text
CORRECT OWNER / ROUTE != READY TICKET
ANALYTICAL ACTION != IMPLEMENTATION SPECIFICATION
FIELDS PRESENT != EXECUTION DECISION RESOLVED
IMPLEMENTATION SPECIFICATION != PRODUCTION SCHEDULE
UNKNOWN EFFORT != LOW EFFORT
UNKNOWN OWNER != ASSIGNABLE
RECHECK TRIGGER != SUCCESS METRIC
```

## UNKNOWN / BLOCKER BEHAVIOR
If a material field needed to implement safely is unknown, move the item to the exact corresponding clarification/pending state. Do not backfill missing project evidence during report writing without a separately authorized research/revalidation step.

## PASS GATE
Every READY item has resolved implementation mode and real-site-change state; exact location/context exists when required; evidence meaning present; no filename-only client justification; no analysis left to implementer; placeholders=0; duplicate visible action/link pairs unexplained=0; acceptance matches requested change; unknown scheduling inputs not fabricated; mapping/no-change/HOLD states preserved separately.

## CLIENT-FACING MEANING
«В итоговом ТЗ готовыми считаются только те задачи, где понятно, что именно менять, зачем, где и как проверить результат. Если не хватает конкретного факта или места размещения, это не прячется под видом готовой рекомендации — клиент получает точный вопрос, который нужно закрыть перед внедрением.»

---

## OWNER CORRECTION 2026-09-10 — TWO OUTPUTS: FULL PAGE SPEC + CHANGE DELTA

The prior implementation-only framing is insufficient for MK02. Step14 must produce **two distinct but linked deliverables**:

```text
1. FULL TARGET PAGE SPECIFICATION REGISTER
   = one specification for every material target landing page / target page role

2. CURRENT→TARGET IMPLEMENTATION DELTA
   = only the physical changes, clarifications and checks required to move the current site toward that target
```

The full target page specification is mandatory even when the current site already matches the target and physical change count is small.

For every material target page, materialize a page specification containing equivalent client meaning for:

```text
TARGET PAGE / PAGE KEY
TARGET URL OR ROUTE
PAGE TYPE
PARENT / SECTION
PAGE PURPOSE
PRIMARY USER TASK / INTENT
PRIMARY / REPRESENTATIVE QUERY
MEMBER PHRASE COUNT
KEY CLUSTER / SEMANTIC SCOPE
WHAT THIS PAGE SHOULD COVER
WHAT SHOULD NOT BE SPLIT INTO A SEPARATE PAGE / WHAT BELONGS ELSEWHERE when material
SUPPORTING / CHILD / RELATED PAGES when material
CURRENT URL MATCH / CURRENT STATE
TARGET ACTION = CREATE | OPTIMIZE | ROUTE | KEEP | NO_STANDALONE | RECHECK
REAL SITE CHANGE REQUIRED = YES | NO | UNRESOLVED
IMPLEMENTATION DETAIL where change is real and resolved
ACCEPTANCE / FINAL EXPECTED STATE
UNCERTAINTY / REQUIRED CLARIFICATION where applicable
```

Phrase-level member detail remains in XLSX and must not be dumped as thousands of lines into PDF. The page specification should show representative/primary demand plus cluster size and scope, while the XLSX provides the complete phrase→target mapping.

`KEEP` is a full specification outcome:

```text
KEEP = this current URL is the accepted target landing page for the defined cluster/task
```

It must remain visible in the page-spec register even when no physical change is required.

`NO_STANDALONE` is also a full specification outcome:

```text
NO_STANDALONE = do not create a separate URL; route this demand into the named parent/owner page
```

The implementation/TZ PDF must therefore not consist only of READY physical changes. It must let the recipient understand the **complete target page plan**, then distinguish which page specs require implementation changes.

Permanent rules:

```text
FULL PAGE SPEC != CHANGE-ONLY TICKET LIST
NO SITE CHANGE != NO TZ ENTRY
THOUSANDS OF PHRASES IN PDF != USEFUL PAGE-BY-PAGE SPEC
PHRASE DETAIL LIVES IN XLSX; PAGE DESIGN / TARGET ROLE MUST BE HUMAN-READABLE IN TZ
SMALL DELTA != PERMISSION FOR A TWO-PAGE EMPTY-LOOKING TZ
```

Additional PASS requirements:

```text
MATERIAL TARGET PAGES WITHOUT PAGE SPEC = 0
KEEP TARGET PAGES WITHOUT PAGE SPEC = 0
NO_STANDALONE TASKS WITHOUT NAMED OWNER/PARENT = 0
IMPLEMENTATION PDF CONTAINS OR SUMMARIZES COMPLETE TARGET PAGE REGISTER = true
PHYSICAL CHANGE TICKETS ARE A SUBSET OF FULL PAGE SPEC REGISTER = true
```

Correct client-facing meaning:

«ТЗ показывает не только страницы, которые надо изменить. Для каждой целевой посадочной страницы фиксируется её назначение, семантика, место в структуре и итоговое решение. Отдельно отмечается, где страницу нужно создать или доработать, а где существующая страница уже правильно выполняет целевую роль.»