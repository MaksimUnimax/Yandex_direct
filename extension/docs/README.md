# Documentation index

Canonical documentation for Yandex Marketing Bridge.

## Read first in every development conversation

1. `PROJECT_PURPOSE.md` — current product boundary and separation of Bridge runtime from external GitHub workflow.
2. `SPECIFICATION.md` — current technical contract.
3. `ROADMAP.md` — current phase/gate status.
4. `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` — permanent living regression firewall. **Run it only immediately before handing the owner a working build; during development run focused tests for changed code/dependencies only.**
5. `DEVELOPMENT_CONTEXT_APPEND_ONLY.md` — immutable historical entries 0001–0021.
6. `DEVELOPMENT_CONTEXT_APPEND_ONLY_CONTINUATION_0.1.1.md` — append-only correction/continuation entries 0022+.

The two development-context files form one chronological append-only chain. Do not rewrite the parent to hide superseded decisions.

## Mandatory development / pre-delivery test rule

There are two different testing stages and they must not be confused:

- **During implementation/bug fixing:** run focused tests for the code being changed, directly affected dependencies, required changed-line/branch coverage, and relevant syntax/static checks. Do not run the entire product regression gate after every edit.
- **Immediately before handing a working extension build/candidate to the owner:** freeze the exact candidate and make Codex run `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` as **one complete regression campaign covering all functionality Codex can validate**. The full gate is mandatory before handoff.

If the pre-delivery gate finds any mandatory FAIL, the build is not handed off. Fix the defect with focused development tests, then rerun the **entire gate from the beginning** against the new exact candidate.

`CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` is a living registry: add tests when functionality is added or changed; remove obsolete tests only when the corresponding product functionality is intentionally removed. Never delete a test merely because it fails.

Controlled Codex/Puppeteer evidence and real-profile/live acceptance remain distinct. The full pre-delivery gate covers every reliably Codex-testable surface; it does not fabricate a real-profile/live PASS.

## Reference / architecture

- `REFERENCE_BASELINE.md` — owner-supplied Wordstat reference identity/hashes.
- `PHASE_0_REFERENCE_AUDIT.md` — Phase 0 exact reference audit.
- `CORE_EXTRACTION_MAP.md` — frozen/common/generic/service-specific extraction map.
- `ORDER_WORKSPACE_LIFECYCLE.md` — external ChatGPT/GitHub order-workspace lifecycle; this is not extension runtime.
- `PHASE_1_WORDSTAT_IMPLEMENTATION_PLAN.md` — historical Phase 1 implementation plan; some Job-runtime assumptions are superseded by 0.1.1 correction history/spec.

## Current implementation gate

Current historical candidate references and phase-specific acceptance records live in the roadmap/ledger and test evidence. Do not use the stale candidate block from an older checkpoint as current authority.

Mandatory phase/live procedure for current Phase 1 remains governed by:

- `PHASE_1_0.1.1_LIVE_ACCEPTANCE.md`
- `../tests/PHASE_1_0.1.1_LIVE_TEST_PLAN_AND_RESULTS.md`

The permanent pre-delivery regression gate is separate:

- `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`

## Machine-readable evidence / WIP recovery

Current evidence is under `extension/tests/`, including governed phase checkpoints, validation reports and reconstruction/package manifests. Historical 0.1.0/earlier candidate evidence remains history and must not override current live GitHub state.

## Current architectural corrections

- no mandatory `job_id` in extension runtime;
- no GitHub API/workspace dependency in extension runtime;
- all errors automatically return to bound ChatGPT regardless of Debug Mode;
- Debug Mode adds only extra redacted logs;
- Export/Import secret settings backup with checksum validation;
- active RUN/manual-operation safety state preserved on import;
- Manual on PAUSED RUN shares the same RUN budget;
- no blind retry after uncertain request outcome;
- Manual Surface v2 decoration is content-independent while Manual is ON and binding is unambiguous.

## Source of truth rule

Before any new development action:

1. connect to live GitHub;
2. fetch current branch HEAD and commit metadata;
3. read this index, current purpose/spec/roadmap, the current regression-gate rule and the append-only context chain;
4. verify current phase gate;
5. only then modify code or run external paid operations.

Do not use chat memory, old handoff text, historical evidence or remembered SHA as authority when live GitHub can answer the question.