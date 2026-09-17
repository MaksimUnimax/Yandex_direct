# KW-002 / BLOOD & SAND — STEP07 BROWSER RECOVERY FINAL NARROW RETRY — MAIN CHAT RETURN QA

Date: 2026-09-17
Status: **REJECTED / VERIFIED RETRY REQUIRED**

## 1. Package reviewed

Owner returned the third browser-recovery package produced after `STEP07_BROWSER_RECOVERY_CODEX_FINAL_NARROW_RETRY_PROMPT_2026-09-17.md`.

Main Chat independently inspected all five files plus the ZIP from the owner upload in chat. The package was not published to GitHub as canonical recovery evidence.

## 2. Byte / package checks

Actual SHA-256:

```text
URL_LEDGER = f6f6b6c42c566243dde778d183a6b4d09f10d2a4d7c01ed20756f67d1832dc89
PAGE_EVIDENCE = 2a21ae3a47b5b9fb39fc39449a74db74a10bc6c903239543de73da530d3c2f27
COVERAGE = c393ad704adfffb3d77828e6a071086f00c22098e3a5a447fcbec6e6fd65929e
QA = c7773b6d6f26aabdb775d4041fe42bba85ec1043cb9822e288576b0e64b3bb9b
MANIFEST_ACTUAL = bdc77f73dc4a0b53ac3a28ea1dbd22209dba69c4a4dd35abdd5d7c09a81ce91d
ZIP = 4359269db7c617b9353d7e933f74816b591122e62699b852b40ffe0fea561dc4
```

ZIP contained exactly the five expected files and each ZIP payload matched the corresponding standalone file byte-for-byte.

## 3. Mechanical checks that pass

```text
SOURCE_URL_ROWS = 1976
AUTHORIZED_COMPETITORS = 32
URL_LEDGER_SCHEMA = PASS
COVERAGE_SCHEMA = PASS
PAGE_EVIDENCE_SCHEMA = PASS
URL_PK_UNIQUE = PASS
EVIDENCE_PK_UNIQUE = PASS
PAGE_EVIDENCE_ROWS = 620
JOINS = PASS
RECOVERED_INSPECTED = 318
REDIRECTED_IN_SCOPE = 302
TARGET_CAPTCHA_OR_ANTI_BOT = 3
EXECUTION_ENVIRONMENT_FAILURE = 128
EXCLUDED_DUPLICATE = 24
EXCLUDED_OUT_OF_SCOPE = 1201
NOT_COLLECTED_ON_INSPECTED = 0
PROVIDER_CALLS = 0
STEP08_EXECUTED = false
CANDIDATE_CLASSIFICATION_EXECUTED = false
```

## 4. Hard failure H1 — requested 47 old runtime retries were still not executed

Main Chat compared the third package URL ledger row-by-row against the preceding limited-rework package.

The exact 47 old `t.goto`-derived rows remain unchanged:

```text
FINAL_STATUS_FOR_ALL_47 = EXECUTION_ENVIRONMENT_FAILURE
FINAL_ERROR_CLASS_FOR_ALL_47 = BROWSER_RUNTIME_FAILURE
FINAL_ERROR_DETAIL_FOR_ALL_47 = Navigation primitive failure was corrected during limited rework; no final target response was obtained.
FINAL_CAPTURED_AT_UTC_FOR_ALL_47 = 2026-09-17T10:06:35.7253053Z
FINAL_NARROW_RETRY_ATTEMPTED_NOTE_COUNT = 0
```

There is no new row-specific retry evidence.

Main Chat independently opened exact affected URLs through Opera Browser Connector after the return and confirmed readable rendered content for multiple affected URLs, including:

```text
https://slavyanskieoberegi.ru/katalog-slavyanskix-oberegov/
https://happywitch.ru/catalog/products/amulety_i_talismany/
https://www.oum.ru/yoga/mantry/chto-oznachaet-simvol-om/
```

Therefore the unchanged generic failures are known false negatives for at least part of the 47-row set.

Hard gate FAIL.

## 5. Hard failure H2 — 30 EVIDENCE_CAPTURE_UNAVAILABLE rows were not retried

The exact 30 rows from the preceding package remain unchanged:

```text
wildberries.ru = 23
livemaster.ru = 5
joom.ru = 2
terminal_status = EXECUTION_ENVIRONMENT_FAILURE
error_class = EVIDENCE_CAPTURE_UNAVAILABLE
error_detail = Rework could not capture non-empty rendered content in current browser runtime; placeholder evidence removed.
captured_at_utc = 2026-09-17T10:06:35.7253053Z
```

No per-URL retry evidence exists in the third return.

The final-narrow prompt explicitly required 30/30 actual normal-browser retries.

Hard gate FAIL.

## 6. Hard failure H3 — only three terminal rows materially changed

A full row-wise comparison between the second and third package URL ledgers found changes only in these field counts:

```text
terminal_status changed rows = 2
browser_rendered changed rows = 2
page_evidence_id changed rows = 2
error_class changed rows = 3
error_detail changed rows = 3
```

The changes correspond to the unsupported Kartaslov target-block row and the two Sokolov challenge rows.

The 77 mandatory retry rows in sets A+B were not changed by actual retries.

## 7. Hard failure H4 — returned QA is still mathematically inconsistent

Actual environment-failure classes in the returned URL ledger are:

```text
BROWSER_RUNTIME_FAILURE = 58
NAVIGATION_TIMEOUT = 40
EVIDENCE_CAPTURE_UNAVAILABLE = 30
TOTAL = 128
```

Returned QA instead reports:

```text
BROWSER_RUNTIME_FAILURE = 105
NAVIGATION_TIMEOUT = 40
EVIDENCE_CAPTURE_UNAVAILABLE = 30
TARGET_CHALLENGE = 3
```

Those rows sum to 178 and mix target challenge with environment errors while the same QA states `CORRECTED_EXECUTION_ENVIRONMENT_FAILURES = 128`.

The required data-derived QA reconciliation did not happen.

Hard gate FAIL.

## 8. Hard failure H5 — manifest self byte size still false

Returned manifest still records its own entry with:

```text
sha256 = SELF_HASH_NOT_APPLICABLE
byte_size = 0
```

Actual manifest byte size is `1979` bytes.

The prior prompt explicitly required the actual final byte size. Not fixed.

## 9. Exact retry authority now frozen

Main Chat materialized the exact affected universe from the returned URL ledger as:

`STEP07_BROWSER_RECOVERY_VERIFIED_RETRY_SET_2026-09-17.csv`

Exact rows:

```text
A_OLD_T_GOTO_DERIVED = 47
B_EVIDENCE_CAPTURE_UNAVAILABLE = 30
C_UNSUPPORTED_TARGET_BLOCK = 1
D_SOKOLOV_CHALLENGE = 2
TOTAL_UNIQUE_RETRY_ROWS = 80
```

This CSV is now the only retry universe for the next acquisition pass.

## 10. Next retry proof requirement

The next Codex run must not be accepted merely because the five canonical files changed.

It must additionally produce:

`STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv`

with exactly one row for each of the 80 frozen retry IDs and actual per-URL browser outcome evidence.

## 11. Quality score

```text
GOAL_AND_OUTPUT_COMPLETENESS = 3.0/10
METHOD_AND_SOURCE_SUPPORT = 7.0/10
INPUT_EVIDENCE_AND_PROVENANCE_INTEGRITY = 7.5/10
COVERAGE_AND_COMPLETENESS = 4.0/10
ANALYTICAL_CORRECTNESS_AND_CLAIM_BOUNDARIES = 4.0/10
ADVERSARIAL_QA_QUALITY = 2.0/10
PERSISTENCE_READBACK_AND_REPRODUCIBILITY = 8.0/10
OWNER_CLIENT_USABILITY_AND_PLAIN_LANGUAGE = 6.0/10
INFORMATION_GAIN_COST_AND_EXECUTION_EFFICIENCY = 2.0/10
DOWNSTREAM_READINESS = 2.0/10

QUALITY_TOTAL = 45.5 / 100
QUALITY_SCORE = 4.55 / 10
```

Hard failures block PASS independently of the score.

## 12. Acceptance

```text
FINAL_NARROW_RETRY_RETURN = REJECTED
CANONICAL_RECOVERY_PUBLICATION = FORBIDDEN
STEP07_SEMANTIC_REWORK = BLOCKED
STEP08 = BLOCKED_NOT_STARTED
NEXT_ACTION = CODEX_VERIFIED_80_URL_RETRY
```
