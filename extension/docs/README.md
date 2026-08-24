# Documentation index

Canonical documentation for Yandex Marketing Bridge.

## Read first in every current, new and resumed conversation

Before analysis, coding, QA planning, handoff, failure recovery or continuation, reconstruct governed state from live GitHub. Do not use chat memory as authority.

Read in this order:

1. `WORKFLOW_OPERATING_RULES.md` — mandatory ChatGPT/Codex/owner operating contract.
2. `CURRENT_STATE.md` — exact current product/artifact identity, latest gate verdict, owner-live state, blockers and authorized next action.
3. `PROJECT_PURPOSE.md` — product boundary and GitHub/runtime separation.
4. `SPECIFICATION.md` — base technical contract.
5. `SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md` — current Phase-2 Search companion; supersedes stale base-spec Search-lock wording for the enabled first slice.
6. `PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md` — Phase-2 Search requirement, pricing-policy and live-boundary authority.
7. `ROADMAP.md` — phase/stage narrative; exact identities remain governed by `CURRENT_STATE.md`.
8. `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` and mandatory Manual/Search addenda — permanent controlled regression firewall.
9. `CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md` — exact-artifact/Codex preparation procedure.
10. current candidate-specific evidence/live procedure listed in `CURRENT_STATE.md`.
11. append-only context chain when provenance can alter interpretation.

## Current Phase-2 status

The exact combined Wordstat+Search candidate has completed the entire controlled pre-delivery boundary with **PASS**.

Current exact candidate:

```text
source: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
artifact SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
artifact bytes: 170734
files: 65
ZIP entries: 68
```

Complete Codex result checkpoint:

```text
../tests/PHASE_2_STAGE_4_CODEX_FULL_GATE_PASS_2026-08-24.md
```

Current owner-live procedure:

```text
PHASE_2_0.1.1_LIVE_ACCEPTANCE.md
```

Current transition is therefore:

```text
controlled pre-delivery gate = PASS
→ fresh official Search pricing check = COMPLETE
→ one minimal owner real-profile synchronous Search = AUTHORIZED / PENDING
→ Phase 2 closes only after truthful usable SEARCH_RESULT_V1 live PASS
```

Do not start Phase 3 Webmaster before that live boundary closes.

## Retained Stage-4 provenance

These remain evidence and debugging authority, but they are no longer the next execution stage:

```text
PHASE_2_STAGE_4_CODEX_EXECUTION_MAP_2026-08-24.md
CODEX_PHASE2_STAGE4_FINAL_RERUN_HANDOFF_2026-08-24.md
CODEX_PHASE2_STAGE4_WINDOWS_TRANSPORT_RECONCILIATION_2026-08-24.md
CODEX_PHASE2_STAGE4_BROWSER_HARNESS_RECONCILIATION_2026-08-24.md
../tests/PHASE_2_STAGE_4_PACKAGED_SUITE_ADAPTER_2026-08-24.md
../tests/PHASE_2_STAGE_4_REFROZEN_CANDIDATE_CHECKPOINT_2026-08-24.md
```

Historical transport/browser failures remain reconciled QA-process evidence only and do not supersede the later complete PASS.

## Authority precedence and conflict rule

The governing order is:

1. explicit current owner instruction that intentionally changes workflow/requirement;
2. `WORKFLOW_OPERATING_RULES.md` for process and roles;
3. `CURRENT_STATE.md` for current control-plane facts/stage;
4. current living product/gate/live-acceptance contracts and mandatory addenda;
5. `ROADMAP.md` for progression narrative;
6. append-only context/historical evidence for provenance.

If current canonical documents materially conflict and no explicit current addendum/reconciliation resolves precedence, stop, reconcile the documents, record the correction, reconstruct state, then continue.

## Mandatory workflow-transition reconstruction

Before every stage transition establish from live GitHub/current evidence:

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

Transitions include new/resumed conversation, requirement→development, development→freeze, freeze→Codex, Codex result→repair/handoff, documentation change→next action, full-gate PASS→owner live, and owner-live result→phase close/reopen.

## Development vs pre-delivery testing

During implementation/repair:

```text
focused tests for changed behavior + affected dependencies
```

Before owner handoff:

```text
freeze exact candidate
→ prepare exact Codex-consumable transport
→ producer read-back / consumer-conformance proof
→ one complete Codex regression campaign
→ only complete PASS allows owner live handoff
```

Controlled browser/Codex evidence must not be relabeled owner real-profile evidence.

## Exact-artifact rule

The artifact given to the owner must be the exact bytes accepted by the complete gate. Do not substitute a logically equivalent rebuild.

## Owner-live rule

Owner performs only irreducible live behavior. For Phase 2 this means one paid synchronous Search request after fresh official pricing verification. Automated UI/runtime cases are observed naturally rather than repeated manually.

If provider initiation may have happened but outcome is ambiguous, no blind retry is allowed.

## Append-only context chain

Historical/correction provenance currently spans:

```text
DEVELOPMENT_CONTEXT_APPEND_ONLY.md
DEVELOPMENT_CONTEXT_APPEND_ONLY_CONTINUATION_0.1.1.md
DEVELOPMENT_CONTEXT_APPEND_ONLY_CONTINUATION_PHASE2_2026-08-19.md
```

These are provenance, not automatic current-stage authority.

## Current architectural corrections

- no mandatory `job_id` in extension runtime;
- no GitHub API/workspace runtime dependency;
- all detected errors are delivered regardless of Debug Mode;
- Debug adds redacted diagnostics only;
- settings Export/Import supports secret backup with integrity validation;
- active RUN/manual safety state survives import rules;
- Manual on PAUSED RUN shares the same RUN budget;
- no blind retry after uncertain provider outcome;
- Manual action is Bridge-owned and independent of native Copy;
- Manual delivery completion uses Send→ready/Microphone, not obsolete sent-turn reconciliation;
- Phase-2 first slice enables only synchronous text `SEARCH_API_V1`; deferred/image/generative Search and Webmaster/Metrika/Direct remain locked.

## Source of truth rule

Before any development action or workflow transition:

1. connect to live GitHub;
2. fetch current `main` HEAD and commit metadata;
3. read this index, `WORKFLOW_OPERATING_RULES.md`, `CURRENT_STATE.md`, current purpose/spec/addenda/roadmap and applicable gate/live documents;
4. inspect append-only history where it can alter interpretation;
5. verify exact phase/gate/handoff state;
6. resolve any unreconciled current-document conflict;
7. only then modify code/QA/governance or authorize paid live operations.
