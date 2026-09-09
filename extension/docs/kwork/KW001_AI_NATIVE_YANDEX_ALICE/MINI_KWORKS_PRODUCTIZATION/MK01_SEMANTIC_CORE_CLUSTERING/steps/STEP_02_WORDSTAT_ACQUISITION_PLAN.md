# MK01 STEP 02 — WORDSTAT ACQUISITION PLAN

## PURPOSE
Design bounded Yandex Wordstat probes that reveal demand vocabulary without pre-approving keywords.

## WHY THIS STEP EXISTS
KW-001 established that a seed is a measurement probe, not the final semantic target.

## INPUTS
Frozen order + current site/business/domain profile.

## REQUIRED EVIDENCE
Confirmed business families, region and current vocabulary; unresolved coverage questions that justify probes.

## METHOD
For each planned probe record expression/seed, region, applicable device/operator mode, information purpose, expected evidence type and stop/coverage condition. Avoid recursive expansion by default. Site taxonomy may suggest probes but does not define the final taxonomy.

## OUTPUTS
Frozen acquisition manifest for Step03.

## SOURCE KW-001 AUTHORITY
Step2 lessons in `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` and provider evidence/cost policies.

## KNOWN FAILURE CLASSES
E03 — seed treated as final relevant keyword.

## ROOT CAUSES
The acquisition mechanism was confused with the later semantic decision.

## NON-REPEAT CONTROLS
`SEED != FINAL KEYWORD`; every probe has an information purpose; downstream rows are evaluated independently.

## CLAIM BOUNDARIES
A planned or successful probe proves neither relevance of every returned phrase nor completeness of the final core.

## UNKNOWN / BLOCKER BEHAVIOR
If a business direction cannot be scoped, do not create unlimited adjacent probes; hold that direction for clarification.

## PASS GATE
Every planned call maps to a frozen business direction/information gap; region/mode recorded; no silent Google source; no unbounded recursion.

## CLIENT-FACING MEANING
«Сначала формирую набор поисковых направлений для Wordstat. Эти формулировки нужны, чтобы раскрыть реальный язык спроса, а не чтобы заранее навязать итоговые ключи.»
