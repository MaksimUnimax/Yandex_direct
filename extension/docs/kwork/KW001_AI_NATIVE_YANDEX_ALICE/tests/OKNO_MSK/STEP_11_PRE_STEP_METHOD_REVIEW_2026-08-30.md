# KW-001 / OKNO-MSK — STEP 11 PRE-STEP METHOD REVIEW

Date: 2026-08-30  
Status: **PRE-STEP RESEARCH COMPLETE / OWNER-FACING METHOD READY / EXECUTION NOT STARTED**

Pre-step base HEAD:

```text
0125f6349000006d39fe4b85c31b0aa09ad9a1dd
```

Current Step-11 permanent-method status in `STEP_RULES_INDEX.md`:

```text
STEP_11_PERMANENT_METHOD = UNVALIDATED
```

This file is job-specific. It records the researched Step-11 method for the current OKNO-MSK execution. It does not silently promote the method to the universal layer.

---

## 1. Whole Kwork goal

Deliver an evidence-backed semantic set and site/page structure recommendation for Yandex ordinary Search plus selective Yandex AI-search evidence, followed by client-ready artifacts and final QA.

Completed upstream work relevant to Step 11:

```text
Step 01 site/business discovery = COMPLETE
Step 08 Search-stage semantic freeze = COMPLETE
Step 09 ordinary Yandex Search evidence = COMPLETE
Step 10 user-task clustering = COMPLETE / VERIFIED
```

Step-10 final truth:

```text
SOURCE_ROWS = 2840
ACTIVE_ROWS = 2332
FINAL_ASSIGNED_ACTIVE_ROWS = 2319
FINAL_SEARCH_REQUIRED_ACTIVE_ROWS = 13
FINAL_ACTIVE_CLUSTERS = 59
FINAL_ZERO_MEMBER_ACTIVE_CLUSTERS = 0
```

---

## 2. Step-11 goal

For every final active Step-10 cluster, determine whether the current public site has an existing page that can truthfully own that user task.

The Step-11 question is:

```text
FOR THIS USER-TASK CLUSTER,
WHICH EXISTING CURRENT PAGE, IF ANY,
IS THE BEST EVIDENCE-BACKED OWNER?
```

Step 11 bridges:

```text
USER TASK / CLUSTER
-> EXISTING SITE PAGE OWNERSHIP
```

It does **not** yet decide what structural action should be taken if ownership is weak or absent.

---

## 3. Exact required output

The Step-11 final ownership ledger must account for all 59 active clusters and preserve at minimum:

```text
CLUSTER_ID
CLUSTER_USER_TASK
BUSINESS_FIT
CANDIDATE_URLS
CANDIDATE_PAGE_PROFILE_EVIDENCE
EXACT_SEARCH / WEBMASTER EVIDENCE IF USED
PRIMARY_OWNER_URL IF RESOLVED
OWNERSHIP_STATE
OWNERSHIP_CONFIDENCE
CONTRADICTIONS / UNCERTAINTY
EVIDENCE_PROVENANCE
LAST_VERIFIED
```

Allowed job-specific ownership states:

```text
OWNER_EXISTING
NO_SUITABLE_EXISTING_PAGE
OWNER_UNRESOLVED_EVIDENCE_REQUIRED
OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP
```

The 13 Step-10 `SEARCH_REQUIRED` phrases are not clusters and therefore receive a separate handoff state:

```text
UNCLUSTERED_SEARCH_REQUIRED / PAGE_OWNERSHIP_NOT_APPLICABLE_UNTIL_TASK_RESOLVED
```

They must not be silently attached to an existing page.

---

## 4. What Step 11 does NOT decide

Step 11 does not make Step-12 or Step-13 decisions prematurely.

Not decided here:

```text
CREATE PAGE
DELETE PAGE
MERGE PAGES
SPLIT PAGE
EXPAND PAGE
KEEP AS-IS
FINAL INFORMATION ARCHITECTURE
CANNIBALIZATION DIAGNOSIS
```

If no existing page fits, Step 11 records:

```text
NO_SUITABLE_EXISTING_PAGE
```

Step 12 later decides the structural action.

If several existing URLs are visible/ranking for a task, Step 11 does not automatically call that cannibalization. Step 13 owns that diagnosis.

---

## 5. Prior errors and non-repeat controls

### Error risk A — found URL treated as read page

Prior Step-01 lesson:

```text
FOUND URL != READ PAGE
```

Control:

```text
OWNER_EXISTING requires a current Step-11 page read/profile.
A stale Step-01 inventory row, slug, title or link discovery is insufficient by itself.
```

### Error risk B — lexical URL/title match treated as ownership

Control:

```text
LEXICAL_MATCH != PAGE_OWNERSHIP
```

Ownership must compare the cluster's user task and expected terminal result with the actual page's current purpose/content.

### Error risk C — ranking URL treated as automatic intended owner

Yandex provides query-to-URL behavior evidence, but a displayed/ranking URL is observed Search behavior, not automatic analytical ownership truth.

Control:

```text
RANKING_URL = EVIDENCE
RANKING_URL != AUTOMATIC_OWNER
```

### Error risk D — multiple URLs treated as immediate cannibalization

Control:

```text
MULTIPLE_URLS_VISIBLE != CANNIBALIZATION_PROVEN
```

Step 11 may use multi-URL behavior to mark an ownership conflict. Step 13 diagnoses cannibalization.

### Error risk E — no Search visibility treated as no suitable page

Control:

```text
NOT_VISIBLE_IN_CURRENT_SEARCH != NO_SUITABLE_EXISTING_PAGE
```

Page suitability is first evaluated from current page content/task fit. Search evidence can strengthen or contradict that conclusion.

### Error risk F — unresolved cluster forced onto a convenient URL

Control:

```text
UNCERTAINTY -> OWNER_UNRESOLVED_EVIDENCE_REQUIRED
```

Do not manufacture certainty to obtain 59 nominal URL assignments.

---

## 6. Fresh external method research

### 6.1 Yandex Webmaster — advanced query analytics by URL

Source:

https://yandex.ru/support/webmaster/ru/service/queries-export

Direct support:

- report contains `URL + query + region + clicks + impressions + position`;
- Yandex explicitly describes this report as helping check whether pages shown in Search match the meaning of a query;
- reports can be filtered by URL, region and dates.

Method consequence:

```text
QUERY<->URL WEBMASTER DATA = STRONG OWNED SEARCH-BEHAVIOR EVIDENCE
```

It may adjudicate ambiguous ownership when available, but it still does not replace reading the page.

### 6.2 Yandex Webmaster — query monitoring / URL view

Source:

https://yandex.ru/support/webmaster/ru/service/popular-queries

Direct support:

- data is grouped by queries and URLs;
- query view exposes a high-impression URL for the query;
- URL view exposes queries for which the URL was displayed;
- URL filters can isolate specific page groups.

Method consequence:

```text
CURRENT YANDEX QUERY<->URL ASSOCIATION CAN BE OBSERVED DIRECTLY
```

### 6.3 Yandex Webmaster — search query and page statistics

Sources:

https://yandex.ru/support/webmaster/ru/service/statistics
https://yandex.ru/support/webmaster/ru/service/urls
https://yandex.ru/support/webmaster/ru/service/queries-analytic

Direct support:

- query statistics include impressions, clicks, CTR and average position;
- page statistics expose Search performance for current URLs;
- page/query reports can be used as owned evidence of how Yandex currently surfaces the site.

### 6.4 Semrush — current keyword mapping method

Source:

https://www.semrush.com/blog/keyword-mapping/

Research date observed: 2026-07-27.

Direct support:

- a keyword/intent cluster is mapped to the page that best satisfies its search intent;
- existing candidate URLs should be opened and checked rather than accepted from an automatic suggestion;
- if no suitable page exists, the map leaves the target URL unmatched / marks a content gap for later action.

Method consequence:

```text
CLUSTER->PAGE MATCH = INTENT/TASK FIT + CURRENT PAGE REVIEW
NO CLEAR MATCH = GAP / NO EXISTING OWNER
```

### 6.5 Ahrefs — keyword mapping

Source:

https://ahrefs.com/blog/keyword-mapping/

Direct support:

- keyword mapping groups same/similar-intent queries into topics and assigns those topics to pages;
- if an existing page covers the topic it may be mapped to that page;
- if it does not, the URL remains absent and a later create action may be considered.

### 6.6 Ahrefs — cannibalization caution

Source:

https://ahrefs.com/seo/glossary/keyword-cannibalization

Direct support:

- multiple pages ranking around a shared keyword do not automatically create a harmful cannibalization case;
- different intents can justify multiple pages;
- cannibalization should be addressed when materially similar pages compete for the same task/queries and the conflict is actually harmful.

Method consequence:

```text
MULTIPLE SEARCH URLS -> OWNERSHIP REVIEW SIGNAL
MULTIPLE SEARCH URLS != STEP11 CANNIBALIZATION VERDICT
```

---

## 7. Current-job page-research channel model

Step 01 already demonstrated that complementary discovery channels find different parts of the site.

Accepted Step-01 factual evidence:

```text
ChatGPT public-web OPENED_READ = 18
Codex Work OPENED_READ = 56
Codex desktop/app OPENED_READ = 5
UNION OPENED_READ URLs = 64
```

Observed complementary strengths:

```text
Codex Work -> deepest internal-family/template coverage
ChatGPT public web -> unique GEO / weakly exposed public-page coverage
Codex desktop -> navigation-taxonomy confirmation and local fetch/control evidence
```

For Step 11, this old inventory is a discovery baseline only. Page content must be refreshed before ownership acceptance.

### Channel A — Codex

Use Codex for scale and consistent page extraction:

```text
refresh the URL inventory;
open/fetch candidate pages in batches;
extract current URL/status/title/H1/headings/main content/CTA;
build structured page profiles;
flag redirects, template families, duplicate-looking pages and newly discovered internal URLs;
persist results to the job workspace.
```

Codex is an acquisition/extraction worker. It does not self-accept page ownership.

### Channel B — ChatGPT Work / Cloud Browser

Use Work for browser-grounded inspection where rendered behavior matters:

```text
open ambiguous candidate pages interactively;
inspect JS/dynamic visible content;
inspect navigation/context/forms/CTA;
check pages whose raw fetch and rendered meaning differ;
use Yandex Webmaster UI evidence when authenticated access is available and execution is authorized.
```

Work is especially useful for adjudicating ambiguous page purpose. In this current Instant-mode pre-step review, Work has not yet been executed.

### Channel C — ChatGPT public web

Use public web as an independent search-visible discovery/cross-check channel:

```text
find public URLs;
check externally discoverable page variants;
identify public pages missed by internal navigation/fetch passes;
cross-check current public exposure.
```

### Channel D — Yandex Marketing Bridge ordinary Search

Step-11 Bridge classification remains:

```text
BRIDGE_CONDITIONAL
```

Use existing exact Step-09 SERP evidence first.

New ordinary Search calls are reserved for unresolved material ownership boundaries where:

```text
two or more current pages remain plausible;
page-content evidence conflicts with observed Search behavior;
no existing evidence resolves a high-impact ownership question.
```

Do not run a blanket paid Search probe for every cluster merely because the Bridge exists.

Any new provider calls remain separately owner-authorized and cost-accounted.

### Channel E — Yandex Webmaster evidence

The current Bridge Webmaster slice reviewed at dialogue start exposes:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

It does not currently expose the new advanced query-by-URL report as a direct Bridge operation.

Therefore:

```text
CURRENT BRIDGE WEBMASTER != COMPLETE STEP11 QUERY<->URL TOOL
```

If query-by-URL Webmaster evidence is needed, use an available authorized Webmaster UI/API route (for example through Work) rather than pretending the current Bridge method exists.

---

## 8. Current page profile schema

Each plausible existing owner candidate must be represented by a current page profile.

Minimum fields:

```text
URL
CURRENT_REACHABLE_STATE
LAST_VERIFIED
PAGE_TYPE
PRIMARY_OBJECT
OBJECT_SCOPE
PRIMARY_USER_TASK
EXPECTED_TERMINAL_RESULT
INTENT_MODE
LIFECYCLE_STAGE
BUSINESS_FIT
TITLE
H1
MAIN_CONTENT_SUMMARY
CTA / CONVERSION_MODE
EXPLICIT_INCLUSIONS
EXPLICIT_EXCLUSIONS
SOURCE_CHANNELS
SEARCH / WEBMASTER EVIDENCE
CONTRADICTIONS / NOTES
```

A Step-01 historical page family can help generate candidates but cannot substitute for this profile.

---

## 9. Ownership decision method

### Stage 1 — freeze inputs

Freeze:

```text
59 final Step-10 active clusters;
13 Step-10 SEARCH_REQUIRED phrases as separate unresolved handoff;
Step-01 merged site inventory as discovery baseline;
Step-09 exact Search evidence;
current site/business scope.
```

### Stage 2 — refresh site/page evidence

Use complementary Codex / Work / public-web channels to refresh current public pages and create page profiles.

Required principle:

```text
CURRENT_PAGE_READ > HISTORICAL_DISCOVERY_ONLY
```

### Stage 3 — candidate generation

For each cluster, identify all plausible existing owner URLs from:

```text
current page profiles;
current site hierarchy/navigation;
known page families;
exact lexical/object signals as candidate-generation aids;
existing Search/Webmaster evidence.
```

Lexical signals may create candidates. They do not decide ownership by themselves.

### Stage 4 — task/profile matching

Compare the Step-10 cluster contract with every plausible candidate page profile across:

```text
PRIMARY USER TASK
PRIMARY OBJECT / SCOPE
EXPECTED TERMINAL RESULT
INTENT MODE
LIFECYCLE STAGE
BUSINESS FIT
PAGE TYPE
CURRENT MAIN CONTENT
CURRENT CTA / CONVERSION MODE
```

### Stage 5 — base ownership verdict

If exactly one page is the strongest compatible current page and no material contradictory evidence remains:

```text
OWNER_EXISTING
```

If plausible current candidates were inspected and none sufficiently matches the cluster task:

```text
NO_SUITABLE_EXISTING_PAGE
```

If two or more pages remain plausible, or page content conflicts with Search/Webmaster behavior:

```text
OWNER_UNRESOLVED_EVIDENCE_REQUIRED
```

For Step-10 outside-scope clusters:

```text
OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP
```

### Stage 6 — evidence escalation for unresolved ownership

Evidence order:

```text
1. CURRENT PAGE CONTENT / PAGE PROFILE
2. EXISTING EXACT STEP-09 SERP EVIDENCE
3. CURRENT YANDEX WEBMASTER QUERY<->URL / PAGE EVIDENCE WHEN AVAILABLE
4. TARGETED NEW ORDINARY SEARCH EVIDENCE WHEN MATERIAL AND OWNER-AUTHORIZED
5. OWNER/BUSINESS CLARIFICATION WHERE THE CONFLICT IS COMMERCIAL RATHER THAN SEARCH-OBSERVABLE
```

Do not escalate automatically merely because uncertainty exists. Escalate only when the evidence can materially resolve Step-11 ownership.

### Stage 7 — preserve legitimate many-cluster-to-one-page ownership

A single existing page may own multiple compatible Step-10 clusters.

```text
MULTIPLE CLUSTERS -> ONE PAGE
```

is not automatically a defect.

Step 12 later decides whether the architecture should remain consolidated or be split.

### Stage 8 — preserve multi-page conflict without premature Step-13 diagnosis

If multiple pages continue to compete for one cluster and no owner can be justified:

```text
OWNER_UNRESOLVED_EVIDENCE_REQUIRED
```

Do not label it `CANNIBALIZATION` in Step 11.

---

## 10. Handling the 13 unclustered SEARCH_REQUIRED phrases

Current unresolved phrases:

```text
6 6 с панорамными окнами
ral алюминиевых окон
rehau окна 2
rehau окна 80
алюминиевые окна 2
алюминиевый м окно
без алюминиевой окна
окон п 44 т
оконные блоки фурнитурой
остекление балкона работу
пластиковые двери 70
пластиковые окна домашние окна
пластиковые окна комарова
```

They are not Step-11 ownership rows because Step 10 did not establish a stable user-task cluster.

Step-11 handoff:

```text
UNCLUSTERED_SEARCH_REQUIRED
PAGE_OWNERSHIP_NOT_APPLICABLE_UNTIL_TASK_RESOLVED
```

A targeted Search check may be proposed only if resolving a phrase can materially affect page ownership/site architecture. No blind provider replay is authorized by this method review.

---

## 11. Source-to-method trace

| Method element | Source/evidence | Exact support | Current-job part | Executable action/output |
|---|---|---|---|---|
| Match query/task to page meaning | Yandex Webmaster advanced query-by-URL analytics | Yandex explicitly frames URL-query data as a way to check whether pages match query meaning | Cluster is the Step-10 task unit | Compare cluster task against current page profile and query↔URL evidence |
| Observe query↔URL relationships | Yandex Webmaster monitoring / URL views | Query and URL views expose which URLs appear for which queries | Use only when access/evidence exists | Add owned Search behavior to candidate-page ledger |
| Map clusters to existing pages | Semrush 2026 keyword mapping; Ahrefs keyword mapping | Intent/topic groups are assigned to the existing page that best satisfies the intent/topic | 59 current clusters | Produce one Step-11 ownership verdict per cluster |
| Read the actual page before acceptance | Semrush mapping + Step-01 project evidence | Automatic/suggested URL match must be opened and checked; prior job proved discovery channels are incomplete alone | Current pages may have changed since Step 01 | Current page profile required for `OWNER_EXISTING` |
| No suitable page remains a gap | Semrush/Ahrefs mapping | If no existing page fits, target URL remains unmatched / later content action is considered | Structural action belongs to Step 12 | Record `NO_SUITABLE_EXISTING_PAGE` only |
| Multiple URLs are not automatic cannibalization | Ahrefs cannibalization guidance | Different-intent pages may both rank legitimately | Step 13 exists separately | Preserve conflict/evidence without Step-13 verdict |
| Codex + Work + public web as complementary research | Step-01 merged project evidence | Different channels exposed different page families/coverage | Reuse same complementary acquisition model for current refresh | Merge current page evidence with channel provenance |
| Targeted Search escalation only when material | Project provider/cost discipline + Step-09 evidence rules | This is a project control, not claimed as an industry threshold | Bridge is conditional in Step 11 | Reuse Step-09 first; propose only unresolved high-value Search calls |
| Outside-scope clusters have no target page owner | Current Step-10 `business_fit=OUTSIDE` | Job-specific semantic state | Preserve final Step-10 truth | `OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP` |
| 13 SEARCH_REQUIRED phrases do not receive page owners | Current Step-10 final assignment | No stable task cluster exists | Job-specific unresolved handoff | Separate 13-row unresolved ledger |

Project-specific element classification:

```text
TARGETED_SEARCH_ESCALATION_POLICY = ANALYST_HEURISTIC / PROJECT CONTROL
OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP = CURRENT JOB RULE
13-ROW UNCLUSTERED HANDOFF = CURRENT JOB FACT
```

No claim is made that these are external industry standards.

---

## 12. Planned Step-11 artifacts after authorization

```text
STEP_11_PAGE_PROFILE_LEDGER.tsv
STEP_11_CLUSTER_PAGE_CANDIDATES.tsv
STEP_11_PAGE_OWNERSHIP.tsv
STEP_11_UNCLUSTERED_SEARCH_REQUIRED_HANDOFF.tsv
STEP_11_QA.json
STEP_11_REPORT.md
```

If Work/Codex produces intermediate raw/extraction evidence, preserve it separately with channel provenance rather than overwriting the final analytical ownership ledger.

---

## 13. Quantitative PASS gate

Step 11 can be called complete only when all applicable checks pass:

```text
FINAL_STEP10_CLUSTERS_ACCOUNTED = 59/59
UNCLUSTERED_SEARCH_REQUIRED_ACCOUNTED = 13/13
OWNER_EXISTING_WITHOUT_CURRENT_PAGE_READ = 0
LEXICAL_ONLY_OWNERSHIP_DECISIONS = 0
RANKING_URL_AUTOMATICALLY_EQUATED_TO_OWNER = 0
SEARCH_ABSENCE_AUTOMATICALLY_EQUATED_TO_NO_PAGE = 0
NO_SUITABLE_EXISTING_PAGE_WITHOUT_PLAUSIBLE_CANDIDATE_REVIEW = 0
UNRESOLVED_CASES_WITHOUT_EXECUTABLE_EVIDENCE_ROUTE = 0
DIRECT_SEARCH_EVIDENCE_TRANSFER_TO_UNPROBED_NEIGHBOURS = 0
PREMATURE_STEP12_STRUCTURAL_ACTIONS = 0
PREMATURE_STEP13_CANNIBALIZATION_VERDICTS = 0
SILENT_CLUSTER_DROPS = 0
PROVIDER_REQUESTS_RECONCILE = true if provider used
PROVIDER_COST_RECONCILES = true if provider used
FINAL_OUTPUT_PRESERVED_AND_READ_BACK = true
```

Final transition marker:

```text
NEXT_STEP_ALLOWED = true
```

only when the verified Step-11 ownership output exists and all counts reconcile.

---

## 14. Owner authorization boundary

This pre-step review authorizes no page mapping, Work browser action, Codex execution, Webmaster export, Bridge provider call, or Step-12 decision by itself.

The next action after this review is:

```text
OWNER REVIEWS METHOD
-> OWNER EXPLICITLY AUTHORIZES STEP-11 EXECUTION
-> EXECUTE CURRENT-PAGE RESEARCH + OWNERSHIP MAPPING
```

Current markers:

```text
STEP11_PRE_STEP_RESEARCH_COMPLETE = true
STEP11_SOURCE_TO_METHOD_TRACE_COMPLETE = true
STEP11_OWNER_METHOD_REVIEW_PRESENTED = true
STEP11_EXECUTION_AUTHORIZED = false
STEP11_EXECUTION_STARTED = false
STEP11_PROVIDER_CALLS_AUTHORIZED = false
STEP11_COMPLETE = false
NEXT_STEP_ALLOWED = false
```
