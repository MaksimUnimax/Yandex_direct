# FSE R2 — corrected pure-module matrix

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`
Plan: `PHASE_1_0.1.1_FULL_SYSTEM_EMULATION_PLAN.md`

Status: **PASS**.

The initial R1 harness had seven invalid expectations/argument-shape assumptions and was recorded separately as TEST ERROR candidate. After source-contract audit, only those harness errors were corrected; the same 80-case corpus was rerun.

```text
80 cases
80 PASS
0 FAIL
```

Covered public contracts:

- conversation identity UUID path/canonical confirmation and conflict;
- service registry exact prefix detection;
- all four Wordstat methods and exact endpoint/body construction;
- malformed prefix/JSON/root/method inputs;
- getTop `numPhrases` lower/upper/out-of-range/fractional bounds;
- device/regions list validation and size limits;
- Dynamics period/date validation;
- Regions Distribution level validation;
- Unicode/NBSP command parsing;
- stable command fingerprint;
- bounded safe API-error payload;
- success report explicit `request_executed:true` / `automatic_retry:false` fields;
- credential capability states;
- policy normalization, allow/deny, credential, autorun/manual policy, method, request-limit and cost-limit decisions;
- standalone Manual no-run budget behavior;
- cost-ledger 50-operation accounting and nonnegative normalization;
- run-context service normalization/mismatch fences;
- generic/legacy/current Copy profile normalization, rejection, dedup and 24-profile cap;
- Autorun busy/manual eligibility, report-prefix due logic, start commit/confirm and delivery claim/commit public state contours.

No real/external Yandex network request occurred.
