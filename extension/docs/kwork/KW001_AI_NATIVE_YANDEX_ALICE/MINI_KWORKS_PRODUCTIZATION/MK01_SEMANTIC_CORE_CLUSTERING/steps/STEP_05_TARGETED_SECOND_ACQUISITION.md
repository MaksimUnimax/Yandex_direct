# MK01 STEP 05 — TARGETED SECOND ACQUISITION

## PURPOSE
Acquire additional Yandex demand only when persisted evidence leaves a named material coverage gap.

## WHY THIS STEP EXISTS
More provider calls are not automatically better coverage; recursive collection can increase cost/noise without information gain.

## INPUTS
Step03 persisted evidence, Step04 triage, explicit unresolved acquisition gap.

## REQUIRED EVIDENCE
A written gap statement showing what is unknown, why it matters and why existing evidence cannot answer it.

## METHOD
If a material gap exists, design the smallest justified additional Wordstat probe set using the same occurrence/demand/provenance schema as Step03. Persist/read back identically. If no gap exists, record `NOT_REQUIRED` and make no provider call.

## OUTPUTS
Union-compatible additional evidence + resolved/unresolved gap result, or explicit NOT_REQUIRED.

## SOURCE KW-001 AUTHORITY
Step5 partial method/data-preservation boundary + Step3 durability/cost rules.

## KNOWN FAILURE CLASSES
E10 — second acquisition became recursive collection.

## ROOT CAUSES
Collection volume was confused with methodological completeness.

## NON-REPEAT CONTROLS
Every call maps to one named information gap; no automatic recursion; schema identical/union-compatible; provider cost recorded.

## CLAIM BOUNDARIES
Step5 does not include Step5A competitor semantic expansion in base MK01.

## UNKNOWN / BLOCKER BEHAVIOR
If the evidence route is unavailable or too weak, keep the gap unresolved instead of fabricating coverage.

## PASS GATE
Every additional request is justified and persisted/reconciled, or the step is explicitly NOT_REQUIRED with no call.

## CLIENT-FACING MEANING
«Дополнительный сбор делаю только там, где первый проход действительно оставил пробел, а не ради искусственного увеличения количества ключей.»
