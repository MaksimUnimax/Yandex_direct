# OKNO_MSK — STEP 18 PRE-STEP METHODOLOGY RESEARCH AND REVIEW

Date: 2026-09-03  
Step: 18 — Prioritization  
Status: **PRE-STEP REVIEW COMPLETE / JOB-SPECIFIC METHOD PREPARED / PERMANENT METHOD UNVALIDATED / EXECUTION NOT STARTED / OWNER AUTHORIZATION REQUIRED**

## 0. Authority and boundary

Current roadmap branch authority at preparation start:

```text
branch = roadmap/kwork-productization-2026-08-28
head = 70dc2c3d7fe91d9310bc4681e0873628d0b476ed
head_message = Promote Step 17 permanent method in rules index
```

Permanent `STEP_RULES_INDEX.md` classifies Step 18 as:

```text
Step 18 | Prioritization | UNVALIDATED
Must research/define how impact, evidence strength, public business relevance,
internal client constraints, effort and uncertainty affect priority.
```

Therefore this file is **current-job Level-2 preparation only**. It does not promote or edit permanent Step-18 methodology.

Canonical process gates applied:

- `PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md`
- `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`
- `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`
- `EVIDENCE_QUALITY_AND_PROVIDER_COST_POLICY.md`
- `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`
- `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md`
- `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md`

## 1. Whole Kwork goal

Deliver an evidence-based Yandex/Search + selective AI-search semantic and site-architecture package that tells the client:

```text
which existing URLs should own which user/search jobs;
which existing pages should be expanded or supported;
which page/task relationships should be routed or internally linked;
where overlap or uncertainty requires caution/recheck;
which actions are justified now;
what should be done first;
what evidence and limitations support every material recommendation.
```

The final output must not promise rankings, traffic, leads, Alice inclusion/citation, or stable AI visibility.

## 2. Whole roadmap state before Step 18

```text
Step 0   COMPLETE
Step 1   COMPLETE
Step 2   COMPLETE
Step 3   COMPLETE
Step 3R  COMPLETE
Step 4   COMPLETE
Step 5   COMPLETE
Step 6   COMPLETE / PRESERVED
Step 6A  COMPLETE
Step 7   COMPLETE AFTER CORRECTION
Step 8   COMPLETE AFTER METHOD CORRECTION
Step 9   COMPLETE AFTER METHOD + EXECUTION + PERSISTENCE CORRECTIONS
Step 10  COMPLETE / VERIFIED
Step 11  COMPLETE AFTER EXTERNAL AUDIT + PHRASE-LEVEL CORRECTION
Step 12  COMPLETE AFTER FAIL-CLOSED CORRECTIONS + INDEPENDENT QA
Step 13  COMPLETE / PASS_BASE_PUBLIC_EVIDENCE_MODE
Step 14  FINAL PASS
Step 14A FINAL PASS / CURRENT-SITE DISCOVERY + TOPOLOGY RECONCILIATION
Step 15  COMPLETE / V2 CORRECTED SELECTION
Step 16  COMPLETE
Step 17  COMPLETE / V3 BOUNDED DIAGNOSTIC / PERMANENT METHOD ACTIVE
Step 18  PRE-STEP ONLY — THIS FILE
Step 19  NOT STARTED
Step 20  NOT STARTED
Step 21  NOT STARTED
Step 22  NOT STARTED
```

Remaining ordered work:

```text
18 prioritization
19 client deliverables
20 final QA
21 handoff / revisions
22 job close
```

## 3. Step-18 goal

Turn the accepted current architecture and evidence from Steps 0–17 into an **auditable implementation priority register** that answers:

```text
WHAT should be done;
WHY it matters;
WHY it should be done before/after another valid action;
WHAT evidence supports the ordering;
WHAT uncertainty limits the recommendation;
WHAT must be rechecked or confirmed instead of guessed.
```

Step 18 must prioritize actions; it must not reopen completed architecture merely to create more work.

## 4. What Step 18 solves

The workflow currently contains many valid but different action/evidence classes:

- structural routing and content actions;
- current-site architecture deltas discovered in Step 14A;
- internal-link implementation edges;
- preserved no-action/defer states;
- three Step-17 content-expansion candidates;
- bounded AI evidence with different confidence/temporal scope;
- public business relevance but no private client margin/capacity priorities;
- no first-party Webmaster/Metrika/Direct performance data in the base rehearsal.

Without Step 18 these cannot be responsibly converted into a client implementation sequence.

## 5. Exact required Step-18 execution outputs

Execution is not performed by this pre-step review. When separately authorized, Step 18 must create at minimum:

```text
STEP_18_ACTION_REGISTER.tsv
STEP_18_PRIORITY_SUMMARY.tsv
STEP_18_HOLD_RECHECK_LEDGER.tsv
STEP_18_QA.json
STEP_18_REPORT.md
STEP_18_CURRENT_STATE.json
JOB_FLOW_STEP18_EXECUTION_SYNC_<DATE>.md
```

Every material action row must preserve lineage to the source architecture/evidence.

## 6. Accepted input truth and precedence

### 6.1 Canonical architecture base

Use Step 14/14A as the **current Search-architecture authority**, not an older Step-12 snapshot in isolation.

Step-14 accepted baseline before 14A:

```text
active phrases = 2332
assigned phrases = 2313
preserved unresolved = 19
structural units = 168
internal-link rows = 58
internal-link IMPLEMENT = 15
new-page actions = 0
destructive actions = 0
```

Step-12 structural action distribution consumed by Step 14:

```text
KEEP_EXISTING_STRUCTURE = 72
ROUTE_TO_EXISTING_PAGE_AS_SUBTASK = 46
DEFER_PENDING_EVIDENCE = 20
NO_STANDALONE_PAGE = 15
OUTSIDE_SCOPE_NO_ACTION = 7
ADD_SECTION_OR_FAQ_TO_EXISTING = 6
EXPAND_EXISTING_PAGE = 2
TOTAL = 168
```

Step 14A independently discovered the current site and added:

```text
CURRENT_PUBLIC_URLS = 2683
CURRENT_MINUS_UPSTREAM = 2624
ARCHITECTURE_MATERIAL_DELTAS = 21
UNCLASSIFIED = 0
MATERIAL_ERROR_UNRESOLVED = 0
```

The 21 material deltas are authoritative overlays and must all be accounted for in Step 18.

### 6.2 Step-17 AI/content overlay

Step 17 V3 current truth:

```text
8/8 = EXACT_QUERY_DIAGNOSTIC
0/8 = USER_JOB_FAMILY_SUPPORTED
7/8 = SINGLE_SNAPSHOT
1/8 = SHORT_WINDOW_REPRODUCED
0/8 = TIME_SEPARATED_REPRODUCED
0/8 = LONGITUDINAL_FIRST_PARTY_SIGNAL

architecture verdicts:
CHANGE = 0
DE_RISK = 4
NO_CHANGE = 3
INSUFFICIENT = 1

content states:
CONTENT_EXPANSION_CANDIDATE = 3
NO_MATERIAL_CONTENT_GAP_OBSERVED = 2
INSUFFICIENT = 2
NOT_APPLICABLE = 1
```

Step-17 AI evidence is an **overlay on already accepted actions/owners**, not a replacement action universe and not a sitewide AI-visibility measure.

### 6.3 Current business/private-data boundary

Accepted job scope:

```text
site = https://okno-msk.ru/
primary region = Moscow
business = manufacture / sale / installation of window and glazing products/services
B2C residential = primary test focus
standalone installation internal priority = UNKNOWN
repair/service internal acquisition priority = UNKNOWN
accessories standalone internal priority = UNKNOWN
finance internal acquisition priority = UNKNOWN
Webmaster/Metrika/Direct = unavailable for base rehearsal
```

Therefore Step 18 may use **public business relevance**, but must not invent margin, capacity, sales priority, lead value, conversion value, implementation budget, or client urgency.

## 7. Relevant prior errors / corrections and non-repeat controls

### S18-NR01 — low frequency is not low value

Permanent lesson:

```text
LOW_FREQUENCY_ALONE != PROOF_OF_IRRELEVANCE
```

Why relevant: prioritization is exactly where demand can be overread.

Control:

```text
human demand is one dimension;
no action is downgraded solely because a phrase/family has low frequency;
user-task importance, business relevance, structural risk and evidence remain separate.
```

### S18-NR02 — evaluation dimension is not an evidence route

Prior Step-8 failure invented business-review routes without an actual independent business evidence source.

Control:

```text
public business relevance = evaluation dimension;
client CRM/margin/capacity = separate evidence only if actually available;
UNKNOWN client priority remains UNKNOWN.
```

### S18-NR03 — research statement is not an execution control

Prior Step-13 lesson:

```text
SOURCE_DISCOVERED != SOURCE_OPERATIONALIZED
LIMITATION_DISCLOSED != LIMITATION_GOVERNED
```

Control: every Step-18 research finding is converted into `STEP_18_RESEARCH_TO_EXECUTION_SCHEMA.tsv` with failure policy, claim boundary, QA and acceptance check.

### S18-NR04 — evidence strength is not business impact

Step-17 V3 repaired overclaim risk by explicitly governing scope/confidence/temporal state.

Control:

```text
EVIDENCE_STRENGTH != BUSINESS_IMPACT
CONFIDENCE != IMPACT
```

Weak evidence may force `HOLD` or lower claim confidence; it does not prove that an action is commercially unimportant.

### S18-NR05 — AI diagnostic support is not stable AI visibility

Step-17 boundary:

```text
EXACT QUERY != USER JOB FAMILY
SINGLE SNAPSHOT != STABILITY
GEN_SEARCH != CONSUMER ALICE
```

Control: AI may support/de-risk/content-prioritize a current action only inside the case's allowed scope. AI alone cannot authorize architecture `CHANGE`, new page, destructive merge/delete, or a sitewide visibility claim.

### S18-NR06 — successful artifact generation is not analytical PASS

Control: Step 18 passes only after action-universe accounting, source reverse-trace, duplicate prevention, unsupported-field checks and adversarial QA all pass.

### S18-NR07 — do not resurrect superseded actions

Step14/14A currently authorize:

```text
new-page actions = 0
destructive actions = 0
```

Control: Step18 cannot reintroduce historical proposed-new pages, merges, redirects, canonical consolidations or deletions unless a later accepted upstream correction explicitly authorizes them.

### S18-NR08 — provider availability is not permission or need

Control: base Step18 reuses persisted evidence. A fresh Bridge call is allowed only if a separately recorded information-gain requirement cannot be satisfied from existing evidence and owner authorization is obtained.

## 8. Fresh external methodology research — 2026-09-03

### 8.1 OFFICIAL — Yandex EPOS / user-task quality

Source:
https://yandex.ru/support/webmaster/ru/epos

Current support:

- evaluate whether landing pages answer real user needs;
- usefulness is whether the page helps the user solve or advance a real task;
- improvement hypotheses should be tested and monitored rather than treated as guaranteed wins;
- quality is multidimensional rather than one SEO factor.

Step-18 implication:

```text
USER_TASK_IMPORTANCE and EXPECTED_USER_OUTCOME must remain explicit;
priority cannot be derived from keyword count alone.
```

### 8.2 OFFICIAL — Yandex Search quality / user objective

Source:
https://yandex.ru/support/webmaster/en/search-quality

Current support:

- Search is oriented toward full, useful, relevant information that lets users complete tasks quickly/easily;
- user-success signals and task completion matter to search-quality evaluation.

Step-18 implication: prioritization should preserve the real task/landing-role improvement represented by an action rather than optimize proxy metrics in isolation.

### 8.3 OFFICIAL / OPTIONAL ENHANCEMENT — Yandex Webmaster query statistics

Sources:
https://yandex.ru/support/webmaster/en/service/statistics
https://yandex.ru/support/webmaster/en/service/popular-queries
https://yandex.ru/support/webmaster/en/service/queries-export

Current support: first-party query/page data can provide impressions, clicks, CTR, positions, demand and query×URL evidence over time.

Current-job classification:

```text
OPTIONAL_ENHANCEMENT
access = unavailable in base rehearsal
not required for base Step18 PASS
historical performance/traffic-loss claims remain forbidden without it
```

### 8.4 OFFICIAL / OPTIONAL ENHANCEMENT — Yandex Metrika conversions

Sources:
https://yandex.ru/support/metrica/en/general/goals
https://yandex.ru/support/metrica/en/content/entry-pages

Current support: owned analytics can measure conversions and landing-page conversion behavior when configured.

Current-job classification:

```text
OPTIONAL_ENHANCEMENT
access = unavailable in base rehearsal
no conversion/revenue-based priority may be fabricated
```

### 8.5 INDUSTRY PRACTICE — separate impact, confidence and effort

Source:
https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/

Useful principle:

- impact, confidence and effort are distinct factors;
- evidence/confidence should curb unsupported high-impact guesses;
- dependencies may legitimately override simple score ordering.

Project adaptation:

```text
DO NOT IMPORT RICE FORMULA.
```

Reason: current job lacks reliable measured reach/person-month effort and permanent runbook already forbids collapsing Step18 into an unexplained magic score.

### 8.6 INDUSTRY PRACTICE — SEO roadmap impact / effort / dependencies

Source:
https://www.semrush.com/blog/seo-roadmap/

Useful principle: prioritize SEO actions using goal alignment, potential impact, implementation effort and dependencies; impact-effort matrices are an acceptable planning aid.

Project adaptation: use categorical tiers and explicit dependency roles; do not import Semrush tool metrics or Google-specific assumptions into Yandex evidence.

### 8.7 INDUSTRY PRACTICE — business potential is distinct from demand

Sources:
https://ahrefs.com/blog/keyword-strategy/
https://ahrefs.com/seo/keyword-research
https://www.semrush.com/blog/keyword-mapping/

Useful principle:

- business relevance/value must be considered alongside demand/search opportunity;
- the same demand can have different business value depending on what the business actually sells;
- keyword/page priorities should be tied to real business relevance, search demand and realistic opportunity.

Project adaptation: use only current public business scope and explicit client truth; do not infer unavailable margin/capacity/internal priority.

## 9. Configured Step-18 decision model for this job

The historical working-runbook skeleton:

```text
H = human demand
A = AI importance / decision relevance
C = commercial value
O = owned-asset value
```

is retained only as historical motivation for **separating reasons**. It is not sufficient as the executable method.

Current job uses these separate auditable dimensions:

```text
1. HUMAN_DEMAND
2. USER_TASK_IMPORTANCE
3. PUBLIC_BUSINESS_RELEVANCE
4. SEARCH_OPPORTUNITY
5. STRUCTURAL_RISK_URGENCY
6. EVIDENCE_STRENGTH
7. AI_DIAGNOSTIC_SUPPORT
8. IMPLEMENTATION_EFFORT
9. DEPENDENCY_READINESS
10. UNCERTAINTY_RECHECK_STATE
```

No dimension is silently substituted for another.

### 9.1 HUMAN_DEMAND

Source: persisted Wordstat + accepted phrase/structural-unit evidence.

Use: relative demand support only.

Forbidden:

```text
LOW DEMAND -> AUTOMATIC LOW PRIORITY
BROAD WORDSTAT -> EXACT DEMAND CLAIM
```

### 9.2 USER_TASK_IMPORTANCE

Source: accepted task/page model + Yandex task-quality principle.

Question: how materially does the action improve the user's ability to understand, choose, order, compare or solve the task represented by the structural unit?

### 9.3 PUBLIC_BUSINESS_RELEVANCE

Source: client brief where explicit + current first-party public site/business role.

Allowed states are evidence-backed categorical values with reason; `UNKNOWN` is valid.

Forbidden: inventing internal sales priority, margin, capacity or lead value.

### 9.4 SEARCH_OPPORTUNITY

Source: accepted Search-only architecture, current page fit, direct SERP evidence, content/ownership gap evidence.

This is a project-specific evaluation dimension, not a third-party keyword-difficulty score.

### 9.5 STRUCTURAL_RISK_URGENCY

Use for current evidence such as:

- wrong/missing specialist owner now corrected by Step14A;
- same-task/cannibalization candidate requiring differentiation/recheck;
- implementation prerequisite/blocker;
- current missing content/route that prevents a declared user task from being served.

Historical traffic loss is not assumed.

### 9.6 EVIDENCE_STRENGTH

Must reflect source directness, freshness, scope, completeness and relevant Step17 confidence/temporal limitations.

Canonical rule:

```text
EVIDENCE_STRENGTH controls confidence/claim eligibility.
EVIDENCE_STRENGTH does not define business impact.
```

### 9.7 AI_DIAGNOSTIC_SUPPORT

Allowed states inherit Step17 case truth and limitations.

AI can:

- support/de-risk an existing action;
- add bounded content-fit evidence;
- create a recheck trigger when evidence is insufficient.

AI cannot by itself create a new architecture change under the current job.

### 9.8 IMPLEMENTATION_EFFORT

Use an effort state only when actual implementation evidence/client estimate exists.

Default when absent:

```text
UNKNOWN
```

Forbidden:

```text
UNKNOWN -> HIGH
UNKNOWN -> LOW
page type -> guessed effort
```

If effort is unknown, it is omitted from relative tie-breaking rather than fabricated.

### 9.9 DEPENDENCY_READINESS

Allowed roles:

```text
PREREQUISITE
INDEPENDENT
DOWNSTREAM
```

A prerequisite may be scheduled before a nominally higher-impact downstream action because otherwise the downstream action cannot be correctly implemented.

### 9.10 UNCERTAINTY_RECHECK_STATE

If missing evidence or client truth prevents responsible ordering, use:

```text
HOLD
```

HOLD means `BLOCKED BY A NAMED UNCERTAINTY`, not `LOW VALUE`.

Every HOLD must have a concrete `recheck_trigger`.

## 10. Priority tiers

Allowed current-job tiers:

```text
P1_HIGH
P2_MEDIUM
P3_LATER
HOLD
```

These are project-specific planning states, not Yandex standards.

### P1_HIGH

Eligible when at least one of the following is true and no blocking uncertainty invalidates implementation:

- the action is a prerequisite/blocker for other accepted actions;
- current evidence supports high material user/business impact plus material Search/structural opportunity;
- current architecture shows a material ownership/routing/content problem requiring prompt correction.

P1 cannot be assigned solely because of high Wordstat volume or AI evidence.

### P2_MEDIUM

Valid actionable improvement with meaningful expected benefit but no prerequisite/blocker urgency, or with moderate evidence/impact relative to P1.

### P3_LATER

Valid accepted action that is not blocked but is relatively less urgent/impactful under current evidence or is intentionally downstream of prerequisites.

Low frequency alone cannot cause P3.

### HOLD

Use when a material missing client fact/evidence or unresolved boundary prevents responsible implementation ordering. HOLD is not a euphemism for rejection.

## 11. Tie-break sequence

When two actions occupy the same broad tier, use this order only as a transparent comparison aid:

```text
1. dependency/prerequisite necessity
2. user + public-business impact
3. structural risk/urgency
4. human-demand/search opportunity
5. evidence strength / uncertainty
6. implementation effort ONLY IF KNOWN
7. AI diagnostic support as bounded secondary evidence
```

No numeric weighted score is calculated.

## 12. Step-18 action-universe assembly

Execution must assemble the action universe in this order:

```text
A. current Step14/14A Search-architecture truth
B. Step14 internal-link IMPLEMENT edges
C. Step17 V3 content/AI overlays
D. current job/client constraints
```

Older Step12/13/15/16 artifacts remain lineage/evidence sources but must not be independently re-added as duplicate actions when Step14/14A already incorporated them.

### 12.1 Structural units

All 168 Step-12 V6 structural units remain in accounting.

Implementation-candidate behavior:

```text
ROUTE_TO_EXISTING_PAGE_AS_SUBTASK -> candidate
ADD_SECTION_OR_FAQ_TO_EXISTING -> candidate
EXPAND_EXISTING_PAGE -> candidate
DEFER_PENDING_EVIDENCE -> HOLD/review candidate only if later Step14A/17 evidence did not resolve it
KEEP_EXISTING_STRUCTURE -> no implementation action unless a later accepted overlay adds a distinct action
NO_STANDALONE_PAGE -> preserved no-action state
OUTSIDE_SCOPE_NO_ACTION -> preserved no-action state
```

### 12.2 Step14A material deltas

Account `21/21` by exact `delta_id`.

If a delta changes/supports an existing structural unit, update/overlay that canonical action rather than creating a duplicate.

Same-task/cannibalization candidates may produce a differentiation/recheck action, but **no destructive merge/delete/redirect/canonical action** is authorized by Step14A.

### 12.3 Internal links

Account all 58 link rows and all `15/15 IMPLEMENT` edges.

Only IMPLEMENT rows become implementation candidates. Deferred/not-applicable rows stay preserved with their reasons unless a later accepted overlay explicitly changes them.

### 12.4 Step17 overlay

Account all 8 selected cases and specifically `3/3 CONTENT_EXPANSION_CANDIDATE` states.

If a Step17 content candidate corresponds to an already existing content/structural action, attach AI/content evidence to that action instead of creating a duplicate.

`INSUFFICIENT` creates/strengthens a recheck boundary, not a guessed action.

## 13. Canonical action identity / de-duplication

Every action must have one stable canonical identity built from source lineage, action type and target/task identity.

The execution register must include:

```text
action_id
canonical_action_key
source_step_ids
source_evidence_paths
affected_structural_unit_ids
affected_delta_ids
affected_step17_case_ids
action_type
target_url_or_scope
description
```

If two upstream sources describe the same implementation change, they become one action with multiple evidence references.

## 14. Required action-register decision fields

Each material action row must contain at least:

```text
action_id
canonical_action_key
action_type
description
target_url_or_scope
source_step_ids
source_evidence_paths
human_demand
user_task_importance
public_business_relevance
search_opportunity
structural_risk_urgency
evidence_strength
ai_diagnostic_support
implementation_effort
dependency_role
depends_on_action_ids
uncertainty_state
priority_tier
priority_reason
limitations
recheck_trigger
client_confirmation_needed
```

## 15. Bridge / provider plan

Base Step18:

```text
REUSE_EXISTING_EVIDENCE = true
PLANNED_NEW_WORDSTAT_CALLS = 0
PLANNED_NEW_SEARCH_CALLS = 0
PLANNED_NEW_GENSEARCH_CALLS = 0
PLANNED_NEW_WEBMASTER_CALLS = 0
PLANNED_NEW_METRIKA_CALLS = 0
PLANNED_NEW_DIRECT_CALLS = 0
PLANNED_NEW_PAID_COST_RUB = 0
```

Bridge remains conditional only.

A fresh call may be proposed only if execution identifies one exact material priority question that cannot be resolved from persisted evidence and whose answer can change the Step18 acceptance result.

Before such a call:

```text
record exact question
record why persisted evidence is insufficient
record exact Bridge operation/query
record expected information gain
record cost/quota boundary
record persistence destination
obtain required owner authorization
execute one interaction
write result to GitHub
read back / reconcile
only then continue
```

Private Webmaster/Metrika/Direct evidence remains optional enhancement in this base rehearsal, not a silent requirement.

## 16. Adversarial self-audit of the configured method

Questions tested:

```text
Did we invent a magic score? -> NO
Did we import RICE formula without measured reach/effort? -> NO
Did we equate low frequency with low value? -> NO
Did we equate evidence strength with business impact? -> NO
Did we infer client margin/capacity/priority? -> NO
Did we infer implementation effort from page type? -> NO
Did we allow AI snapshot to create architecture change? -> NO
Did we resurrect historical new-page/destructive actions? -> NO
Did we create a non-executable evidence route? -> NO
Did we make private Yandex evidence silently mandatory? -> NO
Did we define HOLD with a real next action? -> YES
Did we require exact action lineage and de-duplication? -> YES
Did we account for dependencies? -> YES
Did we create a provider call merely because Bridge can do it? -> NO
```

Self-audit verdict:

```text
UNSUPPORTED_MATERIAL_METHOD_ELEMENTS = 0
NON_EXECUTABLE_EVIDENCE_ROUTES = 0
PROJECT_SPECIFIC_ELEMENTS_LABELLED = true
SOURCE_CLAIMS_NOT_OVEREXTENDED = true
BASE_PROVIDER_INFORMATION_GAIN_REQUIREMENT = none
PRE_STEP_METHOD_VERDICT = READY_FOR_OWNER_REVIEW
```

## 17. Expected Step-18 acceptance gate after execution

Step 18 cannot pass unless all are true:

```text
CURRENT_ACTION_UNIVERSE_ACCOUNTED = true
STRUCTURAL_UNITS_ACCOUNTED = 168/168
STEP14A_MATERIAL_DELTAS_ACCOUNTED = 21/21
STEP14_LINK_ROWS_ACCOUNTED = 58/58
STEP14_IMPLEMENT_LINKS_ACCOUNTED = 15/15
STEP17_CASES_ACCOUNTED = 8/8
STEP17_CONTENT_EXPANSION_CANDIDATES_ACCOUNTED = 3/3
SILENT_DROPS = 0
DUPLICATE_CANONICAL_ACTIONS = 0
MAGIC_NUMERIC_PRIORITY_SCORE_USED = false
PRIVATE_CLIENT_PRIORITY_GUESSES = 0
UNKNOWN_EFFORT_GUESSES = 0
AI_ONLY_ARCHITECTURE_PROMOTIONS = 0
UNAUTHORIZED_NEW_PAGE_ACTIONS = 0
UNAUTHORIZED_DESTRUCTIVE_ACTIONS = 0
EVERY_P1_P2_HAS_EVIDENCE_AND_REASON = true
EVERY_HOLD_HAS_RECHECK_TRIGGER = true
FORWARD_TRACE_PASS = true
REVERSE_TRACE_PASS = true
ADVERSARIAL_QA_PASS = true
FINAL_GITHUB_READBACK = true
```

## 18. What Step 18 explicitly does NOT decide yet

Step 18 does not:

- write the final client-facing deliverable package (Step 19);
- perform final whole-order QA (Step 20);
- claim traffic/revenue lift without owned evidence;
- claim historical cannibalization harm without first-party history;
- claim stable/sitewide Alice visibility;
- authorize a new standalone page;
- authorize merge/delete/redirect/canonical consolidation;
- guess client implementation effort or commercial priority;
- launch a provider call merely to make the analysis look more complete.

## 19. Transition

```text
PERMANENT_STEP18_METHOD = UNVALIDATED
JOB_SPECIFIC_STEP18_PRESTEP_REVIEW = COMPLETE
STEP18_SOURCE_TO_METHOD_TRACE = PREPARED
STEP18_RESEARCH_TO_EXECUTION_SCHEMA = PREPARED
STEP18_EXECUTION_MANIFEST = PREPARED_NOT_EXECUTED
STEP18_EXECUTION_STARTED = false
NEW_PROVIDER_CALLS = 0
NEW_PAID_PROVIDER_COST_RUB = 0
NEXT_LEGAL_ACTION = OWNER_AUTHORIZATION_FOR_STEP18_EXECUTION
```
