# KW-002 — WORK ARTIFACT HANDOFF AND OWNER PUBLICATION RULE

Status: **OWNER-MANDATED / ACTIVE / UNIVERSAL / MUST APPLY TO FUTURE WORK HANDOFFS**
Decision date: 2026-09-16
Applies to: all KW-002 Main ChatGPT → Work execution passes that create or modify project artifacts.

## 1. Purpose

Large artifact publication through Main ChatGPT or Work can consume disproportionate tool calls, context and execution time while adding little analytical value.

For normal KW-002 Work handoffs, the owner is the transport/publication intermediary:

```text
WORK = EXECUTION + QA + PACKAGING
OWNER = DOWNLOAD + GITHUB PUBLICATION TRANSPORT
MAIN CHATGPT = ARCHITECTURE + ACCEPTANCE + REMOTE READBACK + NEXT-STEP CONTROL
```

This rule changes only the transport/publication workflow. It does **not** reduce Work's responsibility for correctness, completeness, reproducibility or QA.

---

## 2. Default handoff contract

Unless the owner explicitly instructs otherwise, a Work execution pass that creates or changes multiple project files must:

1. complete the full bounded task;
2. perform every required QA gate;
3. collect all final deliverable files into **one `.zip` archive**;
4. include only final task artifacts plus a manifest when useful;
5. provide the owner with a direct downloadable link to that ZIP;
6. report the exact ZIP filename;
7. report every file contained in the ZIP;
8. report the recommended exact repository path for every file;
9. state which files are new and which replace existing artifacts;
10. report QA status and all material limitations;
11. state what remained outside the bounded task.

The owner then downloads the archive and publishes its contents to GitHub manually.

After publication, the owner returns to Main ChatGPT with:

- the Work final report;
- the GitHub commit/repository location or links to the published artifacts.

Main ChatGPT then performs remote readback/acceptance and controls the next roadmap step.

---

## 3. Work must not publish by default

Unless the owner explicitly commands publication by Work, Work must **not** spend resources on:

- GitHub commit;
- GitHub push;
- force-push;
- pull-request creation;
- GitHub publication;
- repeated one-by-one upload of a multi-file artifact package.

The default is:

```text
WORK_OUTPUT_READY
-> QA PASS
-> ZIP PACKAGE
-> OWNER DOWNLOAD
-> OWNER MANUAL GITHUB PUBLICATION
-> MAIN CHATGPT REMOTE READBACK / ACCEPTANCE
```

---

## 4. ZIP requirement

ZIP packaging is mandatory when the Work task creates or modifies:

- multiple related files;
- large CSV/JSON evidence sets;
- analytical packages;
- machine-readable registers plus reports;
- any artifact set whose one-by-one transfer would waste material execution resources.

ZIP packaging may be omitted for a single small text artifact when the owner does not require an archive.

The ZIP must contain the final deliverable versions, not temporary/intermediate scratch files unless those scratch artifacts are explicitly part of the required evidence package.

---

## 5. Manifest and final-report requirements

For multi-file handoffs, Work should include a manifest in the ZIP when useful. Whether or not a separate manifest file is necessary, the final Work report must contain:

```text
ZIP_FILENAME
FILES_IN_ARCHIVE
RECOMMENDED_REPOSITORY_PATH_PER_FILE
NEW_VS_REPLACEMENT_STATUS
QA_RESULT
TASK_COMPLETED
TASK_OUT_OF_SCOPE_OR_REMAINING
```

If the task has row-count, checksum, schema, invariant or reconciliation gates, Work must report those values explicitly.

A downloadable archive without a sufficient final report is not a complete handoff.

---

## 6. Owner role is transport, not analytical acceptance

Manual publication by the owner does **not** mean the owner becomes responsible for artifact correctness.

Responsibilities remain separated:

```text
WORK
= produces correct artifacts and proves QA

OWNER
= transports/publishes the already-produced artifacts

MAIN CHATGPT
= independently reads back published artifacts, performs acceptance and controls roadmap continuation
```

Owner upload is not equivalent to technical acceptance.

The next roadmap step must not be declared accepted merely because the owner uploaded the files.

---

## 7. Remote readback after owner publication

Where repository persistence is required, Main ChatGPT must verify the owner's publication before treating the handoff as durable.

At minimum, verify where applicable:

- expected files exist at the reported repository paths;
- file identities/content are consistent with the Work report;
- expected row/file counts reconcile;
- no required artifact is missing;
- no unintended scope expansion occurred.

If Work supplied hashes/checksums, compare them where practical.

```text
OWNER_UPLOAD != ACCEPTANCE
REMOTE_READBACK_PASS = REQUIRED_FOR_DURABLE_ACCEPTANCE
```

---

## 8. Explicit exceptions

This rule may be overridden only by a later explicit owner instruction for the specific task, for example:

- "commit and push it yourself";
- "create the PR";
- "do not ZIP this task";
- another explicit publication workflow.

An exception is local to the explicitly overridden task unless the owner states that the universal rule itself has changed.

---

## 9. Prompt-construction rule for Main ChatGPT

When Main ChatGPT delegates an applicable task to Work, the Work prompt must include the handoff requirement rather than assuming Work remembers it.

For applicable multi-file tasks the prompt must require, at minimum:

```text
DO NOT COMMIT OR PUSH UNLESS EXPLICITLY ORDERED.
PACKAGE ALL FINAL DELIVERABLES INTO ONE ZIP.
PROVIDE A DOWNLOAD LINK TO THE ZIP.
REPORT EVERY FILE IN THE ZIP AND ITS RECOMMENDED REPOSITORY PATH.
REPORT QA RESULTS AND ALL MATERIAL LIMITATIONS.
THE OWNER WILL MANUALLY PUBLISH THE FILES TO GITHUB.
```

This avoids wasting Work resources on publication transport and makes the owner-mediated workflow deterministic.

---

## 10. Anti-regression gates

For every applicable future Work handoff:

```text
WORK_DIRECT_GITHUB_PUBLICATION_WITHOUT_OWNER_ORDER = 0
MULTI_FILE_HANDOFF_WITHOUT_ZIP = 0
ZIP_HANDOFF_WITHOUT_DOWNLOAD_LINK = 0
FINAL_REPORT_WITHOUT_ARCHIVE_INVENTORY = 0
FINAL_REPORT_WITHOUT_RECOMMENDED_REPOSITORY_PATHS = 0
OWNER_UPLOAD_MISTAKEN_FOR_TECHNICAL_ACCEPTANCE = 0
MAIN_CHATGPT_REMOTE_READBACK_AFTER_REQUIRED_PUBLICATION = PASS
```

If any applicable gate fails, the handoff is incomplete and must not be treated as a finished project transition.
