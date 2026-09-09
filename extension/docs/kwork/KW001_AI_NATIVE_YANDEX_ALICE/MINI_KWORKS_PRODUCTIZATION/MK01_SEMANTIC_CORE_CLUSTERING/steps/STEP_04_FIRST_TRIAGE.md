# MK01 STEP 04 — FIRST TRIAGE

## PURPOSE
Remove obvious out-of-scope/noise families early without pretending full semantic cleanup is finished.

## WHY THIS STEP EXISTS
KW-001 showed that family-level screening can be useful operationally but becomes dangerous when treated as member-row semantic proof.

## INPUTS
Persisted Wordstat universe + frozen business/site profile.

## REQUIRED EVIDENCE
Returned phrase families, counts/roles and current business-scope evidence.

## METHOD
Identify clearly irrelevant families using business/scope evidence; preserve ambiguous, low-frequency and associated demand for later row-level judgment. Record family decision and reason separately from member-row state.

## OUTPUTS
Early triage layer with explicit reasons and preserved unresolved rows.

## SOURCE KW-001 AUTHORITY
Step4 lessons in the permanent method ledger.

## KNOWN FAILURE CLASSES
E07 triage=cleanup; E08 low frequency auto-excluded; E09 high count/association auto-kept.

## ROOT CAUSES
Operational screening signal was promoted into final semantic evidence; volume substituted for relevance.

## NON-REPEAT CONTROLS
`FAMILY DECISION != MEMBER ROW`; `LOW FREQUENCY != IRRELEVANT`; `HIGH FREQUENCY != RELEVANT`.

## CLAIM BOUNDARIES
This step does not produce the final active semantic core or final clusters.

## UNKNOWN / BLOCKER BEHAVIOR
Ambiguous in-scope-looking demand remains for Step06/07; do not force a decision for convenience.

## PASS GATE
Obvious noise has reasons; potentially useful ambiguity preserved; no row silently disappears; no claim of full cleanup.

## CLIENT-FACING MEANING
«На первом проходе отсеиваю очевидный мусор и чужие темы, но спорные запросы не выкидываю только из-за низкой частотности или необычной формулировки.»
