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
current_major_step = STEP_03_REPAIR_PRE_STEP
next_major_step = STEP_03_REPAIR_PROVIDER_EXECUTION_AFTER_OWNER_AUTHORIZATION
job_work_complete = false
final_handoff_complete = false
revision_rework_open = true
provider_operator_action_pending = false
safe_to_delete = false
```

## Authority

This directory is the complete temporary working memory and execution history for the current OKNO-MSK job.

It may contain only material specific to this job: mock/client brief, site facts/URLs, job-specific business/page model, words/phrases, provider evidence, job step plans, job flow/status/checkpoints, job-specific corrections, matrices, page/cluster decisions, deliverables, job economics/QA/revisions.

It must not define permanent universal KW-001 rules. Universal methodology lives only in the parent permanent KW-001 layer and may be changed only on explicit owner instruction.

## Current flow authority

Use `JOB_FLOW.md` for the current job sequence/status.

The current Step-03 correction authority is:

```text
STEP_03_COMPLETION_CORRECTION_2026-08-29.md
```

It supersedes the historical PASS verdict in `STEP_03_ACCEPTANCE.md`.

Current truth:

```text
historical Step-03 provider calls = 18 successful technical executions
complete first-pass phrase dataset preserved = false
Step 03 project completion = false
Step 03 repair required = true
forward semantic analysis blocked = true
```

## Preserved downstream observations

Step-05 provider responses:

```text
4/4 preserved completely
estimated provider cost = 0.08 RUB
```

These observations remain valid, but sufficiency of the four-probe expansion choice must be rechecked after Step-03 repair.

Step-06 dynamics responses:

```text
4/4 preserved completely
24 monthly rows per root preserved
estimated provider cost = 0.08 RUB
```

These remain usable standalone demand-history observations and do not repair Step 03.

## Current required repair

Repeat the exact frozen 18 Step-02 Wordstat seeds as a fresh current observation and, after every individual provider call, preserve and verify the complete returned `results[] + associations[]` before any next provider call.

No provider/operator action is currently pending until the Step-03 repair pre-step review is frozen and the owner explicitly authorizes provider execution.

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
KW001_OKNO_MSK_STEP_03_COMPLETE = false
KW001_OKNO_MSK_STEP_03_REPAIR_REQUIRED = true
KW001_OKNO_MSK_FORWARD_ANALYSIS_BLOCKED = true
KW001_OKNO_MSK_PROVIDER_OPERATOR_ACTION_PENDING = false
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```
