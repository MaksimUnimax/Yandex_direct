# KW-001 — STEP RULES INDEX

Date: 2026-09-02  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**

This file is the index of step-specific methodology coverage.

It does not replace detailed method files. It answers three questions before execution:

```text
1. Has this roadmap stage actually earned a validated permanent method?
2. Where is the canonical detailed method / lesson authority for it?
3. Have current research findings been converted into an executable schema for this job?
```

Canonical rules:

```text
ROADMAP_STAGE_EXISTS != METHODOLOGY_VALIDATED
RESEARCH_COLLECTED != METHOD_VALIDATED
RESEARCH_COLLECTED != EXECUTION_SCHEMA_READY
SOURCE_DISCOVERED != REQUIREMENT_OPERATIONALIZED
OLD_SITE_INVENTORY != CURRENT_SITE_TRUTH
KNOWN_URL_RECHECK != CURRENT_SITE_DISCOVERY
UPSTREAM_INPUT_UNIVERSE != CURRENT_SITE_UNIVERSE
SOURCE_LIVE + TARGET_LIVE != EDGE_IMPLEMENTED
SEMANTIC_LINK_RECOMMENDATION != CURRENT_AS_IS_LINK
```

Universal cross-step authorities:

- `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`
- `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md` for Steps 1, 11, 12, 13, 14 and 20 where current URL truth matters.
- `RULES_ARCHITECTURE_CODEX_SITE_DISCOVERY_GATE_ADDENDUM_2026-09-02.md` when a step acceptance depends on current-site completeness, current link topology, crawl reachability or exact current source->target HTML-link evidence.

A universal method is a reusable structure, not a domain-free execution rule:

```text
EXECUTABLE METHOD = UNIVERSAL CORE + CURRENT JOB PROFILE + CURRENT CONSTRAINTS
LOCAL RULE MUST BE SCOPED != LOCAL RULE MUST BE REMOVED
```

Before executing a major step, ChatGPT must:

```text
read SOURCE_TO_METHOD_TRACEABILITY_GATE.md;
read RESEARCH_TO_EXECUTION_SCHEMA_GATE.md;
check this index;
read the listed canonical method/lesson authority;
perform the required current external research for the step;
materialize material research requirements into the execution schema/manifest;
then execute.
```

If a material step is `UNVALIDATED` or has no sufficient detailed entry:

```text
CURRENT INTERNET METHOD RESEARCH = REQUIRED
SOURCE_TO_METHOD TRACE = REQUIRED
RESEARCH_TO_EXECUTION SCHEMA = REQUIRED
OWNER-FACING METHOD REVIEW = REQUIRED
EXECUTION = BLOCKED UNTIL THAT REVIEW IS COMPLETE
```

Permanent promotion requires explicit owner instruction.

---

# Current methodology coverage

| Stage | Purpose | Permanent methodology status | Canonical method / reusable lesson |
|---|---|---|---|
| Step 0 | Order / scope freeze | **APPROVED / ACTIVE** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — freeze brief before evidence. |
| Step 1 | Existing-site discovery / business-page model | **APPROVED / ACTIVE** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` + `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md` — one discovery pass is not automatically complete; cross-check channels, timestamp the inventory and preserve that it is a baseline snapshot rather than timeless absence proof. |
| Step 2 | Seed / acquisition probe plan | **APPROVED / ACTIVE** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — seed is an acquisition probe, not a final keyword/page target. |
| Step 3 | Wordstat/provider acquisition | **APPROVED / ACTIVE** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — provider/API success is not collection completion; complete returned evidence must be preserved and verified before advancing. |
| Step 3R | Repair of incomplete Step-3 acquisition | **JOB-SPECIFIC RECOVERY PATTERN / GOVERNED BY STEP 3** | Step-3 permanent rules + current-job repair evidence. |
| Step 4 | First post-Wordstat triage / cleanup preparation | **APPROVED / ACTIVE** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — family triage is not row-level cleanup; low frequency alone is not irrelevance; associations are not auto-accepted. |
| Step 5 | Targeted second acquisition / expansion | **PARTIALLY DEFINED / NOT YET UNIVERSALLY VALIDATED** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — every probe needs information gain; fresh research required before material reuse. |
| Step 6 | Demand dynamics / seasonality evidence | **UNVALIDATED AS PERMANENT METHOD** | Research before future execution/reuse. |
| Step 6A | Acquisition coverage revalidation | **UNVALIDATED AS PERMANENT METHOD** | Research before future execution/reuse. |
| Step 7 | Row-level semantic cleanup | **APPROVED / ACTIVE AFTER CORRECTION** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — no default KEEP; KEEP requires positive evidence; accounting QA != semantic QA; fix causes/classes; uncertainty -> REVIEW. |
| **Step 8** | **Freeze Search-stage semantic set** | **APPROVED / ACTIVE AFTER METHOD CORRECTION** | **`STEP_08_SEARCH_STAGE_FREEZE_METHOD.md`** — only executable routes; no `REVIEW_BUSINESS`/`REVIEW_SEARCH_AND_BUSINESS` without a real independent evidence source; internal priority is not a semantic route; source-to-method trace required. |
| Step 9 | Ordinary Yandex Search/SERP validation | **UNVALIDATED** | Must research current Yandex/Search evidence methodology, query sampling/full-scope rules, preservation and page-boundary interpretation before execution. |
| **Step 10** | **User-task / SERP clustering** | **APPROVED / ACTIVE AFTER GRANULARITY, SORTING AND UNIVERSALITY CORRECTION** | **`STEP_10_CLUSTERING_GRANULARITY_METHOD.md` + `STEP_10_TASK_FIRST_SORTING_DECISION_METHOD.md` + `STEP_10_SORTING_AND_QA_METHOD.md`** — reusable task-first core plus declared current-domain profile and constraints; fixed counts/ranges and scoped local rules are allowed when owner/client/deliverable requires them. |
| **Step 11** | **Page ownership / keyword-to-page mapping** | **APPROVED / ACTIVE AFTER EXTERNAL METHOD AUDIT + PHRASE-LEVEL CORRECTION** | **`STEP_11_PAGE_OWNERSHIP_METHOD.md` + `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`** — refresh current candidate pages; a `NO_SUITABLE_EXISTING_PAGE` negative claim requires current multi-route absence evidence, not old-inventory absence. Client-private Yandex evidence is optional under `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md` unless a future enhanced scope explicitly changes that. |
| **Step 12** | **Structural actions (keep/expand/split/merge/create)** | **APPROVED / ACTIVE AFTER D12-28..D12-30 EVIDENCE-INDEPENDENCE + GLOBAL-COHERENCE REVALIDATION** | **`STEP_12_FINAL_EXECUTION_PROTOCOL.md` + `STEP_12_STRUCTURAL_ACTION_METHOD.md` + `STEP_12_THIRD_AUDIT_EXECUTION_ORDER_CLARIFICATION.md` + `STEP_12_EVIDENCE_INDEPENDENCE_AND_CURRENT_CONTENT_VALIDATION.md` + `STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md` + `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`** — action/schema consistency cannot prove causal correctness; routing edges are not automatically validated links; known-regression zero is not global coherence. |
| **Step 13** | **Competing-page / cannibalization diagnosis** | **APPROVED / ACTIVE AFTER POST-RUN METHOD + POLICY + EXECUTION-SCHEMA CORRECTION** | **`STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md` + `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md` + `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md` + `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`** — official first-party history discovered during research must be explicitly operationalized, but the owner-approved sellable base package does not require private Webmaster access. Base-public mode may pass with explicit historical/harm claim boundaries; enhanced/history-required mode activates the first-party query×URL history gate. Current OKNO_MSK Step 13 is **COMPLETE / PASS_BASE_PUBLIC_EVIDENCE_MODE** and Step 14 is allowed only through its own pre-step method/evidence review. |
| **Step 14** | **Search-only architecture freeze** | **APPROVED / ACTIVE AFTER POST-RUN DISCOVERY-TOPOLOGY CORRECTION** | **`STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE_METHOD.md` + `RULES_ARCHITECTURE_CODEX_SITE_DISCOVERY_GATE_ADDENDUM_2026-09-02.md` + `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`** — target Search architecture must be reconciled against an independently discovered current public-site universe and literal current HTML link topology. A closed known-URL list cannot prove its own completeness; live source/target endpoints do not prove a current `<a href>` edge. When completeness/topology is material, deterministic Codex/code discovery, persisted outputs, GitHub readback, newly discovered URL reconciliation, and literal classification of required edges are mandatory before final PASS. Current OKNO_MSK Step 14/14A is **FINAL PASS** after the mandatory current-site reconciliation; Step 15 is no longer blocked by Step14. |
| **Step 15** | **AI-case selection** | **APPROVED / ACTIVE AFTER POST-RUN LINEAGE + STABILITY-CONTROL CORRECTION** | **`STEP_15_AI_CASE_SELECTION_METHOD.md`** — build the candidate universe by exact authoritative QF-ID joins, never manual remapping; separate `DIAGNOSTIC_PROBE` from `STABILITY_CONTROL`; pre-register later outcomes; label the selected set as non-representative unless a separate representative-sampling method exists; a single later material AI delta/control break requires confirmation handoff rather than automatic architecture rewrite. Current OKNO_MSK canonical Step15 result is V2: **25 reviewed / 8 selected (6 diagnostics + 2 controls) / 16 rejected / 1 hold**; V1 is superseded. |
| Step 16 | AI-search evidence acquisition | **UNVALIDATED** | Must research current Alice/GenSearch/Webmaster capabilities, preserve complete evidence and separate model/search behaviour from classic SERP evidence. `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md` governs optional owned Webmaster AI evidence vs base GenSearch evidence. |
| Step 17 | Search-vs-AI comparison | **UNVALIDATED** | Must define comparable evidence units and avoid forcing agreement between different retrieval surfaces. |
| Step 18 | Prioritization | **UNVALIDATED** | Must research/define how impact, evidence strength, public business relevance, internal client constraints, effort and uncertainty affect priority. |
| Step 19 | Client deliverables | **UNVALIDATED** | Must map analysis outputs to the sold deliverable and make evidence/uncertainty understandable to the client. |
| Step 20 | Final QA | **UNVALIDATED** | Must reconcile claims, counts, evidence, URLs/actions and unresolved items against the promised Kwork output, including a lightweight current-URL/current-role recheck for implementation-critical pages. |
| Step 21 | Handoff / revisions | **UNVALIDATED** | Must define revision scope, evidence updates, version truth and acceptance boundaries. |
| Step 22 | Job close | **PARTIALLY DEFINED BY JOB_WORKSPACE_LIFECYCLE** | Close only after work, handoff/revisions and pending provider/operator actions are finished; then mark workspace safe to delete. |

---

# Required per-step detail

For any step marked `APPROVED / ACTIVE`, its canonical method authority must preserve:

```text
STEP PURPOSE
APPROVED METHOD
WHY THIS METHOD
METHOD ORIGIN / DIRECT SOURCES
SOURCE-TO-METHOD TRACE
RESEARCH-TO-EXECUTION REQUIREMENT TRACE
CURRENT JOB MODE / SCOPE
REPRODUCIBLE EXECUTION MANIFEST
KNOWN ERROR(S)
ROOT CAUSE
CORRECTED METHOD
NON-REPEAT CONTROLS
CLAIM BOUNDARIES
PASS GATE
STATUS
```

For a step marked `UNVALIDATED`, absence of known errors means only:

```text
WE HAVE NOT YET EARNED A PERMANENT METHOD
```

The next use requires fresh current research first.

---

# How this index is used

Before every major step:

```text
1. read SOURCE_TO_METHOD_TRACEABILITY_GATE.md;
2. read RESEARCH_TO_EXECUTION_SCHEMA_GATE.md;
3. locate current stage in STEP_RULES_INDEX.md;
4. if APPROVED -> read the listed canonical method and configure it with the current domain profile and current constraints;
5. if PARTIAL / UNVALIDATED -> do not infer/replay a method; research the step from current sources;
6. build a source-to-method trace for every material state/rule/route/threshold;
7. convert every material research conclusion into requirement_id + class + action/output + failure policy + claim boundary + QA + acceptance check;
8. materialize a reproducible execution manifest before material provider/execution work;
9. keep required current-job rules and label their scope instead of deleting them for being local;
10. read current-job evidence, site/business model, deliverable and owner constraints;
11. explain old errors + root causes + non-repeat controls where applicable;
12. before designing an evidence mechanism, inspect relevant prior project artifacts/tools for an existing stronger deterministic acquisition pattern capable of testing the same factual claim;
13. apply provider cost/information-gain gates before fresh paid or quota-bearing requests;
14. wait for owner authorization when the governing gate requires it;
15. execute the configured current method;
16. reverse-trace final accepted claims to requirement + evidence + QA before closure.
```

Fresh research remains mandatory when current provider/search behaviour or industry understanding may materially affect the step.

---

# Step-8 permanent lesson summary

The Step-8 correction established:

```text
business relevance/potential = evaluation dimension
internal business priority = client/internal constraint
Search/SERP = observable evidence source

therefore:
EVALUATION_DIMENSION != EVIDENCE_ROUTE
```

A prior method invented review routes after collecting sources that did not support those routes. The permanent non-repeat control is `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`.

---

# Step-10 permanent lesson summary

The Step-10 correction establishes:

```text
UNIVERSAL METHOD != DOMAIN-FREE EXECUTION
UNIVERSAL METHOD != BAN ON LOCAL RULES
EXECUTABLE STEP10 = REUSABLE CORE + CURRENT DOMAIN PROFILE + CURRENT CONSTRAINTS
LOCAL RULE MUST BE SCOPED != LOCAL RULE MUST BE REMOVED
```

Count handling is configurable: absent an explicit owner/client/deliverable count, count may emerge from validated boundaries; with an explicit count/range, record it, apply it, validate it and preserve trade-offs.

Canonical authorities:

- `STEP_10_CLUSTERING_GRANULARITY_METHOD.md`
- `STEP_10_TASK_FIRST_SORTING_DECISION_METHOD.md`
- `STEP_10_SORTING_AND_QA_METHOD.md`

---

# Step-13 permanent lesson summary

The Step-13 correction now establishes two separate lessons.

### Evidence-separation lesson

```text
ACCOUNT ACCESS != TOOL CAPABILITY
PUBLIC SERP SNAPSHOT != FIRST-PARTY QUERY×URL HISTORY
CURRENT MULTI-URL SIGNAL != HISTORICAL COMPETITION != HARM
```

### Research-to-execution lesson

```text
SOURCE_DISCOVERED != SOURCE_OPERATIONALIZED
RESEARCH_STATEMENT != EXECUTION_CONTROL
LIMITATION_DISCLOSED != LIMITATION_GOVERNED
OPTIONAL_ENHANCEMENT != SILENTLY_SKIPPED_SOURCE
```

The original failure was not missing research. Official Yandex historical query-by-URL analytics had already been found. The failure was allowing that source to remain “ideal evidence” instead of turning it into an explicit requirement class, mode, access/capability state, claim boundary, QA check and acceptance field.

The owner-approved base-package policy then established the correct scope classification:

```text
BASE_PUBLIC_EVIDENCE_MODE
-> PRIVATE WEBMASTER HISTORY = OPTIONAL_ENHANCEMENT
-> STEP 13 MAY PASS WITHOUT PRIVATE ACCESS
-> HISTORICAL/HARM CLAIMS REMAIN BOUNDED

ENHANCED_WITH_ACCESS / HISTORY_REQUIRED_MODE
-> FIRST-PARTY QUERY×URL HISTORY MAY BE REQUIRED BY SCOPE
```

The verifier must therefore detect missing required evidence **and** distinguish an explicitly unavailable optional enhancement from a silently skipped requirement.

Canonical authorities:

- `STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md`
- `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`

Current OKNO_MSK schema-hardening evidence:

- `tests/OKNO_MSK/STEP_13_EXECUTION_MANIFEST.json`
- `tests/OKNO_MSK/STEP_13_RESEARCH_TO_EXECUTION_SCHEMA_AUDIT_2026-09-01.md`

---

# Step-14 permanent lesson summary

The Step-14 post-run audit establishes three distinct lessons.

### Completeness lesson

```text
KNOWN_URL_RECHECK != CURRENT_SITE_DISCOVERY
UPSTREAM_INPUT_UNIVERSE != CURRENT_SITE_UNIVERSE
A CLOSED LIST CANNOT PROVE ITS OWN COMPLETENESS
```

The first OKNO_MSK Step-14 run rechecked every URL derived from accepted Step-12/13/14 inputs and got 59/59 live. That was useful freshness evidence for those 59 URLs, but the inference from "all selected known URLs are live" to "current relevant site architecture has been completely discovered" was invalid. Pages absent from the upstream list could never fail that test.

The root cause was not insufficient manual effort. The anti-speculation/scope-preservation control was applied too broadly, so the upstream URL universe behaved as if it were a closed current-site universe. The corrected control is independent deterministic discovery through Codex/code whenever completeness matters.

### Topology lesson

```text
SOURCE_LIVE + TARGET_LIVE + SEMANTIC_FIT != EDGE_IMPLEMENTED
SEMANTIC_LINK_RECOMMENDATION != CURRENT_AS_IS_LINK
```

The first run preserved 15 recommended internal-link edges after current source/target and semantic-role checks. Those checks support keeping the recommendation, but do not prove the literal current HTML `<a href>` exists. The corrected method therefore requires a literal internal-link graph and separate `RECOMMENDATION_STATE` vs `AS_IS_TOPOLOGY_STATE`.

### Evidence-mechanism selection lesson

Step 11 for this same job had already used deterministic Codex-discovery/profile artifacts. The Step-14 pre-step review failed to ask whether an earlier project stage already had a stronger evidence-acquisition mechanism for the same factual claim.

Permanent control:

```text
BEFORE DESIGNING A STEP EVIDENCE MECHANISM,
ASK WHETHER A PRIOR PROJECT TOOL/RUN CAN TEST THE CLAIM MORE COMPLETELY OR REPRODUCIBLY.

IF YES:
USE/EXTEND IT OR EXPLICITLY JUSTIFY WHY IT IS UNSUITABLE.
```

Canonical Step-14 authorities:

- `STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE_METHOD.md`
- `RULES_ARCHITECTURE_CODEX_SITE_DISCOVERY_GATE_ADDENDUM_2026-09-02.md`
- current-job correction `tests/OKNO_MSK/STEP_14A_CODEX_DISCOVERY_TOPOLOGY_CORRECTION_AND_GATE_2026-09-02.md`

Current OKNO_MSK consequence after the mandatory reconciliation:

```text
STEP14_SEMANTIC_FREEZE = FINAL_PASS
STEP14_CURRENT_SITE_RECONCILIATION = COMPLETE
STEP14_AS_IS_TOPOLOGY = 15_OF_15_CLASSIFIED
STEP14_OVERALL = FINAL_PASS
STEP15 = ALLOWED
```

---

# Step-15 permanent lesson summary

The Step-15 post-run correction establishes four reusable lessons.

### Exact-lineage lesson

```text
QF LABEL LOOKS RIGHT != QF METADATA IS RIGHT
MANUAL RECONSTRUCTION != AUTHORITATIVE ID JOIN
```

The first V1 ledger attached incorrect pair IDs, user jobs, query wording or frozen owners to several valid-looking QF labels. The corrected method requires an exact keyed join from Step13 definition + conflict authorities and zero unresolved lineage mismatches before selection.

### Two-track evaluation lesson

```text
HIGH INFORMATION GAIN = DIAGNOSTIC VALUE
STABLE BASELINE = CONTROL VALUE
DIAGNOSTIC VALUE != ONLY VALID SELECTION VALUE
```

A high-information-only batch is intentionally edge-heavy. When that threatens interpretation, Step15 must include stable controls with explicit falsification roles rather than rejecting every stable case as decorative.

### Generalization lesson

```text
DECISION_DIAGNOSTIC_SET_WITH_CONTROLS
!= REPRESENTATIVE QUERY SAMPLE
```

Step15 supports selected-decision analysis, not prevalence estimates for all site demand unless a separate representative-sampling method exists.

### Confirmation-handoff lesson

```text
ONE AI CHANGE / CONTROL BREAK
!= AUTOMATIC ARCHITECTURE CHANGE
```

Step15 must pre-register a confirmation requirement for material downstream AI deltas; the exact confirmation mechanism is defined in Step16/17.

Canonical authority:

- `STEP_15_AI_CASE_SELECTION_METHOD.md`
- current-job correction `tests/OKNO_MSK/STEP_15_POST_RUN_AUDIT_AND_CORRECTION_2026-09-02.md`

---

Markers:

```text
KW001_STEP_RULES_INDEX_ACTIVE = true
KW001_ROADMAP_STAGE_NOT_EQUAL_VALIDATED_METHOD = true
KW001_RESEARCH_COLLECTED_NOT_EQUAL_METHOD_VALIDATED = true
KW001_RESEARCH_COLLECTED_NOT_EQUAL_EXECUTION_SCHEMA_READY = true
KW001_SOURCE_TO_METHOD_TRACEABILITY_REQUIRED = true
KW001_RESEARCH_TO_EXECUTION_SCHEMA_GATE_ACTIVE = true
KW001_MATERIAL_RESEARCH_REQUIREMENT_OPERATIONALIZATION_REQUIRED = true
KW001_REPRODUCIBLE_EXECUTION_MANIFEST_REQUIRED = true
KW001_REVERSE_CLAIM_TRACE_REQUIRED = true
KW001_UNIVERSAL_METHOD_MEANS_REUSABLE_CORE_PLUS_CURRENT_PROFILE = true
KW001_LOCAL_RULES_MUST_BE_SCOPED_NOT_REMOVED = true
KW001_APPROVED_STEP_STILL_REQUIRES_CURRENT_CONFIGURATION = true
KW001_UNVALIDATED_STEP_REQUIRES_METHOD_RESEARCH = true
KW001_STEP8_METHOD_APPROVED_AFTER_CORRECTION = true
KW001_STEP10_GRANULARITY_METHOD_APPROVED = true
KW001_STEP10_TASK_FIRST_SORTING_METHOD_APPROVED = true
KW001_STEP10_SORTING_QA_METHOD_APPROVED = true
KW001_STEP10_UNIVERSALITY_CORRECTION_APPROVED = true
KW001_STEP10_EXPLICIT_TARGET_COUNT_OR_RANGE_ALLOWED = true
KW001_STEP10_DOMAIN_SPECIFIC_EXECUTION_ALLOWED = true
KW001_STEP12_METHOD_APPROVED_AFTER_THIRD_AUDIT_D12_27 = historical_superseded
KW001_STEP12_REOPENED_AFTER_POST_PASS_EVIDENCE_AUDIT = historical_resolved
KW001_STEP12_FINAL_EXECUTION_PROTOCOL_ACTIVE = true
KW001_STEP12_ACTION_CANNOT_PROVE_ITSELF = true
KW001_STEP12_KNOWN_REGRESSION_ZERO_NOT_EQUAL_GLOBAL_COHERENCE = true
KW001_STEP12_THIRD_AUDIT_EXECUTION_ORDER_CLARIFICATION_ACTIVE = true
KW001_STEP12_EXISTING_PAGE_INTERNAL_LINK_EXECUTION_RULE_ACTIVE = true
KW001_STEP13_METHOD_APPROVED_AFTER_POST_RUN_CORRECTION = true
KW001_STEP13_RESEARCH_TO_EXECUTION_SCHEMA_CORRECTION_ACTIVE = true
KW001_STEP13_SOURCE_KNOWN_BUT_NOT_OPERATIONALIZED_FORBIDDEN = true
KW001_STEP13_BASE_PUBLIC_MODE_SUPPORTED_WITHOUT_PRIVATE_WEBMASTER = true
KW001_STEP13_PRIVATE_HISTORY_OPTIONAL_ENHANCEMENT_EXPLICIT = true
KW001_STEP13_HISTORY_REQUIRED_ONLY_WHEN_CURRENT_SCOPE_REQUIRES_IT = true
KW001_STEP13_QA_MUST_TEST_REQUIRED_BUT_MISSING_EVIDENCE = true
KW001_STEP13_CURRENT_OKNO_BASE_PASS = true
KW001_STEP14_ALLOWED_ONLY_THROUGH_PRESTEP_REVIEW = true
KW001_STEP14_METHOD_APPROVED_AFTER_DISCOVERY_TOPOLOGY_CORRECTION = true
KW001_STEP14_KNOWN_URL_RECHECK_NOT_EQUAL_CURRENT_SITE_DISCOVERY = true
KW001_STEP14_UPSTREAM_INPUT_UNIVERSE_NOT_EQUAL_CURRENT_SITE_UNIVERSE = true
KW001_STEP14_ENDPOINTS_LIVE_NOT_EQUAL_EDGE_IMPLEMENTED = true
KW001_STEP14_RECOMMENDATION_NOT_EQUAL_AS_IS_LINK = true
KW001_STEP14_CODEX_DISCOVERY_REQUIRED_WHEN_COMPLETENESS_OR_TOPOLOGY_MATERIAL = true
KW001_STEP14_PRIOR_PROJECT_EVIDENCE_MECHANISM_REVIEW_REQUIRED = true
KW001_STEP14_CURRENT_OKNO_FINAL_PASS = true
KW001_STEP14_STEP15_BLOCKED_UNTIL_CORRECTION_ACCEPTED = historical_resolved
KW001_STEP15_METHOD_APPROVED_AFTER_POST_RUN_CORRECTION = true
KW001_STEP15_EXACT_QF_JOIN_REQUIRED = true
KW001_STEP15_MANUAL_QF_METADATA_RECONSTRUCTION_FORBIDDEN = true
KW001_STEP15_DIAGNOSTIC_CONTROL_TRACKS_SEPARATE = true
KW001_STEP15_DIAGNOSTIC_SET_NOT_REPRESENTATIVE_BY_DEFAULT = true
KW001_STEP15_MATERIAL_AI_DELTA_CONFIRMATION_HANDOFF_REQUIRED = true
KW001_STEP15_CURRENT_OKNO_V2_PASS = true
KW001_PERMANENT_PROMOTION_REQUIRES_OWNER_APPROVAL = true
```
