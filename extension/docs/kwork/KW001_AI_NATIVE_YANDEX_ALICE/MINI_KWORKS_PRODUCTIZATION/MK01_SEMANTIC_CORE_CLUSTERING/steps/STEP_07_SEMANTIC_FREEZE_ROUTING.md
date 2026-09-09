# MK01 STEP 07 — SEMANTIC FREEZE / ROUTING

## PURPOSE
Freeze the preserved semantic universe before Search/clustering and route unresolved rows only to executable next evidence states.

## WHY THIS STEP EXISTS
KW-001 showed that uncertainty can be lost through convenient taxonomies, silent drops or premature lexical merging.

## INPUTS
Row-level cleanup authority + complete demand/provenance joins.

## REQUIRED EVIDENCE
Every governed phrase key, semantic state/reason, demand/provenance trace and allowed uncertainty route.

## METHOD
Materialize an immutable handoff containing active, Search-required, deferred/HOLD and excluded states. Require deterministic phrase→demand/provenance joins. REVIEW is valid only when it names a real next evidence route or explicit deferred state. Do not auto-merge non-exact phrases because they look similar.

## OUTPUTS
Versioned Search-stage semantic authority + review/Search routing manifest.

## SOURCE KW-001 AUTHORITY
`STEP_08_SEARCH_STAGE_FREEZE_METHOD.md` and corrected Step7 controls.

## KNOWN FAILURE CLASSES
E13 invented REVIEW taxonomy; E14 REVIEW simplified away; E15 non-exact duplicates auto-merged.

## ROOT CAUSES
Uncertainty labels were designed for symmetry/convenience rather than executable evidence; lexical similarity replaced unresolved task evidence.

## NON-REPEAT CONTROLS
Every preserved phrase joins 100% to demand/provenance; silent drops=0; REVIEW must route somewhere real; lexical ambiguity stays unresolved until supported.

## CLAIM BOUNDARIES
Freeze is an input authority for MK01 Search/clustering, not page ownership or final website architecture.

## UNKNOWN / BLOCKER BEHAVIOR
No available evidence route -> explicit DEFERRED/HOLD with reason, not invented certainty.

## PASS GATE
Full universe reconciles; joins deterministic; uncertainty executable/explicit; no silent merges/drops; version identity persisted.

## CLIENT-FACING MEANING
«Перед группировкой фиксирую полный набор: рабочие, спорные и исключённые запросы. Спорные запросы не исчезают — для них видно, нужна ли проверка выдачи или решение пока отложено.»
