# KW-002 Step04 post-audit corrective rework — pre-step external research

Date checked: 2026-09-11

Purpose: method support only. No source below supplies Blood & Sand demand, inventory, final intent, SERP clusters, pages or IA.

| Source | Principle used | Concrete control | Limitation |
|---|---|---|---|
| [Yandex Webmaster — Query selection](https://yandex.ru/support/webmaster/ru/service/queries-selection) | Meaning/intent grouping is distinct from demand and competition metrics. | Frequency never enters family assignment or defect gates. | No Wordstat/Search request was made. |
| [Yandex Webmaster — Search quality](https://yandex.com/support/webmaster/en/search-quality) | User objective and usefulness matter. | Explicit meaning/media/DIY/toy tasks outrank unqualified fallbacks. | General guidance, not project-specific truth. |
| [Topvisor — clustering](https://topvisor.com/ru/support/clustering/) | Final SEO grouping depends on SERP overlap and theme testing. | Families remain preliminary and expose `serp_cluster_status=NOT_EVALUATED_AT_STEP04`. | SERP collection is prohibited in this pass. |
| [Ahrefs — keyword clustering](https://ahrefs.com/blog/keyword-clustering/) | Term diagnostics and final intent/SERP clusters answer different questions; clustering is interpretive. | TF-IDF/topics are warnings and QA evidence, not page authority. | Commercial workflow is not a job authority. |
| [Semrush — keyword clustering](https://www.semrush.com/blog/keyword-clustering/) | Shared task/intent matters; subtle wording can change the task. | Task-bearing morphology is checked before unqualified fallback. | No final intent label is assigned. |
| [scikit-learn — feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html) | TF-IDF downweights corpus-common terms; very short texts can be noisy. | Independent QA combines TF-IDF with simultaneous binary boundary signals. | TF-IDF is not ground truth. |
| [Python — regular expressions](https://docs.python.org/3/library/re.html) | Search/match/full-match boundaries differ. | Game evidence uses bounded token morphology; `игруш*` is separate. | Regex correctness does not prove business relevance. |

Trace: source principle → bounded deterministic rule → full-volume invariant → independent post-correction check. Completed Step00–03B remain frozen; W07 is the accepted defect oracle; this execution is W08 Step04 correction only. Step05/06 and all provider acquisition remain blocked.
