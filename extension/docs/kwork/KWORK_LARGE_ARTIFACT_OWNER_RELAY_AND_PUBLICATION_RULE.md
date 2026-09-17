# KWORK — LARGE ARTIFACT OWNER-RELAY AND PUBLICATION RULE

Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**  
Applies to: **KW-001, KW-002, all current/future mini-kworks, and any Work execution under this Kwork ecosystem**  
Owner decision: **2026-09-11**  
Owner single-staging amendment: **2026-09-17**

## 1. Purpose

Large or numerous artifacts produced by ChatGPT Work must not consume excessive time/tokens on byte transport or force the owner to sort files into repository directories.

Core distinction:

```text
ANALYTICAL / GENERATION WORK
!=
ARTIFACT TRANSPORT
!=
FINAL REPOSITORY PLACEMENT
!=
REMOTE ACCEPTANCE
```

A completed local artifact must not be recomputed merely because publication transport failed.

The owner is a **single-hop byte relay only**. The owner is NOT responsible for repository path routing, artifact placement, methodology, file reconstruction, or post-upload QA.

## 2. Universal large-artifact transport rule

For Work executions that produce large/material artifacts:

```text
WORK COMPLETES ANALYSIS / GENERATION
→ LOCAL ARTIFACT FREEZE
→ LOCAL QA
→ WORK PROVIDES DOWNLOADABLE FILES + ONE TRANSPORT ZIP
→ WORK PROVIDES ONE SINGLE OWNER-RELAY STAGING UPLOAD TARGET
→ OWNER DOWNLOADS / EXTRACTS
→ OWNER UPLOADS ALL HANDOFF FILES TO THAT ONE STAGING TARGET
→ OWNER RETURNS MINIMAL CONFIRMATION, E.G. "ГОТОВО"
→ MAIN CHATGPT / WORK READS STAGING PAYLOAD
→ MAIN CHATGPT / WORK PLACES / REPLACES / MOVES EACH FILE AT ITS CANONICAL FINAL REPOSITORY PATH
→ MAIN CHATGPT / WORK DELETES TEMPORARY STAGING COPIES THAT DO NOT BELONG THERE
→ REMOTE READBACK + IDENTITY QA
→ ONLY THEN REMOTE PUBLICATION IS ACCEPTED
```

For large artifacts, the owner MUST NOT be asked to split one handoff across several GitHub directories.

```text
ONE HANDOFF UNIT
→ ONE OWNER UPLOAD TARGET
```

## 3. Trigger

Use this owner-relay route whenever one or more are true:

```text
- one or more artifacts are large enough that moving their full contents through model/tool text is wasteful;
- files are binary or token-expensive: XLSX, PDF, DOCX, ZIP, large CSV/TSV/JSON, images, archives, reports;
- connector publication would require embedding, chunking, base64, or rereading full artifact bytes through the model;
- several output files belong to different canonical repository directories;
- owner can upload the complete handoff bundle quickly through normal authenticated GitHub Web UI;
- remote publication/placement is the remaining step after local QA.
```

This is a transport-efficiency / quality trigger, not a fixed file-size threshold.

## 4. Single staging target — mandatory

Every material Work handoff must freeze exactly one staging upload target before owner relay.

Required manifest fields:

```text
OWNER_RELAY_STAGING_REPOSITORY
OWNER_RELAY_STAGING_BRANCH
OWNER_RELAY_STAGING_DIRECTORY
OWNER_RELAY_UPLOAD_URL
```

Default selection:

```text
OWNER_RELAY_STAGING_DIRECTORY = current job root
```

unless the execution contract explicitly defines a dedicated handoff/inbox directory.

The owner uploads the whole handoff set to this one directory.

The owner does NOT:

```text
- decide which file belongs in LEVEL1 / LEVEL2 / job root / reports / evidence;
- perform NEW vs REPLACE routing;
- move files between repository directories;
- delete staging duplicates;
- reconstruct nested directory structure manually;
- split one handoff into several upload actions merely because final canonical paths differ.
```

Those are executor responsibilities.

## 5. Final-path manifest — mandatory

Before handoff, Work must freeze a machine-readable or clearly structured final-path manifest for every file:

```text
HANDOFF_FILENAME
FINAL_REPOSITORY_PATH
ACTION = NEW | REPLACE
ARTIFACT_ROLE
EXPECTED_HASH / IDENTITY MARKER where available
STAGING_CLEANUP_REQUIRED = true | false
```

If two artifacts would collide by filename in the single staging directory, Work must assign unique transport filenames and record the canonical final filename/path in the manifest.

The owner must never be asked to solve filename collisions manually.

## 6. Owner-relay workflow

The executor must:

```text
1. finish the analytical/generation block locally;
2. run local QA;
3. freeze the exact handoff artifact set;
4. freeze final-path manifest;
5. freeze ONE staging repository/branch/directory;
6. provide downloadable files individually;
7. provide ONE transport ZIP when multiple files exist;
8. state that ZIP is transport-only unless the repository explicitly requires it;
9. provide ONE direct GitHub Upload files link for the staging directory;
10. tell owner to upload ALL extracted handoff files there together;
11. owner returns only a minimal signal, e.g. "готово";
12. Main ChatGPT / Work reads the actual staging payload from the current remote branch;
13. verify filenames/counts/hashes against the frozen handoff manifest;
14. create/update every canonical final repository path;
15. delete staging-only copies after successful canonical placement;
16. read back every final path;
17. run identity/mechanical QA;
18. verify unrelated concurrent changes were not damaged;
19. only then declare remote publication complete.
```

## 7. Large file bytes must not be transported through the model

Forbidden by default:

```text
PRINT ENTIRE LARGE FILE INTO CHAT
READ ENTIRE LARGE FILE SOLELY TO REUPLOAD IT
BASE64 FILE INTO MODEL OUTPUT
SPLIT FILE INTO MANY TEXT CHUNKS FOR CONNECTOR WRITES
RECONSTRUCT LARGE FILE IN A CONNECTOR ARGUMENT
REGENERATE A VALID FILE ONLY BECAUSE TRANSPORT FAILED
```

Bounded reads, hashes, counts, headers and small excerpts remain allowed for QA.

## 8. Transport ZIP rule

When multiple artifacts belong to one publication unit:

```text
PROVIDE INDIVIDUAL FILES
AND
PROVIDE ONE TRANSPORT ZIP
```

Default:

```text
ZIP = TRANSPORT CONTAINER ONLY
DO NOT COMMIT ZIP UNLESS THE EXECUTION CONTRACT EXPLICITLY REQUIRES IT
EXTRACT ZIP LOCALLY
UPLOAD ALL INCLUDED HANDOFF FILES TO THE ONE STAGING TARGET
```

The ZIP should contain the frozen final handoff set and preserve enough manifest information for canonical redistribution.

## 9. Direct upload-link rule

For owner relay, provide exactly one primary operational upload link per handoff unit:

```text
repository
+ branch
+ single staging directory
+ GitHub upload-files screen
```

Do not give the owner several directory-specific upload links as the required workflow.

Additional final-path links may be reported for audit/reference only; they are not owner upload instructions.

## 10. Executor placement responsibility

After the owner says `готово`, Main ChatGPT / Work owns final placement.

For every handoff file:

```text
STAGING FILE
→ VERIFY IDENTITY
→ LOOK UP FINAL PATH IN MANIFEST
→ NEW: CREATE CANONICAL FILE
   OR
→ REPLACE: FETCH CURRENT TARGET + REPLACE SAFELY
→ READ BACK FINAL TARGET
→ VERIFY IDENTITY / CONTENT / QA
→ REMOVE STAGING-ONLY COPY IF FINAL PATH != STAGING PATH
```

No force-push.

Do not overwrite unrelated files.

If target authority has drifted since the handoff manifest was frozen, stop that conflicting placement, preserve the staging artifact, and report the precise conflict rather than silently overwriting newer authority.

## 11. Security boundary

Owner relay must never require credentials in chat.

Forbidden:

```text
ASK OWNER FOR GITHUB PASSWORD
ASK OWNER FOR PAT/TOKEN IN CHAT
ASK OWNER FOR 2FA CODE IN CHAT
EMBED PRIVATE SSH KEY IN REPOSITORY
```

Authentication occurs in the owner's normal GitHub browser/session or another owner-controlled secure channel.

## 12. Concurrency / shared-branch safety

Before handoff, record current branch authority where material.

After owner upload, always fetch the CURRENT remote state.

Verify:

```text
- expected staging files exist;
- upload did not remove unrelated work;
- canonical targets are still safe to create/replace;
- final files exist at intended paths after redistribution;
- final content matches the frozen handoff artifacts;
- staging-only duplicates are removed after successful placement;
- row/file/count QA still passes.
```

If the branch moved during relay, do not assume success from the old HEAD.

## 13. Identity verification

Use the strongest practical checks:

```text
Git blob SHA
cryptographic checksum
byte size
row count / sheet count / page count
required field/header checks
known mechanical QA markers
```

```text
OWNER UPLOAD COMPLETE
!=
FINAL REPOSITORY PLACEMENT COMPLETE
!=
REMOTE ACCEPTANCE COMPLETE
```

Required:

```text
OWNER UPLOAD TO SINGLE STAGING TARGET
→ EXECUTOR REDISTRIBUTION
→ FINAL-PATH REMOTE READBACK
→ IDENTITY / QA VERIFICATION
→ ACCEPT
```

## 14. State separation

Always distinguish:

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

Owner upload proves only that the staging transfer occurred.

## 15. Failure / blocked conditions

PASS requires:

```text
LOCAL_ARTIFACT_SET_FROZEN = true
LOCAL_QA = PASS
FINAL_PATH_MANIFEST_FROZEN = true
ONE_OWNER_STAGING_TARGET = true
OWNER_RECEIVED_FILES = true
OWNER_UPLOAD_COMPLETE = true
STAGING_PAYLOAD_IDENTITY = PASS
FINAL_PLACEMENT_COMPLETE = true
STAGING_CLEANUP_COMPLETE = true where required
REMOTE_FINAL_FILES_PRESENT = true
REMOTE_IDENTITY_MATCH = PASS
REMOTE_QA = PASS where applicable
UNRELATED_REMOTE_CHANGES_DAMAGED = false
```

FAIL / BLOCKED if:

```text
owner received only a prose summary instead of required files
owner was required to split files among multiple final directories
owner was required to decide repository placement
large artifact was silently truncated/reconstructed through model text
staging identity cannot be verified
canonical final path conflicts with newer authority
remote final identity cannot be verified
executor claims publication merely because staging upload occurred
```

## 16. Work-prompt requirement

Every Work prompt that may produce material files must include:

```text
ARTIFACT_PUBLICATION_POLICY = OWNER_RELAY_SINGLE_STAGING_REQUIRED
LARGE_ARTIFACT_MODEL_TRANSPORT = FORBIDDEN_BY_DEFAULT
OWNER_RELAY_ALLOWED = true
OWNER_RELAY_SINGLE_STAGING_REQUIRED = true
OWNER_MUST_NOT_ROUTE_FILES_TO_FINAL_PATHS = true
EXECUTOR_FINAL_PLACEMENT_REQUIRED = true
REMOTE_READBACK_REQUIRED = true
```

It must also freeze:

```text
OWNER_RELAY_STAGING_REPOSITORY
OWNER_RELAY_STAGING_BRANCH
OWNER_RELAY_STAGING_DIRECTORY
OWNER_RELAY_UPLOAD_URL
FINAL_PATH_MANIFEST
```

## 17. Plain-language owner handoff

The owner-facing operational instruction must be short:

```text
1. Download the files/ZIP.
2. Extract the ZIP if needed.
3. Upload ALL handoff files together to THIS ONE GitHub upload link.
4. Commit the upload.
5. Reply: "готово".
```

Do NOT tell the owner to sort files into repository directories.

Do NOT bury this instruction under a technical report.

## 18. Relation of roles

```text
WORK
= LARGE-DATA ANALYSIS / TRANSFORMATION / ARTIFACT MATERIALIZATION / LOCAL QA

OWNER
= DOWNLOAD + SINGLE-STAGING UPLOAD ONLY

MAIN CHATGPT / WORK AFTER OWNER UPLOAD
= STAGING VERIFICATION + CANONICAL FINAL PLACEMENT + CLEANUP + REMOTE QA
```

The owner is not responsible for analysis, methodology, artifact construction, path routing, or final acceptance.

## 19. Permanent markers

```text
KWORK_OWNER_RELAY_PUBLICATION_RULE_ACTIVE = true
KWORK_OWNER_RELAY_APPLIES_TO_KW001 = true
KWORK_OWNER_RELAY_APPLIES_TO_KW002 = true
KWORK_OWNER_RELAY_APPLIES_TO_MINI_KWORKS = true
KWORK_LARGE_ARTIFACT_MODEL_BYTE_TRANSPORT_FORBIDDEN_BY_DEFAULT = true
KWORK_OWNER_RELAY_IS_APPROVED_NORMAL_TRANSPORT = true
KWORK_OWNER_RELAY_SINGLE_STAGING_REQUIRED = true
KWORK_OWNER_MUST_NOT_ROUTE_FINAL_PATHS = true
KWORK_EXECUTOR_FINAL_PLACEMENT_REQUIRED = true
KWORK_FINAL_PATH_MANIFEST_REQUIRED = true
KWORK_ONE_PRIMARY_UPLOAD_LINK_PER_HANDOFF = true
KWORK_DOWNLOADABLE_ARTIFACT_HANDOFF_REQUIRED = true
KWORK_TRANSPORT_ZIP_REQUIRED_FOR_MULTI_FILE_HANDOFF = true
KWORK_STAGING_CLEANUP_REQUIRED = true
KWORK_REMOTE_READBACK_AFTER_FINAL_PLACEMENT_REQUIRED = true
KWORK_OWNER_UPLOAD_IS_NOT_REMOTE_ACCEPTANCE = true
KWORK_TRANSPORT_FAILURE_DOES_NOT_REQUIRE_RECOMPUTE = true
```
