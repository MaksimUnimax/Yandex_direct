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
10. current candidate-specific checkpoint, Codex PASS checkpoint and live-acceptance procedure listed in `CURRENT_STATE.md`.
11. append-only context chain when provenance can alter interpretation.

## Current Phase-2 status

Phase 2 was reopened after the owner's real ChatGPT profile exposed a pre-provider context/binding defect. That product defect was repaired and frozen as exact source `b786918...` / exact artifact `ce824a9f...`.

The first independent Codex campaign returned `FAIL_HARNESS`, not `FAIL_PRODUCT`. ChatGPT reconciled only the obsolete Stage-4 popup lifecycle. Codex then executed a **new complete independent campaign from Step 0 on the same exact artifact** and returned complete PASS.

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
current Stage-4 wrapper commit: 1babfe66222251e2eb63e6e0d4e3eb726ed898e9
```

Current evidence:

```text
../tests/PHASE_2_REAL_PROFILE_BINDING_REPAIR_FREEZE_TRANSPORT_CHECKPOINT_2026-08-25.md
../tests/PHASE_2_REAL_PROFILE_BINDING_STAGE4_HARNESS_RECONCILIATION_2026-08-25.md
../tests/PHASE_2_REAL_PROFILE_BINDING_CODEX_COMPLETE_PASS_2026-08-25.md
PHASE_2_0.1.1_LIVE_ACCEPTANCE.md
```

Accepted independent Codex rerun:

```text
campaign: COMPLETE_RERUN_AFTER_STAGE4_HARNESS_RECONCILIATION
transport: PASS
source suite: 244/244 PASS
packaged suite: 244/244 PASS
B-01/B-02/B-03: PASS
PD-00..PD-17: ALL PASS
mandatory Manual-ON: PASS
S-00..S-17: ALL PASS
real-id late-install repair scenario: PASS
canonical live-receiver repair scenario: PASS
controlled Search stub requests: 1
real Yandex requests: 0
real credentials used: NO
tracked mutations: NO
final cleanliness: PASS
enabled NOT_RUN: 0
verdict: PASS
```

Current transition:

```text
real-profile product repair = frozen
→ exact freeze = PASS
→ Windows-safe exact transport = PASS
→ independent Codex campaign #1 = FAIL_HARNESS
→ Stage-4 harness reconciliation = PASS
→ independent Codex complete rerun = PASS
→ owner real-profile/live acceptance = AUTHORIZED / PENDING
→ Phase 3 Webmaster = BLOCKED until Phase-2 owner-live PASS
```

## Withdrawn/historical candidates

The old `f4aee34... / 739dd5d7...`, `0ee1d38... / d58b5bd...` and `10bb3aca... / 0186b35d...` candidates are historical only and are not eligible for owner-live handoff.

## Authority precedence and conflict rule

The governing order is:

1. explicit current owner instruction that intentionally changes workflow/requirement;
2. `WORKFLOW_OPERATING_RULES.md` for process and roles;
3. `CURRENT_STATE.md` for current control-plane facts/stage;
4. current living product/gate/live-acceptance contracts and mandatory addenda;
5. `ROADMAP.md` for progression narrative;
6. append-only context/historical evidence for provenance.

If current canonical documents materially conflict and no explicit current addendum/reconciliation resolves precedence, stop, reconcile the documents, record the correction, reconstruct state, then continue.

## Exact-artifact rule

The artifact given to the owner must be the exact bytes accepted by the complete independent gate. Do not substitute a logically equivalent rebuild.

## Owner-live rule

Owner performs only irreducible live behavior. Phase 2 owner-live is now authorized on exact `ce824a9f...`: first verify the repaired real-profile binding/Manual path, then — only if healthy and after a fresh official Search pricing check — execute one paid synchronous Search request. If provider initiation may have happened but outcome is ambiguous, no blind retry is allowed.

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
- identity recovery uses trusted location/canonical candidates and fails closed on conflict;
- delivered-but-invalid identity responses are not bootstrap success;
- Bind availability is separated from already-confirmed identity so context can be recovered;
- Manual ON follows content acknowledgement before worker authorization;
- Phase-2 first slice enables only synchronous text `SEARCH_API_V1`; deferred/image/generative Search and Webmaster/Metrika/Direct remain locked.

## Source-of-truth rule

Before any development action or workflow transition: connect to live GitHub, fetch current `main` HEAD, read this index plus `WORKFLOW_OPERATING_RULES.md` and `CURRENT_STATE.md`, inspect applicable current gate/handoff/evidence, resolve any current-document conflict, and only then modify code/QA/governance or authorize paid live operations.