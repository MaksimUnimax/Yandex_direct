# Documentation index

Canonical documentation for Yandex Marketing Bridge.

## Read first in every current, new and resumed conversation

Before analysis, coding, QA planning, handoff, failure recovery or continuation, reconstruct governed state from live GitHub. Do not use chat memory as authority.

Read in this order:

1. `WORKFLOW_OPERATING_RULES.md` — mandatory ChatGPT/Codex/owner operating contract.
2. `CURRENT_STATE.md` — exact current product/artifact identity, latest gate verdict, owner-live state, blockers and authorized next action.
3. `PROJECT_PURPOSE.md` — product boundary and GitHub/runtime separation.
4. `SPECIFICATION.md` — base technical contract.
5. `SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md` — current Phase-2 Search companion.
6. `PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md` — Search requirements, pricing-policy and live-boundary authority.
7. `ROADMAP.md` — phase/stage narrative; exact identities remain governed by `CURRENT_STATE.md`.
8. `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` and mandatory Manual/Search addenda — permanent controlled regression firewall.
9. `CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md` — exact-artifact QA preparation procedure.
10. current candidate-specific checkpoint/handoff listed in `CURRENT_STATE.md`.
11. append-only context chain when provenance can alter interpretation.

## Current Phase-2 status

Phase 2 was reopened after the owner's real ChatGPT profile exposed a pre-provider context/binding defect in the reconstructed candidate. The defect has been repaired and a new exact candidate is frozen, but **the mandatory independent Codex complete gate has not run yet**. Therefore owner-live Search is blocked.

Current exact source and candidate:

```text
source branch: candidate/phase2-real-profile-binding-repair-2026-08-25
source commit: b7869180c229356a6b3d51ac980ec3da5df4c23c
parent: f4aee34c0a3455aa7199f6aa54bd581c71d97337
artifact: yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
artifact SHA-256: ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
artifact bytes: 179013
files: 69
ZIP entries: 72
payload manifest SHA-256: ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
payload manifest bytes: 12125
Windows-safe transport commit: 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
repair browser harness commit: 81625e073d507d70451f1457185a3e906c640c66
```

Current evidence/handoff:

```text
../tests/PHASE_2_REAL_PROFILE_BINDING_REPAIR_FREEZE_TRANSPORT_CHECKPOINT_2026-08-25.md
../tests/CODEX_PHASE_2_REAL_PROFILE_BINDING_REPAIR_FULL_GATE_HANDOFF_2026-08-25.md
```

ChatGPT-controlled pre-Codex evidence:

```text
focused repair suite: 37/37 PASS
complete source suite: 244/244 PASS
freeze run: 32805530317 / job 97674800575 PASS
frozen source suite: 244/244 PASS
frozen packaged suite: 244/244 PASS
deterministic byte-identical rebuild: PASS
Windows transport run: 32805811476 / job 97675604279 PASS
Windows Server 2025 / Git 2.55.0.windows.4 / core.autocrlf=true
exact B64 reassembly + ZIP identity + payload manifest: PASS
real Yandex requests: 0
```

These are ChatGPT-owned preflight/transport results only. They **must not be relabeled as the independent Codex pre-delivery gate**.

Current transition:

```text
real-profile repair = implemented
→ exact freeze = PASS
→ Windows-safe exact transport = PASS
→ independent Codex complete gate = READY / PENDING
→ owner real-profile synchronous Search = BLOCKED until Codex PASS
→ Phase 2 closes only after truthful usable SEARCH_RESULT_V1 owner-live PASS
```

Do not start Phase 3 Webmaster before Phase-2 owner-live closes.

## Withdrawn/historical Phase-2 candidates

The following are historical and not eligible for current owner-live handoff:

```text
f4aee34... / 739dd5d7...  — withdrawn after real-profile binding failure and because the claimed complete gate was ChatGPT Actions, not independent Codex
0ee1d38... / d58b5bd...  — older Stage-4 candidate
10bb3aca... / 0186b35d... — older popup-fix candidate
```

Historical Stage-4 and context-recovery evidence remains useful for provenance/debugging, but it does not supersede `CURRENT_STATE.md` or the current `b786918... / ce824a9f...` candidate.

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

Transitions include new/resumed conversation, requirement→development, development→freeze, freeze→QA, QA result→repair/handoff, documentation change→next action, full-gate PASS→owner live, and owner-live result→phase close/reopen.

## Development vs pre-delivery testing

During implementation/repair:

```text
focused tests for changed behavior + affected dependencies
```

Before owner handoff:

```text
freeze exact candidate
→ prepare exact consumer-safe transport
→ producer read-back / consumer-conformance proof
→ one complete independent Codex controlled regression campaign
→ only complete PASS allows owner live handoff
```

Controlled browser/QA evidence must not be relabeled owner real-profile evidence.

## Exact-artifact rule

The artifact given to the owner must be the exact bytes accepted by the complete independent gate. Do not substitute a logically equivalent rebuild.

## Owner-live rule

Owner performs only irreducible live behavior. For Phase 2 this means one paid synchronous Search request **only after independent Codex complete PASS** and a fresh official Search pricing/tariff check.

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
- popup geometry is bounded for Chrome 151 native action host;
- current ChatGPT identity accepts factual real conversation ids without an invalid RFC UUID-version filter;
- identity recovery uses supported trusted location/canonical candidates and fails closed on conflict;
- delivered-but-invalid identity responses are not bootstrap success;
- Bind availability is separated from already-confirmed identity so context can be recovered;
- Manual ON follows content acknowledgement before worker authorization;
- Phase-2 first slice enables only synchronous text `SEARCH_API_V1`; deferred/image/generative Search and Webmaster/Metrika/Direct remain locked.

## Source-of-truth rule

Before any development action or workflow transition:

1. connect to live GitHub;
2. fetch current `main` HEAD and commit metadata;
3. read this index, `WORKFLOW_OPERATING_RULES.md`, `CURRENT_STATE.md`, current purpose/spec/addenda/roadmap and applicable gate/live documents;
4. inspect append-only history where it can alter interpretation;
5. verify exact phase/gate/handoff state;
6. resolve any unreconciled current-document conflict;
7. only then modify code/QA/governance or authorize paid live operations.
