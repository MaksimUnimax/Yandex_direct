# KW-001 — UNIVERSAL RULES VS PER-JOB WORKSPACE

Date updated: 2026-09-01  
Status: **ACTIVE / UNIVERSAL / OWNER-LOCKED**

This document defines the strict two-layer architecture for KW-001.

---

## 1. Layer A — permanent universal Kwork rules

Permanent layer:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/
```

This layer contains only reusable universal material for the Kwork itself, for example:

```text
workflow/runbook
pre-step review rules
dialogue/analytical discipline
provider/operator safety rules
method-origin rules
approved methodology corrections
approved prevent-repeat rules
product/package boundaries
client private-access policy
templates
```

Mandatory Layer-A companion for client-owned Yandex data:

```text
CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md
```

This policy must be read and applied whenever a job reaches a step that can use client-private Yandex Webmaster evidence. The currently known mandatory access-check steps are 11, 12, 13 and 16. The base Kwork must remain executable without mandatory Webmaster access unless the owner explicitly changes the commercial product policy.

### Owner-lock rule

**Universal rules do not change during execution of a concrete job unless the owner explicitly instructs ChatGPT to change/add/remove a universal rule.**

Finding a possible defect during a job does **not** authorize ChatGPT to edit the permanent method.

Allowed behavior without owner instruction:

```text
identify possible universal-rule problem
explain it in the owner-facing report
show evidence/sources
propose a change
WAIT
```

Forbidden behavior without owner instruction:

```text
automatically update universal runbook
promote a job incident into a permanent lesson
automatically add prevent-repeat rules
rewrite permanent methodology because one case behaved differently
```

Only an explicit owner instruction such as `внеси это в общие правила`, `исправь методику`, `запиши это как постоянное правило` authorizes mutation of Layer A.

---

## 2. Layer B — one concrete job / disposable workspace

Every new client order, test or rehearsal receives one isolated temporary directory.

Canonical future path:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/work/<JOB_ID>/
```

This is **not** a methodology directory. It is the complete working memory and execution history of one concrete job.

It may contain:

```text
JOB_MANIFEST.md
JOB_FLOW.md / current-step status
frozen client/order brief
site/domain facts
URL inventory
business/page model
open client questions
seed plans
all words/phrases
raw Wordstat evidence
raw Search/SERP evidence
raw GenSearch evidence
cleaned phrase tables
review queues
cluster candidates
page maps
matrices
step plans/checkpoints/status/acceptances
intermediate calculations
job-specific decisions and corrections
operator/provider execution records
client deliverables/drafts
revision records
economics/QA records
client private-access state and exact property when applicable
```

It may record **what happened in this job and how this job progressed**.

It must not define permanent universal rules for future jobs.

---

## 3. Strict separation

### Layer A may contain

```text
universal rules approved by owner
reusable stable methodology
owner-approved corrections to methodology
```

### Layer A must not contain

```text
client domains
client URLs
client keyword lists
raw provider results
case-specific matrices
case-specific page maps
case-specific conclusions
```

### Layer B may contain

```text
all concrete job evidence
all concrete job workflow/status
job-specific analytical decisions
job-specific correction history
```

### Layer B must not contain

```text
new universal rules
permanent prevent-repeat policy
claims that a case-specific decision governs future jobs
```

A job file may say `for this job we corrected X because Y evidence showed Z`; it must not say `therefore all future jobs must always do X` unless the owner has separately authorized that universal rule in Layer A.

---

## 4. Create workspace before every new job

Before concrete analysis begins:

```text
1. create work/<JOB_ID>/;
2. create JOB_MANIFEST.md;
3. create/freeze the job's own working flow/brief;
4. record the initial YANDEX_WEBMASTER_ACCESS_STATE without making it a purchase blocker;
5. keep all later job-specific files inside this directory.
```

Do not scatter a client/job across the permanent Kwork layer.

Initial private-access state is informational:

```text
UNKNOWN | UNAVAILABLE | AVAILABLE_NOT_GRANTED | GRANTED_NOT_READY | READY
```

`UNAVAILABLE` is a normal base-package state under `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`.

---

## 5. Job lifecycle

The job directory is temporary from the moment it is created.

Lifecycle:

```text
CREATE JOB DIRECTORY
→ RUN COMPLETE JOB INSIDE IT
→ COMPLETE FINAL HANDOFF / REVISIONS / QA
→ MARK JOB CLOSED
→ DELETE THE ENTIRE JOB DIRECTORY
```

There is **no mandatory lesson-extraction or automatic universal-method update at job close**.

If during the job the owner explicitly ordered a universal-rule change, that change is made directly in Layer A at that time. It is not dependent on final job cleanup.

---

## 6. Deletion gate

Delete the complete per-job directory when:

```text
job work complete = true
final deliverable/handoff complete = true
open revision/rework = false
provider/operator action pending = false
owner has not requested the workspace to be retained = true
safe_to_delete = true
```

Then delete the entire directory from the repository.

Do not retain old job directories merely as methodology history.

Git history may of course contain old commits, but the active branch must not keep the closed workspace tree.

---

## 7. Current legacy OKNO-MSK workspace

Current active rehearsal already lives at:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/
```

Do not move it mid-run merely for naming consistency.

Treat it exactly as Layer B:

```text
contains only OKNO-MSK job evidence + workflow
is temporary
is deleted completely after the job closes
```

Future jobs use `work/<JOB_ID>/`.

For the current OKNO-MSK rehearsal, the owner has explicitly established:

```text
YANDEX_WEBMASTER_ACCESS_STATE = UNAVAILABLE
YANDEX_WEBMASTER_PRIVATE_EVIDENCE_USED = false
BASE_PUBLIC_EVIDENCE_MODE = true
```

This is a current-job fact recorded in Layer B; the reusable rule governing what that means lives in `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`.

---

## 8. Pre-step relationship

Before each major step, ChatGPT reads:

```text
Layer A universal rules
CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md
current job JOB_MANIFEST.md
current job JOB_FLOW.md / relevant step records
previous step evidence/acceptance
```

For Steps 11, 12, 13 and 16, the pre-step review must contain the access-state block required by `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md` and must explain:

```text
current access state
why Webmaster can help in this step
base path without access
enhanced path with access
whether the first-access comparison has already been completed
```

If access is unavailable:

```text
DO NOT BLOCK THE BASE JOB MERELY FOR THAT REASON
DO NOT INVENT PRIVATE PERFORMANCE/HISTORY/OWNED-VISIBILITY CLAIMS
CONTINUE UNDER THE BOUNDED BASE EVIDENCE MODE FOR THAT STEP
```

If self-audit finds a possible flaw in Layer A:

```text
REPORT TO OWNER
DO NOT EDIT LAYER A
WAIT FOR EXPLICIT OWNER INSTRUCTION
```

If self-audit finds a flaw only in the current job execution/artifact:

```text
report it in the pre-step review
correct the current job only after the normal owner authorization gate
```

---

## 9. First real Webmaster access transition

The first future job whose access state becomes `READY` must not simply switch methods silently.

Apply the mandatory controlled comparison in `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`:

```text
freeze WITHOUT_ACCESS baseline first
→ persist/read back
→ use delegated Webmaster evidence
→ create WITH_ACCESS result
→ compare CHANGE / DE_RISK / NEW_FINDING / NO_CHANGE
→ only after comparison consider changing universal product policy
```

The same first-access event also triggers a governed Webmaster Bridge capability review. It does not authorize speculative implementation of every available Webmaster API method.

---

Markers:

```text
KW001_TWO_LAYER_ARCHITECTURE_ACTIVE = true
KW001_UNIVERSAL_RULES_OWNER_LOCKED = true
KW001_NO_AUTOMATIC_UNIVERSAL_RULE_PROMOTION = true
KW001_PER_JOB_WORKSPACE_REQUIRED = true
KW001_PER_JOB_WORKSPACE_DISPOSABLE = true
KW001_JOB_WORKFLOW_BELONGS_IN_JOB_WORKSPACE = true
KW001_JOB_WORKSPACE_DELETE_AFTER_CLOSE = true
KW001_FUTURE_JOB_PATH = work/<JOB_ID>/
KW001_CLIENT_PRIVATE_YANDEX_ACCESS_POLICY_REQUIRED = true
KW001_WEBMASTER_ACCESS_NOT_REQUIRED_FOR_BASE_JOB = true
KW001_WEBMASTER_ACCESS_CHECK_REQUIRED_STEPS_11_12_13_16 = true
KW001_FIRST_READY_WEBMASTER_JOB_REQUIRES_COMPARISON = true
```
