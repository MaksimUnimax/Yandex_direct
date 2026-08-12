# SPECIFICATION v0.1 — Yandex Marketing Bridge

Status: initial architecture specification.
Date: 2026-08-12.

## 1. Product architecture

Create one Chrome/Chromium extension: **Yandex Marketing Bridge**.

Persistent modules:

```text
CORE
├─ writing-block capture
├─ manual Copy integration
├─ autorun state machine
├─ conversation identity/binding
├─ owner-tab protection
├─ composer delivery
├─ protocol detector/router
├─ credential abstraction
├─ policy/cost/quota engine
├─ run/job accounting
├─ pending-result safety
└─ audit/event log

ADAPTERS
├─ Wordstat
├─ Search / SERP
├─ Webmaster
├─ Metrika
└─ Direct
```

The current Wordstat Bridge 1.1.5 is the reference baseline for CORE behavior. New services are added incrementally without replacing proven mechanisms unless a documented incompatibility requires it.

## 2. Protocol routing

There is no generic executable `ROUTER_API` protocol.

The router identifies the target adapter from the service protocol signature of the extracted executable block:

```text
WORDSTAT_API_V1   → WordstatAdapter
SEARCH_API_V1     → SearchAdapter
WEBMASTER_API_V1  → WebmasterAdapter
METRIKA_API_V1    → MetrikaAdapter
DIRECT_API_V1     → DirectAdapter
```

Unknown blocks are ignored and cause no network side effect.

Service-specific protocol parsing and allowlisting remain inside the corresponding adapter/protocol module.

## 3. One RUN = one SERVICE

A run record contains immutable `active_service`.

After `Start`, the active service cannot be changed until `Finish`.

If the assistant emits a valid command for another service during the run, the bridge must not execute it. It returns a safe skipped/blocked result such as:

```text
status = SKIPPED
reason = SERVICE_NOT_ACTIVE
active_service = <current service>
```

Switching service requires:

```text
Finish current RUN
→ operator selects another service
→ Start new RUN
```

Multiple service runs can belong to the same JOB.

## 4. Manual and Autorun modes

Preserve proven reference semantics:

- local native Copy remains native Copy;
- generic assistant-level Copy Response is never an API trigger;
- manual and autorun execution are mutually controlled;
- autorun watches stable new assistant writing/code blocks;
- exactly-once fences are based on assistant turn / command fingerprint / transaction identity;
- Pause, Resume and Finish are conversation scoped;
- user composer is never silently overwritten;
- Send is performed once without blind click retry loops;
- irreversible/paid operations are never blindly retried after uncertain worker state.

## 5. Credential model

Credentials are independent per adapter or credential family.

Minimum states:

```text
PRESENT
MISSING
INVALID_OR_EXPIRED
NO_ACCESS
```

Absence of credentials for one service does not disable other services or the JOB.

A command that requires missing credentials must produce a safe result:

```text
status = SKIPPED
reason = NO_CREDENTIALS
```

The pipeline continues on available evidence.

Credentials must never appear in:

- ChatGPT executable commands;
- result envelopes;
- GitHub repository;
- logs committed to `work/`;
- packaged extension artifacts.

## 6. Operator-controlled Autorun permissions

Credential presence and Autorun permission are separate concepts.

For every service/operation class the operator controls:

- enabled in autorun: yes/no;
- allowed operation classes;
- request limit per run;
- request limit per job where relevant;
- money limit per run/job for billable APIs;
- quota/unit reserve where the API uses non-monetary quotas;
- risk profile for write operations.

ChatGPT commands cannot alter these policy values.

## 7. Paid request guard

Before any billable initiation, PolicyEngine must evaluate at minimum:

```text
credential available
AND service is active
AND autorun enabled
AND operation is allowlisted
AND operation class enabled
AND request_count + expected_requests <= request_limit
AND spent_cost + estimated_cost <= cost_limit
```

If not allowed, do not call the external API and return a safe result:

```text
status = SKIPPED
reason = COST_LIMIT | REQUEST_LIMIT | AUTORUN_DISABLED | OPERATION_DISABLED
```

Expensive operation classes must have separate toggles. A broad `Search API enabled` switch is insufficient when deferred, synchronous, generative and other operations have materially different prices.

## 8. Cost evidence

For paid APIs maintain a per-run and per-job cost ledger with:

- service;
- operation;
- command/transaction id;
- tariff snapshot/source metadata when available;
- estimated cost before execution;
- actual charged cost if the API exposes it;
- timestamp;
- cumulative run cost;
- cumulative job cost.

Paid raw data must be persisted into the current order workspace before it is considered safely reusable.

## 9. Quota guard

Non-monetary APIs still require guards.

Examples of policy concepts:

- Direct units reserve;
- Metrika request/rate quotas;
- Webmaster unit/export quota;
- Search deferred submission/result quotas.

Quota exhaustion should stop only the affected service/run or operation class, not destroy the entire JOB.

## 10. Logical operation vs HTTP request

Global invariant:

**One accepted ChatGPT command = one logical external operation.**

If an official API requires documented polling to retrieve the result of that same submitted operation, polling may occur inside the same transaction.

The bridge must distinguish:

- billable/side-effect initiation;
- status/result polling.

An initiation must not be repeated automatically after an uncertain outcome.

## 11. Result envelopes

Each service keeps its own result signature:

```text
WORDSTAT_RESULT_V1
SEARCH_RESULT_V1
WEBMASTER_RESULT_V1
METRIKA_RESULT_V1
DIRECT_RESULT_V1
```

Common metadata should include where applicable:

```text
bridge
version
service
operation
request_id / transaction_id
run_id
job_id
status
reason
http_status
elapsed_ms
cost_estimate
quota metadata
result
```

No credentials may be included.

## 12. JOB model

A Kwork/customer order is represented by a JOB.

Minimum fields:

```text
job_id
client_alias
type
created_at
status
workspace_path
```

A JOB may contain many service-specific runs.

## 13. RUN model

Minimum fields:

```text
run_id
job_id
conversation_key
owner_tab_id
active_service
permission_profile
status
sequence
requests_attempted
requests_executed
requests_skipped
estimated_cost
actual_cost_if_known
created_at
updated_at
last_error
```

Recommended state machine:

```text
STOPPED
→ STARTING
→ WAITING_COMMAND
→ VALIDATING
→ EXECUTING
→ POLLING (only when required)
→ DELIVERING
→ WAITING_COMMAND

PAUSED / FINISHED / ERROR as controlled terminal or suspended states.
```

## 14. Direct risk profiles

Direct is divided into at least three permission profiles:

### DIRECT_READ
Read campaigns, groups, ads, keywords, settings, reports and search-query performance.

### DIRECT_DRAFT_WRITE
Create or modify only operations explicitly accepted as safe draft/pre-launch preparation by the implementation spec. Every write must be followed by read-back verification.

### DIRECT_LIVE_WRITE
Operations that can affect active advertising, spending, moderation, live bids/strategies, suspension/resume, deletion/archive or other production state.

`DIRECT_LIVE_WRITE` is not unrestricted autorun. It requires an explicit operator-approved changeset/transaction gate and post-write verification.

## 15. GitHub workspace integration

Repository layout:

```text
extension/
  docs/
  reference/
  src/
  tests/

work/
  <job_id>/
```

The bridge/development workflow must treat GitHub `work/<job_id>/` as durable job evidence, not as optional export.

No secret values may be persisted there.

## 16. Order workspace minimum contents

Each active job should be able to contain:

```text
work/<job_id>/
  JOB.md
  manifest.json
  context/
  raw/
    wordstat/
    search/
    webmaster/
    metrika/
    direct/
  normalized/
  analysis/
  deliverables/
  logs/
    runs/
    cost-ledger/
```

Only directories actually used by the order need to contain files.

## 17. Paid evidence persistence invariant

After a paid API result is successfully received, it must be written to the job workspace as raw evidence before the workflow intentionally discards the only local/runtime copy.

The purpose is to prevent duplicate paid collection caused by:

- chat loss;
- browser reload;
- extension restart;
- context-window loss;
- operator switching conversations.

A previously persisted paid result should be reused when its parameters and freshness requirements match the current need.

## 18. Order close lifecycle

After the customer accepts/delivery is complete:

1. verify final deliverables exist;
2. verify required working evidence is committed;
3. mark JOB complete;
4. delete `work/<job_id>/` from the current repository tree as the normal cleanup action.

Normal Git deletion does not erase previous Git history. Full historical purge is a separate exceptional procedure and is not implied by ordinary order cleanup.

## 19. Security invariants

- No arbitrary URL transport.
- Hardcoded/validated service endpoints and methods.
- No secret material in ChatGPT.
- No secret material in GitHub.
- Content script must not receive API secrets when avoidable.
- Client/account binding must come from trusted local operator configuration, not assistant text.
- ChatGPT cannot switch client/account by command.
- ChatGPT cannot raise cost/quota permissions.
- No blind retry of irreversible or billable initiation.
- Unknown blocks do nothing.
- Service mismatch does nothing externally.

## 20. Development gate

One new service is developed and accepted at a time.

No next service starts until the current phase has source tests, packaged tests and controlled live Chrome/ChatGPT acceptance PASS, with regression PASS for all previously accepted services.
