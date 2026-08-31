# Step 12 — Structural actions — pre-step method review

Date: 2026-08-31
Status: **PRE-STEP METHOD REVIEW COMPLETE / EXECUTION BLOCKED PENDING OWNER AUTHORIZATION**
Branch baseline when review started: `698e5d73c5711a811d029fb9772eb650e0e041c6`

## Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page structure recommendation for ordinary Yandex Search plus selective Yandex AI-search evidence, followed by prioritized client-ready artifacts and final QA.

## Accepted upstream state

Steps 0–11 are complete under current job authorities. Step 11 was corrected after external method audit and now materializes the complete active `phrase -> effective cluster -> target URL/state` mapping.

Current Step-11 effective truth:

```text
SOURCE_ACTIVE_ROWS = 2332
EFFECTIVE_ASSIGNED_ROWS = 2313
EFFECTIVE_SEARCH_REQUIRED_ROWS = 19
PHRASE_PAGE_MAP_ROWS = 2332
EFFECTIVE_ACTIVE_CLUSTERS = 75
OWNER_EXISTING = 44
NO_SUITABLE_EXISTING_PAGE = 25
OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP = 6
```

Historical Step-10 files remain preserved. Step-11 post-audit corrections are the effective downstream truth.

## Step-12 permanent methodology status

From `STEP_RULES_INDEX.md`:

```text
STEP_12_PERMANENT_METHOD = UNVALIDATED
CURRENT INTERNET METHOD RESEARCH = REQUIRED
SOURCE_TO_METHOD TRACE = REQUIRED
OWNER-FACING METHOD REVIEW = REQUIRED
EXECUTION = BLOCKED UNTIL REVIEW + OWNER AUTHORIZATION
```

This file is job-specific Layer-C execution/method-review evidence. It does not promote Step 12 into a universal permanent method.

## Exact Step-12 goal

For every effective **assigned** Step-11 cluster, decide what the site structure should do with that user task, using the complete phrase-level map and current page-ownership evidence.

The step converts:

```text
USER TASK + PHRASE MEMBERSHIP + CURRENT OWNER/NO-OWNER STATE
```

into an evidence-backed structural recommendation such as keep, expand, add as a section, create a new page, split a current page, merge structurally redundant pages, reject a standalone page, or take no action because the task is outside scope.

The 19 effective `SEARCH_REQUIRED` phrases do not receive structural actions while their semantic task remains unresolved. They remain an explicit handoff.

## What Step 12 does NOT decide

Step 12 does not diagnose cannibalization. That is Step 13.

Hard boundary:

```text
STRUCTURAL_REDUNDANCY_DECISION != CANNIBALIZATION_VERDICT
MULTIPLE_URLS != CANNIBALIZATION
SEARCH_VISIBILITY_HARM != ASSUMED
```

Step 12 also does not:

- freeze the final Search architecture (Step 14);
- select AI cases (Step 15);
- use GenSearch/Alice evidence (Steps 16–17);
- prioritize implementation order (Step 18);
- compress the internal architecture analysis to the mock client's `up to 15 primary commercial/page directions` limit (that limit applies to the final client-facing map, not to the internal structural truth).

## Relevant prior errors and non-repeat controls

### Error 1 — transient Bridge/Codex evidence nearly got lost

What failed:

Bridge/Codex acquisition results were allowed to exist in transient chat/tool state before complete durable GitHub persistence.

Non-repeat control in Step 12:

```text
BRIDGE_OR_CODEX_RESULT
-> IMMEDIATE GITHUB SAVE
-> GITHUB READBACK + COMPLETENESS CHECK
-> ONLY THEN NEXT ACQUISITION INTERACTION
```

No paid Bridge call is required for this pre-step review. If Step-12 execution later exposes a genuine Yandex evidence gap, a separate YMB authorization/mode/cost/result-storage gate is required before any call.

### Error 2 — cluster-only abstraction hid phrase-level defects

What failed:

A cluster label/representative query was treated as enough to reason downstream; phrase-level materialization later exposed heterogeneous clusters.

Non-repeat control in Step 12:

Every structural action must be traceable to `STEP_11_PHRASE_PAGE_MAP.tsv`; broad or weak clusters must be checked against their actual member phrases before a structural action is accepted.

### Error 3 — `NO_SUITABLE_EXISTING_PAGE` can be misread as `CREATE`

What would fail:

Creating a page merely because Step 11 found no truthful current owner would produce thin, redundant or low-demand pages.

Non-repeat control:

`NO_SUITABLE_EXISTING_PAGE` is only an input state. A new standalone page additionally requires a distinct stable user task, in-scope business value, and enough useful content/value to justify an independent document.

### Error 4 — semantic modifier can be mistaken for page boundary

What would fail:

Price, Moscow, size, color, brand or another lexical modifier could be turned into a new landing page without a distinct terminal task.

Non-repeat control:

A modifier alone never creates a page. Separate-page justification requires distinct task/intent/expected terminal result or independently useful major logical unit.

### Error 5 — Step 12 can accidentally consume Step 13

What would fail:

Seeing two similar URLs and immediately calling the situation cannibalization/merging because of rankings.

Non-repeat control:

Step 12 may recommend merge only from structural redundancy/task/content evidence sufficient without a search-conflict claim. Ranking competition or harmful multi-URL visibility remains Step 13 evidence.

## Fresh external method research

### Official Yandex — user need / query fit

Source: https://yandex.ru/support/webmaster/ru/recommendations/targeting

Yandex states that Search answers user questions and page visibility depends on how well content corresponds to users' formulated needs. This supports using the stable user task as the main structural unit instead of lexical keyword variants.

### Official Yandex — site structure

Source: https://yandex.ru/support/webmaster/ru/recommendations/site-structure

Yandex recommends a clear link structure, that each document belongs to an appropriate section, and navigation lets users quickly find needed documents. This constrains every created/split page to have an explicit place in the hierarchy and internal-link path.

### Official Yandex — information presentation / logical splitting

Source: https://yandex.ru/support/webmaster/ru/recommendations/presentation

Yandex says that when large content is split into multiple web pages, it should be split by **large logical units**, not small fragments such as paragraphs. This supports `SPLIT_EXISTING_PAGE` only for materially independent user-task/logical units, not for minor modifiers or FAQ fragments.

### Official Yandex — low-value / low-demand pages

Source: https://yandex.ru/support/webmaster/ru/site-indexing/low-demand

Yandex can exclude pages that duplicate known pages, contain insufficient useful content, or do not correspond well to user queries. It also states there is no quota on useful pages: any number of pages can be indexed if algorithms consider them useful to users. This blocks arbitrary page-count rules and supports rejecting thin standalone pages even when a keyword exists.

### Official Yandex — duplicate pages

Sources:
- https://yandex.ru/support/webmaster/ru/robot-workings/double
- https://yandex.ru/support/webmaster/ru/yandex-indexing/about-doubles

Yandex may group same-content pages as duplicates, may choose a different URL than the webmaster expects, and similar pages may participate independently and compete. This supports consolidation of **actually redundant/duplicate structural documents**, while not proving cannibalization by itself.

### Semrush 2026 — keyword mapping

Source: https://www.semrush.com/blog/keyword-mapping/
Published: 2026-07-27.

Semrush's current mapping workflow requires checking whether an existing page actually covers the topic and satisfies intent. If yes, it is a target to optimize; if no suitable page exists, a planned page may be created. The source also requires opening suggested URLs rather than accepting automated lexical matching.

### Ahrefs — keyword mapping / clustering

Sources:
- https://ahrefs.com/blog/keyword-mapping/
- https://ahrefs.com/blog/keyword-clustering/

Ahrefs groups same/similar-intent keywords into one topic/page and explicitly warns that similar variants generally do not need separate pages. Its mapping action model distinguishes Create, Optimize and No action. It also treats secondary keywords/subtopics as content that often belongs inside the same page instead of on standalone URLs.

### Semrush 2026 — cannibalization boundary

Source: https://www.semrush.com/blog/keyword-cannibalization-guide/
Published: 2026-07-14.

Semrush defines keyword cannibalization as multiple pages targeting the same keyword(s) **and harming each other's search visibility**. This supports keeping the harm/conflict verdict outside Step 12. Structural similarity can be identified now; harmful competition must be proved later.

## Proposed job-specific structural-action taxonomy

The exact labels below are **PROJECT-SPECIFIC**. External sources support the underlying mechanics, not these exact names.

### `KEEP_EXISTING_STRUCTURE`

Use when a current owner exists, the page already truthfully serves the stable user task, and no material structural/content gap requires a different document or major new layer.

Why: Ahrefs `No action`; Yandex user-need fit.

### `EXPAND_EXISTING_PAGE`

Use when the existing owner is the correct page for the same user task but material member-phrase needs are under-covered and should be added to that page rather than split into a new URL.

Why: Ahrefs/Semrush `Optimize`; same-intent terms belong together.

### `ADD_SECTION_OR_FAQ_TO_EXISTING`

Use when the cluster/task is a subordinate subtopic/question of an existing owner and is useful but not independently strong enough to justify a standalone page.

Why: Ahrefs secondary-keyword/subtopic model; Yandex warning against low-value/low-demand or duplicate pages.

### `NEW_COMMERCIAL_PAGE`

Use only when all are true:

1. stable distinct commercial/service terminal task;
2. task is in scope for the business;
3. no current page truthfully owns it;
4. the task is not merely a modifier/subquestion of an existing page;
5. there is enough real product/service information and conversion outcome to create a useful standalone document;
6. proposed parent/child/internal-link placement is explicit.

### `NEW_INFORMATIONAL_PAGE`

Same as above, but terminal result is information/selection/DIY/legal/reference rather than transaction/service order.

The page must have enough independent informational value to satisfy the task instead of being search-engine-first thin content.

### `SPLIT_EXISTING_PAGE`

Use when one current document is structurally carrying two or more materially different major logical/user-task units that each independently justify their own page.

Do not split for a small modifier, FAQ, paragraph, price variation or city token alone.

### `MERGE_STRUCTURALLY_REDUNDANT_PAGES`

Use only when current first-party pages are sufficiently duplicate/redundant in user task/content that one document can truthfully own the whole task and separate URLs provide no clear user/architecture benefit.

This is **not** a cannibalization verdict. If the only argument is overlapping rankings/queries or suspected visibility competition, defer that conclusion to Step 13.

### `NO_STANDALONE_PAGE`

Use when an in-scope cluster has no suitable current owner but still does not justify its own page: too subordinate, too thin, insufficiently distinct, or more correctly handled within another page/content module. Reason must state where the useful part belongs, or why no publication action is justified.

### `OUTSIDE_SCOPE_NO_ACTION`

Use for Step-11 `OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP` tasks unless the frozen client/business scope changes.

### `DEFER_UNRESOLVED`

Used only for the separate 19-row `SEARCH_REQUIRED` handoff. No URL/page action is assigned until the semantic task is resolved.

## Decision sequence for execution

For each effective assigned cluster:

```text
1. READ ALL MEMBER PHRASES FROM STEP_11_PHRASE_PAGE_MAP
2. CONFIRM EFFECTIVE TASK / INTENT / BUSINESS FIT
3. READ STEP_11 OWNER STATE + CURRENT PAGE EVIDENCE
4. IF OUTSIDE SCOPE -> OUTSIDE_SCOPE_NO_ACTION
5. IF OWNER EXISTS:
      a. does current page already satisfy the stable task? -> KEEP candidate
      b. same task but material coverage gap? -> EXPAND candidate
      c. subordinate subtopic only? -> SECTION/FAQ candidate
      d. current document mixes independently justified major tasks? -> SPLIT candidate
      e. structurally redundant existing documents? -> MERGE candidate
6. IF NO SUITABLE OWNER:
      a. distinct standalone task + sufficient useful content + business fit? -> NEW PAGE candidate
      b. subordinate useful subtopic? -> SECTION/FAQ candidate
      c. otherwise -> NO_STANDALONE_PAGE candidate
7. ADVERSARIAL CHECK AGAINST ALL MEMBER PHRASES
8. RECORD EVIDENCE, COUNTER-EVIDENCE, WHY ALTERNATIVES WERE REJECTED
9. ROLL UP CLUSTER ACTIONS TO PAGE-LEVEL ACTION MAP
```

No universal numeric SERP-overlap, search-volume, phrase-count or page-count threshold is introduced. If such a threshold becomes necessary, it must be researched/traced before use.

## Bridge / Codex plan for Step 12

### Pre-step review

```text
BRIDGE_REQUIRED = NO
NEW_PROVIDER_REQUESTS = 0
NEW_PROVIDER_COST = 0 RUB
```

### Execution

Default input is the frozen Step-11 phrase/page evidence plus current first-party pages already read.

```text
BRIDGE_CONDITIONAL = true
```

Use Yandex Search through Bridge only if a **specific unresolved structural boundary** cannot be decided from current semantic/task/page evidence and direct current Search evidence would change the action. A separate owner-visible YMB mode/objective/request/cost/storage/completeness gate is mandatory before such a call.

If Codex or another site-reading pass is used to refresh pages, every acquisition result follows the Step-11 durability rule: immediate GitHub save + readback before the next acquisition interaction.

## Proposed Step-12 outputs after authorization

```text
STEP_12_STRUCTURAL_ACTIONS.tsv
STEP_12_PAGE_ACTION_ROLLUP.tsv
STEP_12_SEARCH_REQUIRED_HANDOFF.tsv
STEP_12_QA.json
STEP_12_REPORT.md
```

Expected primary action ledger fields:

```text
cluster_id
assigned_phrase_count
user_task
intent_type
business_fit
step11_ownership_state
current_owner_url
structural_action
proposed_target_or_new_page
parent_page_or_section
reason
evidence_for
evidence_against
alternative_rejected
confidence
step13_followup_required
```

## Proposed PASS gate

Step 12 may pass only when:

```text
EFFECTIVE_ASSIGNED_CLUSTERS_ACCOUNTED = 75/75
SEARCH_REQUIRED_ROWS_PRESERVED = 19/19
SILENT_CLUSTER_DROPS = 0
STRUCTURAL_ACTION_WITHOUT_REASON = 0
STRUCTURAL_ACTION_WITHOUT_PHRASE_LEVEL_TRACE = 0
NEW_PAGE_FROM_MODIFIER_ONLY = 0
NEW_PAGE_WITHOUT_DISTINCT_STABLE_TASK = 0
NEW_PAGE_WITHOUT_USEFUL_CONTENT_RATIONALE = 0
NO_SUITABLE_EXISTING_PAGE_AUTO_CREATE = 0
OWNER_EXISTING_AUTO_KEEP_WITHOUT_GAP_REVIEW = 0
SPLIT_WITHOUT_MAJOR_LOGICAL_TASK_BOUNDARY = 0
MERGE_BASED_ONLY_ON_SUSPECTED_CANNIBALIZATION = 0
SEARCH_REQUIRED_WITH_STRUCTURAL_ACTION = 0
OUTSIDE_SCOPE_NEW_PAGE_ACTIONS = 0
PREMATURE_STEP13_CANNIBALIZATION_VERDICTS = 0
PREMATURE_STEP14_ARCHITECTURE_FREEZE = 0
AI_EVIDENCE_USED_IN_STEP12 = 0
FINAL_ARTIFACTS_PRESERVED_AND_READ_BACK = true
```

If any provider/Codex acquisition occurs during execution, add provider/result/cost/persistence reconciliation to the PASS gate.

## Adversarial method review

The proposed method was challenged against these failure modes:

- **one cluster = one page** — rejected; same-intent subtopics can belong inside a page;
- **no owner = create** — rejected;
- **existing owner = keep** — rejected; existing page can require expansion or structural split;
- **different modifier = separate page** — rejected;
- **multiple URLs = merge/cannibalization** — rejected;
- **low phrase count = no page** — rejected as universal rule;
- **high phrase count = page required** — rejected as universal rule;
- **commercial package limit of 15 = force internal architecture to 15** — rejected; client-facing compression happens later;
- **AI search evidence used now** — rejected; AI remains Steps 15–17;
- **19 unresolved phrases forced onto pages** — rejected.

Method verdict before execution:

```text
CURRENT_RESEARCH_COMPLETE = true
SOURCE_TO_METHOD_TRACE_COMPLETE = true
UNSUPPORTED_NUMERIC_THRESHOLDS = 0
NON_EXECUTABLE_EVIDENCE_ROUTES = 0
PROJECT_SPECIFIC_TAXONOMY_LABELLED = true
STEP12_EXECUTION_AUTHORIZED = false
STEP12_STRUCTURAL_ACTIONS_ASSIGNED = 0
```

## ПРОСТЫМИ СЛОВАМИ

### Зачем нужен этот шаг

Чтобы понять, **что именно менять на сайте по каждой группе похожих поисков людей**. После прошлого шага мы уже знаем, какие запросы относятся к каким темам и какая нынешняя страница подходит или не подходит. Теперь надо решить, что с этим делать на самом сайте.

### Что конкретно будем делать

Для каждой группы запросов посмотрим все входящие в неё фразы и текущие страницы сайта. Затем выберем понятное действие: оставить страницу как есть, дополнить её, добавить отдельный раздел на существующей странице, сделать новую страницу, разделить слишком разную по смыслу страницу или объединить действительно дублирующие страницы. Если отдельная страница не нужна, так и зафиксируем — создавать страницу только ради поисковой фразы не будем.

### Что получим в конце

Получим **понятный список изменений сайта**: какие страницы оставить, какие дополнить, какие новые страницы действительно нужны, а какие создавать не стоит. Это станет основой для следующей проверки и затем для финального плана работ для клиента.

## Owner authorization gate

The current user instruction `Начинай 12` authorizes starting Step-12 pre-step work. Under the owner-locked pre-step gate it does not bypass the requirement to present the newly researched method before structural execution.

Next allowed transition after this review is explicit owner authorization to execute the structural-action ledger under the method above.
