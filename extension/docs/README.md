# Documentation index

Canonical documentation for Yandex Marketing Bridge.

## Read first in the current, every new and every resumed conversation

**Before analysis, coding, QA planning, handoff, failure recovery or continuation, reconstruct the current governed state from live GitHub. Do not rely on chat memory as authority.**

Read in this order:

1. `WORKFLOW_OPERATING_RULES.md` — mandatory operating contract for ChatGPT/Codex/owner roles, environment boundaries, workflow transitions, authority conflicts and failure containment.
2. `CURRENT_STATE.md` — current control-plane state: exact product candidate/artifact identity, latest gate state, owner-live status, blockers and the only authorized next stage.
3. `PROJECT_PURPOSE.md` — current product boundary and separation of Bridge runtime from external GitHub workflow.
4. `SPECIFICATION.md` — base technical contract.
5. `SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md` — mandatory current companion that activates governed Phase-2 synchronous text Search and supersedes stale base-spec Search-block wording for Phase 2 only.
6. `ROADMAP.md` — current phase/stage narrative; exact identities remain governed by `CURRENT_STATE.md`.
7. `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` — permanent living regression firewall.
8. `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md` — mandatory real-popup Manual-ON transaction gate.
9. `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md` — mandatory Phase-2 Search gate companion.
10. `CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md` — mandatory pre-Codex exact-artifact/transport procedure.
11. candidate-specific current Stage-4 execution/reconciliation authority listed in `CURRENT_STATE.md`.
12. append-only context chain when provenance can alter interpretation.

## Current Phase-2 Stage-4 candidate-specific authority

At the current Stage-4 checkpoint, `CURRENT_STATE.md` requires these candidate-specific documents:

```text
PHASE_2_STAGE_4_CODEX_EXECUTION_MAP_2026-08-24.md
CODEX_PHASE2_STAGE4_FINAL_HANDOFF_2026-08-24.md
CODEX_PHASE2_STAGE4_WINDOWS_TRANSPORT_RECONCILIATION_2026-08-24.md
CODEX_PHASE2_STAGE4_BROWSER_HARNESS_RECONCILIATION_2026-08-24.md
../tests/PHASE_2_STAGE_4_PACKAGED_SUITE_ADAPTER_2026-08-24.md
../tests/PHASE_2_STAGE_4_REFROZEN_CANDIDATE_CHECKPOINT_2026-08-24.md
```

Candidate-specific precedence is explicit:

```text
Windows transport reconciliation
→ supersedes stale 9ded... transport references in older Stage-4 text.

Browser-harness reconciliation
→ supersedes stale/missing B-01/B-02/B-03 browser venue references in older Stage-4 text.

All other parent PD / Manual / Search / exact-identity requirements remain mandatory.
```

Do not silently revive superseded candidate/transport/browser instructions from historical text.

## Authority precedence and conflict rule

The governing order is:

1. explicit current owner instruction that intentionally changes workflow/requirement;
2. `WORKFLOW_OPERATING_RULES.md` for operating process and roles;
3. `CURRENT_STATE.md` for current control-plane facts/stage;
4. current living product/gate contracts and mandatory current companion/addendum/reconciliation documents;
5. `ROADMAP.md` for progression narrative;
6. append-only context and historical evidence for provenance only.

A lower-precedence or historical document must never silently override a higher-precedence current contract.

**If two current canonical documents materially contradict each other and no explicit current addendum/reconciliation declares precedence, STOP before code/QA/handoff. Reconcile the documents, record the correction, reconstruct current state again, then continue.**

Older wording may remain only when a current addendum/reconciliation explicitly labels it stale/superseded.

## Mandatory workflow-transition reconstruction

Before every transition between workflow stages, explicitly establish from live GitHub/current evidence:

```text
LIVE_HEAD
PRODUCT_SOURCE
HANDOFF_ARTIFACT
LATEST_FULL_GATE
PRODUCTION_BYTES_CHANGED_SINCE_GATE
OWNER_LIVE
OPEN_BLOCKERS
AUTHORIZED_NEXT_STAGE
```

Transitions include:

- new/resumed conversation;
- requirement → development;
- development → candidate freeze;
- freeze → Codex QA;
- Codex PASS/FAIL → repair/handoff;
- failure → next attempt;
- documentation/governance change → next engineering/release action;
- full-gate PASS → owner live acceptance;
- owner live result → phase close/reopen.

If any field is unresolved or a current conflict exists, do not improvise the next stage.

## Development vs pre-delivery testing

During implementation/repair:

```text
focused tests for changed behavior + affected dependencies
```

Immediately before owner handoff:

```text
freeze exact candidate
→ prepare exact Codex-consumable transport
→ producer-side read-back / consumer-conformance proof
→ one complete Codex regression campaign
→ only complete PASS allows owner handoff
```

A partial gate or browser preflight is not the final full-gate PASS.

## Exact-artifact / Codex rule

`CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md` is the mandatory positive execution companion. No Codex prompt is authorized until the applicable exact-artifact preparation and fresh consumer-conformance checks pass.

Controlled Codex/Puppeteer evidence and owner real-profile/live acceptance remain distinct. The controlled gate covers every reliably automatable surface and must not fabricate an owner-live PASS.

## Owner-correction rule

When the owner corrects a repeated workflow/role/safety/QA/handoff/authority rule, classify it immediately:

- one-off instruction; or
- persistent invariant.

Persistent invariants apply immediately and must be canonicalized into the appropriate current document before the same class of mistake can recur. Then reconstruct current state again.

## Append-only context chain

Historical/correction provenance currently spans:

```text
DEVELOPMENT_CONTEXT_APPEND_ONLY.md
DEVELOPMENT_CONTEXT_APPEND_ONLY_CONTINUATION_0.1.1.md
DEVELOPMENT_CONTEXT_APPEND_ONLY_CONTINUATION_PHASE2_2026-08-19.md
```

These form a chronological append-only history. They are provenance, not automatic current candidate/stage authority. Do not rewrite old entries to hide superseded decisions.

## Reference / architecture

- `REFERENCE_BASELINE.md` — owner-supplied Wordstat reference identity/hashes.
- `PHASE_0_REFERENCE_AUDIT.md` — Phase-0 reference audit.
- `CORE_EXTRACTION_MAP.md` — common/service extraction map.
- `ORDER_WORKSPACE_LIFECYCLE.md` — external ChatGPT/GitHub order-workspace lifecycle, not extension runtime.
- `PHASE_1_WORDSTAT_IMPLEMENTATION_PLAN.md` — historical Phase-1 implementation plan.
- `PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md` — current Phase-2 Search requirement/implementation authority.

## Current implementation / live gate

Current exact candidate, transport, browser-harness authority, full-gate status and authorized next stage are read from `CURRENT_STATE.md`.

Permanent controlled pre-delivery authorities:

```text
CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

Current Stage-4 reconciliations must be read in addition to the older final handoff/execution map when `CURRENT_STATE.md` requires them.

## Machine-readable evidence / WIP recovery

Current evidence is under `extension/tests/`, including governed phase checkpoints, validation reports, package manifests and QA transport/browser infrastructure. Historical candidate evidence must not override `CURRENT_STATE.md`.

## Current architectural corrections

- no mandatory `job_id` in extension runtime;
- no GitHub API/workspace dependency in extension runtime;
- all errors automatically return to bound ChatGPT regardless of Debug Mode;
- Debug Mode adds only extra redacted logs;
- Export/Import secret settings backup with checksum validation;
- active RUN/manual-operation safety state preserved on import;
- Manual on PAUSED RUN shares the same RUN budget;
- no blind retry after uncertain request outcome;
- Manual action is Bridge-owned/external and independent of native Copy lifecycle;
- current Manual delivery completion is Send→ready/Microphone based; obsolete sent-user-turn reconciliation/exhaustion is not current behavior;
- Phase-2 Search first slice is synchronous text `SEARCH_API_V1` only; deferred/image/generative Search plus Webmaster/Metrika/Direct remain locked.

## Source of truth rule

Before any development action or workflow-stage transition:

1. connect to live GitHub;
2. fetch current `main` HEAD and commit metadata;
3. read this index, `WORKFLOW_OPERATING_RULES.md`, `CURRENT_STATE.md`, current purpose/spec/addenda/roadmap/gate/runbook and applicable candidate-specific reconciliations;
4. inspect append-only history where it can alter interpretation;
5. verify exact phase/gate/handoff state;
6. resolve any un-reconciled current-document conflict;
7. only then modify code/QA/governance or authorize Codex/paid live operations.

Do not use chat memory, old handoff text, historical evidence or remembered SHA as authority when live GitHub can answer the question.
