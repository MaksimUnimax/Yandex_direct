# KW-002 — LEVEL 1 CHATGPT WORK HANDOFF RULE

Status: **ACTIVE / OWNER-LOCKED**  
Owner instruction: 2026-09-08  
Owner transport amendment: 2026-09-11

Cross-Kwork artifact-publication authority:

`../../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md`

## 1. Purpose

Large-data work must not be degraded merely to fit an ordinary chat context.

```text
LARGE DATA
!= SAMPLE IT
!= TRUNCATE IT
!= SUMMARIZE BEFORE ANALYSIS

LARGE DATA
→ HAND OFF THE COMPLETE EXECUTION UNIT TO CHATGPT WORK
```

Work must also avoid wasting model context/tokens on byte transport after the analytical work is already complete.

```text
LARGE ARTIFACT COMPLETE
!= SEND ITS FULL BYTES THROUGH THE MODEL
```

## 2. Trigger

Use ChatGPT Work when one or more are true:

```text
- complete analysis of a large table or several large files is required;
- row-level joins/deduplication/reconciliation cannot be verified reliably in ordinary chat;
- full provider evidence would otherwise be sampled or omitted;
- pairwise/cluster analysis creates a large intermediate universe;
- a final workbook/report must be generated from large structured inputs;
- ordinary-context limits materially risk skipped rows, lost provenance, partial QA or repeated reconstruction.
```

This is a quality trigger, not an arbitrary row-count threshold.

## 3. Canonical Work prompt authority

The MAIN CHATGPT WORKFLOW prepares the exact Work prompt for the current step. The owner/user only relays that prompt to ChatGPT Work.

```text
MAIN CHATGPT = PROMPT AUTHOR
OWNER / USER = PROMPT RELAY
CHATGPT WORK = EXECUTION ENVIRONMENT
```

Mandatory sequence:

```text
CURRENT STEP PRE-STEP REVIEW
→ WORK TRIGGER CONFIRMED
→ PRE-HANDOFF MANIFEST FROZEN
→ MAIN CHATGPT WRITES COMPLETE CANONICAL WORK PROMPT
→ OWNER RELAYS PROMPT TO WORK WITHOUT NEEDING TO DESIGN IT
→ WORK EXECUTES
→ WORK MATERIALIZES + QA'S ARTIFACTS
→ APPROVED PUBLICATION ROUTE
→ OWNER RETURNS WORK RESULT/ARTIFACTS OR UPLOAD CONFIRMATION
→ MAIN CHATGPT RUNS RETURN QA
```

The owner is not responsible for inventing, completing or correcting the Work prompt.

Main ChatGPT must include all current step/job constraints in the prompt and must not ask the owner to supply a methodology prompt that the project already knows how to construct.

If the owner edits the prompt intentionally, the latest explicit owner instruction has authority. Otherwise the generated prompt is the canonical handoff contract for that execution.

## 4. Required pre-handoff manifest

Before writing the Work prompt, freeze:

```text
JOB_ID
STEP_ID
WHY_WORK_REQUIRED
ALLOWED_INPUT_FILES / SOURCES
PROHIBITED_INPUT_FILES / SOURCES
CURRENT AUTHORITATIVE UPSTREAM ARTIFACTS
EXACT EXECUTION GOAL
REQUIRED OUTPUT FILES / TABLES
MANDATORY FIELDS
ROW / COUNT / JOIN EXPECTATIONS where known
CLAIM BOUNDARIES
QA / ACCEPTANCE CHECKS
STOP CONDITIONS
ARTIFACT_PUBLICATION_POLICY
```

For clean tests, the source whitelist is mandatory.

For any Work execution expected to produce material files, include:

```text
ARTIFACT_PUBLICATION_POLICY = NATIVE_GIT_IF_ALREADY_AUTHENTICATED | OWNER_RELAY_IF_MORE_EFFICIENT
LARGE_ARTIFACT_MODEL_TRANSPORT = FORBIDDEN_BY_DEFAULT
OWNER_RELAY_ALLOWED = true
REMOTE_READBACK_REQUIRED = true
```

## 5. Work is execution environment, not authority

```text
WORK OUTPUT != AUTOMATICALLY ACCEPTED TRUTH
```

Work must obey the same Level 1 and Level 2 rules as ordinary execution and may not:

- create new permanent methodology;
- override client scope;
- silently drop rows;
- replace missing evidence with assumptions;
- change evidence classes;
- treat partial processing as complete;
- use prohibited prior-research sources;
- silently make provider calls outside the authorized step.

## 6. Post-Work return gate

After Work finishes:

```text
1. receive produced artifacts/results;
2. verify source manifest;
3. verify row/count/join truth;
4. verify required fields and provenance;
5. inspect HOLD/ERROR/UNRESOLVED rows;
6. compare output to Level 2 acceptance contract;
7. persist accepted artifacts in work/<JOB_ID>/ using an approved publication route;
8. read back from GitHub/storage;
9. verify remote identity/mechanical QA;
10. only then mark the step complete and continue.
```

## 6A. Large-artifact publication route — mandatory decision

Canonical cross-Kwork rule:

`../../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md`

Work must separate **generation/analysis** from **artifact transport**.

Preferred decision:

```text
IF NORMAL AUTHENTICATED GIT PUSH ALREADY WORKS RELIABLY
→ USE NORMAL GIT
→ REMOTE READBACK

ELSE IF OWNER RELAY IS CHEAPER / FASTER / SAFER
→ STOP DEBUGGING GIT AUTH
→ LOCAL ARTIFACT FREEZE + LOCAL QA
→ GIVE OWNER DOWNLOADABLE FILES INDIVIDUALLY AND/OR TRANSPORT ZIP
→ GIVE OWNER DIRECT GITHUB UPLOAD PAGE FOR EXACT REPO / BRANCH / DIRECTORY
→ OWNER UPLOADS THROUGH NORMAL AUTHENTICATED GITHUB WEB UI
→ OWNER CONFIRMS
→ WORK / MAIN CHATGPT PERFORMS REMOTE READBACK + IDENTITY QA
```

Owner relay is an approved normal transport mechanism. It is not a fallback by quality reduction.

This applies to large TSV/CSV/JSON, XLSX, DOCX, PDF, ZIP, images, evidence packs, reports and other material artifacts.

## 6B. Do not transport large file bytes through the model

Forbidden by default when the file already exists locally:

```text
PRINT ENTIRE LARGE FILE INTO CHAT
BASE64 THE FILE INTO MODEL OUTPUT
SPLIT IT INTO MANY TEXT CHUNKS FOR CONNECTOR WRITES
RECONSTRUCT THE FILE THROUGH GIANT TOOL ARGUMENTS
REGENERATE A VALID ARTIFACT ONLY BECAUSE GIT AUTH FAILED
```

Bounded reads, shell counts, hashes, row checks and small excerpts remain allowed for QA.

The prohibition is on using the model/tool text channel as the byte-transfer mechanism.

## 6C. Owner handoff requirements

When owner relay is selected, Work must make the transfer simple:

```text
- provide exact files for download;
- provide a ZIP too when multiple files make download easier;
- state clearly whether ZIP is transport-only and must be extracted;
- provide a direct GitHub Upload files link to the intended repo/branch/folder when possible;
- state target branch and directory in text;
- provide commit message when useful;
- tell owner the minimal completion signal to return, e.g. "готово".
```

Do not require the owner to reconstruct filenames or directory structure manually.

Do not ask the owner to paste GitHub password, PAT, 2FA code or private key into chat.

## 6D. Publication state and checkpoint truth

Keep separate:

```text
LOCAL_ARTIFACT_COMPLETE
LOCAL_QA_PASS
PUBLICATION_HANDOFF_READY
OWNER_UPLOAD_COMPLETE
REMOTE_READBACK_PASS
REMOTE_PUBLICATION_COMPLETE
```

A Git-auth/network failure after local QA does **not** invalidate the local analytical result.

```text
GIT AUTH FAILURE
!= RECOMPUTE DATA
!= ANALYTICAL FAIL
```

Likewise:

```text
OWNER UPLOADED FILES
!= PUBLICATION ACCEPTED
```

Remote readback/identity QA is always required.

For long Work jobs, owner relay may be used at intermediate semantic checkpoints so large completed blocks become remote-recoverable without spending hours debugging Git authentication.

## 7. No ordinary-chat fallback by quality reduction

If a Work-triggered step cannot be run in Work, do not silently switch to representative samples, first-N rows, manual examples or summary-only processing.

Record `WORK_EXECUTION_REQUIRED / BLOCKED`, or split into complete independently valid units only when the Level 2 method explicitly permits it without loss of global coherence.

Owner-relay publication is **not** such a quality reduction because the artifact itself remains exact; only the transport actor changes.

## 8. Relation to Bridge

```text
BRIDGE = PROVIDER EVIDENCE ACQUISITION / PERSISTENCE
WORK = LARGE-DATA ANALYSIS / TRANSFORMATION / ARTIFACT EXECUTION
MAIN CHATGPT = METHOD CONTROL / WORK PROMPT AUTHOR / DECISIONS / RETURN QA / OWNER COMMUNICATION
OWNER = AUTHORIZATION / PROMPT RELAY / OPTIONAL LARGE-ARTIFACT FILE RELAY / COMMERCIAL SCOPE AUTHORITY
```

The owner may relay file bytes without becoming responsible for analysis, methodology, QA design or artifact construction.

## 9. Markers

```text
KW002_WORK_HANDOFF_RULE_ACTIVE = true
KW002_MAIN_CHATGPT_WRITES_WORK_PROMPT = true
KW002_OWNER_RELAYS_WORK_PROMPT = true
KW002_OWNER_DOES_NOT_HAVE_TO_DESIGN_WORK_PROMPT = true
KW002_LARGE_DATA_MUST_NOT_BE_SAMPLED_FOR_CONTEXT_CONVENIENCE = true
KW002_WORK_OUTPUT_REQUIRES_RETURN_QA = true
KW002_WORK_PROMPT_MUST_FREEZE_ARTIFACT_PUBLICATION_POLICY = true
KW002_OWNER_RELAY_PUBLICATION_APPROVED = true
KW002_OWNER_RELAY_MAY_BE_USED_FOR_CHECKPOINTS = true
KW002_LARGE_ARTIFACT_MODEL_TRANSPORT_FORBIDDEN_BY_DEFAULT = true
KW002_DIRECT_UPLOAD_LINK_PREFERRED_FOR_OWNER_RELAY = true
KW002_REMOTE_READBACK_AFTER_OWNER_UPLOAD_REQUIRED = true
KW002_GIT_AUTH_FAILURE_DOES_NOT_REQUIRE_RECOMPUTE = true
```
