# KW-002 Step06 — external method audit

Date: 2026-09-17  
Status: **FINAL EXTERNAL CONTROL PASS**

## Sources

### Yandex-specific authority

1. Yandex Webmaster — “Подбор поисковых запросов и анализ рынка”  
   https://yandex.ru/support/webmaster/ru/service/queries-selection

Yandex explicitly supports analysis of popular sites and pages, describes clustering as grouping queries close by meaning/intent, describes competitiveness in the context of promotion into Top-10, and allows region/device selection. Its own market data are aggregated over time, which reinforces that a one-time live SERP acquisition must be described as a snapshot.

### Cross-industry SERP / intent methodology

2. Ahrefs — Search Intent in SEO  
   https://ahrefs.com/blog/search-intent/

3. Ahrefs — SERPs explained / Top-10 intent review  
   https://ahrefs.com/blog/serps/

Ahrefs' 3Cs framework uses dominant content type, format and angle from top-ranking results as intent evidence. This supports Step06 page-type/format analysis. It does not constitute a Yandex-specific ranking rule.

### SERP-similarity clustering methodology

4. SE Ranking — “Как кластеризовать запросы”  
   https://help.seranking.com/hc/ru/articles/16332627413148-%D0%9A%D0%B0%D0%BA-%D0%BA%D0%BB%D0%B0%D1%81%D1%82%D0%B5%D1%80%D0%B8%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81%D1%8B

SE Ranking scans Top-10 and groups queries by matching ranking URLs; hard grouping compares queries with each other. This supports the 231-pair exact-URL matrix and the rule that domain overlap alone is not enough.

### Search competitor vs business competitor

5. Ahrefs — SEO Competitor Analysis  
   https://ahrefs.com/blog/seo-competitor-analysis/

6. Semrush — SEO Competitor Analysis  
   https://www.semrush.com/blog/how-to-do-seo-competitive-analysis/

Both distinguish organic/search competitors from direct business rivals. That supports Step06's core `BUSINESS RIVAL != SEARCH COMPETITOR` rule.

## External-method verdict

The final Step06 method is aligned with the external evidence on the points that materially matter for this bounded step:

- actual SERP occupants, not a preselected business-rival list;
- Top-10 as the main analytical layer;
- concrete ranking pages, not domains alone;
- result type/format as intent evidence;
- exact URL overlap in Top-10 as a clustering signal;
- region/device disclosure;
- bounded snapshot language;
- collision preservation and uncertainty;
- no premature final page decision.

## Defects found during this second audit and corrected

1. **Stale accepted denominators in the first hardened registry.** `commercial_*_8` and `informational_*_9` were based on preliminary labels. Final accepted populations are 6 and 11. The stale fields were removed/recomputed.
2. **Ambiguous “clean” recurrence wording.** The actual metric excluded whole flagged queries, not non-target rows. It is now named `safe_query_subset_*` and explicitly marked query-level.
3. **Page-type taxonomy gap.** The frozen Work enum omitted `AUDIO`; recurring listening/music results can be under `OTHER`. Limitation is now explicit and future method is extensible.
4. **Region/device scope was not prominent enough.** Region is Russia/provider 225; device is not captured and is now explicitly disclosed.
5. **Full 3C content-angle analysis was not actually done.** The final method does not pretend it was; content-angle work is deferred to the later content/page-specification stage.
6. **Work-only transport rule had been overgeneralized to Main ChatGPT.** Corrected separately in Level1.

## Quality score

### Before this second external audit

`8.8 / 10`

The underlying data and Work classification were strong, but stale denominator fields and ambiguous recurrence semantics meant the “hardened” derivative files were not yet final-quality.

### After this final patch

`9.3 / 10 — BOUNDED PASS`

Component view:

| Component | Score |
|---|---:|
| acquisition/evidence accounting | 10.0/10 |
| 440-row semantic classification + explicit uncertainty | 9.2/10 |
| 22 Top-10 query profiles | 9.5/10 |
| 231 exact-URL/domain pairwise matrix | 10.0/10 |
| collision/uncertainty handling | 9.5/10 |
| competitor recurrence/registry after denominator fix | 9.5/10 |
| scope discipline / no premature page decisions | 10.0/10 |
| temporal/device/SERP-feature coverage | 7.5/10 |

The remaining gap from 10/10 is not a hidden analytical defect. It is the explicitly bounded source scope: one temporal snapshot, device not captured, SERP features not captured, frozen page-type enum coarsens audio surfaces, and full content-angle analysis belongs to a later step.

No new provider acquisition is justified merely to inflate the score. Those limitations should remain visible and be handled only when the roadmap requires them.
