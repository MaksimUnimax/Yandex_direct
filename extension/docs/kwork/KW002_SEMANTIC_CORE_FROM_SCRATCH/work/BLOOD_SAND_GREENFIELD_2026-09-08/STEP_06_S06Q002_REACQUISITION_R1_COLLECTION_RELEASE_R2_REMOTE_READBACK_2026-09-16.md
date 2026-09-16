# KW-002 Step06 — S06Q002 CONTROLLED REACQUISITION R1 COLLECTION RELEASE R2 REMOTE READBACK

Date: 2026-09-16
Status: **PASS / RELEASE R2 AND CURSOR V47 VERIFIED / EXACTLY ONE collectN MAY BE ACTIVATED BY SUCCESSOR CURSOR**

## 1. Scope

```text
QUERY_ID = S06Q002
QUERY_TEXT = оберег
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q002-r1-20260916
PROVIDER_OPERATION_ID = sprriom53ppme5q13epe
```

## 2. Live remote truth

```text
BRANCH = roadmap/kwork-productization-2026-08-28
HEAD = 0479a797dd8bd9702a761e11d3dac4356e191474
HEAD_MESSAGE = docs(kw002): activate S06Q002 R1 collection R2 readback gate
COLLECTION_RELEASE_R2_FILE = STEP_06_S06Q002_REACQUISITION_R1_COLLECTION_RELEASE_R2_2026-09-16.md
COLLECTION_RELEASE_R2_BLOB_SHA = f55574032cb08ece68d5b010fac147df95599cd0
CURSOR_SCHEMA = KW002_CURRENT_EXECUTION_CURSOR_V47
CURSOR_BLOB_SHA = 99c786cd3870850812a2bc2f6f1bb664ba219620
```

The live remote release and cursor agree that:

```text
provider_submit_calls = 1
provider_collect_calls = 0
local_no_due_collect_commands = 1
WAITING = 1
polls_started = 0
revision = 2
V46 conservative threshold = 2026-09-16T12:36:54+05:00
R2 live-time check = 2026-09-16T12:36:57+05:00
R2 conservative guard elapsed = true
```

## 3. Exact command eligible for successor activation

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"collectN","jobId":"kw002-s06q002-r1-20260916","count":1}
```

Runtime due-state remains authoritative. If the command again returns `NO_DUE_OPERATIONS`, it must be preserved as a local no-op and must not be counted as a provider collect.

## 4. Boundary

```text
EXACT_COLLECTION_COMMANDS_TO_AUTHORIZE_IN_SUCCESSOR_CURSOR = 1
SECOND_PROVIDER_SUBMIT_ALLOWED = false
AUTOMATIC_RETRY = false
SYNCHRONOUS_SEARCH_CALLS_ALLOWED = 0
WORDSTAT_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
PROVIDER_CALLS_DURING_THIS_READBACK = 0
```

After the one collection command, preserve its exact returned envelope before any export or subsequent collection decision.

## 5. Verdict

```text
S06Q002_R1_COLLECTION_RELEASE_R2_REMOTE_READBACK = PASS
COLLECT_MAY_BE_ACTIVATED_BY_SUCCESSOR_CURSOR = true
PROVIDER_SUBMIT_MAY_NOT_REPEAT = true
S06Q003_RELEASED = false
```
