# KW-001 — PER-JOB WORKSPACE LIFECYCLE

Date created: 2026-08-28  
Status: **ACTIVE / UNIVERSAL / REQUIRED FOR EVERY NEW JOB**

This document defines the separation between permanent Kwork methodology and disposable evidence/workspace for one concrete client/test job.

---

## 1. Core separation

KW-001 must always maintain two distinct layers.

### A. Permanent Kwork layer

Lives directly under:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/
```

Contains only reusable cross-job knowledge such as:

```text
workflow/runbook
pre-step review rules
dialogue/analytical discipline
provider/operator safety rules
method-origin rules
per-step reusable lessons
known failure modes
prevent-repeat rules
final reusable templates
product definition / package boundaries
```

Do **not** store concrete client domains, URLs, keyword lists, provider result dumps, client matrices, case-specific page maps or client conclusions in this permanent layer.

### B. Per-job disposable workspace

Every new order/test/rehearsal must receive its own isolated directory inside the Kwork area.

Canonical future path:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/work/<JOB_ID>/
```

A job directory may contain everything needed only for that concrete work:

```text
client brief / frozen order
site/domain facts
URL inventory
business/page model
open client questions
seed plans
raw Wordstat phrases/results
raw Search/SERP evidence
raw GenSearch evidence
cleaned phrase tables
review queues
cluster candidates
page maps
Search-vs-AI matrices
source/competitor matrices
step checkpoints
step acceptances
intermediate calculations
client deliverables / drafts
revision records
economics/operator-burden records
job-specific QA evidence
```

This directory is the complete working memory for the concrete job and is intentionally disposable after the job is fully closed.

---

## 2. Rule — create workspace before starting a new job

**RULE**  
Before any concrete client/test analysis begins, create one dedicated per-job directory and keep all case-specific artifacts inside it.

Do not scatter one client's files across the permanent Kwork directory.

**PURPOSE**  
Prevent cross-client contamination, stale evidence reuse and repository clutter.

**FAILURE IF IGNORED**

```text
future ChatGPT may reuse old client words/URLs by mistake;
case-specific evidence may look like universal methodology;
cleanup becomes difficult;
client/test artifacts accumulate permanently;
method docs become polluted with examples that anchor later work;
```

**REVIEW TRIGGER**  
Only if repository storage/lifecycle is later replaced by a different formally accepted workspace system.

---

## 3. Rule — no concrete case evidence in permanent methodology docs

Permanent docs may record only generalized lessons such as:

```text
PROJECT_TEST_VALIDATED: cross-channel discovery exposed complementary blind spots
```

They must not retain concrete case material such as:

```text
specific domain
specific URL
specific client keyword list
exact case cluster/page map
raw provider payload
client-specific page recommendation
```

Concrete evidence belongs only in the active job workspace until that workspace is deleted.

---

## 4. Job-close extraction gate

A per-job workspace must **not** be deleted immediately when the client deliverable is produced.

Before deletion run the mandatory extraction gate:

```text
1. confirm client/job work is fully closed;
2. confirm no revision/rework remains open;
3. review every recorded error/incident/lesson from the job;
4. promote only reusable lessons into permanent methodology docs;
5. update STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md where needed;
6. update universal runbook/rules if method changed;
7. record product/economics changes if reusable;
8. verify no client-specific facts leaked into universal docs;
9. confirm final deliverable has been handed off/stored where required;
10. only then delete the complete per-job workspace directory from the repo.
```

This extraction step prevents two opposite failures:

```text
A. keeping every old job forever and polluting the repository;
B. deleting a job before its reusable lessons have been captured.
```

---

## 5. Rule — delete the entire job directory after successful close extraction

**RULE**  
After the job is fully closed and reusable lessons have been promoted, delete the entire per-job workspace directory from the repository.

Do not keep old case workspaces merely as passive history.

**PURPOSE**  
Keep the Kwork repository clean and force the permanent methodology to contain only generalized, reusable knowledge.

**FAILURE IF IGNORED**

```text
repository bloat;
stale-case anchoring;
accidental cross-client evidence reuse;
unclear authority between old case files and current runbook;
slow clean-context onboarding;
```

**REVIEW TRIGGER**  
If a future compliance/audit requirement explicitly requires long-term case retention, then retention must use a separate archive policy rather than the active Kwork methodology directory.

---

## 6. Exception — active historical workspace already created under another path

Do not migrate an in-progress job solely to satisfy the new folder name if migration risks broken references or unnecessary churn.

For an already active workspace under a legacy path such as:

```text
tests/<CASE_ID>/
```

apply the same lifecycle semantics:

```text
ACTIVE = temporary job workspace
CLOSE = extract reusable lessons
THEN = delete complete case directory
```

Future new jobs should use the canonical `work/<JOB_ID>/` path unless the owner changes this convention.

---

## 7. Required workspace manifest

Every new per-job workspace should begin with a small authority file:

```text
JOB_MANIFEST.md
```

Minimum fields:

```text
JOB_ID
KWORK_ID
status
created_at
client/test label
scope freeze reference
current step
workspace is disposable = true
close-extraction complete = false
safe-to-delete = false
```

At completion, before deletion, set/check:

```text
close-extraction complete = true
universal lessons promoted = true
final handoff complete = true
revision window closed = true
safe-to-delete = true
```

The directory may be deleted only when all required close conditions are true.

---

## 8. Relationship to per-step review

Before every major step, ChatGPT must read:

```text
PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md
STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md
current job workspace JOB_MANIFEST.md
current job STEP_REVIEW_AND_ERRORS_LEDGER.md if present
previous step acceptance/evidence
```

This ensures permanent method truth and current-job facts remain separated but both are available during execution.

---

## 9. Current OKNO-MSK handling

The existing rehearsal workspace currently lives under the legacy path:

```text
tests/OKNO_MSK/
```

It is treated as a disposable active job workspace under this rule.

Do not move it mid-run solely for naming consistency.

When the OKNO-MSK rehearsal is fully completed:

```text
extract all reusable methodology lessons
update permanent KW-001 docs
confirm final rehearsal artifacts/handoff requirements
mark safe-to-delete
then delete the entire tests/OKNO_MSK/ directory
```

No concrete OKNO-MSK evidence should remain in the permanent universal layer after final cleanup, except generalized lessons stripped of case-specific facts.

---

Markers:

```text
KW001_PER_JOB_WORKSPACE_REQUIRED = true
KW001_PER_JOB_WORKSPACE_DISPOSABLE = true
KW001_JOB_CLOSE_EXTRACTION_REQUIRED = true
KW001_JOB_WORKSPACE_DELETE_AFTER_CLOSE = true
KW001_PERMANENT_METHOD_SEPARATE_FROM_CASE_EVIDENCE = true
KW001_FUTURE_JOB_PATH = work/<JOB_ID>/
```
