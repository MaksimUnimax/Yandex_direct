# SPECIFICATION v0.4 — Yandex Marketing Bridge

Status: current technical specification.  
Updated: 2026-08-18.

## 1. Product boundary

One Chrome/Chromium extension: **Yandex Marketing Bridge**.

Runtime architecture:

```text
CORE
├─ writing/code-block structural capture
├─ manual independent sibling Yandex action surface
├─ autorun state machine
├─ conversation identity/binding
├─ owner-tab protection
├─ composer delivery
├─ protocol detector/router
├─ credential storage/capability
├─ policy/cost guards
├─ RUN accounting
├─ durable pending-result/error delivery
├─ recovery/reconciliation
├─ settings export/import
└─ diagnostic event log

ADAPTERS
├─ Wordstat      [Phase 1]
├─ Search        [blocked]
├─ Webmaster     [blocked]
├─ Metrika       [blocked]
└─ Direct        [blocked]
```

The audited Wordstat Bridge 1.1.5 and other proven bridge mechanisms remain behavior references where they are compatible with current production ChatGPT DOM and the current governed contracts.

## 2. GitHub is outside extension runtime

The extension MUST NOT require or implement:

```text
job_id
GitHub token
GitHub API
repository/branch/commit
work/<job_id>/
```

No API command may be rejected because a GitHub/order Job ID is absent.

GitHub order persistence is an external ChatGPT/development workflow:

```text
Bridge delivers result to ChatGPT
→ ChatGPT may persist evidence to GitHub work/<job_id>/
```

This separation is mandatory.

## 3. Protocol routing

No generic executable router protocol exists.

```text
WORDSTAT_API_V1   → Wordstat adapter
SEARCH_API_V1     → Search adapter
WEBMASTER_API_V1  → Webmaster adapter
METRIKA_API_V1    → Metrika adapter
DIRECT_API_V1     → Direct adapter
```

Only adapters registered for the accepted phase may execute. Phase 1 registers **Wordstat only**. Unknown/future prefixes cause no provider/network side effect.

## 4. One RUN = one SERVICE

Autorun RUN has immutable `active_service` until Finish/Stop.

Minimum runtime fields:

```text
run_id
conversation_key
owner_tab_id
active_service
permission_profile
status
sequence
requests_attempted
requests_executed
requests_skipped
estimated_cost_rub
created_at
updated_at
last_error
```

`job_id` is explicitly absent.

Recommended states retain reference semantics:

```text
STOPPED
STARTING
WAITING_COMMAND
REQUESTING
DELIVERING
PAUSED
ERROR
```

Recoverable ordinary failures should return toward `WAITING_COMMAND` when safe instead of killing Autorun.

## 5. Manual Surface v2 / Autorun semantics

Manual is a **DOM/action-surface mode**, not a page-side command pre-validator.

Required Manual invariants:

- Manual OFF: ordinary local Copy remains native and Bridge-owned decoration/action is absent;
- Manual ON + confirmed bound conversation: every **uniquely resolved local Copy belonging to a supported assistant writing/code block** remains native and gets exactly one separate adjacent Yandex sibling action;
- the sibling is visibly Yandex-yellow with a visible `Яндекс` label and `data-ymb-manual-action="true"`;
- visual arming is **independent of block contents**: plain text, arbitrary JSON, malformed material, valid protocol and multi-command content are all decorated identically when structural binding is valid;
- content/page code must not prefilter by protocol marker, JSON validity, allowed service/method, credentials, policy, price or provider availability;
- generic assistant-level whole-response Copy is excluded and remains native;
- ambiguous local Copy mapping fails closed and remains native/unarmed;
- the smallest unambiguous structural locality is used; no cross-block/cross-assistant binding;
- native Copy behavior remains intact and native Copy never dispatches a Bridge action;
- only the separate sibling Yandex action dispatches Manual and submits the **complete bound block** to worker/core;
- worker/core owns command discovery, strict validation, routing, policy, credentials, cost and controlled no-command/malformed errors;
- DOM mutations/rerenders are rescanned; decoration is idempotent; disabling Manual restores the exact native surface; re-enable decorates once again;
- Manual and Autorun remain mutually controlled according to the current runtime contract;
- exactly-once fences use command/assistant/delivery identities;
- owner-tab and conversation binding are fail-closed;
- composer text is never silently overwritten;
- irreversible request/Send boundaries are durably fenced;
- billable/irreversible initiation is never blindly retried after uncertain outcome.

Manual delivery invariant: after a committed Send, the operation remains fenced
until the matching sent user-turn confirmation exists. Runtime reconciliation
may be bounded and confirmation-only; it must not click Send again, replay
`WS_EXECUTE_MANUAL_BLOCK`, or replay provider/API initiation. Confirmation makes
the operation terminal/completed and admits the next Manual action. An
unresolved committed boundary remains fenced.

The current factual ChatGPT family includes assistant sections/message containers with local `PRE` blocks and readonly CodeMirror-like bodies plus exactly one local Copy button in the same block. Current and legacy supported adapters may coexist, but unknown/ambiguous DOM must fail closed.

## 6. Manual budget semantics

A Manual click authorizes processing of the clicked block; whether it contains an executable command is determined by worker/core after admission.

If there is **no active paused RUN**, standalone Manual has no invented JOB budget.

If Manual is used while the current Autorun RUN is **PAUSED**, any executable request admitted from that block must use the same RUN request/cost counters and ceilings:

```text
Pause RUN
→ Manual block click
→ worker discovers command
→ same RUN budget
```

Switching to Manual must not bypass an active RUN limit.

## 7. Credential model

Credentials are local trusted operator data.

Minimum capability states:

```text
PRESENT
MISSING
INVALID_OR_EXPIRED
NO_ACCESS
```

Credential presence is separate from Manual/Autorun permission and separate from Manual visual arming.

Missing credentials for an executable command produce a controlled result/error with zero external request, for example:

```text
status = SKIPPED
reason = NO_CREDENTIALS
request_executed = false
```

Missing credentials do not terminate the whole workflow.

Credentials must not appear in ordinary ChatGPT executable commands, result envelopes, error/debug reports or GitHub.

## 8. Storage compatibility

Phase 1 must preserve proven Wordstat storage continuity, including existing keys such as:

```text
wsmb_api_key
wsmb_folder_id
wsmb_auto_send
wsmb_conversation_bindings
wsmb_manual_modes
wsmb_auto_runs
wsmb_report_prefix_configs
wsmb_auto_start_prompts
wsmb_send_button_profile
wsmb_copy_button_profiles
```

In-place unpacked upgrade + Reload must retain those values through normal Chrome extension storage continuity.

## 9. Export settings / Import settings

The popup must provide explicit settings backup/restore.

Backup is versioned and intentionally secret-bearing:

```text
format
backup_version
settings_schema_version
exported_at
extension_version
extension_id
contains_secrets = true
settings_sha256
settings
```

`settings_sha256` is canonical SHA-256 over the settings payload.

Import requirements:

- supported format/version only;
- checksum verification before mutation;
- reject tampered backup;
- validate credentials/settings;
- merge compatible state;
- create a local migration rollback backup;
- preserve active RUN records;
- preserve binding/service/manual-mode safety state for active RUN/manual operations;
- never import active execution transactions from the backup.

The exported file itself contains secrets and must be treated like a credential file.

## 10. Always-on ChatGPT error delivery

Every detected extension failure that can be associated with a bound ChatGPT conversation must be delivered automatically to that conversation.

This includes:

- Manual worker/core discovery/validation failures;
- Autorun failures;
- credential/policy rejection where represented as error rather than result;
- network/runtime errors;
- watcher/content errors;
- result/error delivery errors;
- recovery/reconciliation problems.

Canonical error signature:

```text
YMB_ERROR_V1
```

Minimum useful metadata:

```text
bridge
version
service
channel
stage
code
message
recoverable
request_executed
automatic_retry
run_id
operation
autorun_continues
timestamp
```

No secrets.

A Manual click on a structurally eligible block that contains no supported executable command must not silently disappear; worker/core must return a controlled explicit result/error with `request_executed:false` and zero provider request.

## 11. Debug Mode

Debug Mode controls **additional diagnostics only**.

```text
Debug OFF → error still automatically goes to ChatGPT
Debug ON  → same error + extra redacted diagnostic events
```

Debug Mode must never be required for error delivery.

Redaction must exclude at minimum:

- API key;
- OAuth/access/refresh tokens;
- Authorization header;
- passwords/cookies;
- complete secret backup contents.

## 12. Durable result/error delivery

Result/error delivery uses a worker-owned durable outbox lifecycle:

```text
claimed
→ staged in composer
→ committed before Send click
→ one Send click
→ confirmed
```

If worker/content reloads after an irreversible boundary, recovery is reconciliation-only. It must not repeat Send blindly and must never repeat the original Yandex request.

A completed provider result that cannot be delivered before Send commit must remain durably recoverable without replaying provider initiation.

## 13. Wordstat Phase 1 policy

Supported methods:

```text
getTop
getDynamics
getRegionsDistribution
getRegionsTree
```

Operator controls:

- Autorun enabled;
- Manual enabled;
- allowed methods;
- max requests per RUN;
- max estimated RUB per RUN;
- tariff snapshot/source metadata.

ChatGPT cannot raise these limits by command.

Before an Autorun billable initiation, Bridge reserves the RUN budget before the external initiation. Conservative over-count after a crash is acceptable; under-count that enables an unsafe duplicate is not.

All future services remain execution-disabled during Phase 1.

## 14. Result envelope

Service-specific signatures remain:

```text
WORDSTAT_RESULT_V1
SEARCH_RESULT_V1
WEBMASTER_RESULT_V1
METRIKA_RESULT_V1
DIRECT_RESULT_V1
```

Wordstat common metadata includes where applicable:

```text
bridge
version
service
operation
request_id
run_id
status
reason
cost_estimate
policy
command
http_status
elapsed_ms
result
request_executed
automatic_retry
```

`job_id` is not a Bridge result field.

Successful sent requests must explicitly report `request_executed:true`; pre-network validation/credential/policy skips report `false`; irreversible unknown outcomes report `UNKNOWN` and are not blindly retried.

## 15. HTTP/error semantics

One accepted executable command = one logical external initiation.

- HTTP 2xx → normal result.
- HTTP 4xx/5xx received from the one request → deliver ERROR result/evidence; do not automatically replay.
- validation/no credential/policy limit before fetch → zero request.
- timeout/network/session-loss where initiation outcome is uncertain → report `request_executed = UNKNOWN`, `automatic_retry = false`; fence identical retry until safe reconciliation/operator/assistant decision.
- malformed/no-command Manual blocks are handled before provider initiation and produce zero provider request.

## 16. Visual feedback

Reference-compatible visible feedback is required in ChatGPT/popup.

Manual Surface v2 visual rule:

```text
Manual OFF → supported local Copy stays native
Manual ON + confirmed conversation + unique supported local binding
           → yellow + visible Яндекс
```

This visual state is **not** proof that block content is a valid command. Command validity is a worker/core concern after the click.

Request initiation/response/error feedback must remain explicit and reference-consistent. A valid API block must not fail silently.

## 17. GitHub order workspace workflow

Outside the extension, project workflow may use:

```text
work/<job_id>/
```

for raw evidence, normalized data, analysis, deliverables and logs.

No secret values may be stored there.

This workspace is not a prerequisite for Bridge execution and is not accessed by the extension.

## 18. Direct risk profiles

Future Direct implementation remains separated into at least:

```text
DIRECT_READ
DIRECT_DRAFT_WRITE
DIRECT_LIVE_WRITE
```

No unrestricted live-write Autorun.

## 19. Development and pre-delivery testing contract

Testing has two deliberately different modes.

### 19.1 Development mode

While code is being changed, run only what the change requires:

- focused tests for changed behavior;
- directly affected dependency/regression tests;
- changed-line/branch execution where appropriate;
- syntax/static checks needed by the touched surface.

Do **not** run the complete product regression campaign after every small edit.

### 19.2 Mandatory pre-delivery mode

Immediately before a frozen working build/candidate is handed to the owner, Codex must execute the permanent living gate:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
```

Requirements:

- all enabled Codex-capable functional tests run in **one complete campaign** against the exact candidate to be handed off;
- any mandatory FAIL blocks handoff;
- after a production fix, focused tests are used during development, then the **entire pre-delivery gate reruns from the beginning** on the newly frozen candidate;
- new/changed functionality must add/update gate coverage;
- removed functionality removes obsolete gate coverage only in the same governed functional removal;
- tests are never deleted merely because they fail;
- before each full run, product/spec/source surfaces are compared against the gate registry and missing Codex-capable coverage itself is a FAIL;
- deterministic packaging and source↔package identity are part of pre-delivery acceptance;
- controlled CfT/Puppeteer evidence is never relabeled as owner real-profile/live evidence.

### 19.3 Phase ordering

```text
one service
→ implement/fix with focused tests
→ freeze working candidate
→ full Codex pre-delivery regression gate
→ exact package/identity PASS
→ remaining irreducible real-profile/live acceptance
→ phase PASS
→ next service
```

Search remains blocked until Wordstat Phase 1 live acceptance passes.
