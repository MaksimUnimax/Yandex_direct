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
current_major_step = STEP_05_COMPLETE_PASS
next_major_step = STEP_06_PRE_STEP_REVIEW
job_work_complete = false
final_handoff_complete = false
revision_rework_open = true
provider_operator_action_pending = false
safe_to_delete = false
```

## Authority

This directory is the complete temporary working memory and execution history for the current OKNO-MSK job.

It may contain only material specific to this job, including:

```text
mock/client brief
site facts / URLs
job-specific business/page model
words / phrases
provider evidence
job step plans
job flow/status/checkpoints
job-specific corrections
matrices
page/cluster decisions
deliverables
job economics / QA / revisions
```

It must not define permanent universal KW-001 rules.

Universal methodology lives only in the parent permanent KW-001 layer and may be changed only on explicit owner instruction.

## Current flow authority

Use:

```text
JOB_FLOW.md
```

for the current job's step sequence and status.

Current completed Step-5 authorities:

```text
STEP_05_PRE_STEP_REVIEW.md
STEP_05_WORDSTAT_PASS2_MANIFEST.md
STEP_05_P2_01_CHECKPOINT.md
STEP_05_P2_02_CHECKPOINT.md
STEP_05_P2_03_CHECKPOINT.md
STEP_05_P2_04_CHECKPOINT.md
STEP_05_P2_01_RAW_NORMALIZED.tsv
STEP_05_P2_02_RAW_NORMALIZED.tsv
STEP_05_P2_03_RAW_NORMALIZED.tsv
STEP_05_P2_04_RAW_NORMALIZED.tsv
STEP_05_FINAL_BATCH_STATUS.md
STEP_05_ACCEPTANCE.md
```

Step-5 final facts:

```text
job_id = kw001-okno-msk-wordstat-pass2-20260828
status = COMPLETED
succeeded = 4
failed_terminal = 0
outcome_unknown = 0
requests_started = 4
estimated_cost_rub = 0.08
next_safe_action = NONE
```

No provider/operator action is currently pending. The next major step requires its own pre-step review and explicit owner authorization.

## Close rule

When all are true:

```text
job_work_complete = true
final_handoff_complete = true
revision_rework_open = false
provider_operator_action_pending = false
safe_to_delete = true
```

then delete the entire:

```text
tests/OKNO_MSK/
```

directory from the active branch.

There is no mandatory export/extraction of job lessons into permanent rules at close.

Markers:

```text
KW001_OKNO_MSK_WORKSPACE_DISPOSABLE = true
KW001_OKNO_MSK_WORKSPACE_JOB_SPECIFIC_ONLY = true
KW001_OKNO_MSK_STEP_05_COMPLETE = true
KW001_OKNO_MSK_PROVIDER_OPERATOR_ACTION_PENDING = false
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```
