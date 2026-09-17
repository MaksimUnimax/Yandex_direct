# KW-002 JOB FLOW — BLOOD_SAND_GREENFIELD_2026-09-08

Updated: 2026-09-17

Current status: **STEP06 DURABLE PASS / STEP07 PREPARATION ACCEPTED / STEP07 ATTEMPT 1 REJECTED / BROWSER RECOVERY VERIFIED-80 RETURN REJECTED / RESIDUAL CLOSURE RELEASED TO CODEX / STEP07 SEMANTIC REWORK BLOCKED / STEP08 BLOCKED**

---

## 0. Role boundary

```text
MAIN CHAT
= GOVERNANCE / METHOD / RELEASE / RETURN QA / ACCEPTANCE / CURSOR

CHATGPT WORK
= FULL-VOLUME SEMANTIC EXECUTION / REWORK / LOCAL QA / HANDOFF

CODEX BROWSER RECOVERY
= PUBLIC BROWSER EVIDENCE ACQUISITION ONLY

OWNER
= PROMPT RELAY + SINGLE-STAGING BYTE RELAY
```

Main Chat governance gates are not Work/Codex runtime gates.

---

## 1. Roadmap cursor

```text
STEP00 = COMPLETE
STEP01 = COMPLETE
STEP02 = COMPLETE
STEP03 = COMPLETE
STEP03A = COMPLETE
STEP03B = COMPLETE
STEP04 = ACCEPTED
STEP05 = COMPLETE / PASS
STEP06 = DURABLE PASS

STEP07_PREPARATION = ACCEPTED
STEP07_ATTEMPT_1 = REJECTED / INCOMPLETE
STEP07_BROWSER_RECOVERY_ATTEMPT_1 = REJECTED
STEP07_BROWSER_RECOVERY_LIMITED_REWORK = REJECTED
STEP07_BROWSER_RECOVERY_FINAL_NARROW_RETRY = REJECTED
STEP07_BROWSER_RECOVERY_VERIFIED_80_URL_RETRY = RETURNED / MAIN_CHAT_REJECTED_RESIDUAL_CLOSURE_REQUIRED
STEP07_BROWSER_RECOVERY_RESIDUAL_CLOSURE = RELEASED_TO_CODEX
STEP07_BROWSER_RECOVERY_REMOTE_PUBLICATION = NOT_ALLOWED_YET
STEP07_SEMANTIC_REWORK = BLOCKED_PENDING_ACCEPTED_BROWSER_RECOVERY
STEP07 = INCOMPLETE / REWORK_REQUIRED

STEP08 = BLOCKED / NOT_STARTED
STEP09 = NOT_STARTED
STEP10 = NOT_STARTED
STEP11 = NOT_STARTED
STEP12 = NOT_STARTED
STEP13 = NOT_STARTED
STEP14 = NOT_STARTED
STEP15 = NOT_STARTED
STEP16 = NOT_STARTED
STEP17 = NOT_STARTED
STEP18 = NOT_STARTED
STEP19 = NOT_STARTED
STEP20 = NOT_STARTED
STEP21 = NOT_STARTED
STEP22 = NOT_STARTED
```

Canonical roadmap authority remains `LEVEL2/STEP_RULES_INDEX.md` through Step22.

---

## 2. Accepted upstream state entering Step07

```text
STEP03A_RAW_OCCURRENCES = 25,979
STEP03A_NORMALIZED_IDENTITIES = 24,576
STEP03B_KEEP = 5,100
STEP03B_HOLD = 13,035
STEP03B_EXCLUDE = 6,441
STEP04_FAMILY_ROWS = 32
STEP04_IDENTITY_ROWS = 24,576
STEP04_OCCURRENCE_ROWS = 25,979
STEP04_QUEUE_ROWS = 13
STEP05_QUEUE_ROWS = 13
STEP05_PROVIDER_CANDIDATES = 1
STEP05_NEW_UNION_ROWS = 0
STEP06_REPRESENTATIVE_QUERIES = 22
STEP06_CLASSIFIED_SERP_ROWS = 440
STEP06_QUERY_TOP10_PROFILES = 22
STEP06_PAIRWISE_COMPARISONS = 231
STEP06_DOMAIN_RECURRENCE_UNIVERSE = 165
STEP06_CURATED_COMPETITORS = 32
STEP06_COLLISION_ROWS = 5
```

Obsolete Step03B `5074/12750/6752` and Step05 orientation `259600/200577/2658` remain superseded.

---

## 3. Step07 Attempt 1

Attempt 1 remains rejected/incomplete:

```text
DISCOVERED_URLS = 1976
INSPECTED_URLS = 24
EXCLUDED_URLS = 1201
INACCESSIBLE_URLS = 751
CANDIDATE_IDENTITIES = 686
PROVENANCE_ROWS = 1417
NEW_CANDIDATE = 400
```

Reasons: incomplete bounded coverage plus systematic candidate-producer pollution.

Authority: `STEP07_MAIN_CHAT_RETURN_QA_2026-09-17.md`.

---

## 4. Browser recovery history

### Attempt 1 — rejected

Rejected for schema drift, placeholder evidence, executor navigation failures and unauthorized sitemap contamination.

Authority: `STEP07_BROWSER_RECOVERY_MAIN_CHAT_RETURN_QA_2026-09-17.md`.

### Limited rework — rejected

Mechanically improved schemas/hashes, but old navigation failures were batch relabelled without demonstrated retries; QA totals and target/environment classification remained false.

Authority: `STEP07_BROWSER_RECOVERY_LIMITED_REWORK_MAIN_CHAT_RETURN_QA_2026-09-17.md`.

### Final narrow retry — rejected

Independent row comparison proved most requested browser retries were not actually executed.

Authority: `STEP07_BROWSER_RECOVERY_FINAL_NARROW_RETRY_MAIN_CHAT_RETURN_QA_2026-09-17.md`.

### Verified 80-URL retry — returned and independently rejected for residual closure

This return finally proves the frozen 80 browser actions:

```text
FROZEN_RETRY_SET_ROWS = 80
RETRY_AUDIT_ROWS = 80
ACTUAL_BROWSER_NAVIGATION_ATTEMPTED = 80/80
SET_A = 47/47
SET_B = 30/30
SET_C = 1/1
SET_D = 2/2
```

Mechanical data quality is materially improved:

```text
SOURCE_URL_ROWS = 1976
PAGE_EVIDENCE_ROWS = 663
URL/COVERAGE/PAGE_EVIDENCE/RETRY_AUDIT SCHEMAS = PASS
JOINS = PASS
SHA_VERIFICATION = PASS
NOT_COLLECTED_ON_INSPECTED = 0
```

Final returned terminal counts:

```text
EXCLUDED_OUT_OF_SCOPE = 1201
EXCLUDED_DUPLICATE = 24
RECOVERED_INSPECTED = 329
REDIRECTED_IN_SCOPE = 334
TARGET_CAPTCHA_OR_ANTI_BOT = 3
UNRESOLVED_DYNAMIC_CONTENT = 34
EXECUTION_ENVIRONMENT_FAILURE = 51
```

Main Chat acceptance still fails because:

1. `51 EXECUTION_ENVIRONMENT_FAILURE + 34 UNRESOLVED_DYNAMIC_CONTENT = 85` residual acquisition gaps remain;
2. four Azbyka DDoS-Guard challenge pages are misclassified as normal inspected/redirected content;
3. Kartaslov row `R9-S07U000396` is falsely classified target anti-bot although normal public page content is readable;
4. 41 rows are marked `REDIRECTED_IN_SCOPE` with same source/final URL and empty redirect chain; 39 are deterministic ordinary-content reclassifications, 2 are Azbyka challenge rows;
5. coverage suppresses all 34 unresolved rows from `remaining_unresolved_or_environment_failure_urls`;
6. manifest retains stale artifact-set/head/terminal-state metadata.

Main Chat return authority:

`STEP07_BROWSER_RECOVERY_VERIFIED_80_RETURN_MAIN_CHAT_QA_2026-09-17.md`

Quality:

```text
QUALITY_TOTAL = 67.5 / 100
QUALITY_SCORE = 6.75 / 10
BROWSER_RECOVERY_ACCEPTED = false
```

---

## 5. Current residual-closure authority

Current execution entry point:

`STEP07_BROWSER_RECOVERY_CODEX_RESIDUAL_CLOSURE_PROMPT_V2_2026-09-17.md`

Base method/output contract:

`STEP07_BROWSER_RECOVERY_CODEX_RESIDUAL_CLOSURE_PROMPT_2026-09-17.md`

Frozen exact correction set:

`STEP07_BROWSER_RECOVERY_RESIDUAL_CORRECTION_SET_2026-09-17.csv`

Exact frozen set:

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

Hard execution model:

```text
39 deterministic corrections
+ 90 actual residual browser retries
→ regenerate final recovery ledgers/evidence/coverage/QA/manifest
→ preserve existing verified-80 retry audit
→ create STEP07_BROWSER_RECOVERY_RESIDUAL_RETRY_AUDIT.csv (90 rows)
```

The executor must not derive, expand or shrink this correction universe.

Final residual handoff contains exactly seven files:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
STEP07_BROWSER_RECOVERY_COVERAGE.csv
STEP07_BROWSER_RECOVERY_QA.md
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv
STEP07_BROWSER_RECOVERY_RESIDUAL_RETRY_AUDIT.csv
```

Browser recovery cannot PASS while final residual `EXECUTION_ENVIRONMENT_FAILURE + UNRESOLVED_DYNAMIC_CONTENT > 0`.

---

## 6. Step07 semantic rework boundary

Only after browser recovery acceptance may ChatGPT Work execute semantic rework over:

```text
ALL 686 current candidate identities
ALL 1417 current provenance rows
ALL accepted recovered browser evidence
ALL current/recovered URL coverage for all 32 competitors
```

The current `NEW_CANDIDATE = 400` set remains unsafe for Step08.

Semantic rework prompt remains:

`STEP07_REWORK_WORK_PROMPT_2026-09-17.md`

Status: `BLOCKED_PENDING_ACCEPTED_BROWSER_RECOVERY`.

---

## 7. Provider/downstream boundary

```text
WORDSTAT_CALLS_ALLOWED_NOW = 0
YANDEX_SEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
STEP08_STARTED = false
FINAL_INTENT_DECISIONS = NONE
FINAL_CLUSTER_DECISIONS = NONE
FINAL_PAGE_DECISIONS = NONE
```

---

## 8. Exact next action

```text
CURRENT_NEXT_ACTION = OWNER_RELAY_STEP07_BROWSER_RECOVERY_CODEX_RESIDUAL_CLOSURE_PROMPT_V2_TO_CODEX
STEP07_BROWSER_RECOVERY_RESIDUAL_CLOSURE = RELEASED_TO_CODEX
STEP07_BROWSER_RECOVERY_REMOTE_PUBLICATION = BLOCKED_PENDING_ACCEPTED_RETURN
STEP07_SEMANTIC_REWORK = BLOCKED_PENDING_ACCEPTED_BROWSER_RECOVERY
STEP07 = INCOMPLETE_REWORK_REQUIRED
STEP08 = BLOCKED_NOT_STARTED
```

Do not upload the rejected verified-80 return as canonical recovery evidence.