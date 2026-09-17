# KW-002 / BLOOD & SAND — STEP07 BROWSER RECOVERY — CODEX RESIDUAL CLOSURE V2

Status: **CURRENT / EXECUTION-ONLY / FROZEN SCOPE OVERLAY**

This file is the current execution entry point for the Step07 browser-recovery residual closure.

It does NOT replace the method and output contract in:

`STEP07_BROWSER_RECOVERY_CODEX_RESIDUAL_CLOSURE_PROMPT_2026-09-17.md`

It freezes the exact correction/retry universe so the executor must not infer it again.

Repository: `MaksimUnimax/Yandex_direct`
Branch: `roadmap/kwork-productization-2026-08-28`
Job root: `extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

## 1. Startup

Fetch the CURRENT live branch.

Read IN FULL, in this order:

```text
STEP07_BROWSER_RECOVERY_VERIFIED_80_RETURN_MAIN_CHAT_QA_2026-09-17.md
STEP07_BROWSER_RECOVERY_CODEX_RESIDUAL_CLOSURE_PROMPT_V2_2026-09-17.md
STEP07_BROWSER_RECOVERY_CODEX_RESIDUAL_CLOSURE_PROMPT_2026-09-17.md
STEP07_BROWSER_RECOVERY_RESIDUAL_CORRECTION_SET_2026-09-17.csv
STEP07_OPERA_BROWSER_CONTROL_PROBE_2026-09-17.md
STEP_07_AUTHORIZED_COMPETITOR_UNIVERSE.csv
```

Use the latest owner-returned verified-80 six-file package in the current Codex workspace as the base.

Do NOT redo Main Chat governance/research/release work.
Do NOT make provider calls.
Do NOT start Step08.
Do NOT perform Step07 semantic candidate classification.
Do NOT commit/push/PR.

## 2. Frozen correction authority

The ONLY correction/retry universe is:

`STEP07_BROWSER_RECOVERY_RESIDUAL_CORRECTION_SET_2026-09-17.csv`

Expected exact file structure:

```text
correction_class
browser_retry_required
recovery_url_id
```

Expected exact counts:

```text
TOTAL_CORRECTION_ROWS = 129

DETERMINISTIC_RECLASSIFY_SAME_URL_REDIRECT = 39
AZBYKA_DDOS_CHALLENGE_RETRY = 4
KARTASLOV_FALSE_TARGET_BLOCK_RETRY = 1
RESIDUAL_EXECUTION_ENVIRONMENT_FAILURE_RETRY = 51
RESIDUAL_UNRESOLVED_DYNAMIC_CONTENT_RETRY = 34

browser_retry_required=false = 39
browser_retry_required=true = 90
```

Hard rule:

```text
DO NOT DERIVE / REBUILD / EXPAND / SHRINK THE CORRECTION SET.
```

Join every correction row to the base `STEP07_BROWSER_RECOVERY_URL_LEDGER.csv` by `recovery_url_id` before execution.

If any ID is missing, duplicated, or does not match the expected base state described by Main Chat QA, stop with `RESIDUAL_SET_DRIFT`.

## 3. Execution

For the 39 rows with:

`browser_retry_required=false`

apply exactly the deterministic same-URL false-redirect correction defined in the base residual-closure prompt. No new browser action is required for those rows.

For the 90 rows with:

`browser_retry_required=true`

perform real browser navigation exactly as required by the base residual-closure prompt and create one row per retry in:

`STEP07_BROWSER_RECOVERY_RESIDUAL_RETRY_AUDIT.csv`

Required proof:

```text
RESIDUAL_RETRY_AUDIT_ROWS = 90
UNIQUE_RESIDUAL_RETRY_IDS = 90
MISSING_FROZEN_BROWSER_RETRY_IDS = 0
EXTRA_BROWSER_RETRY_IDS = 0
ACTUAL_BROWSER_NAVIGATION_ATTEMPTED = 90/90
```

The exact correction CSV, not an error query, controls which rows are processed.

## 4. Preserve everything else

Rows/evidence outside the frozen 129-row correction set must remain unchanged except deterministic coverage totals, terminal-count totals, QA summaries and manifest metadata caused by corrected rows.

Do NOT restart the 1976-URL collection.

## 5. Required output

Follow the base residual-closure prompt in full.

Return exactly seven files plus one transport ZIP:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
STEP07_BROWSER_RECOVERY_COVERAGE.csv
STEP07_BROWSER_RECOVERY_QA.md
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv
STEP07_BROWSER_RECOVERY_RESIDUAL_RETRY_AUDIT.csv
```

The existing verified-80 retry audit is preserved; the residual retry audit is new.

## 6. Pass boundary

Do not declare browser recovery PASS merely because all 90 retries were attempted.

The final package must satisfy every hard QA condition in the base residual-closure prompt, including truthful coverage accounting and:

```text
FINAL_RESIDUAL_ACQUISITION_GAPS = 0
```

If residual `EXECUTION_ENVIRONMENT_FAILURE` or `UNRESOLVED_DYNAMIC_CONTENT` rows remain after the allowed legitimate retries, return the package truthfully as `INCOMPLETE` with exact evidence; do not relabel them to force PASS.
