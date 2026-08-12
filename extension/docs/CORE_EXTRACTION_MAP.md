# CORE EXTRACTION MAP

Date: 2026-08-12
Status: Phase 0 design baseline.

## Purpose

Define exactly how the audited Wordstat Bridge 1.1.5 reference is used to build the unified Yandex Marketing Bridge without losing proven lifecycle behavior and without dragging Wordstat-specific assumptions into future Search/Webmaster/Metrika/Direct adapters.

## Tier A — immutable shared baseline

Copy byte-identically first and keep under hash guard during Phase 1:

```text
shared/composer_send.js
shared/conversation_identity.js
shared/manual_controls.js
shared/proven_writing_block_capture.js
```

These four files are byte-identical to the Business Bridge 2.0.0.22 common reference and have broad runtime coverage in the supplied Wordstat audit.

Phase 1 policy:

- do not rename their globals;
- do not format/rewrite them;
- do not "clean up" selectors or timing;
- add hash tests so any accidental edit fails CI/local tests;
- future modification requires an explicit documented defect and differential acceptance against the frozen reference.

## Tier B — generic lifecycle model requiring controlled genericization

```text
shared/autorun_model.js
```

Reusable semantics:

- run statuses;
- Start phases;
- Delivery phases;
- Pause/Finish decision;
- commit-before-click model;
- confirmation transitions;
- recovery/no-replay decisions;
- prefix cadence/idempotency.

Current coupling:

```text
globalThis.WordstatAutorunModel
```

Phase 1 target:

```text
globalThis.MarketingAutorunModel
```

Recommended migration:

1. preserve exact function semantics;
2. rename only product-specific global identity first;
3. expose temporary `WordstatAutorunModel = MarketingAutorunModel` compatibility alias while migrating worker/content tests;
4. add differential tests asserting old reference inputs produce the same lifecycle decisions;
5. remove compatibility alias only after the Wordstat unified package passes regression/live gate.

## Tier C — service protocol / adapter

```text
shared/wordstat_protocol.js
```

This remains Wordstat-specific.

Target responsibility:

```text
WordstatProtocol
├─ detect/isCommandText
├─ parse/normalize
├─ allowlist methods
├─ build trusted request descriptor
├─ command fingerprint
├─ safe service error payload
└─ WORDSTAT_RESULT_V1 formatting
```

The protocol module must not own generic run state, client binding, autorun permission or cost policy.

Known defect not to inherit:

- audited 1.1.5 package has stale report-format version constant `1.1.1` while package/manifest are `1.1.5`.

Target rule:

- result version must come from one package-wide authoritative version or be proven equal by executable consistency test.

## Tier D — mixed runtime orchestration to separate by responsibility

### service worker

Reference file:

```text
service_worker.js
```

Target conceptual split:

```text
CORE WORKER
├─ storage primitives
├─ lock/single-flight primitives
├─ diagnostics
├─ conversation binding
├─ run persistence
├─ manual-operation persistence
├─ owner/rebind checks
├─ Start lifecycle
├─ command grant lifecycle
├─ Delivery lifecycle
├─ Pause/Resume/Finish
├─ content-ready recovery
├─ credential abstraction
├─ policy engine
├─ job/run metadata
└─ adapter dispatcher

WORDSTAT ADAPTER
├─ Wordstat credential/folder config
├─ Wordstat transport
├─ execute one Wordstat logical operation
├─ Wordstat test connection
└─ Wordstat result/error mapping
```

### content script

Reference file:

```text
content_script.js
```

Target conceptual split:

```text
CORE CONTENT
├─ ChatGPT conversation context
├─ writing-block observer
├─ local Copy ownership/capture
├─ Manual dispatch surface
├─ Autorun watcher
├─ Start composer delivery/reconciliation
├─ result composer delivery/reconciliation
├─ Send/Copy picker fallback
└─ content diagnostics

SERVICE HOOK
├─ protocol signature detector
├─ adapter-specific parse metadata for UI/logs
└─ service-specific UI strings only
```

Important: the content script must not receive API secrets.

### popup

Target conceptual split:

```text
CORE POPUP
├─ bind current conversation
├─ select active service before Start
├─ select current Job ID
├─ Manual / Autorun
├─ Pause / Resume / Finish
├─ run counters/cost/quota status
├─ diagnostics
├─ fallback picker controls
└─ policy editor

SERVICE CONFIG PANEL
└─ credentials/settings/policy for selected adapter
```

## New CORE modules introduced by Yandex Marketing Bridge

These do not exist as independent modules in the reference and must be added gradually in Phase 1:

### `service_registry`

Purpose:

- register known protocol signatures;
- map protocol prefix to service adapter;
- enforce `active_service` match;
- unknown prefix => no external side effect.

Phase 1 registry contains only:

```text
WORDSTAT_API_V1 → wordstat
```

The future signatures may be registered only in their own service phase.

### `policy_model`

Purpose:

- distinguish credential presence from autorun permission;
- request limits;
- cost limits;
- operation-class allowlist;
- service mismatch;
- safe SKIPPED/BLOCKED reasons.

ChatGPT commands cannot mutate policy.

### `job_model`

Purpose:

- trusted local Job ID selected/entered by operator;
- one conversation binding can be associated with current job metadata;
- run records contain Job ID and immutable active service;
- result envelopes can carry non-secret `job_id`/`run_id` provenance.

The Job ID does not authorize or switch client credentials.

### `credential_registry`

Purpose:

- adapter-owned credentials remain isolated;
- common API exposes only capability state (`PRESENT/MISSING/...`) to content/popup/ChatGPT result metadata;
- secret value stays worker-local;
- missing credential => controlled `SKIPPED / NO_CREDENTIALS` before network.

### `cost_ledger_model`

Purpose:

- record estimated billable initiation before execution;
- increment counters only on the correct initiation boundary;
- carry run/job totals;
- return policy evidence to ChatGPT/operator.

Important distinction:

- extension cost guard is a hard technical ceiling based on configured/current policy;
- ChatGPT's separate obligation to verify the current official tariff before each executable paid command remains an operational contract where applicable;
- neither mechanism replaces the other.

## GitHub job evidence boundary

The extension does **not** receive a GitHub token and does not write the repository directly.

Persistence workflow is:

```text
API result
→ durable bridge result delivery to ChatGPT
→ ChatGPT uses connected GitHub to write raw evidence into work/<job_id>/
→ GitHub commit succeeds
→ only then ChatGPT intentionally proceeds to the next paid collection step when reuse/persistence matters
```

This preserves the owner's requirement that collected/paid information survives chat loss while avoiding another secret/API surface inside the extension.

The bridge may stamp `job_id`, `run_id`, `request_id`, service and operation into the result to make deterministic filenames/audit records possible.

## Phase 1 forbidden shortcuts

Do not:

- add Search/Webmaster/Metrika/Direct code during Wordstat phase;
- introduce generic arbitrary URL fetch;
- merge all service credentials into one free-form object controlled by assistant text;
- allow assistant command to select client/account;
- allow assistant command to enable autorun/cost permissions;
- weaken commit/reconciliation/no-replay semantics to simplify code;
- use a global "paid APIs ON" switch;
- perform hidden batch Wordstat requests behind one accepted `WORDSTAT_API_V1` block.

## Extraction success criterion

CORE extraction is successful only when:

1. audited Wordstat behaviors still pass;
2. Tier A hashes remain exact;
3. new generic modules have independent tests;
4. Wordstat protocol/transport is reachable only through the registered Wordstat adapter;
5. a non-Wordstat signature cannot create a network side effect in Phase 1;
6. service/job/policy metadata is generic enough that Phase 2 can add Search without rewriting the accepted lifecycle engine.
