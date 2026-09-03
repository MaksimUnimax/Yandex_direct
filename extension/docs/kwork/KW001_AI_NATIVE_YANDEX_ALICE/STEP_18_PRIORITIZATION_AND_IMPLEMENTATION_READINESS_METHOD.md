# KW-001 — STEP 18 PRIORITIZATION AND IMPLEMENTATION-READINESS METHOD

Date: 2026-09-03  
Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-AUTHORIZED AFTER EXTERNAL METHOD AUDIT**

This file is the permanent Step-18 authority. It is reusable across unrelated client sites, industries and semantic corpora.

Concrete client domains, URLs, product names, page families, row counts, action IDs, provider results, private business facts and job-specific priority results belong only in `tests/<CASE_ID>/` or another declared Level-2 job workspace.

---

## 1. Step purpose

Step 18 converts the accepted upstream action/evidence universe into an auditable priority model and, when the required implementation inputs exist, into an implementation-ready execution order.

It must answer two different questions without conflating them:

```text
A. IDEAL ANALYTICAL PRIORITY
= based on current evidence, which actions appear more important to address and why?

B. EXPECTED IMPLEMENTATION PRIORITY
= after real owner, effort, capacity, dependencies, business importance and measurement readiness are known, in what order can the organization actually execute them?
```

Canonical distinction:

```text
IDEAL_ANALYTICAL_PRIORITY != IMPLEMENTATION_READY_ORDER
```

A job may legitimately complete Step 18 in `ANALYTICAL_PRIORITY_MODE` when the sold deliverable is prioritized recommendations and real implementation data is unavailable. In that mode the output must be labelled as analytical priority, not as a production-ready implementation schedule.

If the sold scope promises an implementation-ready roadmap, missing implementation calibration blocks that stronger claim.

---

## 2. External method origin and what it supports

### Search Engine Land — SEO roadmap / SCOPE, 2026-08-25

https://searchengineland.com/turn-seo-backlog-into-roadmap-485713

Industry-practice support for distinguishing a backlog from an executable roadmap and considering strategic alignment, confidence/delivery feasibility, ownership, potential impact, effort/elapsed time, measurement and sequencing.

### Aleyda Solis — actionable SEO audit / prioritization

https://www.aleydasolis.com/en/search-engine-optimization/how-to-winning-seo-website-audit-growth/

Industry-practice support for separating an ideal priority based on expected impact from an expected priority calibrated by implementation difficulty/resources and stakeholder reality.

### Aleyda Solis — content prioritization in an AI-search era, 2026

https://www.aleydasolis.com/en/ai-search/content-prioritization-ai-search/

Industry-practice support for keeping traffic/click opportunity, AI citation/mention opportunity and business value as separate dimensions and adapting priority to actual site/business data rather than treating AI visibility as business impact by itself.

### Semrush — SEO roadmap

https://www.semrush.com/blog/seo-roadmap/

Industry-practice support for goal alignment, potential impact, effort and dependencies as distinct roadmap considerations.

### Ahrefs — SEO roadmap

https://ahrefs.com/blog/seo-roadmap/

Industry-practice support for impact/effort prioritization, appropriately granular work items and reprioritization when implementation facts/results change.

### Intercom — RICE prioritization

https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/

Transferred product-prioritization support for keeping impact, confidence and effort conceptually separate. The RICE formula itself is **not** a mandatory KW-001 formula.

### Official Yandex — user-task/content quality and query metrics

https://yandex.ru/support/webmaster/ru/epos  
https://yandex.ru/support/webmaster/ru/service/popular-queries  
https://yandex.ru/support/webmaster/ru/service/queries-export

Official support for focusing on real user task/usefulness and, when client-owned evidence is available, measuring query/page outcomes through impressions, clicks, positions and related first-party search metrics.

### Official Yandex Metrika — goals

https://yandex.ru/support/metrica/ru/general/goals

Official support for post-implementation goal/conversion measurement when configured and available in the current client scope.

External sources do **not** prescribe one universal numeric SEO priority formula, one fixed number of actions, or one fixed implementation horizon.

---

## 3. Permanent failure history — what failed, why it failed, and what prevents recurrence

A permanent lesson is useful only when the causal chain is preserved. Do not reduce this section to a checklist of mistakes.

### E18-01 — ideal analytical priority was overstated as an implementation-ready order

**What failed**

A prior execution correctly ranked actions using evidence, demand, user-task importance, public business relevance, structural urgency, dependencies and uncertainty, while leaving unknown implementation effort unguessed. The end report nevertheless described the result too strongly as a ready order of real implementation work.

**Root cause**

```text
ANALYTICAL PRIORITY MODEL
+ UNKNOWN IMPLEMENTATION VARIABLES
WAS ALLOWED TO PRODUCE
IMPLEMENTATION-READY WORDING
```

The method had a field for effort, but did not make missing real owner/effort/capacity information mechanically change the allowed output claim.

**Corrected control**

Every action has two separate states:

```text
IDEAL_PRIORITY_TIER
EXPECTED_IMPLEMENTATION_PRIORITY
```

If implementation calibration is missing:

```text
EXPECTED_IMPLEMENTATION_PRIORITY = PENDING_CALIBRATION
IMPLEMENTATION_READY_STATE = NOT_READY__MISSING_IMPLEMENTATION_INPUTS
```

The analytical layer may still PASS when that is the sold scope, but it may not be described as a production-ready schedule.

---

### E18-02 — “do not guess effort” was treated as sufficient, but no calibration workflow followed

**What failed**

Unknown effort was honestly preserved as `UNKNOWN`, but the process stopped there.

**Root cause**

The safety rule prevented fabrication but the schema contained no second-stage mechanism for obtaining or recording real implementation difficulty.

```text
NO_GUESS_CONTROL
WAS MISTAKEN FOR
IMPLEMENTATION_CALIBRATION_COMPLETE
```

**Corrected control**

For every action intended for implementation-ready ordering, preserve:

```text
implementation_effort_state
implementation_effort_value_or_band
effort_evidence_source
```

Allowed evidence sources include an implementer estimate, client estimate, historical delivery evidence, measured task effort or another explicit current-job source. Analyst intuition is not sufficient evidence for a client-specific effort claim.

---

### E18-03 — execution owner, capacity and elapsed-time constraints were missing

**What failed**

The priority register identified what mattered but did not say who could execute each item, whether that owner had capacity, or the realistic delivery window.

**Root cause**

Step 18 was designed as analyst ranking rather than as a two-layer decision between analytical importance and organizational executability.

**Corrected control**

Implementation-ready actions require explicit fields:

```text
execution_owner_role
owner_confirmation_state
capacity_state
timeline_or_delivery_window
dependency_readiness
```

Unknown values remain explicit and prevent an implementation-ready claim when the current scope requires one.

---

### E18-04 — uncertainty recheck triggers were mistaken for a measurement plan

**What failed**

The process correctly defined when uncertain decisions should be revisited, but did not separately define how completed actions would be measured for success or failure.

**Root cause**

```text
UNCERTAINTY GOVERNANCE
WAS TREATED AS IF IT ALSO COVERED
POST-IMPLEMENTATION OUTCOME MEASUREMENT
```

A `recheck_trigger` answers “when can we reconsider this uncertain decision?” It does not answer “how will we know the implemented action worked?”

**Corrected control**

Every implementation-ready action must preserve, where applicable:

```text
expected_outcome
success_metric
baseline_state
measurement_source
measurement_window
measurement_readiness
post_implementation_review_trigger
```

If a baseline/source is unavailable, record that limitation. Never invent a pre-change baseline or promised uplift.

---

### E18-05 — accounting batches were allowed to masquerade as executable work items

**What failed**

A large number of accepted routing actions were represented by one aggregate action row. This was valid for accounting, but too coarse for practical implementation.

**Root cause**

```text
ACCOUNTING CONVENIENCE
WAS ALLOWED TO SUBSTITUTE FOR
WORK-ITEM GRANULARITY
```

A batch proves nothing was lost; it does not prove that an executor can estimate, assign, implement or verify that batch as one task.

**Corrected control**

Maintain two representations when needed:

```text
ACCOUNTING_BATCH
IMPLEMENTATION_WORK_PACKAGE(S)
```

Implementation work packages must be decomposed to a manageable level using real shared execution properties such as target page/family, source page/family, implementation owner, dependency, template, content block or delivery wave. Every source action/unit must retain exact membership traceability.

---

### E18-06 — public business relevance was not explicitly separated from client-confirmed business importance in the final priority claim

**What failed**

The analytical layer correctly refused to guess margin, capacity, lead value or internal strategic importance. But the final wording did not always make clear that public business relevance is not the same as client-confirmed internal business priority.

**Root cause**

The method had a non-guess rule but no explicit calibration state controlling the stronger client-business claim.

**Corrected control**

Preserve separately:

```text
PUBLIC_BUSINESS_RELEVANCE
CLIENT_BUSINESS_IMPORTANCE_STATE = CONFIRMED | UNAVAILABLE | NOT_REQUIRED
CLIENT_BUSINESS_IMPORTANCE
```

Public relevance may support ideal analytical priority. Client-confirmed business importance may alter expected implementation priority when available and in scope.

---

### E18-07 — detailed technical reporting substituted for the mandatory plain-language owner summary

**What failed**

A technically detailed pre-step/status report was treated as sufficient even though the universal owner-communication gate requires a separate non-specialist summary.

**Root cause**

```text
TECHNICAL COMPLETENESS
WAS MISTAKEN FOR
OWNER COMPREHENSION
```

**Corrected control**

`STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md` is mandatory. Before authorization and after execution, Step18 must end with the dedicated plain-language `why / what we do / what we get` summary. Missing summary blocks transition.

---

## 4. Priority model — keep dimensions separate

Do not collapse the following into an unexplained score:

```text
HUMAN_DEMAND
USER_TASK_IMPORTANCE
PUBLIC_BUSINESS_RELEVANCE
SEARCH_OPPORTUNITY
STRUCTURAL_RISK_URGENCY
EVIDENCE_STRENGTH
AI_DIAGNOSTIC_SUPPORT
IMPLEMENTATION_EFFORT
DEPENDENCY_READINESS
UNCERTAINTY_RECHECK_STATE
CLIENT_BUSINESS_IMPORTANCE when available
CAPACITY / OWNER READINESS when implementation-ready mode applies
MEASUREMENT_READINESS when implementation-ready mode applies
```

Canonical rules:

```text
LOW_FREQUENCY != LOW_VALUE
EVIDENCE_STRENGTH != BUSINESS_IMPACT
CONFIDENCE != IMPACT
AI_DIAGNOSTIC_SUPPORT != STABLE_AI_VISIBILITY
UNKNOWN_CLIENT_PRIORITY != GUESSED_PRIORITY
UNKNOWN_EFFORT != LOW_EFFORT
UNKNOWN_OWNER != ASSIGNABLE
PROVIDER_CAPABILITY != PROVIDER_NEED
RECHECK_TRIGGER != SUCCESS_METRIC
```

A numeric scoring framework such as RICE may be used only if its inputs are real, the current job needs such a model, every component is traceable, and the score does not hide dependencies or required prerequisite work. No magic numerical score is mandatory.

---

## 5. Step18 execution modes

Declare one mode before execution.

### ANALYTICAL_PRIORITY_MODE

Use when the deliverable is prioritized recommendations and real implementation ownership/effort/capacity data are unavailable or outside scope.

Required output:

```text
IDEAL_ANALYTICAL_PRIORITY = COMPLETE
EXPECTED_IMPLEMENTATION_PRIORITY = PENDING_CALIBRATION where required inputs are unavailable
```

This mode may PASS if claims are bounded correctly.

### IMPLEMENTATION_READY_ROADMAP_MODE

Use when the promised output is an operational roadmap/schedule.

Requires real calibration for material executable actions:

```text
OWNER
EFFORT
CAPACITY
DEPENDENCIES
DELIVERY WINDOW / ELAPSED TIME
CLIENT BUSINESS IMPORTANCE when material
MEASUREMENT PLAN
```

Missing required calibration prevents full implementation-readiness PASS.

---

## 6. Correct full Step18 workflow

### Phase 0 — goal/status/error review before method execution

Follow `PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md` and `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`.

Before external method work or execution, state:

```text
WHOLE KWORK GOAL
FULL ROADMAP
COMPLETED WORK
REMAINING WORK
STEP18 GOAL
STEP18 REQUIRED OUTPUT
KNOWN PRIOR STEP18 FAILURES
ROOT CAUSES
NON-REPEAT CONTROLS
```

Then perform current external method research, source-to-method trace, research-to-execution schema, adversarial self-audit and mandatory plain-language owner summary. Obtain owner authorization where required.

### Phase 1 — freeze the complete accepted action universe

Read only current accepted upstream authorities and later overlays.

Predeclare all required accounting universes, for example:

```text
STRUCTURAL ACTIONS
CURRENT-SITE DELTAS / OVERLAYS
INTERNAL-LINK ACTIONS
AI/CONTENT OVERLAYS
UNRESOLVED/HOLD ITEMS
CLIENT CONSTRAINTS
```

A superseded historical action must not be reintroduced merely because it exists in an older artifact.

### Phase 2 — canonicalize and de-duplicate actions

One real proposed implementation change receives one canonical action key. Multiple evidence sources may support the same action.

```text
ONE IMPLEMENTATION CHANGE = ONE CANONICAL ACTION
MANY EVIDENCE REFS ARE ALLOWED
```

Do not double-count the same change because it appears in Search, AI, structural and current-site evidence.

### Phase 3 — classify non-actions and HOLD explicitly

Preserve accepted no-action states and unresolved states.

`HOLD` requires:

```text
NAMED BLOCKING UNCERTAINTY
+ CONCRETE RECHECK TRIGGER
```

HOLD is not low value, rejection or a hidden no-action judgment.

### Phase 4 — assign analytical dimensions

For every canonical action evaluate only supported dimensions. Preserve unknowns rather than filling them from intuition.

At minimum:

```text
human_demand
user_task_importance
public_business_relevance
search_opportunity
structural_risk_urgency
evidence_strength
ai_diagnostic_support
uncertainty_state
```

Implementation effort may be recorded here only when a real source already exists; otherwise `UNKNOWN`.

### Phase 5 — build the dependency graph

Classify actions as applicable:

```text
PREREQUISITE
INDEPENDENT
DOWNSTREAM
```

Record explicit `depends_on_action_ids` or equivalent relationships.

Check for cycles and impossible dependency states.

Dependencies can legitimately move a prerequisite before a nominally higher-impact downstream task.

### Phase 6 — assign IDEAL analytical priority

Assign categorical tiers such as:

```text
P1_HIGH
P2_MEDIUM
P3_LATER
HOLD
```

or another declared equivalent.

When two actions fall into the same broad tier, a strong default tie-break is:

```text
1. dependency / prerequisite necessity
2. user-task + public-business impact
3. structural risk / urgency
4. human demand + search opportunity
5. evidence strength / uncertainty
6. implementation effort ONLY IF KNOWN
7. bounded AI diagnostic support
```

The result of this phase is `IDEAL_ANALYTICAL_PRIORITY`, not yet necessarily a production schedule.

### Phase 7 — decompose accounting batches into implementation work packages

Any aggregate action that contains multiple independently executable changes must be decomposed before implementation-ready ordering.

Group only by real shared execution properties, for example:

```text
same target owner/page family
same source page/template
same responsible team
same technical/content mechanism
same prerequisite
same deployment/review wave
```

Preserve exact membership so:

```text
SOURCE ACTIONS / UNITS
-> WORK PACKAGE
-> IMPLEMENTATION TASK
```

remains reversible.

### Phase 8 — implementation calibration

For every executable work package collect or classify:

```text
execution_owner_role
owner_confirmation_state
implementation_effort_state
implementation_effort_value_or_band
effort_evidence_source
capacity_state
client_business_importance_state
client_business_importance
dependency_readiness
timeline_or_delivery_window
```

Do not fabricate missing values.

If current sold scope is analytical only, missing calibration does not invalidate ideal priority; it limits the output claim.

If current sold scope promises implementation-ready ordering, missing material calibration blocks that stronger output.

### Phase 9 — assign EXPECTED implementation priority

Only after calibration may Step18 emit a real implementation order/wave.

Possible states:

```text
READY_WAVE_1
READY_WAVE_2
READY_LATER
BLOCKED_DEPENDENCY
PENDING_CLIENT_OR_IMPLEMENTER_CALIBRATION
HOLD_EVIDENCE
```

Exact labels are project-configurable.

A high ideal priority can become later expected priority if an unresolved prerequisite, unavailable owner or real effort/capacity constraint requires it. This must be visible, not hidden inside a score.

### Phase 10 — create the measurement plan

For every executable material action/work package define:

```text
expected_outcome
success_metric
baseline_state
measurement_source
measurement_window
measurement_readiness
post_implementation_review_trigger
```

Possible measurement sources include current-site verification, literal internal-link verification, Yandex Webmaster query/page metrics, Metrika goals/conversions or another explicit client-approved source.

Measurement scope must match evidence availability. A public-only job must not invent private analytics baselines.

### Phase 11 — run full accounting and adversarial QA

At minimum verify:

```text
ALL REQUIRED SOURCE UNIVERSES ACCOUNTED
SILENT DROPS = 0
DUPLICATE CANONICAL ACTIONS = 0
UNSUPPORTED PRIORITY PROMOTIONS = 0
LOW DEMAND AS SOLE DOWNGRADE = 0
EVIDENCE STRENGTH SUBSTITUTED FOR BUSINESS IMPACT = 0
PRIVATE CLIENT PRIORITY GUESSES = 0
UNKNOWN EFFORT GUESSES = 0
AI-ONLY ARCHITECTURE PROMOTIONS = 0
UNAUTHORIZED NEW-PAGE ACTIONS = 0
UNAUTHORIZED DESTRUCTIVE ACTIONS = 0
EVERY HOLD HAS RECHECK TRIGGER
EVERY P1/P2 HAS EVIDENCE + REASON + LIMITATION
ACCOUNTING BATCHES CLAIMED AS IMPLEMENTATION-READY = 0
IMPLEMENTATION-READY ACTIONS WITHOUT OWNER/EFFORT/CAPACITY WHEN REQUIRED = 0
IMPLEMENTATION-READY ACTIONS WITHOUT MEASUREMENT PLAN WHEN REQUIRED = 0
FORWARD TRACE = PASS
REVERSE TRACE = PASS
```

### Phase 12 — persist, read back, then report

Required current-job artifacts should include equivalent forms of:

```text
ACTION REGISTER
IDEAL PRIORITY SUMMARY
HOLD / RECHECK LEDGER
IMPLEMENTATION CALIBRATION LEDGER
WORK-PACKAGE / DECOMPOSITION LEDGER when batching exists
MEASUREMENT PLAN
QA
REPORT
CURRENT STATE
JOB FLOW UPDATE
FINAL GITHUB READBACK QA
```

Do not set final COMPLETE in the same unverified write that creates the closure candidate.

Preferred closure:

```text
WRITE CANDIDATE OUTPUTS
-> GITHUB READBACK
-> VERIFY ACCOUNTING / CLAIMS / MODE
-> UPDATE FINAL STATE
-> FINAL READBACK
-> END-OF-STEP PLAIN-LANGUAGE SUMMARY
```

---

## 7. Required action/work-package fields

A strong reusable schema includes:

```text
action_id
canonical_action_key
work_package_id
action_type
description
target_or_scope
source_step_ids
source_evidence_paths
affected_upstream_ids
human_demand
user_task_importance
public_business_relevance
search_opportunity
structural_risk_urgency
evidence_strength
ai_diagnostic_support
uncertainty_state
dependency_role
depends_on_action_ids
ideal_priority_tier
ideal_priority_reason
execution_owner_role
owner_confirmation_state
implementation_effort_state
implementation_effort_value_or_band
effort_evidence_source
capacity_state
client_business_importance_state
client_business_importance
timeline_or_delivery_window
expected_implementation_priority
implementation_ready_state
expected_outcome
success_metric
baseline_state
measurement_source
measurement_window
measurement_readiness
limitations
recheck_trigger
post_implementation_review_trigger
client_confirmation_needed
```

Not every field must be populated with a known value. The schema exists so missing implementation truth becomes explicit instead of silently disappearing.

---

## 8. Claim boundaries

```text
HIGH ANALYTICAL PRIORITY
!= HIGH CLIENT REVENUE IMPACT

IDEAL PRIORITY
!= GUARANTEED IMPLEMENTATION ORDER

IMPLEMENTATION EFFORT UNKNOWN
!= EASY
!= HARD

PUBLIC BUSINESS RELEVANCE
!= CLIENT-CONFIRMED STRATEGIC PRIORITY

SEARCH / AI OPPORTUNITY
!= GUARANTEED RANKING / TRAFFIC / CITATION / REVENUE

MEASUREMENT PLAN
!= PROMISED POSITIVE RESULT
```

When private Webmaster/Metrika/CRM/business inputs are unavailable, state that limitation mechanically in the output mode and fields.

---

## 9. Provider / Bridge rule

Step18 normally reuses persisted upstream evidence.

A fresh provider call is allowed only when:

```text
NAMED MISSING INFORMATION
+ CURRENT PERSISTED EVIDENCE CANNOT ANSWER IT
+ THE RESULT CAN CHANGE PRIORITY / CALIBRATION / CLAIM ELIGIBILITY
+ EXACT PROVIDER OPERATION IS DECLARED
+ COST / AUTHORIZATION GATE PASSES
+ BRIDGE PERSISTENCE GATE WILL BE APPLIED
```

Provider availability alone never justifies a call.

For implementation calibration, client/implementer input is often the correct source for owner/effort/capacity rather than Search/Wordstat/AI provider evidence.

---

## 10. Pass gates

### Analytical-priority pass

```text
STEP18_ANALYTICAL_PRIORITIZATION_PASS = true
```

only when:

```text
complete accepted action universe accounted
canonical actions deduplicated
analytical dimensions evidence-derived
unknowns preserved
HOLD governed by blocker + trigger
dependencies materialized
ideal priority assigned
claim boundaries explicit
full QA + readback pass
plain-language owner summary present
```

### Implementation-readiness pass

```text
STEP18_IMPLEMENTATION_READINESS_PASS = true
```

only when the current mode requires it and every material executable work package has sufficient real:

```text
owner
owner confirmation
implementation effort evidence
capacity state
dependency readiness
delivery window / elapsed-time expectation
client business importance when material to the promised ordering
measurement plan / readiness
```

If those inputs are unavailable:

```text
ANALYTICAL_PRIORITY_MODE may still PASS
IMPLEMENTATION_READY_ROADMAP claim = FORBIDDEN
EXPECTED_IMPLEMENTATION_PRIORITY = PENDING_CALIBRATION where applicable
```

---

## 11. Source-to-method trace summary

```text
Search Engine Land SCOPE
-> ownership/capacity/impact/effort/measurement/sequencing are execution-roadmap dimensions

Aleyda ideal vs expected priority
-> separate evidence-based ideal importance from real-world implementation priority

Semrush/Ahrefs roadmap practice
-> goal alignment + impact + effort + dependencies + manageable work-item granularity

Intercom RICE
-> confidence/evidence strength must not be silently collapsed into impact; formula not mandatory

Yandex EPOS
-> real user task/usefulness remains a valid impact dimension

Yandex Webmaster/Metrika
-> first-party search and goal metrics are valid measurement sources when available

prior controlled Step18 execution + external audit
-> no-guess controls alone did not make an analytical priority register implementation-ready
```

---

## 12. Permanent non-repeat markers

```text
KW001_STEP18_METHOD_ACTIVE = true
KW001_STEP18_IDEAL_PRIORITY_NOT_EQUAL_IMPLEMENTATION_ORDER = true
KW001_STEP18_ANALYTICAL_AND_IMPLEMENTATION_PRIORITY_SEPARATE = true
KW001_STEP18_UNKNOWN_EFFORT_NOT_GUESSED = true
KW001_STEP18_UNKNOWN_EFFORT_REQUIRES_CALIBRATION_FOR_IMPLEMENTATION_READY_MODE = true
KW001_STEP18_EXECUTION_OWNER_AND_CAPACITY_REQUIRED_FOR_IMPLEMENTATION_READY_MODE = true
KW001_STEP18_CLIENT_BUSINESS_IMPORTANCE_SEPARATE_FROM_PUBLIC_RELEVANCE = true
KW001_STEP18_RECHECK_TRIGGER_NOT_EQUAL_SUCCESS_METRIC = true
KW001_STEP18_MEASUREMENT_PLAN_REQUIRED_FOR_IMPLEMENTATION_READY_MODE = true
KW001_STEP18_ACCOUNTING_BATCH_NOT_EQUAL_IMPLEMENTABLE_WORK_ITEM = true
KW001_STEP18_WORK_PACKAGE_DECOMPOSITION_REQUIRED_WHEN_BATCH_IS_TOO_COARSE = true
KW001_STEP18_HOLD_NOT_EQUAL_LOW_VALUE = true
KW001_STEP18_NO_MAGIC_SCORE_REQUIRED = true
KW001_STEP18_AI_SUPPORT_NOT_EQUAL_AI_ARCHITECTURE_AUTHORITY = true
KW001_STEP18_PROVIDER_CAPABILITY_NOT_EQUAL_PROVIDER_NEED = true
KW001_STEP18_PLAIN_LANGUAGE_SUMMARY_REQUIRED = true
KW001_STEP18_JOB_SPECIFIC_RESULTS_FORBIDDEN_IN_PERMANENT_METHOD = true
```
