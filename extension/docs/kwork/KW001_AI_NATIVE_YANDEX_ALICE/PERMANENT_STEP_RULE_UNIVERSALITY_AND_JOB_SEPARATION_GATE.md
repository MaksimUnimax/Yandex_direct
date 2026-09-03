# KW-001 — PERMANENT STEP-RULE UNIVERSALITY AND JOB-SEPARATION GATE

Date: 2026-09-03  
Status: **ACTIVE / UNIVERSAL / OWNER-AUTHORIZED / APPLIES TO ALL PERMANENT STEP RULES**

## 1. Purpose

Permanent methodology must preserve reusable causality without anchoring future work to one rehearsal, client, site, product family, row count, URL set, provider receipt or repository incident.

Canonical architecture:

```text
PERMANENT METHOD
= REUSABLE RULE + PURPOSE + ROOT CAUSE + CONTROL + SOURCE CLASS + PASS GATE

CURRENT JOB WORKSPACE
= CONCRETE DOMAIN + URLS + IDS + COUNTS + RESULTS + RECEIPTS + CLIENT FACTS + CURRENT STATUS
```

These layers may reference each other by role, but their factual contents must not be merged.

---

## 2. Failure that caused this gate

Several permanent step-method files preserved useful lessons from controlled executions but copied the concrete rehearsal identity and current-job evidence into the universal rule itself.

Examples of the **failure class** included:

```text
specific test-case names inside permanent method prose;
specific client/site URLs inside permanent execution instructions;
exact current-job row counts used as universal pass-gate values;
concrete semantic family/product names used as if they were reusable examples;
exact commit SHAs / local branch incidents inside a permanent synchronization rule;
current job completion state copied into a universal methodology index.
```

### Root cause

```text
PROJECT TEST EVIDENCE
WAS USED TO EARN A REUSABLE LESSON
AND THEN
THE TEST EVIDENCE ITSELF WAS COPIED INTO THE REUSABLE LESSON
```

The distinction between:

```text
"this incident proved the rule"
```

and:

```text
"this incident is part of the rule"
```

was not enforced mechanically.

A second root cause was convenience: exact historical counts/examples made a lesson easier to explain during the original correction, but no later promotion step stripped them back to reusable variables/classes.

---

## 3. Permanent rule

A permanent step-method/rule file must not contain concrete job evidence except when the value is itself a genuinely universal product contract or owner-approved permanent constant.

Forbidden by default inside permanent step rules:

```text
CLIENT / TEST CASE NAME
CLIENT DOMAIN OR URL
CLIENT PRODUCT / SERVICE FAMILY USED AS A CURRENT-JOB EXAMPLE
CURRENT-JOB SEMANTIC CLUSTER / QUERY / ACTION ID
CURRENT-JOB ROW / PAGE / LINK / QUERY COUNTS
CURRENT-JOB PROVIDER COST / REQUEST ID / RECEIPT
CURRENT-JOB COMMIT SHA / LOCAL HEAD / MERGE PATH
CURRENT-JOB COMPLETION / BLOCKED STATE
CURRENT-JOB ARTIFACT PATH UNDER tests/<CASE_ID>/
```

Allowed:

```text
<CURRENT_SITE_URL>
<CURRENT_CASE_ID>
<CURRENT_EXPECTED_TOTAL>
<CURRENT_REQUIRED_EDGE_SET>
<CURRENT_JOB_ARTIFACT>
GENERIC_PRODUCT / SERVICE / INFORMATION EXAMPLES
ABSTRACT FAILURE CLASSES
PROJECT_TEST_VALIDATED
REFERENCE TO "CURRENT JOB WORKSPACE" WITHOUT COPYING ITS FACTS
```

A permanent rule may say that a controlled rehearsal exposed a failure. It should preserve **what failed, root cause and non-repeat control**, not the identity/data of that rehearsal.

---

## 4. Promotion transformation

When a job-specific lesson is promoted into permanent methodology, perform this transformation:

```text
CONCRETE INCIDENT
-> IDENTIFY FAILURE CLASS
-> IDENTIFY ROOT CAUSE
-> IDENTIFY FALSE ASSUMPTION
-> IDENTIFY GENERAL CONTROL
-> PARAMETERIZE COUNTS / URLS / IDS
-> REMOVE CLIENT/CASE IDENTITY
-> MOVE/KEEP CONCRETE PROOF IN LEVEL-2 WORKSPACE
-> ADD GENERIC PASS/FAIL GATE
```

Canonical distinction:

```text
CONCRETE PROOF MAY EARN A PERMANENT RULE
CONCRETE PROOF MUST NOT BECOME A PERMANENT INPUT VALUE
```

---

## 5. Causal lesson requirement

Do not solve contamination by deleting the incident lesson entirely.

A reusable correction must still explain:

```text
WHAT FAILED
WHY IT FAILED
WHAT FALSE ASSUMPTION / PROCESS GAP CAUSED IT
HOW THE CONTROL BLOCKS THAT CAUSE
WHAT WOULD TRIGGER RE-REVIEW OF THE RULE
```

Therefore:

```text
UNIVERSALIZATION != LOSS OF CAUSAL HISTORY
```

The goal is to remove anchoring data, not to turn the rule into an unexplained checklist.

---

## 6. Job-specific examples

If an exact example is necessary to understand or regression-test a method, store it in one of:

```text
tests/<CASE_ID>/
job-specific regression fixture
job execution manifest
job QA artifact
job incident report
```

The permanent method may state:

```text
PROJECT_TEST_VALIDATED
```

and identify the **type of evidence**, but should not copy concrete business/site facts.

---

## 7. Permanent-rule audit before final write

Every created or modified permanent step rule must pass a contamination scan before final readback.

Search at minimum for:

```text
known current/past CASE_ID values;
known client/test domains;
`tests/` paths with concrete case directories;
current-job action/query/cluster IDs;
current-job exact totals used as hard gates;
current-job commit SHAs and local branch state;
current-job product/service examples not explicitly genericized.
```

Then manually inspect matches. A word can be legitimate in a generic context, so this is a semantic audit, not only a string search.

Required output:

```text
PERMANENT_RULE_UNIVERSALITY_AUDIT
files_checked
matches_reviewed
job_specific_bindings_remaining
allowed_universal_constants
verdict
```

---

## 8. Interaction with domain profiles

This gate does **not** prohibit domain-specific execution.

Canonical rule:

```text
UNIVERSAL METHOD != DOMAIN-FREE EXECUTION
```

Current execution may and should use actual products, services, phrases, URLs, taxonomy and local rules when needed. Those facts belong in the current domain/job profile, manifest, rules overlay or Level-2 evidence, not in the permanent core.

A scoped local rule is valid:

```text
LOCAL RULE MUST BE SCOPED
!= LOCAL RULE MUST BE REMOVED
```

---

## 9. Pass gate

Before a permanent step method can be called universal/active after modification:

```text
CAUSAL LESSON PRESERVED = true
CLIENT_OR_TEST_CASE_NAME_IN_PERMANENT_METHOD = 0
CLIENT_DOMAIN_OR_URL_IN_PERMANENT_METHOD = 0
CURRENT_JOB_COUNTS_AS_UNIVERSAL_THRESHOLDS = 0
CURRENT_JOB_IDS_AS_UNIVERSAL_METHOD_INPUTS = 0
CURRENT_JOB_COMMIT_OR_RECEIPT_DETAILS_IN_METHOD = 0
CONCRETE_TEST_ARTIFACT_PATHS_AS_METHOD_AUTHORITY = 0
JOB-SPECIFIC PROOF REMAINS IN LEVEL2 = true
PARAMETERIZED EXECUTION VARIABLES = true where applicable
FINAL GITHUB READBACK = PASS
```

A historical file may contain generic external-source URLs or permanent project-level repository paths. Those are not client-job contamination.

---

## 10. Permanent markers

```text
KW001_PERMANENT_STEP_RULE_UNIVERSALITY_GATE_ACTIVE = true
KW001_PERMANENT_METHOD_MUST_NOT_COPY_JOB_EVIDENCE = true
KW001_PROJECT_TEST_EVIDENCE_MAY_EARN_RULE_BUT_NOT_BECOME_RULE_INPUT = true
KW001_JOB_SPECIFIC_RESULTS_BELONG_LEVEL2 = true
KW001_PERMANENT_LESSON_MUST_PRESERVE_ROOT_CAUSE = true
KW001_UNIVERSALIZATION_MUST_PARAMETERIZE_COUNTS_URLS_IDS = true
KW001_PERMANENT_RULE_CONTAMINATION_SCAN_REQUIRED = true
```
