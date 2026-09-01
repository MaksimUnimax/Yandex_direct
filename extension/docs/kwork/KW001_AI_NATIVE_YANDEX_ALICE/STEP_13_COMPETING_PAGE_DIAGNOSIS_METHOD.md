# KW-001 — STEP 13 COMPETING-PAGE / CANNIBALIZATION DIAGNOSIS METHOD

Date: 2026-09-01  
Status: **OWNER-DIRECTED CORRECTED METHOD / ACTIVE / BASE-PUBLIC AND ENHANCED MODES EXPLICITLY SEPARATED**

Normative companion authorities:

- `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`
- `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY_BRIDGE_CAPABILITY_UPDATE_2026-09-01.md`
- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`

## 1. Step purpose

Step 13 determines whether related current URLs are:

- legitimate pages for different user tasks;
- normal parent/child or primary/supporting pages;
- pages with a current ownership warning signal;
- pages that repeatedly compete for the same query family when historical evidence is available;
- duplicate/near-duplicate candidates;
- or cases where available evidence is insufficient for a stronger conclusion.

The purpose is not to maximize the number of “cannibalization” findings. The purpose is to distinguish normal multi-page coverage from actual query-level competition without inventing certainty.

Canonical distinctions:

```text
RELATED PAGES != CANNIBALIZATION
CURRENT SERP OVERLAP != HISTORICAL COMPETITION
HISTORICAL COMPETITION != PROVEN HARM
BASE PUBLIC DIAGNOSIS != ENHANCED FIRST-PARTY HISTORY DIAGNOSIS
```

## 2. Permanent lesson from the first OKNO_MSK execution

The first Step-13 execution found official Yandex query-by-URL historical evidence before execution but failed to convert that research finding into an executable schema decision.

The failure class is:

```text
RESEARCH_TO_EXECUTION_SCHEMA_GAP
```

Historical causal chain:

```text
OFFICIAL SOURCE DISCOVERED
-> SOURCE RECORDED AS “IDEAL EVIDENCE”
-> ACCESS PROBLEM TREATED AS A LIMITATION
-> LIMITATION NOT CONVERTED INTO MODE / REQUIREMENT CLASS / CLAIM BOUNDARY / ACCEPTANCE FIELD
-> PUBLIC CURRENT-PAGE + SERP WORK CONTINUED
-> QA CHECKED EXISTING ARTIFACTS BUT NOT REQUIRED-EVIDENCE COVERAGE
-> STEP WAS MARKED COMPLETE
```

The correction is **not** “Webmaster must always be mandatory”. The owner-approved commercial policy later established that private Webmaster evidence is optional for the sellable base Kwork.

Therefore the permanent non-repeat rule is:

```text
SOURCE_DISCOVERED != SOURCE_OPERATIONALIZED
SOURCE_OPERATIONALIZED != EVIDENCE_ACQUIRED
LIMITATION_DISCLOSED != LIMITATION_GOVERNED
OPTIONAL_ENHANCEMENT != SILENTLY_SKIPPED_SOURCE
```

Every material research-derived requirement must pass `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`.

## 3. External method authority

### Official Yandex

- Extended search-query analytics by URL: `https://yandex.ru/support/webmaster/ru/service/queries-export`
- Enhanced export API: `https://www.yandex.ru/dev/webmaster/doc/ru/reference/enhanced-export`
- Search query monitoring: `https://yandex.ru/support/webmaster/ru/service/popular-queries`
- Search query analytics: `https://yandex.ru/support/webmaster/ru/service/queries-analytic`
- Duplicate/similar page handling: `https://yandex.ru/support/webmaster/ru/robot-workings/double`

The enhanced export is first-party evidence for `query × URL × time` behavior and can expose date, URL, query, region, clicks, impressions and position. It is directly relevant when the task scope requires historical competition diagnosis.

### Industry corroboration

Ahrefs and Semrush cannibalization/intent methodology supports the principle that shared vocabulary alone is insufficient: user intent, page role and repeated URL competition matter more than lexical overlap.

Exact KW-001 states remain project-specific.

## 4. Evidence model

Step 13 keeps four evidence layers separate.

### Layer A — relationship/accounting evidence

Answers:

```text
Which related page pairs / candidate URL sets must be investigated?
```

This is discovery/accounting evidence only. It cannot prove a conflict.

### Layer B — current first-party page evidence

Answers:

```text
What does each current page actually do now?
What object, task, lifecycle stage and intent does it serve?
```

All material candidate URLs must pass the current-site freshness gate.

### Layer C — current public Search evidence

Answers:

```text
What URL/page type does current Yandex Search select for a bounded direct query now?
Does the target site currently expose one or several URLs in the observed result set?
```

This is a current snapshot, not a historical performance series.

### Layer D — first-party historical query×URL evidence

Answers:

```text
For the same relevant query/query family, which target-site URLs received impressions/clicks over time?
Did ownership repeatedly alternate or fragment across candidate URLs?
Were position/impression/click patterns stable, complementary or conflicting?
```

For the sellable **BASE_PUBLIC_EVIDENCE_MODE**, Layer D is an explicit optional enhancement when client-private access is unavailable.

For an explicitly sold/authorized **ENHANCED_WITH_ACCESS** or research-grade historical diagnosis, Layer D may be mandatory by scope.

## 5. Mandatory execution-mode and access gate

Before Step-13 diagnosis, classify the current job mode:

```text
BASE_PUBLIC_EVIDENCE_MODE
ENHANCED_WITH_ACCESS_MODE
RESEARCH_GRADE_HISTORY_REQUIRED_MODE
```

Then build the source/capability/access matrix required by `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`.

Required state fields for the historical route:

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

Under `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`:

```text
CLIENT_PRIVATE_DATA_UNAVAILABLE
-> BASE_PUBLIC_EVIDENCE_MODE
-> NOT A PROCESS FAILURE
-> STEP 13 MAY COMPLETE THE BASE-PACKAGE PURPOSE
-> HISTORICAL/HARM CLAIMS REMAIN BOUNDED TO AVAILABLE EVIDENCE
```

### Enhanced/history-required policy

If the sold or owner-authorized scope requires historical query×URL diagnosis:

```text
REQUIRED HISTORY UNAVAILABLE
-> ENHANCED/HISTORY SCOPE BLOCKED OR DEGRADED
-> DO NOT RELABEL BASE PUBLIC EVIDENCE AS HISTORY
```

## 6. Correct execution order

```text
1. FREEZE INPUT PAIR / URL UNIVERSE
2. RECONCILE ALL INPUT IDS
3. READ CURRENT URL EVIDENCE
4. DISCOVER MATERIAL CURRENT SPECIALIST PAGES MISSED BY FROZEN EVIDENCE
5. EXTEND THE EFFECTIVE PAIR / URL UNIVERSE WHEN CURRENT DISCOVERY REQUIRES IT
6. GROUP MATERIAL SURVIVORS AS QUERY FAMILY × CANDIDATE URL SET
7. BUILD RESEARCH-TO-EXECUTION REQUIREMENT TRACE
8. DECLARE CURRENT EXECUTION MODE
9. BUILD SOURCE / ACCESS / CAPABILITY / COST MATRIX
10. MATERIALIZE THE EXECUTION MANIFEST
11. REUSE SAVED FIRST-PARTY HISTORY IF APPLICABLE AND ALREADY PRESENT
12. REUSE SAVED ORDINARY SEARCH EVIDENCE
13. CLOSE CLEAR DISTINCT-TASK / HIERARCHICAL RELATIONSHIPS
14. COLLECT FOCUSED ORDINARY SEARCH ONLY WHERE CURRENT OWNERSHIP IS STILL MATERIAL
15. IF CURRENT MODE REQUIRES HISTORY, COLLECT / INSPECT FIRST-PARTY QUERY×URL HISTORY
16. SEPARATE CURRENT SIGNAL, HISTORICAL COMPETITION AND HARM
17. ASSIGN VERDICT WITH EVIDENCE LEVEL
18. RECOMMEND REMEDIATION ONLY AFTER THE VERDICT
19. INDEPENDENT QA CHECKS BOTH PRESENT AND MISSING REQUIRED EVIDENCE
20. REVERSE-TRACE ACCEPTED CLAIMS TO REQUIREMENT + EVIDENCE + QA
21. GITHUB PERSISTENCE + READBACK
22. ONLY THEN FINAL ACCEPTANCE
```

No new provider call is justified merely because the provider is available. Fresh calls require explicit information gain and acceptance use.

## 7. First-party history collection protocol

When history is applicable to the current mode, prefer evidence routes in this order as appropriate:

1. existing saved Webmaster exports already in the job;
2. Webmaster query/URL monitoring or page/query analytics if they expose the required view;
3. enhanced query-by-URL export for selected candidate URLs and justified date/region scope;
4. another first-party source only if it genuinely exposes comparable query×URL historical behavior and the substitution is documented.

Do not invent a universal fixed number of days. Predeclare a justified window based on available dates, seasonality, query volume, case severity, quota, candidate URL count and the client decision being made.

Required normalized row when available:

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

Historical analysis asks whether multiple candidate URLs receive impressions for the same/similar family, whether visibility is simultaneous or alternating, whether one URL clearly dominates, whether ownership switches repeatedly, whether switching is explainable by intent/seasonality/content, and whether there is actual harm rather than merely multi-URL visibility.

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

`CONFIRMED_HARMFUL_CANNIBALIZATION` may be used only when evidence supports all necessary parts of that statement. It must not be inferred from shared keywords, shared cluster, related pages, one public SERP, one target/relevant mismatch, or multi-URL visibility without harm evidence.

## 9. Remediation rules

No destructive site action follows automatically from overlap.

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

## 10. Mandatory execution schema for Step 13

The current job must preserve a reproducible Step-13 execution manifest with at least:

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
webmaster_access_state
webmaster_tool_capability_state
ordinary_search_reuse_state
fresh_search_trigger_state
provider_boundaries
provider_cost
claim_boundaries
remediation_boundary
qa_state
acceptance_state
```

Material research-derived requirements must receive stable IDs and forward/reverse traceability.

## 11. Mandatory QA

QA must check absence as well as presence.

Required questions:

```text
Did every declared pair/case reconcile?
Were current URLs re-read?
Were newly discovered material pages incorporated?
Did every material research conclusion become a requirement/mode/action/field/check?
Was private-history availability explicitly classified?
If unavailable in base mode, was the optional enhancement state explicit and were historical/harm claims bounded?
If history is required by enhanced scope, was the step blocked/degraded until that requirement was satisfied?
Did the verifier inspect missing evidence rather than only validate existing artifacts?
Did any one-SERP observation become a historical/harm claim?
Did any destructive action exceed its evidence level?
Are provider outcomes/costs/readbacks reconciled?
Can every accepted final claim be reverse-traced to requirement + evidence + QA?
```

## 12. Pass gates by mode

### BASE_PUBLIC_EVIDENCE_MODE

A full base-package Step-13 PASS requires:

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
INDEPENDENT QA BLOCKING FINDINGS = 0
FINAL GITHUB READBACK = PASS
STEP14_EXECUTED = false
```

Private query×URL history is **not** required to complete the sellable base scope when unavailable.

### ENHANCED_WITH_ACCESS / RESEARCH_GRADE_HISTORY_REQUIRED

If current scope explicitly requires historical diagnosis:

```text
FIRST_PARTY_QUERY_URL_HISTORY_GATE = AVAILABLE_AND_USED
```

or the enhanced/history-required portion cannot receive full PASS.

## 13. Current OKNO_MSK application

Current owner-approved mode:

```text
MODE = BASE_PUBLIC_EVIDENCE_MODE
YANDEX_WEBMASTER_ACCESS = UNAVAILABLE
PRIVATE_FIRST_PARTY_HISTORY_USED = false
```

Preserved completed evidence:

```text
historical base pairs = 195
effective pair universe after current-site discoveries = 199
pairs accounted = 199/199
query-family cases = 21
presearch cases closed without fresh Search = 5
fresh ordinary-Search cases with usable evidence = 16/16
current-page evidence URLs = 49
provider boundaries started = 17
provider cost accounted = 8.296 RUB
confirmed harmful cannibalization from public/current evidence = 0
destructive remediation authorized = 0
```

The historical first-party route is explicitly classified as:

```text
OPTIONAL_ENHANCEMENT_UNAVAILABLE__BASE_PUBLIC_MODE_ACCEPTED
```

The base Step-13 acceptance therefore remains valid, with historical/harm claim boundaries preserved. Step 14 is allowed only through its mandatory pre-step method/evidence review.

Current schema-hardening artifacts:

- `tests/OKNO_MSK/STEP_13_EXECUTION_MANIFEST.json`
- `tests/OKNO_MSK/STEP_13_RESEARCH_TO_EXECUTION_SCHEMA_AUDIT_2026-09-01.md`

## 14. Non-repeat markers

```text
STEP13_RESEARCH_TO_EXECUTION_SCHEMA_GAP_FORBIDDEN = true
STEP13_SOURCE_KNOWN_BUT_NOT_OPERATIONALIZED_FORBIDDEN = true
STEP13_SOURCE_DISCOVERED_NOT_EQUAL_SOURCE_OPERATIONALIZED = true
STEP13_LIMITATION_DISCLOSED_NOT_EQUAL_LIMITATION_GOVERNED = true
STEP13_BASE_PUBLIC_MODE_SUPPORTED_WITHOUT_PRIVATE_WEBMASTER = true
STEP13_PRIVATE_HISTORY_OPTIONAL_ENHANCEMENT_MUST_BE_EXPLICIT = true
STEP13_ENHANCED_HISTORY_SCOPE_REQUIRES_HISTORY_WHEN_DECLARED = true
STEP13_ACCOUNT_ACCESS_AND_TOOL_CAPABILITY_ARE_SEPARATE = true
STEP13_EXECUTION_MANIFEST_REQUIRED = true
STEP13_QA_MUST_TEST_MISSING_REQUIRED_EVIDENCE = true
STEP13_ONE_SERP_CANNOT_PROVE_HISTORY_OR_HARM = true
STEP13_REVERSE_CLAIM_TRACE_REQUIRED = true
```
