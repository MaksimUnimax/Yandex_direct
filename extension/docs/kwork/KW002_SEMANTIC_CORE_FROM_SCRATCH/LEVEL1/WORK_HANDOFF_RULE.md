# KW-002 — LEVEL 1 CHATGPT WORK HANDOFF RULE

Status: **ACTIVE / OWNER-LOCKED**  
Owner instruction: 2026-09-08  
Owner transport amendment: 2026-09-11  
Owner large-artifact relay lock: 2026-09-17  
Owner single-staging placement lock: 2026-09-17

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

Large artifact transport is a separate problem:

```text
LARGE ARTIFACT COMPLETE
!= SEND ITS FULL BYTES THROUGH THE MODEL
```

The owner/user is not responsible for sorting handoff files across repository directories.

```text
OWNER = SINGLE-STAGING BYTE RELAY
MAIN CHATGPT / WORK = FINAL REPOSITORY PLACEMENT + QA
```

## 2. Work trigger

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
→ WORK HANDS OWNER DOWNLOADABLE FILES + ONE TRANSPORT ZIP
→ OWNER UPLOADS ALL HANDOFF FILES TO ONE SINGLE STAGING TARGET
→ OWNER RETURNS MINIMAL CONFIRMATION, E.G. "ГОТОВО"
→ MAIN CHATGPT / WORK VERIFIES STAGING PAYLOAD
→ MAIN CHATGPT / WORK PLACES / REPLACES FILES AT ALL CANONICAL FINAL PATHS
→ MAIN CHATGPT / WORK REMOVES STAGING-ONLY COPIES
→ FINAL-PATH REMOTE READBACK + RETURN QA
→ ONLY THEN STEP MAY BE ACCEPTED
```

The owner is not responsible for inventing, completing or correcting the Work prompt.

The owner is also not responsible for repository path routing.

## 4. Required pre-handoff manifest

Before writing the Work prompt, freeze:

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

For any Work execution expected to produce material files, also freeze:

```text
ARTIFACT_PUBLICATION_POLICY = OWNER_RELAY_SINGLE_STAGING_REQUIRED
LARGE_ARTIFACT_MODEL_TRANSPORT = FORBIDDEN_BY_DEFAULT
OWNER_RELAY_ALLOWED = true
OWNER_RELAY_SINGLE_STAGING_REQUIRED = true
OWNER_MUST_NOT_ROUTE_FILES_TO_FINAL_PATHS = true
WORK_DIRECT_LARGE_ARTIFACT_GITHUB_PUBLICATION = FORBIDDEN_BY_DEFAULT
EXECUTOR_FINAL_PLACEMENT_REQUIRED = true
REMOTE_READBACK_REQUIRED = true

OWNER_RELAY_STAGING_REPOSITORY
OWNER_RELAY_STAGING_BRANCH
OWNER_RELAY_STAGING_DIRECTORY
OWNER_RELAY_UPLOAD_URL
FINAL_PATH_MANIFEST
```

For clean tests, the source whitelist is mandatory.

## 5. Final-path manifest — mandatory

Every handoff file must have a frozen mapping:

```text
HANDOFF_FILENAME
FINAL_REPOSITORY_PATH
ACTION = NEW | REPLACE
ARTIFACT_ROLE
EXPECTED_HASH / IDENTITY MARKER where available
STAGING_CLEANUP_REQUIRED = true | false
```

If final files belong to different repository directories, this does NOT create multiple owner upload actions.

```text
MANY FINAL PATHS
!= MANY OWNER UPLOAD TARGETS

ONE HANDOFF UNIT
→ ONE OWNER UPLOAD TARGET
```

If transport filenames would collide in the single staging directory, Work must create unique transport filenames and map them back to canonical final names/paths in the manifest.

The owner never resolves collisions manually.

## 6. Work is execution environment, not authority

```text
WORK OUTPUT != AUTOMATICALLY ACCEPTED TRUTH
```

Work must obey the same Level 1 and Level 2 rules as ordinary execution and may not:

- create new permanent methodology without authority;
- override client scope;
- silently drop rows;
- replace missing evidence with assumptions;
- change evidence classes;
- treat partial processing as complete;
- use prohibited prior-research sources;
- silently make provider calls outside the authorized step.

## 7. Large-artifact owner handoff — ONE staging target only

For material handoffs, Work must give the owner:

```text
- a direct downloadable link for every required final file;
- ONE transport ZIP when multiple files exist;
- the exact ZIP contents;
- one frozen final-path manifest;
- ONE primary GitHub Upload files link;
- one staging repository;
- one staging branch;
- one staging directory;
- one intended staging-upload commit message when useful;
- one minimal completion signal, e.g. "готово".
```

The owner-facing instruction must be operationally simple:

```text
1. download files/ZIP;
2. extract if needed;
3. upload ALL handoff files together to THIS ONE staging upload link;
4. commit;
5. reply "готово".
```

Do NOT tell the owner to split files between LEVEL1 / LEVEL2 / job root / reports / evidence or any other final directories.

Do NOT require the owner to perform NEW/REPLACE routing.

Do NOT require the owner to delete temporary copies.

## 8. Executor placement after owner upload

After the owner replies `готово`, Main ChatGPT / Work owns the final placement.

For every staging artifact:

```text
STAGING FILE
→ VERIFY AGAINST HANDOFF MANIFEST
→ RESOLVE FINAL PATH
→ IF ACTION = NEW: CREATE CANONICAL FINAL FILE
→ IF ACTION = REPLACE: FETCH CURRENT TARGET AND REPLACE SAFELY
→ READ BACK FINAL PATH
→ VERIFY IDENTITY / CONTENT / MECHANICAL QA
→ DELETE STAGING-ONLY COPY WHEN FINAL PATH != STAGING PATH
```

No force-push.

Do not overwrite unrelated concurrent work.

If the final target changed after the manifest was frozen and a safe replacement cannot be proved, keep the staging copy, report the exact authority drift/conflict, and do not silently overwrite newer work.

## 9. Post-Work return gate

After Work finishes and owner upload occurs:

```text
1. fetch current remote branch state;
2. verify expected staging payload exists;
3. verify source manifest;
4. verify row/count/join truth;
5. verify required fields and provenance;
6. inspect HOLD/ERROR/UNRESOLVED rows;
7. compare output to Level 2 acceptance contract;
8. redistribute staging files to all canonical final paths according to FINAL_PATH_MANIFEST;
9. remove staging-only copies after successful placement;
10. read back every final path;
11. verify remote identity/mechanical QA;
12. verify unrelated remote changes were not damaged;
13. only then mark the step complete and continue.
```

## 10. Do not transport large file bytes through the model

Forbidden by default:

```text
PRINT ENTIRE LARGE FILE INTO CHAT
BASE64 THE FILE INTO MODEL OUTPUT
SPLIT IT INTO MANY TEXT CHUNKS FOR CONNECTOR WRITES
RECONSTRUCT THE FILE THROUGH GIANT TOOL ARGUMENTS
REGENERATE A VALID ARTIFACT ONLY BECAUSE TRANSPORT FAILED
```

Bounded reads, shell counts, hashes, row checks and small excerpts remain allowed for QA.

## 11. Publication-state truth

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
```

```text
OWNER UPLOAD COMPLETE
!= FINAL PLACEMENT COMPLETE
!= REMOTE PUBLICATION ACCEPTED
```

Remote readback after final placement is mandatory.

## 12. No ordinary-chat fallback by quality reduction

If a Work-triggered step cannot be run in Work, do not silently switch to representative samples, first-N rows, manual examples or summary-only processing.

Record:

```text
WORK_EXECUTION_REQUIRED / BLOCKED
```

or split into complete independently valid units only when the Level 2 method explicitly permits it without loss of global coherence.

## 13. Relation to Bridge / Work / Main Chat / Owner

```text
BRIDGE
= PROVIDER EVIDENCE ACQUISITION / PERSISTENCE

WORK
= LARGE-DATA ANALYSIS / TRANSFORMATION / ARTIFACT EXECUTION / LOCAL QA

MAIN CHATGPT
= METHOD CONTROL / WORK PROMPT AUTHOR / DECISIONS / RETURN QA / FINAL REPOSITORY PLACEMENT CONTROL

OWNER
= AUTHORIZATION / PROMPT RELAY / DOWNLOAD + SINGLE-STAGING FILE UPLOAD / COMMERCIAL SCOPE AUTHORITY
```

The owner relays bytes without becoming responsible for analysis, methodology, QA design, artifact construction, repository routing or final acceptance.

## 14. Security

Do not ask the owner to paste GitHub password, PAT, 2FA code or private key into chat.

Authentication happens in the owner's normal authenticated GitHub session.

## 15. Markers

```text
KW002_WORK_HANDOFF_RULE_ACTIVE = true
KW002_MAIN_CHATGPT_WRITES_WORK_PROMPT = true
KW002_OWNER_RELAYS_WORK_PROMPT = true
KW002_OWNER_DOES_NOT_HAVE_TO_DESIGN_WORK_PROMPT = true
KW002_LARGE_DATA_MUST_NOT_BE_SAMPLED_FOR_CONTEXT_CONVENIENCE = true
KW002_WORK_OUTPUT_REQUIRES_RETURN_QA = true
KW002_WORK_PROMPT_MUST_FREEZE_ARTIFACT_PUBLICATION_POLICY = true
KW002_OWNER_RELAY_PUBLICATION_APPROVED = true
KW002_OWNER_RELAY_REQUIRED_FOR_LARGE_ARTIFACTS = true
KW002_OWNER_RELAY_SINGLE_STAGING_REQUIRED = true
KW002_OWNER_MUST_NOT_ROUTE_FINAL_PATHS = true
KW002_EXECUTOR_FINAL_PLACEMENT_REQUIRED = true
KW002_FINAL_PATH_MANIFEST_REQUIRED = true
KW002_WORK_DIRECT_LARGE_ARTIFACT_GITHUB_PUBLICATION_FORBIDDEN_BY_DEFAULT = true
KW002_LARGE_ARTIFACT_MODEL_TRANSPORT_FORBIDDEN_BY_DEFAULT = true
KW002_DIRECT_DOWNLOAD_LINK_REQUIRED_FOR_LARGE_ARTIFACTS = true
KW002_TRANSPORT_ZIP_REQUIRED_WHEN_MULTIPLE_FILES = true
KW002_ONE_PRIMARY_UPLOAD_LINK_PER_HANDOFF = true
KW002_STAGING_CLEANUP_REQUIRED = true
KW002_REMOTE_READBACK_AFTER_FINAL_PLACEMENT_REQUIRED = true
KW002_OWNER_UPLOAD_IS_NOT_REMOTE_ACCEPTANCE = true
```
