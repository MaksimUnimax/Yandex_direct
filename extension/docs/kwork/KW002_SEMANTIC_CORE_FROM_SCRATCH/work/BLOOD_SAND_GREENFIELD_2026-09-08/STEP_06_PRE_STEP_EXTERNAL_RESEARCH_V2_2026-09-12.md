# KW-002 Blood & Sand — Step06 corrected pre-step external research V2

Date: 2026-09-12
Status: **FRESH RESEARCH COMPLETE / OWNER-FACING DISCLOSURE REQUIRED BEFORE EXECUTION / NO PROVIDER CALL**
Base HEAD before corrected preparation: `b33080d83272b9cd4f4b06cb42c35cce9fc94955`

## Exact Step06 questions researched

1. What current Yandex API operation returns ordinary organic web-search results?
2. What request fields, region, depth and result format are current?
3. What current quota/limits/pricing apply?
4. What evidence is required to identify current organic competitors for a new site with no ranking history?
5. How should direct business rivals be distinguished from sites that merely compete in organic results?
6. What current Bridge implementation can preserve for Step06 and what remains unproven about the installed runtime?

## External source-to-method trace

| source_id | source_title | publisher | source_class | url | checked_at | method_element_supported | exact_claim_supported | project_specific_application | claim_boundary |
|---|---|---|---|---|---|---|---|---|---|
| S06-S01 | Web Search API, REST: WebSearch.Search | Yandex AI Studio | OFFICIAL_PROVIDER | https://aistudio.yandex.ru/ru/docs/search-api/api-ref/WebSearch/search | 2026-09-12 | ordinary Search request/response contract | `POST /v2/web/search`; query/search/group fields; XML/HTML response format; `rawData` response field; XML groups 1..100 | Use ordinary `search`, not GenSearch; RU search; explicit region; page 0; flat groups | API schema does not decide SEO competitor-selection thresholds |
| S06-S02 | Текстовый поиск | Yandex AI Studio | OFFICIAL_PROVIDER | https://aistudio.yandex.ru/ru/docs/search-api/concepts/web-search | 2026-09-12 | result format/depth/defaults | XML contains search results without extra browser-SERP elements; max 250 results/query; XML `groupsOnPage` default 20 and allowed 1..100; sync result is Base64 `rawData` | Use XML and a bounded top-20 Step06 observation; treat 20 as cutoff by design | Provider maximum/default does not prove semantic completeness or mandate project depth |
| S06-S03 | Квоты и лимиты Yandex Search API | Yandex AI Studio | OFFICIAL_PROVIDER | https://aistudio.yandex.ru/ru/docs/search-api/concepts/limits | 2026-09-12 | request limits | sync 10 req/s, 10,000 req/h; max 250 results; max 400 chars; max 40 words | Planned Step06 volume is far below provider quota; still execute under project durability gates | Quota capacity is not permission or information-gain proof |
| S06-S04 | Правила тарификации для Yandex Search API | Yandex AI Studio | OFFICIAL_PROVIDER | https://aistudio.yandex.ru/ru/docs/search-api/pricing | 2026-09-12 | current cost | 488 RUB/1000 daytime sync; 366 RUB/1000 night sync; night window 00:00–07:59:59 UTC+3 | Cost each ordinary sync call as 0.488/0.366 RUB and record actual request count | Cost does not determine analytical truth |
| S06-S05 | Регионы поиска | Yandex AI Studio | OFFICIAL_PROVIDER | https://aistudio.yandex.ru/ru/docs/search-api/reference/regions | 2026-09-12 | Russia region ID | region `225` = Russia | Use region 225 because frozen job market/search geography is Russia | Region does not prove business relevance of a result |
| S06-S06 | Search results don't match the query | Yandex Search Help | OFFICIAL_YANDEX | https://yandex.com/support/search/en/troubleshooting/unrelevant-results | 2026-09-12 | mixed result types / multiple interpretations | Yandex search results can intentionally include different interpretations and result types; region can affect ranking | Preserve and type marketplaces, sellers, publishers, directories, UGC/media separately rather than calling all direct rivals | Browser help describes Yandex Search generally, not the exact Search API payload contract |
| S06-S07 | How can I find new competitor websites using the Traffic Share reports? | Ahrefs Help Center | INDUSTRY_PRACTICE | https://help.ahrefs.com/en/articles/2073915-how-can-i-find-new-competitor-websites-using-the-traffic-share-reports | 2026-09-12 | competitor discovery for arbitrary keyword sets | A list of keywords + target country can be used to identify domains/pages competing for those terms | Appropriate for a greenfield site with no own ranking history: start from representative target-demand queries and observe recurring domains | Ahrefs methodology/data is not Yandex evidence and does not set KW002 thresholds |
| S06-S08 | Discover your Online Competitors Using Semrush | Semrush Knowledge Base | INDUSTRY_PRACTICE | https://www.semrush.com/kb/844-discover-competitors | 2026-09-12 | organic competitor definition by shared rankings | Organic competitors are based on shared organic keyword rankings; target-keyword competitor discovery is a separate useful mode | Supports `BUSINESS RIVAL != SEARCH COMPETITOR` and recurrence/overlap as evidence | Semrush uses its own database and primarily Google-oriented data; it corroborates method only |

## Project/internal source-to-method trace

| source_id | source | source_class | exact support | Step06 application | boundary |
|---|---|---|---|---|---|
| S06-P01 | `LEVEL2/STEP_RULES_INDEX.md` Step06 | OWNER_SCOPE_RULE / INTERNAL_PROCESS_AUTHORITY | Step06 discovers current Yandex organic competitors from representative retained directions; `BUSINESS RIVAL != SEARCH COMPETITOR` | Defines Step06 purpose/output/PASS | Internal rule is process authority, not independent proof |
| S06-P02 | `LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md` | OWNER_SCOPE_RULE | Search evidence may preserve `raw or durable normalized result reference` with query/region/time/mode/provenance | A complete durable normalized Search envelope is allowed if required rows/fields are preserved | Does not allow lossy summaries or dropped result rows |
| S06-P03 | `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md` F03 | OWNER_SCOPE_RULE | provider success != durable feed-forward completion | Persist each substantive Search result and remote-readback before the next provider action | HTTP 200/chat visibility alone never closes evidence |
| S06-P04 | `LEVEL1/SERP_COVERAGE_MODE_DECISION_2026-09-10.md` | OWNER_SCOPE_RULE | FULL coverage applies to future final Search-stage selected set | Step06 representative competitor discovery must not be mislabeled as Step12 full Search coverage | Step06 selective discovery cannot be reused as proof that Step12 full coverage is complete |
| S06-P05 | `extension/src/shared/search_protocol.js` + `search_xml.js` + `service_worker.js` | PROJECT_TEST_VALIDATED / REPOSITORY_IMPLEMENTATION | repo Search path parses provider `rawData` and emits all XML `<doc>` rows with rank/url/domain/title/snippet/modtime into the full JSON envelope | Durable normalized result is structurally sufficient for Step06 if actual installed runtime matches/accepts this contract and returned row list is persisted exactly | Original Base64/XML is not preserved by this repo path; fields outside the Step06 normalized projection are not retained |
| S06-P06 | `extension/src/shared/product.js` | PROJECT_TEST_VALIDATED / REPOSITORY_IMPLEMENTATION | branch product version = `0.1.2` | Must be reconciled against installed runtime before Search release | Owner's preceding provider result reported runtime `0.1.4`; current runtime source identity is not proven |

## Method conclusions

### A. Competitor source

```text
CURRENT YANDEX SERP EVIDENCE
→ DOMAIN/URL RECURRENCE ACROSS REPRESENTATIVE DEMAND DIRECTIONS
→ RESULT-TYPE / RELEVANCE REVIEW
→ SEARCH COMPETITOR REGISTRY
```

No domain is included because the client named it. The client supplied no competitor list.

### B. New-site discovery route

The site has no ranking history. Therefore Step06 starts from representative retained demand directions rather than “keywords shared with our existing domain”. This is compatible with the Ahrefs arbitrary-keyword-list competitor-discovery pattern and the KW002 greenfield scope.

### C. Planned Search mode

```text
method = search
searchType = SEARCH_TYPE_RU
region = 225
page = 0
groupsOnPage = 20
groupMode = GROUP_MODE_FLAT
docsInGroup = 1
sortMode = SORT_MODE_BY_RELEVANCE
familyMode = FAMILY_MODE_MODERATE
fixTypoMode = FIX_TYPO_MODE_OFF
responseFormat = FORMAT_XML
GenSearch = forbidden for Step06
```

`fixTypoMode=OFF` is a project-specific precision control: the probe identity should not be silently rewritten by provider autocorrection. It is not an external SEO standard.

### D. Depth

`groupsOnPage=20` is the current XML default and a bounded Step06 discovery depth. The project uses it as an `ANALYST_HEURISTIC / PROJECT-SPECIFIC` choice for top-result competitor recurrence.

```text
RETURNED_ROWS = 20
=> TOP20_CUTOFF_BY_DESIGN
!= SERP_COMPLETE
```

No external source establishes “20 = enough competitors” universally.

### E. Competitor recurrence

External sources support shared-query/ranking overlap as competitor evidence but do not supply a universal threshold for this job.

V2 therefore uses recurrence tiers as **candidate evidence**, not automatic truth:

```text
SINGLE_OBSERVATION
RECURRING_WITHIN_DIRECTION (2+ selected queries in one direction)
CROSS_DIRECTION_RECURRING (2+ selected coverage directions)
```

A domain is selected for the Step06 registry only after relevance/result-type review; a numeric recurrence tier alone cannot force selection.

### F. Persistence

For Step06, current universal rules allow full durable normalized Search results. Required persisted fields are:

```text
query_id
query_text
request_id
received_at / snapshot identity
search_type
region
page
groups_requested
rank
url
domain
title
snippet where available
modtime where available
result_count
provider/status/provenance
```

Every returned result row must remain recoverable. A summary/top-domain list alone is insufficient.

### G. Current unresolved execution blocker

```text
INSTALLED_RUNTIME_VERSION_OBSERVED = 0.1.4
CURRENT_REPOSITORY_PRODUCT_VERSION = 0.1.2
CURRENT_INSTALLED_SEARCH_SCHEMA/SOURCE_IDENTITY = UNPROVEN
```

Before any paid Search call, perform a non-provider runtime/schema reconciliation/handshake or sync the authoritative installed runtime source. This is the remaining Bridge release blocker found by V2.

## Provider calls in this research pass

```text
ORDINARY_SEARCH = 0
GENSEARCH = 0
WORDSTAT = 0
AI_SEARCH = 0
```
