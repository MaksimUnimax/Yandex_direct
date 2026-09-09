# MK01 STEP 00 — ORDER / SCOPE FREEZE

## PURPOSE
Persist exactly what the client bought before provider evidence can influence the task.

## WHY THIS STEP EXISTS
KW-001 showed that evolving evidence can otherwise silently change the original success criterion.

## INPUTS
`CLIENT_INPUT_CONTRACT.md`: public URL, primary region, included directions, exclusions/NONE, business/conversion job, optional client materials.

## REQUIRED EVIDENCE
Client-supplied business facts plus readable public-site identity sufficient to confirm the order target.

## METHOD
Create a Level-2 order record with site, existing-site mode, region, included/excluded scope, business description, conversion job, package=MK01, optional-data states, unresolved questions and frozen timestamp. Record Yandex-only scope explicitly.

## OUTPUTS
Immutable initial order/scope authority; later changes are revisions, not rewritten history.

## SOURCE KW-001 AUTHORITY
Step0 lessons, `IMPLEMENTATION_PLAN.md` mock-client/order-freeze logic, `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`.

## KNOWN FAILURE CLASSES
E01 — evidence silently changed the sold task.

## ROOT CAUSES
Research progress was allowed to redefine the brief instead of changing only conclusions.

## NON-REPEAT CONTROLS
No Wordstat/Search acquisition before freeze. Material site/region/business-family changes after freeze get a revision record and impact analysis.

## CLAIM BOUNDARIES
The freeze proves the agreed research scope, not completeness of the website or validity of any keyword.

## UNKNOWN / BLOCKER BEHAVIOR
Missing URL, unreadable site, missing primary region or unresolved material business scope blocks provider acquisition. Do not infer them silently.

## PASS GATE
All required fields persisted; Yandex-only acknowledged; no secret/password dependency; unresolved questions explicitly recorded.

## CLIENT-FACING MEANING
«До сбора запросов фиксируем сайт, регион и направления, чтобы исследование не ушло в соседние темы и результат соответствовал заказу.»
