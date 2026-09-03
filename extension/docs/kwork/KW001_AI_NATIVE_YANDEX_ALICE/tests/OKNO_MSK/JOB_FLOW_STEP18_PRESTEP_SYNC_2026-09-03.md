# OKNO_MSK job flow sync — Step 18 pre-step preparation

Date: 2026-09-03

Status: **STEP18 PRE-STEP COMPLETE / EXECUTION NOT STARTED / OWNER AUTHORIZATION REQUIRED**

This overlay supersedes older `JOB_FLOW.md` / prior step-status lines where they conflict with the current accepted state. It does not rewrite permanent methodology.

## Full roadmap status

| Step | Status | Current note |
|---|---|---|
| 0 | ✅ COMPLETE | Scope/order freeze |
| 1 | ✅ COMPLETE | Cross-channel current-site/business discovery |
| 2 | ✅ COMPLETE | Seed/acquisition plan |
| 3 | ✅ COMPLETE | Wordstat acquisition |
| 3R | ✅ COMPLETE | Durable recovery/reconciliation |
| 4 | ✅ COMPLETE | Family triage |
| 5 | ✅ COMPLETE | Targeted expansion |
| 6 | ✅ COMPLETE / PRESERVED | Demand dynamics |
| 6A | ✅ COMPLETE | Acquisition coverage revalidation |
| 7 | ✅ COMPLETE AFTER CORRECTION | Row-level semantic cleanup |
| 8 | ✅ COMPLETE AFTER METHOD CORRECTION | Search-stage semantic freeze |
| 9 | ✅ COMPLETE AFTER METHOD + EXECUTION + PERSISTENCE CORRECTIONS | Ordinary Yandex Search validation |
| 10 | ✅ COMPLETE / VERIFIED | User-task / SERP clustering |
| 11 | ✅ COMPLETE AFTER EXTERNAL AUDIT + PHRASE-LEVEL CORRECTION | Page ownership / phrase-to-page mapping |
| 12 | ✅ COMPLETE AFTER FAIL-CLOSED CORRECTIONS + INDEPENDENT QA | Structural actions / internal-link plan |
| 13 | ✅ COMPLETE / PASS_BASE_PUBLIC_EVIDENCE_MODE | Competing-page / cannibalization diagnosis |
| 14 | ✅ FINAL PASS | Search-only architecture freeze |
| 14A | ✅ FINAL PASS | Independent current-site discovery / topology / 21 material architecture deltas |
| 15 | ✅ COMPLETE / V2 CORRECTED | AI-case selection: 25 reviewed / 8 selected / 16 rejected / 1 hold |
| 16 | ✅ COMPLETE | Selective GenSearch evidence acquisition |
| 17 | ✅ COMPLETE / V3 BOUNDED DIAGNOSTIC | Search-vs-AI comparison; permanent Step17 method active |
| 18 | 🟡 PRE-STEP COMPLETE / AWAITING OWNER AUTHORIZATION | Method research + trace + schema + draft manifest complete; prioritization not executed |
| 19 | ⬜ NOT STARTED | Client deliverables; blocked by Step18 |
| 20 | ⬜ NOT STARTED | Final QA; blocked |
| 21 | ⬜ NOT STARTED | Handoff / revisions; blocked |
| 22 | ⬜ NOT STARTED | Job close; blocked |

## Step18 preparation artifacts

```text
STEP_18_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW_2026-09-03.md
STEP_18_SOURCE_TO_METHOD_TRACE.tsv
STEP_18_RESEARCH_TO_EXECUTION_SCHEMA.tsv
STEP_18_EXECUTION_MANIFEST_DRAFT_2026-09-03.json
STEP_18_CURRENT_STATE.json
```

## Step18 prepared method summary

```text
PERMANENT_STEP18_METHOD = UNVALIDATED
JOB_SPECIFIC_STEP18_METHOD = PREPARED_FOR_CURRENT_JOB_ONLY
PRIORITY_MODEL = CATEGORICAL / AUDITABLE / NO MAGIC SCORE
TIERS = P1_HIGH / P2_MEDIUM / P3_LATER / HOLD
DEPENDENCY_ROLES = PREREQUISITE / INDEPENDENT / DOWNSTREAM
```

Separate decision dimensions:

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
```

Canonical non-repeat boundaries:

```text
LOW_FREQUENCY != LOW_VALUE
EVIDENCE_STRENGTH != BUSINESS_IMPACT
CONFIDENCE != IMPACT
AI_DIAGNOSTIC_SUPPORT != STABLE_AI_VISIBILITY
NO_ARCHITECTURE_CHANGE != NO_CONTENT_CHANGE
UNKNOWN_CLIENT_PRIORITY != GUESSED_PRIORITY
UNKNOWN_EFFORT != GUESSED_EFFORT
PROVIDER_CAPABILITY != PROVIDER_NEED
```

## Current action/evidence accounting targets for authorized execution

```text
STRUCTURAL_UNITS = 168
STEP14A_MATERIAL_DELTAS = 21
STEP14_LINK_ROWS = 58
STEP14_IMPLEMENT_LINKS = 15
STEP17_CASES = 8
STEP17_CONTENT_EXPANSION_CANDIDATES = 3
PRESERVED_UNRESOLVED_PHRASES = 19
AUTHORIZED_NEW_PAGE_ACTIONS = 0
AUTHORIZED_DESTRUCTIVE_ACTIONS = 0
```

Step18 must de-duplicate upstream overlays so one implementation change has one canonical action with multiple evidence references rather than repeated rows.

## Private/client evidence boundary

Current base rehearsal still has no private Webmaster/Metrika/Direct evidence and several internal acquisition priorities remain UNKNOWN.

Therefore:

```text
PUBLIC_BUSINESS_RELEVANCE = ALLOWED WITH EVIDENCE
PRIVATE_MARGIN/CAPACITY/SALES_PRIORITY = NOT AVAILABLE / DO NOT GUESS
CONVERSION/REVENUE PRIORITY = NOT AVAILABLE / DO NOT GUESS
IMPLEMENTATION EFFORT = UNKNOWN UNLESS EXPLICIT EVIDENCE EXISTS
```

Webmaster/Metrika/Direct remain optional enhancements in base mode and do not block Step18.

## Bridge correlation

```text
STEP18_BASE_BRIDGE = NOT REQUIRED
STEP18_BRIDGE = CONDITIONAL ONLY
PLANNED_NEW_PROVIDER_CALLS = 0
PLANNED_NEW_PAID_COST_RUB = 0
```

A new provider call may be proposed only if a concrete material prioritization question cannot be answered from persisted evidence and the answer can change Step18 acceptance. Such a call requires an explicit information-gain record, cost/quota boundary, persistence destination and new owner authorization.

## Execution outputs required after authorization

```text
STEP_18_ACTION_REGISTER.tsv
STEP_18_PRIORITY_SUMMARY.tsv
STEP_18_HOLD_RECHECK_LEDGER.tsv
STEP_18_QA.json
STEP_18_REPORT.md
STEP_18_CURRENT_STATE.json (execution state update)
JOB_FLOW_STEP18_EXECUTION_SYNC_<DATE>.md
```

## Step18 execution acceptance targets

```text
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
EVERY_P1_P2_HAS_EVIDENCE_REASON_LIMITATIONS = true
EVERY_HOLD_HAS_RECHECK_TRIGGER = true
FORWARD_TRACE_PASS = true
REVERSE_TRACE_PASS = true
ADVERSARIAL_QA_PASS = true
FINAL_GITHUB_READBACK = true
```

## Current transition

```text
STEP18_PRESTEP_REVIEW = COMPLETE
STEP18_SOURCE_TO_METHOD_TRACE = PASS_PRE_EXECUTION
STEP18_RESEARCH_TO_EXECUTION_SCHEMA = PASS_PRE_EXECUTION
STEP18_EXECUTION_MANIFEST = PREPARED_NOT_EXECUTED
STEP18_OWNER_AUTHORIZATION = NOT_RECEIVED
STEP18_EXECUTION_STARTED = false
NEW_PROVIDER_CALLS = 0
NEW_PAID_PROVIDER_COST_RUB = 0
NEXT_LEGAL_ACTION = OWNER_AUTHORIZATION_FOR_STEP18_EXECUTION
```
