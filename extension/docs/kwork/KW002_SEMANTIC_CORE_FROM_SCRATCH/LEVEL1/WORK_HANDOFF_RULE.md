# KW-002 — LEVEL 1 CHATGPT WORK HANDOFF RULE

Status: **ACTIVE / OWNER-LOCKED**  
Owner instruction: 2026-09-08  
Owner transport amendment: 2026-09-11  
Owner single-staging amendment: 2026-09-17  
Owner role-boundary correction: 2026-09-17 — **MAIN CHAT GOVERNANCE MUST NOT BE DUPLICATED INSIDE WORK RUNTIME.**

Cross-Kwork artifact-publication authority:

`../../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md`

## 1. Purpose

Large-data work must not be degraded merely to fit ordinary chat context.

```text
LARGE DATA
!= SAMPLE IT
!= TRUNCATE IT
!= SUMMARIZE BEFORE ANALYSIS

LARGE DATA
→ HAND OFF THE COMPLETE EXECUTION UNIT TO CHATGPT WORK
```

At the same time:

```text
MAIN CHAT GOVERNANCE
!= WORK EXECUTION
```

Work is an execution environment for a contract that Main Chat has already researched, designed, checked and released.

## 2. Canonical roles

```text
MAIN CHATGPT
= ARCHITECT / METHOD CONTROL / RULE REREAD / FRESH RESEARCH / OWNER REPORT / WORK PROMPT AUTHOR / RELEASE / RETURN QA / ACCEPTANCE / CURSOR CONTROL

OWNER
= AUTHORIZATION / PROMPT RELAY / DOWNLOAD + SINGLE-STAGING UPLOAD / COMMERCIAL SCOPE AUTHORITY

CHATGPT WORK
= EXECUTE THE RELEASED FULL-VOLUME TASK / TRANSFORM DATA / MATERIALIZE ARTIFACTS / LOCAL QA / PACKAGE HANDOFF
```

Permanent distinction:

```text
MAIN CHAT DECIDES WHAT / WHY / WHETHER / UNDER WHICH AUTHORITY
WORK EXECUTES HOW THE RELEASED PROMPT SAYS
```

## 3. Work trigger

Use Work when one or more are true:

- complete analysis of a large table or several large files is required;
- full-volume row joins/dedup/reconciliation are unsafe in ordinary chat;
- sampling/truncation would otherwise be required for context convenience;
- pairwise/cluster/crawl/frontier work creates large intermediate data;
- large structured deliverables must be generated and QA'd;
- ordinary context materially risks skipped rows, lost provenance or partial QA.

This is a quality trigger, not an arbitrary row threshold.

## 4. Main Chat pre-handoff responsibility

Before Work receives the task, Main Chat owns and completes, where applicable:

```text
CURRENT LIVE AUTHORITY FETCH
→ FULL APPLICABLE RULE REREAD
→ PRIOR FAILURE / NON-REPEAT REVIEW
→ FRESH EXTERNAL METHODOLOGY RESEARCH
→ OWNER-FACING CLICKABLE SOURCE DISCLOSURE
→ PLAIN-LANGUAGE OWNER REPORT
→ WORK TRIGGER DECISION
→ PRE-HANDOFF MANIFEST
→ COMPLETE EXECUTION CONTRACT
→ RELEASE AUTHORIZATION
```

These are **Main Chat responsibilities**.

Do not move them into Work merely because Work will execute the next step.

## 5. Canonical Work prompt

Main Chat writes one complete canonical Work prompt containing only what the executor needs to perform the released task, such as:

```text
TASK IDENTITY
REPOSITORY / BRANCH / JOB
EXACT INPUT AUTHORITIES
ALLOWED / PROHIBITED SOURCES
EXECUTION METHOD
FULL-VOLUME BOUNDARY
CLAIM BOUNDARIES
OUTPUT FILES / SCHEMAS
QA / PASS / FAIL / HOLD
STOP CONDITIONS
HANDOFF / PUBLICATION CONTRACT
```

The owner relays this prompt without needing to design, complete or correct it.

## 6. Explicit prohibition — do not duplicate Main Chat governance in Work

For an ordinary execution task, Work MUST NOT be burdened with a second full governance/release cycle.

By default, do **not** require Work to:

```text
READ ALL LEVEL1 RULES IN FULL
READ MAIN CHAT 00/01 ANTI-REGRESSION GATES
RERUN FRESH EXTERNAL METHODOLOGY RESEARCH
REPEAT OWNER-FACING SOURCE DISCLOSURE
WRITE OWNER-FACING PRE-STEP REPORT
REPEAT PLAIN-LANGUAGE RELEASE REPORT
REDECIDE WHETHER THE STEP IS AUTHORIZED
REVIEW MAIN CHAT'S HISTORICAL FAILURE INCIDENTS
REBUILD THE ROADMAP OR RELEASE DECISION
```

Those controls belong to Main Chat and must already be reflected in the frozen execution prompt.

Exception: if the Work task itself is explicitly a **methodology/rule audit/research task**, then those activities can be part of that task by definition.

## 7. Allowed Work startup preflight — narrow and technical only

Work may and usually should perform a bounded freshness check before expensive execution:

```text
FETCH CURRENT REMOTE HEAD
→ VERIFY THE NAMED RELEASE RECORD / PROMPT IDENTITY STILL EXISTS
→ VERIFY NAMED INPUT FILES / MANIFEST / SCHEMA / AUTHORITY HASHES
→ CLASSIFY WHETHER THERE IS MATERIAL EXECUTION-CONTRACT DRIFT
```

If no material drift:

```text
EXECUTE IMMEDIATELY
```

If material drift affects the released task:

```text
STOP
→ RETURN AUTHORITY_DRIFT WITH THE EXACT CONFLICT
→ DO NOT IMPROVISE A NEW METHOD
```

This preflight is not permission to reread the entire governance stack or redo Main Chat's release process.

## 8. Work authority boundary

```text
WORK OUTPUT != AUTOMATICALLY ACCEPTED TRUTH
```

Work must follow the frozen prompt and the specific execution/data contracts named there. It may not:

- create new permanent methodology;
- override client scope;
- silently drop rows;
- replace missing evidence with assumptions;
- change evidence classes;
- treat partial processing as complete;
- use prohibited prior research;
- make provider calls outside the explicit task;
- perform downstream stages prohibited by the prompt.

## 9. Pre-handoff manifest

Before the owner relay, Main Chat must freeze at least:

```text
JOB_ID
STEP_ID
WHY_WORK_REQUIRED
ALLOWED_INPUT_FILES / SOURCES
PROHIBITED_INPUT_FILES / SOURCES
CURRENT_AUTHORITATIVE_UPSTREAM_ARTIFACTS
EXACT_EXECUTION_GOAL
REQUIRED_OUTPUT_FILES / TABLES
MANDATORY_FIELDS
ROW / COUNT / JOIN EXPECTATIONS where known
CLAIM_BOUNDARIES
QA / ACCEPTANCE CHECKS
STOP CONDITIONS
ARTIFACT_PUBLICATION_POLICY
```

For material files:

```text
ARTIFACT_PUBLICATION_POLICY = OWNER_RELAY_SINGLE_STAGING_REQUIRED
LARGE_ARTIFACT_MODEL_TRANSPORT = FORBIDDEN_BY_DEFAULT
OWNER_RELAY_ALLOWED = true
OWNER_RELAY_SINGLE_STAGING_REQUIRED = true
OWNER_MUST_NOT_ROUTE_FILES_TO_FINAL_PATHS = true
WORK_DIRECT_LARGE_ARTIFACT_GITHUB_PUBLICATION = FORBIDDEN_BY_DEFAULT
MAIN_CHAT_FINAL_PLACEMENT_AND_ACCEPTANCE_REQUIRED = true
REMOTE_READBACK_REQUIRED = true
```

Also freeze:

```text
OWNER_RELAY_STAGING_REPOSITORY
OWNER_RELAY_STAGING_BRANCH
OWNER_RELAY_STAGING_DIRECTORY
OWNER_RELAY_UPLOAD_URL
FINAL_PATH_MANIFEST
```

## 10. Final-path manifest

Every Work handoff file maps to:

```text
HANDOFF_FILENAME
FINAL_REPOSITORY_PATH
ACTION = NEW | REPLACE
ARTIFACT_ROLE
EXPECTED_HASH / IDENTITY MARKER where available
STAGING_CLEANUP_REQUIRED = true | false
```

Many final paths never create many owner upload actions.

```text
ONE HANDOFF UNIT
→ ONE OWNER UPLOAD TARGET
```

The owner never resolves path routing or filename collisions manually.

## 11. Large-artifact owner handoff

Work gives the owner:

- direct download link for every required final file;
- one transport ZIP when multiple files exist;
- exact ZIP contents;
- final-path manifest;
- exactly one primary GitHub Upload-files link;
- staging repo / branch / directory;
- one minimal completion signal, e.g. `готово`.

Operational instruction:

```text
1. download the files/ZIP;
2. extract if needed;
3. upload ALL handoff files together to the ONE staging link;
4. commit;
5. reply "готово".
```

Do not ask the owner to split files by Level1/Level2/job directories, perform NEW/REPLACE routing or clean staging.

## 12. After owner upload — Main Chat owns placement and acceptance

After `готово`:

```text
MAIN CHAT FETCHES CURRENT REMOTE
→ VERIFIES STAGING PAYLOAD AGAINST MANIFEST
→ CREATES / REPLACES CANONICAL FINAL FILES SAFELY
→ REMOVES STAGING-ONLY COPIES
→ READS BACK FINAL PATHS
→ RUNS IDENTITY / MECHANICAL / ANALYTICAL RETURN QA
→ UPDATES MUTABLE JOB_FLOW / CURSOR
→ ONLY THEN ACCEPTS / ADVANCES
```

Work may assist with artifact QA, but the governance/acceptance decision belongs to Main Chat.

## 13. Large file bytes must not be transported through the model

Forbidden by default:

```text
PRINT ENTIRE LARGE FILE INTO CHAT
BASE64 FILE INTO MODEL OUTPUT
SPLIT FILE INTO MANY TEXT CHUNKS FOR CONNECTOR WRITES
RECONSTRUCT LARGE FILE THROUGH GIANT TOOL ARGUMENTS
REGENERATE VALID DATA MERELY BECAUSE TRANSPORT FAILED
```

Hashes, counts, headers, bounded excerpts and mechanical QA are allowed.

## 14. Publication-state truth

Keep separate:

```text
LOCAL_ARTIFACT_COMPLETE
LOCAL_QA_PASS
PUBLICATION_HANDOFF_READY
OWNER_UPLOAD_COMPLETE
STAGING_READBACK_PASS
FINAL_PLACEMENT_COMPLETE
STAGING_CLEANUP_COMPLETE
REMOTE_READBACK_PASS
REMOTE_PUBLICATION_COMPLETE
MAIN_CHAT_ACCEPTANCE
```

```text
OWNER UPLOAD COMPLETE
!= FINAL PLACEMENT COMPLETE
!= REMOTE ACCEPTANCE
```

## 15. No ordinary-chat fallback by quality reduction

If a Work-triggered unit cannot be executed in Work, Main Chat must not silently replace it with a sample/first-N/manual summary.

Record `WORK_EXECUTION_REQUIRED / BLOCKED` or split only into deterministic complete units explicitly permitted by the step contract.

## 16. Markers

```text
KW002_WORK_HANDOFF_RULE_ACTIVE = true
KW002_MAIN_CHAT_WRITES_AND_RELEASES_WORK_PROMPT = true
KW002_OWNER_RELAYS_PROMPT = true
KW002_WORK_EXECUTES_RELEASED_CONTRACT = true
KW002_MAIN_CHAT_GOVERNANCE_MUST_NOT_BE_DUPLICATED_IN_WORK = true
KW002_WORK_FULL_LEVEL1_REREAD_FORBIDDEN_BY_DEFAULT = true
KW002_WORK_FRESH_EXTERNAL_RESEARCH_REDO_FORBIDDEN_BY_DEFAULT = true
KW002_WORK_OWNER_FACING_REPORT_GATE_FORBIDDEN_BY_DEFAULT = true
KW002_WORK_RELEASE_REAUTHORIZATION_FORBIDDEN_BY_DEFAULT = true
KW002_WORK_NARROW_REMOTE_AND_INPUT_DRIFT_PREFLIGHT_ALLOWED = true
KW002_LARGE_DATA_MUST_NOT_BE_SAMPLED_FOR_CONTEXT_CONVENIENCE = true
KW002_OWNER_RELAY_SINGLE_STAGING_REQUIRED = true
KW002_OWNER_MUST_NOT_ROUTE_FINAL_PATHS = true
KW002_FINAL_PATH_MANIFEST_REQUIRED = true
KW002_WORK_DIRECT_LARGE_ARTIFACT_GITHUB_PUBLICATION_FORBIDDEN_BY_DEFAULT = true
KW002_MAIN_CHAT_FINAL_PLACEMENT_AND_REMOTE_ACCEPTANCE_REQUIRED = true
KW002_LARGE_ARTIFACT_MODEL_TRANSPORT_FORBIDDEN_BY_DEFAULT = true
KW002_TRANSPORT_ZIP_REQUIRED_WHEN_MULTIPLE_FILES = true
KW002_ONE_PRIMARY_UPLOAD_LINK_PER_HANDOFF = true
```
