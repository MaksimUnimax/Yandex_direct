# KW-002 — WORK ARTIFACT HANDOFF AND OWNER PUBLICATION RULE

Status: **OWNER-MANDATED / ACTIVE / UNIVERSAL FOR DELEGATED WORK HANDOFFS**  
Decision date: 2026-09-16  
Scope clarification: 2026-09-17

## 1. Scope boundary

This rule applies to **delegated ChatGPT Work executions only**.

It does **not** make the owner a transport intermediary for Main ChatGPT's own repository edits.

```text
WORK = EXECUTION + QA + ZIP PACKAGING
OWNER = MANUAL TRANSPORT/PUBLICATION OF WORK OUTPUT
MAIN CHATGPT = ARCHITECTURE + ACCEPTANCE + ITS OWN REPOSITORY EDITS/PUBLICATION + REMOTE READBACK
```

Default Main rule:

```text
MAIN_CREATED_OR_EDITED_ARTIFACTS -> MAIN PUBLISHES THEM ITSELF
OWNER_TRANSPORT_FOR_MAIN -> FORBIDDEN BY DEFAULT
```

Main may ask the owner to transport Main-created files only when:

1. the owner explicitly asks for that workflow for the specific task; or
2. a real technical limitation prevents Main from publishing them directly, and Main states that limitation plainly.

A Work resource-saving rule must never be generalized into a universal owner-upload requirement for Main ChatGPT.

## 2. Default Work handoff contract

Unless the owner explicitly orders otherwise, Work that creates or changes multiple project files must:

1. complete the full bounded task;
2. run every required QA gate;
3. package all final deliverables into one `.zip`;
4. include only final task artifacts plus a manifest when useful;
5. provide a direct downloadable ZIP link;
6. list every file in the ZIP;
7. give the exact recommended repository path for every file;
8. identify NEW vs REPLACE files;
9. report QA, counts/checksums where applicable, limitations and out-of-scope work;
10. make **no GitHub commit/push/PR/publication** unless the owner explicitly orders Work to do so.

The owner manually publishes Work output. Main then performs independent readback/acceptance.

## 3. Work must not publish by default

```text
WORK_OUTPUT_READY
-> WORK_QA_PASS
-> ZIP_PACKAGE
-> OWNER_DOWNLOAD
-> OWNER_MANUAL_GITHUB_PUBLICATION
-> MAIN_REMOTE_READBACK / ACCEPTANCE
```

Work must not, by default:

- commit;
- push;
- force-push;
- create a PR;
- publish to GitHub;
- spend repeated calls uploading a multi-file package one file at a time.

## 4. Main ChatGPT publication rule

For Main ChatGPT's own edits, the opposite transport default applies:

```text
MAIN_EDIT -> MAIN_PUBLISH -> MAIN_READBACK
```

Before modifying an already-published artifact, Main must first inventory the remote state and distinguish:

- existing file requiring an in-place content replacement;
- genuinely new file;
- unchanged file that must not be redundantly republished.

Main must not reconstruct/re-upload already-published Work artifacts merely because downstream analysis references them.

## 5. Owner role is transport, not acceptance

Owner upload of Work files is not technical acceptance.

```text
OWNER_UPLOAD != ACCEPTANCE
WORK_PASS != MAIN_ACCEPTANCE
```

Main must read back the published Work artifacts and independently verify the important invariants before advancing the roadmap.

## 6. Anti-regression gates

```text
WORK_DIRECT_GITHUB_PUBLICATION_WITHOUT_OWNER_ORDER = 0
MULTI_FILE_WORK_HANDOFF_WITHOUT_ZIP = 0
WORK_ZIP_WITHOUT_DOWNLOAD_LINK = 0
WORK_REPORT_WITHOUT_REPOSITORY_PATHS = 0
OWNER_UPLOAD_MISTAKEN_FOR_ACCEPTANCE = 0
WORK_ONLY_RULE_APPLIED_TO_MAIN_PUBLICATION = 0
MAIN_REDUNDANT_REUPLOAD_OF_UNCHANGED_WORK_FILES = 0
MAIN_REMOTE_READBACK_AFTER_WORK_PUBLICATION = PASS
```

A later explicit owner instruction may override the transport mechanism for that bounded task only.
