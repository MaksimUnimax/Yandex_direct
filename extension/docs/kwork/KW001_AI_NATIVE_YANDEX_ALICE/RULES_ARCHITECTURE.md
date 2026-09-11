# KW-001 — RULES ARCHITECTURE

Updated: 2026-09-11  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**

This document defines where KW-001 rules and evidence live and how they are combined before a major step.

Cross-Kwork large-artifact publication authority:

`../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md`

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

Cross-Kwork authorities located one level above KW-001 also apply when explicitly owner-locked for the whole Kwork ecosystem. In particular:

```text
../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md
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
3. owner-approved cross-Kwork universal authority;
4. owner-approved Level1 universal process rule;
5. owner-approved Level1 step-specific method;
6. current Level2 frozen job scope/profile;
7. current Level2 accepted evidence/artifact;
8. analyst convenience or older superseded history.
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
1. READ APPLICABLE CROSS-KWORK AUTHORITIES, INCLUDING LARGE-ARTIFACT PUBLICATION RULE WHEN FILE GENERATION/PERSISTENCE IS MATERIAL.
2. READ LEVEL1 CROSS-STEP RULES.
3. READ STEP_RULES_INDEX.md.
4. READ CURRENT STEP'S LEVEL1 METHOD / COMPANION GATES.
5. READ CURRENT LEVEL2 MANIFEST / FLOW / RELEVANT EVIDENCE.
6. LOAD CURRENT DOMAIN/BUSINESS/URL/ID/CONSTRAINT PROFILE FROM LEVEL2.
7. RE-READ RELEVANT PERMANENT FAILURE LESSONS + ROOT CAUSES.
8. STATE WHOLE JOB GOAL / COMPLETED / REMAINING / CURRENT STEP GOAL.
9. SEARCH CURRENT EXTERNAL METHOD SOURCES WHEN REQUIRED.
10. BUILD SOURCE-TO-METHOD TRACE.
11. BUILD RESEARCH-TO-EXECUTION SCHEMA / MANIFEST.
12. CONFIGURE LEVEL1 METHOD WITH LEVEL2 INPUTS WITHOUT COPYING THEM INTO LEVEL1.
13. ADVERSARIALLY SELF-AUDIT.
14. GIVE MANDATORY PLAIN-LANGUAGE OWNER SUMMARY.
15. OBTAIN OWNER AUTHORIZATION WHEN REQUIRED.
16. EXECUTE ONLY AUTHORIZED STEP/MODE.
17. PERSIST USING THE CHEAPEST RELIABLE APPROVED TRANSPORT; THEN READ BACK / ACCOUNT / QA.
18. REPORT FULL ROADMAP + PLAIN-LANGUAGE END SUMMARY.
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

# 7A. Large-artifact persistence and publication transport

Canonical authority:

`../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md`

When Work or another executor creates large/tabular/binary artifacts, publication transport is a separate execution concern from the analytical work.

Required policy:

```text
IF NATIVE AUTHENTICATED GIT IS ALREADY AVAILABLE AND RELIABLE
→ USE NORMAL GIT + REMOTE READBACK

ELSE IF OWNER RELAY IS CHEAPER / FASTER / SAFER
→ LOCAL GENERATION + LOCAL QA
→ PROVIDE DOWNLOADABLE FILES / OPTIONAL TRANSPORT ZIP
→ PROVIDE DIRECT GITHUB UPLOAD LINK TO CORRECT REPO / BRANCH / DIRECTORY
→ OWNER UPLOADS THROUGH NORMAL AUTHENTICATED WEB UI
→ REMOTE READBACK + IDENTITY QA

DO NOT MOVE LARGE FILE BY DEFAULT THROUGH
LLM TEXT / BASE64 / MANY CONNECTOR CHUNKS / GIANT TOOL ARGUMENTS
```

Owner relay is an approved normal transport path, not a quality reduction and not evidence degradation.

A Git credential/network failure after local QA does not justify regenerating already valid artifacts.

```text
LOCAL_ARTIFACT_COMPLETE != REMOTE_PUBLICATION_COMPLETE
OWNER_UPLOAD_COMPLETE != REMOTE_READBACK_PASS
```

Remote readback remains mandatory whichever transport route is used.

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

For an owner-relay publication handoff, keep the instruction operational and short: what files to download, where to upload them, whether to unzip, the target branch/folder, and what confirmation to return. Do not bury the owner upload action under a long Git-auth incident report.

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
KW001_LARGE_ARTIFACT_OWNER_RELAY_RULE_INHERITED = true
KW001_LARGE_ARTIFACT_MODEL_BYTE_TRANSPORT_FORBIDDEN_BY_DEFAULT = true
KW001_REMOTE_READBACK_AFTER_OWNER_RELAY_REQUIRED = true
```
