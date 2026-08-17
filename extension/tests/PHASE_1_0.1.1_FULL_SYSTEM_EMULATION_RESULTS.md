# Phase 1 0.1.1 — full-system exhaustive emulation results

Date: 2026-08-17
Candidate: `yandex-marketing-bridge-0.1.1-phase1-k02-generic-dom-patch-candidate.zip`
SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`
Plan: `PHASE_1_0.1.1_FULL_SYSTEM_EMULATION_PLAN.md`

## R0 — exploratory baseline (not counted as governed closure)

- exact ZIP hash rechecked: MATCH;
- fresh extraction file count: 42;
- built-in package suite: 319/319 PASS;
- Node test-runner aggregate coverage over the test harness: line 99.37%, branch 92.36%, functions 95.72%. This metric does not by itself prove production runtime coverage because several production files are executed through VM/browser harnesses.

## R1 — FSE-02 initial independent pure-module input/output matrix

Status: **TEST ERROR CANDIDATE — expectations must be audited before any product defect is inferred.**

Raw result:

```text
80 cases
73 PASS
7 apparent FAIL
```

Apparent failures:

1. `CI-2`, `CI-3`, `CI-4`: harness used deliberately short fake conversation ids (`ABC-123`, `xyz`, `a`, `b`) while the production identity module validates ChatGPT conversation-id shape. The expected `confirmed/conflict` classifications are therefore not yet justified.
2. `AUTO-prefix-N2-b`: harness expected the prefix due-state from an assumed `confirmed_count` contract without first verifying the module's public prefix-record fields.
3. `AUTO-commit-start`: harness inspected a nonexistent top-level `start_phase`; production model stores start state in `start_delivery.phase`.
4. `AUTO-claim-delivery` and `AUTO-commit-delivery`: harness inspected a nonexistent top-level `delivery_phase`; production model stores delivery state in `delivery.phase`. The raw returned objects visibly contain the expected claimed/committed phases inside the nested delivery record.

No production patch is authorized from R1. Next step is to audit the module public contracts, correct only the harness expectations that are demonstrably wrong, and rerun the same input corpus. No Yandex network request occurred.
