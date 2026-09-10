# MK01 / OKNO_MSK — historical client PDF correction QA

Status: **SUPERSEDED BY ANALYTICAL REBUILD 2026-09-10**

This file is retained only as historical evidence that the first PDF-report correction passed numerical, language and physical checks.

It is **not the current client-report acceptance authority**.

## Why it was superseded

The PDF dated 2026-09-09 was numerically correct and physically readable, but later owner review found a higher-level defect: the document behaved too much like an execution protocol. It explained what was done and how many rows existed more strongly than what the semantic research actually showed about demand structure.

The earlier `25 PASS / 0 FAIL` therefore proved only the checks that existed at that time; those checks were incomplete.

Permanent failure classes introduced by the correction:

- **E38 — client PDF became an execution protocol instead of an analytical report**;
- **E39 — page count was used as a proxy for report quality**.

## Current authority

Use instead:

- `CLIENT_REPORT_SOURCE_2026-09-10.md`;
- `CLIENT_REPORT_ARTIFACT_MANIFEST_2026-09-10.json`;
- `PHASE_6_CLIENT_REPORT_REBUILD_QA_2026-09-10.md`;
- current `CLIENT_REPORT_SPEC.md`;
- current `steps/STEP_10_CLIENT_MATERIALIZATION_QA.md`.

Current reviewed client-report binary identity:

```text
MK01_OKNO_MSK_CLIENT_REPORT_2026-09-10.pdf
SHA-256 = 9faae858b40a5e6617019f0688759d11034f27d4d800b3b46dc180461788764b
```

The old report and this old QA must not be used as templates for new MK01 orders.
