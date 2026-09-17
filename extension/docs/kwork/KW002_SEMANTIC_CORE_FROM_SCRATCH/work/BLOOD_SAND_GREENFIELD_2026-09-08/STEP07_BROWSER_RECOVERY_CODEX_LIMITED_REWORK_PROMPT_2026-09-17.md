# KW-002 / BLOOD & SAND — STEP07 BROWSER RECOVERY — CODEX LIMITED REWORK PROMPT

Status: **CURRENT / EXECUTION-ONLY / LIMITED REWORK OF BROWSER RECOVERY**

CONTINUE THE EXISTING KW-002 BLOOD & SAND GREENFIELD SEMANTIC-CORE REHEARSAL.

THIS IS NOT A NEW PROJECT.
THIS IS NOT STEP08.
THIS IS NOT STEP07 SEMANTIC CLASSIFICATION.
THIS IS A LIMITED REWORK OF THE FIRST BROWSER RECOVERY RETURN.

Do NOT restart successful browser evidence acquisition from zero.
Do NOT rerun Main Chat governance/research/release work.
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
1. FIRST ACTION
======================================================================

Fetch current remote branch.

Read IN FULL:

```text
STEP07_BROWSER_RECOVERY_MAIN_CHAT_RETURN_QA_2026-09-17.md
STEP07_BROWSER_RECOVERY_CODEX_LIMITED_REWORK_PROMPT_2026-09-17.md
STEP07_BROWSER_RECOVERY_CODEX_PROMPT_2026-09-17.md
STEP07_OPERA_BROWSER_CONTROL_PROBE_2026-09-17.md
STEP_07_AUTHORIZED_COMPETITOR_UNIVERSE.csv
```

Use the first recovery artifacts already present in your local Codex workspace as the rework base:

```text
STEP07_BROWSER_RECOVERY_URL_LEDGER.csv
STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl
STEP07_BROWSER_RECOVERY_COVERAGE.csv
STEP07_BROWSER_RECOVERY_QA.md
STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json
```

Record current remote HEAD.

If the authorized 32-competitor universe materially changed, stop with `AUTHORITY_DRIFT`.

Otherwise execute immediately.

======================================================================
2. REWORK PRINCIPLE
======================================================================

Preserve valid first-recovery evidence.

Do NOT discard legitimate browser content merely because the first return failed QA.

The rework must correct the underlying deterministic production rules across the complete affected universe.

```text
PATCH THE PRODUCER
!=
PATCH A FEW EXAMPLES
```

======================================================================
3. FIX URL LEDGER TO THE RELEASED SCHEMA
======================================================================

Regenerate `STEP07_BROWSER_RECOVERY_URL_LEDGER.csv` with exactly these fields in this order:

```text
recovery_url_id
competitor_authority_id
canonical_site
scope_policy
source_url_raw
attempt1_url_id
computed_canonical_url
final_url
discovery_source
discovery_parent_url
access_route
terminal_status
target_http_status
robots_decision
browser_rendered
page_evidence_id
error_class
error_detail
captured_at_utc
notes
```

Requirements:

- preserve all 1976 source URL identities through a deterministic mapping;
- preserve all 32 authorized competitor IDs;
- `attempt1_url_id` must point to the source Attempt-1 URL identity when applicable;
- every row has exactly one terminal status;
- every `RECOVERED_INSPECTED` row has a valid `page_evidence_id`;
- every row with `page_evidence_id` resolves to exactly one JSONL evidence record;
- `EXECUTION_ENVIRONMENT_FAILURE` must expose deterministic `error_class` and full `error_detail`;
- target-level failures must not be mixed with execution-environment failures.

======================================================================
4. FIX COVERAGE TO THE RELEASED RECOVERY SCHEMA
======================================================================

Regenerate `STEP07_BROWSER_RECOVERY_COVERAGE.csv` with exactly one row for each `S07A001..S07A032` and these fields:

```text
competitor_authority_id
canonical_site
attempt1_inspected_urls
attempt1_inaccessible_urls
recovery_urls_attempted
recovery_inspected_urls
recovery_target_blocked_urls
recovery_environment_failure_urls
new_urls_discovered
page_evidence_rows
remaining_unresolved_or_environment_failure_urls
recovery_status
notes
```

Counts must derive programmatically from Attempt-1 + corrected recovery ledgers.

No narrative/manual count overrides.

======================================================================
5. FIX PAGE EVIDENCE TO THE EXACT RELEASED FIELD CONTRACT
======================================================================

Regenerate `STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl` using exactly these fields:

```text
evidence_id
competitor_authority_id
canonical_site
scope_policy
source_url_raw
final_url
computed_canonical_url
declared_canonical_url
redirect_chain
discovery_source
discovery_parent_url
page_type
page_title
h1
headings_h2_h6
breadcrumbs
navigation_labels
category_labels
product_or_service_names
faq_questions
glossary_terms
structured_metadata_visible_or_public
body_text_blocks
full_visible_main_text
content_sha256
captured_at_utc
browser_route
notes
```

Existing first-recovery data may be transformed into these exact fields where semantically equivalent, e.g. split combined arrays deterministically rather than losing data.

Hard evidence rule:

```text
RECOVERED_INSPECTED
→ non-empty full_visible_main_text
→ content_sha256 = valid lowercase 64-hex SHA-256 of UTF-8 full_visible_main_text
```

Do NOT use:

```text
NOT_COLLECTED
UNKNOWN
PLACEHOLDER
```

for `full_visible_main_text` or `content_sha256` on a `RECOVERED_INSPECTED` row.

If content cannot actually be captured, the URL cannot remain `RECOVERED_INSPECTED`; retry normally or classify the truthful terminal state.

The first return had 30 evidence records with `NOT_COLLECTED`, including 28 linked to `RECOVERED_INSPECTED`; all are in mandatory rework scope.

======================================================================
6. RETRY ALL EXECUTION-ENVIRONMENT FAILURES THAT ARE FIXABLE
======================================================================

First recovery returned 98 `EXECUTION_ENVIRONMENT_FAILURE` rows.

Known failure classes from Main Chat independent parsing:

```text
47 = TypeError: t.goto is not a function
38 = normal navigation timeout
8  = browser site-safety policy blocks
5  = other browser/CDP/evaluate/deadline/tool failures
```

### 6.1 `t.goto is not a function`

This is a deterministic executor bug.

Fix the navigation implementation/primitive and retry ALL 47 affected URLs.

Do not preserve this TypeError as final terminal evidence if normal browser navigation now works.

### 6.2 Timeouts / deadline / CDP failures

Give each affected URL one normal browser retry after stabilizing the navigation route.

If it still fails because the execution environment/tool fails before a meaningful target response, retain `EXECUTION_ENVIRONMENT_FAILURE` with exact error class/detail.

If the target itself returns a real block/error, classify the target state instead.

### 6.3 Site-safety policy blocks

Do NOT bypass platform/browser safety policy.

If the browser runtime refuses navigation due to site-safety policy, keep `EXECUTION_ENVIRONMENT_FAILURE` with explicit policy reason.

Do not mislabel as target block.

======================================================================
7. RECHECK THE 30 `NOT_COLLECTED` EVIDENCE RECORDS
======================================================================

Mandatory full-volume correction of all 30 first-return evidence rows where:

```text
content_sha256 = NOT_COLLECTED
or
full_visible_main_text = NOT_COLLECTED
```

For the 28 currently linked to `RECOVERED_INSPECTED`:

- recollect real rendered main content if accessible;
- calculate real SHA-256;
- or reclassify the URL away from `RECOVERED_INSPECTED` if content cannot legitimately be captured.

For redirect rows, preserve the redirect lineage and only attach page evidence when final content was actually read.

======================================================================
8. REMOVE UNAUTHORIZED SITEMAP CONTAMINATION
======================================================================

The first recovery QA incorrectly cited:

`https://okno-msk.ru/sitemap.xml`

This domain is NOT in the 32 authorized Step07 competitor universe and does not occur in the recovery URL ledger.

Remove this evidence/claim completely from Step07 recovery artifacts.

Any sitemap/robots attempt in the corrected recovery must:

```text
belong to an authorized competitor
AND
respect that competitor's exact Step07 scope_policy
```

Do not add `okno-msk.ru` or any other unrelated domain.

If an authorized sitemap cannot be accessed, record the exact authorized host and execution state without claiming sitemap absence.

======================================================================
9. PRESERVE VALID TARGET EVIDENCE / NO BYPASS
======================================================================

Preserve valid observations from first recovery and Main Chat Opera control.

Do not bypass:

- Wildberries VPN/anti-bot block;
- CAPTCHA;
- login;
- robots;
- browser/runtime safety policy;
- certificate/security restrictions where the execution environment forbids access.

Remember:

```text
TARGET BLOCK
!= EXECUTION ENVIRONMENT FAILURE
!= CONNECTOR SECURITY POLICY
```

======================================================================
10. REGENERATE QA PROGRAMMATICALLY
======================================================================

Replace `STEP07_BROWSER_RECOVERY_QA.md`.

At minimum prove with executable checks:

```text
AUTHORIZED_COMPETITOR_ROWS = 32
AUTHORIZED_IDS_EXACT = S07A001..S07A032
SOURCE_URL_UNIVERSE_ACCOUNTED = 1976
SILENT_SKIP = 0
URL_LEDGER_EXACT_SCHEMA = PASS
COVERAGE_EXACT_SCHEMA = PASS
PAGE_EVIDENCE_EXACT_SCHEMA = PASS
URL_PRIMARY_KEYS_UNIQUE = PASS
EVIDENCE_PRIMARY_KEYS_UNIQUE = PASS
EVERY_PAGE_EVIDENCE_JOIN_RESOLVES = PASS
EVERY_RECOVERED_INSPECTED_HAS_PAGE_EVIDENCE = PASS
EVERY_RECOVERED_INSPECTED_HAS_NONEMPTY_FULL_VISIBLE_MAIN_TEXT = PASS
EVERY_RECOVERED_INSPECTED_HAS_VALID_SHA256 = PASS
EVERY_VALID_SHA256_MATCHES_UTF8_FULL_VISIBLE_MAIN_TEXT = PASS
NOT_COLLECTED_ON_RECOVERED_INSPECTED = 0
T_GOTO_TYPEERROR_FINAL_ROWS = 0
UNAUTHORIZED_DOMAIN_ROWS = 0
UNAUTHORIZED_SITEMAP_REFERENCES = 0
TARGET_FAILURES_DISTINGUISHED_FROM_ENVIRONMENT_FAILURES = PASS
ONLY_AUTHORIZED_COMPETITORS_USED = PASS
PROVIDER_CALLS = 0
STEP08_EXECUTED = false
CANDIDATE_CLASSIFICATION_EXECUTED = false
GIT_MUTATION = none
```

Report exact corrected terminal-state totals and exact remaining environment-failure totals by authority and error class.

A remaining truthful environment failure is allowed.

A producer bug, placeholder evidence or schema drift is not.

======================================================================
11. REGENERATE HANDOFF MANIFEST
======================================================================

Replace `STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json`.

Include:

```text
artifact_set
generated_at_utc
source_registry_sha256
authorized_competitors
source_url_rows
terminal_counts
provider_calls
step08_executed
candidate_classification_executed
git_mutation
codex_rework_start_remote_head
codex_pre_handoff_remote_head
authority_drift
files[]
```

For every handoff file in `files[]`, include at least:

```text
filename
sha256
byte_size
row_count_or_jsonl_record_count
```

======================================================================
12. ZIP / HANDOFF
======================================================================

Produce exactly these corrected five files:

1. `STEP07_BROWSER_RECOVERY_URL_LEDGER.csv`
2. `STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl`
3. `STEP07_BROWSER_RECOVERY_COVERAGE.csv`
4. `STEP07_BROWSER_RECOVERY_QA.md`
5. `STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json`

Create one transport ZIP containing exactly those five corrected files.

Do NOT commit/push/PR.

Do NOT ask owner to sort repository paths.

Provide direct links to the five files + ZIP.

Owner will return the corrected package to Main Chat for QA.

======================================================================
13. FINAL REPORT
======================================================================

Return at minimum:

```text
CODEX_REWORK_START_REMOTE_HEAD
CODEX_PRE_HANDOFF_REMOTE_HEAD

SOURCE_URL_ROWS
CORRECTED_RECOVERED_INSPECTED
CORRECTED_REDIRECTED_IN_SCOPE
CORRECTED_TARGET_BLOCKED
CORRECTED_EXECUTION_ENVIRONMENT_FAILURES
T_GOTO_TYPEERROR_FINAL_ROWS
NOT_COLLECTED_ON_RECOVERED_INSPECTED
UNAUTHORIZED_SITEMAP_REFERENCES

URL_LEDGER_SCHEMA = PASS|FAIL
COVERAGE_SCHEMA = PASS|FAIL
PAGE_EVIDENCE_SCHEMA = PASS|FAIL
SHA_VERIFICATION = PASS|FAIL
JOIN_QA = PASS|FAIL

PROVIDER_CALLS = 0
STEP08_EXECUTED = false
CANDIDATE_CLASSIFICATION_EXECUTED = false
GIT_MUTATION = none
```

Do not declare PASS if any hard defect above remains.