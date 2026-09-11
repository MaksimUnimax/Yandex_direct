# KW-002 Step04 independent audit — external method source trace

Date checked: 2026-09-11

Scope: methodology only. None of these sources is used as authority for Blood & Sand business facts, demand, inventory, intent, page design or IA.

| Source | Current methodological principle used | Audit use | Boundary |
|---|---|---|---|
| [Yandex Webmaster — Query selection](https://yandex.ru/support/webmaster/ru/service/queries-selection) | Query clusters are automatic groupings by close meaning or user intent; demand/click/competition are separate measures. | Tests topical/task coherence separately from frequency. | Webmaster grouping is not copied as this job's family authority. |
| [Yandex Webmaster — Search quality](https://yandex.com/support/webmaster/en/search-quality) | Search quality is evaluated against the user's objective and usefulness. | Requires family task hypotheses to be supported by member wording. | No ordinary Yandex Search call was made. |
| [Topvisor — clustering](https://topvisor.com/ru/support/clustering/) | Final SEO clustering commonly uses overlap in Yandex/Google Top-10 and must be tested for the theme. | Establishes why this audit may test preliminary lexical families but cannot approve final clusters. | No SERP collection or final clustering was performed. |
| [Ahrefs — keyword clustering](https://ahrefs.com/blog/keyword-clustering/) | Intent/SERP similarity clustering and term/co-occurrence clustering answer different questions. | Uses term TF-IDF/topic decomposition only as an independent diagnostic. | Diagnostic topics do not become pages or final keyword clusters. |
| [Ahrefs — search intent](https://ahrefs.com/blog/search-intent/) | Mixed/volatile result sets can reflect mixed or changing intent. | Rewards preserved ambiguity and rejects premature intent labels. | No live SERP inference was made. |
| [Semrush — keyword clustering](https://www.semrush.com/blog/keyword-clustering/) | Large sets need scalable grouping while respecting SERP similarity, content breadth and user journey. | Supports exhaustive machine checks plus explicit downstream boundaries. | This pass does not design content or user journeys. |
| [scikit-learn — text feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html) | TF-IDF downweights corpus-common terms; short text remains noisy. | Provides a reproducible independent term-space diagnostic over all 18,135 active/HOLD identities. | TF-IDF distances are evidence, not ground truth. |
| [scikit-learn — clustering evaluation](https://scikit-learn.org/stable/modules/clustering.html) | Internal clustering measures describe separation and have known limitations. | Uses topic entropy, centroid similarity and alternate-centroid rates as warnings, not final verdicts. | Human-governed rule/lineage evidence controls material defect findings. |

Pre-execution owner-facing disclosure was made before the diagnostic run and identified the job goal, completed/remaining steps, this audit's purpose, prior failures, controls, planned method and acceptance conditions.
