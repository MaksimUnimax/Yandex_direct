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
