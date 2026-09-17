# KW-002 JOB FLOW — BLOOD_SAND_GREENFIELD_2026-09-08

Updated: 2026-09-17

Current status: **STEP06 DURABLE PASS / STEP07 PREPARATION ACCEPTED / STEP07 ATTEMPT 1 REMOTELY PUBLISHED BUT REJECTED / BROWSER RECOVERY RELEASED TO CODEX / STEP07 REWORK REQUIRED / STEP08 BLOCKED**

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
STEP07_BROWSER_RECOVERY = RELEASED_TO_CODEX / NOT YET RETURNED
STEP07_SEMANTIC_REWORK = REQUIRED AFTER BROWSER RECOVERY
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

## 3. Step07 Attempt 1 publication

Owner upload commit:

`4b596b048d87a7e657bf3b84b715e7ee95980a3f`

Upload base:

`00230d7f1a8f83bb2aebfcbad89b896b122879d5`

The upload added exactly six expected files and no unrelated changes:

```text
COMPETITOR_GAP_CANDIDATES.csv
STEP07_COMPETITOR_COVERAGE_LEDGER.csv
STEP07_SOURCE_URL_LEDGER.csv
STEP07_CANDIDATE_PROVENANCE_LEDGER.csv
STEP07_EXECUTION_QA.md
STEP07_EXECUTION_HANDOFF_MANIFEST.json
```

```text
OWNER_UPLOAD_COMPLETE = true
STAGING_READBACK_PASS = true
FINAL_PLACEMENT_COMPLETE = true
STAGING_CLEANUP = NOT_APPLICABLE
REMOTE_PUBLICATION_COMPLETE = true
```

The failed attempt remains preserved in Git history and current paths until accepted rework replaces it.

---

## 4. Attempt 1 accounting / failure

```text
DISCOVERED_URLS = 1,976
INSPECTED_URLS = 24
EXCLUDED_URLS = 1,201
INACCESSIBLE_URLS = 751
UNRESOLVED_URLS = 0
ERROR_URLS = 0
PROVENANCE_ROWS = 1,417
CANDIDATE_IDENTITIES = 686
```

Attempt 1 candidate statuses:

```text
ALREADY_PRESENT = 10
NEW_CANDIDATE = 400
NORMALIZED_DUPLICATE = 0
POSSIBLE_VARIANT = 3
OUT_OF_SCOPE = 207
AMBIGUOUS = 66
```

Only `S07A010 / kartaslov.ru` yielded inspected candidate pages.

Work itself correctly reported:

```text
COMPLETE_BOUNDED_COMPETITOR_UNIVERSE_PROCESSED = FAIL
EXECUTION_COMPLETENESS_DEMONSTRABLE = FAIL
STEP07 = INCOMPLETE
QUALITY_SCORE = 7.4 / 10
```

Main Chat return QA additionally found:

1. many inaccessible rows reflected Work-runtime/proxy failures rather than proven source-level inaccessibility;
2. several authorized competitor public pages were retrievable through a normal browser route;
3. the semantic candidate producer systematically promoted arbitrary prose, quotations, broken dictionary fragments and metadata-like text to `NEW_CANDIDATE`;
4. Work QA retained stale seven-file wording after the contract had become six-file.

Main Chat return authority:

`STEP07_MAIN_CHAT_RETURN_QA_2026-09-17.md`

```text
MAIN_CHAT_ACCEPTANCE = REJECTED_REWORK_REQUIRED
MAIN_CHAT_RETURN_QUALITY_SCORE = 5.2 / 10
STEP08 = BLOCKED
```

---

## 5. Recovery architecture

Do not repeat the failed architecture.

```text
CODEX BROWSER RECOVERY
→ acquire missing legitimate public competitor page evidence
→ no candidate classification
→ no provider calls
→ persist browser recovery ledgers/page evidence

THEN

CHATGPT WORK STEP07 REWORK
→ consume Attempt 1 + browser recovery evidence
→ re-evaluate ALL existing 686 candidates / 1417 provenance rows
→ apply corrected candidate-eligibility producer
→ merge newly collected evidence
→ rerun complete Step07 QA
```

Current Codex recovery prompt:

`STEP07_BROWSER_RECOVERY_CODEX_PROMPT_2026-09-17.md`

Current Work semantic rework prompt:

`STEP07_REWORK_WORK_PROMPT_2026-09-17.md`

---

## 6. Codex browser recovery output contract

Codex must create exactly five recovery artifacts:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
STEP07_BROWSER_RECOVERY_COVERAGE.csv
STEP07_BROWSER_RECOVERY_QA.md
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
```

Codex does NOT replace current Step07 candidates/provenance.

Codex must distinguish target access decisions from its own execution-environment/browser failures.

No CAPTCHA/robots/login/paywall bypass.

---

## 7. Step07 rework boundary

After browser recovery is remotely uploaded/read back, Work rework must process at full volume:

```text
ALL 686 current candidate identities
ALL 1417 current provenance rows
ALL newly recovered browser page evidence
ALL current/recovered URL coverage for all 32 competitors
```

Known bad rows are regression examples only, not patch targets.

The current `NEW_CANDIDATE = 400` set is not safe for Step08 and must be fully re-evaluated.

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
CURRENT_NEXT_ACTION = OWNER_RELAY_STEP07_BROWSER_RECOVERY_CODEX_PROMPT
STEP07_BROWSER_RECOVERY = RELEASED_TO_CODEX
STEP07 = INCOMPLETE_REWORK_REQUIRED
STEP08 = BLOCKED_NOT_STARTED
```

After Codex returns the five recovery files, owner uploads them together to the one job-root staging target and replies `готово`. Main Chat then performs remote readback and releases the already-prepared full-volume Work semantic rework.