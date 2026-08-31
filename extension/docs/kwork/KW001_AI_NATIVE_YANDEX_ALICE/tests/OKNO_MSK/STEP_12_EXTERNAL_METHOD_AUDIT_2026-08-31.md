# Step 12 — Independent external methodology audit

Date: 2026-08-31
Status: **CORRECTION REQUIRED BEFORE FINAL ACCEPTANCE**
Scope: independent post-execution review of Step 12 structural actions. This audit does not execute Step 13 and does not rewrite Step-12 decisions yet.

## Plain-language verdict

Step 12 got the main idea right: do not create a separate page for every search phrase, reuse strong existing pages, add content to the right page where possible, and create a new page only when there is a real independent user need.

However, the final `PASS` is too strong. During implementation, 191 phrase-level destinations were assigned through hard-coded word-pattern rules, all structural decisions defaulted to HIGH confidence unless explicitly changed, several QA checks were self-asserted instead of independently derived, and some supposedly stable clusters still contain materially different user tasks. The five proposed new pages therefore are not equally proven.

Audit verdict:

```text
STEP12_ANALYTICAL_DIRECTION = GOOD
STEP12_IMPLEMENTATION_AUDITABILITY = INSUFFICIENT
STEP12_NEW_PAGE_EVIDENCE = INCOMPLETE
STEP12_QA_INDEPENDENCE = FAIL
STEP12_FINAL_ACCEPTANCE = WITHDRAWN_PENDING_CORRECTION
NEXT_STEP_13 = BLOCKED UNTIL STEP12 CORRECTION / RE-ACCEPTANCE
OVERALL_SCORE = 6.5 / 10
```

## External method basis

### Yandex Webmaster — user need must define the answer
https://yandex.ru/support/webmaster/ru/recommendations/targeting?lang=ru

Yandex states that Search answers user questions and that page visibility depends on how well page content corresponds to how users formulate their needs. This supports task-first page mapping and rejects purely lexical URL assignment.

### Yandex Webmaster — site structure
https://yandex.ru/support/webmaster/ru/recommendations/site-structure

Yandex recommends a clear link structure, a logical section for every document, ordinary crawlable links, and navigation that lets users find needed documents quickly. New pages therefore need an explicit position and internal-link path, not only a proposed slug.

### Yandex Webmaster — information presentation
https://yandex.ru/support/webmaster/ru/recommendations/presentation

Yandex recommends splitting large content into separate pages only by major logical units, not by small fragments. This supports the Step-12 principle that small modifiers or FAQ questions should not automatically become separate URLs.

### Yandex Webmaster — low-value / low-demand pages
https://yandex.ru/support/webmaster/ru/site-indexing/low-demand

Yandex can exclude pages that duplicate existing pages, lack useful content, or do not correspond well to real user queries. Yandex also states there is no quota on useful pages. This supports both avoiding thin page inflation and avoiding arbitrary page-count limits.

### Yandex Webmaster — useful content
https://yandex.ru/support/webmaster/ru/threat/useless-content

Yandex emphasizes that useful content solves the user's task, gives a quality and trustworthy answer, is original, understandable and easy to navigate.

### Semrush — Keyword Mapping, 2026-07-27
https://www.semrush.com/blog/keyword-mapping/

Semrush's current workflow: group closely related terms that share intent; review the keyword assignments; check monthly demand; assess intent, volume and difficulty; map a suitable existing page or mark a new one to create; open and confirm every suggested URL. New-page prioritization should consider business relevance, search volume and realistic ranking opportunity.

### Ahrefs — Keyword Mapping
https://ahrefs.com/blog/keyword-mapping/

Ahrefs groups same/similar-intent terms into one topic/page, uses secondary keywords for subordinate subtopics, and distinguishes Create / Optimize / No action. It also recommends considering traffic and business potential when deciding which topics deserve standalone pages.

### Ahrefs — Keyword Clustering
https://ahrefs.com/blog/keyword-clustering/

SERP-similar queries generally belong together, but clustering is explicitly imperfect and ambiguous/mixed cases need closer review. This is important for the mixed Step-12 clusters noted below.

### Rush Analytics — structure from semantic core
https://www.rush-analytics.ru/faq/kak-sozdat-strukturu-sayta-na-osnove-semanticheskogo-yadra
https://www.rush-analytics.ru/faq/klasterizaciya-zaprosov-semanticheskogo-yadra-rukovodstvo
https://www.rush-analytics.ru/faq/klasterizaciya/opredelenie-relevantnyh-url-dlya-klasterov

Rush ties page structure to clustered queries, SERP similarity and frequency, and treats the decision to create additional pages as something that should be informed by demand and the search result structure rather than keyword wording alone.

### Semantica Media — relevance map, 2026-06-05
https://semantica-media.ru/blog/karta-relevantnosti-chto-eto-takoe-zachem-nuzhna-i-kak-sostavit-dlya-sajta.html

The relevance map is a working decision table, not only a keyword list. It should preserve cluster, target URL, page type, status and implementation notes. The article also stresses that different expected formats/tasks should be split and that the map must connect to site structure and internal linking.

### Semrush — cannibalization, 2026-07-14
https://www.semrush.com/blog/keyword-cannibalization-guide/

Multiple ranking pages are not automatically cannibalization. Harmful competition must be established separately. Step 12 was correct to reserve that diagnosis for Step 13.

## What Step 12 did well

### 1. It rejected the dangerous `NO OWNER -> CREATE` shortcut

The 25 Step-11 clusters without a suitable page did not become 25 new pages. Step 12 proposed only five new pages and deliberately rejected unsupported products/services and neutral-rating pages. This is strongly consistent with Yandex low-value guidance and Ahrefs/Semrush mapping practice.

### 2. It distinguished keep / expand / section / new page / no page

The action set is much better than a binary old-page/new-page model. Subordinate questions such as balcony selection and French-window definitions are assigned as sections on existing pages rather than thin independent URLs.

### 3. It preserved all 2332 active phrases

The phrase-action map contains the full active set, with 19 unresolved phrases preserved and no silent drops. This is a strong auditability improvement over cluster-only decisions.

### 4. It refused to invent products and services

Wood windows, timber-aluminium windows, roof windows, soft windows, standalone mosquito-net repair and PVC-door repair/replacement were not converted into commercial pages where the current site did not verify the offer. This is a strong business-truth control.

### 5. It kept cannibalization out of Step 12

Step 12 did not claim that multiple similar URLs necessarily harm rankings. This matches current Semrush guidance and the project roadmap boundary.

### 6. It used the existing hierarchy rather than creating duplicate pages

Existing REHAU model pages, PVC-door children, aluminium sliding/hinged pages, warm/cold veranda pages, calculator, P-44, private-house and accessory pages were reused where appropriate.

## Material defect 1 — 191 phrase routes are hard-coded lexical rules, not validated structural units

The implementation function `route_override(cluster_id, phrase)` assigns pages by substring rules such as:

```text
contains "рассроч" or "кредит" -> credit/instalment page
contains "калькулятор" -> calculator
contains "частного дома" -> private-house page
contains "п44" -> P-44 page
contains "раздвиж" in aluminium -> sliding page
contains "тепл" in outdoor glazing -> warm-veranda page
contains model token -> exact REHAU model page
```

This produced 191 overrides, including 53 phrases routed to the finance page from six source clusters.

Many of these destinations are plausible, especially exact model and exact object/subtype queries. But the mechanic is still a lexical classifier. It was not separately registered in `STEP_12_SOURCE_TO_METHOD_TRACE.tsv`, and it does not prove that the specialized page is the best primary search landing rather than a supporting conversion page.

Correction required:

```text
PHRASE OVERRIDE
-> explicit structural subunit / subcluster
-> task statement
-> all member phrases
-> current page read
-> evidence for primary vs supporting destination
-> confidence
```

Do not keep 191 independent hidden exceptions as the final architecture model.

## Material defect 2 — the “full phrase audit” still left mixed clusters and then created pages from them

### `WINDOW_INSTALLATION_DIY_INFO`

The 36 phrases are not one pure “install PVC windows yourself” task. The set also contains:

- installing/removing PVC doors;
- removing a balcony door;
- aluminium-window assembly/removal;
- French-window DIY phrases.

Yet all 36 are routed to proposed `/stati/ustanovka-plastikovyh-okon-svoimi-rukami/`.

That proposed page may still be justified for the true PVC-window DIY subset, but the current 36/36 mapping is not acceptable.

### `PANORAMIC_WINDOWS_COMMERCIAL`

The 73-row cluster contains strong commercial phrases, but also inspiration/object/architecture and command-like phrases. The statement “large, stable commercial task” is therefore too strong for the full set without another split/review.

A broad commercial panoramic page is plausible, but it should not receive every current member automatically.

### `GLAZING_PERMISSION_INFO`

The no-generic-page verdict is reasonable, but the cluster mixes balcony permission, French-window redevelopment, boiler-room requirements and hardware standards. Step 12 says these should be distributed to relevant contexts but does not actually materialize those phrase-level destinations.

### `WOOD_WINDOWS_COMMERCIAL`

The cluster contains `пластиковые окна в деревянном доме`, which is not a wooden-window product query and likely belongs to private-house PVC planning. A cluster-level `NO_STANDALONE_PAGE` leaves that useful phrase without the more appropriate existing destination.

Correction required: re-audit mixed clusters before final structural actions. Preserve the history, but create explicit post-Step-12 semantic/structural correction rows instead of hiding the mismatch.

## Material defect 3 — proposed new pages lack an explicit demand/competition evidence matrix

The five new pages are justified mainly with:

- number of assigned phrases;
- stable-task narrative;
- current page gap;
- business fit.

The action ledger does not show, per new page:

```text
aggregated / representative Wordstat demand
which high-demand phrases drive the page
whether direct Search/SERP evidence confirms a standalone page type
which competitor/result page types dominate
whether the target business can provide the promised content/service
```

Semrush 2026 explicitly recommends using intent, volume and difficulty/reachability when selecting page ideas and gives higher weight to higher-demand page ideas. Ahrefs likewise recommends traffic + business potential. Rush also uses frequency and SERP clustering to decide on additional pages.

This does not mean every new page is wrong. It means `HIGH` confidence is not auditable yet.

Correction required: create `STEP_12_NEW_PAGE_EVIDENCE.tsv` for all new-page candidates using already collected Wordstat/Search evidence first. Only call Bridge if a named evidence gap remains and owner authorizes it.

## Material defect 4 — confidence is HIGH by default

The helper is defined as:

```python
def spec(..., confidence='HIGH', ...)
```

Therefore any action not manually downgraded becomes HIGH. The current confidence column is not an evidence-derived score.

This especially overstates:

- new panoramic commercial page;
- replacement service page;
- hardware guide;
- DIY installation guide;
- DIY repair guide;
- broad EXPAND decisions inherited from MEDIUM Step-11 ownership.

Correction required: confidence must be derived from explicit evidence dimensions, for example task coherence, business truth, current page fit, demand support and direct SERP support. Do not default to HIGH.

## Material defect 5 — important QA counters are self-asserted or structurally wrong

The script hard-codes or weakly proxies several PASS conditions:

```text
new_page_from_modifier_only = 0
premature_step13_cannibalization_verdicts = 0
premature_step14_architecture_freeze = 0
ai_evidence_used_in_step12 = 0
full_phrase_level_trace_used = True
existing_child_and_utility_routing_used = True
```

Other checks do not actually test the declared property:

```text
new_page_without_distinct_stable_task
= only checks whether a rationale string exists
```

Most importantly:

```text
split_without_major_logical_task_boundary = action_counts[SPLIT_EXISTING_PAGE]
merge_based_only_on_suspected_cannibalization = action_counts[MERGE_STRUCTURALLY_REDUNDANT_PAGES]
```

This means **any** SPLIT or MERGE action would automatically fail QA, even when it was properly justified. The implementation therefore cannot validate legitimate split/merge decisions and is biased toward zero such actions.

The current `SPLIT=0 / MERGE=0` may still be analytically correct, but the QA cannot prove it.

Correction required: QA must inspect the evidence attached to each split/merge, not count every split/merge as an error. Hard-coded zero/true gates should be replaced by independently computed checks or explicit execution receipts.

## Material defect 6 — Step-13 handoff is manually curated rather than derived from actual multi-page routing

Step 12 flags only selected clusters for Step 13. But the actual phrase map routes many source clusters across parent + child/utility pages (REHAU model pages, P-44, private-house, finance, PVC-door children, aluminium children, accessory children, etc.).

Not all of these are cannibalization problems, but they are the exact places where Step 13 may need to confirm that parent/child responsibility is stable.

Correction required: generate a Step-13 candidate-pair ledger from the actual phrase/page map:

```text
source semantic family / cluster
page A
page B
shared / adjacent task
phrases routed to each
reason overlap may be normal
reason direct Search check may be needed
```

Then Step 13 can sample/validate from a complete candidate universe instead of manually selected flags.

## Material defect 7 — new-page hierarchy is only partially implementation-ready

New pages have `parent_page_or_section`, which is good, but Yandex's site-structure guidance expects actual crawlable placement and clear navigation. The current artifact does not yet state the concrete inbound/outbound internal links and user path for every new page.

Correction required for each final new page:

```text
parent URL
link from parent: yes / anchor concept
links to relevant child/support pages
links back to commercial conversion page when informational
navigation/breadcrumb placement
```

This is not a technical SEO audit; it is the structural implementation layer required to make the proposed architecture coherent.

## Specific verdict on the five proposed new pages

### `PANORAMIC_WINDOWS_COMMERCIAL`
Verdict: **PLAUSIBLE, NOT YET HIGH-CONFIDENCE FINAL**.

Strong commercial demand is visibly present, and no broad current commercial owner exists. However, current membership is still mixed. Re-split noncommercial/object-inspiration phrases and attach explicit Wordstat/SERP evidence before final acceptance.

### `WINDOW_REPLACEMENT_SERVICE`
Verdict: **STRONGEST NEW COMMERCIAL CANDIDATE**.

The 13 phrases are much more coherent, and the current installation page is related but not identical. Keep as a candidate, but attach demand/SERP evidence and reduce confidence until that trace is materialized.

### `WINDOW_HARDWARE_INFO`
Verdict: **PLAUSIBLE INFORMATIONAL PILLAR, NEEDS TASK/SERP REVIEW**.

The set contains definitions, selection, rankings/reviews and maintenance/lubrication. One broad guide may work, but external clustering practice says mixed intent should be verified rather than assumed. Consider one pillar with explicit subtopics only if SERP/task coherence holds.

### `WINDOW_INSTALLATION_DIY_INFO`
Verdict: **CURRENT 36/36 MAPPING FAILS**.

The proposed PVC-window DIY article may survive for a corrected subset, but the current cluster contains doors, aluminium and French-window tasks. It must be split/reassigned before the page can be accepted.

### `WINDOW_REPAIR_DIY_INFO`
Verdict: **PLAUSIBLE, NEEDS CLEANUP + DEMAND/SERP SUPPORT**.

Most phrases fit broad self-help repair/adjustment, but some ambiguous/outlier phrases remain. Clean the set and then verify the standalone topic against demand/search evidence.

## Scorecard

| Dimension | Score | Audit comment |
|---|---:|---|
| High-level structural logic | 9/10 | Strong separation of keep/expand/section/new/no-page and no auto-create. |
| Business truth / offer discipline | 9/10 | Strong refusal to invent products/services. |
| Phrase accounting | 10/10 | 2332/2332 preserved, 19 unresolved preserved. |
| Existing-page reuse | 8/10 | Strong idea, but 191 overrides are implemented as lexical rules. |
| New-page justification | 6/10 | Useful rationale exists, but demand/SERP evidence is not materialized per page. |
| Semantic coherence of final routes | 6/10 | Several mixed clusters survived full review. |
| Confidence calibration | 3/10 | HIGH is the default rather than evidence-derived. |
| QA independence | 3/10 | Multiple gates are hard-coded/self-certified; split/merge check is logically wrong. |
| Step-boundary discipline | 9/10 | Cannibalization and AI were correctly deferred. |
| Implementation-ready hierarchy | 6/10 | Parent placement exists, internal-link plan is incomplete. |

Overall: **6.5/10 — good analytical direction, material correction required before final acceptance.**

## Required correction sequence

1. Freeze the current Step-12 artifacts as historical first pass; do not overwrite them silently.
2. Replace `route_override()` lexical exceptions with an explicit structural-subunit ledger and evidence for each group.
3. Re-audit mixed clusters, at minimum `WINDOW_INSTALLATION_DIY_INFO`, `PANORAMIC_WINDOWS_COMMERCIAL`, `GLAZING_PERMISSION_INFO`, `WOOD_WINDOWS_COMMERCIAL`, plus risk-based checks of `WINDOW_HARDWARE_INFO` and `WINDOW_REPAIR_DIY_INFO`.
4. Build `STEP_12_NEW_PAGE_EVIDENCE.tsv` for the five proposed pages using existing Wordstat and Search evidence: demand, representative queries, page-type/intent evidence, business fit, current gap.
5. Recompute confidence from evidence; no default HIGH.
6. Rewrite QA so every gate is independently computed and valid SPLIT/MERGE actions are allowed when supported.
7. Generate a complete Step-13 candidate-pair handoff from the final phrase-to-page mapping.
8. Add explicit hierarchy/internal-link placement for every final new page.
9. Rebuild phrase-action map and page rollup; require 2332/2332 accounting and GitHub readback.
10. Only then reissue Step-12 acceptance and allow Step 13.

## Bridge / provider implication

No new paid provider call is automatically required for the correction. Existing Wordstat and Search evidence should be reconciled first. If the new-page evidence matrix exposes a specific missing Search boundary after using saved evidence, stop and request owner authorization before any new Bridge call.
