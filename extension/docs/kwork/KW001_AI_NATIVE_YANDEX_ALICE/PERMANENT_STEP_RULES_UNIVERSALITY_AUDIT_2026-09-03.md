# KW-001 — PERMANENT STEP-RULES UNIVERSALITY AUDIT

Date: 2026-09-03  
Status: **PASS AFTER REOPENED CROSS-FILE AUTHORITY CONSISTENCY CHECK / OWNER-REQUESTED FULL LEVEL-1 REVIEW**

This audit checks reusable Level-1 rule/method/gate/runbook authorities for accidental coupling to one concrete rehearsal/client/site **and** for stale cross-file authority statements that can make a universal method internally inconsistent.

It follows:

`PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`

## 1. Audit boundary

Audited scope:

```text
permanent .md rule / method / gate / policy / runbook / index authorities
under the KW-001 Level-1 methodology directory
```

Excluded from the universality verdict:

```text
current Level-2 job workspaces under tests/<CASE_ID>/
historical helper/migration/patch .py scripts that are not declared methodology authority
Git history containing old concrete evidence
```

Helper scripts may contain historical migration mechanics. They must not be used as methodology authority; future method decisions must come from the current `.md` authorities registered by `STEP_RULES_INDEX.md`.

The audit also distinguishes:

```text
JOB-SPECIFIC CONTAMINATION
!=
STALE CROSS-FILE AUTHORITY / CAPABILITY STATEMENT
```

Both can break reuse. The first hard-codes one job into the method; the second can make two permanent authorities disagree about what is currently supported or validated.

## 2. Contamination and consistency classes checked

Every material method/rule was reviewed for these classes:

```text
CONCRETE TEST/CLIENT IDENTITY
CONCRETE CLIENT DOMAIN / URL
CURRENT-JOB PRODUCT / SERVICE / SEMANTIC FAMILY AS NORMATIVE RULE
CURRENT-JOB QUERY / CLUSTER / ACTION / CASE ID
CURRENT-JOB ROW / PAGE / LINK / QUERY TOTAL USED AS UNIVERSAL THRESHOLD
CURRENT-JOB PROVIDER COST / REQUEST RECEIPT
CURRENT-JOB COMMIT SHA / LOCAL HEAD / CONFLICT PATH
CURRENT-JOB COMPLETION / BLOCKED STATE
CONCRETE tests/<CASE_ID>/ PATH USED AS PERMANENT AUTHORITY
ACCOUNTING RESULT COPIED INTO METHODOLOGY INSTEAD OF ABSTRACTED
STALE CAPABILITY SNAPSHOT DUPLICATED OUTSIDE CURRENT CAPABILITY AUTHORITY
STALE STEP-METHOD STATUS DUPLICATED OUTSIDE STEP_RULES_INDEX / CURRENT METHOD AUTHORITY
PARENT POLICY CONTRADICTING A LATER OWNER-APPROVED CAPABILITY/METHOD UPDATE
```

A universal product constant, external source URL, method filename, generic placeholder such as `<CURRENT_SITE_URL>`, or abstract example is not contamination.

A dedicated current capability authority may legitimately contain product-version facts when those facts describe the reusable product itself rather than a client job. Other permanent files should reference that authority rather than copying a capability list that can become stale.

## 3. Files checked

### Cross-step / architecture authorities

- `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md`
- `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`
- `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY_BRIDGE_CAPABILITY_UPDATE_2026-09-01.md`
- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`
- `DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md`
- `EVIDENCE_QUALITY_AND_PROVIDER_COST_POLICY.md`
- `IMPLEMENTATION_PLAN.md`
- `JOB_WORKSPACE_LIFECYCLE.md`
- `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`
- `PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md`
- `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `RULES_ARCHITECTURE.md`
- `RULES_ARCHITECTURE_CODEX_EVIDENCE_CONFLICT_PRESERVATION_ADDENDUM_2026-09-02.md`
- `RULES_ARCHITECTURE_CODEX_EXECUTION_RELIABILITY_GATE_ADDENDUM_2026-09-02.md`
- `RULES_ARCHITECTURE_CODEX_SITE_DISCOVERY_GATE_ADDENDUM_2026-09-02.md`
- `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`
- `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`
- `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md`
- `STEP_RULES_INDEX.md`
- `WORKING_RUNBOOK_FOR_CHATGPT.md`

### Step-specific authorities

- `STEP_08_SEARCH_STAGE_FREEZE_METHOD.md`
- `STEP_10_CLUSTERING_GRANULARITY_METHOD.md`
- `STEP_10_SORTING_AND_QA_METHOD.md`
- `STEP_10_TASK_FIRST_SORTING_DECISION_METHOD.md`
- `STEP_11_PAGE_OWNERSHIP_METHOD.md`
- `STEP_12_EVIDENCE_INDEPENDENCE_AND_CURRENT_CONTENT_VALIDATION.md`
- `STEP_12_FINAL_EXECUTION_PROTOCOL.md`
- `STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md`
- `STEP_12_STRUCTURAL_ACTION_METHOD.md`
- `STEP_12_THIRD_AUDIT_EXECUTION_ORDER_CLARIFICATION.md`
- `STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md`
- `STEP_14_CODEX_BROWSER_FIRST_DISCOVERY_CORRECTION_2026-09-02.md`
- `STEP_14_CODEX_CRAWLER_EXECUTION_RELIABILITY_GATE.md`
- `STEP_14_CODEX_REPOSITORY_SYNC_GATE.md`
- `STEP_14_NO_RUN_SKIP_AND_CRAWLER_REMOVAL_RULE_2026-09-02.md`
- `STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE_METHOD.md`
- `STEP_15_AI_CASE_SELECTION_METHOD.md`
- `STEP_17_PERMANENT_METHOD_PROMOTION_AND_NON_REPEAT_ADDENDUM_2026-09-03.md`
- `STEP_17_SEARCH_VS_AI_COMPARISON_METHOD.md`
- `STEP_18_PRIORITIZATION_AND_IMPLEMENTATION_READINESS_METHOD.md`

## 4. Defect classes found during this audit

### U-01 — concrete rehearsal evidence embedded in permanent Step methods

Some permanent methods historically copied concrete site identity, domain-specific semantic examples, exact row/page/link totals and current job state directly into the reusable lesson.

**Root cause:** the concrete execution proved a useful lesson, but promotion copied the proof itself instead of abstracting its causal failure class.

**Correction:** affected permanent methods were rewritten to keep:

```text
WHAT FAILED
ROOT CAUSE
FALSE ASSUMPTION
CORRECT CONTROL
PARAMETERIZED PASS GATE
```

while concrete proof remains Level-2/Git-history evidence.

### U-02 — concrete repository incident details embedded in execution rules

Repository-sync/reliability rules historically contained exact local/remote commit identities and concrete conflict paths.

**Root cause:** incident diagnostics were mistaken for permanent rule inputs.

**Correction:** rules now retain abstract conflict classes, safe-sync procedure, staged runner qualification and lossless evidence-preservation controls without concrete incident identity.

### U-03 — current job result embedded in permanent methodology index/lesson ledger

A methodology index/lesson summary historically included current job completion/results.

**Root cause:** navigation convenience blurred `PERMANENT METHOD STATUS` with `CURRENT JOB STEP STATUS`.

**Correction:** index/lesson ledger now store only reusable method status/authority and causal lessons. Current progress remains Level-2 job flow/state.

### U-04 — concrete historical case count remained in a universal Step17 lesson

A Step17 permanent explanation still referred to a concrete completed-case count from one execution even though the underlying lesson was generic.

**Root cause:** job-output completeness was used as the example for the permanent failure and the example count survived method promotion.

**Correction:** the number was removed. The permanent rule is now only:

```text
JOB OUTPUT COMPLETENESS != PERMANENT METHOD VALIDATION
```

### U-05 — Step18 initially lacked a permanent two-layer priority/readiness method

The older universal runbook contained only a lightweight priority sketch and did not mechanically separate ideal analytical priority from implementation readiness.

**Root cause:** a planning sketch was treated as sufficient until a real end-to-end prioritization execution exposed the missing implementation-calibration layer.

**Correction:** `STEP_18_PRIORITIZATION_AND_IMPLEMENTATION_READINESS_METHOD.md` is now the canonical permanent authority and `STEP_RULES_INDEX.md` registers it as approved/active.

### U-06 — contamination scan passed while a parent policy still contained stale permanent authority statements

After the first universality audit PASS, `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md` still contained two stale statements:

```text
1. an obsolete fixed snapshot saying Webmaster Bridge support was only a limited first slice and lacked enhanced query-by-URL export;
2. wording that treated Step18 prioritization as a future/unvalidated method even though a permanent Step18 method had already been approved.
```

This was **not** client-job contamination. It was a cross-file authority-consistency failure.

**Root cause:**

```text
CONTAMINATION SCAN
WAS TREATED AS IF IT ALSO PROVED
CURRENT CROSS-FILE AUTHORITY CONSISTENCY
```

The audit checked whether job facts leaked into Level-1, but did not separately check whether one permanent file had become stale relative to a later owner-approved permanent capability/method authority.

**Correction:**

- the parent access policy now defers current Bridge capability to `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY_BRIDGE_CAPABILITY_UPDATE_2026-09-01.md` and the canonical Bridge product authority named there instead of duplicating a method list;
- the parent policy now recognizes the approved permanent Step18 method and describes private first-party data as optional analytical calibration/enhancement rather than as support for a hypothetical future method;
- first real client access now triggers capability **verification against current authority**, and actual Bridge enhancement only if a named required evidence surface is truly missing;
- this audit was reopened and the consistency class added before final PASS.

Permanent control:

```text
JOB CONTAMINATION SCAN != CROSS-FILE AUTHORITY CONSISTENCY CHECK

PARENT / SUMMARY POLICY
-> REFERENCE CURRENT SPECIALIZED AUTHORITY
-> DO NOT DUPLICATE FAST-CHANGING CAPABILITY SNAPSHOTS
```

## 5. Universal-vs-local rule after audit

```text
UNIVERSAL METHOD
= CAUSAL REUSABLE CORE

CURRENT EXECUTION
= UNIVERSAL CORE
+ CURRENT DOMAIN PROFILE
+ CURRENT SITE / BUSINESS / EVIDENCE
+ CURRENT OWNER / DELIVERABLE CONSTRAINTS
```

Therefore domain-specific facts are **required where they make the current job correct**, but they live in Level-2/current execution configuration and are not copied into Level-1 as universal truth.

Cross-file authority consistency adds another boundary:

```text
STABLE PARENT POLICY
= COMMERCIAL / ACCESS / GENERAL GOVERNANCE

SPECIALIZED CAPABILITY AUTHORITY
= CURRENT REUSABLE PRODUCT CAPABILITY SNAPSHOT

STEP_RULES_INDEX + STEP METHOD
= CURRENT PERMANENT METHOD VALIDATION STATUS
```

A parent policy should reference the specialized authority rather than re-copying fast-changing facts.

## 6. Audit verdict

```text
FILES_CHECKED = all current permanent .md rule/method/gate/runbook/index authorities listed above
CAUSAL LESSONS PRESERVED = true
CONCRETE REHEARSAL/CLIENT DOMAIN AS PERMANENT RULE = 0
CONCRETE CURRENT-JOB SEMANTIC IDS AS PERMANENT RULE INPUT = 0
CONCRETE CURRENT-JOB COUNTS AS UNIVERSAL THRESHOLDS = 0
CONCRETE CURRENT-JOB COMMIT/RECEIPT DETAILS AS METHOD INPUT = 0
CURRENT JOB STATUS IN PERMANENT STEP INDEX = 0
LEVEL2 JOB FACTS REQUIRED FOR REAL EXECUTION = allowed and required when scoped
HISTORICAL HELPER SCRIPTS TREATED AS METHOD AUTHORITY = false
STALE BRIDGE METHOD LIST IN PARENT ACCESS POLICY = 0
STALE STEP18 UNVALIDATED/FUTURE STATUS IN PARENT ACCESS POLICY = 0
PARENT POLICY DEFERS CURRENT BRIDGE CAPABILITY TO SPECIALIZED AUTHORITY = true
CROSS_FILE_AUTHORITY_CONSISTENCY_RECHECK = PASS
VERDICT = PASS
```

## 7. Non-repeat control

Before any future permanent rule update:

```text
PROMOTE FAILURE CLASS / ROOT CAUSE / CONTROL
NOT JOB FACTS
```

Then run both:

```text
A. contamination scan from PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md;
B. cross-file authority consistency check against specialized capability authorities and STEP_RULES_INDEX/current approved step methods.
```

A PASS is final only after both checks and final GitHub readback.