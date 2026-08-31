# Step 13 — corrected pre-step methodology research and owner review

Date: 2026-08-31  
Status: **PRE-STEP REVIEW CORRECTED / EXECUTION NOT STARTED / AWAITING EXPLICIT OWNER AUTHORIZATION AFTER THIS REVIEW**

Job: `OKNO_MSK`  
Step: 13 — competing-page / cannibalization diagnosis

## PROCESS CORRECTION — why the previous pre-step review did not pass

The first Step-13 pre-step review contained the method research, completed/remaining lists, sources, risks and pass gate, but it omitted two owner-facing elements required by `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`:

1. one continuous full-roadmap view from job start through final close;
2. the mandatory ordinary-language summary at the end of the pre-step review.

Therefore:

```text
PREVIOUS_STEP13_METHOD_RESEARCH = PRESERVED AS EVIDENCE
PREVIOUS_OWNER_COMMUNICATION_GATE = FAILED
PREVIOUS_STEP13_EXECUTION_AUTHORIZATION_GATE = NOT SATISFIED
STEP13_PROVIDER_CALLS = 0
STEP13_EXECUTION_STARTED = false
```

The research is not discarded, but it cannot authorize execution until the corrected owner-facing review below is presented and the owner explicitly authorizes execution after seeing it.

---

# A. GOAL OF THE WHOLE KWORK

Build a trustworthy semantic and page architecture for `okno-msk.ru` for ordinary Yandex Search, then investigate selected AI-search cases, compare classic Search and AI evidence, prioritize changes and deliver a client-facing action plan.

The final client should understand:

- which current pages should answer which real search needs;
- which page/content changes are justified;
- where pages genuinely compete or overlap;
- what should be implemented first;
- where evidence is strong, weak or unavailable.

---

# B. FULL KWORK ROADMAP WITH CURRENT PROGRESS

| Stage | What this stage does in ordinary language | Status |
|---|---|---|
| 0. Scope freeze | Fix what business, site, region and deliverables we are actually analyzing | ✅ COMPLETE |
| 1. Existing-site discovery | Understand what pages/services/content already exist | ✅ COMPLETE |
| 2. Demand-probe plan | Decide what search-demand directions to measure | ✅ COMPLETE |
| 3. Historical first acquisition | Original incomplete Wordstat collection approach | 🔁 SUPERSEDED |
| 3R. Repaired acquisition | Recollect/preserve the complete reusable demand dataset | ✅ COMPLETE |
| 4. Family triage | Separate obvious noise and unresolved demand families | ✅ COMPLETE |
| 5. Targeted demand expansion | Fill important demand-coverage gaps | ✅ COMPLETE |
| 6. Demand dynamics | Preserve seasonality/demand context | ✅ COMPLETE / PRESERVED |
| 6A. Coverage revalidation | Verify that no additional Wordstat acquisition is currently required | ✅ COMPLETE |
| 7. Phrase-level cleanup | Decide phrase by phrase what stays, leaves scope or remains uncertain | ✅ COMPLETE AFTER CORRECTION |
| 8. Search-stage freeze | Freeze the exact set that can proceed to ordinary Yandex Search | ✅ COMPLETE AFTER CORRECTION |
| 9. Ordinary Yandex Search evidence | Collect bounded real search-result evidence for unresolved boundaries | ✅ COMPLETE AFTER CORRECTIONS |
| 10. User-task grouping | Group phrases that truly represent the same user task | ✅ COMPLETE |
| 11. Page ownership | Decide which current page should answer each task where possible | ✅ COMPLETE AFTER AUDIT/CORRECTION |
| 12. Structural actions | Decide what page roles/content should stay, change, route or defer | ✅ COMPLETE AFTER D12-28..D12-30 REVALIDATION |
| **13. Competing-page diagnosis** | **Check whether pages really compete for the same search task or normally coexist** | **🟡 CURRENT — METHOD REVIEW COMPLETE, EXECUTION NOT STARTED** |
| 14. Search architecture freeze | Freeze the final classic-Search page architecture after Step 13 | ⬜ NOT STARTED |
| 15. AI-case selection | Choose only cases where AI-search evidence can change a decision | ⬜ NOT STARTED |
| 16. AI-search evidence | Collect selected Alice/GenSearch evidence | ⬜ NOT STARTED |
| 17. Search-vs-AI comparison | Compare classic Yandex Search and AI-search behavior | ⬜ NOT STARTED |
| 18. Prioritization | Rank changes by value, confidence and effort | ⬜ NOT STARTED |
| 19. Client deliverables | Build the client-facing workbook/report/action map | ⬜ NOT STARTED |
| 20. Final QA | Reconcile evidence, numbers, URLs and recommendations | ⬜ NOT STARTED |
| 21. Handoff/revisions | Deliver the result and process allowed revisions | ⬜ NOT STARTED |
| 22. Job close | Close the job only after handoff/revisions are finished | ⬜ NOT STARTED |

---

# C. WORK ALREADY COMPLETED ACROSS THE WHOLE JOB

In ordinary language:

- the business/site scope is frozen;
- the current public site has been inventoried;
- demand evidence has been collected and repaired where the first collection was incomplete;
- 2,332 active phrases have been carried through phrase-level analysis without silent loss;
- phrases have been grouped by real user task rather than by surface wording alone;
- current page ownership has been mapped;
- Step 12 has been fully reworked after repeated audits so page actions are now based on current page evidence rather than actions proving themselves;
- Step 12 finished with 168 structural units and a complete 2,332-row phrase/action map;
- 195 page-pair candidates were handed to Step 13 as a broad investigation universe;
- Step 13 itself has **not** executed any Yandex provider calls yet.

Current Step-12 handoff facts:

```text
STEP12_FINAL_PHRASE_ROWS = 2332
STEP12_FINAL_STRUCTURAL_UNITS = 168
STEP13_INPUT_PAIR_UNIVERSE = 195
STEP12_FLAGGED_FOR_FUTURE_STEP13_REVIEW = 186
STEP13_DEPENDENCY_UNITS = 98
STEP13_PROVIDER_CALLS_SO_FAR = 0
```

---

# D. WORK STILL REMAINING

1. Complete Step 13 competing-page diagnosis.
2. Freeze the final ordinary-Search architecture in Step 14.
3. Select only decision-relevant AI cases.
4. Collect selected AI-search evidence.
5. Compare Search and AI evidence.
6. Prioritize implementation actions.
7. Produce the client-facing deliverables.
8. Run final QA.
9. Deliver and process revisions/handoff.
10. Close the job only after delivery/revisions are complete.

---

# E. GOAL OF THE CURRENT STEP

Determine, for every Step-12 page relationship, whether the two pages:

- answer genuinely different needs and should coexist;
- are a normal parent/child or supporting relationship;
- show a current search-ownership warning signal;
- probably compete for the same search need;
- are true duplicate/near-duplicate candidates;
- or cannot be judged strongly with the evidence available.

The goal is **not** to find as many conflicts as possible. The goal is to avoid both false conflicts and missed real conflicts.

---

# F. WHAT THIS STEP SOLVES

Step 12 intentionally handed forward a broad list of 195 page pairs. A pair only means "these pages are related enough to inspect later". It does **not** mean they compete.

Step 13 solves that uncertainty by checking the actual user task, current pages and Yandex Search evidence before any conflict conclusion.

---

# G. REQUIRED OUTPUT OF STEP 13

At completion we must have:

```text
STEP_13_PAIR_ELIGIBILITY.tsv
STEP_13_QUERY_FAMILY_CASES.tsv
STEP_13_CURRENT_PAGE_EVIDENCE.tsv
STEP_13_EXISTING_SEARCH_EVIDENCE.tsv
STEP_13_SEARCH_MANIFEST.tsv              # only if fresh Search is really required
STEP_13_SEARCH_RESULTS.tsv               # only if provider actually executes
STEP_13_CONFLICT_DIAGNOSIS.tsv
STEP_13_REMEDIATION_RECOMMENDATIONS.tsv
STEP_13_QA.json
STEP_13_QA_FINDINGS.tsv
STEP_13_REPORT.md
STEP_13_ACCEPTANCE_2026-08-31.md
```

Every one of the 195 input pairs must be accounted for directly or through a query-family case that references the original pair IDs.

---

# RELEVANT PRIOR ERRORS / WHAT FAILED BEFORE

The rules and Step-12 history show several failure patterns that are directly relevant here:

1. A relationship in our own graph is not proof that Search sees a conflict.
2. Two related URLs do not automatically mean cannibalization.
3. A target URL differing from the URL Yandex chooses is a warning signal, not automatically a defect.
4. One current search-result snapshot cannot prove long-term traffic harm or repeated URL swapping.
5. The same logic that proposes a conflict may not be the only logic that verifies it.
6. Checking only known bad examples is not enough; the full declared Step-13 universe must reconcile.

Root failure pattern to prevent:

```text
OUR INTERNAL RELATIONSHIP
→ SUSPECTED CONFLICT
→ OUR OWN DERIVED STATE USED AS PROOF
→ FALSE CERTAINTY
```

---

# NON-REPEAT CONTROL FOR STEP 13

Mandatory causal order:

```text
195 PAIR CANDIDATES
→ READ CURRENT PAGE/TASK EVIDENCE
→ DECIDE IF THE SAME REAL SEARCH NEED CAN EXPECT BOTH URLS
→ CLOSE OBVIOUS NORMAL RELATIONSHIPS WITHOUT SEARCH
→ GROUP SURVIVORS BY QUERY FAMILY × URL SET
→ REUSE SAVED STEP-9/11 SEARCH EVIDENCE
→ ONLY THEN DECIDE IF NEW SEARCH IS NECESSARY
→ OBSERVE SEARCH OWNERSHIP SIGNALS
→ ASSIGN EVIDENCE-STRENGTH VERDICT
→ ONLY THEN RECOMMEND REMEDIATION
→ INDEPENDENTLY RECOMPUTE / CHALLENGE VERDICTS
→ SAVE DIAGNOSTICS
→ GITHUB READBACK
→ COMPLETE
```

No final verdict may use its own label as evidence.

---

# METHOD SOURCES CHECKED

Official Yandex sources:

- Duplicate/similar pages and how Yandex can group/select them: https://yandex.ru/support/webmaster/ru/robot-workings/double
- Extended query-by-URL analytics (`date × URL × query × region × clicks × impressions × position`): https://yandex.ru/support/webmaster/ru/service/queries-export
- Query monitoring by URL/query: https://yandex.ru/support/webmaster/ru/service/popular-queries
- Search-query analytics: https://yandex.ru/support/webmaster/ru/service/queries-analytic

Current industry methodology:

- Semrush, *Keyword Cannibalization Guide* (2026): https://www.semrush.com/blog/keyword-cannibalization-guide/
- Ahrefs, *How to Increase Organic Traffic* (2026 update): https://ahrefs.com/blog/how-to-increase-organic-traffic/
- Ahrefs, *Keyword Intent*: https://ahrefs.com/blog/keyword-intent/
- Ahrefs, *Keyword Cannibalization*: https://ahrefs.com/blog/keyword-cannibalization/
- Topvisor, target vs relevant URL and relevant-URL history: https://topvisor.com/ru/support/rankings/target-url/

What these sources support:

```text
MULTIPLE RELATED URLS != AUTOMATIC CANNIBALIZATION
SAME / VERY SIMILAR SEARCH INTENT IS REQUIRED FOR A STRONG CONFLICT THEORY
CURRENT MULTI-URL VISIBILITY OR TARGET/RELEVANT MISMATCH IS A SIGNAL, NOT AUTOMATIC HARM
HISTORY / QUERY×URL PERFORMANCE IS STRONGER THAN ONE SNAPSHOT
REMEDIATION DEPENDS ON THE TYPE AND STRENGTH OF THE CONFLICT
```

Project-specific choice:

The exact verdict labels used below are a fail-closed KW-001 taxonomy; they are not claimed as official Yandex terminology.

---

# HOW STEP 13 WILL BE DONE

## 1. Freeze 195/195 input pairs
No pair may silently disappear.

## 2. Read unique current URLs once
Deduplicate page reads rather than opening the same page for every pair.

## 3. Close obvious normal relationships before Search
Compare page object, user task, intent, member phrases and parent/supporting roles.

If the same real search need would not reasonably expect both pages as alternative primary answers, close the pair as normal without spending a Search request.

## 4. Convert surviving pairs into query-family cases
The real investigation unit is:

```text
QUERY FAMILY × CANDIDATE URL SET
```

not merely `PAGE A × PAGE B`.

## 5. Reuse existing Yandex Search evidence first
Join existing Step-9/11 evidence before any new provider acquisition.

## 6. Build a fresh Search manifest only for unresolved material cases
A Step-12 `future_search_check=true` marker does not automatically authorize a new Search request.

## 7. If fresh Search is needed, use ordinary Yandex Search only
No GenSearch/Alice calls belong in Step 13.

## 8. Assign evidence-strength verdict
Allowed project verdicts include normal coexistence, current mismatch/multi-URL signal, probable ownership conflict, duplicate/near-duplicate conflict, or insufficient evidence.

One public SERP snapshot cannot be labelled `CONFIRMED_HARMFUL_CANNIBALIZATION`.

## 9. Recommend remediation only after the verdict
No automatic merge/redirect/noindex merely because two pages overlap in wording.

## 10. Independent QA + durable readback
QA must be capable of overturning a proposed conflict and must independently reconcile 195/195 inputs.

---

# SELF-AUDIT FINDINGS

- The 195-pair universe is deliberately overinclusive and therefore must be filtered before Search.
- Historical shared-cluster provenance is useful for discovery but is not conflict evidence.
- The base rehearsal has no Webmaster/Metrika account access, so some harmful-cannibalization claims are impossible to prove strongly here.
- Public Search can prove current selection/multi-URL signals, not historical performance harm by itself.
- Strong uncertainty must remain uncertainty rather than being upgraded to a dramatic SEO conclusion.

Review verdict:

```text
SUPPORTED_WITH_PROJECT_SPECIFIC_FAIL_CLOSED_VERDICT_TAXONOMY
```

---

# RISKS / UNCERTAINTIES

- rankings vary by time, region and other conditions;
- mixed-intent search results can legitimately show different page types;
- related pages can rank for different long-tail needs while sharing a broad head term;
- current public Search is a snapshot;
- without private Webmaster/Metrika history, some cases must remain probable/insufficient rather than confirmed harmful conflicts.

---

# WHAT WE WILL NOT DO YET

```text
NO GenSearch / Alice calls
NO Step-14 architecture freeze
NO automatic merge/redirect/noindex from keyword overlap
NO confirmed harmful-cannibalization claim from one public Search snapshot
NO fresh Search for all 186 flagged pairs by default
NO claims from Webmaster/Metrika data we do not have
```

---

# YMB GATE IF FRESH SEARCH BECOMES NECESSARY

```text
YMB STEP OBJECTIVE
= collect complete ordinary Yandex Search evidence only for surviving material query-family cases whose page ownership remains unresolved after current-page and saved-evidence review.

YMB REQUIRED MODE
= Active service: SEARCH
= ordinary search / search_batch only
= no GenSearch
= current accepted Moscow-region configuration

YMB REQUIRED SAVED RESULT
= complete bounded ranked result page for every selected query + request identity/outcome/cost + normalized target-domain URL/rank evidence.

YMB COMPLETENESS CHECK
= planned queries == accounted outcomes; complete returned rows saved for every successful query; returned/saved counts reconcile; evidence is readable from GitHub before any next provider interaction.

YMB STOP CONDITION
= incomplete/unsaved/unreadable/OUTCOME_UNKNOWN result or count mismatch → STOP immediately.

YMB_INTERACTION_GATE_EMBEDDED = true
YMB_PROJECT_RESULT_DEFINED = true
YMB_REQUIRED_STORAGE_DEFINED = true
YMB_COMPLETENESS_CHECK_DEFINED = true
YMB_STOP_ON_INCOMPLETE_RESULT = true
```

---

# PROPOSED PASS CONDITION

Step 13 can pass only when:

```text
195/195 INPUT PAIRS ACCOUNTED
SILENT PAIR DROPS = 0
ALL MATERIAL CASES HAVE CURRENT PAGE/TASK EVIDENCE
SURVIVING PAIRS MAP TO EXPLICIT QUERY-FAMILY CASES
NORMAL RELATIONSHIPS ARE CLOSED WITHOUT UNNECESSARY SEARCH
SAVED SEARCH EVIDENCE IS REUSED BEFORE FRESH SEARCH
IF SEARCH EXECUTED: PLANNED/EXECUTED/RETURNED/SAVED/VERIFIED COUNTS RECONCILE
STRONG VERDICT FROM ONE SNAPSHOT = 0
DESTRUCTIVE REMEDIATION WITHOUT QUALIFYING EVIDENCE = 0
EVERY VERDICT HAS CAUSALLY UPSTREAM EVIDENCE
INDEPENDENT QA FINDINGS = 0
FINAL GITHUB READBACK = PASS
STEP14_EXECUTED = false
```

---

# ПРОСТЫМИ СЛОВАМИ

## Зачем нужен этот шаг

У сайта есть много связанных страниц. Например, есть общая страница про алюминиевые окна и отдельные страницы про раздвижные или распашные окна. Сам факт, что они похожи по теме, ещё не означает проблему.

Этот шаг нужен, чтобы понять, **где страницы нормально дополняют друг друга, а где две страницы действительно пытаются отвечать на один и тот же запрос и мешают поисковику понять, какую из них показывать**.

## Что конкретно будем делать

Сначала возьмём все 195 подозрительных сочетаний страниц и отсеем очевидно нормальные случаи: например, общая страница и её узкая дочерняя страница, если они отвечают на разные вопросы.

Для оставшихся случаев посмотрим, какие реальные запросы относятся к обеим страницам, что сейчас написано на самих страницах и какую страницу Яндекс уже выбирал в сохранённых результатах поиска.

Только если после этого всё ещё будет непонятно, какая страница должна отвечать на запрос, сделаем ограниченные новые проверки в Яндексе. Мы **не будем запускать поиск для всех 195 пар просто потому, что они попали в список**.

## Что получим в конце

Получим понятный список:

- какие страницы оставить как есть в структуре, потому что они решают разные задачи;
- где нужно чётче развести смысл двух страниц;
- где есть реальный признак того, что Яндекс путается между страницами;
- где страницы действительно выглядят как дубли или конкуренты;
- где данных пока недостаточно и нельзя честно делать сильный вывод.

После этого можно будет безопасно перейти к следующему шагу и зафиксировать окончательную структуру страниц для обычного поиска Яндекса.

---

```text
PLAIN_LANGUAGE_SUMMARY_PRESENT = true
FULL_ROADMAP_PRESENT = true
OWNER_COMMUNICATION_GATE = READY_FOR_OWNER_REVIEW
STEP13_EXECUTION_STARTED = false
STEP13_PROVIDER_CALLS = 0
WAITING_FOR_EXPLICIT_OWNER_AUTHORIZATION_AFTER_THIS_CORRECTED_REVIEW = true
```
