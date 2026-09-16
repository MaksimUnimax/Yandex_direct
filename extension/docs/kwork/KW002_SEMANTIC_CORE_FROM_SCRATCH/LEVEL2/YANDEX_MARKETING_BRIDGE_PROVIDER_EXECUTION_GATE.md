# KW-002 — LEVEL 2 Yandex Marketing Bridge provider execution gate

Status: **ACTIVE / UNIVERSAL ROADMAP GATE**

Level-1 authority:

`../LEVEL1/YANDEX_MARKETING_BRIDGE_EXECUTION_RULE.md`

This gate applies whenever a KW-002 roadmap step uses Yandex Marketing Bridge to execute Wordstat, Search, deferred Search, GenSearch/AI-search or another provider-backed YMB command.

## 1. Roadmap steps covered

Mandatory for at least:

| Roadmap step | YMB use |
|---|---|
| STEP 03 | primary Wordstat acquisition |
| STEP 05 | targeted provider acquisition where justified |
| STEP 06 | current ordinary Yandex Search competitor discovery |
| STEP 08 | competitor-derived Wordstat expansion |
| STEP 12 | current ordinary Yandex Search evidence acquisition |
| STEP 16 | GenSearch / AI-search evidence acquisition |

The same gate applies to corrective/re-acquisition branches inside those steps.

## 2. Before rendering any command

Executor must first establish:

```text
CURRENT_ACCEPTED_YMB_BUILD = known
CURRENT_PROTOCOL_PREFIX = verified
CURRENT_RESULT_PREFIX = verified
ACTIVE_YMB_SERVICE = explicit
MANUAL_OR_AUTORUN_MODE = explicit
COMMAND_JSON = validated against current protocol
PROVIDER_PERMISSION = released by current cursor/gate
```

If any item is unknown, do not guess a command.

## 3. Required assistant output form for Manual execution

One command = one standalone fenced Markdown code block.

Required block shape:

```text
<PROTOCOL_PREFIX>
<ONE JSON OBJECT>
```

Forbidden inside the same block:

```text
explanatory prose
bullets
second command
second protocol
expected result fabricated by assistant
```

The executable command block must be separate from owner-facing explanation.

## 4. Required real execution sequence

```text
COMMAND_PREPARED
→ STANDALONE_CODE_BLOCK_RENDERED
→ YMB `Яндекс` ACTION DISCOVERED
→ OWNER/USER CLICKS `Яндекс`
→ BRIDGE PREFLIGHT/ACTION ATTEMPT
→ ACTUAL *_RESULT_V1 RECEIVED
→ RESULT RECONCILED
→ REQUIRED EVIDENCE PERSISTED/READ BACK
→ NEXT ACTION MAY BE RELEASED
```

No arrow may be skipped by assumption.

Especially:

```text
RENDERED COMMAND != EXECUTED COMMAND
CLICK != SUCCESSFUL PROVIDER EXECUTION
EXPECTED RESULT != ACTUAL RESULT
PROVIDER SUCCESS != PROJECT STEP COMPLETION
```

## 5. Result/accounting fields

Every provider-backed execution record must preserve the actual Bridge truth available for that protocol, including as applicable:

```text
protocol/action
result prefix
request_executed
provider_calls
automatic_retry
job_id
operation_id
provider/local status
result count / normalized count
error/UNKNOWN state
```

Do not increase provider-call accounting without an actual result proving execution.

## 6. Current known command families

The current accepted job/build must re-verify these before use; they are not immutable forever.

```text
WORDSTAT_API_V1 -> WORDSTAT_RESULT_V1
WORDSTAT_BATCH_API_V1 -> WORDSTAT_BATCH_RESULT_V1
SEARCH_API_V1 -> SEARCH_RESULT_V1
SEARCH_ASYNC_BATCH_API_V1 -> SEARCH_ASYNC_BATCH_RESULT_V1
```

`SEARCH_API_V1` is used for both ordinary Search and `method:"genSearch"` in the accepted current build.

## 7. Step-specific application

### STEP 03 / STEP 08 — Wordstat

Before every actual Wordstat acquisition command, apply this gate in addition to Wordstat depth, RAW persistence and remote-readback rules.

### STEP 05 — targeted provider acquisition

Only candidates already released by the Step05 information-gain/provider gate may reach YMB. The Bridge execution gate then controls how the command is rendered, triggered and proven.

### STEP 06 — competitor discovery

Ordinary/deferred Search commands must follow this gate. Deferred local `start`, provider `submitN`, explicit `collectN`, local status and export are separate actions and must not be collapsed into one claimed execution state.

### STEP 12 — full current SERP acquisition

Every selected-query Search command/batch must follow this gate before the result can count toward SERP coverage.

### STEP 16 — AI-search

GenSearch/AI-search commands must follow this gate. A generated answer shown in chat is not AI-search provider evidence unless it came from the actual Bridge/provider result required by the step.

## 8. Failure handling

If no `Яндекс` action appears or no result comes back:

```text
DO NOT CLAIM EXECUTION
DO NOT INCREASE PROVIDER_CALLS
DO NOT GUESS JOB/OPERATION STATE
DO NOT USE DEVTOOLS BYPASS
DO NOT AUTO-RETRY UNKNOWN PAID REQUESTS
```

Investigate normal YMB preconditions and current production contract first.

## PASS

```text
COMMAND_FORMAT = PASS
ONE_COMMAND_PER_BLOCK = true
REAL_YMB_TRIGGER_USED = true
ACTUAL_BRIDGE_RESULT_RECEIVED = true
REQUEST_EXECUTED_RECONCILED = true
PROVIDER_CALLS_RECONCILED = true
REQUIRED_EVIDENCE_PERSISTENCE = PASS where applicable
NO_FALSE_EXECUTION_CLAIM = true
```

If an actual result has not yet been received, this gate remains at `COMMAND_PREPARED` / `EXECUTION_NOT_VERIFIED`; it cannot PASS.
