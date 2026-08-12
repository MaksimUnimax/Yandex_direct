# DEVELOPMENT CONTEXT — APPEND ONLY

Created: 2026-08-12.

## Canonical rule

This file is the chronological context/decision log for Yandex Marketing Bridge development.

After creation it is **append-only**:

- previous entries are not deleted;
- previous entries are not rewritten to make history look cleaner;
- corrections to earlier decisions are appended as new entries;
- new architectural decisions, live-test results, rejected approaches, implementation discoveries and rollback notes are appended at the end;
- every appended entry must include a date and a short status/purpose heading.

The current state of the product is defined by the latest applicable entries plus the living `SPECIFICATION.md` and `ROADMAP.md`. This file preserves why the state changed.

---

# ENTRY 0001 — 2026-08-12 — PROJECT ORIGIN AND TOOLING GOAL

## Context

The owner intends to take real marketing orders, primarily via Kwork, and wants ChatGPT to perform the substantive work through controlled browser/API bridges rather than only provide manual instructions.

The earlier `blood_sand` repository/work was explicitly reclassified as an example of already performed marketing research, not as the project being optimized here.

The current project is a reusable execution environment for many future customer orders.

## Existing proven capability

A Wordstat Bridge already exists and has been iterated through controlled manual/autorun development. The owner supplied version 1.1.5 plus canonical append-only documentation as the implementation reference.

The new system must preserve proven ChatGPT DOM/control behavior from that reference instead of inventing a new automation surface without need.

---

# ENTRY 0002 — 2026-08-12 — REQUIRED SERVICE SET

After reviewing typical Kwork offers for Yandex Direct/semantics work, the required working dataset was defined as broader than Wordstat alone.

The unified bridge is planned to support:

1. Wordstat — search demand, frequency, dynamics, regions.
2. Yandex Search / SERP — real search results for intent/SERP clustering and competitive evidence.
3. Webmaster — actual organic queries and site search evidence; owner explicitly required this module immediately, not as a later optional phase.
4. Metrika — conversion/behavioral evidence.
5. Direct — campaign/account reads, audits, reports, later draft writes and gated live writes.

---

# ENTRY 0003 — 2026-08-12 — ONE EXTENSION, MULTIPLE ADAPTERS

Rejected approach:

```text
separate Wordstat extension
separate Search extension
separate Webmaster extension
separate Metrika extension
separate Direct extension
```

Reason for rejection: each extension would compete for the same ChatGPT writing blocks, Copy controls, MutationObservers, autorun state, composer delivery and conversation ownership.

Adopted architecture:

```text
one Yandex Marketing Bridge
+ one shared CORE
+ independent service adapters
```

The user/operator must not have to disable one Chrome extension and enable another between research stages.

---

# ENTRY 0004 — 2026-08-12 — ROUTING WITHOUT A GENERIC ROUTER COMMAND

The owner questioned whether a new generic executable router command was necessary.

Decision: **no generic `YANDEX_MARKETING_API_V1` executable wrapper is required.**

The common watcher extracts a special block and the protocol detector routes based on the service protocol itself:

```text
WORDSTAT_API_V1  → Wordstat
SEARCH_API_V1    → Search
WEBMASTER_API_V1 → Webmaster
METRIKA_API_V1   → Metrika
DIRECT_API_V1    → Direct
```

The router is a dispatcher, not another command language.

Unknown/non-service blocks cause no API action.

---

# ENTRY 0005 — 2026-08-12 — ONE RUN = ONE SERVICE

The owner requested development and testing in isolated service increments: one run, one service, test, then continue.

This became both a development rule and a product safety rule.

Decision:

- every RUN has one immutable `active_service`;
- commands for another service during that run are not executed;
- to switch services, Finish the current run and Start a new run;
- multiple sequential runs remain linked by one JOB/order.

Example:

```text
JOB-001
RUN-001 Wordstat
RUN-002 Search
RUN-003 Webmaster
RUN-004 Metrika
RUN-005 Direct READ
```

This prevents a Wordstat autorun from unexpectedly drifting into a materially more expensive or dangerous service.

---

# ENTRY 0006 — 2026-08-12 — MISSING CREDENTIALS MUST NOT STOP THE JOB

Owner requirement:

If a customer does not provide a key/token/access for a service, the workflow should continue using the services that are available.

Decision:

- credentials are independent per service/credential family;
- missing credentials return controlled `SKIPPED / NO_CREDENTIALS` semantics;
- the whole JOB does not fail merely because one optional evidence source is unavailable;
- the final work must clearly distinguish unavailable evidence from successfully collected evidence;
- if the requested deliverable intrinsically requires the unavailable service, that part cannot be falsely marked complete.

---

# ENTRY 0007 — 2026-08-12 — AUTORUN PERMISSIONS AND COST CONTROL BELONG TO THE EXTENSION

Owner requirement:

Paid requests must be usable in autorun, but not blindly. The operator decides which services/operation classes are enabled and must be able to limit spending.

Decision:

- credential presence does not imply autorun permission;
- autorun permission is operator-controlled per service/operation class;
- request and cost hard limits are enforced by the extension, not by ChatGPT promises;
- expensive operation classes receive separate toggles;
- ChatGPT commands cannot raise limits or enable disabled expensive operations;
- cost/quota limit breach returns a controlled SKIPPED/BLOCKED result without external request;
- Direct/Metrika/Webmaster non-monetary quotas also require guards.

Paid/irreversible initiation must never be blindly retried after uncertain worker/browser state.

---

# ENTRY 0008 — 2026-08-12 — DIRECT RISK SEPARATION

Direct cannot be treated like read-only Wordstat.

Adopted profiles:

```text
DIRECT_READ
DIRECT_DRAFT_WRITE
DIRECT_LIVE_WRITE
```

READ may be autorun once tested and permitted.

DRAFT/PRE-LIVE WRITE is developed only after READ acceptance and must use read-back verification.

LIVE WRITE is not unrestricted autorun. It requires a specific operator-approved changeset/transaction and post-write verification.

---

# ENTRY 0009 — 2026-08-12 — DEVELOPMENT ORDER

Owner required strict service-by-service development.

Adopted order:

```text
PHASE 0  Repository/reference/core design
PHASE 1  Wordstat + unified core
PHASE 2  Search / SERP
PHASE 3  Webmaster
PHASE 4  Metrika
PHASE 5  Direct READ
PHASE 6  Direct DRAFT/PRE-LIVE WRITE
PHASE 7  Direct LIVE WRITE
PHASE 8  Full Kwork order E2E
```

No next service is started until the current phase passes source tests, packaged tests, controlled real Chrome/production ChatGPT acceptance and regressions of previously accepted services.

---

# ENTRY 0010 — 2026-08-12 — GITHUB WORKSPACE AND ORDER DATA PERSISTENCE

The owner provided private repository:

```text
MaksimUnimax/Yandex_direct
```

At discovery time it was empty and used `main` as default branch.

Owner required two separate persistent top-level areas:

```text
extension/
work/
```

Decision:

- `extension/` contains product code, tests, reference and permanent documentation;
- `work/` contains only active-order workspaces;
- each order receives `work/<job_id>/`;
- all important collected evidence, including paid API results, must be persisted there so chat/context loss does not force recollection/re-spend;
- after order delivery/acceptance, `work/<job_id>/` is removed from the current repository tree.

Important Git semantics recorded for owner: ordinary deletion removes the folder from current HEAD but previous commits remain in Git history. Full historical purge would be a separate exceptional operation.

Secrets are prohibited from GitHub even though the repository is private.

---

# ENTRY 0011 — 2026-08-12 — DOCUMENTATION LOCATION AND APPEND-ONLY CONTEXT

Owner added a direct requirement:

Inside `extension/`, create a separate documentation directory and put there:

- project goal and meaning;
- technical specification;
- roadmap;
- development/dialog context.

The context/development history must be appended **append-only**.

Adopted location:

```text
extension/docs/
```

Canonical files initially created:

```text
PROJECT_PURPOSE.md
SPECIFICATION.md
ROADMAP.md
REFERENCE_BASELINE.md
DEVELOPMENT_CONTEXT_APPEND_ONLY.md
```

This entry establishes the append-only rule for the last file.

---

# ENTRY 0012 — 2026-08-12 — PHASE 0 EXACT REFERENCE VERIFICATION

The exact owner-supplied reference ZIP was independently hashed, freshly extracted and executed during Phase 0.

Verified artifact:

```text
wordstat-bridge-v1.1.5-full-function-environment-audit(4).zip
SHA-256 a39bbe65b046ef6eac5a7890b8afd84e69550db34debf271b7c373d08a1fef1a
```

Canonical documentation:

```text
WORDSTAT_BRIDGE_DOCUMENTATION_APPEND_ONLY_FULL_FUNCTION_ENVIRONMENT_AUDIT(4).md
SHA-256 437a69022b31621d7a749e3b92c0faf0c45f3d7be60e1a901cda65c3faf0a25a
```

Fresh extracted artifact results obtained in the current development session:

```text
npm test: 283/283 PASS
node --check: PASS for all production/shared JS files checked
```

The supplied reference's own full-function audit records 21/21 real Chromium E2E checks with ChatGPT DOM/Yandex HTTPS mocks and source↔ZIP byte identity. This is strong reference evidence but does not replace later production ChatGPT acceptance of Yandex Marketing Bridge.

---

# ENTRY 0013 — 2026-08-12 — REFERENCE 1.1.5 VS HISTORICAL 1.1.6

During Phase 0 the canonical append-only document was read through its final line.

It contains a historical `1.1.6` narrow provenance/version patch, but later append-only entries intentionally continue a manifest/runtime `1.1.5` line for Start parity, single-flight/concurrency repairs and the final full-function/environment audit.

The owner supplied the final audited `1.1.5` ZIP identified by the final append-only entry, so that exact ZIP is the behavioral reference authority for migration.

A known defect is preserved in that artifact:

```text
shared/wordstat_protocol.js
const VERSION = "1.1.1"
```

while package/manifest are `1.1.5`.

The historical 1.1.6 entry proves this is a stale result-provenance defect. Decision: do not silently replace the owner-supplied reference; instead explicitly fix version consistency in the new product and add an executable regression test so the defect cannot recur.

---

# ENTRY 0014 — 2026-08-12 — CORE EXTRACTION CLASSIFICATION

Phase 0 classified reference code into four tiers.

Tier A — freeze/copy byte-identically first:

```text
shared/composer_send.js
shared/conversation_identity.js
shared/manual_controls.js
shared/proven_writing_block_capture.js
```

These are proven byte-identical to Business Bridge 2.0.0.22.

Tier B — generic lifecycle semantics but Wordstat-named export:

```text
shared/autorun_model.js
```

It may be genericized under differential tests.

Tier C — service-specific:

```text
shared/wordstat_protocol.js
```

It remains the Wordstat adapter/protocol boundary.

Tier D — mixed generic + Wordstat-specific orchestration requiring controlled extraction:

```text
service_worker.js
content_script.js
popup.*
```

Detailed boundaries are recorded in `CORE_EXTRACTION_MAP.md`.

---

# ENTRY 0015 — 2026-08-12 — GITHUB PERSISTENCE IS A CHATGPT WORKFLOW, NOT AN EXTENSION SECRET SURFACE

Clarification made during Phase 0:

The extension itself will not receive/store a GitHub token merely to satisfy order evidence persistence.

The required workflow is:

```text
API result delivered durably to ChatGPT
→ ChatGPT uses its connected GitHub capability
→ exact raw evidence is committed into work/<job_id>/
→ then the workflow proceeds to the next paid collection step when persistence/reuse matters
```

The bridge may stamp trusted local `job_id`, `run_id`, service, operation and request identifiers into the result so GitHub evidence can be named and audited deterministically.

This keeps GitHub credentials outside the Chrome extension while preserving the owner's requirement that paid evidence is not lost with chat/browser context.

---

# ENTRY 0016 — 2026-08-12 — PHASE 0 GATE AND PHASE 1 START AUTHORIZATION

Phase 0 produced:

- repository split `extension/` + `work/`;
- canonical documentation area;
- reference baseline/hashes and exact 41-file inventory;
- fresh reference test verification;
- reference authority decision;
- known-defect record;
- CORE extraction map;
- detailed `PHASE_1_WORDSTAT_IMPLEMENTATION_PLAN.md`.

Decision: Phase 0 design/reference gate is PASS. Phase 1 may begin with **Wordstat as the only executable service**.

No Search/Webmaster/Metrika/Direct implementation is authorized until Phase 1 reaches its own acceptance gate.

---

# ENTRY 0017 — 2026-08-12 — PHASE 1 UNIFIED PRODUCT IDENTITY AND ROUTING

Phase 1 implementation began from the audited Wordstat lifecycle rather than a blank rewrite.

New product identity:

```text
Yandex Marketing Bridge — ChatGPT ↔ Yandex
version 0.1.0
bridge id: yandex-marketing-bridge
```

A single shared product version now drives result provenance, eliminating the known stale Wordstat 1.1.5 report-version defect.

Phase 1 registry intentionally contains exactly one executable signature:

```text
WORDSTAT_API_V1 → wordstat
```

No Search/Webmaster/Metrika/Direct executable adapter was added. Future protocol signatures are not registered and cannot create a network side effect in Phase 1.

---

# ENTRY 0018 — 2026-08-12 — JOB, ACTIVE SERVICE, CREDENTIAL CAPABILITY, POLICY AND COST GUARDS

Phase 1 added generic CORE models for:

- trusted Job ID;
- immutable active service per run;
- credential capability state;
- operator policy;
- request/cost ledger.

Job ID is locally/operator controlled and rejects path separators/traversal.

Start binds:

```text
job_id
active_service = wordstat
```

and those values cannot be changed by assistant text during an active run.

Credential presence is now independent from Autorun permission. Missing Wordstat credentials no longer need to stop the Job/run startup merely because the evidence source is unavailable. A valid command can produce:

```text
WORDSTAT_RESULT_V1
status = SKIPPED
reason = NO_CREDENTIALS
```

with zero external Yandex request.

Operator policy controls method allowlist, request ceilings and estimated-ruble ceilings per run/job. ChatGPT commands cannot change those settings.

For paid initiation, budget/accounting reservation occurs before network initiation. If the browser/worker crashes afterward, accounting may conservatively over-count but must not under-count and accidentally permit another paid attempt.

---

# ENTRY 0019 — 2026-08-12 — MANUAL MODE ALSO OBEYS JOB COST LIMITS

A safety gap was identified during Phase 1 design: if hard money/request limits protected only Autorun, an operator or workflow could bypass those ceilings simply by switching to Manual Copy.

Decision and implementation:

- Manual remains an explicit native-Copy authorization surface;
- Manual does not require the Autorun-enabled bit;
- but Manual **does** obey service/method policy and per-Job hard request/cost ceilings;
- missing credentials in Manual produce a durable SKIPPED result with zero fetch;
- a Manual paid request reserves Job budget before initiation;
- Manual cannot be used as a cost-limit bypass.

Manual currently has no durable RUN of its own, so per-run counters are an Autorun concept; the per-Job ceiling is the common hard protection across both channels.

---

# ENTRY 0020 — 2026-08-12 — PHASE 1 SOURCE AND EXACT ZIP PRE-LIVE ACCEPTANCE

After migration and test-harness updates, the final Phase 1 pre-live candidate reached:

```text
source full suite:        299/299 PASS
fresh ZIP full suite:     299/299 PASS
source ↔ fresh ZIP:        41/41 files byte-identical
fresh ZIP JS/MJS syntax:   36/36 PASS
manifest/package JSON:      2/2 PASS
Chromium 144 load smoke:   PASS
```

The 299 tests consist of migrated reference regression coverage plus 16 new unified-core tests covering Job/service/policy/cost/missing-credential/manual safeguards and result provenance.

Exact candidate artifact:

```text
yandex-marketing-bridge-0.1.0-phase1-wordstat-candidate.zip
SHA-256 79c2bca5e2e65aaa1cb7cc38754589a0bf3b0b436c82f36416934cd175cafa2a
```

Four Business Bridge common shared modules remain at their exact reference hashes.

Chromium smoke proves the exact unpacked candidate loads without observed manifest/extension/service-worker errors in the test environment. It does **not** claim current production ChatGPT live acceptance.

Machine-readable evidence is stored under `extension/tests/`.

---

# ENTRY 0021 — 2026-08-12 — PHASE 1 LIVE GATE BLOCKS SEARCH DEVELOPMENT

A controlled production test procedure was created:

```text
extension/docs/PHASE_1_LIVE_ACCEPTANCE.md
```

It requires proof of:

- current production ChatGPT writing-block/Copy behavior;
- missing-credential SKIP with zero request;
- operator-disabled/cost-limit SKIP paths;
- one real free Wordstat network request if current official pricing still marks the chosen operation free;
- one minimal intentional paid Wordstat request only after fresh official tariff verification;
- exactly-once request and delivery;
- correct 0.1.0 + Job/Run/cost provenance;
- immediate GitHub persistence of paid raw evidence;
- Manual cost guard;
- Pause/Resume/Finish and ownership/isolation controls.

Current lifecycle status:

```text
PHASE 0: PASS
PHASE 1: PRE-LIVE PASS / PRODUCTION LIVE PENDING
PHASE 2 SEARCH: BLOCKED
```

No Search implementation is authorized until the operator live acceptance for Phase 1 passes and the result is appended here.
