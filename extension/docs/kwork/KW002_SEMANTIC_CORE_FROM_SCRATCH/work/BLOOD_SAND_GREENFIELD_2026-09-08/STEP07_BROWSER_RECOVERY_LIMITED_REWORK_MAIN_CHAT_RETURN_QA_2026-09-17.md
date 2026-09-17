# KW-002 / BLOOD & SAND — STEP07 BROWSER RECOVERY LIMITED REWORK — MAIN CHAT RETURN QA

Date: 2026-09-17
Status: **REJECTED / FINAL NARROW RETRY REQUIRED**

## 1. Scope

Main Chat independently inspected the owner-returned corrected five-file browser-recovery package plus transport ZIP produced under `STEP07_BROWSER_RECOVERY_CODEX_LIMITED_REWORK_PROMPT_2026-09-17.md`.

The returned package was NOT published to GitHub as canonical browser-recovery evidence because acceptance failed before owner staging publication.

## 2. Package identity / mechanical checks

Owner-returned local artifacts:

- `STEP07_BROWSER_RECOVERY_URL_LEDGER.csv`
- `STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl`
- `STEP07_BROWSER_RECOVERY_COVERAGE.csv`
- `STEP07_BROWSER_RECOVERY_QA.md`
- `STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json`
- transport ZIP containing exactly those five files.

Independent byte/hash verification:

```text
URL_LEDGER_SHA256 = 27c313b2c0efe7cce785d8233dce44562e51bb642f99bac0b6d819393bcb8859
PAGE_EVIDENCE_SHA256 = e102a06e6dbac438c4db40c16ac5e7b983d46d98507bf3820529b8e7f05f4a65
COVERAGE_SHA256 = 0b379ad40cc49d414df810e83a05109f3c4a2825aba93a1ee1af2b33301538bd
QA_SHA256 = 6a76602c75902a8cbc57d346345275d4e62c91a7749e94cfc4086b7b94ff5e28
MANIFEST_ACTUAL_SHA256 = 7d09ef642643a756af188544b09be89a5d9c7f90539ed620ba1808c410bf8889
TRANSPORT_ZIP_SHA256 = 1874709fec84f7f3c454afec274a6d09c8fb6b5e40cacf42bc1f5289ad315b92
```

ZIP payload byte identities matched the five returned standalone files.

## 3. Checks that PASS

```text
SOURCE_URL_ROWS = 1976
AUTHORIZED_COMPETITOR_IDS = 32 / S07A001..S07A032
URL_LEDGER_EXACT_FIELD_ORDER = PASS
COVERAGE_EXACT_FIELD_ORDER = PASS
PAGE_EVIDENCE_EXACT_FIELD_ORDER = PASS
URL_PRIMARY_KEYS_UNIQUE = PASS
EVIDENCE_PRIMARY_KEYS_UNIQUE = PASS
PAGE_EVIDENCE_ROWS = 622
EVERY_URL_PAGE_EVIDENCE_JOIN_RESOLVES = PASS
UNUSED_PAGE_EVIDENCE_ROWS = 0
RECOVERED_INSPECTED_ROWS = 318
REDIRECTED_IN_SCOPE_ROWS = 304
EVERY_RECOVERED_INSPECTED_HAS_PAGE_EVIDENCE = PASS
EVERY_RECOVERED_INSPECTED_HAS_NONEMPTY_FULL_VISIBLE_MAIN_TEXT = PASS
EVERY_PAGE_EVIDENCE_CONTENT_SHA256_FORMAT = PASS
EVERY_PAGE_EVIDENCE_CONTENT_SHA256_MATCHES_UTF8_TEXT = PASS
NOT_COLLECTED_IN_FULL_VISIBLE_MAIN_TEXT_OR_CONTENT_SHA256 = 0
UNAUTHORIZED_SOURCE_URL_HOST_ROWS = 0
UNAUTHORIZED_OKNO_MSK_REFERENCE = 0
LITERAL_T_GOTO_ERROR_ROWS = 0
PROVIDER_CALLS = 0
STEP08_EXECUTED = false
CANDIDATE_CLASSIFICATION_EXECUTED = false
```

Terminal ledger totals reconcile:

```text
EXCLUDED_OUT_OF_SCOPE = 1201
EXCLUDED_DUPLICATE = 24
RECOVERED_INSPECTED = 318
REDIRECTED_IN_SCOPE = 304
TARGET_CAPTCHA_OR_ANTI_BOT = 1
EXECUTION_ENVIRONMENT_FAILURE = 128
TOTAL = 1976
```

Coverage table programmatically reconciles its `recovery_urls_attempted`, `recovery_inspected_urls`, target-blocked, environment-failure, page-evidence and remaining-failure fields to the corrected URL/evidence ledgers.

## 4. HARD FAILURE H1 — mandatory retry of all 47 old `t.goto` failures was not actually demonstrated

The previous recovery contained exactly 47 rows whose concrete failure was:

`TypeError: t.goto is not a function`

The limited-rework prompt explicitly required:

```text
fix the navigation primitive
→ retry ALL 47 affected URLs
→ preserve the actual resulting target/environment outcome
```

In the returned corrected URL ledger:

```text
OLD_T_GOTO_AFFECTED_ROWS = 47
FINAL_STATUS_FOR_ALL_47 = EXECUTION_ENVIRONMENT_FAILURE
FINAL_ERROR_CLASS_FOR_ALL_47 = BROWSER_RUNTIME_FAILURE
FINAL_ERROR_DETAIL_FOR_ALL_47 = "Navigation primitive failure was corrected during limited rework; no final target response was obtained."
FINAL_CAPTURED_AT_UTC_FOR_ALL_47 = 2026-09-17T10:06:35.7253053Z
FINAL_NOTES_FOR_ALL_47 = "0 links observed"
```

This is not row-specific retry evidence. It is a batch replacement of the old concrete TypeError with one generic sentence.

Main Chat independently retried exact affected URLs through the owner's connected Opera Browser Connector after receiving this corrected package and proved that multiple exact URLs are currently browser-readable, including:

- `https://slavyanskieoberegi.ru/katalog-slavyanskix-oberegov/`
- `https://happywitch.ru/catalog/products/amulety_i_talismany/`
- `https://www.oum.ru/yoga/mantry/chto-oznachaet-simvol-om/`

Their rendered public content/accessibility trees were readable. Therefore at least some of the unchanged 47 generic failures are demonstrably false-negative final states.

```text
T_GOTO_LITERAL_REMOVED = true
MANDATORY_47_URL_RETRY_PROVED = false
```

Hard gate = FAIL.

## 5. HARD FAILURE H2 — returned QA contains false environment-failure totals

Actual `EXECUTION_ENVIRONMENT_FAILURE` rows in the returned URL ledger:

```text
BROWSER_RUNTIME_FAILURE = 58
NAVIGATION_TIMEOUT = 40
EVIDENCE_CAPTURE_UNAVAILABLE = 30
TOTAL = 128
```

Returned `STEP07_BROWSER_RECOVERY_QA.md` instead states:

```text
BROWSER_RUNTIME_FAILURE = 105
NAVIGATION_TIMEOUT = 40
EVIDENCE_CAPTURE_UNAVAILABLE = 30
```

Those claimed classes sum to 175 while the same QA states corrected environment failures = 128.

Therefore:

```text
QA_ERROR_CLASS_TOTALS = FAIL
QA_SELF_RECONCILIATION = FAIL
```

The prompt required exact remaining environment-failure totals by error class. Hard gate = FAIL.

## 6. HARD FAILURE H3 — target block vs environment failure remains misclassified

The returned ledger reclassified 30 previous placeholder evidence rows to `EVIDENCE_CAPTURE_UNAVAILABLE` environment failures:

```text
wildberries.ru = 23
livemaster.ru = 5
joom.ru = 2
```

But Main Chat's accepted Opera control observed a real browser-level Wildberries VPN/anti-bot block (`Возможно, нужно выключить VPN`). The limited-rework prompt explicitly required preserving valid Main Chat target-block observations and distinguishing them from execution-environment failures.

The 23 Wildberries rows cannot be batch-kept as generic environment capture failures without an actual final per-URL retry/outcome. They require truthful final retry/classification.

Additionally, the sole `TARGET_CAPTCHA_OR_ANTI_BOT` row (`R9-S07U000396`) has:

```text
target_http_status = NOT_COLLECTED
browser_rendered = false
error_class = blank
error_detail = blank
```

That does not preserve sufficient target-level evidence for the asserted target block.

Hard gate = FAIL.

## 7. HARD FAILURE H4 — challenge content is retained as ordinary redirected page evidence

Two Sokolov rows:

- `R9-S07U001927`
- `R9-S07U001928`

remain `REDIRECTED_IN_SCOPE` while their page evidence main text is only:

`Пожалуйста, подождите, мы проверяем ваше соединение... © SOKOLOV`

and `source_url_raw == final_url`.

This is challenge/block-like content, not proven normal inspected content behind an in-scope redirect. These rows require normal retry and truthful reclassification.

Hard gate = FAIL.

## 8. Manifest identity defect

The manifest's self-entry reports:

```text
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
sha256 = SELF_HASH_NOT_APPLICABLE
byte_size = 0
```

Actual returned manifest byte size is `1979` bytes.

Self-hash recursion may use an explicit sentinel, but byte size must not be false. Fix the self-entry or use an explicit self-identity convention that reports the actual byte size.

## 9. Remaining truthful environment failures are allowed only after actual retry

The contract allows truthful residual environment failures. It does NOT require artificial zero failures.

The acceptance problem is not `128 > 0` by itself.

The problem is:

- 47 required retries were not demonstrated and multiple exact URLs are independently readable;
- 30 generic capture failures were not truthfully reconciled with known target-block/browser evidence;
- returned QA reports impossible error-class totals;
- target/challenge states remain insufficiently evidenced/misclassified.

## 10. Quality score

Each criterion scored independently 0–10:

```text
GOAL_AND_OUTPUT_COMPLETENESS = 7.5/10
METHOD_AND_SOURCE_SUPPORT = 8.0/10
INPUT_EVIDENCE_AND_PROVENANCE_INTEGRITY = 8.0/10
COVERAGE_AND_COMPLETENESS = 6.0/10
ANALYTICAL_CORRECTNESS_AND_CLAIM_BOUNDARIES = 5.5/10
ADVERSARIAL_QA_QUALITY = 4.5/10
PERSISTENCE_READBACK_AND_REPRODUCIBILITY = 8.0/10
OWNER_CLIENT_USABILITY_AND_PLAIN_LANGUAGE = 7.0/10
INFORMATION_GAIN_COST_AND_EXECUTION_EFFICIENCY = 7.0/10
DOWNSTREAM_READINESS = 4.0/10

QUALITY_TOTAL = 65.5 / 100
QUALITY_SCORE = 6.55 / 10
```

What lost points:

- mandatory retry semantics were not fulfilled;
- final target/environment states are not fully truthful;
- QA contains mathematically impossible error-class totals;
- downstream semantic rework cannot safely treat browser recovery as accepted authority.

Hard failures independently block PASS regardless of score.

## 11. Acceptance decision

```text
STEP07_BROWSER_RECOVERY_LIMITED_REWORK_OWNER_RETURN = RECEIVED
MECHANICAL_ARTIFACT_QA = PARTIAL_PASS
ANALYTICAL_RETURN_QA = FAIL
MAIN_CHAT_ACCEPTANCE = REJECTED_FINAL_NARROW_RETRY_REQUIRED
CANONICAL_GITHUB_UPLOAD_OF_THIS_RETURN = FORBIDDEN
STEP07_SEMANTIC_REWORK = BLOCKED
STEP08 = BLOCKED_NOT_STARTED
```

## 12. Next action

Run only the final narrow browser-recovery retry defined by:

`STEP07_BROWSER_RECOVERY_CODEX_FINAL_NARROW_RETRY_PROMPT_2026-09-17.md`

Do not recollect the entire successful universe from zero.
