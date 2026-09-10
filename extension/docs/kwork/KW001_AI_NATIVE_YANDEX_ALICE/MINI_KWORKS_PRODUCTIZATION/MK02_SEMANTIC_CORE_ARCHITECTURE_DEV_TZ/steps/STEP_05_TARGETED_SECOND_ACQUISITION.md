# MK02 STEP 05 — TARGETED SECOND ACQUISITION

## PURPOSE
Fill only named semantic coverage gaps that can materially improve the MK02 semantic foundation before cleanup and architecture work.

## WHY THIS STEP EXISTS
A second acquisition pass can improve coverage, but uncontrolled recursive expansion creates cost, noise and an illusion of completeness. MK02 also must not silently turn this step into competitor-gap research.

## INPUTS
Step04 named gaps; persisted Step03 evidence; frozen scope; current provider/cost state.

## REQUIRED EVIDENCE
Each proposed second-pass request has a specific unresolved information gap, expected information gain and stop condition.

## METHOD
Run only justified new Wordstat probes. Use the same complete occurrence/provenance schema as Step03 so results can be unioned without losing lineage. Reassess information gain after the bounded pass and stop when the named gap is sufficiently covered or further collection is not justified.

## OUTPUTS
Union-compatible second-pass evidence; updated occurrence layer; explicit stop decision.

## SOURCE KW-001 AUTHORITY
KW-001 Step5 partial method/data-preservation boundary; MK01 Step05; Step3 persistence/cost gates.

## KNOWN FAILURE CLASSES
S09 recursive collection; S04 provider response not durably persisted; hidden Step5A competitor expansion.

## ROOT CAUSES
“More keywords” was treated as self-justifying progress rather than evidence acquisition for a concrete decision gap.

## NON-REPEAT CONTROLS
Named gap + expected decision use + bounded request set + same persistence schema + explicit stop. Competitor-derived seeds/pages are not introduced in base MK02.

## CLAIM BOUNDARIES
Second-pass growth does not prove semantic relevance, page ownership or need for new pages.

## UNKNOWN / BLOCKER BEHAVIOR
If expected information gain is low or cost/authorization is not justified, preserve the gap instead of collecting indefinitely.

## PASS GATE
Every request traces to a named gap; returned rows fully persisted/reconciled; stop decision recorded; Step5A competitor work absent; no recursive open-ended expansion.

## CLIENT-FACING MEANING
«Дополнительный сбор делаем только там, где первый проход действительно оставил пробел, а не ради увеличения количества ключей.»
