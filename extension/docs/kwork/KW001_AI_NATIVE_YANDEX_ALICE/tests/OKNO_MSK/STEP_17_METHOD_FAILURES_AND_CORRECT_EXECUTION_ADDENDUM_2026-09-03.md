# OKNO_MSK — Step 17 post-audit method failures and correct execution addendum

Date: 2026-09-03
Authority type: **job-specific Step-17 non-repeat rule / post-run method correction**
Status: **ACTIVE / REQUIRED BEFORE STEP-17 CORRECTION OR ANY FUTURE STEP-17-LIKE SEARCH-vs-GENSEARCH COMPARISON**

Parent authorities:
- `../../IMPLEMENTATION_PLAN.md`
- `../../STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`
- `../../DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md`
- `../../RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `STEP_16_METHOD_VALIDATION_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-02.md`
- `STEP_17_PRE_STEP_METHOD_REVIEW_2026-09-02.md`

---

## 1. Purpose

The external post-run audit found **three Step-17 method/output defects** even though method research had been performed before execution.

The important failure is therefore not:

```text
NO METHOD RESEARCH WAS DONE
```

The failure is:

```text
METHOD RESEARCH WAS DONE
BUT
THE RESEARCH + ORIGINAL STEP CONTRACT WERE NOT REVERSE-MAPPED COMPLETELY
INTO REQUIRED FINAL FIELDS, EVIDENCE LINKS AND QA STATES
```

Canonical root cause:

```text
RESEARCH READ
+
METHOD DISCUSSED
!=
EVERY REQUIRED OUTPUT OPERATIONALIZED AND VERIFIED
```

More specifically:

```text
IMPLEMENTATION_PLAN REQUIRED OUTPUT
-> SHOULD HAVE BEEN MAPPED TO SCHEMA FIELD
-> SHOULD HAVE BEEN MAPPED TO EXECUTION ACTION
-> SHOULD HAVE BEEN MAPPED TO FINAL LEDGER COLUMN
-> SHOULD HAVE BEEN MAPPED TO QA CHECK
```

That end-to-end reverse mapping was incomplete.

This is the same failure class already warned about by `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`:

```text
SOURCE_DISCOVERED != REQUIREMENT_OPERATIONALIZED
RESEARCH_STATEMENT != EXECUTION_CONTROL
```

but Step 17 still passed because the pre-step review verified many method rules without performing a final **original-contract-to-artifact coverage audit**.

A future Step-17-like run is blocked unless every required comparison output is traceable from original authority to final artifact.

---

# S17-M01 — Required `source-worthiness implication` was omitted from the final comparison contract

## What failed

The active KW-001 `IMPLEMENTATION_PLAN.md` requires Step Search-vs-AI comparison to classify for each AI-tested decision:

```text
ordinary Search user job
AI user job
source-type difference
commercial/explanatory difference
source-worthiness implication
material decision delta = CHANGE / DE_RISK / NO_CHANGE / INSUFFICIENT
```

Step 17 implemented the first, second, source-role, commerciality and material-delta parts, but did **not** materialize the required `source-worthiness implication` as a first-class output.

The final Step-17 ledger contains fields such as:

```text
source_role_delta
target_site_fit
materiality_reason
architecture_delta_required
```

but these answer a different question:

```text
DOES AI CHANGE PAGE RESPONSIBILITY / ARCHITECTURE?
```

They do not systematically answer:

```text
WHAT DOES THE USED GENSEARCH SOURCE SET IMPLY
ABOUT THE CONTENT / EVIDENCE / EXPERTISE / SPECIFICITY
THAT THE EXISTING TARGET PAGE SHOULD CONTAIN
TO BE A STRONG SOURCE-WORTHY ANSWER FOR THIS TASK?
```

Therefore the Step-17 result can validly say:

```text
ARCHITECTURE CHANGE = NOT REQUIRED
```

while still being unable to say:

```text
CONTENT IMPROVEMENT = NOT REQUIRED
```

The post-run wording that the site generally did not need AI-related changes was therefore stronger than the Step-17 artifact actually proved.

## Why it failed despite pre-step research

The pre-step method focused heavily on the defect inherited from Step 16:

```text
DO NOT TURN ONE GENSEARCH SNAPSHOT INTO ARCHITECTURE CHANGE
```

and on validating source **roles**:

```text
DIY / SERVICE / PRODUCT / SPECIALIST / COMPARISON / BROAD
```

That caused the execution schema to treat:

```text
SOURCE ROLE VALIDATED
```

as if it covered the full source-analysis obligation.

It did not.

The original `IMPLEMENTATION_PLAN.md` required another dimension — `source-worthiness implication` — but no reverse checklist compared every original Step-8 field against the final Step-17 ledger columns before execution authorization.

Canonical causal error:

```text
SOURCE ROLE VALIDATION
WAS INCORRECTLY TREATED AS
COMPLETE SOURCE-WORTHINESS ANALYSIS
```

## External support used in the audit

Official Yandex material:

- https://yandex.ru/support/webmaster/ru/service/alice-answers
- https://yandex.ru/support/webmaster/ru/alice

Yandex recommends examining which landing pages and useful content appear in Alice AI, how competitors solve the user task, and whether the site has sufficient useful/expert/original/substantive content.

This does **not** create a universal content recipe. It supports the need to compare the content capabilities of observed source pages with the target page when making a source-worthiness implication.

## Mandatory correction

For every Step-17 case add these fields:

```text
source_worthiness_evidence
source_worthiness_implication
content_gap_vs_used_sources
content_improvement_state
content_improvement_action_if_any
content_claim_boundary
```

Allowed `content_improvement_state`:

```text
NO_MATERIAL_CONTENT_GAP_OBSERVED
CONTENT_EXPANSION_CANDIDATE
SOURCE_WORTHINESS_GAP
INSUFFICIENT
NOT_APPLICABLE
```

These states are **separate** from architecture verdicts.

Required distinction:

```text
FINAL_STEP17_VERDICT = NO_CHANGE
CAN COEXIST WITH
CONTENT_IMPROVEMENT_STATE = CONTENT_EXPANSION_CANDIDATE
```

and:

```text
FINAL_STEP17_VERDICT = DE_RISK
DOES NOT AUTOMATICALLY MEAN
NO CONTENT GAP
```

If a case lacks an explicit source-worthiness implication:

```text
SOURCE_WORTHINESS_OUTPUT_GATE = FAILED
STEP17_ACCEPTANCE = BLOCKED
```

---

# S17-M02 — Search-side conclusions were insufficiently reverse-traced to concrete persisted SERP evidence

## What failed

The Step-17 final ledger describes ordinary Search using fields such as:

```text
ordinary_search_task
ordinary_search_content_type
ordinary_search_format
ordinary_search_angle
ordinary_search_specificity
```

but the final `evidence_refs` often point primarily to:

```text
STEP_15_SELECTED_CASES_V2.tsv#C15-xxx
```

Step 15 contains a **pre-digested baseline** derived from earlier Search work.

That is useful input, but it is not the strongest auditable reverse trace for a final Step-17 comparison claim.

A future reviewer should be able to take:

```text
ordinary_search_task = X
```

and follow it directly to the saved Search evidence rows / ranked URLs / query result artifact that justify X.

## Why it failed despite pre-step research

The pre-step review correctly said:

```text
ordinary_search_task must come from persisted Search evidence, not query wording alone
```

but the execution manifest accepted the Step-15 baseline as sufficient evidence authority without requiring a **case-level direct Search evidence reference field** in the final ledger.

Canonical causal error:

```text
UPSTREAM SUMMARY IS DERIVED FROM RAW EVIDENCE
WAS INCORRECTLY TREATED AS
UPSTREAM SUMMARY IS SUFFICIENT FINAL REVERSE TRACE
```

This is a traceability defect, not necessarily proof that the Search-side conclusions themselves are wrong.

## External support used in the audit

- https://yandex.ru/support/webmaster/ru/search-quality
- https://ahrefs.com/blog/search-intent/
- https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

Yandex supports evaluating the actual result/page usefulness for a user task. Ahrefs provides a practitioner framework around content type/format/angle. NIST supports traceable evaluation conditions/evidence and documented uncertainty.

The `type / format / angle` labels remain analyst/industry descriptions; they are not Yandex-native intent fields.

## Mandatory correction

For every Step-17 case add:

```text
ordinary_search_direct_evidence_refs
ordinary_search_observed_result_count
ordinary_search_decisive_result_refs
ordinary_search_task_derivation_note
ordinary_search_trace_state
```

Allowed trace state:

```text
DIRECT_TRACE_PASS
PARTIAL_TRACE
TRACE_MISSING
```

The final ledger may retain the Step-15 baseline as a convenience summary, but it must additionally point to the underlying Search evidence used to validate the Step-17 description.

Acceptance rule:

```text
ORDINARY_SEARCH_DIRECT_TRACE_PASS = 8/8
```

unless a case is explicitly marked `INSUFFICIENT` because the original Search evidence is not available at the required fidelity.

No paid replay is justified solely to beautify bookkeeping if the already persisted evidence can be located and referenced.

If a material Search-side field cannot be reverse-traced:

```text
SEARCH_SIDE_REVERSE_TRACE_GATE = FAILED
AFFECTED_CASE_FINAL_VERDICT = BLOCKED OR INSUFFICIENT
```

---

# S17-M03 — Adversarial self-review was partially mislabeled as independent QA

## What failed

The final QA artifact truthfully declares:

```text
qa_mode = ADVERSARIAL_SECOND_PASS
```

The same analytical process then challenged each verdict against the strongest alternative.

That is useful **adversarial self-review**.

However the acceptance vocabulary also used:

```text
INDEPENDENT_QA_BLOCKING_FINDINGS = 0
```

without a separately executed independent reviewer/process whose independence was demonstrated.

Therefore:

```text
ADVERSARIAL_SELF_REVIEW
WAS PARTIALLY RELABELLED AS
INDEPENDENT_QA
```

## Why it failed despite pre-step research

The pre-step method included NIST-inspired language about independent/adversarial review, but it did not define:

```text
WHO / WHAT COUNTS AS INDEPENDENT
```

and did not require an explicit `qa_independence_mode` field.

A generic acceptance template then inherited the older marker `INDEPENDENT_QA_BLOCKING_FINDINGS` even though the actual procedure was only a second adversarial pass by the same analytical process.

Canonical causal error:

```text
STRONGER SECOND PASS
WAS INCORRECTLY TREATED AS
INDEPENDENT REVIEW
```

## External support used in the audit

- https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

NIST supports independent review as a useful risk-reduction control. It does not mean every second pass by the same analyst is independent.

## Mandatory correction

Before Step-17 QA choose and declare exactly one mode:

```text
QA_MODE = ADVERSARIAL_SELF_REVIEW
```

or

```text
QA_MODE = INDEPENDENT_REVIEW
```

If `ADVERSARIAL_SELF_REVIEW`:

```text
ADVERSARIAL_SELF_REVIEW_BLOCKING_FINDINGS
```

is the allowed marker.

Do not use `INDEPENDENT_QA_*` terminology.

If `INDEPENDENT_REVIEW`:

persist:

```text
independent_reviewer_or_process
independence_boundary
input_artifacts
review_method
findings
```

and only then allow `INDEPENDENT_QA_*` markers.

If the QA mode is not explicit:

```text
QA_INDEPENDENCE_LABEL_GATE = FAILED
STEP17_ACCEPTANCE = BLOCKED
```

---

# 2. Why the pre-step method gate still failed

The Step-17 pre-step work did several things correctly:

```text
external method research was performed
Step16 errors were carried forward causally
GenSearch != consumer Alice was enforced
source order/count ranking was forbidden
material source roles required direct reads
reproducibility was handled cautiously
Step17/Step18 scope was reviewed
fresh provider calls were blocked by default
```

Yet three defects still escaped.

The root process failure was that pre-step validation asked mainly:

```text
IS EACH RULE WE WROTE REASONABLE?
```

but did not finally ask:

```text
DID WE ACCOUNT FOR EVERY REQUIRED OUTPUT FROM THE ORIGINAL STEP CONTRACT?
```

The missing final audit should have been:

```text
ORIGINAL IMPLEMENTATION PLAN STEP OUTPUTS
+
EXTERNAL METHOD REQUIREMENTS
+
PRIOR NON-REPEAT CONTROLS
-> ONE MASTER REQUIREMENT REGISTER
-> EVERY REQUIREMENT HAS EXECUTION FIELD
-> EVERY EXECUTION FIELD HAS FINAL ARTIFACT COLUMN
-> EVERY FINAL COLUMN HAS QA / ACCEPTANCE CHECK
```

Without that reverse coverage check, a method can be individually sensible and still incomplete.

Canonical new non-repeat rule:

```text
METHOD VALIDATION
!=
RULE-BY-RULE PLAUSIBILITY REVIEW ONLY

METHOD VALIDATION
=
SOURCE / ORIGINAL CONTRACT / PRIOR LESSONS
-> COMPLETE REQUIREMENT REGISTER
-> FORWARD TRACE
-> REVERSE TRACE
-> FINAL OUTPUT COVERAGE AUDIT
```

---

# 3. Correct Step-17 execution — mandatory step-by-step method

The following is the required Step-17 method for the correction pass and future comparable jobs.

## Phase 0 — freeze the exact Step-17 contract

### Action

Read and extract every required output from:

```text
IMPLEMENTATION_PLAN.md
current job roadmap
Step15 preregistered decision questions
Step16 corrected evidence/claim boundaries
current external method research
permanent non-repeat rules
```

Create one master requirement table.

Minimum required comparison dimensions:

```text
ordinary Search user job
AI / GenSearch user job
source-type difference
commercial / explanatory / procedural / comparison difference
specificity / taxonomy difference
source-worthiness implication
material decision delta
content improvement implication
architecture delta if justified
claim boundary
```

### Why

This prevents a required field such as `source-worthiness implication` from disappearing merely because the local method concentrated on architecture.

### Gate

```text
ORIGINAL_STEP_CONTRACT_REQUIREMENTS_ACCOUNTED = 100%
```

No analysis starts if this is not true.

---

## Phase 1 — build an evidence map for each frozen case

### Action

For each selected exact query create an evidence map before interpreting it:

```text
CASE ID / exact query
Step15 preregistered question
ordinary Search direct evidence refs
Step15 baseline summary
Step16 corrected GenSearch observation
Step16 raw GenSearch ref(s)
current target page
used=true source URLs
reproducibility state
```

### Why

Step 17 is a **comparison** step. A comparison cannot be audited if one side is only a prose summary with no direct evidence path.

### Gate

```text
SEARCH_DIRECT_TRACE_PRESENT = true
GENSEARCH_DIRECT_TRACE_PRESENT = true
```

for every case, or the case is explicitly `INSUFFICIENT`.

---

## Phase 2 — derive the ordinary Search side directly from persisted SERP evidence

### Action

Read the already persisted Yandex Search results for the exact query and record:

```text
decisive ranked result refs / URLs
observed dominant user task
content type
content format
content angle
commerciality
specificity / taxonomy
uncertainty / mixedness
```

The Step15 baseline is used as a cross-check, not as the sole final evidence reference.

### Why

The final Step17 verdict must be auditable without trusting an earlier analyst summary blindly.

### Gate

```text
ORDINARY_SEARCH_DIRECT_TRACE_PASS = 8/8
```

for the current OKNO_MSK set.

---

## Phase 3 — derive the GenSearch side from corrected raw evidence

### Action

For each case read:

```text
GenSearch answer
searchQueries[]
used=true sources
answer orientation
specificity / taxonomy
reproducibility state
```

Do not import old Step16 final labels.

### Why

Step17 owns the actual cross-surface verdict. Historical Step16 comparison labels would contaminate the comparison with already-made conclusions.

### Gate

```text
OLD_STEP16_FINAL_LABELS_USED_AS_VERDICT_INPUT = 0
```

---

## Phase 4 — direct-read material source pages and the current target page

### Action

Directly read a `used=true` source when the verdict or content implication depends on what role/content it actually has.

Read the current OKNO_MSK target page whenever comparing its capability with observed source content.

Record separately:

```text
source role
source content capabilities
specific information/features used for comparison
target page corresponding capabilities
blocked/unreadable state
```

Unreadable pages are not used decisively.

### Why

URL/title is enough to identify a returned URL, but not enough to support a material statement about content type, expertise, procedural depth or source-worthiness.

### Gate

```text
MATERIAL_SOURCE_ROLE_WITHOUT_DIRECT_VALIDATION = 0
MATERIAL_SOURCE_WORTHINESS_CLAIM_WITHOUT_DIRECT_VALIDATION = 0
MATERIAL_TARGET_CONTENT_CLAIM_WITHOUT_CURRENT_EVIDENCE = 0
```

---

## Phase 5 — compare fixed Search-vs-GenSearch axes

### Action

Compare the same fixed dimensions for all cases:

```text
TASK DELTA
COMMERCIALITY / CONTENT-MODE DELTA
SPECIFICITY / TAXONOMY DELTA
SOURCE-ROLE DELTA
TARGET-SITE FIT
REPRODUCIBILITY
```

### Why

A fixed comparison matrix prevents post-hoc reasoning where one case is judged on source count, another on answer wording and another on intuition.

### Gate

All comparison dimensions populated or explicitly `UNRESOLVED / NOT_APPLICABLE`.

---

## Phase 6 — perform the separate source-worthiness/content-gap analysis

### Action

For each case compare the content of decision-relevant GenSearch-used sources with the current target page.

Ask:

```text
What useful information/content characteristics do the used sources provide?
Does the target page already provide the same capability?
Is the difference material to solving the exact tested task?
Is the gap architectural or only within-page content?
Can the gap be proven from current evidence?
```

Record:

```text
source_worthiness_evidence
content_gap_vs_used_sources
content_improvement_state
content_improvement_action_if_any
```

### Why

An AI comparison has two different outputs:

```text
A. DOES PAGE RESPONSIBILITY / ARCHITECTURE CHANGE?
B. EVEN IF NOT, DOES EXISTING PAGE CONTENT NEED STRENGTHENING?
```

Step17 must answer both where evidence permits.

### Gate

```text
SOURCE_WORTHINESS_IMPLICATION_PRESENT = 8/8
CONTENT_IMPROVEMENT_STATE_PRESENT = 8/8
```

---

## Phase 7 — assign architecture/material verdict separately from content-improvement state

### Action

Architecture/material verdict remains:

```text
CHANGE
DE_RISK
NO_CHANGE
INSUFFICIENT
```

Content improvement remains separate:

```text
NO_MATERIAL_CONTENT_GAP_OBSERVED
CONTENT_EXPANSION_CANDIDATE
SOURCE_WORTHINESS_GAP
INSUFFICIENT
NOT_APPLICABLE
```

### Why

This prevents the false equivalence:

```text
NO ARCHITECTURE CHANGE
=
NO SITE CHANGE AT ALL
```

which the first Step17 execution accidentally encouraged in owner-facing interpretation.

### Gate

Architecture verdict and content-improvement state both exist for every case.

---

## Phase 8 — apply reproducibility and upstream-baseline gates

### Action

Keep the already-correct rule:

```text
ONE UNREPRODUCED AI SNAPSHOT
!=
SUFFICIENT AI-DRIVEN ARCHITECTURE CHANGE
```

If direct non-AI evidence independently proves the frozen upstream baseline wrong:

```text
UPSTREAM_BASELINE_CORRECTION_REQUIRED
```

Do not hide it as AI-driven `CHANGE`.

### Why

This keeps stochastic AI evidence separate from ordinary Search/current-site baseline correctness.

---

## Phase 9 — run two QA layers and label them truthfully

### Layer A — adversarial self-review

For every case:

```text
current verdict
strongest alternative verdict
what evidence could flip the decision
why current decision survives or changes
```

Marker:

```text
QA_MODE = ADVERSARIAL_SELF_REVIEW
```

### Layer B — independent review, only if actually executed

If a separate independent process/reviewer is used, record its independence explicitly.

Otherwise do **not** emit independent-QA markers.

### Why

A rigorous second pass is valuable, but calling it independent when it is not makes the audit trail stronger on paper than in reality.

### Gate

```text
QA_MODE_LABEL_MATCHES_ACTUAL_PROCESS = true
```

---

## Phase 10 — final original-contract coverage audit

### Action

Before PASS, perform a reverse audit:

For every original Step17 requirement ask:

```text
Where is the final field?
Which evidence supports it?
Which QA check validated it?
Which claim boundary controls it?
```

Required minimum:

```text
ordinary Search user job -> field + direct Search evidence refs + QA
AI user job -> field + GenSearch raw refs + QA
source-type difference -> field + source validation + QA
commercial/explanatory difference -> field + evidence + QA
source-worthiness implication -> field + content comparison + QA
material decision delta -> field + evidence + QA
content improvement implication -> field + evidence + QA
```

### Why

This is the check that was missing in the first Step17 execution.

### Gate

```text
ORIGINAL_CONTRACT_FINAL_OUTPUT_COVERAGE = 100%
REVERSE_TRACE_MISSING = 0
```

---

## Phase 11 — accept Step 17 and hand off to Step 18

Step 17 may pass only when:

```text
CASES_ACCOUNTED = 8/8
SEARCH_DIRECT_TRACE = 8/8
GENSEARCH_DIRECT_TRACE = 8/8
SOURCE_WORTHINESS_IMPLICATION = 8/8
CONTENT_IMPROVEMENT_STATE = 8/8
MATERIAL_SOURCE_VALIDATION_GAPS = 0
OLD_STEP16_LABEL_CONTAMINATION = 0
SOURCE_ORDER_RANK_INFERENCE = 0
CONSUMER_ALICE_EQUIVALENCE = 0
UNREPRODUCED_AI_ONLY_CHANGE = 0
QA_MODE_LABEL_MATCH = true
ORIGINAL_CONTRACT_FINAL_OUTPUT_COVERAGE = 100%
FINAL_GITHUB_READBACK = PASS
```

Only then:

```text
STEP17 = COMPLETE
STEP18_PRESTEP_ALLOWED = true
```

---

# 4. Correct interpretation of the current OKNO_MSK Step-17 result before correction

The existing architectural verdicts are **not automatically discarded** by this audit.

Current evidence still supports that no qualified AI-driven architecture `CHANGE` was found in the first comparison pass.

However current Step17 is reopened because it did not fully answer:

```text
WHAT CONTENT / SOURCE-WORTHINESS IMPROVEMENTS MAY STILL BE NEEDED
INSIDE THE EXISTING PAGE RESPONSIBILITIES?
```

and because Search-side direct reverse trace and QA independence labeling need correction.

Therefore current status must be:

```text
STEP17 = CORRECTION_REQUIRED
STEP18 = BLOCKED
```

until the correction pass closes these three defects and final readback passes.

No new paid Search/GenSearch request is automatically required. Existing persisted evidence should be reused first.

---

# 5. Mandatory non-repeat markers

```text
STEP17_POST_AUDIT_DEFECTS_RECORDED = true
STEP17_SOURCE_WORTHINESS_OUTPUT_REQUIRED = true
STEP17_CONTENT_IMPROVEMENT_STATE_REQUIRED = true
STEP17_SEARCH_DIRECT_REVERSE_TRACE_REQUIRED = true
STEP17_STEP15_BASELINE_NOT_SUFFICIENT_AS_SOLE_FINAL_SEARCH_TRACE = true
STEP17_ADVERSARIAL_SELF_REVIEW_NOT_EQUAL_INDEPENDENT_QA = true
STEP17_QA_MODE_MUST_MATCH_ACTUAL_PROCESS = true
STEP17_ORIGINAL_CONTRACT_FINAL_OUTPUT_COVERAGE_AUDIT_REQUIRED = true
STEP17_RULE_RESEARCH_NOT_EQUAL_COMPLETE_OPERATIONALIZATION = true
STEP17_NO_ARCHITECTURE_CHANGE_NOT_EQUAL_NO_CONTENT_CHANGE = true
STEP17_CORRECTION_REQUIRED_BEFORE_STEP18 = true
```
