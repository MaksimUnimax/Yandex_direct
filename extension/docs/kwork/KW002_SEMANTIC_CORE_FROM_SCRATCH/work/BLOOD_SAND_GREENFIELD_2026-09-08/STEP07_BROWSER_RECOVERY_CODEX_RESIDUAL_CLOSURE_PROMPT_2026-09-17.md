# KW-002 / BLOOD & SAND — STEP07 BROWSER RECOVERY — CODEX RESIDUAL CLOSURE

Status: **CURRENT / EXECUTION-ONLY / RESIDUAL ACQUISITION CLOSURE**

CONTINUE THE EXISTING KW-002 BLOOD & SAND GREENFIELD SEMANTIC-CORE REHEARSAL.

THIS IS NOT A NEW PROJECT.
THIS IS NOT STEP08.
THIS IS NOT STEP07 SEMANTIC CANDIDATE CLASSIFICATION.
THIS IS NOT A FULL 1976-URL RESTART.

Your task is to preserve all valid browser-recovery evidence, correct deterministic terminal-state defects, and perform real browser acquisition only for the exact residual rows defined below.

Do NOT redo Main Chat governance/research/release work.
Do NOT make Wordstat, Yandex Search, AI Search or GenSearch provider calls.
Do NOT classify Step07 semantic candidates.
Do NOT commit/push/PR.

Repository:
`MaksimUnimax/Yandex_direct`

Branch:
`roadmap/kwork-productization-2026-08-28`

Job root:
`extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

======================================================================
1. STARTUP — NARROW ONLY
======================================================================

Fetch the CURRENT live branch and record:

`CODEX_RESIDUAL_CLOSURE_START_REMOTE_HEAD`

Read IN FULL:

```text
STEP07_BROWSER_RECOVERY_VERIFIED_80_RETURN_MAIN_CHAT_QA_2026-09-17.md
STEP07_BROWSER_RECOVERY_CODEX_RESIDUAL_CLOSURE_PROMPT_2026-09-17.md
STEP07_BROWSER_RECOVERY_CODEX_VERIFIED_80_URL_RETRY_PROMPT_2026-09-17.md
STEP07_OPERA_BROWSER_CONTROL_PROBE_2026-09-17.md
STEP_07_AUTHORIZED_COMPETITOR_UNIVERSE.csv
```

Use the latest owner-returned verified 80-URL six-file recovery package already present in your local Codex workspace as the base.

Expected base identities:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
SHA256 = a56240dd8c2084fe2da415e7b87b8230cc28852d04a4fef762a0e906c48d6d95

STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
SHA256 = 0c21c243b9f873829b8b9a8666a1a0b4cce9b5b1c36dc9d0c06936bd42f23309

STEP07_BROWSER_RECOVERY_COVERAGE.csv
SHA256 = ee36dce7b26019ece9d114d937a8cbd8109a285aaf2be2ae006d5d3e4c9fd4c1

STEP07_BROWSER_RECOVERY_QA.md
SHA256 = 14045db51fce14869f881aad391812a04278238bd80091a7287a6b3b6ae04457

STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv
SHA256 = 1cbe984c47854eeb55eb1a1a07fc3134a030a1a841cd6a7f22e82326a01295a6
```

If those base data artifacts do not match, stop and report `BASE_ARTIFACT_DRIFT`.

If the authorized 32-competitor universe materially changed, stop with `AUTHORITY_DRIFT`.

Otherwise execute immediately.

======================================================================
2. PRESERVE VALID DATA — NO FULL RESTART
======================================================================

Do not recollect or rewrite valid rows/evidence outside the exact correction/retry predicates below except for deterministic coverage/count/manifest consequences.

Preserve existing valid:

```text
EXCLUDED_OUT_OF_SCOPE rows
EXCLUDED_DUPLICATE rows
normal RECOVERED_INSPECTED evidence
real REDIRECTED_IN_SCOPE evidence with actual redirect chain
valid page-evidence text/hashes
accepted verified-80 retry audit
```

======================================================================
3. DETERMINISTIC CORRECTION SET — NO BROWSER REQUIRED
======================================================================

Derive from the base package exactly this set:

```text
terminal_status = REDIRECTED_IN_SCOPE
AND normalized(source_url_raw) = normalized(final_url)
AND page evidence redirect_chain is empty
AND page evidence is NOT a challenge/block page
```

Normalization for this equality check may ignore only a terminal `/` difference.

Expected count from the frozen base package:

`DETERMINISTIC_SAME_URL_FALSE_REDIRECT_ROWS = 39`

For every such row:

```text
terminal_status = RECOVERED_INSPECTED
preserve existing page_evidence_id
preserve page evidence bytes/text/hash
browser_rendered = true
error_class = blank
error_detail = blank
notes append RESIDUAL_CLOSURE_DETERMINISTIC_FALSE_REDIRECT_FIX=true
```

Do NOT perform new browser acquisition for these 39 rows.

Hard rule:

```text
REDIRECTED_IN_SCOPE
→ actual redirect relation exists
→ normalized source URL differs from normalized final URL
   OR evidence redirect_chain is non-empty and proves an actual redirect
```

After correction:

`SAME_URL_EMPTY_CHAIN_REDIRECT_ROWS = 0`

======================================================================
4. EXACT BROWSER RETRY UNIVERSE — 90 ROWS
======================================================================

Derive the browser retry set from the BASE URL ledger only using these exact rules.

### Set R1 — residual execution-environment failures

All rows where:

`terminal_status = EXECUTION_ENVIRONMENT_FAILURE`

Expected count:

`R1 = 51`

### Set R2 — residual unresolved dynamic content

All rows where:

`terminal_status = UNRESOLVED_DYNAMIC_CONTENT`

Expected count:

`R2 = 34`

### Set R3 — Azbyka challenge pages misclassified as content

Exactly:

```text
R9-S07U001947
R9-S07U001948
R9-S07U001949
R9-S07U001950
```

Expected count:

`R3 = 4`

### Set R4 — Kartaslov false target-block claim

Exactly:

`R9-S07U000396`

Expected count:

`R4 = 1`

The sets are disjoint in the frozen base.

Hard total:

```text
RESIDUAL_BROWSER_RETRY_ROWS
= R1 + R2 + R3 + R4
= 51 + 34 + 4 + 1
= 90
```

Before browser execution, materialize the derived 90 IDs locally and prove:

```text
RESIDUAL_BROWSER_RETRY_ROWS = 90
UNIQUE_RESIDUAL_BROWSER_RETRY_IDS = 90
R1 = 51
R2 = 34
R3 = 4
R4 = 1
```

If any expected count differs, STOP with `RESIDUAL_SET_DRIFT`.

Do not invent/add any other URL to the retry universe.

======================================================================
5. REAL BROWSER ACTION REQUIRED FOR ALL 90
======================================================================

For every exact residual browser row:

1. navigate to its exact `source_url_raw` using a real browser/browser-automation route;
2. wait for a meaningful rendered browser/target result;
3. if the first attempt fails before a meaningful target response because of environment/runtime/timeout/empty-rendered-content, perform ONE second normal fresh-tab/browser retry using the same legitimate public route;
4. do not bypass CAPTCHA, anti-bot, robots, login, paywall, certificate/security policy or site-safety policy;
5. record actual start/finish timestamps for the final retry sequence;
6. record final URL/title;
7. if normal content is readable, capture real page evidence and SHA-256;
8. if the target itself displays a challenge/block, record the exact target evidence and classify it as target block;
9. if the execution environment still fails before meaningful target response, preserve exact final environment error;
10. if browser navigation succeeds but meaningful main content still cannot be established, retain truthful `UNRESOLVED_DYNAMIC_CONTENT` with exact evidence/reason.

Forbidden substitutes:

```text
batch relabel without navigation
generic copied error text
synthetic shared timestamps
claiming target block from a normal page widget
claiming successful content from a challenge page
```

======================================================================
6. CHALLENGE / NORMAL-CONTENT CLASSIFICATION
======================================================================

### Azbyka regression control

The base evidence for `R9-S07U001947..1950` contains only DDoS-Guard browser-verification content such as:

```text
DDoS-Guard
Проверка браузера перед переходом на azbyka.ru
Подождите несколько секунд — после проверки сайт откроется автоматически
```

That is NOT normal inspected semantic content.

If retry still shows this challenge, classify `TARGET_CAPTCHA_OR_ANTI_BOT` with exact displayed evidence and remove ordinary page evidence from the semantic evidence set.

If real Azbyka article content loads, capture it normally.

### Kartaslov regression control

`R9-S07U000396` previously displayed a normal public association page plus the site's ordinary `НАУЧИ БОТА!` contribution widget.

```text
NORMAL PUBLIC PAGE + BOT-TRAINING WIDGET
!= ACCESS CHALLENGE
```

Do not classify as target anti-bot merely because the words `бот` / `НАУЧИ БОТА` occur inside normal content.

Only a real access-block/challenge may produce target-block status.

### General challenge detector

Before final classification, adversarially inspect page title/H1/main text for challenge surfaces, including patterns such as:

```text
DDoS-Guard
Проверка браузера
проверяем ваше соединение
Возможно, нужно выключить VPN
CAPTCHA / verify you are human / Just a moment
```

A challenge page must not survive as `RECOVERED_INSPECTED` or ordinary `REDIRECTED_IN_SCOPE` evidence.

======================================================================
7. RESIDUAL RETRY AUDIT — REQUIRED NEW CONTROL FILE
======================================================================

Create:

`STEP07_BROWSER_RECOVERY_RESIDUAL_RETRY_AUDIT.csv`

Exactly 90 rows, one per derived residual retry ID.

Required schema:

```text
residual_set
recovery_url_id
competitor_authority_id
canonical_site
source_url_raw
prior_terminal_status
prior_error_class
retry_started_at_utc
retry_finished_at_utc
browser_navigation_attempted
browser_route
attempt_count
navigation_result
final_url
page_title
final_terminal_status
final_error_class
exact_final_error_detail
page_evidence_id
content_sha256_if_inspected
notes
```

Hard rules:

```text
RESIDUAL_RETRY_AUDIT_ROWS = 90
UNIQUE_RESIDUAL_RETRY_AUDIT_IDS = 90
MISSING_RESIDUAL_IDS = 0
EXTRA_RESIDUAL_IDS = 0
browser_navigation_attempted = true on 90/90
browser_route = true on 90/90
retry timestamps nonblank on 90/90
```

If inspected, evidence ID/hash must resolve to final JSONL.
If target blocked, exact target challenge evidence must be preserved.
If environment failure remains, exact final tool/browser failure must be preserved.
If unresolved remains, exact unresolved reason must be preserved.

======================================================================
8. COVERAGE LEDGER MUST COUNT UNRESOLVED TRUTHFULLY
======================================================================

Regenerate coverage programmatically from the corrected URL ledger.

Hard formula for every competitor:

```text
remaining_unresolved_or_environment_failure_urls
=
count(UNRESOLVED_DYNAMIC_CONTENT)
+
count(EXECUTION_ENVIRONMENT_FAILURE)
```

Current frozen-base defects to eliminate:

```text
wildberries.ru: reported 0, actual 23
livemaster.ru: reported 6, actual 11
joom.ru: reported 0, actual 2
goroskop365.ru: reported 0, actual 4
```

Recovery status must be data-derived:

```text
if UNRESOLVED_DYNAMIC_CONTENT > 0
→ INCOMPLETE_UNRESOLVED_COVERAGE

else if EXECUTION_ENVIRONMENT_FAILURE > 0
→ INCOMPLETE_EXECUTION_ENVIRONMENT_FAILURES

else if target-block/inaccessible evidence > 0
→ COMPLETE_WITH_TARGET_BLOCK_EVIDENCE

else
→ COMPLETE
```

Do not call unresolved/environment-failure coverage complete.

======================================================================
9. REGENERATE FINAL RECOVERY FILES
======================================================================

Regenerate/update the five canonical recovery data/control files:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
STEP07_BROWSER_RECOVERY_COVERAGE.csv
STEP07_BROWSER_RECOVERY_QA.md
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
```

Preserve the accepted existing verified-80 audit unchanged:

`STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv`

Add the new residual audit:

`STEP07_BROWSER_RECOVERY_RESIDUAL_RETRY_AUDIT.csv`

Final handoff therefore contains exactly SEVEN files.

======================================================================
10. QA — DATA DERIVED ONLY
======================================================================

Regenerate `STEP07_BROWSER_RECOVERY_QA.md` from final artifacts.

At minimum prove:

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

VERIFIED_80_RETRY_AUDIT_ROWS = 80
RESIDUAL_BROWSER_RETRY_ROWS = 90
RESIDUAL_RETRY_AUDIT_ROWS = 90
RESIDUAL_RETRY_AUDIT_UNIQUE_IDS = 90
ACTUAL_RESIDUAL_BROWSER_NAVIGATION_ATTEMPTED = 90/90

DETERMINISTIC_SAME_URL_FALSE_REDIRECT_ROWS_INPUT = 39
SAME_URL_EMPTY_CHAIN_REDIRECT_ROWS_FINAL = 0

AZBYKA_CHALLENGE_MISCLASSIFIED_AS_CONTENT = 0
KARTASLOV_NORMAL_PAGE_FALSE_TARGET_BLOCK = 0
CHALLENGE_PAGE_MISCLASSIFIED_AS_INSPECTED_OR_REDIRECT = 0

COVERAGE_REMAINING_FIELD_RECONCILES = PASS
FINAL_UNRESOLVED_DYNAMIC_CONTENT_TOTAL = data-derived
FINAL_EXECUTION_ENVIRONMENT_FAILURE_TOTAL = data-derived
FINAL_RESIDUAL_ACQUISITION_GAPS = sum of those two

NOT_COLLECTED_ON_INSPECTED = 0
UNAUTHORIZED_DOMAIN_ROWS = 0
UNAUTHORIZED_SITEMAP_REFERENCES = 0
PROVIDER_CALLS = 0
STEP08_EXECUTED = false
CANDIDATE_CLASSIFICATION_EXECUTED = false
GIT_MUTATION = none
```

If final residual acquisition gaps are non-zero, browser recovery is still `INCOMPLETE`; do not declare PASS.

Truthful target-block/inaccessible evidence is allowed and does not by itself count as an execution gap.

======================================================================
11. MANIFEST — REMOVE STALE METADATA
======================================================================

Regenerate `STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json` from final bytes.

Required corrections:

```text
artifact_set = KW002_STEP07_BROWSER_RECOVERY_RESIDUAL_CLOSURE
```

Use exact canonical terminal-state names in `terminal_counts`, including:

`TARGET_CAPTCHA_OR_ANTI_BOT`

Do NOT use alias `TARGET_BLOCKED`.

Record actual current heads:

```text
codex_residual_closure_start_remote_head
codex_residual_closure_pre_handoff_remote_head
```

Do not retain stale `3191f221...` metadata from an older rework.

Manifest `files[]` contains all seven returned files.

For self-entry:

```text
sha256 = SELF_HASH_NOT_APPLICABLE
byte_size = actual final manifest byte size
row_count_or_jsonl_record_count = 1
```

All other hashes/sizes/counts must match actual final bytes.

======================================================================
12. PRE-HANDOFF REMOTE CHECK
======================================================================

Fetch the current branch again and record:

`CODEX_RESIDUAL_CLOSURE_PRE_HANDOFF_REMOTE_HEAD`

If competitor authority materially changed, stop with `AUTHORITY_DRIFT`.

======================================================================
13. HANDOFF
======================================================================

Do NOT commit/push/PR.

Return direct downloadable links for exactly seven files:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
STEP07_BROWSER_RECOVERY_COVERAGE.csv
STEP07_BROWSER_RECOVERY_QA.md
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv
STEP07_BROWSER_RECOVERY_RESIDUAL_RETRY_AUDIT.csv
```

Create ONE transport ZIP containing exactly those seven files.

Owner returns the package to Main Chat for independent acceptance.

======================================================================
14. FINAL REPORT
======================================================================

Return at minimum:

```text
CODEX_RESIDUAL_CLOSURE_START_REMOTE_HEAD
CODEX_RESIDUAL_CLOSURE_PRE_HANDOFF_REMOTE_HEAD

DETERMINISTIC_SAME_URL_FALSE_REDIRECT_ROWS_FIXED = 39/39
RESIDUAL_BROWSER_RETRY_ROWS = 90
RESIDUAL_RETRY_AUDIT_ROWS = 90
ACTUAL_RESIDUAL_BROWSER_NAVIGATION_ATTEMPTED = 90/90

FINAL_TERMINAL_STATUS_COUNTS
FINAL_UNRESOLVED_DYNAMIC_CONTENT_TOTAL
FINAL_EXECUTION_ENVIRONMENT_FAILURE_TOTAL
FINAL_RESIDUAL_ACQUISITION_GAPS

AZBYKA_CHALLENGE_MISCLASSIFIED_AS_CONTENT = 0
KARTASLOV_NORMAL_PAGE_FALSE_TARGET_BLOCK = 0
SAME_URL_EMPTY_CHAIN_REDIRECT_ROWS_FINAL = 0
COVERAGE_REMAINING_FIELD_RECONCILES = PASS
MANIFEST_METADATA = PASS
MANIFEST_SELF_BYTE_SIZE_MATCH = PASS
URL_LEDGER_SCHEMA = PASS
COVERAGE_SCHEMA = PASS
PAGE_EVIDENCE_SCHEMA = PASS
SHA_VERIFICATION = PASS
JOIN_QA = PASS

PROVIDER_CALLS = 0
STEP08_EXECUTED = false
CANDIDATE_CLASSIFICATION_EXECUTED = false
GIT_MUTATION = none
```

Do not declare browser recovery PASS if `FINAL_RESIDUAL_ACQUISITION_GAPS > 0`.
