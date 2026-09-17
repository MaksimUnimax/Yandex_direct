# KW-002 JOB FLOW — BLOOD_SAND_GREENFIELD_2026-09-08

Updated: 2026-09-17

Current status: **STEP06 DURABLE PASS / STEP07 PREPARATION ACCEPTED / STEP07 ATTEMPT 1 REJECTED / BROWSER RECOVERY ATTEMPT 1 REJECTED / LIMITED CODEX REWORK RETURNED BUT REJECTED / FINAL NARROW CODEX RETRY RELEASED / STEP07 SEMANTIC REWORK BLOCKED / STEP08 BLOCKED**

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
STEP07_ATTEMPT_1_OWNER_UPLOAD = COMPLETE
STEP07_ATTEMPT_1_REMOTE_PUBLICATION = COMPLETE
STEP07_ATTEMPT_1_WORK_QA = FAIL / INCOMPLETE
STEP07_ATTEMPT_1_MAIN_CHAT_RETURN_QA = REJECTED / REWORK_REQUIRED

STEP07_BROWSER_RECOVERY_ATTEMPT_1 = RETURNED / MAIN_CHAT_REJECTED
STEP07_BROWSER_RECOVERY_LIMITED_REWORK = RETURNED / MAIN_CHAT_REJECTED
STEP07_BROWSER_RECOVERY_FINAL_NARROW_RETRY = RELEASED_TO_CODEX
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

Attempt 1 remains rejected/incomplete.

```text
DISCOVERED_URLS = 1,976
INSPECTED_URLS = 24
EXCLUDED_URLS = 1,201
INACCESSIBLE_URLS = 751
PROVENANCE_ROWS = 1,417
CANDIDATE_IDENTITIES = 686
```

Work hard failures:

```text
COMPLETE_BOUNDED_COMPETITOR_UNIVERSE_PROCESSED = FAIL
EXECUTION_COMPLETENESS_DEMONSTRABLE = FAIL
```

Main Chat additionally found systematic candidate-producer pollution and false inaccessibility caused by Work runtime/proxy behavior.

Main Chat return authority:

`STEP07_MAIN_CHAT_RETURN_QA_2026-09-17.md`

---

## 4. Browser recovery architecture

```text
CODEX BROWSER RECOVERY
→ acquire missing legitimate public competitor page evidence
→ no candidate classification
→ no provider calls

THEN

CHATGPT WORK STEP07 SEMANTIC REWORK
→ consume Attempt 1 + accepted corrected browser recovery evidence
→ re-evaluate ALL existing 686 candidates / 1417 provenance rows
→ merge recovered evidence
→ rerun complete Step07 QA
```

Main Chat Opera-control authority:

`STEP07_OPERA_BROWSER_CONTROL_PROBE_2026-09-17.md`

---

## 5. Browser recovery Attempt 1 return — rejected

Reported first recovery totals:

```text
AUTHORIZED_COMPETITORS = 32
SOURCE_URL_ROWS = 1976
RECOVERY_ROWS_ACCOUNTED = 751
SILENT_SKIP = 0
RECOVERED_INSPECTED = 346
REDIRECTED_IN_SCOPE = 306
TARGET_CAPTCHA_OR_ANTI_BOT = 1
EXECUTION_ENVIRONMENT_FAILURE = 98
EXCLUDED_DUPLICATE = 24
EXCLUDED_OUT_OF_SCOPE = 1201
```

Main Chat rejected the first recovery for schema drift, placeholder evidence, unretried `t.goto` producer failures and unauthorized sitemap contamination.

Authority:

`STEP07_BROWSER_RECOVERY_MAIN_CHAT_RETURN_QA_2026-09-17.md`

---

## 6. Limited browser-recovery rework return — received but rejected

Owner returned the corrected five-file limited-rework package to Main Chat. It was QA'd locally before any canonical GitHub upload.

Independent mechanical results that PASS:

```text
SOURCE_URL_ROWS = 1976
AUTHORIZED_COMPETITORS = 32
URL_LEDGER_EXACT_FIELD_ORDER = PASS
COVERAGE_EXACT_FIELD_ORDER = PASS
PAGE_EVIDENCE_EXACT_FIELD_ORDER = PASS
URL_PK_UNIQUE = PASS
EVIDENCE_PK_UNIQUE = PASS
PAGE_EVIDENCE_ROWS = 622
ALL_PAGE_EVIDENCE_JOINS = PASS
RECOVERED_INSPECTED = 318
REDIRECTED_IN_SCOPE = 304
EXCLUDED_OUT_OF_SCOPE = 1201
EXCLUDED_DUPLICATE = 24
TARGET_CAPTCHA_OR_ANTI_BOT = 1
EXECUTION_ENVIRONMENT_FAILURE = 128
ALL_INSPECTED_TEXT_NONEMPTY = PASS
ALL_EVIDENCE_SHA256_MATCH = PASS
NOT_COLLECTED_TEXT_OR_HASH = 0
UNAUTHORIZED_SOURCE_URL_HOST_ROWS = 0
UNAUTHORIZED_SITEMAP_REFERENCES = 0
LITERAL_T_GOTO_ERROR_ROWS = 0
ZIP_BYTE_PARITY = PASS
```

But Main Chat acceptance failed on material execution/QA truthfulness.

Authority:

`STEP07_BROWSER_RECOVERY_LIMITED_REWORK_MAIN_CHAT_RETURN_QA_2026-09-17.md`

Hard defects:

1. all 47 old `t.goto` rows remain `EXECUTION_ENVIRONMENT_FAILURE` with the same generic replacement detail/timestamp instead of demonstrated per-URL retry results;
2. Main Chat independently opened exact affected URLs on `slavyanskieoberegi.ru`, `happywitch.ru` and `oum.ru` through Opera after the return, proving at least some of those 47 final failures are false negatives;
3. returned QA reports impossible environment-failure error-class totals (`105 + 40 + 30`) while the ledger contains `58 + 40 + 30 = 128`;
4. 30 `EVIDENCE_CAPTURE_UNAVAILABLE` rows remain, including 23 Wildberries URLs despite existing Main Chat browser evidence of a target-level VPN/anti-bot block requiring truthful target-vs-environment classification;
5. asserted target CAPTCHA row `R9-S07U000396` has blank error evidence and does not substantiate the target-block claim;
6. Sokolov rows `R9-S07U001927` and `R9-S07U001928` are retained as `REDIRECTED_IN_SCOPE` although captured content is only a connection-check/challenge page;
7. manifest self-entry reports `byte_size = 0` although the returned manifest is non-empty.

Quality:

```text
QUALITY_TOTAL = 65.5 / 100
QUALITY_SCORE = 6.55 / 10
MAIN_CHAT_ACCEPTANCE = REJECTED_FINAL_NARROW_RETRY_REQUIRED
```

The rejected limited-rework package must NOT be uploaded to GitHub as canonical recovery evidence.

---

## 7. Current final narrow Codex retry

Current execution prompt:

`STEP07_BROWSER_RECOVERY_CODEX_FINAL_NARROW_RETRY_PROMPT_2026-09-17.md`

This is NOT a new full collection.

Preserve valid successful evidence and retry only defective/retry-scope rows.

Mandatory final-narrow-retry scope:

```text
47 old t.goto-derived generic BROWSER_RUNTIME_FAILURE rows
30 EVIDENCE_CAPTURE_UNAVAILABLE rows
R9-S07U000396 unsupported target-block assertion
R9-S07U001927 Sokolov challenge page
R9-S07U001928 Sokolov challenge page
```

The executor must produce actual per-URL retry outcomes, actual retry timestamps and exact final errors where failures remain.

Required QA invariants include:

```text
OLD_T_GOTO_ROWS_ACTUALLY_RETRIED = 47/47
OLD_T_GOTO_GENERIC_PLACEHOLDER_ERROR_DETAIL_FINAL = 0
EVIDENCE_CAPTURE_UNAVAILABLE_ROWS_RETRIED = 30/30
UNSUPPORTED_TARGET_BLOCK_ROWS = 0
SOKOLOV_CHALLENGE_MISCLASSIFIED_AS_REDIRECT = 0
FINAL_ERROR_CLASS_COUNTS_SUM_MATCHES_ENV_FAILURE_TOTAL = PASS
MANIFEST_SELF_BYTE_SIZE_MATCH = PASS
```

Truthful residual environment failures remain allowed.

---

## 8. Browser recovery output contract

The accepted browser recovery package must remain exactly five canonical files:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
STEP07_BROWSER_RECOVERY_COVERAGE.csv
STEP07_BROWSER_RECOVERY_QA.md
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
```

Only after Main Chat accepts the final corrected package may owner relay it to canonical single staging and may the semantic Work rework be released.

---

## 9. Step07 semantic rework boundary

After browser recovery is accepted, Work semantic rework must process at full volume:

```text
ALL 686 current candidate identities
ALL 1417 current provenance rows
ALL accepted recovered browser evidence
ALL current/recovered URL coverage for all 32 competitors
```

The current `NEW_CANDIDATE = 400` set remains unsafe for Step08 and must be fully re-evaluated.

---

## 10. Provider/downstream boundary

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

## 11. Exact next action

```text
CURRENT_NEXT_ACTION = RELAY_STEP07_BROWSER_RECOVERY_CODEX_FINAL_NARROW_RETRY_PROMPT_TO_CODEX
STEP07_BROWSER_RECOVERY_FINAL_NARROW_RETRY = RELEASED_TO_CODEX
STEP07_SEMANTIC_REWORK = BLOCKED_PENDING_ACCEPTED_BROWSER_RECOVERY
STEP07 = INCOMPLETE_REWORK_REQUIRED
STEP08 = BLOCKED_NOT_STARTED
```

Do not upload the rejected limited-rework package to GitHub as canonical recovery evidence.