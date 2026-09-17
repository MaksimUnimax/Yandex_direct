# KW-002 / BLOOD & SAND — STEP07 BROWSER RECOVERY — CODEX FINAL NARROW RETRY

Status: **CURRENT / EXECUTION-ONLY / FINAL NARROW RETRY**

CONTINUE THE EXISTING KW-002 BLOOD & SAND GREENFIELD SEMANTIC-CORE REHEARSAL.

THIS IS NOT A NEW PROJECT.
THIS IS NOT STEP08.
THIS IS NOT STEP07 SEMANTIC CANDIDATE CLASSIFICATION.
THIS IS NOT A FULL RECOVERY RESTART.

Your task is to correct ONLY the still-defective browser-recovery rows and regenerate the five canonical recovery artifacts.

Do NOT redo Main Chat governance/research/release work.
Do NOT recollect already valid successful page evidence unless a defective row requires it.
Do NOT make Wordstat, Yandex Search, AI Search or GenSearch provider calls.
Do NOT classify Step07 candidates.
Do NOT commit/push/PR.

Repository:
`MaksimUnimax/Yandex_direct`

Branch:
`roadmap/kwork-productization-2026-08-28`

Job root:
`extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

======================================================================
1. STARTUP PREFLIGHT — NARROW ONLY
======================================================================

Fetch current remote branch and record `CODEX_FINAL_RETRY_START_REMOTE_HEAD`.

Read IN FULL:

```text
STEP07_BROWSER_RECOVERY_LIMITED_REWORK_MAIN_CHAT_RETURN_QA_2026-09-17.md
STEP07_BROWSER_RECOVERY_CODEX_FINAL_NARROW_RETRY_PROMPT_2026-09-17.md
STEP07_BROWSER_RECOVERY_CODEX_LIMITED_REWORK_PROMPT_2026-09-17.md
STEP07_OPERA_BROWSER_CONTROL_PROBE_2026-09-17.md
STEP_07_AUTHORIZED_COMPETITOR_UNIVERSE.csv
```

Use the corrected limited-rework five-file package in your current Codex workspace as the base.

If the 32-authorized-competitor authority changed materially, STOP with `AUTHORITY_DRIFT`.

Otherwise execute immediately.

======================================================================
2. PRESERVE VALID DATA
======================================================================

Preserve all rows/evidence that already independently pass:

```text
EXCLUDED_OUT_OF_SCOPE = 1201
EXCLUDED_DUPLICATE = 24
valid RECOVERED_INSPECTED page evidence
valid REDIRECTED_IN_SCOPE page evidence
valid SHA-256/text identities
```

Do NOT restart the complete 1976-URL collection from zero.

Only defective/retry-scope rows may change terminal status/evidence.

======================================================================
3. MANDATORY RETRY SET A — THE 47 OLD `t.goto` ROWS
======================================================================

Identify exactly the 47 current URL-ledger rows whose final state is:

```text
terminal_status = EXECUTION_ENVIRONMENT_FAILURE
error_class = BROWSER_RUNTIME_FAILURE
error_detail = Navigation primitive failure was corrected during limited rework; no final target response was obtained.
```

These are the old `TypeError: t.goto is not a function` rows.

The prior rework did NOT demonstrate the required per-URL browser retry.

For ALL 47:

1. use the actual working browser navigation primitive;
2. navigate to the exact `source_url_raw` as a normal public browser user;
3. wait for a meaningful target/browser result;
4. capture actual rendered content if available;
5. classify the actual final state;
6. store the actual retry timestamp for that URL;
7. do not use one shared synthetic timestamp/detail for the 47 rows.

Main Chat independently verified after the failed rework that exact affected URLs are browser-readable, including:

```text
https://slavyanskieoberegi.ru/katalog-slavyanskix-oberegov/
https://happywitch.ru/catalog/products/amulety_i_talismany/
https://www.oum.ru/yoga/mantry/chto-oznachaet-simvol-om/
```

Therefore a generic `BROWSER_RUNTIME_FAILURE` on all 47 is not acceptable.

For every final environment failure, `error_detail` must contain the exact actual final retry/tool error, not a generic narrative sentence.

Add to `notes` for these rows:

`FINAL_NARROW_RETRY_ATTEMPTED=true`

If successfully inspected, create/update page evidence and real SHA-256.

======================================================================
4. MANDATORY RETRY SET B — 30 EVIDENCE_CAPTURE_UNAVAILABLE ROWS
======================================================================

Retry every current row with:

```text
terminal_status = EXECUTION_ENVIRONMENT_FAILURE
error_class = EVIDENCE_CAPTURE_UNAVAILABLE
```

Expected current count = 30.

Known distribution from Main Chat QA:

```text
wildberries.ru = 23
livemaster.ru = 5
joom.ru = 2
```

### Wildberries

Main Chat's Opera control observed a genuine current browser-level Wildberries VPN/anti-bot block:

`Возможно, нужно выключить VPN`

Do not bypass it.

For each Wildberries URL, perform one normal browser retry. If the same target-level block is actually shown, classify truthfully as target anti-bot/block and preserve the actual displayed evidence in `error_class/error_detail/notes` rather than `EVIDENCE_CAPTURE_UNAVAILABLE`.

If your browser environment fails before receiving a meaningful Wildberries response, retain an environment failure with the exact tool error.

### Livemaster / Joom

Perform one normal browser retry for all seven URLs.

Recover content if accessible; otherwise preserve the exact actual target/environment result.

======================================================================
5. MANDATORY RETRY SET C — ASSERTED TARGET BLOCK WITHOUT EVIDENCE
======================================================================

Retry exact URL-ledger row:

`R9-S07U000396`

Current state asserts `TARGET_CAPTCHA_OR_ANTI_BOT` but has blank `error_class`, blank `error_detail`, `target_http_status=NOT_COLLECTED` and `browser_rendered=false`.

That target-block claim is not sufficiently evidenced.

Required outcome:

- if actual target CAPTCHA/anti-bot is shown: retain target-block state and record exact observed block evidence;
- if normal content loads: recover it;
- if environment fails first: classify `EXECUTION_ENVIRONMENT_FAILURE` with exact error;
- do not preserve unsupported target-block assertion.

======================================================================
6. MANDATORY RETRY SET D — SOKOLOV CHALLENGE PAGES
======================================================================

Retry:

```text
R9-S07U001927
R9-S07U001928
```

Current evidence main text is only:

`Пожалуйста, подождите, мы проверяем ваше соединение... © SOKOLOV`

while current terminal status is `REDIRECTED_IN_SCOPE` and `source_url_raw == final_url`.

This is not valid ordinary redirected-page evidence.

Required:

- normal content available → classify inspected and capture real content;
- challenge/anti-bot persists → classify target block with exact displayed evidence;
- execution environment fails first → environment failure with exact actual error.

Do not retain these as ordinary redirect evidence if only the challenge page is captured.

======================================================================
7. URL LEDGER / EVIDENCE INVARIANTS
======================================================================

Keep the already-correct exact URL-ledger schema and page-evidence field contract.

For every final `RECOVERED_INSPECTED` or redirected row carrying page evidence:

```text
page_evidence_id resolves exactly once
full_visible_main_text is non-empty real rendered text
content_sha256 is lowercase 64-hex SHA-256 of UTF-8 full_visible_main_text
browser_route = true
```

No `NOT_COLLECTED`, `UNKNOWN` or placeholder for text/hash on inspected evidence.

Every final `EXECUTION_ENVIRONMENT_FAILURE`:

```text
error_class != blank
error_detail = exact actual final retry/tool failure
captured_at_utc = actual retry timestamp for that row
```

Every final target block must preserve actual target-level evidence sufficient to distinguish it from executor failure.

======================================================================
8. CORRECT QA COUNTS — DATA-DERIVED ONLY
======================================================================

Regenerate `STEP07_BROWSER_RECOVERY_QA.md` from the final ledger.

Do NOT hardcode the prior false table.

Programmatically derive:

```text
FINAL_TERMINAL_STATUS_COUNTS
FINAL_EXECUTION_ENVIRONMENT_FAILURE_TOTAL
FINAL_ERROR_CLASS_COUNTS
FINAL_ERROR_CLASS_COUNTS_SUM
```

Hard assertion:

```text
FINAL_ERROR_CLASS_COUNTS_SUM
=
FINAL_EXECUTION_ENVIRONMENT_FAILURE_TOTAL
```

The rejected limited-rework QA falsely reported `105 + 40 + 30` while total environment failures were `128`. That contradiction must be impossible in the new QA.

Also prove:

```text
OLD_T_GOTO_ROW_COUNT = 47
OLD_T_GOTO_ROWS_ACTUALLY_RETRIED = 47
OLD_T_GOTO_GENERIC_PLACEHOLDER_ERROR_DETAIL_FINAL = 0
FINAL_NARROW_RETRY_NOTES_PRESENT_ON_47 = 47
UNSUPPORTED_TARGET_BLOCK_ROWS = 0
SOKOLOV_CHALLENGE_MISCLASSIFIED_AS_REDIRECT = 0
NOT_COLLECTED_ON_INSPECTED = 0
UNAUTHORIZED_DOMAIN_ROWS = 0
UNAUTHORIZED_SITEMAP_REFERENCES = 0
```

======================================================================
9. MANIFEST SELF-IDENTITY FIX
======================================================================

Regenerate `STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json`.

For the manifest's own `files[]` entry:

- `sha256 = SELF_HASH_NOT_APPLICABLE` is allowed because recursive self-hash cannot be stable;
- `byte_size` MUST equal the actual final manifest byte size, not `0`;
- `row_count_or_jsonl_record_count = 1`.

All other file SHA-256/byte-size/count values must match the actual final bytes.

======================================================================
10. REQUIRED FINAL OUTPUTS
======================================================================

Replace exactly these five corrected artifacts in your local workspace:

1. `STEP07_BROWSER_RECOVERY_URL_LEDGER.csv`
2. `STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl`
3. `STEP07_BROWSER_RECOVERY_COVERAGE.csv`
4. `STEP07_BROWSER_RECOVERY_QA.md`
5. `STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json`

Create one transport ZIP containing exactly those five files.

Do NOT commit/push/PR.

======================================================================
11. FINAL QA / STOP CONDITION
======================================================================

Before packaging, prove:

```text
SOURCE_URL_ROWS = 1976
AUTHORIZED_COMPETITORS = 32
SILENT_SKIP = 0
URL_LEDGER_SCHEMA = PASS
COVERAGE_SCHEMA = PASS
PAGE_EVIDENCE_SCHEMA = PASS
URL_PK_UNIQUE = PASS
EVIDENCE_PK_UNIQUE = PASS
JOINS = PASS
SHA_VERIFICATION = PASS
OLD_T_GOTO_ROWS_ACTUALLY_RETRIED = 47/47
OLD_T_GOTO_GENERIC_PLACEHOLDER_ERROR_DETAIL_FINAL = 0
EVIDENCE_CAPTURE_UNAVAILABLE_ROWS_RETRIED = 30/30
UNSUPPORTED_TARGET_BLOCK_ROWS = 0
SOKOLOV_CHALLENGE_MISCLASSIFIED_AS_REDIRECT = 0
FINAL_ERROR_CLASS_COUNTS_SUM_MATCHES_ENV_FAILURE_TOTAL = PASS
MANIFEST_SELF_BYTE_SIZE_MATCH = PASS
UNAUTHORIZED_DOMAIN_ROWS = 0
UNAUTHORIZED_SITEMAP_REFERENCES = 0
PROVIDER_CALLS = 0
STEP08_EXECUTED = false
CANDIDATE_CLASSIFICATION_EXECUTED = false
GIT_MUTATION = none
```

Truthful residual environment failures are allowed.

Unretried old producer failures, generic replacement errors, unsupported target blocks or false QA totals are NOT allowed.

======================================================================
12. PRE-HANDOFF REMOTE CHECK
======================================================================

Fetch current remote branch again and record:

`CODEX_FINAL_RETRY_PRE_HANDOFF_REMOTE_HEAD`

If competitor authority materially changed, stop with `AUTHORITY_DRIFT`.

======================================================================
13. HANDOFF
======================================================================

Return direct downloadable links for the five corrected files plus one transport-only ZIP.

Do not upload to GitHub.

Owner returns package to Main Chat for acceptance QA.

======================================================================
14. FINAL REPORT
======================================================================

Return at minimum:

```text
CODEX_FINAL_RETRY_START_REMOTE_HEAD
CODEX_FINAL_RETRY_PRE_HANDOFF_REMOTE_HEAD
SOURCE_URL_ROWS
FINAL_TERMINAL_STATUS_COUNTS
FINAL_EXECUTION_ENVIRONMENT_FAILURE_TOTAL
FINAL_ERROR_CLASS_COUNTS
OLD_T_GOTO_ROWS_ACTUALLY_RETRIED
OLD_T_GOTO_GENERIC_PLACEHOLDER_ERROR_DETAIL_FINAL
EVIDENCE_CAPTURE_UNAVAILABLE_ROWS_RETRIED
UNSUPPORTED_TARGET_BLOCK_ROWS
SOKOLOV_CHALLENGE_MISCLASSIFIED_AS_REDIRECT
MANIFEST_SELF_BYTE_SIZE_MATCH
URL_LEDGER_SCHEMA
COVERAGE_SCHEMA
PAGE_EVIDENCE_SCHEMA
SHA_VERIFICATION
JOIN_QA
PROVIDER_CALLS = 0
STEP08_EXECUTED = false
CANDIDATE_CLASSIFICATION_EXECUTED = false
GIT_MUTATION = none
```

Do not declare PASS if any hard assertion above fails.
