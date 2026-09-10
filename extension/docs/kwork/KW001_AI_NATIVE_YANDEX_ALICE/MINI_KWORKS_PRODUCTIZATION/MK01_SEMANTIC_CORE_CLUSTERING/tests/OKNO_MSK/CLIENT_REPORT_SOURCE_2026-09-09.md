# MK01 / OKNO_MSK — historical client report source 2026-09-09

Status: **SUPERSEDED — DO NOT USE AS CURRENT CLIENT REPORT TEMPLATE**

The original source is preserved in Git history. This branch-level file is intentionally reduced to a tombstone so a future executor cannot accidentally regenerate the rejected report as the current MK01 client deliverable.

## Reason for supersession

The 2026-09-09 report was numerically correct and physically readable, but owner review found that it behaved too much like an execution protocol. It emphasized process chronology and row counts while under-explaining what the semantic research showed about demand structure.

Permanent controls now classify this as:

- **E38 — client PDF became an execution protocol instead of an analytical report**;
- **E39 — page count was used as a proxy for report quality**.

## Current report source

Use:

`CLIENT_REPORT_SOURCE_2026-09-10.md`

Current client report must follow:

- `../../CLIENT_REPORT_SPEC.md`;
- `../../steps/STEP_10_CLIENT_MATERIALIZATION_QA.md`;
- `PHASE_6_CLIENT_REPORT_REBUILD_QA_2026-09-10.md`.

Canonical anti-repeat rule:

```text
CLIENT REPORT != EXECUTION PROTOCOL
CORRECT COUNTS + CLEAN LAYOUT != ANALYTICAL REPORT PASS
```
