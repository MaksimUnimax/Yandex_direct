# Documentation index

Canonical documentation for Yandex Marketing Bridge.

## Read first in every development conversation

1. `PROJECT_PURPOSE.md` — current product boundary and separation of Bridge runtime from external GitHub workflow.
2. `SPECIFICATION.md` — current technical contract.
3. `ROADMAP.md` — current phase/gate status.
4. `DEVELOPMENT_CONTEXT_APPEND_ONLY.md` — immutable historical entries 0001–0021.
5. `DEVELOPMENT_CONTEXT_APPEND_ONLY_CONTINUATION_0.1.1.md` — append-only correction/continuation entries 0022+.

The two development-context files form one chronological append-only chain. Do not rewrite the parent to hide superseded decisions.

## Reference / architecture

- `REFERENCE_BASELINE.md` — owner-supplied Wordstat reference identity/hashes.
- `PHASE_0_REFERENCE_AUDIT.md` — Phase 0 exact reference audit.
- `CORE_EXTRACTION_MAP.md` — frozen/common/generic/service-specific extraction map.
- `ORDER_WORKSPACE_LIFECYCLE.md` — external ChatGPT/GitHub order-workspace lifecycle; this is not extension runtime.
- `PHASE_1_WORDSTAT_IMPLEMENTATION_PLAN.md` — historical Phase 1 implementation plan; some Job-runtime assumptions are superseded by 0.1.1 correction history/spec.

## Current implementation gate

Current candidate:

```text
yandex-marketing-bridge-0.1.1-phase1-repair-candidate.zip
SHA-256 311353e2671052b7170e12db3e1318dfed4f59ccf945c7eda6ec59152ee3abfb
```

Current status:

```text
PHASE 0  PASS
PHASE 1  0.1.0 WITHDRAWN
PHASE 1  0.1.1 PRE-LIVE PASS / PRODUCTION LIVE PENDING
PHASE 2  BLOCKED
```

Mandatory live procedure:

- `PHASE_1_0.1.1_LIVE_ACCEPTANCE.md`

Historical 0.1.0 live procedure remains as history and must not be used as authority for the repaired candidate.

## Machine-readable evidence / WIP recovery

```text
extension/tests/PHASE_1_0.1.1_PRELIVE_TEST_EVIDENCE.json
extension/tests/PHASE_1_CANDIDATE_SOURCE_MANIFEST.json              # historical 0.1.0 evidence
extension/tests/PHASE_1_PRELIVE_TEST_EVIDENCE.json                 # historical 0.1.0 evidence
extension/tests/wip/phase1-0.1.1-repair/                           # repair checkpoints
```

## Current architectural corrections

- no mandatory `job_id` in extension runtime;
- no GitHub API/workspace dependency in extension runtime;
- all errors automatically return to bound ChatGPT regardless of Debug Mode;
- Debug Mode adds only extra redacted logs;
- Export/Import secret settings backup with checksum validation;
- active RUN/manual-operation safety state preserved on import;
- Manual on PAUSED RUN shares the same RUN budget;
- no blind retry after uncertain request outcome.

## Source of truth rule

Before any new development action:

1. connect to live GitHub;
2. fetch current branch HEAD and commit metadata;
3. read this index, current purpose/spec/roadmap and the append-only context chain;
4. verify current phase gate;
5. only then modify code or run external paid operations.

Do not use chat memory, old handoff text, historical 0.1.0 evidence or remembered SHA as authority when live GitHub can answer the question.
