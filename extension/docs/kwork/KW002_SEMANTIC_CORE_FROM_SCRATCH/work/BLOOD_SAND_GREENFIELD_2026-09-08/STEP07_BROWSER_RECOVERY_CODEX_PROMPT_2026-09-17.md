# KW-002 / BLOOD & SAND — STEP07 BROWSER RECOVERY — CODEX EXECUTION PROMPT

Status: **CURRENT / EXECUTION-ONLY / EVIDENCE ACQUISITION RECOVERY**

CONTINUE THE EXISTING KW-002 BLOOD & SAND GREENFIELD SEMANTIC-CORE REHEARSAL.

THIS IS NOT A NEW PROJECT.
THIS IS NOT STEP08.
THIS IS NOT SEMANTIC RECLASSIFICATION.
THIS IS A BROWSER-BASED RECOVERY PASS FOR MISSING STEP07 COMPETITOR PAGE EVIDENCE AFTER ATTEMPT 1 FAILED TO INSPECT MOST AUTHORIZED COMPETITOR SURFACES.

Your role in this pass is **browser evidence acquisition only**.

Do NOT redo Main Chat governance/research/release work.
Do NOT make Wordstat, Yandex Search, AI Search or GenSearch provider calls.
Do NOT classify final Step07 candidates.
Do NOT make final intent/cluster/page decisions.
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

Fetch the current remote branch and record `CODEX_START_REMOTE_HEAD`.

Read only the concrete execution inputs needed for this recovery:

```text
STEP07_MAIN_CHAT_RETURN_QA_2026-09-17.md
STEP07_OPERA_BROWSER_CONTROL_PROBE_2026-09-17.md
STEP07_BROWSER_RECOVERY_CODEX_PROMPT_2026-09-17.md
STEP_07_AUTHORIZED_COMPETITOR_UNIVERSE.csv
STEP_07_PRE_HANDOFF_MANIFEST.md
STEP07_COMPETITOR_COVERAGE_LEDGER.csv
STEP07_SOURCE_URL_LEDGER.csv
STEP07_EXECUTION_QA.md
KW002_STEP06_SEARCH_COMPETITOR_REGISTRY_HARDENED.csv
```

Verify:

```text
AUTHORIZED_COMPETITORS = 32
AUTHORITY_IDS = S07A001..S07A032
SOURCE_REGISTRY_SHA256 = b15e601db56d8f3c23d7a8c4a2193fc14000dc9773229d693c200756240efcdb
```

If competitor membership/scope authority materially changed, stop and report `AUTHORITY_DRIFT`.

Otherwise execute immediately.

======================================================================
2. WHY THIS RECOVERY EXISTS
======================================================================

Step07 Attempt 1 produced:

```text
DISCOVERED_URLS = 1976
INSPECTED_URLS = 24
EXCLUDED_URLS = 1201
INACCESSIBLE_URLS = 751
```

Only `S07A010 / kartaslov.ru` yielded inspected candidate evidence.

Many failed rows were not reliable target-site access decisions. They contain Work-runtime/proxy failures such as:

```text
ClientHttpProxyError:403
url='http://127.0.0.1:...'
```

Main Chat independently ran a normal-browser control probe through the owner's Opera Browser Connector and proved that multiple zero-inspected competitors are reachable and readable in a browser. Read the exact evidence in:

`STEP07_OPERA_BROWSER_CONTROL_PROBE_2026-09-17.md`

Browser-accessible/readable controls included at minimum:

```text
ru.wikipedia.org
slavyanskieoberegi.ru
sibpodkova.ru
artvaza.ru
happywitch.ru
simvolroda.ru
oum.ru
```

The probe also observed genuine browser-level problems for some targets/snapshots, including Wildberries VPN blocking and a privacy/certificate error on runarium.ru. Do not generalize either direction; retry and classify each target truthfully.

Therefore this pass must distinguish:

```text
TARGET-SITE ACCESS RESULT
!=
CODEX / LOCAL / PROXY / TOOL FAILURE
```

A local browser/tool failure is NOT competitor semantic closure.

======================================================================
3. AUTHORIZED UNIVERSE AND SCOPE
======================================================================

Use exactly the 32 rows in:

`STEP_07_AUTHORIZED_COMPETITOR_UNIVERSE.csv`

Do not admit new competitors.
Do not inherit arbitrary sibling/subdomains.
Do not use prior sealed Blood & Sand competitor research.

Obey each row's `scope_policy`:

### EVIDENCE_ANCHORED_RELEVANT_SUBTREE

For broad marketplaces/general information sites:

- start from all Step06-observed URLs and current failed-attempt URLs;
- use browser-visible navigation/breadcrumbs/category links inside the same relevant thematic subtree;
- use legitimate public sitemap/pagination where available;
- do not crawl the whole general-purpose host.

### THEME_SCOPED_PUBLIC_TAXONOMY

For specialized thematic sites:

- enumerate the complete public taxonomy relevant to amulets/charms/talismans/runes/symbols and the frozen business theme;
- include category, subcategory, product, landing, guide/article, FAQ/help and glossary surfaces when relevant;
- exclude unrelated branches explicitly.

Important control from the Opera probe:

```text
BROWSER ACCESSIBLE
!=
WHOLE SITE RELEVANT
```

Broad/possibly off-theme domains such as `sibpodkova.ru`, `artvaza.ru` and `oum.ru` must remain bounded by their Step06 evidence and exact Step07 scope. Do not ingest unrelated site-wide taxonomy merely because the domain is reachable.

======================================================================
4. BROWSER-FIRST ACCESS ROUTE
======================================================================

Use your real browser/browser-automation capability as the primary acquisition route.

Do NOT rely on the same raw HTTP/proxy path that produced local `127.0.0.1` proxy failures in Attempt 1.

For each URL, navigate as a normal public browser user.

Allowed:

- ordinary public page navigation;
- following visible in-scope links;
- public breadcrumbs/categories;
- public pagination;
- public sitemap/robots documents;
- browser-rendered JavaScript content;
- normal redirects.

Forbidden:

- login/authentication to access private content;
- CAPTCHA bypass;
- anti-bot bypass;
- paywall bypass;
- robots bypass;
- hidden/private APIs;
- evasion/fingerprinting tricks;
- brute-force URL generation;
- external search-demand providers.

If the target itself presents CAPTCHA/login/block/robots restriction, record it truthfully and stop that path.

If the Codex browser/tool itself errors before a meaningful target response, record `EXECUTION_ENVIRONMENT_FAILURE`, not target inaccessibility.

======================================================================
5. PRIORITIZATION — RECOVER THE MISSING EVIDENCE
======================================================================

Start with every authorized competitor that had `inspected_urls = 0` in Attempt 1.

Then retry all Attempt-1 URLs currently classified as:

```text
INACCESSIBLE_TIMEOUT_OR_NETWORK
INACCESSIBLE_ROBOTS where the prior evidence was only an unreachable/redirect/error robots fetch rather than an actual disallow decision
other access failures caused by local/proxy/runtime error
```

Do not waste time re-collecting the 24 already inspected `kartaslov.ru` pages unless needed for a deterministic link/frontier relation.

However, if a newly reachable in-scope page legitimately discovers a new in-scope URL on an authorized host, add it to the recovery frontier and process it.

No arbitrary top-N.

======================================================================
6. URL RECOVERY TERMINAL STATES
======================================================================

Every recovery URL must end in one exact state:

```text
RECOVERED_INSPECTED
TARGET_ROBOTS_DISALLOWED
TARGET_CAPTCHA_OR_ANTI_BOT
TARGET_LOGIN_REQUIRED
TARGET_HTTP_ERROR
TARGET_NOT_FOUND
TARGET_TIMEOUT_OR_NETWORK
REDIRECTED_IN_SCOPE
REDIRECTED_OUT_OF_SCOPE
EXCLUDED_OUT_OF_SCOPE
EXCLUDED_DUPLICATE
EXCLUDED_NON_HTML_OR_UNSUPPORTED
UNRESOLVED_DYNAMIC_CONTENT
EXECUTION_ENVIRONMENT_FAILURE
ERROR
```

Key rule:

```text
EXECUTION_ENVIRONMENT_FAILURE
!= TARGET_TIMEOUT_OR_NETWORK
!= TARGET_ROBOTS_DISALLOWED
```

For a target-level status, preserve evidence sufficient to show the target actually produced that result.

For environment/tool failure, preserve the exact error and do not claim semantic closure.

======================================================================
7. PAGE EVIDENCE CAPTURE
======================================================================

For each successfully inspected public page create one JSONL evidence record containing at minimum:

```text
evidence_id
competitor_authority_id
canonical_site
scope_policy
source_url_raw
final_url
computed_canonical_url
declared_canonical_url if visible
redirect_chain if any
discovery_source
discovery_parent_url
page_type
page_title
h1
headings_h2_h6[]
breadcrumbs[]
navigation_labels[]
category_labels[]
product_or_service_names[]
faq_questions[]
glossary_terms[]
structured_metadata_visible_or_public[]
body_text_blocks[]
full_visible_main_text
content_sha256
captured_at_utc
browser_route = true
notes
```

`full_visible_main_text` must preserve the complete visible main content relevant to later semantic extraction, not merely a summary.

Do not include user-private/account content.
Do not expand review/comment text into business truth.

Page evidence should be structurally extracted from the rendered page/DOM/accessibility tree where possible.

======================================================================
8. THIS PASS DOES NOT CREATE STEP07 CANDIDATES
======================================================================

Do not write or replace:

```text
COMPETITOR_GAP_CANDIDATES.csv
STEP07_CANDIDATE_PROVENANCE_LEDGER.csv
```

Do not classify phrases as:

```text
NEW_CANDIDATE
ALREADY_PRESENT
POSSIBLE_VARIANT
OUT_OF_SCOPE
AMBIGUOUS
```

That is the next Work rework unit.

Your job is to provide trustworthy browser evidence and coverage only.

======================================================================
9. REQUIRED OUTPUTS
======================================================================

Create exactly these five recovery artifacts in the job root:

1. `STEP07_BROWSER_RECOVERY_URL_LEDGER.csv`
2. `STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl`
3. `STEP07_BROWSER_RECOVERY_COVERAGE.csv`
4. `STEP07_BROWSER_RECOVERY_QA.md`
5. `STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json`

### URL ledger minimum fields

```text
recovery_url_id
competitor_authority_id
canonical_site
scope_policy
source_url_raw
attempt1_url_id if applicable
computed_canonical_url
final_url
discovery_source
discovery_parent_url
access_route
terminal_status
target_http_status if available
robots_decision
browser_rendered
page_evidence_id if inspected
error_class
error_detail
captured_at_utc
notes
```

### Coverage minimum fields

One row per all 32 authorized competitors:

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

======================================================================
10. QA
======================================================================

Programmatically prove at minimum:

```text
AUTHORIZED_COMPETITOR_ROWS = 32
ONLY_AUTHORIZED_COMPETITORS_USED = true
ALL_32_COMPETITORS_PRESENT_IN_RECOVERY_COVERAGE = true
ATTEMPT1_ZERO_INSPECTED_COMPETITORS_RETRIED = true
ALL_RETRYABLE_ATTEMPT1_RUNTIME_NETWORK_FAILURES_ACCOUNTED = true
NO_ARBITRARY_TOP_N = true
EVERY_RECOVERY_URL_HAS_ONE_TERMINAL_STATUS = true
EVERY_RECOVERED_INSPECTED_URL_HAS_PAGE_EVIDENCE = true
EVERY_PAGE_EVIDENCE_HAS_RAW_URL + FINAL_URL + AUTHORITY + TIMESTAMP = true
FULL_VISIBLE_MAIN_TEXT_PRESENT_FOR_INSPECTED_PAGES = true
CONTENT_SHA256_PRESENT = true
TARGET_BLOCKS_DISTINGUISHED_FROM_ENVIRONMENT_FAILURES = true
CAPTCHA_BYPASS = false
ROBOTS_BYPASS = false
LOGIN_BYPASS = false
PROVIDER_CALLS = 0
STEP08_STARTED = false
STEP07_CANDIDATE_CLASSIFICATION_PERFORMED = false
```

Report exact totals for all terminal states.

A truthful partial recovery is allowed if some target pages remain legitimately blocked, but environment/tool failures must remain explicit and cannot be relabelled as completed competitor coverage.

======================================================================
11. HANDOFF
======================================================================

Do not commit/push/PR.

Provide direct downloadable links for all five files and one transport-only ZIP containing exactly those five files.

Use one staging upload target:

```text
repository = MaksimUnimax/Yandex_direct
branch = roadmap/kwork-productization-2026-08-28
directory = extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08
upload URL = https://github.com/MaksimUnimax/Yandex_direct/upload/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08
```

All five files are `NEW` for this recovery pass unless current remote already contains a newer canonical version.

ZIP is transport-only; do not commit the ZIP.

Owner action:

```text
download ZIP
→ extract
→ upload all five files together to the one staging link
→ commit
→ reply "готово"
```

======================================================================
12. FINAL REPORT
======================================================================

Return:

```text
CODEX_START_REMOTE_HEAD
CODEX_PRE_HANDOFF_REMOTE_HEAD
AUTHORIZED_COMPETITORS = 32
ATTEMPT1_ZERO_INSPECTED_COMPETITORS_RETRIED
RECOVERY_URLS_ATTEMPTED
RECOVERY_INSPECTED_URLS
RECOVERY_TARGET_BLOCKED_URLS
RECOVERY_ENVIRONMENT_FAILURE_URLS
NEW_IN_SCOPE_URLS_DISCOVERED
PAGE_EVIDENCE_ROWS
REMAINING_UNRESOLVED_OR_ENVIRONMENT_FAILURE_URLS
```

Also provide per-competitor recovery totals and exact QA results.

Explicitly confirm:

```text
NEW_WORDSTAT_CALLS = 0
NEW_YANDEX_SEARCH_CALLS = 0
NEW_AI_SEARCH_OR_GENSEARCH_CALLS = 0
STEP08_STARTED = false
STEP07_CANDIDATE_CLASSIFICATION_PERFORMED = false
CODEX_GITHUB_COMMIT_PUSH_PR = false
OWNER_UPLOAD_COMPLETE = false
REMOTE_READBACK_PASS = false
MAIN_CHAT_ACCEPTANCE = PENDING
```

Do not stop after testing a few sites. Process the complete bounded recovery universe.
