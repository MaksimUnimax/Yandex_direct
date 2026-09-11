# KWORK — LARGE ARTIFACT OWNER-RELAY AND PUBLICATION RULE

Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**  
Applies to: **KW-001, KW-002, all current/future mini-kworks, and any Work execution under this Kwork ecosystem**  
Owner decision: **2026-09-11**

## 1. Purpose

Large or numerous artifacts produced by ChatGPT Work must not consume excessive time/tokens merely because Work cannot conveniently publish them through Git credentials or because the files are inefficient to transmit through model/tool text channels.

This rule creates a universal publication transport method in which the owner/user may act as a trusted manual relay between Work's local filesystem and the repository's normal web-upload surface.

Core distinction:

```text
ANALYTICAL / GENERATION WORK
!=
ARTIFACT TRANSPORT
!=
REMOTE ACCEPTANCE
```

A completed local artifact must not be recomputed merely because publication transport failed.

## 2. Universal non-repeat lesson

Failure class:

```text
LARGE ARTIFACT ALREADY COMPLETE
→ DIRECT GIT PUSH AUTH BLOCKED OR EXPENSIVE TO RECOVER
→ EXECUTOR TRIES TO MOVE FILE CONTENT THROUGH LLM / CONNECTOR / BASE64 / CHUNKS
→ LARGE TOKEN/TIME WASTE
→ RISK OF TRUNCATION / CORRUPTION / REPROCESSING
```

Root cause:

```text
publication transport was treated as if Work itself had to carry the bytes through the model/tool channel
```

Corrected principle:

```text
WORK MAY GENERATE + QA LOCALLY
OWNER MAY RELAY FILE BY NORMAL DOWNLOAD/UPLOAD
WORK/MAIN CHATGPT THEN VERIFIES REMOTE STATE
```

## 3. When this method applies

Use this method whenever one or more are true:

```text
- one or more artifacts are large enough that moving their full contents through model/tool text is wasteful;
- files are binary or token-expensive: XLSX, PDF, DOCX, ZIP, large CSV/TSV/JSON, images, archives, reports;
- Work has finished the file but Git HTTPS/SSH credentials are unavailable or unreliable;
- retrying Git authentication would consume more time than owner relay;
- connector upload would require embedding, chunking, base64, or rereading the full artifact through the model;
- a finished report/workbook/data authority needs durable repository publication and the owner can perform the final browser upload quickly;
- remote branch publication is the only remaining blocker after local QA.
```

This is a transport-efficiency trigger, not a fixed file-size threshold.

## 4. Preferred transport order

Choose the cheapest reliable transport that preserves exact bytes and repository truth.

```text
A. NATIVE AUTHENTICATED GIT PUSH
   only when already available, reliable and inexpensive

ELSE

B. OWNER-RELAY WEB PUBLICATION
   Work prepares/downloadable files
   + Work provides exact GitHub upload page
   + owner uploads through normal authenticated GitHub UI
   + Work/Main ChatGPT performs remote readback

NEVER BY DEFAULT

C. LLM / CONNECTOR CONTENT TRANSPORT OF LARGE FILE
   base64
   giant text paste
   repeated chunking
   full-file reconstruction through tool arguments
```

Method B is not a failure or emergency-only workaround. It is an approved normal publication route for large artifacts.

## 5. Owner-relay workflow

When owner relay is selected, the executor must:

```text
1. finish the analytical/generation block locally;
2. run local QA before handoff;
3. freeze the intended artifact set;
4. preserve exact filenames;
5. provide the owner with downloadable files individually and/or a transport ZIP;
6. provide a direct link to the exact repository / target branch / target directory upload page when possible;
7. tell the owner whether a ZIP is transport-only and must be extracted before repository upload;
8. provide the exact commit-message text when useful;
9. owner uploads the exact files through the authenticated GitHub web UI;
10. owner signals completion;
11. executor fetches/reads remote state;
12. compare remote paths/content identity against the locally frozen artifacts;
13. rerun required mechanical QA from remote where possible;
14. only then declare publication complete.
```

## 6. Work must not push large file contents through the model

For a large already-generated artifact, forbidden by default:

```text
PRINT ENTIRE FILE INTO CHAT
READ ENTIRE FILE SOLELY TO REUPLOAD IT
BASE64 FILE INTO MODEL OUTPUT
SPLIT FILE INTO MANY TEXT CHUNKS FOR CONNECTOR WRITES
RECONSTRUCT LARGE FILE IN A CONNECTOR ARGUMENT
REGENERATE A VALID FILE ONLY BECAUSE GIT AUTH FAILED
```

Model/tool inspection may still read bounded sections or run local mechanical commands when needed for QA. The prohibition is on using the model channel as the byte-transport mechanism.

## 7. Download package rule

Work should make the handoff easy for the owner.

When several artifacts belong to one publication unit:

```text
PROVIDE INDIVIDUAL FILES
AND, WHEN USEFUL,
PROVIDE ONE ZIP FOR CONVENIENT DOWNLOAD
```

If the repository expects individual files, clearly state:

```text
ZIP = TRANSPORT CONTAINER ONLY
DO NOT COMMIT ZIP
EXTRACT AND UPLOAD THE INCLUDED FILES
```

Do not force the owner to manually reconstruct filenames, directory structure or file contents.

## 8. Direct upload-link rule

Whenever GitHub web upload is used, provide a direct link targeting as closely as possible:

```text
repository
+ intended branch
+ intended directory
+ upload-files screen
```

The owner should not have to navigate the repository tree manually when a direct upload route can be prepared.

The handoff must explicitly state the intended target branch and directory in text as a cross-check.

## 9. Security boundary

Owner relay must not require the user to paste credentials into ChatGPT/Work.

Forbidden:

```text
ASK OWNER FOR GITHUB PASSWORD
ASK OWNER FOR PAT/TOKEN IN CHAT
ASK OWNER FOR 2FA CODE IN CHAT
EMBED PRIVATE SSH KEY IN REPOSITORY
```

Authentication happens in the owner's normal GitHub browser/session or another owner-controlled secure channel.

## 10. Concurrency / shared-branch safety

Owner relay does not waive shared-branch safety.

Before preparing the upload target, record/read the current remote branch state where material.

After owner upload:

```text
REMOTE READBACK IS MANDATORY
```

Verify that:

```text
- intended files exist at intended paths;
- unrelated concurrent changes were not removed;
- uploaded artifacts match the frozen local artifacts;
- the publication commit contains only the expected payload when that condition is required;
- row/file/count QA still passes.
```

If the shared branch moved during the relay, do not assume success from an old HEAD. Read the actual resulting remote commit/state.

## 11. Identity verification

Prefer exact identity checks available for the file type and environment:

```text
Git blob SHA
cryptographic checksum
byte size
row count / sheet count / page count
required field/header checks
known mechanical QA markers
```

The owner manually uploading a file does not itself prove successful publication.

```text
OWNER UPLOAD COMPLETE
!=
REMOTE ACCEPTANCE COMPLETE
```

Required:

```text
OWNER UPLOAD
→ REMOTE READBACK
→ IDENTITY / QA VERIFICATION
→ ACCEPT
```

## 12. State separation

Always distinguish:

```text
LOCAL_ARTIFACT_COMPLETE
LOCAL_QA_PASS
PUBLICATION_HANDOFF_READY
OWNER_UPLOAD_COMPLETE
REMOTE_READBACK_PASS
REMOTE_PUBLICATION_COMPLETE
```

A Git auth/network failure after local QA must not invalidate the completed analytical work.

Likewise, local completion is not remote publication completion.

## 13. Checkpoint use for long Work tasks

For long Work jobs, this method may be used at any meaningful recoverable checkpoint, not only at final delivery.

Example:

```text
large data authority complete
→ local QA
→ owner-relay publication
→ remote readback
→ continue next block
```

This reduces the risk that hours of Work remain only in scratch storage while avoiding excessive Git-auth/debug overhead.

## 14. Reports and client deliverables

This rule applies equally to:

```text
large TSV/CSV/JSON authorities
XLSX workbooks
DOCX/PDF reports
ZIP bundles
generated client deliverables
QA evidence packs
large source/evidence snapshots
other material artifacts
```

If a file is meant for the client rather than repository storage, owner relay may also be used simply to move the artifact out of Work without forcing it through model text.

## 15. Acceptance / failure conditions

PASS for an owner-relay publication requires:

```text
LOCAL_ARTIFACT_SET_FROZEN = true
LOCAL_QA = PASS
OWNER_RECEIVED_FILES = true
TARGET_REPO_BRANCH_PATH_EXPLICIT = true
REMOTE_FILES_PRESENT = true
REMOTE_IDENTITY_MATCH = PASS
REMOTE_QA = PASS where applicable
UNRELATED_REMOTE_CHANGES_DAMAGED = false
```

FAIL / BLOCKED if:

```text
owner received only a prose summary instead of required files
large artifact was silently truncated or reconstructed through model text
remote identity cannot be verified
wrong branch/path was used
manual upload overwrote unrelated work
executor claims publication merely because files were offered for download
```

## 16. Work-prompt requirement

Every Work prompt that may create material files must decide the artifact-publication route before execution or at the first material checkpoint.

At minimum include:

```text
ARTIFACT_PUBLICATION_POLICY = NATIVE_GIT_IF_ALREADY_AUTHENTICATED | OWNER_RELAY_IF_MORE_EFFICIENT
LARGE_ARTIFACT_MODEL_TRANSPORT = FORBIDDEN_BY_DEFAULT
OWNER_RELAY_ALLOWED = true
REMOTE_READBACK_REQUIRED = true
```

Do not make Work spend substantial execution time debugging Git authentication when the owner-relay route is clearly cheaper and safe.

## 17. Plain-language owner handoff

When relay is required, the executor should tell the owner only what is needed to perform the transfer:

```text
what files to download
where to upload them
what branch/folder to verify
whether to unzip first
what to click/commit
what short confirmation to send back
```

Do not bury this operational handoff under a long technical incident report.

## 18. Permanent markers

```text
KWORK_OWNER_RELAY_PUBLICATION_RULE_ACTIVE = true
KWORK_OWNER_RELAY_APPLIES_TO_KW001 = true
KWORK_OWNER_RELAY_APPLIES_TO_KW002 = true
KWORK_OWNER_RELAY_APPLIES_TO_MINI_KWORKS = true
KWORK_LARGE_ARTIFACT_MODEL_BYTE_TRANSPORT_FORBIDDEN_BY_DEFAULT = true
KWORK_OWNER_RELAY_IS_APPROVED_NORMAL_TRANSPORT = true
KWORK_DIRECT_UPLOAD_LINK_PREFERRED = true
KWORK_DOWNLOADABLE_ARTIFACT_HANDOFF_REQUIRED = true
KWORK_REMOTE_READBACK_AFTER_OWNER_UPLOAD_REQUIRED = true
KWORK_GIT_AUTH_FAILURE_DOES_NOT_REQUIRE_RECOMPUTE = true
```
