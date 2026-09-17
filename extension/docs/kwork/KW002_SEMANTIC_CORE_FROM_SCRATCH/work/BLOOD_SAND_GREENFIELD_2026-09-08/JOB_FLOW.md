# KW-002 JOB FLOW — BLOOD_SAND_GREENFIELD_2026-09-08

Updated: 2026-09-17

Current status: **STEP06 DURABLE PASS / STEP07 PREPARATION ACCEPTED / STEP07 ATTEMPT 1 REJECTED / BROWSER RECOVERY ATTEMPT 1 REJECTED / LIMITED REWORK REJECTED / FINAL NARROW RETRY REJECTED / VERIFIED 80-URL CODEX RETRY RELEASED / STEP07 SEMANTIC REWORK BLOCKED / STEP08 BLOCKED**

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
STEP07_BROWSER_RECOVERY_VERIFIED_80_URL_RETRY = RELEASED_TO_CODEX
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

## 3. Step07 Attempt 1 — rejected

```text
DISCOVERED_URLS = 1,976
INSPECTED_URLS = 24
EXCLUDED_URLS = 1,201
INACCESSIBLE_URLS = 751
PROVENANCE_ROWS = 1,417
CANDIDATE_IDENTITIES = 686
NEW_CANDIDATE = 400
```

Attempt 1 failed bounded coverage and produced systematic semantic-candidate pollution. Authority:

`STEP07_MAIN_CHAT_RETURN_QA_2026-09-17.md`

---

## 4. Browser recovery history

### Recovery Attempt 1 — rejected

Reported:

```text
RECOVERED_INSPECTED = 346
REDIRECTED_IN_SCOPE = 306
TARGET_CAPTCHA_OR_ANTI_BOT = 1
EXECUTION_ENVIRONMENT_FAILURE = 98
```

Rejected for schema drift, placeholder evidence, executor navigation failures and unauthorized sitemap contamination.

Authority:

`STEP07_BROWSER_RECOVERY_MAIN_CHAT_RETURN_QA_2026-09-17.md`

### Limited rework — rejected

Mechanically improved to exact schemas and valid page-evidence hashes, but 47 old navigation-bug rows were batch relabelled without demonstrated retries, 30 capture-failure rows remained un-retried, QA totals were false, target/environment states remained mixed, and manifest self byte-size was false.

Authority:

`STEP07_BROWSER_RECOVERY_LIMITED_REWORK_MAIN_CHAT_RETURN_QA_2026-09-17.md`

### Final narrow retry return — rejected

Owner returned a third five-file package + ZIP. Independent Main Chat byte/row comparison proved that it did not execute the requested retry universe:

```text
SOURCE_URL_ROWS = 1976
PAGE_EVIDENCE_ROWS = 620
RECOVERED_INSPECTED = 318
REDIRECTED_IN_SCOPE = 302
TARGET_CAPTCHA_OR_ANTI_BOT = 3
EXECUTION_ENVIRONMENT_FAILURE = 128
EXCLUDED_DUPLICATE = 24
EXCLUDED_OUT_OF_SCOPE = 1201
```

Critical comparison with the preceding package:

```text
URL_LEDGER_ROWS = 1976
terminal_status changed rows = 2
browser_rendered changed rows = 2
page_evidence_id changed rows = 2
error_class changed rows = 3
error_detail changed rows = 3
```

The exact 47 old `t.goto`-derived rows remained unchanged with one generic error/timestamp and no retry marker. The exact 30 `EVIDENCE_CAPTURE_UNAVAILABLE` rows also remained unchanged. Returned QA still reported impossible error-class totals. Manifest self-entry still reported `byte_size=0` although actual manifest was 1979 bytes.

Main Chat independently opened exact affected URLs through Opera after the return, including SlavyanskieOberegi, HappyWitch and OUM pages, proving that at least some unchanged final environment failures are false negatives.

Authority:

`STEP07_BROWSER_RECOVERY_FINAL_NARROW_RETRY_MAIN_CHAT_RETURN_QA_2026-09-17.md`

```text
QUALITY_TOTAL = 45.5 / 100
QUALITY_SCORE = 4.55 / 10
MAIN_CHAT_ACCEPTANCE = REJECTED
```

---

## 5. Current verified retry control

Main Chat froze the retry universe directly from the owner-returned URL ledger:

`STEP07_BROWSER_RECOVERY_VERIFIED_RETRY_SET_2026-09-17.csv`

Exact distribution:

```text
A_OLD_T_GOTO_DERIVED = 47
B_EVIDENCE_CAPTURE_UNAVAILABLE = 30
C_UNSUPPORTED_TARGET_BLOCK = 1
D_SOKOLOV_CHALLENGE = 2
TOTAL_UNIQUE_RETRY_ROWS = 80
```

Current execution prompt:

`STEP07_BROWSER_RECOVERY_CODEX_VERIFIED_80_URL_RETRY_PROMPT_2026-09-17.md`

Codex must execute real browser navigation for all 80 exact rows and create an additional proof artifact:

`STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv`

Required audit invariants:

```text
RETRY_AUDIT_ROWS = 80
UNIQUE_RETRY_AUDIT_IDS = 80
EVERY_FROZEN_RETRY_ID_PRESENT = true
EXTRA_RETRY_IDS = 0
ACTUAL_BROWSER_NAVIGATION_ATTEMPTED = 80/80
SET_A_ACTUAL_BROWSER_RETRIES = 47/47
SET_B_ACTUAL_BROWSER_RETRIES = 30/30
SET_C_ACTUAL_BROWSER_RETRIES = 1/1
SET_D_ACTUAL_BROWSER_RETRIES = 2/2
```

The retry audit is a control artifact required to prove acquisition execution. It does not authorize Step08 or semantic candidate classification.

---

## 6. Current browser-recovery handoff contract

The next Codex return contains six files:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
STEP07_BROWSER_RECOVERY_COVERAGE.csv
STEP07_BROWSER_RECOVERY_QA.md
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv
```

No canonical recovery publication is allowed until Main Chat independently accepts this verified return.

---

## 7. Step07 semantic rework boundary

After browser recovery acceptance, ChatGPT Work must process at full volume:

```text
ALL 686 current candidate identities
ALL 1417 current provenance rows
ALL accepted recovered browser evidence
ALL current/recovered URL coverage for all 32 competitors
```

The current `NEW_CANDIDATE = 400` set is unsafe for Step08 and must be fully re-evaluated.

Current semantic rework prompt:

`STEP07_REWORK_WORK_PROMPT_2026-09-17.md`

---

## 8. Provider/downstream boundary

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

## 9. Exact next action

```text
CURRENT_NEXT_ACTION = OWNER_RELAY_STEP07_BROWSER_RECOVERY_CODEX_VERIFIED_80_URL_RETRY_PROMPT_TO_CODEX
STEP07_BROWSER_RECOVERY_VERIFIED_80_URL_RETRY = RELEASED_TO_CODEX
STEP07_SEMANTIC_REWORK = BLOCKED_PENDING_ACCEPTED_BROWSER_RECOVERY
STEP07 = INCOMPLETE_REWORK_REQUIRED
STEP08 = BLOCKED_NOT_STARTED
```

Do not upload the rejected third browser-recovery package to GitHub as canonical recovery evidence.