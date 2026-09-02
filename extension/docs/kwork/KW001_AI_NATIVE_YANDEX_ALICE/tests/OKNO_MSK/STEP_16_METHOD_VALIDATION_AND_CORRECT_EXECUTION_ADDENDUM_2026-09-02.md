# OKNO_MSK — Step 16 method-validation failures and correct execution addendum

Date: 2026-09-02
Authority type: **job-specific Step-16 non-repeat rule / method correction**
Status: **ACTIVE / REQUIRED BEFORE ANY FUTURE STEP-16-LIKE AI EVIDENCE ACQUISITION**
Parent authorities:
- `STEP_16_PROCESS_NON_REPEAT_RULES_2026-09-02.md`
- `STEP_16_PROCESS_NON_REPEAT_RULES_COMMAND_SURFACE_ADDENDUM_2026-09-02.md`
- `STEP_16_PROCESS_NON_REPEAT_RULES_RAW_VERBATIM_ADDENDUM_2026-09-02.md`

This addendum records **exactly four additional method-validation failures** discovered by the post-run external audit of Step 16. These four items are separate from S16-P01..S16-P09 and must not be merged into one long undifferentiated error list.

---

## Purpose

The failure was not that Step 16 produced unusable provider data. The nine GenSearch interactions are useful evidence and were preserved correctly after the raw-evidence correction.

The failure was that the **method was admitted to paid execution before four material methodological questions had been fully resolved and converted into executable controls**.

Canonical root cause:

```text
RULES / SOURCES WERE READ
BUT
UNRESOLVED METHOD QUESTIONS WERE NOT TREATED AS BLOCKERS
```

and:

```text
METHOD RESEARCH EXISTS
!=
METHOD VALIDATION COMPLETE
```

A future Step-16-like run is blocked until all four controls below are explicitly resolved in the pre-step method review and execution schema.

---

# S16-M01 — Reproducibility was under-specified before execution

## What failed

Most selected queries were executed only once. The only material candidate, C15-010, was repeated once almost immediately in the same execution session.

That is enough to show that a material direction appeared twice in a bounded test. It is **not enough** to claim stable AI behavior over time.

The label `CHANGE_CONFIRMED` was therefore too strong if read as "stable AI behavior confirmed" or "architecture change confirmed".

## Why it failed

The pre-step method review checked the GenSearch protocol and available output fields, but it did **not** first answer the experimental-design question:

```text
HOW MANY INDEPENDENT OBSERVATIONS ARE NEEDED
FOR EACH STRENGTH OF CLAIM?
```

A weak confirmation mechanism was invented operationally after the general method had already been accepted:

```text
material candidate
-> one immediate same-query repeat
```

The method never distinguished clearly between:

- one-time observation;
- short-window reproduction;
- multi-time reproduction;
- long-term stability.

## External support checked on 2026-09-02

Official Yandex documentation states that Alice AI forms a new answer from current search results and that the answer/source set may change over time for the same query:

- https://yandex.ru/support/webmaster/ru/service/alice-answers

This means one observation cannot be treated as permanent behavior.

NIST AI RMF Measure guidance supports documenting evaluation conditions, test sets and measurement methodology rather than treating one sample as an unconditional system property:

- https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

## Mandatory correction

Before any provider call, the Step-16 method must pre-register a **claim-strength-to-repeat policy**.

Minimum required distinction:

```text
ONE INITIAL OBSERVATION
-> may describe only what was observed in that run

MATERIAL DIRECTION REPRODUCED IN SHORT WINDOW
-> may say the direction reproduced in the bounded short-window test
-> MUST NOT say long-term stable

LONGER-TERM / STABILITY CLAIM
-> requires a separately pre-registered multi-time observation design
-> timing/number of runs must be defined before provider execution
```

The exact number and timing of repetitions are job-scoped and must be justified before execution. No universal magic repeat count is invented here.

For the existing OKNO_MSK C15-010 result, the correct claim boundary is:

```text
MATERIAL_AI_DIRECTION_REPRODUCED_IN_BOUNDED_SHORT_WINDOW_TEST = true
LONG_TERM_STABILITY_PROVEN = false
ARCHITECTURE_CHANGE_CONFIRMED = false
```

If the repeat policy is not defined before the first paid call:

```text
REPRODUCIBILITY_METHOD_GATE = FAILED
PROVIDER_EXECUTION = BLOCKED
```

---

# S16-M02 — Exact-query test was allowed to expand into user-job claims

## What failed

Each selected case was normally tested using one exact authoritative query string. However, later analysis sometimes described the result as evidence of how AI understands the broader **user job / intent family**.

One exact phrasing does not by itself establish behavior for all natural phrasings of the same user task.

## Why it failed

The pre-step method did not explicitly choose between two different experiments:

```text
A. EXACT-QUERY OBSERVATION
B. USER-JOB / INTENT-FAMILY OBSERVATION
```

Because this distinction was not frozen before execution, claim scope expanded after the provider answers were visible.

Canonical error:

```text
ONE EXACT QUERY RESPONSE
WAS ALLOWED TO SUPPORT
BROADER USER-JOB CLAIMS
```

## External support checked on 2026-09-02

Current AI-visibility methodologies use multiple prompts/query variants when measuring broader topic or brand behavior rather than relying on one wording only. Example methodology reviewed:

- Ahrefs Brand Radar methodology: https://ahrefs.com/blog/brand-radar-methodology/
- Semrush AI Visibility Index methodology: https://ai-visibility-index.semrush.com/methodology

These are industry methodologies, not Yandex ranking standards. They support the general evaluation principle that broader task/topic coverage requires broader prompt coverage.

## Mandatory correction

Before Step 16 execution, each selected case must declare exactly one mode:

```text
TEST_SCOPE = EXACT_QUERY
```

or

```text
TEST_SCOPE = USER_JOB
```

### If `EXACT_QUERY`

Use the exact authoritative query and restrict all claims to that wording/run family.

Allowed:

```text
"For the exact query X, GenSearch observed Y."
```

Forbidden:

```text
"AI understands the whole user task this way."
```

unless separately supported.

### If `USER_JOB`

Before provider execution, pre-register a bounded set of natural query variants representing the same user job, with a reason for each variant and a rule for combining observations.

The variants must be frozen before seeing AI results. Post-hoc prompt generation to force a preferred conclusion is forbidden.

If test scope is not explicit:

```text
QUERY_SCOPE_GATE = FAILED
PROVIDER_EXECUTION = BLOCKED
```

---

# S16-M03 — GenSearch proxy boundary was documented but not fully enforced in output semantics

## What failed

The method correctly contained the provenance restriction:

```text
GEN_SEARCH != CONSUMER_ALICE
```

However, Step 16 was still explained and summarized too broadly as if it had checked "Alice AI" behavior for the site.

The actual execution used official Yandex Search API `genSearch`. No client-private Webmaster "Visibility in Alice AI" evidence and no direct consumer-Alice evidence were available for OKNO_MSK.

## Why it failed

The rule existed as a provenance statement but was not propagated through the complete output contract:

```text
PROVENANCE RESTRICTION WAS READ
BUT
RESULT NAMING / CLAIM BOUNDARY DID NOT FULLY INHERIT IT
```

In other words, the technical data layer respected the boundary better than the owner-facing interpretation layer.

## External support checked on 2026-09-02

Official GenSearch API documentation describes the Search API generative response and its returned message, sources, used flags and search queries:

- https://aistudio.yandex.ru/ru/docs/search-api/api-ref/GenSearch/search

Yandex separately documents site visibility in Alice AI in Webmaster, including queries, pages, mentions/examples and historical statistics:

- https://yandex.ru/support/webmaster/ru/service/alice-answers

These are different evidence surfaces. GenSearch is useful official Yandex generative-search evidence, but it must not be silently relabeled as direct consumer-Alice visibility evidence.

## Mandatory correction

The Step-16 evidence mode must be declared before execution:

```text
EVIDENCE_SURFACE = YANDEX_GENSEARCH_API_PROXY
```

unless a different direct evidence surface is actually available and authorized.

For base public mode without private Webmaster/consumer evidence, owner-facing and client-facing claims must use wording equivalent to:

```text
"official Yandex GenSearch diagnostic evidence"
```

and must not claim:

```text
"the site was checked in consumer Alice AI"
"Alice will cite these pages"
"this is current Alice visibility"
```

If Webmaster Alice visibility is available in a future job, it must be preserved as a separate evidence route and never merged into GenSearch provenance.

Required distinction:

```text
GEN_SEARCH_INPUT / ANSWER / SOURCE / QUERY_OBSERVED
!=
CONSUMER_ALICE_ANSWER / SOURCE
!=
WEBMASTER_ALICE_VISIBILITY_STATISTICS
```

If output wording exceeds the actual evidence surface:

```text
EVIDENCE_SURFACE_CLAIM_GATE = FAILED
STEP_ACCEPTANCE = BLOCKED
```

---

# S16-M04 — Step 16 crossed into Step 17 comparison/decision work

## What failed

The original KW-001 implementation plan separates:

```text
AI TEST-SET SELECTION
-> OFFICIAL GENSEARCH ACQUISITION
-> SEARCH-VS-AI COMPARISON
-> FINAL SEMANTIC/PAGE ARCHITECTURE
```

In the expanded OKNO_MSK roadmap this became approximately:

```text
STEP 15 = select cases
STEP 16 = acquire AI evidence
STEP 17 = compare Search vs AI and decide material implications
```

But Step 16 itself began assigning labels such as:

```text
DE_RISK
NO_CHANGE
CHANGE_CONFIRMED
INSUFFICIENT
```

against the frozen Search baseline.

This performed part of the planned Search-vs-AI comparison before Step 17.

## Why it failed

The detailed Step-16 method was not adversarially reconciled against the original `IMPLEMENTATION_PLAN.md` before execution.

Canonical root cause:

```text
DETAILED LOCAL STEP METHOD
WAS NOT CHECKED FOR
SCOPE OVERLAP WITH THE NEXT ROADMAP STEP
```

The presence of a next-step comparison phase should have blocked any Step-16 output contract that already claimed final material decision deltas.

## Source authority

Original project implementation plan:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/IMPLEMENTATION_PLAN.md`

Canonical sequence in that plan:

```text
Step 6 — AI test-set selection
Step 7 — official GenSearch acquisition
Step 8 — Search-vs-AI comparison
Step 9 — final semantic/page architecture
```

## Mandatory correction

Future Step 16 output must separate **provider observation** from **cross-surface decision**.

### Step 16 is allowed to produce

For each case:

```text
exact input query / query set
complete GenSearch raw result
generated-answer orientation
sources and used flags
refined search queries
optional fields / transport
source-page type after direct page inspection where decision-relevant
observation confidence / ambiguity
whether an observation is material enough to require additional evidence under the pre-registered repeat policy
```

### Step 16 is NOT allowed to produce as a final architecture verdict

```text
final Search-vs-AI CHANGE
final DE_RISK
final page merge/split/new-page decision
final owner reassignment
final cannibalization decision
```

A Step-16 temporary materiality marker may exist only to trigger required additional evidence. It must be explicitly named as provisional, for example:

```text
MATERIAL_OBSERVATION_CANDIDATE
CONTROL_ANOMALY_CANDIDATE
OBSERVATION_INSUFFICIENT
```

These markers are **not** final Search-vs-AI verdicts.

### Step 17 must perform

```text
ORDINARY SEARCH BASELINE
+
STEP16 GENSEARCH OBSERVATIONS
+
CURRENT SITE/PAGE EVIDENCE
+
DIRECT ALICE/WEBMASTER EVIDENCE IF ACTUALLY AVAILABLE
->
FINAL SEARCH-VS-AI COMPARISON
->
MATERIAL DECISION DELTA
->
ARCHITECTURE / CONTENT-ROLE DECISION
```

If Step-16 method contains final Search-vs-AI decision labels before Step 17:

```text
ROADMAP_SCOPE_SEPARATION_GATE = FAILED
STEP16_EXECUTION = BLOCKED
```

---

# Correct Step-16 execution contract for the next run

The following order is mandatory before any future Step-16-like paid provider action.

## Phase 0 — method-validation preflight

Before provider execution, explicitly answer and persist:

```text
1. What exact evidence surface is being tested?
2. Is this EXACT_QUERY or USER_JOB testing?
3. If USER_JOB: what frozen prompt variants represent the job?
4. What claims are allowed from one observation?
5. What material signal requires repetition?
6. What repeat schedule/count is required for the intended claim strength?
7. What does the current evidence surface NOT prove?
8. Which outputs belong to Step 16 only?
9. Which judgments are reserved for Step 17?
10. For decision-relevant used sources, will the source page itself be directly inspected before assigning a page-role label?
```

Any unresolved answer = execution blocked.

Required markers:

```text
STEP16_EVIDENCE_SURFACE_FROZEN = true
STEP16_TEST_SCOPE_FROZEN = true
STEP16_REPEAT_POLICY_FROZEN = true
STEP16_CLAIM_BOUNDARY_FROZEN = true
STEP16_STEP17_SCOPE_BOUNDARY_FROZEN = true
STEP16_SOURCE_PAGE_INSPECTION_POLICY_FROZEN = true
```

## Phase 1 — acquire one observation

```text
frozen case/query
-> Manual YMB code/writing block
-> provider execution
-> complete verbatim raw GitHub write
-> raw readback
-> normalized provider observation
-> normalized readback
```

No final Search-vs-AI judgment yet.

## Phase 2 — inspect material used sources when needed

If the interpretation depends on a source being commercial/informational/DIY/service/specialist/broad:

```text
used=true URL
-> open/read current page
-> preserve page-role evidence
-> only then assign analytical source role
```

URL/title alone may be used as a weak descriptive hint, not as decisive page-role evidence when the conclusion is material.

## Phase 3 — apply only the pre-registered observation rule

The result may be classified only at the **observation** level, e.g.:

```text
OBSERVED_DIRECTION_COMPATIBLE
MATERIAL_OBSERVATION_CANDIDATE
CONTROL_ANOMALY_CANDIDATE
OBSERVATION_MIXED
OBSERVATION_INSUFFICIENT
```

If a material candidate triggers the repeat policy, execute exactly the pre-registered repeat design.

Do not invent additional repeats or stop conditions after seeing a preferred result.

## Phase 4 — finalize Step 16 as evidence acquisition

Step 16 final deliverable must contain:

```text
all selected cases accounted
all raw evidence persisted/read back
all normalized observations persisted/read back
all required repeats completed
exact query/test-scope accounting
provider cost accounting
evidence-surface claim boundary
observation ledger
ambiguities / insufficient cases
material observation candidates for Step 17
NO final architecture decisions
```

## Phase 5 — stop

```text
STEP16 = EVIDENCE ACQUISITION COMPLETE
STEP17 = NOT STARTED
```

A new Step-17 pre-step gate is required before Search-vs-AI comparison or architecture decisions.

---

# Correct interpretation of the existing OKNO_MSK Step-16 evidence

The existing nine provider interactions remain valid evidence and must not be discarded.

However, the old final outcome labels must not be treated as final architecture verdicts merely because they were written during Step 16.

Correct carry-forward rule:

```text
OLD STEP16 LABELS = PROVISIONAL ANALYTICAL NOTES / HISTORICAL OUTPUT
STEP17 MUST REASSESS FROM RAW + NORMALIZED EVIDENCE
```

Especially:

```text
C15-010 old label: CHANGE_CONFIRMED
correct evidence statement:
"installation/how-to material direction reproduced in two same-query observations in a short bounded window"

NOT PROVEN:
- long-term AI stability
- consumer Alice behavior
- final page ownership change
- need for a new page
```

C15-020 remains a useful example of insufficient target-site role discrimination and must not be forced into a final change/no-change conclusion without Step-17 comparison evidence.

---

# Mandatory pre-send blocking checklist

Before declaring a future Step-16 method ready, ChatGPT must answer `YES` to every item:

```text
[ ] I identified the exact external evidence surface.
[ ] I did not equate GenSearch with consumer Alice.
[ ] I declared EXACT_QUERY vs USER_JOB scope.
[ ] If USER_JOB, variants were frozen before provider results.
[ ] I defined what one observation can and cannot prove.
[ ] I defined material-repeat conditions before the first paid call.
[ ] I defined repeat timing/count appropriate to the intended claim strength.
[ ] I separated short-window reproduction from long-term stability.
[ ] I reconciled the local Step-16 method against the original implementation roadmap.
[ ] Step 16 outputs stop at evidence/observation level.
[ ] Final Search-vs-AI decision labels are reserved for Step 17.
[ ] Material source-role claims require direct inspection of used pages when needed.
[ ] All useful provider evidence will be preserved verbatim before analysis.
[ ] Provider/accounting/persistence gates are ready.
```

Any `NO` means:

```text
STEP16_METHOD_VALIDATION = FAILED
OWNER_REVIEW = BLOCKED_FROM_APPROVAL
PAID_PROVIDER_EXECUTION = BLOCKED
```

---

# Non-repeat markers

```text
STEP16_S16_M01_REPRODUCIBILITY_FAILURE_RECORDED = true
STEP16_S16_M02_EXACT_QUERY_SCOPE_FAILURE_RECORDED = true
STEP16_S16_M03_GENSEARCH_PROXY_BOUNDARY_FAILURE_RECORDED = true
STEP16_S16_M04_STEP16_STEP17_SCOPE_OVERLAP_RECORDED = true

STEP16_REPEAT_POLICY_REQUIRED_BEFORE_EXECUTION = true
STEP16_EXACT_QUERY_OR_USER_JOB_SCOPE_REQUIRED = true
STEP16_GENSEARCH_PROXY_LABEL_REQUIRED_IN_BASE_PUBLIC_MODE = true
STEP16_FINAL_SEARCH_VS_AI_VERDICT_FORBIDDEN = true
STEP16_USED_SOURCE_DIRECT_INSPECTION_REQUIRED_WHEN_MATERIAL = true
STEP16_CORRECT_EXECUTION_CONTRACT_RECORDED = true
```

---

# External references used for this correction

Official / primary:

1. Yandex Search API / GenSearch API reference  
   https://aistudio.yandex.ru/ru/docs/search-api/api-ref/GenSearch/search
2. Yandex Webmaster — site visibility in Alice AI  
   https://yandex.ru/support/webmaster/ru/service/alice-answers
3. NIST AI RMF — Measure  
   https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

Industry methodology used only for prompt-coverage/evaluation-design context:

4. Ahrefs Brand Radar methodology  
   https://ahrefs.com/blog/brand-radar-methodology/
5. Semrush AI Visibility Index methodology  
   https://ai-visibility-index.semrush.com/methodology

Project authority for roadmap separation:

6. `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/IMPLEMENTATION_PLAN.md`

Claim boundary:

```text
OFFICIAL YANDEX / NIST SOURCES SUPPORT THE CORE EVIDENCE-SURFACE AND EVALUATION-BOUNDARY CONTROLS.
AHREFS / SEMRUSH SUPPORT ONLY GENERAL INDUSTRY PRACTICE FOR BROADER PROMPT/TOPIC COVERAGE.
THE EXACT KW-001 STEP16/STEP17 SEPARATION IS PROJECT-SPECIFIC AND COMES FROM IMPLEMENTATION_PLAN.md.
```
