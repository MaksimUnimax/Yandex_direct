# SPECIFICATION v0.2 — Yandex Marketing Bridge

Status: current technical specification.
Updated: 2026-08-12.

## 1. Product boundary

One Chrome/Chromium extension: **Yandex Marketing Bridge**.

Runtime architecture:

```text
CORE
├─ writing-block capture
├─ manual native-Copy integration
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

The audited Wordstat Bridge 1.1.5 and proven Business Bridge 2 mechanisms are the behavior references. Proven common mechanisms are preserved unless a documented incompatibility requires change.

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

Only adapters registered for the accepted phase may execute. Phase 1 registers **Wordstat only**. Unknown/future prefixes cause no network side effect.

## 4. One RUN = one SERVICE

Autorun RUN has immutable `active_service` until Finish.

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
ERROR      # only when a truly terminal/suspended condition requires it
```

Recoverable ordinary failures should return toward `WAITING_COMMAND` when safe instead of killing Autorun.

## 5. Manual / Autorun reference semantics

Required invariants:

- native local Copy remains native Copy;
- generic assistant-level Copy Response is never an API trigger;
- Manual and Autorun are mutually controlled;
- watcher accepts only stable new assistant writing/code blocks;
- exactly-once fences use command/assistant/delivery identities;
- owner-tab and conversation binding are fail-closed;
- composer text is never silently overwritten;
- Start and result/error Send are committed before the one browser click where reference requires it;
- recovery after a committed click is reconciliation-only;
- billable/irreversible initiation is never blindly retried after uncertain outcome.

## 6. Manual budget semantics

Manual Copy is an explicit per-command operator authorization.

If there is **no active paused RUN**, standalone Manual has no invented JOB budget.

If Manual is used while the current Autorun RUN is **PAUSED**, the request must use the same RUN request/cost counters and ceilings:

```text
Pause RUN
→ Manual Copy
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

Credential presence is separate from Manual/Autorun permission.

Missing credentials for an executable command produce a controlled result with zero external request, for example:

```text
status = SKIPPED
reason = NO_CREDENTIALS
request_executed = false
```

Missing credentials do not terminate the whole workflow.

Credentials must not appear in ordinary ChatGPT executable commands, result envelopes, error/debug reports or GitHub.

## 8. Storage compatibility

Phase 1 must preserve proven Wordstat storage continuity, including the existing keys used by the reference such as:

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

This applies to:

- Manual;
- Autorun;
- command parsing/validation;
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

## 12. Durable error delivery

Error delivery uses a worker-owned durable outbox lifecycle analogous to proven result delivery:

```text
claimed
→ staged in composer
→ committed before Send click
→ one Send click
→ confirmed
```

If the worker/content reloads after commit, recovery is reconciliation-only. It must not repeat Send blindly and must never repeat the original Yandex request.

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

## 15. HTTP/error semantics

One accepted command = one logical external initiation.

- HTTP 2xx → normal result.
- HTTP 4xx/5xx received from the one request → deliver ERROR result/evidence; do not automatically replay.
- validation/no credential/policy limit before fetch → zero request.
- timeout/network/session-loss where initiation outcome is uncertain → report `request_executed = UNKNOWN`, `automatic_retry = false`; fence identical retry until reconciliation/operator/assistant chooses a safe path.

## 16. Visual feedback

Reference-compatible visible feedback is required in the ChatGPT page/popup.

At minimum, user must see clear state around request initiation/response/error. Wordstat-local Copy remains Yandex-yellow reference style where supported by current DOM.

A valid API block must not fail silently.

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

## 19. Development gate

Strict order:

```text
one service
→ implementation
→ source tests
→ exact packaged tests
→ source/package identity
→ syntax/static checks
→ Chromium load smoke
→ controlled real Chrome + production ChatGPT acceptance
→ PASS
→ next service
```

Search remains blocked until Wordstat 0.1.1 production live acceptance passes.
