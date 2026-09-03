# KW-001 — RULES ARCHITECTURE

Updated: 2026-09-03  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**

This document defines where KW-001 rules and evidence live and how they are combined before a major step.

## 1. Strict two-level operational architecture

```text
LEVEL 1 — PERMANENT UNIVERSAL METHOD
LEVEL 2 — CURRENT JOB WORKSPACE / EVIDENCE
```

There is no third operational layer that may store semi-permanent client/domain facts.

Step-specific permanent methods are part of **Level 1** and must obey the same universality rule as cross-step process gates.

```text
EXECUTABLE CURRENT METHOD
= LEVEL1 UNIVERSAL CORE / STEP METHOD
+ LEVEL2 CURRENT JOB PROFILE / CONSTRAINTS / EVIDENCE
```

Canonical distinctions:

```text
UNIVERSAL METHOD != DOMAIN-FREE EXECUTION
CURRENT JOB DATA MAY BE REQUIRED FOR EXECUTION
BUT
CURRENT JOB DATA MUST NOT BE COPIED INTO PERMANENT METHOD
```

Authority: `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.

---

# 2. Level 1 — permanent universal method

Location:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/
```

Level1 includes:

```text
A. universal cross-step process rules/gates;
B. reusable step-specific methods/lessons registered in STEP_RULES_INDEX.md.
```

Typical Level1 files:

```text
RULES_ARCHITECTURE.md
DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md
STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md
PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md
SOURCE_TO_METHOD_TRACEABILITY_GATE.md
RESEARCH_TO_EXECUTION_SCHEMA_GATE.md
JOB_WORKSPACE_LIFECYCLE.md
BRIDGE_EVIDENCE_PERSISTENCE_GATE.md
PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md
STEP_RULES_INDEX.md
STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md
STEP_<N>_*_METHOD.md
approved permanent addenda/gates
```

## Level1 may contain

```text
reusable rule
step purpose
failure class
root cause
false assumption/process gap
corrected method
non-repeat control
external source/method trace
execution mode schema
parameterized fields/placeholders
claim boundary
pass/fail gate
generic examples that do not encode a concrete client/test case
product-level provider capability authority when genuinely reusable
```

## Level1 must not contain by default

```text
client/test case name
client domain or URL
current product/service/category vocabulary copied from one job
current phrase/query/cluster/action IDs
current page/row/query/link counts
current provider result/request/cost/receipt
current client access state
current job completion state
current job artifact paths under tests/<CASE_ID> or work/<JOB_ID>
current job commit SHA/local HEAD/merge incident details as method inputs
```

Allowed permanent values are only genuinely reusable product/system constants or authorities, not current-job facts.

### Core causal rule

```text
CONCRETE JOB EVIDENCE MAY EARN A PERMANENT LESSON
BUT
CONCRETE JOB EVIDENCE MUST NOT BECOME THE PERMANENT RULE INPUT
```

Permanent promotion transforms:

```text
INCIDENT
-> FAILURE CLASS
-> ROOT CAUSE
-> FALSE ASSUMPTION
-> REUSABLE CONTROL
-> PARAMETERIZED METHOD
-> GENERIC PASS GATE
```

Concrete proof stays Level2 or Git history.

---

# 3. Level 2 — current job workspace / evidence

Canonical future location:

```text
work/<JOB_ID>/
```

Accepted active legacy location:

```text
tests/<CASE_ID>/
```

Level2 contains all concrete execution truth, including:

```text
job/client/site identity
scope/brief/region
actual business/product/service vocabulary
actual URLs
phrases/queries
cluster/unit/action/case IDs
current domain profile
job-specific thresholds/targets when authorized
provider requests/results/receipts/costs
private access/property state
current job modes
row/page/link counts
step manifests
intermediate/final analytical decisions
corrections/postmortems
current job QA
current state/job flow
client deliverables/revisions/economics
```

Level2 may be highly domain-specific. That is correct.

```text
UNIVERSAL METHOD != GENERIC EXECUTION DATA
```

Level2 does not become permanent method merely because a job passed.

---

# 4. Authority and precedence

When sources appear to conflict:

```text
1. latest explicit owner instruction;
2. explicit current client/deliverable constraint authorized by owner;
3. owner-approved Level1 universal process rule;
4. owner-approved Level1 step-specific method;
5. current Level2 frozen job scope/profile;
6. current Level2 accepted evidence/artifact;
7. analyst convenience or older superseded history.
```

A historical PASS never overrides newer defect evidence.

A script does not prove its own correctness.

Provider/API success does not prove the analytical goal was achieved.

External research collected does not prove the method built afterward is supported by it.

---

# 5. Required read order before every major step

Once per dialogue when Bridge capability is material:

```text
CURRENT CANONICAL BRIDGE CAPABILITY
-> ROADMAP-to-BRIDGE MAP
```

Before every major step:

```text
1. READ LEVEL1 CROSS-STEP RULES.
2. READ STEP_RULES_INDEX.md.
3. READ CURRENT STEP'S LEVEL1 METHOD / COMPANION GATES.
4. READ CURRENT LEVEL2 MANIFEST / FLOW / RELEVANT EVIDENCE.
5. LOAD CURRENT DOMAIN/BUSINESS/URL/ID/CONSTRAINT PROFILE FROM LEVEL2.
6. RE-READ RELEVANT PERMANENT FAILURE LESSONS + ROOT CAUSES.
7. STATE WHOLE JOB GOAL / COMPLETED / REMAINING / CURRENT STEP GOAL.
8. SEARCH CURRENT EXTERNAL METHOD SOURCES WHEN REQUIRED.
9. BUILD SOURCE-TO-METHOD TRACE.
10. BUILD RESEARCH-TO-EXECUTION SCHEMA / MANIFEST.
11. CONFIGURE LEVEL1 METHOD WITH LEVEL2 INPUTS WITHOUT COPYING THEM INTO LEVEL1.
12. ADVERSARIALLY SELF-AUDIT.
13. GIVE MANDATORY PLAIN-LANGUAGE OWNER SUMMARY.
14. OBTAIN OWNER AUTHORIZATION WHEN REQUIRED.
15. EXECUTE ONLY AUTHORIZED STEP/MODE.
16. PERSIST / READ BACK / ACCOUNT / QA.
17. REPORT FULL ROADMAP + PLAIN-LANGUAGE END SUMMARY.
```

If the step method is missing/unvalidated:

```text
METHOD_RESEARCH_REQUIRED = true
EXECUTION BLOCKED UNTIL PRE-STEP METHOD GATE PASSES
```

---

# 6. Source-to-method and research-to-execution constraints

Every material method element must trace:

```text
METHOD ELEMENT
-> SOURCE / PROJECT EVIDENCE / OWNER OR DELIVERABLE REQUIREMENT
-> EXACT SUPPORTED CLAIM
-> PROJECT-SPECIFIC ADAPTATION IF NEEDED
-> EXECUTABLE ACTION / OUTPUT
```

Then every material research finding must become:

```text
REQUIREMENT CLASS
-> CURRENT MODE
-> ACTION/COLLECTION
-> ARTIFACT FIELD/OUTPUT
-> FAILURE POLICY
-> CLAIM BOUNDARY
-> QA CHECK
-> ACCEPTANCE CHECK
```

```text
RESEARCH_COLLECTED != METHOD_VALIDATED
SOURCE_DISCOVERED != REQUIREMENT_OPERATIONALIZED
```

---

# 7. Bridge capability alignment

Current Bridge capability authority is the dedicated accepted Bridge product branch/build, not an older extension snapshot inside a working roadmap branch.

At dialogue start or whenever the Bridge materially changes, map each roadmap stage to:

```text
BRIDGE_REQUIRED
BRIDGE_CONDITIONAL
NO_BRIDGE
```

Provider acquisition and analytical judgment remain separate:

```text
BRIDGE = GOVERNED EVIDENCE ACQUISITION / TRANSPORT
CHATGPT = ANALYTICAL JUDGMENT
OWNER = AUTHORIZATION / COMMERCIAL SCOPE AUTHORITY
```

Bridge capability does not itself authorize a provider call. Useful Bridge evidence follows `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md`.

---

# 8. Error recording and permanent promotion

When a material error is found in a current job, Level2 first records:

```text
WHAT FAILED
OBSERVED CONSEQUENCE
ROOT CAUSE
FALSE ASSUMPTION / PROCESS GAP
WHY OLD METHOD WAS INVALID/INSUFFICIENT
CURRENT EVIDENCE/SOURCES USED TO RECHECK
CORRECTION
QA THAT EXPOSED IT
CURRENT LIMITS
```

If reusable, ChatGPT may propose permanent promotion.

Without explicit owner instruction:

```text
LEVEL1 MUTATION = FORBIDDEN
```

With owner authorization, promote only the universal causal lesson and parameterized control. Run the universality contamination audit before finalizing the Level1 change.

---

# 9. Permanent rule universality audit

Every Level1 file created or materially modified must be scanned for:

```text
known CASE_ID values
known client/test domains
concrete tests/<CASE_ID> paths
current action/query/cluster IDs
current job exact counts used as hard method values
current job commit/receipt details
current-job product/service examples masquerading as method
```

Matches require semantic review; generic words are not automatically defects.

Required result:

```text
PERMANENT_RULE_UNIVERSALITY_AUDIT = PASS
JOB_SPECIFIC_BINDINGS_REMAINING = 0
```

---

# 10. Plain-language owner communication

Technical method completeness never substitutes for owner comprehension.

Before authorization and after execution, apply `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`.

```text
PLAIN-LANGUAGE SUMMARY
= WHY THIS STEP
+ WHAT WE ACTUALLY DO/DID
+ WHAT RESULT IT PRODUCES/PRODUCED
```

Missing required summary blocks transition.

---

# 11. Job close

Level2 workspace is disposable under `JOB_WORKSPACE_LIFECYCLE.md`.

```text
JOB WORK COMPLETE
+ FINAL HANDOFF COMPLETE
+ REVISIONS CLOSED
+ NO PENDING PROVIDER/OPERATOR ACTION
+ SAFE_TO_DELETE
-> DELETE CURRENT JOB WORKSPACE
```

Closing a job does not automatically promote lessons to Level1.

---

## Permanent markers

```text
KW001_STRICT_TWO_LEVEL_ARCHITECTURE_ACTIVE = true
KW001_LEVEL1_INCLUDES_CROSS_STEP_AND_STEP_SPECIFIC_PERMANENT_METHODS = true
KW001_LEVEL1_MUST_BE_UNIVERSAL = true
KW001_LEVEL2_CONTAINS_ALL_CONCRETE_JOB_TRUTH = true
KW001_JOB_EVIDENCE_MAY_EARN_RULE_BUT_NOT_BECOME_RULE_INPUT = true
KW001_LEVEL1_CONTAMINATION_SCAN_REQUIRED = true
KW001_JOB_EXECUTION_SUCCESS_NOT_EQUAL_PERMANENT_METHOD_VALIDATION = true
KW001_RESEARCH_COLLECTED_NOT_EQUAL_METHOD_VALIDATED = true
KW001_PROVIDER_SUCCESS_NOT_EQUAL_ANALYTICAL_PASS = true
KW001_PLAIN_LANGUAGE_OWNER_SUMMARY_REQUIRED = true
```
