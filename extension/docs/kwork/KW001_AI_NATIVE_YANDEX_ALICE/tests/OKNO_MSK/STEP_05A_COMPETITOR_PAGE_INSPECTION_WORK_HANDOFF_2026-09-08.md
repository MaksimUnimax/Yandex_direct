# KW-001 / OKNO_MSK — Step 5A competitor-page inspection Work handoff

Status: **READY FOR WORK EXECUTION**

## 1. Purpose

Continue the already-started first project validation of Level-1 Step 5A.

This execution covers only the next evidence-producing subphase:

```text
STEP 5A.2 — INSPECT EVIDENCE-BEARING COMPETITOR PAGES
→ STEP 5A.3 — DERIVE CANDIDATE COMPETITOR SEEDS WITH PAGE-LEVEL LINEAGE
```

It must stop before any new Wordstat or Yandex Search acquisition.

Canonical Level-1 authority:

- `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md`
- `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/STEP_RULES_INDEX.md`

Prior completed first-execution authority:

- `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_05A_FIRST_EXECUTION_2026-09-08/STEP_05A_FIRST_EXECUTION_REPORT.md`
- `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_05A_FIRST_EXECUTION_2026-09-08/STEP_05A_FIRST_EXECUTION_QA.json`
- `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_05A_FIRST_EXECUTION_2026-09-08/STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv`

Current method state remains:

```text
PROJECT_TEST_VALIDATED = false
OWNER_REVIEW = pending
```

Do not promote Step 5A in Level-1 during this task.

## 2. Repository / starting state

Repository:

`MaksimUnimax/Yandex_direct`

Branch:

`roadmap/kwork-productization-2026-08-28`

Expected starting HEAD:

`3deac1eb29c5f82c6c271d200f0c4276862ed64c`

Before writing, re-read live remote HEAD. If legitimate later commits exist, preserve them and work from the actual current branch state.

## 3. Role boundary

This is a Work bulk task because it requires opening and comparing dozens of competitor pages and reconciling candidate topics against a large existing semantic authority.

Work may use its public web/browser capability to open the exact URLs authorized below.

Work does **not** control Yandex Bridge.

Main ChatGPT controls any later Wordstat / Yandex Search provider acquisition.

## 4. Hard acquisition boundary

This execution must make **zero new governed Yandex provider calls**:

```text
NEW_YANDEX_SEARCH_CALLS = 0
NEW_WORDSTAT_CALLS = 0
NEW_ALICE_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_WEBMASTER_CALLS = 0
NEW_METRIKA_CALLS = 0
NEW_DIRECT_CALLS = 0
NEW_PAID_PROVIDER_COST_RUB = 0
```

Allowed:

- direct public opening of the exact competitor URLs preserved from Step 9;
- normal HTTP/browser access needed to inspect those public pages.

Not allowed:

- Yandex Search to rediscover pages;
- search-engine discovery of extra competitor URLs;
- reverse-domain SEO providers;
- crawling whole competitor sites;
- Wordstat expansion in this task.

## 5. Exact inspection universe

Authority:

`STEP_05A_FIRST_EXECUTION_2026-09-08/STEP_05A_COMPETITOR_CANDIDATE_SELECTION.tsv`

Only rows with:

`selection_state = SELECTED_FOR_NEXT_STEP5A_PAGE_INSPECTION`

are in scope.

Selected domains = 9:

1. `mosokna.ru`
2. `i-okna.ru`
3. `msk.okna-servise.com`
4. `okna-moskva.ru`
5. `oknafactoria.ru`
6. `okna-germany.ru`
7. `fabrikaokon.ru`
8. `aluminarium.ru`
9. `elit-balkon.ru`

The exact preserved ranking URLs are stored in column:

`exact_ranking_urls_to_inspect_next`

Expected authorized URL targets from the current selection = **44**.

Do not expand beyond those exact targets merely because a page links elsewhere.

If a URL redirects canonically within the same public page, record both requested URL and final URL. Do not follow unrelated internal navigation as a new evidence target.

## 6. Step 5A.2 — required page inspection

For each authorized URL, persist one page-evidence row even if access fails.

Required fields where observable:

```text
inspection_id
competitor_domain
requested_url
final_url
source_step09_query_index
source_step09_query_text
source_step09_rank
http_or_browser_access_state
observation_date
page_type
page_title
h1
material_h2_h3_topics
material_commercial_axes
material_product_service_axes
material_use_case_axes
material_problem_solution_axes
price_or_calculator_presence
portfolio_or_examples_presence
installation_process_presence
faq_presence
trust_or_proof_elements_presence
relevant_internal_navigation_labels
page_evidence_notes
claim_boundary
```

Important:

- Record only what the page itself supports.
- Do not infer full-site architecture from one page.
- Do not infer exact ranking keywords from page text.
- Do not infer traffic, leads, revenue, conversion or market share.
- Do not treat marketing copy as proof that the competitor actually provides every claimed service unless the page clearly presents it as the business offer.
- If the page is inaccessible, blocked, removed or materially redirected, preserve that state and do not substitute the old SERP title as current page content.

## 7. Page-type classification

Use a bounded page-type vocabulary where possible, e.g.:

```text
COMMERCIAL_CATEGORY
COMMERCIAL_SERVICE
COMMERCIAL_PRODUCT
COMMERCIAL_LANDING
PRICE_FINANCE
ARTICLE_GUIDE
COMPARISON_SELECTION
PORTFOLIO_GALLERY
HOME_OR_HUB
MIXED_COMMERCIAL_INFORMATIONAL
OTHER
UNKNOWN
```

Do not force a page into a type when evidence is insufficient.

## 8. Step 5A.3 — derive candidate competitor seeds

A competitor-derived seed must have explicit page-level lineage:

```text
candidate seed
← exact page element/topic
← exact competitor URL
← exact preserved Step 9 query/rank that exposed that URL
```

Canonical boundary:

```text
COMPETITOR PAGE TOPIC
!= ACCEPTED KEYWORD
!= EXACT QUERY RANKING CLAIM
!= FULL COMPETITOR KEYWORD UNIVERSE
```

Do not create candidate seeds from domain names or URL slugs alone.

Useful candidate sources may include:

- Title/H1/H2/H3 topic distinctions;
- explicit product/service variants;
- explicit use-case variants;
- explicit problem/solution directions;
- explicit comparison/selection dimensions;
- explicit pricing/finance/service-process directions;
- explicit balcony/house/veranda/terrace/material/profile/system distinctions;
- other material semantic directions actually present on the page.

A candidate seed should be a concise normalized topic/query direction suitable for later Wordstat expansion, not copied competitor marketing prose.

## 9. Compare candidates against existing OKNO_MSK semantic authority

Before asking Main ChatGPT to spend Wordstat calls, compare every candidate seed against the existing semantic model.

Use current canonical authorities, primarily:

- `RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv`
- `RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv`
- existing Wordstat acquisition layers where needed for provenance/coverage checks.

Classify each page-derived candidate as one of:

```text
ALREADY_COVERED_EXACT_OR_CLOSE
POTENTIALLY_NEW_WORDSTAT_SEED
OFF_SCOPE_BUSINESS
INSUFFICIENT_PAGE_EVIDENCE
DUPLICATE_OF_ANOTHER_COMPETITOR_SEED
HOLD_REVIEW
```

Do not claim that a candidate is genuinely new merely because the exact wording is absent. Compare semantic direction/task, not string equality only.

## 10. Required candidate-seed register

Materialize a durable register with at least:

```text
seed_id
normalized_candidate_seed
semantic_axis
competitor_domain
source_requested_url
source_final_url
source_step09_query_index
source_step09_query_text
source_step09_rank
source_page_element_type
source_page_element_text
source_page_evidence_summary
existing_semantic_match_state
existing_semantic_match_examples
business_scope_state
seed_decision
wordstat_required
wordstat_priority
rationale
claim_boundary
```

For `POTENTIALLY_NEW_WORDSTAT_SEED`, `wordstat_required = true`.

For all other states, explain why a new Wordstat call is not yet justified.

## 11. Dedupe and information-gain gate

Many competitors may expose the same topic.

Deduplicate candidate seeds by semantic meaning while preserving all source URLs/domains that independently support the direction.

For each surviving `POTENTIALLY_NEW_WORDSTAT_SEED`, record:

- how many selected competitors/pages exposed it;
- why it is not already covered in the current semantic model;
- why testing it through Wordstat could add information.

Do not generate dozens of near-synonym seeds when one bounded seed can test the same missing direction.

## 12. Wordstat requirement package — output only, no calls

At the end, create an exact package for Main ChatGPT / Yandex Bridge.

Required fields:

```text
wordstat_seed_order
normalized_candidate_seed
semantic_axis
supporting_competitor_count
supporting_page_count
supporting_source_ids
why_existing_core_is_insufficient
business_scope_state
recommended_wordstat_region
recommended_device_scope
provider_call_authorization_state
```

Set:

```text
provider_call_authorization_state = RETURN_TO_MAIN_CHATGPT_FOR_BRIDGE_EXECUTION
```

No Wordstat call in Work.

If no evidence-backed new seed survives, explicitly materialize an empty requirement package and state that competitor inspection found no material semantic gap requiring Wordstat.

## 13. Required artifacts

Create under:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_05A_FIRST_EXECUTION_2026-09-08/`

At minimum:

```text
CHECKPOINT_01_COMPETITOR_PAGE_INSPECTION_BASELINE.md
STEP_05A_COMPETITOR_PAGE_EVIDENCE.tsv
STEP_05A_DERIVED_SEED_CANDIDATES.tsv
STEP_05A_WORDSTAT_REQUIREMENT_PACKAGE.tsv
STEP_05A_PAGE_INSPECTION_QA.json
STEP_05A_PAGE_INSPECTION_REPORT.md
STEP_05A_PAGE_INSPECTION_EXECUTION_LOG.md
```

Scripts/helpers used for deterministic reconciliation should also be persisted if material to reproducibility.

Do not overwrite the completed first-execution artifacts from the prior phase unless a genuine defect is found. If a defect is found, preserve the correction explicitly rather than silently replacing history.

## 14. Required QA

At minimum verify:

```text
SELECTED_DOMAINS_EXPECTED = 9
AUTHORIZED_URL_TARGETS_EXPECTED = 44
AUTHORIZED_URL_TARGETS_ACCOUNTED = 44
OUT_OF_SCOPE_URLS_OPENED_AS_EVIDENCE_TARGETS = 0
PAGE_EVIDENCE_ROWS = 44
PAGE_ACCESS_FAILURES_EXPLICIT = true
SEEDS_WITHOUT_PAGE_LINEAGE = 0
SEEDS_FROM_URL_SLUG_ONLY = 0
SEEDS_FROM_DOMAIN_NAME_ONLY = 0
SEMANTIC_CANDIDATES_COMPARED_TO_EXISTING_CORE = all
POTENTIALLY_NEW_WORDSTAT_SEEDS_DEDUPED = true
WORDSTAT_REQUIREMENT_ROWS = surviving new seeds only
NEW_YANDEX_PROVIDER_CALLS = 0
CLIENT_RELEASE_MODIFIED = false
DOCUMENTS_01_02_03_MODIFIED = false
SEMANTIC_CORE_04_MODIFIED = false
LEVEL1_METHOD_PROMOTED = false
```

If any authorized page cannot be inspected, QA may still pass only if the failure is explicit and no content/seed is invented for it.

## 15. Scope protection

Do not modify:

- corrected client release;
- Documents 01–03;
- standalone semantic-core XLSX;
- historical Step 0–20 canonical outputs;
- Level-1 Step 5A status/promotion state.

This remains an isolated methodology-validation execution.

## 16. Persistence discipline

After each material block:

```text
WORK
→ SAVE
→ COMMIT
→ REMOTE GITHUB READBACK
→ CONTINUE
```

At minimum persist/read back:

1. baseline + exact 44-URL inventory;
2. page evidence first material tranche;
3. complete 44-URL page evidence;
4. candidate-seed reconciliation against existing core;
5. Wordstat requirement package + report + QA.

Do not stop after creating `CHECKPOINT_01` or after inspecting only a sample of competitors.

## 17. Completion boundary

This Work task is complete only when:

- all 44 authorized URL targets are accounted for;
- all accessible pages have page-level evidence;
- inaccessible pages are explicitly recorded;
- candidate semantic directions have exact page lineage;
- all candidates are reconciled against the existing core;
- genuinely new candidates are deduplicated into an exact Wordstat requirement package;
- no governed Yandex provider calls were made;
- artifacts are committed;
- remote GitHub readback passes.

Then return control to Main ChatGPT for the Bridge-controlled Wordstat subphase.

## 18. Final Work response

Return an execution summary containing:

- starting HEAD;
- final HEAD;
- commit SHAs;
- selected domains accounted `9/9`;
- authorized URLs accounted `44/44`;
- accessible / inaccessible / redirected counts;
- page-type counts;
- raw page-derived candidate count;
- deduplicated candidate count;
- `ALREADY_COVERED_EXACT_OR_CLOSE` count;
- `POTENTIALLY_NEW_WORDSTAT_SEED` count;
- off-scope / insufficient / hold counts;
- exact surviving Wordstat seeds in priority order;
- confirmation new Yandex provider calls = `0`;
- confirmation corrected client artifacts modified = `false`;
- remote GitHub readback = PASS/FAIL.
