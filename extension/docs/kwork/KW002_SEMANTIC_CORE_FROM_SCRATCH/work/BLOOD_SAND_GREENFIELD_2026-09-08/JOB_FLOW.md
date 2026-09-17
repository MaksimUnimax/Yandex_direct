# KW-002 JOB FLOW — BLOOD_SAND_GREENFIELD_2026-09-08

Updated: 2026-09-17

Current status: **STEP06 DURABLE PASS / STEP07 PREPARATION ACCEPTED / STEP07 ATTEMPT 1 REJECTED / BROWSER RECOVERY ATTEMPT 1 RETURNED BUT REJECTED / LIMITED CODEX REWORK RELEASED / STEP07 SEMANTIC REWORK BLOCKED / STEP08 BLOCKED**

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
STEP07_BROWSER_RECOVERY_LIMITED_REWORK = RELEASED_TO_CODEX
STEP07_BROWSER_RECOVERY_REMOTE_PUBLICATION = NOT_ALLOWED_YET

STEP07_SEMANTIC_REWORK = BLOCKED_PENDING_CORRECTED_BROWSER_RECOVERY
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
→ consume Attempt 1 + corrected browser recovery evidence
→ re-evaluate ALL existing 686 candidates / 1417 provenance rows
→ merge recovered evidence
→ rerun complete Step07 QA
```

Main Chat Opera-control authority:

`STEP07_OPERA_BROWSER_CONTROL_PROBE_2026-09-17.md`

---

## 5. Browser recovery Attempt 1 return

Codex returned owner-side five-file recovery package with reported totals:

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
PROVIDER_CALLS = 0
STEP08_EXECUTED = false
CANDIDATE_CLASSIFICATION_EXECUTED = false
```

The return materially improved access evidence, but independent Main Chat QA rejected it.

Authority:

`STEP07_BROWSER_RECOVERY_MAIN_CHAT_RETURN_QA_2026-09-17.md`

Hard defects:

1. recovery URL ledger does not use the released recovery schema;
2. recovery coverage CSV uses the old Attempt-1-style schema instead of required Attempt1→Recovery fields;
3. 30 JSONL evidence rows use `NOT_COLLECTED`; 28 of them are linked to rows labelled `RECOVERED_INSPECTED`;
4. JSONL field names drift from the released machine contract;
5. 47 of 98 environment failures are deterministic executor bug `TypeError: t.goto is not a function` and must be retried after fixing navigation;
6. QA contains unauthorized sitemap contamination referencing `okno-msk.ru`, not one of the authorized 32 competitors.

Therefore:

```text
STEP07_BROWSER_RECOVERY_ATTEMPT_1_RETURN = REJECTED
CANONICAL_RECOVERY_UPLOAD = NOT_ALLOWED
```

The owner-uploaded first recovery package remains outside canonical repository publication.

---

## 6. Current limited Codex rework

Current execution prompt:

`STEP07_BROWSER_RECOVERY_CODEX_LIMITED_REWORK_PROMPT_2026-09-17.md`

The rework must preserve valid browser evidence while correcting the producer across the complete affected universe.

Mandatory corrections include:

```text
URL_LEDGER_EXACT_RECOVERY_SCHEMA
COVERAGE_EXACT_RECOVERY_SCHEMA
PAGE_EVIDENCE_EXACT_FIELD_SCHEMA
NOT_COLLECTED_ON_RECOVERED_INSPECTED = 0
T_GOTO_TYPEERROR_FINAL_ROWS = 0
UNAUTHORIZED_SITEMAP_REFERENCES = 0
VALID_SHA256_FOR_EVERY_RECOVERED_INSPECTED
FULL_JOIN_QA
```

Retry policy:

- retry all 47 `t.goto` bug rows after fixing navigation;
- one normal retry for timeout/deadline/CDP environment failures;
- never bypass site-safety policy, anti-bot, login, robots, certificate/security controls.

---

## 7. Browser recovery output contract

Corrected Codex package remains exactly five files:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
STEP07_BROWSER_RECOVERY_COVERAGE.csv
STEP07_BROWSER_RECOVERY_QA.md
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
```

Only after Main Chat accepts the corrected package may owner relay it to canonical single staging and may the semantic Work rework be released.

---

## 8. Step07 semantic rework boundary

After corrected browser recovery is accepted, Work rework must process at full volume:

```text
ALL 686 current candidate identities
ALL 1417 current provenance rows
ALL corrected recovered browser evidence
ALL current/recovered URL coverage for all 32 competitors
```

The current `NEW_CANDIDATE = 400` set remains unsafe for Step08 and must be fully re-evaluated.

---

## 9. Provider/downstream boundary

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

## 10. Exact next action

```text
CURRENT_NEXT_ACTION = RELAY_STEP07_BROWSER_RECOVERY_CODEX_LIMITED_REWORK_PROMPT_TO_CODEX
STEP07_BROWSER_RECOVERY_LIMITED_REWORK = RELEASED_TO_CODEX
STEP07_SEMANTIC_REWORK = BLOCKED_PENDING_CORRECTED_BROWSER_RECOVERY
STEP07 = INCOMPLETE_REWORK_REQUIRED
STEP08 = BLOCKED_NOT_STARTED
```

Do not upload the rejected first recovery package to GitHub as canonical recovery evidence. Codex must first return the corrected five-file package.