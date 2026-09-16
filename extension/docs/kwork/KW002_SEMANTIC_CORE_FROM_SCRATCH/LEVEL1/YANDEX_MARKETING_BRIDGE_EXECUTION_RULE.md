# KW-002 — Yandex Marketing Bridge execution rule

Status: **ACTIVE / LEVEL-1 EXECUTION AUTHORITY**

This rule governs every KW-002 step that is executed through Yandex Marketing Bridge (YMB), including Wordstat, ordinary Search, deferred Search, GenSearch / AI-search, and any later YMB service used by the roadmap.

It exists to prevent a critical execution-truth failure:

```text
ASSISTANT PRINTED A BRIDGE COMMAND
!=
BRIDGE EXECUTED THE COMMAND
```

A model must never infer execution from its own emitted text.

---

## 1. Mandatory UI execution path

For the current ChatGPT ↔ YMB Manual workflow, a Bridge command must be emitted as one standalone fenced Markdown code block.

The code block must contain exactly one Bridge command:

```text
<BRIDGE_PROTOCOL_PREFIX>
<ONE JSON OBJECT>
```

Requirements:

```text
STANDALONE_MARKDOWN_FENCED_CODE_BLOCK = required
ONE_BRIDGE_COMMAND_PER_CODE_BLOCK = required
PROSE_INSIDE_COMMAND_BLOCK = forbidden
SECOND_BRIDGE_COMMAND_IN_SAME_BLOCK = forbidden
MIXING_BRIDGE_PROTOCOLS_IN_ONE_BLOCK = forbidden
```

The surrounding assistant response may explain the command outside the code block, but the executable block itself must remain clean.

The extension discovers assistant code blocks in the ChatGPT page and renders its Manual action button (`Яндекс`) for an eligible block. Merely displaying the code block does not call the worker or provider.

Execution path:

```text
assistant emits standalone fenced code block
→ YMB content script discovers the assistant code block
→ YMB renders the `Яндекс` action for that block
→ owner/user clicks `Яндекс`
→ content script sends WS_EXECUTE_MANUAL_BLOCK with dialogue identity + exact block text
→ service worker performs preflight
→ only then local/provider action may execute
→ Bridge puts its actual result/report into delivery/outbox
→ actual *_RESULT_V1 response is delivered back to chat
```

No step may skip from “assistant emitted command” directly to “execution happened”.

---

## 2. Execution proof rule

A Bridge action is considered executed only when there is an actual Bridge result for that command.

For current protocols this is a versioned `*_RESULT_V1` report, for example:

```text
WORDSTAT_RESULT_V1
WORDSTAT_BATCH_RESULT_V1
SEARCH_RESULT_V1
SEARCH_ASYNC_BATCH_RESULT_V1
```

The exact result prefix must be verified against the currently accepted YMB source/build when the protocol changes.

Hard truth rule:

```text
COMMAND_BLOCK_RENDERED = preparation only
YANDEX_BUTTON_VISIBLE = command discovered only
YANDEX_BUTTON_CLICKED = execution attempt initiated only
ACTUAL_BRIDGE_RESULT_RECEIVED = execution outcome may be claimed
```

Without the actual result, forbidden claims include:

```text
"запущено"
"выполнено"
"job создан"
"provider request выполнен"
"provider_calls = N"
"результат получен"
```

unless that exact claim is independently proven by another accepted runtime/evidence source.

If no Bridge result has been received, record:

```text
EXECUTION_VERIFIED = false
EXECUTION_OUTCOME = NOT_OBSERVED
PROVIDER_CALLS = not increased from the last proven value
```

Never invent the expected Bridge reply.

---

## 3. Manual preflight requirements

Before clicking/executing a Manual YMB command, verify the applicable current build contract. For the accepted current Manual architecture, at minimum:

```text
current ChatGPT dialogue/tab is bound in YMB
Manual mode is enabled
correct YMB service is active
required credentials are present
credential/folder scope matches any durable job being continued
no conflicting Manual operation is active
no conflicting delivery/outbox operation blocks the command
paused/active Autorun restrictions are respected where applicable
```

If the `Яндекс` button is absent, do not use DevTools, console injection, IndexedDB editing, service-worker hacks or invented direct calls as a substitute.

Normal recovery order:

```text
confirm command is one standalone fenced code block
→ confirm exactly one Bridge command is inside it
→ confirm the correct dialogue is bound
→ confirm Manual mode
→ confirm active service
→ confirm required credentials/scope
→ confirm no active conflicting operation/delivery
→ re-check the currently installed/accepted YMB build contract
```

If still unresolved, stop and investigate YMB itself; do not claim execution.

---

## 4. Provider accounting rule

Always distinguish local Bridge actions from provider calls.

Examples of local/non-provider actions may include protocol parsing, local durable job creation, status reads, local controls and exports. Provider actions include actual Yandex API submit/search/collect calls according to the active protocol.

Never infer billing/call count from the command name alone. Use the actual Bridge result and the accepted protocol/runtime accounting.

For any acquisition cursor/evidence record persist, where applicable:

```text
bridge_protocol
bridge_action
bridge_result_prefix
request_executed
provider_calls
automatic_retry
job_id / operation_id where applicable
actual terminal/local state
```

If `request_executed = UNKNOWN`, preserve UNKNOWN and apply the protocol's no-blind-retry/reconciliation rule.

---

## 5. Deferred Search special rule

Deferred Search is a multi-stage lifecycle. Do not collapse these stages:

```text
start
!=
submit / submitN
!=
collect / collectN / collectReady
!=
status / itemsPage
!=
exportPage
```

`start` may be local-only while later submit/collect actions may touch provider endpoints. The current accepted build/source defines the actual accounting.

A multi-item deferred job does not mean one provider batch request or one billed request. Preserve per-item operation identity and the protocol's request/cost accounting.

No hidden polling, hidden retry or implicit execution may be assumed. If the accepted build says collection is explicit, the roadmap executor must explicitly issue the next collection command as a new clean Bridge code block and wait for the actual result.

---

## 6. Wordstat / Search / GenSearch command discipline

Before emitting a command:

```text
1. identify required YMB service and Manual/Autorun mode;
2. identify exact protocol prefix from accepted current YMB source/build;
3. validate the JSON fields against that protocol;
4. emit exactly one command in one standalone fenced code block;
5. state outside the block what the command is intended to do, when useful;
6. do not claim execution yet;
7. wait for the actual Bridge result;
8. reconcile request_executed/provider_calls/result payload;
9. persist required evidence/readback before the next action when the step requires it.
```

Never put explanatory prose, bullets, a second command or a second protocol inside the same executable block.

---

## 7. Roadmap integration

This Level-1 authority is mandatory for every roadmap step that uses YMB/provider execution.

At minimum it applies to:

```text
STEP 03 — primary Wordstat acquisition
STEP 05 — targeted expansion when provider acquisition is required
STEP 06 — current Yandex organic competitor discovery
STEP 08 — competitor-derived Wordstat expansion
STEP 12 — current ordinary Yandex Search evidence acquisition
STEP 16 — AI-search evidence acquisition
```

It also applies to any re-acquisition, corrective acquisition, credential check or later provider-backed substep performed through YMB.

Each concrete job may add a version-pinned execution contract, but a job-specific contract may not weaken this Level-1 truth rule.

---

## 8. Required state language

Use these states explicitly when material:

```text
COMMAND_PREPARED
COMMAND_BLOCK_RENDERED
EXECUTION_ATTEMPT_INITIATED
BRIDGE_RESULT_RECEIVED
PROVIDER_EXECUTED_TRUE
PROVIDER_EXECUTED_FALSE
PROVIDER_EXECUTION_UNKNOWN
EVIDENCE_PERSISTED
REMOTE_READBACK_PASS
```

Do not merge preparation, action attempt, provider execution, evidence persistence and project completion into one status.

---

## 9. Anti-regression acceptance test

Before advancing after any Bridge command, answer all of these from evidence, not expectation:

```text
Was the command in a standalone fenced code block?
Was there exactly one Bridge command in that block?
Was it actually triggered through YMB?
What exact Bridge result was received?
What does request_executed say?
How many provider_calls does the actual result prove?
What job/operation identity was returned, if applicable?
Was the required evidence persisted/read back?
Is the next action actually released?
```

If any required answer is unknown, stop at that boundary rather than inventing the missing state.

---

## Marker

```text
KW002_YMB_EXECUTION_AUTHORITY = LEVEL1/YANDEX_MARKETING_BRIDGE_EXECUTION_RULE.md
KW002_YMB_COMMAND_SURFACE = STANDALONE_MARKDOWN_FENCED_CODE_BLOCK
KW002_YMB_ONE_COMMAND_PER_BLOCK = true
KW002_YMB_EXECUTION_TRIGGER = USER_CLICKS_YANDEX_ACTION
KW002_YMB_EMITTED_COMMAND_IS_EXECUTION = false
KW002_YMB_RESULT_REQUIRED_FOR_EXECUTION_CLAIM = true
KW002_YMB_NO_RESULT_NO_EXECUTION_CLAIM = true
KW002_YMB_DEVTOOLS_BYPASS_FORBIDDEN = true
```
