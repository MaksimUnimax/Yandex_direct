# KW-002 / BLOOD & SAND — STEP07 BROWSER RECOVERY VERIFIED 80-URL RETURN — MAIN CHAT QA

Date: 2026-09-17
Status: **REJECTED / RESIDUAL CLOSURE REQUIRED**

## 1. Live authority / Main Chat readback

```text
LIVE_REMOTE_HEAD = b87750e082c30cbc6bbb2c86994828cb1a7f3642
CURRENT_MAIN_CHAT_ACTION = STEP07_BROWSER_RECOVERY_VERIFIED_80_RETURN_ACCEPTANCE
MAIN_CHAT_EXECUTION_ALLOWED = true
```

Freshly reread from the live branch before acceptance:

- `LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`
- `LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md`
- `LEVEL1/COMMON_RULES.md`
- `LEVEL1/RESULT_QUALITY_SCORING_RULE.md`
- `LEVEL1/WORK_HANDOFF_RULE.md`
- `LEVEL2/STEP_07_COMPETITOR_SEMANTIC_EXPANSION.md`
- current `JOB_FLOW.md`
- current `KW002_EXECUTION_CURSOR_2026-09-17.json`
- current verified 80-URL retry prompt / frozen retry set.

## 2. Package inspected

Owner returned six standalone files plus one ZIP:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
STEP07_BROWSER_RECOVERY_COVERAGE.csv
STEP07_BROWSER_RECOVERY_QA.md
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv
```

ZIP contains exactly the same six files byte-for-byte.

Independent SHA-256:

```text
URL_LEDGER = a56240dd8c2084fe2da415e7b87b8230cc28852d04a4fef762a0e906c48d6d95
PAGE_EVIDENCE = 0c21c243b9f873829b8b9a8666a1a0b4cce9b5b1c36dc9d0c06936bd42f23309
COVERAGE = ee36dce7b26019ece9d114d937a8cbd8109a285aaf2be2ae006d5d3e4c9fd4c1
QA = 14045db51fce14869f881aad391812a04278238bd80091a7287a6b3b6ae04457
RETRY_AUDIT = 1cbe984c47854eeb55eb1a1a07fc3134a030a1a841cd6a7f22e82326a01295a6
MANIFEST_ACTUAL = 82d2d4cb854458241ccf3e9bb3e90793d32b66c27ff79b24e693769d2e5fe3f5
TRANSPORT_ZIP = cb469a33a21bf22210aa37181dfa0ff0dd05054fc72746d7b38a9ef3d7eeb4e1
```

## 3. What now passes

The verified retry execution itself materially improved and is independently supported:

```text
FROZEN_RETRY_SET_ROWS = 80
RETRY_AUDIT_ROWS = 80
RETRY_AUDIT_UNIQUE_IDS = 80
SET_A = 47 / 47
SET_B = 30 / 30
SET_C = 1 / 1
SET_D = 2 / 2
browser_navigation_attempted = true on 80 / 80
audit browser_route = true on 80 / 80
row-specific retry timestamps present
final audit state joins final URL ledger = PASS
final audit page-evidence hashes resolve = PASS
```

Primary mechanical package checks also pass:

```text
SOURCE_URL_ROWS = 1976
AUTHORIZED_COMPETITORS = 32
URL_LEDGER_SCHEMA = PASS
COVERAGE_SCHEMA = PASS
PAGE_EVIDENCE_SCHEMA = PASS
RETRY_AUDIT_SCHEMA = PASS
URL_PK_UNIQUE = PASS
EVIDENCE_PK_UNIQUE = PASS
PAGE_EVIDENCE_ROWS = 663
EVIDENCE_JOINS = PASS
EVIDENCE_SHA256_FORMAT = PASS
EVIDENCE_SHA256_TEXT_IDENTITY = PASS
NOT_COLLECTED_ON_INSPECTED = 0
PROVIDER_CALLS = 0
STEP08_EXECUTED = false
CANDIDATE_CLASSIFICATION_EXECUTED = false
GIT_MUTATION = none
```

Returned terminal counts:

```text
EXCLUDED_OUT_OF_SCOPE = 1201
EXCLUDED_DUPLICATE = 24
RECOVERED_INSPECTED = 329
REDIRECTED_IN_SCOPE = 334
TARGET_CAPTCHA_OR_ANTI_BOT = 3
UNRESOLVED_DYNAMIC_CONTENT = 34
EXECUTION_ENVIRONMENT_FAILURE = 51
TOTAL = 1976
```

## 4. HARD FAILURE H1 — 85 URLs remain acquisition-incomplete

Current URL ledger still contains:

```text
EXECUTION_ENVIRONMENT_FAILURE = 51
UNRESOLVED_DYNAMIC_CONTENT = 34
TOTAL_RESIDUAL_ACQUISITION_GAPS = 85
```

Environment failures include, among others:

- `market.yandex.ru` — 20 navigation timeouts;
- `avito.ru` — 8 browser-policy/runtime failures;
- `ru.ruwiki.ru` — 8 navigation timeouts;
- `livemaster.ru` — 6 residual environment failures;
- `kartaslov.ru` — 3 residual environment failures;
- `sibpodkova.ru` — 3 navigation timeouts;
- `aliexpress.ru` — 2 navigation timeouts;
- `ru.wikipedia.org` — 1 browser runtime failure.

Main Chat already has independent Opera evidence that at least some affected hosts/pages are normally browser-readable (`ru.wikipedia.org`, `sibpodkova.ru`, several specialty sites). Therefore environment failure is not Step07 semantic closure.

Unresolved dynamic content is distributed as:

```text
wildberries.ru = 23
livemaster.ru = 5
joom.ru = 2
goroskop365.ru = 4
```

Step07 full-volume authority does not permit material unresolved coverage to be hidden behind aggregate terminal accounting.

Hard gate = FAIL.

## 5. HARD FAILURE H2 — four Azbyka DDoS-Guard challenge pages are misclassified as normal content

Page evidence for these exact rows is only a DDoS-Guard browser verification page:

```text
R9-S07U001947
R9-S07U001948
R9-S07U001949
R9-S07U001950
```

Evidence title/H1 includes:

```text
DDoS-Guard
Проверка браузера перед переходом на azbyka.ru
```

Yet final statuses are split between `RECOVERED_INSPECTED` and `REDIRECTED_IN_SCOPE`.

A browser verification/challenge page is not ordinary target content.

Required: retry normally; if challenge persists classify target challenge/block with exact evidence; if real page content loads collect it; if the executor fails first classify environment failure.

Hard gate = FAIL.

## 6. HARD FAILURE H3 — Kartaslov normal content is falsely classified as target anti-bot

Exact row:

`R9-S07U000396`

The returned retry audit/URL ledger classifies it as `TARGET_CAPTCHA_OR_ANTI_BOT`, but the captured text is a normal public Kartaslov association page (`Ассоциации к слову «дом»`) plus the site's normal `НАУЧИ БОТА!` interactive contribution widget.

The presence of a normal bot-training widget inside readable public page content is not an access challenge.

Required: normal browser retry and truthful access classification. If the public page is readable, store page evidence and classify as inspected.

Hard gate = FAIL.

## 7. HARD FAILURE H4 — 41 rows are called redirects without a redirect

Independent URL/evidence comparison found:

```text
REDIRECTED_IN_SCOPE_ROWS = 334
SOURCE_URL_EQUALS_FINAL_URL = 41
REDIRECT_CHAIN_EMPTY = 41 / 41
```

Among those 41:

- 2 are Azbyka DDoS-Guard challenge evidence and belong in the browser-retry set;
- 39 contain ordinary readable page evidence and require deterministic reclassification to `RECOVERED_INSPECTED` while preserving their existing evidence.

`REDIRECTED_IN_SCOPE` requires an actual redirect relation. Same URL + empty redirect chain is not a redirect.

Hard gate = FAIL.

## 8. HARD FAILURE H5 — coverage ledger suppresses all 34 unresolved URLs

The coverage table field is explicitly:

`remaining_unresolved_or_environment_failure_urls`

But current per-competitor values include only `EXECUTION_ENVIRONMENT_FAILURE` rows and omit every `UNRESOLVED_DYNAMIC_CONTENT` row.

Incorrect affected coverage rows:

```text
wildberries.ru: actual remaining = 23, reported = 0
livemaster.ru: actual remaining = 11, reported = 6
joom.ru: actual remaining = 2, reported = 0
goroskop365.ru: actual remaining = 4, reported = 0
```

All four are also labelled `COMPLETE_WITH_TRUTHFUL_ENV_FAILURES` despite unresolved dynamic coverage.

Required:

```text
remaining_unresolved_or_environment_failure_urls
= EXECUTION_ENVIRONMENT_FAILURE + UNRESOLVED_DYNAMIC_CONTENT
```

A competitor with non-zero unresolved dynamic coverage cannot be represented as complete.

Hard gate = FAIL.

## 9. Manifest metadata defects

Current manifest has several stale/non-exact control fields:

- `artifact_set = KW002_STEP07_BROWSER_RECOVERY_LIMITED_REWORK` although this return is the verified 80-URL retry;
- `codex_rework_start_remote_head` and `codex_pre_handoff_remote_head` still contain old `3191f221...` while the actual verified retry QA correctly reports `b87750e...` for start and pre-handoff;
- manifest terminal count uses alias `TARGET_BLOCKED = 3` while the canonical URL-ledger terminal state is `TARGET_CAPTCHA_OR_ANTI_BOT = 3`.

The manifest self byte-size defect from the previous return is fixed (`2254` actual bytes recorded), but the remaining metadata must be regenerated from the final corrected package.

## 10. Quality score

Each dimension independently scored 0–10:

```text
GOAL_AND_OUTPUT_COMPLETENESS = 8.0/10
METHOD_AND_SOURCE_SUPPORT = 8.5/10
INPUT_EVIDENCE_AND_PROVENANCE_INTEGRITY = 8.5/10
COVERAGE_AND_COMPLETENESS = 5.5/10
ANALYTICAL_CORRECTNESS_AND_CLAIM_BOUNDARIES = 5.0/10
ADVERSARIAL_QA_QUALITY = 5.0/10
PERSISTENCE_READBACK_AND_REPRODUCIBILITY = 7.5/10
OWNER_CLIENT_USABILITY_AND_PLAIN_LANGUAGE = 8.0/10
INFORMATION_GAIN_COST_AND_EXECUTION_EFFICIENCY = 7.0/10
DOWNSTREAM_READINESS = 4.5/10

QUALITY_TOTAL = 67.5 / 100
QUALITY_SCORE = 6.75 / 10
```

Points were lost because the 80-URL retry is finally auditable, but acquisition coverage is still materially incomplete and several target-state/redirect/coverage claims are demonstrably false.

Hard failures independently block PASS.

## 11. Acceptance decision

```text
VERIFIED_80_URL_RETRY_OWNER_RETURN = RECEIVED
80_URL_BROWSER_EXECUTION_PROOF = PASS
MECHANICAL_FILE_IDENTITY = PASS
ANALYTICAL_RETURN_QA = FAIL
BROWSER_RECOVERY_ACCEPTED = false
CANONICAL_RECOVERY_PUBLICATION = BLOCKED
STEP07_SEMANTIC_REWORK = BLOCKED_PENDING_RESIDUAL_CLOSURE
STEP08 = BLOCKED_NOT_STARTED
```

## 12. Exact next action

Run only the frozen residual-closure contract defined by:

- `STEP07_BROWSER_RECOVERY_RESIDUAL_CORRECTION_SET_2026-09-17.csv`
- `STEP07_BROWSER_RECOVERY_CODEX_RESIDUAL_CLOSURE_PROMPT_2026-09-17.md`

Do not restart the valid 1976-URL collection.
