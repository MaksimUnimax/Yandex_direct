# Documentation index

Canonical documentation for Yandex Marketing Bridge.

## Read first in the current, every new and every resumed development conversation

**These rules apply immediately in the current conversation. Before any analysis, coding, QA planning, handoff, failure recovery or continuation, reconstruct the current governed state from live GitHub. Do not rely on chat memory as authority.**

Read in this exact order:

1. `WORKFLOW_OPERATING_RULES.md` — mandatory operating contract for ChatGPT/Codex/owner roles, environment boundaries, workflow-transition reconstruction, authority conflict handling, failure containment and owner-correction canonicalization.
2. `CURRENT_STATE.md` — compact current control-plane state: live GitHub HEAD, exact product candidate/artifact identity, latest full-gate status, owner-live status, open blockers and the only authorized next stage.
3. `PROJECT_PURPOSE.md` — current product boundary and separation of Bridge runtime from external GitHub workflow.
4. `SPECIFICATION.md` — current technical contract.
5. `ROADMAP.md` — current phase/gate status and historical/superseded candidate records.
6. `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` — permanent living regression firewall. **Run it only immediately before handing the owner a working build; during development run focused tests for changed code/dependencies only.**
7. `DEVELOPMENT_CONTEXT_APPEND_ONLY.md` — immutable historical entries 0001–0021.
8. `DEVELOPMENT_CONTEXT_APPEND_ONLY_CONTINUATION_0.1.1.md` — append-only correction/continuation entries 0022+.

The two development-context files form one chronological append-only chain. Do not rewrite the parent to hide superseded decisions.

## Authority precedence and conflict rule

The current governing order is:

1. explicit current owner instruction in the active conversation, when it intentionally changes the workflow/requirement;
2. `WORKFLOW_OPERATING_RULES.md` for operating-process/role/environment rules;
3. `CURRENT_STATE.md` for current control-plane facts and stage;
4. current living product contracts: `PROJECT_PURPOSE.md`, `SPECIFICATION.md`, `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`;
5. `ROADMAP.md` for phase progression and historical/current status narrative;
6. append-only context and historical evidence for provenance only.

A lower-precedence or historical document must never silently override a higher-precedence current contract.

**If two current canonical documents materially contradict each other, STOP before code/QA/handoff. Do not choose one by intuition. Reconcile the documents first, record the correction, reconstruct current state again, then continue.** Historical superseded text may remain only when explicitly labeled historical/superseded.

## Mandatory workflow-transition reconstruction

Reconstruct current state not only before new development, but **before every transition between workflow stages**, including:

- immediately after a persistent workflow/governance correction in the current conversation;
- new conversation / resumed conversation;
- requirement → development;
- development → candidate freeze;
- freeze → Codex gate;
- Codex PASS/FAIL → next action;
- failure → repair;
- full-gate PASS → owner handoff/live acceptance;
- owner live PASS/FAIL → phase close/reopen;
- any GitHub documentation/governance change that may affect authority or the next permitted step.

At each transition, explicitly establish from live GitHub/current evidence:

```text
live HEAD
current canonical docs
exact product source identity
exact handoff artifact identity/SHA/bytes
latest gate verdict and candidate authority
open blockers/issues
owner-live acceptance status
whether production bytes changed
only authorized next stage
```

If any of these is unresolved or contradictory, do not improvise the next stage.

## Mandatory development / pre-delivery test rule

There are two different testing stages and they must not be confused:

- **During implementation/bug fixing:** run focused tests for the code being changed, directly affected dependencies, required changed-line/branch coverage, and relevant syntax/static checks. Do not run the entire product regression gate after every edit.
- **Immediately before handing a working extension build/candidate to the owner:** freeze the exact candidate and make Codex run `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` as **one complete regression campaign covering all functionality Codex can validate**. The full gate is mandatory before handoff.

If the pre-delivery gate finds any mandatory FAIL, the build is not handed off. Apply the failure-containment rules in `WORKFLOW_OPERATING_RULES.md`, fix only the proven failing layer, then rerun the entire gate from the beginning if production bytes changed or if the living gate explicitly requires a fresh complete campaign.

`CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` is a living registry: add tests when functionality is added or changed; remove obsolete tests only when the corresponding product functionality is intentionally removed. Never delete a test merely because it fails.

Controlled Codex/Puppeteer evidence and real-profile/live acceptance remain distinct. The full pre-delivery gate covers every reliably Codex-testable surface; it does not fabricate a real-profile/live PASS.

## Owner-correction rule

When the owner corrects a repeated workflow, role, safety, QA, handoff or authority rule, ChatGPT must classify it immediately in the **current conversation**:

- **one-off instruction** — applies only to the current action; or
- **persistent invariant** — applies immediately and must be canonicalized into the appropriate current document before proceeding far enough that the same mistake can recur.

For a persistent invariant, ChatGPT must inspect current canonical documents for conflicting text, reconcile them and reconstruct current state. Do not leave a permanent owner correction only in chat memory and do not defer its effect until a future chat.

## Reference / architecture

- `REFERENCE_BASELINE.md` — owner-supplied Wordstat reference identity/hashes.
- `PHASE_0_REFERENCE_AUDIT.md` — Phase 0 exact reference audit.
- `CORE_EXTRACTION_MAP.md` — frozen/common/generic/service-specific extraction map.
- `ORDER_WORKSPACE_LIFECYCLE.md` — external ChatGPT/GitHub order-workspace lifecycle; this is not extension runtime.
- `PHASE_1_WORDSTAT_IMPLEMENTATION_PLAN.md` — historical Phase 1 implementation plan; some Job-runtime assumptions are superseded by current correction history/spec.

## Current implementation / live gate

Current exact candidate, gate verdict and authorized next stage are read from `CURRENT_STATE.md`, not from old candidate blocks in historical evidence.

Current mandatory owner-live procedure for Phase 1 is:

- `PHASE_1_0.1.1_LIVE_ACCEPTANCE.md`

The old ledger below is retained as **historical test/evidence provenance only** and must not be used as current candidate or current live procedure authority:

- `../tests/PHASE_1_0.1.1_LIVE_TEST_PLAN_AND_RESULTS.md`

The permanent controlled pre-delivery regression gate is separate:

- `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`

## Machine-readable evidence / WIP recovery

Current evidence is under `extension/tests/`, including governed phase checkpoints, validation reports and reconstruction/package manifests. Historical 0.1.0/earlier candidate evidence remains history and must not override `CURRENT_STATE.md` or current live GitHub state.

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
- current Manual delivery completion is Send→ready/Microphone based; obsolete sent-user-turn `manual_reconcile`/12-attempt exhaustion is not current behavior.

## Source of truth rule

Before any new development action **or workflow-stage transition, including the next action in the current conversation after a persistent correction**:

1. connect to live GitHub;
2. fetch current branch HEAD and commit metadata;
3. read this index, `WORKFLOW_OPERATING_RULES.md`, `CURRENT_STATE.md`, current purpose/spec/roadmap, the current regression-gate rule and the append-only context chain as required by the change;
4. verify current phase/gate/handoff state;
5. resolve any canonical-document conflict before action;
6. only then modify code, QA infrastructure, governance, or run external paid operations.

Do not use chat memory, old handoff text, historical evidence or remembered SHA as authority when live GitHub can answer the question.
