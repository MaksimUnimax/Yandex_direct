# KW-001 / OKNO-MSK — JOB MANIFEST

Date updated: 2026-08-29  
Workspace status: **ACTIVE / DISPOSABLE / JOB-SPECIFIC ONLY / LEGACY PATH**

```text
JOB_ID = OKNO_MSK
KWORK_ID = KW001_AI_NATIVE_YANDEX_ALICE
workspace_path = extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/
canonical_future_workspace_path = extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/work/<JOB_ID>/
workspace_is_disposable = true
workspace_contains_universal_rules = false
legacy_path_allowed_until_close = true
current_major_step = STEP_06_DYNAMICS_MANIFEST_FROZEN
next_major_step = STEP_06_PROVIDER_EXECUTION_D1
job_work_complete = false
final_handoff_complete = false
revision_rework_open = true
provider_operator_action_pending = true
safe_to_delete = false
```

## Authority

This directory is the complete temporary working memory and execution history for the current OKNO-MSK job.

It may contain only material specific to this job: mock/client brief, site facts/URLs, job-specific business/page model, words/phrases, provider evidence, job step plans, job flow/status/checkpoints, job-specific corrections, matrices, page/cluster decisions, deliverables, job economics/QA/revisions.

It must not define permanent universal KW-001 rules. Universal methodology lives only in the parent permanent KW-001 layer and may be changed only on explicit owner instruction.

## Current flow authority

Use `JOB_FLOW.md` for current job sequence/status.

Completed Step-5 authorities remain frozen in the workspace, including full normalized provider rows and `STEP_05_ACCEPTANCE.md`.

Current Step-6 authorities:

```text
STEP_06_PRE_STEP_REVIEW.md
STEP_06_DYNAMICS_MANIFEST.md
```

Frozen Step-6 execution:

```text
method = getDynamics
period = PERIOD_MONTHLY
fromDate = 2024-08-01T00:00:00Z
toDate = 2026-07-31T23:59:59Z
regions = ["213"]
devices = ["DEVICE_ALL"]
D1 = пластиковые окна
D2 = остекление балконов
D3 = остекление веранды
D4 = окна для частного дома
provider_request_ceiling = 4
estimated_step_cost_rub = 0.08
```

No Step-6 provider request had been made at manifest freeze. Provider/operator action is pending for D1.

## Close rule

When all are true:

```text
job_work_complete = true
final_handoff_complete = true
revision_rework_open = false
provider_operator_action_pending = false
safe_to_delete = true
```

then delete the entire `tests/OKNO_MSK/` directory from the active branch.

There is no mandatory export/extraction of job lessons into permanent rules at close.

Markers:

```text
KW001_OKNO_MSK_WORKSPACE_DISPOSABLE = true
KW001_OKNO_MSK_WORKSPACE_JOB_SPECIFIC_ONLY = true
KW001_OKNO_MSK_STEP_05_COMPLETE = true
KW001_OKNO_MSK_STEP_06_MANIFEST_FROZEN = true
KW001_OKNO_MSK_PROVIDER_OPERATOR_ACTION_PENDING = true
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```
