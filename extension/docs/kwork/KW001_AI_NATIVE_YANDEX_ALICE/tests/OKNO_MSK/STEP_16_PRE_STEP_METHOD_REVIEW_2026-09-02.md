# OKNO_MSK — STEP 16 PRE-STEP METHOD / EVIDENCE REVIEW

Date: 2026-09-02
Status: **POST-RUN CORRECTED / ORIGINAL PRE-STEP METHOD-VALIDATION VERDICT INVALIDATED**

## Correction authority

This file was originally used to declare the Step-16 project-specific method ready for owner review. A post-run external audit found four material method-validation defects that should have blocked paid execution until resolved.

Authoritative correction:

`STEP_16_METHOD_VALIDATION_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-02.md`

The original paid GenSearch results remain valid provider observations. The original claim that the pre-step method had been fully validated does not.

## Whole KW-001 goal

Deliver an evidence-backed semantic/page architecture using Yandex human-demand evidence, ordinary Search evidence and selective generative-search evidence, then make final Search-vs-AI page/content decisions in a separately gated comparison step.

## Correct roadmap boundary

```text
Steps 0–14A = ordinary-demand/Search/site architecture work
Step 15 = select/preregister bounded AI test cases
Step 16 = acquire and preserve GenSearch evidence only
Step 17 = compare ordinary Search + Step16 GenSearch + current-site evidence and make material decision deltas
Steps 18–22 = prioritization, deliverables, QA, handoff, close
```

Canonical rule:

```text
STEP16_GENSEARCH_ACQUISITION != STEP17_SEARCH_VS_AI_COMPARISON
```

## Correct Step-16 goal

For each Step-15-selected case, obtain a complete official Yandex GenSearch observation under a predeclared test scope, preserve the full provider response, document ambiguity and limitations, and hand observations—not final architecture verdicts—to Step 17.

## Evidence surface

For OKNO_MSK:

```text
EVIDENCE_SURFACE = YANDEX_GENSEARCH_API_PROXY
YANDEX_WEBMASTER_ALICE_VISIBILITY = UNAVAILABLE_NOT_EXECUTED
DIRECT_CONSUMER_ALICE_EVIDENCE = NOT_EXECUTED
```

Therefore:

```text
GEN_SEARCH_* != CONSUMER_ALICE_*
GEN_SEARCH_* != WEBMASTER_ALICE_VISIBILITY_STATISTICS
```

Owner/client-facing wording must say **official Yandex GenSearch diagnostic evidence**, not claim that the site was directly tested in consumer Alice AI.

## Test-scope rule

Every case must declare before provider execution:

```text
TEST_SCOPE = EXACT_QUERY
```

or

```text
TEST_SCOPE = USER_JOB
```

For `EXACT_QUERY`, claims are restricted to the exact tested wording/run family.

For `USER_JOB`, a bounded set of natural prompt/query variants must be frozen before provider execution with a rule for combining observations.

The executed OKNO_MSK run used exact authoritative Step-15 query strings only. Therefore the existing evidence is now interpreted as:

```text
TEST_SCOPE = EXACT_QUERY
```

and must not be generalized to the whole user-job family without additional evidence.

## Reproducibility / claim-strength rule

Before paid execution, the method must define how many independent observations are needed for the intended claim strength.

Minimum distinctions:

```text
ONE OBSERVATION
-> describes only that run

SHORT-WINDOW REPRODUCTION
-> may state that a material direction reproduced in a bounded short-window test
-> may NOT claim long-term stability

LONG-TERM/STABILITY CLAIM
-> requires a separately preregistered multi-time design
```

No universal repeat count is invented. Count/timing are job-scoped and must be frozen before execution.

Existing C15-010 evidence consists of two same-query observations in a short window. Correct claim:

```text
MATERIAL_AI_DIRECTION_REPRODUCED_IN_BOUNDED_SHORT_WINDOW_TEST = true
LONG_TERM_STABILITY_PROVEN = false
ARCHITECTURE_CHANGE_CONFIRMED = false
```

## Source-role evidence rule

GenSearch returns URL/title/used, but material page-role claims must not rely only on URL/title when the page role affects a decision.

If a conclusion depends on a used source being commercial, informational, DIY, service, specialist or broad:

```text
used=true URL
-> open/read current page
-> preserve page-role evidence
-> only then use decisive page-role classification
```

URL/title alone may be retained as a weak descriptive hint.

Source-array order and used-source counts are never provider ranking signals.

## Correct Step-16 output taxonomy

Step 16 may describe observations and provisional materiality only:

```text
OBSERVED_DIRECTION
OBSERVATION_MIXED
OBSERVATION_INSUFFICIENT
MATERIAL_OBSERVATION_CANDIDATE
CONTROL_ANOMALY_CANDIDATE
MATERIAL_OBSERVATION_REPRODUCED_SHORT_WINDOW
```

Step 16 must not issue final Search-vs-AI verdicts:

```text
final CHANGE
final DE_RISK
final NO_CHANGE
final architecture/page-owner decision
```

Those belong to Step 17.

## Correct execution order

```text
1. Freeze evidence surface.
2. Freeze EXACT_QUERY vs USER_JOB scope.
3. Freeze repeat policy and allowed claim strength.
4. Freeze Step16/Step17 scope boundary.
5. Freeze material used-source inspection policy.
6. Verify exact Step15 V2 case/query.
7. Execute one Manual GenSearch interaction.
8. Save COMPLETE provider result verbatim.
9. Read back verbatim raw.
10. Normalize provider observation without final Search-vs-AI verdict.
11. Read back normalized observation.
12. If a preregistered material observation triggers repetition, follow the frozen repeat policy exactly.
13. Complete provider/cost accounting.
14. Produce observation ledger and ambiguity/limitation report.
15. STOP. Step17 remains not started.
```

## External support checked in the post-run audit

- Yandex GenSearch API: https://aistudio.yandex.ru/ru/docs/search-api/api-ref/GenSearch/search
- Yandex Webmaster Alice AI visibility: https://yandex.ru/support/webmaster/ru/service/alice-answers
- NIST AI RMF Measure: https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- Ahrefs Brand Radar methodology: https://ahrefs.com/blog/brand-radar-methodology/
- Semrush AI Visibility methodology: https://ai-visibility-index.semrush.com/methodology
- Project implementation plan: `../../IMPLEMENTATION_PLAN.md`

## Four post-run method-validation failures

```text
S16-M01 = repeat/reproducibility policy under-specified
S16-M02 = exact-query evidence allowed to expand into user-job claims
S16-M03 = GenSearch proxy boundary not fully enforced in result naming/claims
S16-M04 = Step16 crossed into Step17 comparison/decision work
```

Full root causes and blocking controls are in `STEP_16_METHOD_VALIDATION_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-02.md`.

## Corrected pass gate for future runs

Before the first paid interaction all must be true:

```text
STEP16_EVIDENCE_SURFACE_FROZEN = true
STEP16_TEST_SCOPE_FROZEN = true
STEP16_REPEAT_POLICY_FROZEN = true
STEP16_CLAIM_BOUNDARY_FROZEN = true
STEP16_STEP17_SCOPE_BOUNDARY_FROZEN = true
STEP16_SOURCE_PAGE_INSPECTION_POLICY_FROZEN = true
```

Any false value blocks paid provider execution.

## Existing OKNO_MSK run status

The paid run is not discarded. Its nine provider responses remain evidence.

However:

```text
ORIGINAL_PRESTEP_METHOD_VALIDATION = FAILED_POST_RUN_AUDIT
RAW_PROVIDER_EVIDENCE = PRESERVED_AND_USABLE
OLD_STEP16_FINAL_DELTA_LABELS = SUPERSEDED_AS_FINAL_DECISION_AUTHORITY
STEP17_MUST_REASSESS_FROM_CORRECTED_STEP16_OBSERVATIONS
```
