# KW-001 — STEP 13 COMPETING-PAGE / CANNIBALIZATION DIAGNOSIS METHOD

Date: 2026-09-01  
Updated: 2026-09-03  
Status: **OWNER-DIRECTED CORRECTED METHOD / ACTIVE / UNIVERSAL / BASE-PUBLIC AND ENHANCED MODES EXPLICITLY SEPARATED**

Normative companion authorities:

- `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`
- `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY_BRIDGE_CAPABILITY_UPDATE_2026-09-01.md`
- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`
- `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`

## 1. Step purpose

Step 13 determines whether related current URLs are:

- legitimate pages for different user tasks;
- normal parent/child or primary/supporting pages;
- pages with a current ownership warning signal;
- pages that repeatedly compete for the same query family when historical evidence is available;
- duplicate/near-duplicate candidates;
- or cases where available evidence is insufficient for a stronger conclusion.

The purpose is not to maximize the number of “cannibalization” findings. The purpose is to distinguish normal multi-page coverage from actual query-level competition without inventing certainty.

```text
RELATED PAGES != CANNIBALIZATION
CURRENT SERP OVERLAP != HISTORICAL COMPETITION
HISTORICAL COMPETITION != PROVEN HARM
BASE PUBLIC DIAGNOSIS != ENHANCED FIRST-PARTY HISTORY DIAGNOSIS
```

## 2. Permanent failure lesson

A prior controlled Step13 execution found official first-party query-by-URL historical evidence during method research, but the discovered source was not converted into an executable requirement/mode/claim boundary before execution.

Failure class:

```text
RESEARCH_TO_EXECUTION_SCHEMA_GAP
```

Causal chain:

```text
OFFICIAL SOURCE DISCOVERED
-> SOURCE RECORDED AS “IDEAL EVIDENCE”
-> ACCESS PROBLEM TREATED AS A LIMITATION
-> LIMITATION NOT CONVERTED INTO MODE / REQUIREMENT / CLAIM BOUNDARY / ACCEPTANCE FIELD
-> PUBLIC CURRENT-PAGE + SEARCH WORK CONTINUED
-> QA CHECKED EXISTING ARTIFACTS BUT NOT MISSING REQUIRED-EVIDENCE COVERAGE
-> STEP WAS OVERSTATED
```

### Root cause

```text
RESEARCH DISCOVERY
WAS MISTAKEN FOR
OPERATIONALIZED EXECUTION REQUIREMENT
```

and:

```text
LIMITATION DISCLOSURE
WAS NOT MADE TO CHANGE
MODE / CLAIM / PASS ELIGIBILITY
```

The correction is **not** “private Webmaster evidence is always mandatory”. The current sold scope decides whether historical first-party evidence is an optional enhancement or a required evidence route.

Permanent rules:

```text
SOURCE_DISCOVERED != SOURCE_OPERATIONALIZED
SOURCE_OPERATIONALIZED != EVIDENCE_ACQUIRED
LIMITATION_DISCLOSED != LIMITATION_GOVERNED
OPTIONAL_ENHANCEMENT != SILENTLY_SKIPPED_SOURCE
```

Every material research-derived requirement must pass `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`.

## 3. External method authority

### Official Yandex

- https://yandex.ru/support/webmaster/ru/service/queries-export
- https://www.yandex.ru/dev/webmaster/doc/ru/reference/enhanced-export
- https://yandex.ru/support/webmaster/ru/service/popular-queries
- https://yandex.ru/support/webmaster/ru/service/queries-analytic
- https://yandex.ru/support/webmaster/ru/robot-workings/double

First-party query×URL history can provide date, URL, query, region, clicks, impressions and position evidence when the task scope requires historical competition diagnosis.

### Industry corroboration

Current Ahrefs/Semrush cannibalization and search-intent practice supports the principle that shared vocabulary alone is insufficient; user intent, page role and repeated URL competition matter more than lexical overlap.

Exact KW-001 verdict names remain project-specific.

## 4. Evidence model

### Layer A — relationship/accounting evidence

Which related page pairs/candidate URL sets must be investigated? Discovery/accounting evidence cannot by itself prove conflict.

### Layer B — current first-party page evidence

What does each current page actually do now? Material candidate URLs must satisfy current-site freshness requirements.

### Layer C — current public Search evidence

What page/URL types does current Search select for a bounded direct query now? This is a current snapshot, not historical performance history.

### Layer D — first-party historical query×URL evidence

For the same relevant query/query family, which target-site URLs received visibility/click evidence over time, and did ownership repeatedly alternate or fragment?

For a sellable `BASE_PUBLIC_EVIDENCE_MODE`, Layer D may be an explicit optional enhancement when client-private access is unavailable.

For `ENHANCED_WITH_ACCESS_MODE` or `RESEARCH_GRADE_HISTORY_REQUIRED_MODE`, Layer D may be mandatory by scope.

## 5. Mandatory execution-mode and access gate

Before diagnosis classify the current job mode:

```text
BASE_PUBLIC_EVIDENCE_MODE
ENHANCED_WITH_ACCESS_MODE
RESEARCH_GRADE_HISTORY_REQUIRED_MODE
```

Build the source/capability/access matrix required by `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`.

Preserve equivalent state fields:

```text
SOURCE_EXISTS
ACCESS_STATE
PROPERTY_RESOLVED_STATE
TOOL_CAPABILITY_STATE
PROVIDER_READY_STATE
QUOTA_OR_COST_STATE
COLLECTION_STATE
PERSISTENCE_STATE
CLAIM_BOUNDARY
```

Valid history-route states include:

```text
AVAILABLE_AND_USED
AVAILABLE_NOT_YET_USED
OPTIONAL_ENHANCEMENT_UNAVAILABLE__BASE_PUBLIC_MODE_ACCEPTED
UNAVAILABLE_ACCOUNT_OR_PROPERTY_ACCESS
UNAVAILABLE_PROVIDER_READINESS
UNAVAILABLE_PROVIDER_QUOTA_OR_DATE_RANGE
UNAVAILABLE_OTHER_WITH_EVIDENCE
REQUIRED_BY_ENHANCED_SCOPE_NOT_YET_SATISFIED
```

Forbidden:

```text
KNOWN_SOURCE_BUT_SILENTLY_SKIPPED
```

### Base-public policy

```text
CLIENT_PRIVATE_DATA_UNAVAILABLE
-> BASE_PUBLIC_EVIDENCE_MODE
-> NOT AUTOMATIC PROCESS FAILURE
-> BASE-PACKAGE PURPOSE MAY COMPLETE
-> HISTORICAL/HARM CLAIMS REMAIN BOUNDED
```

### Enhanced/history-required policy

```text
REQUIRED HISTORY UNAVAILABLE
-> ENHANCED/HISTORY SCOPE BLOCKED OR DEGRADED
-> DO NOT RELABEL PUBLIC SNAPSHOT EVIDENCE AS HISTORY
```

## 6. Correct execution order

```text
1. FREEZE INPUT PAIR / URL UNIVERSE
2. RECONCILE ALL INPUT IDS
3. READ CURRENT URL EVIDENCE
4. DISCOVER MATERIAL CURRENT SPECIALIST PAGES MISSED BY FROZEN EVIDENCE
5. EXTEND EFFECTIVE PAIR / URL UNIVERSE WHEN CURRENT DISCOVERY REQUIRES IT
6. GROUP MATERIAL SURVIVORS AS QUERY FAMILY × CANDIDATE URL SET
7. BUILD RESEARCH-TO-EXECUTION REQUIREMENT TRACE
8. DECLARE CURRENT EXECUTION MODE
9. BUILD SOURCE / ACCESS / CAPABILITY / COST MATRIX
10. MATERIALIZE EXECUTION MANIFEST
11. REUSE SAVED FIRST-PARTY HISTORY IF APPLICABLE
12. REUSE SAVED ORDINARY SEARCH EVIDENCE
13. CLOSE CLEAR DISTINCT-TASK / HIERARCHICAL RELATIONSHIPS
14. COLLECT FOCUSED ORDINARY SEARCH ONLY WHERE CURRENT OWNERSHIP IS STILL MATERIAL
15. IF CURRENT MODE REQUIRES HISTORY, COLLECT / INSPECT FIRST-PARTY QUERY×URL HISTORY
16. SEPARATE CURRENT SIGNAL, HISTORICAL COMPETITION AND HARM
17. ASSIGN VERDICT WITH EVIDENCE LEVEL
18. RECOMMEND REMEDIATION ONLY AFTER VERDICT
19. QA CHECKS BOTH PRESENT AND MISSING REQUIRED EVIDENCE
20. REVERSE-TRACE CLAIMS TO REQUIREMENT + EVIDENCE + QA
21. GITHUB PERSISTENCE + READBACK
22. ONLY THEN FINAL ACCEPTANCE
```

No new provider call is justified merely because a provider is available. Fresh calls require explicit information gain and acceptance use.

## 7. First-party history protocol

When history is applicable, prefer existing saved first-party evidence before new collection. Use the narrowest current first-party source that exposes the required query×URL behavior.

Do not invent a universal fixed date window. Predeclare a justified window based on available dates, seasonality, query volume, severity, quota, candidate URL count and the decision being made.

Normalized rows should preserve equivalent fields:

```text
date
host
url
query
region
clicks
impressions
position
source
collection_window
```

Historical analysis distinguishes simultaneous/complementary visibility, clear dominance, repeated switching/fragmentation and actual harm.

## 8. Verdict taxonomy

Permitted classes include:

```text
NORMAL_DISTINCT_TASKS
NORMAL_PARENT_CHILD
NORMAL_PRIMARY_SUPPORTING
NORMAL_MIXED_INTENT
CURRENT_TARGET_RELEVANT_MISMATCH_SIGNAL
CURRENT_MULTI_URL_VISIBILITY_SIGNAL
HISTORICAL_MULTI_URL_COMPETITION_SUPPORTED
HISTORICAL_OWNER_SWITCHING_SUPPORTED
TRUE_DUPLICATE_OR_NEAR_DUPLICATE_CONFLICT
HARMFUL_IMPACT_SUPPORTED
EVIDENCE_INSUFFICIENT
```

A strong harmful-cannibalization verdict requires evidence for the actual harm claim. It must not be inferred from shared keywords, related pages, one public Search snapshot or multi-URL visibility alone.

## 9. Remediation rules

No destructive action follows automatically from overlap.

Possible outputs:

```text
KEEP_BOTH
DIFFERENTIATE_PRIMARY_RESPONSIBILITY
STRENGTHEN_INTERNAL_LINK_SIGNAL
REASSIGN_PRIMARY_OWNER
CONTENT_SCOPE_REPAIR
CONSOLIDATION_CANDIDATE
REDIRECT_CANDIDATE
CANONICAL_CANDIDATE
DEFER_PENDING_HISTORY
```

Destructive remediation requires qualifying evidence and a check that useful independent intent/value will not be lost.

## 10. Required execution schema

The current job must preserve a reproducible manifest with equivalent fields:

```text
job
step
method_authority
research_to_execution_gate
current_job_mode
base_pair_universe
effective_pair_universe
pair_accounting
query_family_case_count
current_page_evidence_count
required_sources
optional_sources
private_history_access_state
private_history_tool_capability_state
ordinary_search_reuse_state
fresh_search_trigger_state
provider_boundaries
provider_cost
claim_boundaries
remediation_boundary
qa_state
acceptance_state
```

Material research-derived requirements need stable IDs and forward/reverse traceability.

## 11. Mandatory QA

Verify:

```text
all declared pairs/cases reconcile;
current URLs were re-read;
new material pages were incorporated;
all research conclusions became requirements/modes/actions/fields/checks;
private-history availability was explicitly classified;
base-mode historical/harm claims remain bounded;
history-required mode blocks/degrades when history is missing;
missing required evidence is checked, not just present artifacts;
one Search snapshot never becomes historical/harm proof;
destructive action never exceeds evidence level;
provider outcomes/cost/readbacks reconcile;
accepted claims reverse-trace to requirement + evidence + QA.
```

## 12. Pass gates by mode

### BASE_PUBLIC_EVIDENCE_MODE

```text
PAIR / CASE ACCOUNTING = COMPLETE
SILENT DROPS = 0
CURRENT PAGE FRESHNESS = COMPLETE FOR MATERIAL URLS
MATERIAL CURRENT-SITE DISCOVERIES = INCORPORATED
PUBLIC SEARCH EVIDENCE = RECONCILED WHERE USED
CLIENT_PRIVATE_HISTORY_ROUTE = EXPLICITLY CLASSIFIED
OPTIONAL_ENHANCEMENT_SILENTLY_SKIPPED = 0
HISTORICAL CLAIM FROM PUBLIC-ONLY EVIDENCE = 0
HARM CLAIM WITHOUT QUALIFYING EVIDENCE = 0
DESTRUCTIVE REMEDIATION WITHOUT QUALIFYING EVIDENCE = 0
RESEARCH_TO_EXECUTION_SCHEMA_GATE = PASS
QA BLOCKING FINDINGS = 0
FINAL GITHUB READBACK = PASS
NEXT STEP NOT EXECUTED PREMATURELY
```

### ENHANCED_WITH_ACCESS / RESEARCH_GRADE_HISTORY_REQUIRED

If current scope explicitly requires historical diagnosis:

```text
FIRST_PARTY_QUERY_URL_HISTORY_GATE = AVAILABLE_AND_USED
```

or the enhanced/history-required portion cannot receive full PASS.

## 13. Job-specific application boundary

Concrete execution mode, URL/pair counts, provider costs, verdict counts, artifact paths and completion state belong exclusively in the current Level-2 job workspace.

```text
PERMANENT STEP13 METHOD
!= CURRENT JOB STEP13 RESULT
```

## 14. Non-repeat markers

```text
STEP13_RESEARCH_TO_EXECUTION_SCHEMA_GAP_FORBIDDEN = true
STEP13_SOURCE_KNOWN_BUT_NOT_OPERATIONALIZED_FORBIDDEN = true
STEP13_SOURCE_DISCOVERED_NOT_EQUAL_SOURCE_OPERATIONALIZED = true
STEP13_LIMITATION_DISCLOSED_NOT_EQUAL_LIMITATION_GOVERNED = true
STEP13_BASE_PUBLIC_MODE_SUPPORTED_WITHOUT_PRIVATE_HISTORY = true
STEP13_PRIVATE_HISTORY_OPTIONAL_ENHANCEMENT_MUST_BE_EXPLICIT = true
STEP13_ENHANCED_HISTORY_SCOPE_REQUIRES_HISTORY_WHEN_DECLARED = true
STEP13_ACCOUNT_ACCESS_AND_TOOL_CAPABILITY_ARE_SEPARATE = true
STEP13_EXECUTION_MANIFEST_REQUIRED = true
STEP13_QA_MUST_TEST_MISSING_REQUIRED_EVIDENCE = true
STEP13_ONE_SEARCH_SNAPSHOT_CANNOT_PROVE_HISTORY_OR_HARM = true
STEP13_REVERSE_CLAIM_TRACE_REQUIRED = true
STEP13_JOB_SPECIFIC_RESULTS_FORBIDDEN_IN_PERMANENT_METHOD = true
```
