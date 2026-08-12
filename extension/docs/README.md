# Documentation index

Canonical documentation for Yandex Marketing Bridge.

## Read first in every new development conversation

1. `PROJECT_PURPOSE.md` — зачем существует проект, границы и целевая рабочая модель.
2. `SPECIFICATION.md` — текущее техническое ТЗ/архитектурные требования.
3. `ROADMAP.md` — текущий phase/gate status и порядок: один сервис → один run → acceptance → следующий сервис.
4. `DEVELOPMENT_CONTEXT_APPEND_ONLY.md` — хронология решений, тестов, исправлений и gate-переходов. **APPEND ONLY.**

Then read phase/reference documents relevant to the current gate.

## Reference / architecture

- `REFERENCE_BASELINE.md` — идентификация и правила использования owner-supplied Wordstat reference.
- `PHASE_0_REFERENCE_AUDIT.md` — exact ZIP verification, reference authority, known stale-version defect and Phase 0 findings.
- `CORE_EXTRACTION_MAP.md` — что переносится как frozen common CORE, что genericized, что остаётся Wordstat adapter.
- `ORDER_WORKSPACE_LIFECYCLE.md` — как создаётся, наполняется, сохраняется и удаляется рабочая директория заказа.

## Current implementation gate

- `PHASE_1_WORDSTAT_IMPLEMENTATION_PLAN.md` — approved implementation plan for Wordstat + unified CORE.
- `PHASE_1_LIVE_ACCEPTANCE.md` — mandatory controlled real Chrome + production ChatGPT acceptance procedure for candidate `0.1.0`.

At the time of this index update:

```text
PHASE 0  PASS
PHASE 1  PRE-LIVE PASS / PRODUCTION LIVE PENDING
PHASE 2  BLOCKED
```

Do not begin Search implementation by relying on a stale chat summary; confirm live `ROADMAP.md` and append-only context first.

## Machine-readable evidence / inventories

Under repository paths:

```text
extension/reference/REFERENCE_INVENTORY.json
extension/tests/PHASE_1_CANDIDATE_SOURCE_MANIFEST.json
extension/tests/PHASE_1_PRELIVE_TEST_EVIDENCE.json
```

These identify exact reference/candidate hashes and pre-live test results.

## Update policy

- `PROJECT_PURPOSE.md` — living document; material purpose changes must also be recorded in the append-only context log.
- `SPECIFICATION.md` — living current specification; architecture changes must also be recorded in the append-only context log.
- `ROADMAP.md` — living current roadmap; phase/gate changes must also be recorded in the append-only context log.
- `REFERENCE_BASELINE.md` — stable baseline declaration; changes only when a new explicitly approved reference is adopted, with a new context-log entry.
- `PHASE_0_REFERENCE_AUDIT.md` — stable audit evidence; superseding findings are documented rather than silently rewriting history.
- `CORE_EXTRACTION_MAP.md` — architecture baseline; material changes require an append-only context entry.
- `ORDER_WORKSPACE_LIFECYCLE.md` — living operational contract; material changes recorded in context log.
- `PHASE_1_WORDSTAT_IMPLEMENTATION_PLAN.md` — Phase 1 plan/evidence baseline; later corrections are recorded explicitly.
- `PHASE_1_LIVE_ACCEPTANCE.md` — live acceptance procedure; observed results go to append-only context/evidence.
- `DEVELOPMENT_CONTEXT_APPEND_ONLY.md` — never rewrite history; only append new dated entries/corrections.

## Source of truth rule

Before continuing development in a new ChatGPT conversation:

1. connect to live GitHub;
2. fetch current branch HEAD/commit metadata;
3. read this index plus the current roadmap/spec/context;
4. verify current phase gate;
5. only then modify code or run paid external operations.

Do not rely on chat memory, a handoff prompt or remembered SHA when the live repository can answer the question directly.
