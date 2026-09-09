# STEP 04 — PRE-STEP SOURCE TRACE

Date: 2026-09-09
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Purpose: methodology-only pre-step research before any downstream semantic triage.

## Sources reviewed

1. Yandex Webmaster — Подбор поисковых запросов и анализ рынка β
   https://yandex.ru/support/webmaster/ru/service/queries-selection

2. Yandex Webmaster — Мониторинг поисковых запросов
   https://yandex.ru/support/webmaster/ru/service/popular-queries

3. Yandex Webmaster — Расширенная аналитика поисковых запросов по URL β
   https://yandex.ru/support/webmaster/ru/service/queries-export

4. Ahrefs — How To Do Keyword Clustering the Easy Way
   https://ahrefs.com/blog/keyword-clustering/

## Source-to-method mapping

Yandex states that keyword-selection data is used to find target queries, including non-obvious formulations, and describes clusters as groups close by meaning or user intent. Yandex also exposes query↔URL relationships and explicitly frames them as a way to check whether pages match query meaning.

Ahrefs describes clustering as grouping keywords with the same or similar intent and often using SERP similarity. This is useful as a downstream warning boundary: Step04 must not collapse triage into final clustering or page assignment.

For Step04 the resulting methodological refinement is deliberately narrow:

```text
1. Frequency alone is not a relevance decision.
2. Every acquired phrase/family must be evaluated against the current job's business/assortment authority and user meaning.
3. Clearly relevant expansion -> RELEVANT_EXPANSION.
4. Clearly off-topic/provider-morphology/entity collision -> NOISY_EXPANSION.
5. Genuine ambiguity -> AMBIGUOUS_EXPANSION / HOLD, not forced keep/reject.
6. Preserve originating seed/request/source provenance for every decision.
7. Do not perform final clustering, page design, IA, or query-to-page assignment in Step04.
```

## Limitations

- Wordstat `getTop` is an acquisition source, not a final statement of business relevance.
- High `count` can belong to unrelated entities, products, media, automotive homonyms, games, or morphology; counts therefore cannot be used alone for retention.
- Search-intent and SERP-based clustering are later-stage methods; they are not authorization to create pages during Step04.
- The clean-greenfield source boundary remains authoritative: sealed prior Blood & Sand SEO/Wordstat/Search/Alice/competitor/cluster/IA research is not allowed as execution input.
- This trace does not itself authorize Step04 execution. The current Level-2 step gate remains independently authoritative.
