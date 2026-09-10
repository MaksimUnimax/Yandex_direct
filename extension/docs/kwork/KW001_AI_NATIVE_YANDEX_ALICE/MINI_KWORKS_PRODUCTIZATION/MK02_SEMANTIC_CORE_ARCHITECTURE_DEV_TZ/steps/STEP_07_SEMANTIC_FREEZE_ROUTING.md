# MK02 STEP 07 — SEMANTIC FREEZE / UNCERTAINTY ROUTING

## PURPOSE
Freeze one deterministic pre-Search semantic universe and route every phrase to its next legitimate evidence state before clustering/page work.

## WHY THIS STEP EXISTS
Without an explicit freeze, later Search/clustering/page ownership can silently lose excluded/review rows, overwrite uncertainty or rebuild from inconsistent intermediate sources.

## INPUTS
Step06 row-level decisions; complete demand/provenance layer; frozen order/business profile.

## REQUIRED EVIDENCE
One governed unique phrase key; current semantic state/reason; complete occurrence/demand provenance; explicit unresolved route where applicable.

## METHOD
Materialize one current semantic set with equivalent states for active/core candidates, Search-routed review, deferred review and preserved exclusions. Every phrase keeps a deterministic join to demand/provenance. Review routes must correspond to a real next action/evidence source; do not invent unsupported taxonomy merely to classify uncertainty.

## OUTPUTS
Frozen semantic universe; route ledger; explicit deferred/excluded preservation; reconciliation manifest.

## SOURCE KW-001 AUTHORITY
KW-001 `STEP_08_SEARCH_STAGE_FREEZE_METHOD.md`; MK01 Step07.

## KNOWN FAILURE CLASSES
S12 invented/erased uncertainty states; silent field loss; stale intermediate authority reused downstream.

## ROOT CAUSES
Pipeline convenience treated uncertainty/exclusions as temporary processing noise rather than part of accepted truth.

## NON-REPEAT CONTROLS
One current freeze; 100% deterministic joins; explicit route semantics; excluded/review rows preserved; later consumer must read current authority rather than resurrect earlier state.

## CLAIM BOUNDARIES
A Search route means evidence is needed; it does not imply the phrase will be accepted. Deferred does not mean rejected.

## UNKNOWN / BLOCKER BEHAVIOR
Unresolved phrases remain explicit. If a named route cannot actually be executed in current product/mode, use deferred/HOLD rather than a fictional action.

## PASS GATE
Full phrase accounting reconciles; duplicate current keys = 0; silent drops = 0; all review states have legitimate route/reason; complete provenance join; freeze persisted/read back.

## CLIENT-FACING MEANING
«Перед дальнейшим анализом фиксируем единый список: рабочие кандидаты, спорные запросы, отложенные и исключённые — ничего не теряется между этапами.»
