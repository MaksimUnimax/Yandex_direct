# KW-002 Blood & Sand — Step05 W10 pre-acquisition external research V2

Date: 2026-09-12
Status: **CORRECTED CURRENT PRE-STEP SOURCE TRACE / OWNER-FACING DISCLOSURE REQUIRED BEFORE WORK EXECUTION**

Repository: `MaksimUnimax/Yandex_direct`
Branch: `roadmap/kwork-productization-2026-08-28`
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Handoff: `KW002-BS-W10-V2`

## 1. Exact Step05 questions researched

1. What Wordstat GetTop evidence represents and its current time window.
2. Which operators can isolate morphology/word order and what they do not prove.
3. Current Wordstat quotas and relevant limits.
4. Current GetTop price.
5. Whether Yandex itself recommends expanding to non-obvious query formulations.
6. How current industry keyword-research practice treats relevance/prioritization after expansion.
7. Which part of the execution contract comes from official provider documentation versus the current Yandex Marketing Bridge code.
8. How to prevent a local Step04 coverage hypothesis from becoming a duplicate provider request.

## 2. External source-to-method trace

| source_id | source_title | publisher | source_class | url | checked_at | method_element_supported | exact_claim_supported | project_specific_application | claim_boundary |
|---|---|---|---|---|---|---|---|---|---|
| S05V2-01 | WordstatService | Yandex Cloud | OFFICIAL_PROVIDER_API | https://yandex.cloud/en/docs/search-api/api-ref/grpc/Wordstat/ | 2026-09-12 | provider semantics | GetTop returns last-30-days popular queries containing the keyword and similar queries; other Wordstat methods are separately defined | Step05 uses GetTop only as targeted current-demand/related-query evidence where a real vocabulary gap survives | does not prove business relevance, inventory, final intent, page ownership or the local Bridge envelope |
| S05V2-02 | Operators | Yandex Wordstat | OFFICIAL_PROVIDER_DOCS | https://yandex.ru/support2/wordstat/ru/content/operators | 2026-09-12 | operator semantics | `!` fixes a word form; quotes fix word count; `[]` fixes word order; operators can be combined and are supported for Top queries | operators may isolate a specific unresolved morphology/referent question | an operator match is not semantic truth and does not prove client facts |
| S05V2-03 | Quotas and limits | Yandex Cloud | OFFICIAL_PROVIDER_LIMITS | https://yandex.cloud/en/docs/overview/concepts/quotas-limits | 2026-09-12 | request safety / limits | Wordstat statistics quota is 10 requests/sec and 100 requests/hour; maximum associations returned is 20 | Step05 remains sequential and far below quota; quota is never a reason to acquire unnecessary probes | general Search API result limits must not be silently applied to Wordstat GetTop depth |
| S05V2-04 | Yandex Cloud Product Digest — April 2026 | Yandex Cloud | OFFICIAL_PRICING_PUBLICATION | https://yandex.cloud/en/blog/digest-april-2026 | 2026-09-12 | current provider price | from GA, GetTop is 20 RUB / 1000 requests; GetDynamics 20/1000; RegionsDistribution 50/1000; RegionsTree free | one GetTop call is approximately 0.02 RUB, but price must be rechecked immediately before a later executable command | tariff does not establish whether a probe is worth executing |
| S05V2-05 | Подбор поисковых запросов и анализ рынка β | Yandex Webmaster | OFFICIAL_SEARCH_ENGINE_GUIDANCE | https://yandex.ru/support/webmaster/ru/service/queries-selection | 2026-09-12 | discovery/expansion principle | Yandex recommends selecting target queries, finding additional/non-obvious formulations, and evaluating which formulations are suitable; supports region/device controls and `!` for word form | confirms that targeted expansion is legitimate, but only after checking suitability and scope | this Webmaster tool is not the project provider contract and does not define Step05 queue authorization |
| S05V2-06 | На какие вопросы отвечает ваш сайт | Yandex Webmaster | OFFICIAL_SEARCH_ENGINE_GUIDANCE | https://yandex.ru/support/webmaster/ru/recommendations/targeting | 2026-09-12 | vocabulary breadth / relevance | users may use synonyms and other words to widen or narrow a query; popularity varies and suitable phrases must be selected | supports looking for missing vocabulary rather than copying only client labels | does not define final clustering or prove inventory/claims |
| S05V2-07 | How to do keyword research in 2026 | Semrush | HIGH_QUALITY_INDUSTRY_PRACTICE | https://www.semrush.com/blog/keyword-research/ | 2026-09-12 | prioritization after expansion | modern keyword research includes discovering terms and deciding which are actually worth pursuing; irrelevant terms must be filtered rather than retained automatically | corroborates the project rule that expansion candidates must be relevant and useful, not generated just because a tool can return them | third-party practice; does not override Yandex provider semantics or project authority |
| S05V2-08 | Keyword Intent: What It Is and How to Use It in Your SEO Strategy | Ahrefs | HIGH_QUALITY_INDUSTRY_PRACTICE | https://ahrefs.com/blog/keyword-intent/ | 2026-09-12 | relevance before volume | intent/business fit should be considered before raw volume when deciding whether a keyword belongs in a strategy | supports rejecting low-information or business-misaligned expansion candidates even when they may have demand | Step05 does not make final intent/page decisions; those remain later roadmap stages |

## 3. Current repository-side Bridge authority

Checked on the live project branch:

- `extension/src/shared/product.js`
- `extension/src/shared/wordstat_protocol.js`
- relevant Wordstat execution path in `extension/src/service_worker.js`

Current repository product identity: `Yandex Marketing Bridge 0.1.2`.

Current `WORDSTAT_API_V1` Bridge schema supports methods:

```text
getTop
getDynamics
getRegionsDistribution
getRegionsTree
```

For `getTop`, current repository validation includes:

```text
phrase = required
numPhrases = integer 1..2000, default 100
regions = array, default ["225"]
devices = DEVICE_ALL | DEVICE_DESKTOP | DEVICE_PHONE | DEVICE_TABLET
```

Hard distinction:

```text
OFFICIAL YANDEX DOCS
= provider/search meaning, supported operators, quotas, pricing

CURRENT BRIDGE CODE
= executable project envelope and local field validation

HISTORICAL SUCCESSFUL REQUEST
= project-tested historical evidence only
```

Do not present a Bridge-only field as an official Yandex public API field unless current official docs explicitly support it.

## 4. Source-driven Step05 method

Current Step05 method is therefore:

```text
accepted Step04 gap hypothesis
→ reconcile against ALL durable existing acquisition evidence
→ distinguish search-demand unknown from owner/business-fact unknown
→ reject literal and semantic duplicates
→ use bounded operator/qualification only when it isolates a genuinely different question
→ require positive information gain
→ require useful negative-result value
→ require explicit stop condition
→ authorize no more acquisition than the unresolved question needs
→ preserve complete RAW if later executed
→ immediately normalize/sanitize new evidence through Step03A/03B rules before union
```

This directly implements universal F05-1 and F05-2.

## 5. Current W09 queue implication

Accepted W09 queue state:

```text
POSSIBLE_SEARCH_GAP_CANDIDATES_TO_CHALLENGE = PSQ001, PSQ004, PSQ005
OWNER_FACT_FIRST_OR_ONLY = PSQ002, PSQ003, PSQ009, PSQ012, PSQ013
EXISTING_EVIDENCE_REUSE = PSQ006, PSQ007, PSQ008, PSQ010
DEFER_TO_LATER_SERP_INTENT = PSQ011
PROVIDER_READY_NOW = 0
```

Historical E013 `!чётки` is durable evidence with remote readback PASS and must not be blindly replayed.

## 6. Method changes caused by this research/correction

Compared with the premature V1 preparation:

1. industry-practice corroboration is now explicitly present, as required for an analytical SEO step;
2. the current Yandex Webmaster query-selection guidance is included as official search-engine support for discovering non-obvious formulations;
3. the project keeps a strict line between query expansion and final intent/clustering/page ownership;
4. current Bridge code is explicitly separated from Yandex provider documentation;
5. no current queue row is provider-authorized before W10 reconciliation.

## 7. External-source gate conclusion

Fresh external research supports a **targeted, deduplicated, bounded expansion** method. It does not support broad recollection, owner-fact inference from search data, or automatic execution of every Step04 gap.

`PRE_STEP_EXTERNAL_RESEARCH` may pass only together with the owner-facing clickable disclosure in chat and the mandatory plain-Russian summary before Work execution.
