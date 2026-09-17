# KW-002 / BLOOD & SAND — STEP07 MAIN CHAT OPERA RESIDUAL AUDIT

Date: 2026-09-17
Status: **FINAL OPERA ACQUISITION CLOSED / LOCAL 7-FILE PACKAGE QA PASS / CANONICAL REMOTE ACCEPTANCE WAITING OWNER SINGLE-STAGING BYTE RELAY**

## 1. Frozen scope

Authority remains:

`STEP07_BROWSER_RECOVERY_RESIDUAL_CORRECTION_SET_2026-09-17.csv`

Only rows with:

```text
browser_retry_required = true
```

were resolved through the owner-connected Opera Browser Connector.

```text
FROZEN_BROWSER_RETRY_ROWS = 90
URL_UNIVERSE_EXPANDED = false
WORDSTAT_CALLS = 0
YANDEX_SEARCH_PROVIDER_CALLS = 0
AI_SEARCH_OR_GENSEARCH_CALLS = 0
STEP08_STARTED = false
SEMANTIC_CANDIDATE_CLASSIFICATION = false
```

No CAPTCHA, anti-bot, VPN, login, security or robots bypass was performed.

## 2. Final exact Opera outcomes

A later exact Wildberries recheck supersedes the earlier interim `70 readable / 20 target-block` snapshot.

Current frozen-90 result:

```text
RECOVERED_INSPECTED_WITH_DURABLE_EVIDENCE = 66
TARGET_CAPTCHA_OR_ANTI_BOT = 24
EXECUTION_ENVIRONMENT_FAILURE = 0
UNRESOLVED_DYNAMIC_CONTENT = 0
TOTAL = 90
FINAL_RESIDUAL_ACQUISITION_GAPS = 0
```

Target-block breakdown:

```text
Wildberries official VPN target page = 22
AliExpress official verification target page = 2
```

The four Wildberries rows that changed from the interim readable observation to the final target-side block are:

```text
R9-S07U000008
R9-S07U000010
R9-S07U000016
R9-S07U000018
```

Each was re-opened through the exact authority URL. Current target page text states:

```text
Возможно, нужно выключить VPN
Не смогли загрузить страницу: попробуйте выключить VPN.
```

`R9-S07U000014` remains normally readable and has durable rendered product/category evidence.

## 3. Final frozen-90 domain reconciliation

```text
wildberries.ru = 1 readable + 22 target block = 23
market.yandex.ru = 20 readable
livemaster.ru = 11 readable
avito.ru = 8 readable
aliexpress.ru = 2 target block
joom.ru = 2 readable
ru.wikipedia.org = 1 readable
ru.ruwiki.ru = 8 readable
kartaslov.ru = 4 readable
sibpodkova.ru = 3 readable
azbyka.ru = 4 readable
goroskop365.ru = 4 readable

READABLE = 66
TARGET_BLOCK = 24
ENVIRONMENT_FAILURE = 0
UNRESOLVED = 0
TOTAL = 90
```

## 4. Durable evidence materialization

All 66 readable rows now have durable page-evidence records.

Evidence policy used in the final package:

- marketplace/search/category pages: complete current candidate-bearing headings, category labels and visible product/service names; generic UI, ads, prices, ratings and reviews are filtered deterministically;
- informational/encyclopedic pages: stable topic/section/glossary surfaces from complete public page inspection; arbitrary prose/example sentences are not promoted as candidate identities;
- the long Azbyka Chapter V page was inspected across all 8 connector pagination pages and its stable symbol/topic register was retained.

This matches the Step07 rework anti-contamination boundary:

```text
RAW PROSE != AUTOMATIC CANDIDATE
STABLE TOPIC / CATEGORY / PRODUCT / TERMINOLOGY SURFACE = ELIGIBLE FOR REWORK EVALUATION
```

## 5. Independent final-package QA

Independent re-read of the rebuilt package returned:

```text
OUTSIDE_FROZEN_URL_ROWS_CHANGED = 0
FROZEN_ROWS_CHANGED = 90/90
MISSING_FROZEN_BROWSER_RETRY_IDS = 0
EXTRA_BROWSER_RETRY_IDS = 0
URL_PK_UNIQUE = PASS
EVIDENCE_PK_UNIQUE = PASS
URL_LEDGER_SCHEMA = PASS
COVERAGE_SCHEMA = PASS
PAGE_EVIDENCE_SCHEMA = PASS
JOINS = PASS
COVERAGE_ROWS = 32
ALL_REMAINING_UNRESOLVED_OR_ENVIRONMENT_FAILURE = 0
MANIFEST_HASHES = PASS
ZIP_SEVEN_FILE_BYTE_IDENTITY = PASS
```

Final global terminal counts across all 1,976 recovery URL rows:

```text
EXCLUDED_OUT_OF_SCOPE = 1201
EXCLUDED_DUPLICATE = 24
RECOVERED_INSPECTED = 432
REDIRECTED_IN_SCOPE = 293
TARGET_CAPTCHA_OR_ANTI_BOT = 26
EXECUTION_ENVIRONMENT_FAILURE = 0
UNRESOLVED_DYNAMIC_CONTENT = 0
TOTAL = 1976
```

The global target-block count is 26 because two legitimate SOKOLOV target challenges already existed outside the frozen 90.

Final page evidence rows:

```text
PRE_OPERA_VALID_EVIDENCE = 659
NEW_OPERA_DURABLE_EVIDENCE = 66
TOTAL_PAGE_EVIDENCE = 725
```

## 6. Local final package hashes

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
SHA256 = 2fb8a69b6861a1e9934b0976dbf44029a79579d93457c284bd50ba5c392cf0e2

STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
SHA256 = 7eefe0001428c926680faab9218bda9d7ddfd197347dd97b6140e993d7353592

STEP07_BROWSER_RECOVERY_COVERAGE.csv
SHA256 = 8cd07a7c1b21e9495d276ab8c7a53c4a8f34525dfb305684dcc811411b8433ce

STEP07_BROWSER_RECOVERY_QA.md
SHA256 = 46d8885743a2ae3358a3e6a11ec57c57438c156b0a6d00e1030ae0a5bcb1ee83

STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv
SHA256 = 1cbe984c47854eeb55eb1a1a07fc3134a030a1a841cd6a7f22e82326a01295a6

STEP07_BROWSER_RECOVERY_RESIDUAL_RETRY_AUDIT.csv
SHA256 = ad77bad53a960c6ea37c4689f556e2f92f17bc5a57fcdd0dfaa0d7b6a03faf3d

STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
SHA256 = e5bad200b5f460f266ecc6305db874edc5c92ebcb215baf6eac374c3b4f58b1e

TRANSPORT ZIP
SHA256 = f08cca3b26cce93767d22916c328ccf8e37fd809c60aef8e91aebfe9e0205f36
FILES = exactly 7
```

## 7. Publication boundary

Pre-publication remote check:

```text
REMOTE_HEAD = 71ff2a0a754d67c549fd7838b9835a8e25f2d216
AUTHORITY_DRIFT = false
```

The final package is **locally accepted by Main Chat QA**, but the 22.3 MB page-evidence file cannot be safely written through the text-only GitHub `update_file` connector.

Therefore the frozen handoff architecture applies:

```text
OWNER = ONE BYTE RELAY
ONE ZIP
→ EXTRACT EXACTLY 7 FILES
→ ONE STAGING DIRECTORY
→ ONE COMMIT
→ REPLY "готово"
→ MAIN CHAT REMOTE READBACK / HASH QA
→ CANONICAL BROWSER RECOVERY ACCEPTANCE
→ RELEASE STEP07 SEMANTIC REWORK
```

Until remote readback succeeds:

```text
LOCAL_RECOVERY_PACKAGE_QA = PASS
CANONICAL_REMOTE_BROWSER_RECOVERY_ACCEPTED = false
STEP07_SEMANTIC_REWORK = BLOCKED_PENDING_REMOTE_RECOVERY_ACCEPTANCE
STEP08 = BLOCKED_NOT_STARTED
```
