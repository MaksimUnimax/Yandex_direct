# KW-002 / BLOOD & SAND — STEP07 BROWSER RECOVERY RESIDUAL CLOSURE — MAIN CHAT RETURN QA

Date: 2026-09-17
Status: **REJECTED / HONEST INCOMPLETE / SWITCH BROWSER EXECUTOR**

## 1. Live authority

```text
LIVE_REMOTE_HEAD = 302f55813b2729d8b73c1a281e3fbc680c6f9d51
CURRENT_MAIN_CHAT_ACTION = STEP07_BROWSER_RECOVERY_RESIDUAL_CLOSURE_RETURN_ACCEPTANCE
MAIN_CHAT_EXECUTION_ALLOWED = true
```

Freshly reread before acceptance:

- `LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`
- `LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md`
- `LEVEL1/COMMON_RULES.md`
- `LEVEL1/RESULT_QUALITY_SCORING_RULE.md`
- `LEVEL1/WORK_HANDOFF_RULE.md`
- `LEVEL2/STEP_07_COMPETITOR_SEMANTIC_EXPANSION.md`
- current `JOB_FLOW.md`
- current `KW002_EXECUTION_CURSOR_2026-09-17.json`
- `STEP07_BROWSER_RECOVERY_CODEX_RESIDUAL_CLOSURE_PROMPT_V2_2026-09-17.md`
- `STEP07_BROWSER_RECOVERY_CODEX_RESIDUAL_CLOSURE_PROMPT_2026-09-17.md`

## 2. Package reviewed

Owner returned exactly seven standalone files plus one transport ZIP:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
STEP07_BROWSER_RECOVERY_COVERAGE.csv
STEP07_BROWSER_RECOVERY_QA.md
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv
STEP07_BROWSER_RECOVERY_RESIDUAL_RETRY_AUDIT.csv
```

Independent SHA-256:

```text
URL_LEDGER = 18dfa2348bce2a68fa24992623179d939fec8d939d09798b4dc1f2e7d6ebfd4d
PAGE_EVIDENCE = 5fc4266f1c235a567744a0ad6bcab8da5208dca4e94e6785d60801b09448e1d9
COVERAGE = 9d79dbc35af5c5b65ebe7fd0cc6786cd55a91091bc075753337b1e5ea2cce15d
QA = 090fecf601e20cc884a4304001644befd84df04468b45abac3edc0c1d30fd1b3
VERIFIED_80_RETRY_AUDIT = 1cbe984c47854eeb55eb1a1a07fc3134a030a1a841cd6a7f22e82326a01295a6
RESIDUAL_RETRY_AUDIT = 6dc03e2d8b1a2c918df4188242b17ff8b9c5a8a082f861a9c91472afd1d0861b
MANIFEST_ACTUAL = 5f3210b7a961686644d58f050c7f3be3b483246f82337b1ba930cbfd3d2976ad
TRANSPORT_ZIP = 2fb123fc53366b96454461ec04c8ebc2ffbd70b0f5454f63327d4dc7764f4ad5
```

ZIP contains exactly the same seven files byte-for-byte.

## 3. What passes

The executor finally obeyed the frozen residual correction scope.

```text
SOURCE_URL_ROWS = 1976
AUTHORIZED_COMPETITORS = 32
TOTAL_FROZEN_CORRECTION_ROWS = 129
ROWS_CHANGED_OUTSIDE_FROZEN_SET = 0
DETERMINISTIC_CORRECTION_ROWS = 39
DETERMINISTIC_SAME_URL_FALSE_REDIRECT_ROWS_FIXED = 39/39
RESIDUAL_BROWSER_RETRY_ROWS = 90
RESIDUAL_RETRY_AUDIT_ROWS = 90
UNIQUE_RESIDUAL_RETRY_IDS = 90
MISSING_FROZEN_BROWSER_RETRY_IDS = 0
EXTRA_BROWSER_RETRY_IDS = 0
browser_navigation_attempted = true on 90/90
browser_route = true on 90/90
attempt_count = 2 on 90/90
```

The 39 deterministic false redirects are correctly reclassified to `RECOVERED_INSPECTED`; their existing evidence IDs/text/hashes are preserved.

Primary data checks:

```text
URL_LEDGER_SCHEMA = PASS
COVERAGE_SCHEMA = PASS
PAGE_EVIDENCE_SCHEMA = PASS
URL_PK_UNIQUE = PASS
EVIDENCE_PK_UNIQUE = PASS
PAGE_EVIDENCE_ROWS = 659
PAGE_EVIDENCE_JOINS = PASS
PAGE_EVIDENCE_SHA256_TEXT_IDENTITY = PASS
NOT_COLLECTED_ON_INSPECTED = 0
SAME_URL_EMPTY_CHAIN_REDIRECT_ROWS_FINAL = 0
AZBYKA_CHALLENGE_MISCLASSIFIED_AS_CONTENT = 0
KARTASLOV_NORMAL_PAGE_FALSE_TARGET_BLOCK = 0
CHALLENGE_PAGE_MISCLASSIFIED_AS_INSPECTED_OR_REDIRECT = 0
COVERAGE_REMAINING_FIELD_RECONCILES = PASS
UNAUTHORIZED_DOMAIN_ROWS = 0
UNAUTHORIZED_SITEMAP_REFERENCES = 0
PROVIDER_CALLS = 0
STEP08_EXECUTED = false
CANDIDATE_CLASSIFICATION_EXECUTED = false
```

The previous four Azbyka challenge evidence rows are removed from ordinary semantic page evidence. The two Sokolov target-challenge rows remain explicit target-block evidence.

Coverage ledger now correctly derives:

```text
recovery_urls_attempted
recovery_inspected_urls
recovery_target_blocked_urls
recovery_environment_failure_urls
remaining_unresolved_or_environment_failure_urls
recovery_status
```

from the final URL ledger for all 32 competitors.

Manifest identity is materially corrected:

```text
artifact_set = KW002_STEP07_BROWSER_RECOVERY_RESIDUAL_CLOSURE
start_remote_head = 302f55813b2729d8b73c1a281e3fbc680c6f9d51
pre_handoff_remote_head = 302f55813b2729d8b73c1a281e3fbc680c6f9d51
self byte_size = 2501 = actual
seven-file manifest = complete
```

## 4. Hard failure — browser recovery remains incomplete

Final URL terminal counts are:

```text
EXCLUDED_OUT_OF_SCOPE = 1201
EXCLUDED_DUPLICATE = 24
RECOVERED_INSPECTED = 366
REDIRECTED_IN_SCOPE = 293
TARGET_CAPTCHA_OR_ANTI_BOT = 2
EXECUTION_ENVIRONMENT_FAILURE = 90
UNRESOLVED_DYNAMIC_CONTENT = 0
TOTAL = 1976
```

Therefore:

```text
FINAL_UNRESOLVED_DYNAMIC_CONTENT_TOTAL = 0
FINAL_EXECUTION_ENVIRONMENT_FAILURE_TOTAL = 90
FINAL_RESIDUAL_ACQUISITION_GAPS = 90
```

The controlling residual-closure contract explicitly requires:

```text
FINAL_RESIDUAL_ACQUISITION_GAPS = 0
```

for browser-recovery PASS.

Hard gate = FAIL.

## 5. Exact residual environment root cause

The 90-row residual retry audit is no longer a synthetic relabel. It records real attempted browser actions and exact final failures.

Independent parsing of all 90 `exact_final_error_detail` values shows:

```text
82 = browser navigation reached a Chromium error page containing ERR_TIMED_OUT;
     the executor then could not inspect that internal data:text/html error page because Browser Use URL policy blocks it.

8 = explicit Browser Use site-safety policy blocks on Avito URLs.
```

Domain distribution:

```text
ERR_TIMED_OUT / browser-error-page path:
  wildberries.ru = 23
  market.yandex.ru = 20
  livemaster.ru = 11
  ru.ruwiki.ru = 8
  kartaslov.ru = 4
  goroskop365.ru = 4
  azbyka.ru = 4
  sibpodkova.ru = 3
  aliexpress.ru = 2
  joom.ru = 2
  ru.wikipedia.org = 1

Browser site-safety policy:
  avito.ru = 8
```

This matters because Main Chat already has prior normal-browser Opera evidence that several affected hosts are readable (`ru.wikipedia.org`, `sibpodkova.ru`, Kartaslov and other competitor sites). Therefore these 90 rows are not target-site semantic closure. They are a demonstrated limit of the current Codex Browser Use environment.

Repeating the same 90 through the same executor is not justified.

## 6. Quality score

Each criterion independently 0–10:

```text
GOAL_AND_OUTPUT_COMPLETENESS = 7.5/10
METHOD_AND_SOURCE_SUPPORT = 9.0/10
INPUT_EVIDENCE_AND_PROVENANCE_INTEGRITY = 9.5/10
COVERAGE_AND_COMPLETENESS = 4.0/10
ANALYTICAL_CORRECTNESS_AND_CLAIM_BOUNDARIES = 9.0/10
ADVERSARIAL_QA_QUALITY = 8.5/10
PERSISTENCE_READBACK_AND_REPRODUCIBILITY = 9.5/10
OWNER_CLIENT_USABILITY_AND_PLAIN_LANGUAGE = 8.0/10
INFORMATION_GAIN_COST_AND_EXECUTION_EFFICIENCY = 5.5/10
DOWNSTREAM_READINESS = 4.0/10

QUALITY_TOTAL = 74.5 / 100
QUALITY_SCORE = 7.45 / 10
```

What is good:

- frozen scope obeyed exactly;
- 39 deterministic fixes are correct;
- 90 browser attempts are now auditable rather than fabricated;
- evidence integrity, hashes, joins, coverage and manifest are clean;
- the executor truthfully returned `INCOMPLETE` instead of forcing PASS.

What blocks PASS:

- 90 required public-page outcomes remain environment failures;
- Step07 full-volume browser-recovery contract requires those acquisition gaps to be closed or converted to legitimate target-level evidence;
- semantic rework cannot safely treat executor failures as competitor-page closure.

## 7. Acceptance decision

```text
RESIDUAL_CLOSURE_OWNER_RETURN = RECEIVED
MECHANICAL_FILE_IDENTITY = PASS
FROZEN_SCOPE_COMPLIANCE = PASS
DETERMINISTIC_CORRECTIONS = PASS
RESIDUAL_RETRY_AUDIT = PASS
ANALYTICAL_RETURN_QA = FAIL_INCOMPLETE
BROWSER_RECOVERY_ACCEPTED = false
CANONICAL_RECOVERY_PUBLICATION = BLOCKED
STEP07_SEMANTIC_REWORK = BLOCKED_PENDING_BROWSER_RECOVERY
STEP08 = BLOCKED_NOT_STARTED
```

## 8. Executor switch / exact next action

Do NOT send these 90 rows back to the same Codex Browser Use environment again.

Reuse the exact already-frozen 90 browser rows from:

`STEP07_BROWSER_RECOVERY_RESIDUAL_CORRECTION_SET_2026-09-17.csv`

where:

`browser_retry_required = true`

Next executor:

```text
MAIN CHAT + OWNER-CONNECTED OPERA BROWSER CONNECTOR
```

No new methodology, no new URL universe, no provider calls, no Step08.

Current external blocker at acceptance time:

```text
OPERA_BROWSER_CONNECTOR = NOT_CONNECTED
```

When Opera connection is restored, Main Chat executes the exact frozen 90-row browser residual universe, preserves target-level evidence / real page evidence, merges the resulting states into the accepted recovery package, and reruns Main Chat acceptance.

Until then:

```text
STEP07_BROWSER_RECOVERY = INCOMPLETE_EXECUTION_ENVIRONMENT_FAILURES
```
