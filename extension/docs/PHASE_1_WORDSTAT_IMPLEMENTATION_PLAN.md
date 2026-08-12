# PHASE 1 — WORDSTAT + UNIFIED CORE IMPLEMENTATION PLAN

Date: 2026-08-12
Status: READY TO IMPLEMENT after Phase 0 reference audit.

## Goal

Produce the first installable **Yandex Marketing Bridge** package with exactly one executable service:

```text
active_service = wordstat
```

It must preserve the audited Wordstat lifecycle behavior while introducing the generic architecture required for later services.

No Search/Webmaster/Metrika/Direct execution is implemented in this phase.

## 1. Source bootstrap

Start from the owner-supplied audited Wordstat 1.1.5 artifact, not from a blank extension.

Copy reference-common modules byte-identically:

```text
shared/composer_send.js
shared/conversation_identity.js
shared/manual_controls.js
shared/proven_writing_block_capture.js
```

Import the reference Wordstat production files/tests only as migration input; the frozen reference itself remains under `extension/reference/` and is never edited.

## 2. Product identity

New product name:

```text
Yandex Marketing Bridge — ChatGPT ↔ Yandex
```

Initial unified version should start at a new product version namespace (recommended `0.1.0`) rather than pretending to be Wordstat Bridge `1.1.5`.

One authoritative version must feed/validate:

- manifest;
- package;
- runtime result envelopes;
- popup display;
- diagnostics.

Add an executable version-consistency regression test from the beginning.

## 3. Phase 1 source layout

Recommended:

```text
extension/src/
├─ manifest.json
├─ package.json
├─ popup.html
├─ popup.css
├─ popup.js
├─ content_script.js
├─ service_worker.js
├─ shared/
│  ├─ composer_send.js                 # frozen hash
│  ├─ conversation_identity.js         # frozen hash
│  ├─ manual_controls.js               # frozen hash
│  ├─ proven_writing_block_capture.js  # frozen hash
│  ├─ autorun_model.js                 # genericized lifecycle model
│  ├─ service_registry.js              # new
│  ├─ policy_model.js                  # new
│  ├─ job_model.js                     # new
│  └─ cost_ledger_model.js             # new
└─ adapters/
   └─ wordstat/
      ├─ protocol.js
      └─ transport.js (or worker-owned adapter functions if separation is clearer)
```

Avoid premature module fragmentation when it weakens reference traceability. The exact physical split of large worker/content files may be incremental, but logical service boundaries must be testable.

## 4. Service registry in Phase 1

Only one registered executable signature:

```text
WORDSTAT_API_V1 → wordstat
```

Unknown signatures:

```text
no dispatch
no credential read
no network
```

If a future-looking block such as `SEARCH_API_V1` appears during Phase 1, it is non-executable.

## 5. RUN contract

At Start, operator selects/has selected:

```text
job_id
active_service = wordstat
permission profile
```

These become trusted run metadata.

`active_service` is immutable until Finish.

A run cannot switch service based on assistant text.

Minimum run counters:

```text
requests_attempted
requests_executed
requests_skipped
estimated_cost_rub
sequence
```

Preserve Start/Request/Delivery/Pause/Finish durable lifecycle from reference.

## 6. Job ID and GitHub workspace

Popup should provide a non-secret current Job ID field or equivalent trusted binding control.

Validation recommendation:

```text
[A-Za-z0-9][A-Za-z0-9._-]{0,119}
```

No path separators or traversal.

The operator/ChatGPT creates the actual repository directory separately:

```text
work/<job_id>/
```

The bridge stamps `job_id` and `run_id` into results/diagnostics, but does not hold GitHub credentials.

## 7. Credential semantics

Wordstat requires its own locally stored credential/folder configuration.

Phase 1 changes from old behavior:

- missing API credential must be representable as capability `MISSING`;
- Manual explicit request may surface a clear pre-network error;
- Autorun command must return a controlled safe result/status and not destroy the Job;
- `NO_CREDENTIALS` is not a reason to mutate another service or search for another credential automatically.

Content script never receives the secret key.

## 8. Policy semantics

Separate:

```text
credential available
≠
autorun enabled
```

Wordstat operator policy contains at minimum:

```text
autorun_enabled
allowed_methods
max_requests_per_run
max_cost_rub_per_run
```

Recommended additional fields from the beginning:

```text
max_requests_per_job
max_cost_rub_per_job
configured_tariff_snapshot
configured_tariff_checked_at
```

ChatGPT command has no method/field that changes these values.

## 9. Wordstat cost model

The old reference relies operationally on ChatGPT checking current official pricing before each executable command. Preserve that instruction contract.

The unified extension adds an independent hard technical guard.

For Phase 1:

- operation cost is calculated from operator-controlled/configured tariff policy;
- extension shows run/job estimated spend;
- request is rejected before fetch if the configured hard request/cost limit would be exceeded;
- tariff source/timestamp may be shown in popup and result metadata;
- assistant cannot edit policy through executable protocol.

A stale local tariff configuration must never result in unlimited spend: request-count limits remain an independent ceiling.

## 10. Wordstat execution contract

Preserve:

```text
one accepted WORDSTAT_API_V1 block
→ at most one billable Wordstat initiation
```

No batch of multiple phrases hidden behind one command.

No automatic retry after HTTP/network/worker uncertainty.

Supported methods remain:

```text
getTop
getDynamics
getRegionsDistribution
getRegionsTree
```

`getRegionsTree` remains non-paid according to current service semantics but still passes normal method/policy validation.

## 11. Result contract

Keep signature:

```text
WORDSTAT_RESULT_V1
```

Add generic provenance fields where safe:

```text
bridge: yandex-marketing-bridge
version
service: wordstat
operation
request_id
run_id
job_id
status
reason
http_status
elapsed_ms
cost_estimate
policy/counter metadata
command
result
```

No API key/folder credential secret.

Existing downstream Wordstat data parsing should remain straightforward.

## 12. Safe SKIP/BLOCK results

Before network, common reasons include:

```text
NO_CREDENTIALS
AUTORUN_DISABLED
SERVICE_NOT_ACTIVE
OPERATION_DISABLED
REQUEST_LIMIT
COST_LIMIT
INVALID_COMMAND
```

Important semantic split:

- validation/policy rejection = zero external request;
- Yandex HTTP error after initiation = external request occurred and must be recorded as such;
- uncertain worker loss during request = `REQUEST_OUTCOME_UNKNOWN_NO_RETRY` behavior preserved.

## 13. Manual mode

Preserve reference behavior:

- operator explicitly enables Manual for bound conversation;
- local native Copy remains native Copy;
- supported recent/new writing blocks may be visually armed;
- actual clicked block is parsed only after local Copy ownership is established;
- non-Wordstat block performs only normal Copy;
- generic turn-level Copy is excluded;
- durable worker-owned manual operation persists from request claim through delivery completion;
- disabling Manual does not erase an already in-flight durable manual operation.

## 14. Autorun

Preserve:

- explicit operator Start confirmation;
- bound conversation requirement;
- stable assistant-block watcher;
- exactly one atomic command grant;
- worker-owned delivery single-flight;
- Start commit-before-click;
- Delivery commit-before-click;
- no second click after committed state;
- Pause immediate/deferred semantics;
- Resume fresh baseline;
- Finish immediate/deferred semantics;
- recovery/no-replay behavior.

New Phase 1 gate before command execution:

```text
protocol detected
→ registry says wordstat
→ active_service == wordstat
→ credential capability
→ autorun permission
→ method allowlist
→ cost/request policy
→ atomic execution grant
→ Wordstat adapter
```

## 15. GitHub evidence workflow test

Phase 1 must include an operational acceptance scenario proving the user's persistence model:

```text
create work/<job_id>/
→ Start Wordstat run
→ execute one paid Wordstat request
→ receive WORDSTAT_RESULT_V1
→ ChatGPT commits exact raw result + run/cost record to work/<job_id>/
→ simulate chat/reload/context interruption
→ verify persisted raw result is discoverable and can be reused
→ do not recollect the same paid evidence merely because chat state was lost
```

This is a workflow acceptance, not a direct extension-to-GitHub API call.

## 16. Test migration strategy

First copy the reference tests that protect generic lifecycle behavior.

Then add new tests for:

- product/version consistency;
- frozen Tier A hashes;
- registry only contains Wordstat;
- future service signatures do nothing;
- immutable active service;
- Job ID validation;
- missing credential safe result;
- autorun disabled safe result;
- request limit;
- cost limit;
- configured tariff accounting;
- assistant cannot alter policy;
- result carries run/job/service provenance;
- known stale reference report-version defect is absent;
- old Wordstat protocol method/validation regression;
- manual/autorun concurrency regression;
- exactly-once paid request under concurrent duplicate command events;
- worker-owned delivery single-flight;
- request-uncertain restart no-retry.

## 17. Package acceptance ladder

Before asking operator for live Chrome test:

1. all source tests PASS;
2. syntax/static checks PASS;
3. manifest and JSON parse PASS;
4. exact final ZIP is generated;
5. final ZIP extracted to a fresh empty directory;
6. same tests run from exact extracted ZIP PASS;
7. source ↔ ZIP production byte identity verified;
8. unpacked Chromium smoke/E2E harness PASS where available;
9. hashes/evidence committed to GitHub.

Then controlled production ChatGPT acceptance:

```text
bind conversation
→ select Job ID
→ active service Wordstat
→ configure autorun/cost limits
→ Start
→ useful WORDSTAT_API_V1
→ exactly one Yandex request
→ result with correct product version/job/run metadata
→ persist raw result in GitHub work/<job_id>/
→ next watcher
→ second useful command if intended
→ Pause/Resume
→ Finish
```

## 18. Phase 1 stop condition

Do not start Search code merely because source tests pass.

Phase 1 finishes only when:

```text
WORDSTAT + UNIFIED CORE = ACCEPTED
```

with exact package evidence and controlled live production ChatGPT/user acceptance.
