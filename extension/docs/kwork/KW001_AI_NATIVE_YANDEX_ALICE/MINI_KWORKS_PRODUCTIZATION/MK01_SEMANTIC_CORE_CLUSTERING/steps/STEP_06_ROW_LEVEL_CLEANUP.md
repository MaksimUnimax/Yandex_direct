# MK01 STEP 06 — ROW-LEVEL SEMANTIC CLEANUP

## PURPOSE
Give every governed phrase an explicit semantic state, reason and uncertainty before clustering.

## WHY THIS STEP EXISTS
KW-001 exposed two false shortcuts: no-rejection fallthrough became KEEP, and row-count/accounting PASS was mistaken for semantic correctness.

## INPUTS
Complete persisted acquisition universe, business/site profile, triage layer and any justified Step05 additions.

## REQUIRED EVIDENCE
Phrase text/context, Wordstat provenance/demand role, business relevance evidence and current domain constraints.

## METHOD
Evaluate every governed phrase. Assign an explicit current-job state such as KEEP/active, REVIEW/SEARCH_REQUIRED, DEFERRED/HOLD or EXCLUDE with a concrete reason. KEEP requires positive semantic/business support; exclusion cannot rely on frequency alone. Run row accounting and independent semantic challenge QA separately.

## OUTPUTS
Complete row-level semantic decision table with no silent fallthrough.

## SOURCE KW-001 AUTHORITY
Corrected Step7 permanent method in `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` / source `STEP_RULES_INDEX.md`.

## KNOWN FAILURE CLASSES
E11 default KEEP; E12 arithmetic QA substituted for semantic QA; E08/E09 frequency-signal misuse.

## ROOT CAUSES
Absence of a reject rule was interpreted as evidence for relevance; deterministic completeness was confused with analytical correctness.

## NON-REPEAT CONTROLS
No default KEEP. Positive evidence required. Separate accounting QA and adversarial semantic QA. Uncertainty remains explicit.

## CLAIM BOUNDARIES
This step decides semantic/business suitability only; it does not assign final page owners or architecture.

## UNKNOWN / BLOCKER BEHAVIOR
Potentially useful but unresolved rows remain REVIEW/SEARCH_REQUIRED/HOLD; never delete uncertainty to finish faster.

## PASS GATE
100% governed-row accounting; no default KEEP; every state has reason; independent semantic QA completed; uncertainty preserved.

## CLIENT-FACING MEANING
«Каждый запрос получает отдельное решение: оставить, исключить или вынести на дополнительную проверку. Я не считаю запрос полезным только потому, что он не попал под готовое правило удаления.»
