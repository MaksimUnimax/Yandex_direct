# KW-001 / OKNO-MSK — STEP 11 METHOD CORRECTION: DIRECT YANDEX EVIDENCE PRIORITY

Date: 2026-08-30  
Status: **ACTIVE / OWNER-DIRECTED CORRECTION / SUPERSEDES CONFLICTING STEP-11 COST-AVOIDANCE LANGUAGE**

Authority corrected:

```text
STEP_11_PRE_STEP_METHOD_REVIEW_2026-08-30.md
```

Universal economics authority added by owner direction:

```text
EVIDENCE_QUALITY_AND_PROVIDER_COST_POLICY.md
```

This correction does not authorize Step-11 execution by itself. It changes how evidence must be acquired once execution is authorized.

---

## 1. Owner correction

The workflow must optimize for the quality and speed of a sellable client result, not for minimum provider spend.

```text
QUALITY / RELIABILITY / TIME
> PROVIDER COST MINIMIZATION
```

Provider cost is included in delivery economics and must be priced into the service.

Therefore the previous Step-11 language:

```text
use Step-09 evidence first
reserve new ordinary Search for unresolved boundaries
use Webmaster query<->URL only as later escalation
```

is too cost-avoidant and is superseded where it would reduce evidence quality, freshness, coverage, or execution speed.

---

## 2. Fresh official Yandex verification

### Yandex Webmaster — advanced query analytics by URL

Official source:

https://yandex.ru/support/webmaster/ru/service/queries-export

Yandex states that the report:

```text
contains URL + query + region + clicks + impressions + position;
shows queries and pages reached from Search;
can be filtered by region and dates;
is intended to help check whether pages in Yandex Search match query meaning.
```

The report supports up to 100 URLs in one request. The basic access tier provides 100 request units per day; expanded access exists for materially larger workloads.

Method implication:

```text
FOR YANDEX QUERY<->SITE-URL BEHAVIOR:
DIRECT WEBMASTER DATA > CODEX / WORK / CHATGPT INFERENCE
```

### Yandex Webmaster — monitoring queries

Official source:

https://yandex.ru/support/webmaster/ru/service/popular-queries

Yandex states that query data is grouped by query and URL. Query view exposes a high-impression URL for a query, and URL view exposes queries associated with a URL.

Method implication:

```text
YANDEX QUERY<->URL ASSOCIATION IS DIRECTLY OBSERVABLE
```

---

## 3. Correct distinction between tools

The correction does **not** mean direct Yandex data replaces page reading.

They answer different questions.

### Actual page meaning

Best evidence route:

```text
current first-party page read
-> Codex batch extraction
-> Work rendered inspection where needed
-> public-web independent cross-check
```

This answers:

```text
what the page actually sells/explains;
primary object;
user task;
terminal result;
content scope;
CTA;
page type;
visible exclusions/inclusions.
```

### Yandex-observed page/query behavior

Best evidence route:

```text
Yandex Webmaster query<->URL evidence
+ regional ordinary Yandex Search / SERP evidence
```

This answers:

```text
which site URL Yandex currently associates with a query;
which site URL receives impressions/clicks;
which URLs coexist for the same query;
what Yandex currently ranks for the task;
what result/page types define the current SERP context.
```

Therefore:

```text
PAGE_READ != SEARCH_BEHAVIOR_EVIDENCE
SEARCH_BEHAVIOR_EVIDENCE != PAGE_READ
STEP11_HIGH_QUALITY_DECISION = BOTH WHEN MATERIAL
```

---

## 4. Corrected Step-11 evidence acquisition order

The old linear escalation model is replaced by an early parallel evidence model.

### Stage A — freeze semantic inputs

Freeze:

```text
59 final active Step-10 clusters;
13 SEARCH_REQUIRED phrases separately;
current business/site scope;
Step-01 inventory as discovery baseline;
Step-09 evidence as historical/current reusable evidence, not a ceiling.
```

### Stage B — acquire direct Yandex evidence early

Do **not** wait for a later two-URL dispute before using the strongest direct provider evidence.

When Webmaster access is available and authorized:

```text
collect current query<->URL evidence early for material candidate pages / cluster families;
preserve region and date window;
preserve impressions/clicks/position where available;
use query and URL views to expose existing Yandex associations and competing site URLs.
```

For ordinary Search:

```text
reuse Step-09 exact evidence where it matches the current Step-11 question;
add fresh ordinary Search probes wherever cluster coverage, freshness, current ranking context, or ownership confidence materially improves;
do not suppress a useful new Search request merely because an older Step-09 result exists.
```

The acquisition target is **decision coverage**, not the smallest possible request count.

### Stage C — refresh actual current pages

In parallel analytical terms, refresh current page evidence using Codex / Work / public web.

Every `OWNER_EXISTING` still requires current actual-page evidence.

```text
DIRECT YANDEX DATA CANNOT BY ITSELF PROVE WHAT THE PAGE ACTUALLY CONTAINS
```

### Stage D — combine the two evidence planes

For each cluster compare:

```text
CLUSTER TASK
<-> CURRENT PAGE CONTENT/TASK FIT
<-> CURRENT YANDEX QUERY/URL BEHAVIOR
<-> CURRENT SERP CONTEXT
```

A strong ownership decision is a convergence decision, not a lexical or single-channel shortcut.

---

## 5. Corrected provider-use principle

The previous project control:

```text
TARGETED_SEARCH_ESCALATION_ONLY_WHEN_UNRESOLVED
```

is superseded.

Correct principle:

```text
DIRECT_YANDEX_EVIDENCE_EARLY_WHEN_MATERIAL = true
NEW_SEARCH_NOT_BLOCKED_BY_EXISTING_STEP09 = true
PROVIDER_REQUEST_COUNT_MINIMIZATION = false
DECISION_COVERAGE_AND_FRESHNESS = primary
```

This does not require mechanically probing every phrase.

Instead, build direct Yandex coverage at the level needed to validate every material cluster/page ownership decision. Large or internally heterogeneous clusters may justify more than one representative query; a narrow cluster may need one or already have sufficient direct evidence.

Exact sampling is an execution decision based on cluster/task diversity and existing evidence, not a fixed low-cost quota.

---

## 6. Evidence hierarchy by question

Do not use one total hierarchy for unlike questions.

### Question: what does the page mean?

```text
CURRENT FIRST-PARTY PAGE CONTENT
> historical page inventory
> slug/title-only inference
```

### Question: how does Yandex associate the site's pages with queries?

```text
CURRENT YANDEX WEBMASTER QUERY<->URL EVIDENCE
> agent inference from page wording
```

### Question: what is Yandex currently ranking for the user task?

```text
CURRENT REGIONAL ORDINARY YANDEX SEARCH / SERP
> stale SERP evidence
> agent inference
```

### Question: which existing page should analytically own the cluster?

```text
CURRENT PAGE TASK FIT
+ DIRECT YANDEX SEARCH-BEHAVIOR EVIDENCE
+ BUSINESS SCOPE
+ CONTRADICTION REVIEW
-> OWNERSHIP VERDICT
```

No provider observation is automatically equal to intended analytical ownership:

```text
RANKING_URL != AUTOMATIC_OWNER
```

but provider evidence must not be withheld simply to save cost.

---

## 7. Work and Codex role after correction

### Codex

Use aggressively for scale:

```text
current URL inventory;
batch fetch/read;
structured page profiles;
main-content extraction;
current Title/H1/CTA;
redirect and template-family detection;
reconciliation and artifacts.
```

### Work

Use where it gives faster/more reliable browser-grounded evidence:

```text
rendered content;
dynamic/JS sections;
forms and navigation context;
authenticated Webmaster UI;
manual adjudication of ambiguous page meaning.
```

### Direct Yandex sources

Use as first-class evidence, not as last resort:

```text
Webmaster query<->URL;
ordinary regional Search / SERP;
other relevant direct Yandex surfaces.
```

Tool choice is based on which source most directly answers the question, not which source is cheapest.

---

## 8. Cost and time accounting

Provider economics remain mandatory:

```text
planned requests
executed requests
successful/failed/outcome_unknown
cost per surface where known
total provider cost
additional evidence rationale
```

But the output of this accounting is used to calculate service cost and later pricing/margin.

```text
IF REQUIRED EVIDENCE MAKES CURRENT PRICE UNPROFITABLE
-> CHANGE PRICE / PACKAGE ECONOMICS
NOT
-> SECRETLY LOWER EVIDENCE QUALITY
```

---

## 9. Corrected Step-11 PASS implications

In addition to the existing Step-11 gate:

```text
FINAL_STEP10_CLUSTERS_ACCOUNTED = 59/59
OWNER_EXISTING_WITHOUT_CURRENT_PAGE_READ = 0
LEXICAL_ONLY_OWNERSHIP_DECISIONS = 0
RANKING_URL_AUTOMATICALLY_EQUATED_TO_OWNER = 0
```

also require:

```text
MATERIAL_IN_SCOPE_CLUSTERS_WITHOUT_DIRECT_YANDEX_EVIDENCE_ROUTE = 0
DIRECT_YANDEX_EVIDENCE_WITHHELD_ONLY_TO_SAVE_COST = 0
OLD_STEP09_EVIDENCE_USED_AS_ARTIFICIAL_REQUEST_CEILING = 0
PROVIDER_COST_ACCOUNTED = true when provider used
```

A cluster may still have no direct observation if the direct source genuinely has no data or cannot answer the question, but that absence must be explicit rather than caused by cost avoidance.

---

## 10. Current execution status

```text
STEP11_METHOD_CORRECTION_APPLIED = true
STEP11_DIRECT_YANDEX_EVIDENCE_PRIORITY = true
STEP11_COST_MINIMIZATION_AS_PRIMARY_GOAL = false
STEP11_EXECUTION_AUTHORIZED = false
STEP11_EXECUTION_STARTED = false
STEP11_COMPLETE = false
NEXT_STEP_ALLOWED = false
```
