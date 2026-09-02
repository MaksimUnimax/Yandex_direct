# OKNO_MSK — Step 16 process non-repeat rules / YMB command-surface addendum

Date: 2026-09-02
Authority type: **job-specific Step-16 execution rule / owner-requested non-repeat addendum**
Status: **ACTIVE FOR THE REMAINDER OF STEP 16**
Parent authority: `STEP_16_PROCESS_NON_REPEAT_RULES_2026-09-02.md`

## Failure S16-P08 — YMB command was emitted as ordinary assistant text instead of an executable assistant code/writing block

### What ChatGPT did wrong

After owner authorization for Step 16, ChatGPT correctly stated the YMB service/mode/case/cost but then emitted the command as ordinary prose text:

`SEARCH_API_V1 {"method":"genSearch","queryText":"панорамные алюминиевые окна","confirmBillable":true}`

That violated the Manual action-surface contract of the installed Yandex Marketing Bridge.

The current owner-directed contract is `extension/docs/MANUAL_CODE_BLOCK_ACTION_CONTRACT_V2_2026-08-17.md`. In Manual ON mode the bridge binds a **local assistant code/writing block** to its local native Copy control, creates a separate adjacent yellow `Яндекс` action, and on that Yandex action click captures the complete block text and sends the complete block to worker/core.

Ordinary assistant prose is not the required Manual action surface and does not provide the intended local block→Copy→`Яндекс` interaction.

### Why it happened

ChatGPT remembered the **protocol payload contract** but failed to re-check the separate **DOM/action-surface transport contract** immediately before issuing the live Manual command.

Canonical causal error:

```text
VALID COMMAND TEXT
WAS INCORRECTLY TREATED AS
VALID MANUAL COMMAND SURFACE
```

and:

```text
PROTOCOL CONTRACT CHECKED
BUT
MANUAL UI/ACTION CONTRACT NOT CHECKED AT EXECUTION BOUNDARY
```

The command string itself matched the GenSearch protocol shape, but it was placed in the wrong assistant output surface.

### Exact current YMB Manual command-surface contract

For Step 16 Manual execution:

```text
assistant standalone code/writing block
-> local native Copy remains native
-> Manual ON creates one separate adjacent yellow `Яндекс` action
-> owner clicks `Яндекс`
-> extension captures the complete block text
-> worker discovers SEARCH_API_V1 marker + JSON
-> strict validation/policy/credential/cost gates
-> provider execution/result lifecycle
```

The GenSearch text inside the block must obey the frozen production command contract:

```text
SEARCH_API_V1 {"method":"genSearch","queryText":"...","confirmBillable":true}
```

Allowed fields are exactly:

```text
method
queryText
confirmBillable
```

### Mandatory non-repeat control

Before every YMB Manual command emitted for the remainder of Step 16, ChatGPT must validate **both** layers:

```text
LAYER 1 — COMMAND PAYLOAD
PREFIX = SEARCH_API_V1
JSON ROOT = object
method = genSearch
queryText = exact authoritative query for current case/attempt
confirmBillable = literal true
no unsupported fields

LAYER 2 — MANUAL ACTION SURFACE
command is inside one standalone assistant code/writing block
command is not emitted only as ordinary prose
block contains the complete executable command text
one current paid interaction per block for the Step-16 sequential workflow
Manual mode stated ON
owner uses the block-local yellow `Яндекс` sibling action, not whole-response Copy
```

If either layer fails:

```text
YMB_COMMAND_READY = false
PROVIDER_EXECUTION_TRANSITION = BLOCKED
```

### Execution-state correction

The malformed presentation in the previous assistant message did **not** constitute evidence that a Yandex Manual block was clicked or that a provider request executed.

Until an actual Bridge result says otherwise:

```text
C15-004_INITIAL_PROVIDER_EXECUTION = NOT_YET_OBSERVED
STEP16_PROVIDER_CALLS_EXECUTED = 0
STEP16_PROVIDER_COST_INCURRED_RUB = 0.0
```

No retry counter is consumed by the plain-text presentation error because no provider interaction is evidenced.

### Mandatory pre-command checklist extension

Append to the parent Step-16 execution checklist:

```text
YMB_MANUAL_ACTION_CONTRACT_RECHECKED = true
COMMAND_IN_STANDALONE_CODE_OR_WRITING_BLOCK = true
LOCAL_BLOCK_ACTION_SURFACE_EXPECTED = true
ORDINARY_PROSE_ONLY_COMMAND = false
WHOLE_RESPONSE_COPY_IS_NOT_MANUAL_TRIGGER = true
```

## Markers

```text
STEP16_S16_P08_COMMAND_SURFACE_FAILURE_RECORDED = true
STEP16_VALID_TEXT_NOT_EQUAL_VALID_MANUAL_SURFACE = true
STEP16_MANUAL_COMMAND_BLOCK_REQUIRED = true
STEP16_YANDEX_LOCAL_SIBLING_ACTION_REQUIRED = true
STEP16_PLAIN_TEXT_COMMAND_FORBIDDEN = true
STEP16_C15_004_STILL_NOT_EXECUTED_UNTIL_BRIDGE_RESULT = true
```
