# KW-002 / BLOOD & SAND — STEP07 BROWSER RECOVERY — MAIN CHAT RETURN QA

Date: 2026-09-17
Status: **FAIL / LIMITED CODEX REWORK REQUIRED**
Source under review: owner-chat-uploaded Codex recovery handoff (5 files + transport ZIP)
Remote branch at review start: `d8244b56b1f8a60424bb59423c4f8dd3cf34c6ef`

## 1. What passed

The recovery materially improved access evidence versus Step07 Attempt 1:

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

No provider calls were made; Step08 was not started; candidate classification was not performed; GitHub was not mutated by Codex.

The transport ZIP contains exactly the five expected filenames and its file bytes match the separately uploaded artifacts.

## 2. Hard defect A — recovery URL ledger schema does not match the released contract

Released minimum URL-ledger fields included:

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

Returned `STEP07_BROWSER_RECOVERY_URL_LEDGER.csv` instead uses:

```text
source_url_id
competitor_authority_id
canonical_site
source_url_raw
final_url
opened_read_state
terminal_state
title
h1
discovery_origin
discovery_source_url
known_upstream
redirect_or_error_state
notes
```

Material required fields are missing, including the explicit page-evidence join key, target HTTP status, robots decision, browser-rendered marker, exact capture timestamp and normalized error-class/detail split.

Therefore the returned URL ledger cannot pass the frozen recovery schema contract.

## 3. Hard defect B — recovery coverage artifact uses the wrong schema

Released coverage minimum fields were:

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

Returned `STEP07_BROWSER_RECOVERY_COVERAGE.csv` instead uses the old Attempt-1-style coverage schema:

```text
discovered_urls
eligible_urls
inspected_urls
excluded_urls
inaccessible_urls
redirected_terminal_urls
candidate_yield_urls
no_candidate_urls
unresolved_urls
candidate_identity_count
...
```

It has 32 authority rows but does not expose the required Attempt1→Recovery reconciliation fields. This is a hard contract failure.

## 4. Hard defect C — some RECOVERED_INSPECTED rows do not contain inspected page content

Independent parsing found 652 JSONL evidence records. All parse as valid JSON and all evidence IDs are unique.

However:

```text
CONTENT_SHA256 = NOT_COLLECTED : 30 evidence rows
FULL_VISIBLE_MAIN_TEXT = NOT_COLLECTED : 30 evidence rows
PAGE_TITLE = NOT_COLLECTED : 30 evidence rows
```

Of those 30:

```text
28 are linked to URL rows classified RECOVERED_INSPECTED
2 are linked to URL rows classified REDIRECTED_IN_SCOPE
```

The 28 `RECOVERED_INSPECTED` rows therefore contradict the mandatory evidence rule:

```text
RECOVERED_INSPECTED
→ actual readable page evidence
→ non-empty full_visible_main_text
→ valid SHA-256
```

Affected examples include Wildberries tag/product URLs, Livemaster URLs and Joom URLs.

A page that opened but whose content was not collected cannot remain `RECOVERED_INSPECTED`.

## 5. Hard defect D — evidence JSONL field names drifted from the released schema

Released names included:

```text
headings_h2_h6[]
navigation_labels[]
category_labels[]
product_or_service_names[]
faq_questions[]
glossary_terms[]
structured_metadata_visible_or_public[]
```

Returned JSONL instead uses combined/renamed fields such as:

```text
h2_h6
nav_category_labels
product_service_names
faq_glossary
structured_metadata
same_site_links
```

The content can be retained, but the file must be regenerated into the exact released machine-readable field contract before acceptance.

## 6. Hard defect E — 47 of 98 environment failures are an executor bug, not a terminal recovery result

The 98 explicit `EXECUTION_ENVIRONMENT_FAILURE` rows break down approximately as:

```text
47 = TypeError: t.goto is not a function
38 = normal browser navigation timeouts
8  = browser site-safety policy blocks
5  = other browser/CDP/evaluate/deadline/tool failures
```

`TypeError: t.goto is not a function` is a deterministic implementation defect in the recovery executor. Those 47 URLs must be retried after fixing the navigation primitive.

Timeout/deadline failures should receive one normal browser retry where permitted. Site-safety policy blocks must not be bypassed and may remain explicit environment failures.

## 7. Hard defect F — unauthorized sitemap contamination in QA

The returned QA states:

```text
SITEMAP_ACCESS_STATE = BLOCKED_BY_CLIENT
on https://okno-msk.ru/sitemap.xml
```

`okno-msk.ru` is not one of the 32 Step07 authorized competitors and does not occur in the returned URL ledger.

This is unrelated-domain contamination and cannot serve as Step07 sitemap evidence.

The corrected recovery must remove this claim and ensure any sitemap/robots evidence is tied only to an authorized competitor and its allowed scope.

## 8. What remains valid and should NOT be thrown away

Do not restart the whole recovery from zero.

Preserve and reuse, after schema normalization and validation:

- successfully captured browser page content with real SHA-256;
- legitimate redirect observations;
- explicit target anti-bot evidence;
- legitimate site-safety policy blocks;
- valid target-level browser observations;
- existing source URL identities and authorized competitor IDs.

The limited rework should focus on:

1. exact schema compliance;
2. fixing/retrying environment-executor failures;
3. removing false `RECOVERED_INSPECTED` states without content;
4. removing unauthorized sitemap contamination;
5. regenerating QA + manifest from the corrected artifacts.

## 9. Acceptance state

```text
STEP07_BROWSER_RECOVERY_ATTEMPT_1_RETURN = REJECTED
STEP07_BROWSER_RECOVERY_REWORK_REQUIRED = true
STEP07_BROWSER_RECOVERY_REMOTE_PUBLICATION = NOT_ALLOWED_YET
STEP07_SEMANTIC_REWORK_WORK_RELEASE = BLOCKED_PENDING_CORRECTED_BROWSER_RECOVERY
STEP08 = BLOCKED
```

Do not upload/accept this first recovery package as the canonical recovery result.

The rejected package remains owner-side evidence of the failed first recovery return; the repository stores this independent return QA and the bounded rework prompt.