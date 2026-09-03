# KW-001 — UNIVERSAL RULES VS PER-JOB WORKSPACE

Updated: 2026-09-03  
Status: **ACTIVE / UNIVERSAL / OWNER-LOCKED**

This document defines the strict two-layer architecture for KW-001.

---

## 1. Layer A — permanent universal Kwork rules

Permanent layer:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/
```

This layer contains reusable universal material only, for example:

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

Mandatory companions include:

```text
CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md
PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md
```

### Owner-lock rule

Universal rules do not change during execution of a concrete job unless the owner explicitly instructs ChatGPT to change/add/remove a universal rule.

Finding a possible defect during a job does **not** itself authorize permanent-method mutation.

Allowed without owner instruction:

```text
identify possible universal-rule problem
explain it
show evidence/sources
propose a change
WAIT
```

Forbidden without owner instruction:

```text
automatically update universal runbook
promote a job incident into a permanent lesson
automatically add prevent-repeat rules
rewrite permanent methodology because one case behaved differently
```

Only explicit owner instruction authorizes Layer-A mutation.

---

## 2. Layer B — one concrete job / disposable workspace

Every new client order, test or rehearsal receives one isolated temporary directory.

Canonical future path:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/work/<JOB_ID>/
```

This is not a methodology directory. It is the working memory and execution history of one concrete job.

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
raw provider evidence
cleaned phrase tables
review queues
cluster candidates
page maps
matrices
step plans/checkpoints/status/acceptances
intermediate calculations
job-specific decisions/corrections
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
client/test case identity
client domains or URLs
client keyword/product/service lists
raw provider results
case-specific matrices or page maps
case-specific conclusions/counts/status
case-specific provider receipts/costs
case-specific commit/branch incidents as method inputs
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

A job file may say `for this job we corrected X because Y evidence showed Z`; it must not say `therefore all future jobs must always do X` unless the owner separately authorized that universal rule in Layer A.

---

## 4. Create workspace before every new job

Before concrete analysis begins:

```text
1. create work/<JOB_ID>/;
2. create JOB_MANIFEST.md;
3. create/freeze the job's own working flow/brief;
4. record initial client-private access state without making it a purchase blocker unless product policy says otherwise;
5. keep later job-specific files inside this directory.
```

Do not scatter a client/job across the permanent Kwork layer.

Initial private-access state can use equivalent values:

```text
UNKNOWN | UNAVAILABLE | AVAILABLE_NOT_GRANTED | GRANTED_NOT_READY | READY
```

`UNAVAILABLE` is a normal base-package state under `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`.

---

## 5. Job lifecycle

The job directory is temporary from creation.

```text
CREATE JOB DIRECTORY
→ RUN COMPLETE JOB INSIDE IT
→ COMPLETE FINAL HANDOFF / REVISIONS / QA
→ MARK JOB CLOSED
→ DELETE THE ENTIRE JOB DIRECTORY
```

There is no mandatory lesson extraction or automatic universal-method update at job close.

If during the job the owner explicitly ordered a universal-rule change, that change is made directly in Layer A at that time. It is not dependent on final cleanup.

---

## 6. Deletion gate

Delete the complete per-job directory when:

```text
job work complete = true
final deliverable/handoff complete = true
open revision/rework = false
provider/operator action pending = false
owner has not requested workspace retention = true
safe_to_delete = true
```

Do not retain old job directories merely as methodology history. Git history may preserve past commits, but active branch policy follows the lifecycle rule.

---

## 7. Legacy workspace handling

Older active rehearsals/jobs may already live under legacy paths such as:

```text
extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/<CASE_ID>/
```

Do not move an active job mid-run merely for naming consistency when relocation itself would create avoidable state/provenance risk.

Treat every such legacy path exactly as Layer B:

```text
contains only that job's evidence + workflow
is temporary
must not define universal rules
is deleted under the normal close/deletion gate
```

Concrete case IDs/access states belong inside that Level-2 workspace and must not be copied into this permanent lifecycle rule.

Future jobs use `work/<JOB_ID>/` unless owner-approved architecture changes.

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

For access-sensitive steps, apply the current access policy. If access is unavailable:

```text
DO NOT BLOCK A BASE JOB MERELY FOR THAT REASON WHEN POLICY ALLOWS BASE MODE
DO NOT INVENT PRIVATE PERFORMANCE/HISTORY/OWNED-VISIBILITY CLAIMS
CONTINUE UNDER THE BOUNDED BASE EVIDENCE MODE FOR THAT STEP
```

If self-audit finds a possible flaw in Layer A:

```text
REPORT TO OWNER
DO NOT EDIT LAYER A
WAIT FOR EXPLICIT OWNER INSTRUCTION
```

If self-audit finds a flaw only in current job execution/artifact:

```text
report it
correct current job under the applicable authorization gate
```

---

## 9. First real private-access transition

The first future job whose relevant private-access state becomes usable must apply the controlled comparison defined by `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md` before universal commercial/method claims are changed.

Canonical pattern:

```text
freeze WITHOUT_ACCESS baseline first
→ persist/read back
→ use delegated private evidence
→ create WITH_ACCESS result
→ compare change/de-risk/new-finding/no-change
→ only after comparison consider changing universal product policy
```

A first-access event may trigger a governed Bridge capability review. It does not authorize speculative implementation of every available API method.

---

## Markers

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
KW001_FIRST_READY_PRIVATE_ACCESS_JOB_REQUIRES_COMPARISON = true
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
