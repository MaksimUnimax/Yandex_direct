# STEP 04 — PRE-STEP SOURCE TRACE — REFRESH

Date checked: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Step: `04 — first family triage`
Status: **PASS / FRESH INTERNET RESEARCH COMPLETE / SOURCE DISCLOSURE SHOWN TO OWNER BEFORE EXECUTION**

## Exact methodological questions

1. What does current Yandex Wordstat top-query evidence actually prove?
2. Is discovery of non-obvious related query formulations a legitimate coverage signal?
3. Should frequency alone decide business relevance?
4. Where is the boundary between preliminary family triage and later intent/SERP clustering/page design?
5. How should mixed or uncertain intent be handled before later SERP evidence?

## Source-to-method trace

| source_id | source_title | publisher | source_class | url | checked_at | method_element_supported | exact_claim_supported | project_specific_application | claim_boundary |
|---|---|---|---|---|---|---|---|---|---|
| S04-WEB-01 | Вордстат | Яндекс | OFFICIAL_PROVIDER | https://yandex.ru/support2/wordstat/ru/ | 2026-09-10 | meaning of Wordstat evidence | Wordstat provides Yandex query statistics, top queries with chosen words and other queries on the same topic | treat Step03 rows/associations as observed demand/discovery evidence, not final business labels | does not prove client relevance, intent, cluster or page ownership |
| S04-WEB-02 | Вордстат — интерфейс / Топы запросов | Яндекс | OFFICIAL_PROVIDER | https://yandex.ru/support2/wordstat/ru/interface/new | 2026-09-10 | top-query scope, region/device and related-query discovery | Top queries show popular queries containing the entered phrase and queries similar to it; region/device can be selected | preserve region/provenance and recognize that related rows can contain both useful expansion and noise | does not state that every returned query is suitable for this business |
| S04-WEB-03 | Подбор поисковых запросов и анализ рынка β | Яндекс Вебмастер | OFFICIAL_SEARCH_ENGINE | https://yandex.ru/support/webmaster/ru/service/queries-selection | 2026-09-10 | coverage discovery | Yandex describes finding suitable and additional queries, including non-obvious wording | coverage-gap / requires-expansion is a legitimate Step04 state; do not discard unfamiliar wording mechanically | tool guidance does not define Blood & Sand business fit |
| S04-WEB-04 | Мониторинг поисковых запросов / Расширенная аналитика по URL | Яндекс Вебмастер | OFFICIAL_SEARCH_ENGINE | https://yandex.ru/support/webmaster/ru/service/popular-queries ; https://yandex.ru/support/webmaster/ru/service/queries-export | 2026-09-10 | query↔URL and meaning boundary | Yandex exposes query-to-URL relationships and frames URL reports as checking page relevance to query meaning | confirms that page-fit/ownership is a separate downstream evidence layer; Step04 must not design pages | new greenfield site does not yet have its own query↔URL history |
| S04-WEB-05 | Keyword Intent: What It Is and How to Use It in Your SEO Strategy | Ahrefs | INDUSTRY_PRACTICE | https://ahrefs.com/blog/keyword-intent/ | 2026-09-10 | relevance before volume; mixed intent | intent is a strategic filter and mixed intent requires explicit handling | supports not using search volume as the only relevance verdict and preserving ambiguity | Google-oriented industry practice; corroboration, not Yandex official rule |
| S04-WEB-06 | How to Do Keyword Clustering & Why It Helps SEO | Semrush | INDUSTRY_PRACTICE | https://www.semrush.com/blog/keyword-clustering/ | 2026-09-10 | downstream clustering boundary | clustering groups keywords by intent and can use SERP similarity | confirms clustering/page grouping belongs later, not in Step04 family triage | industry method, not an official Yandex requirement |

## Method conclusion

Fresh research confirms the current Step04 method with one important execution boundary made explicit:

```text
WORDSTAT RETURNED ROW != AUTOMATIC BUSINESS-RELEVANT KEYWORD
WORDSTAT COUNT != RELEVANCE VERDICT
FAMILY TRIAGE != FINAL ROW CLEANUP
FAMILY TRIAGE != FINAL CLUSTERING
FAMILY TRIAGE != PAGE OWNERSHIP
UNKNOWN / MIXED MEANING -> mixed/ambiguous, not forced keep/reject
NON-OBVIOUS BUT BUSINESS-SUPPORTED LANGUAGE -> preserve as plausible/coverage signal
```

Step04 must evaluate families against current client/business/assortment authority and observed query meaning while preserving source provenance. Obvious entity collisions, unrelated media/games/books, Chery Amulet/automotive homonyms, morphology noise and other unrelated topics may be marked obvious out-of-scope only when the meaning/evidence supports that decision, never because of a token or low count alone.

## Execution boundary

No Wordstat/Search/GenSearch/Alice/provider request is needed for Step04 itself. No Search-based clustering, URL assignment, IA, Page Jobs or content design may be performed.

Fresh pre-step web research: PASS.
Owner-facing clickable source disclosure: PASS before Work execution.
