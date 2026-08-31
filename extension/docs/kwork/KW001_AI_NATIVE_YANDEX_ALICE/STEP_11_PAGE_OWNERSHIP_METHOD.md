# Step 11 — Page ownership / keyword-to-page mapping method

Status: **APPROVED / ACTIVE AFTER EXTERNAL METHOD AUDIT + PHRASE-LEVEL CORRECTION**  
Scope: reusable Step-11 method for Kwork semantic/site-architecture jobs.  
Step boundary: page ownership and phrase→page materialization only. Structural actions belong to Step 12; cannibalization verdicts belong to Step 13.

## 1. What Step 11 must produce

Step 11 answers two related but different questions:

1. **Cluster ownership:** does the current public site have an existing page that truthfully satisfies the user task represented by a semantic cluster, and if yes, what is the intended target URL?
2. **Phrase-level page map:** after ownership is decided, which exact active phrases map to that owner through their effective cluster, and which phrases remain without an applicable target because the cluster has no suitable page, is outside scope, or still requires semantic/search resolution?

The step is not complete if only question 1 is answered. A cluster-only ownership ledger is analytically useful but is not yet a complete keyword map because the final deliverable and QA must expose every active phrase against its effective cluster and target-page state.

Canonical relationship:

```text
PHRASE
→ EFFECTIVE USER-TASK CLUSTER
→ TARGET PAGE / EXPLICIT NO-PAGE STATE
```

Do not replace this with independent page selection for each lexical variant. Queries with the same stable user task should normally share one cluster and one target page; however, the full phrase list must still be materialized after cluster ownership so the mapping is inspectable and auditable.

## 2. External method grounding

Current external sources that constrain this method:

- Semrush, *Keyword Mapping: A Step-by-Step Guide for 2026*: related keywords are grouped into clusters and each cluster is mapped to the page that best satisfies search intent; existing suggested pages must be reviewed before acceptance; the keyword map must expose the keyword/topic group and target URL/status.  
  https://www.semrush.com/blog/keyword-mapping/
- Ahrefs, *Keyword Mapping for SEO*: queries with the same or sufficiently similar intent normally belong to one page rather than one page per lexical variant.  
  https://ahrefs.com/blog/keyword-mapping/
- Ahrefs, *Keyword Clustering*: SERP/intention clustering is useful but imperfect; ambiguous and mixed boundaries require manual review rather than blind inheritance.  
  https://ahrefs.com/blog/keyword-clustering/
- Rush Analytics, *Определение релевантных URL для кластеров*: after clustering, determine which page should be promoted for the cluster; a selected URL is assigned to the cluster and to all keywords in that cluster.  
  https://www.rush-analytics.ru/faq/klasterizaciya/opredelenie-relevantnyh-url-dlya-klasterov
- Topvisor, *Целевые URL*: distinguish an SEO-assigned target URL from a search-engine relevant/ranking URL.  
  https://topvisor.com/ru/support/rankings/target-url/
- Yandex Webmaster recommendations on satisfying the user's formulated need and query↔URL analytics.  
  https://yandex.ru/support/webmaster/ru/recommendations/targeting  
  https://yandex.ru/support/webmaster/ru/service/queries-export

These sources support the reusable core, but do not replace current-site reading, current business scope, current search behavior, or job-specific evidence.

## 3. Mandatory terminology

### 3.1 Target URL / owner

`TARGET_EXISTING_URL` or `OWNER_EXISTING` means:

> the current site has a page that the analyst has verified as a truthful intended owner for the cluster's user task.

This is an SEO mapping decision.

### 3.2 Yandex relevant URL

`YANDEX_RELEVANT_URL` means:

> a URL that Yandex is actually surfacing/associating with the query, verified by current Search results or authorized Yandex Webmaster query↔URL data.

Do not call an analyst-selected target URL a Yandex relevant URL without direct evidence.

Hard rule:

```text
TARGET_URL != PROVEN_YANDEX_RELEVANT_URL
```

### 3.3 No suitable existing page

`NO_SUITABLE_EXISTING_PAGE` means only:

> plausible current pages were reviewed and none truthfully owns the full frozen user task.

Because this is a **negative current-site existence claim**, it must also satisfy `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`: absence from the Step-1 inventory is not proof. Use current multi-route discovery (broad Codex/browser discovery when needed, plus targeted current first-party reads) and record coverage limitations. If current-site absence is not sufficiently proven, use an explicit unresolved/absence-not-proven state rather than a confident no-page verdict.

It does **not** mean “create a page”. Creation/merge/split/expansion decisions belong to Step 12.

## 4. Required inputs

Before execution, read and reconcile:

1. the current branch/HEAD and canonical job workspace;
2. current Layer-A process rules;
3. `STEP_RULES_INDEX.md` and this registered Step-11 method;
4. the current job manifest/flow and frozen business/region/scope constraints;
5. the final Step-10 phrase assignment ledger, not only its cluster summary;
6. the final Step-10 cluster summary/taxonomy;
7. unresolved/Search-required handoffs from the previous step;
8. current public-site inventory and page reads;
9. available current Yandex Search/Webmaster evidence when required;
10. previous Step-11 mistakes and non-repeat controls below.

### Why the full phrase ledger is mandatory before ownership

A cluster label can look coherent while its actual member phrases are not. Page ownership imposed on a bad upstream cluster hides the original semantic defect. Therefore Step 11 must retain the ability to inspect all member phrases and must reject or repair an incoherent cluster before assigning a page.

## 5. Critical non-repeat control — Bridge/Codex evidence durability

### Incident that caused this rule

In the OKNO-MSK Step-11 run, Bridge and Codex acquisition results were allowed to exist temporarily in conversational/tool state before all of the useful evidence had been durably written to the canonical GitHub job workspace. The run came close to losing results that had already cost provider requests and analyst work. Replaying paid or stateful acquisition later may be expensive, impossible, or not reproduce the same evidence.

The previous generic rule `REQUEST_SUCCEEDED != PROJECT_RESULT_COMPLETE` was correct but insufficiently operational. It did not force persistence **immediately after each acquisition interaction**.

### Permanent rule

For every Bridge or Codex acquisition interaction that produces evidence used by the job:

```text
INTERACTION EXECUTION TRUTH
→ COMPLETE REQUIRED RESULT AVAILABLE
→ IMMEDIATE SAVE TO CANONICAL GITHUB JOB WORKSPACE
→ GITHUB READBACK / PARSE / COMPLETENESS VERIFY
→ ONLY THEN THE NEXT ACQUISITION INTERACTION MAY START
```

Never collect several Bridge/Codex interactions with the intention to “save everything at the end”.

### Why

Tool/provider success proves only that the interaction happened. It does not prove project durability. Conversation context, browser state, provider state, extension state, or a later tool failure can disappear. GitHub persistence plus readback turns transient evidence into reusable project evidence and prevents needless paid replay.

### Bridge-specific mandatory record

Before any Yandex Marketing Bridge call, state:

```text
YMB MODE:
- Active service: <wordstat|search|webmaster|metrika|direct>
- Execution mode: <Manual|Autorun|accepted other>
- Manual mode: ON   # when relevant
```

Also define before execution:

```text
YMB STEP OBJECTIVE
YMB REQUIRED SAVED RESULT
YMB COMPLETENESS CHECK
YMB STOP CONDITION
```

After each interaction record and persist:

- provider execution truth;
- project result, not only HTTP/status/cost;
- raw/normalized data required by the job;
- request/job IDs when available;
- completeness/accounting state;
- cost state when billable;
- limitation if any evidence could not be preserved.

If the required result is incomplete, stop. Do not issue the next Bridge interaction merely because the previous request returned HTTP 200 or `SUCCEEDED`.

### Codex-specific mandatory record

A Codex/site-review pass is also acquisition. Persist immediately:

- discovered URL inventory;
- exact pages actually opened/read;
- page profile fields needed for ownership;
- final URL/title/H1/visible task/CTA and important limitations;
- any page that could not be read;
- acquisition timestamp/source provenance.

Then read the saved artifact back from GitHub before another acquisition batch.

## 6. Step-11 execution sequence

### 6.1 Freeze the input and build a cluster-membership view

Start from the final Step-10 phrase ledger. For every active phrase preserve at minimum:

- phrase;
- Step-10 assignment status;
- Step-10 cluster ID;
- user task / intent / business fit;
- assignment confidence/evidence mode;
- unresolved state where applicable.

Do not begin ownership from the cluster summary alone.

**Why:** the cluster summary hides heterogeneous member phrases. Step 11 is a downstream semantic integrity checkpoint, not a blind consumer of labels.

### 6.2 Refresh the current public-site page inventory

Use `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`. Use current public-site evidence (Codex/ChatGPT public browsing/first-party reads as allowed by the job) to identify plausible owner candidates. A small named positive check can be done with targeted web reads; a material negative claim that no page exists on a large site requires broad multi-route discovery and should use Codex/browser as the preferred discovery channel when available.

For material candidates, record:

- current URL/final URL;
- title/H1 and visible page purpose;
- product/service/information task actually covered;
- CTA/transactional capability where relevant;
- important inclusions/exclusions;
- parent/child/sibling page relationships when they affect ownership.

Persist every acquisition batch immediately under the durability protocol in section 5.

**Why:** a URL name or old sitemap entry is not proof that a current page can own a task. Ownership is about current content and user outcome.

### 6.3 Build the candidate ledger before deciding ownership

For each active cluster, list plausible current candidate URLs and evidence for/against each one.

Do not choose an owner by title/URL token overlap.

**Why:** a similarly named page may be too narrow, transactional instead of informational, a sub-step rather than a standalone service, or a different object entirely.

### 6.4 Audit cluster coherence before accepting an owner

This is mandatory and was missing from the first OKNO-MSK Step-11 run.

For every cluster, and especially every `MEDIUM`/`LOW` ownership candidate or broad heterogeneous cluster:

1. inspect all member phrases, not only a representative phrase;
2. ask whether they share one stable terminal user task;
3. compare the frozen cluster label with the actual member phrases;
4. if a subset clearly has a different task, correct via an explicit post-Step-10 overlay/split rather than silently changing the cluster meaning;
5. if an individual phrase remains ambiguous, move it to `SEARCH_REQUIRED` / explicit unresolved state rather than forcing it onto a page;
6. preserve the original Step-10 artifact and record corrections separately so history is auditable.

**Why:** a representative SERP query is evidence about that query, not permission to rewrite the meaning of every phrase in the cluster. A bad cluster cannot be repaired by assigning it a convenient URL.

Hard rule:

```text
REPRESENTATIVE_QUERY_BEHAVIOR != PERMISSION_TO_REWRITE_CLUSTER_BOUNDARY
```

### 6.5 Use Yandex Search only where it resolves a real decision boundary

Search evidence may establish dominant result type, object boundary, commercial/informational intent, or page-type expectation.

Do not use ranking absence as proof that the target site lacks a suitable page.

Do not transfer one query's SERP evidence automatically to unprobed neighbours.

If direct Yandex evidence is required, use the Bridge protocol and immediate GitHub persistence gate in section 5.

**Why:** Search behavior helps define user expectation, but ownership still requires current first-party page fit.

### 6.6 Decide cluster ownership

Accepted decision chain:

```text
CURRENT PAGE TASK FIT
+ CURRENT SEARCH-BEHAVIOR EVIDENCE WHEN MATERIAL
+ BUSINESS SCOPE
+ CONTRADICTION REVIEW
+ FULL MEMBER-PHRASE COHERENCE CHECK
→ OWNERSHIP VERDICT
```

Allowed ownership states:

- `OWNER_EXISTING`
- `NO_SUITABLE_EXISTING_PAGE`
- `OWNER_UNRESOLVED_EVIDENCE_REQUIRED`
- `OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP`

For every `OWNER_EXISTING`, the current target page must have been read and its task fit documented.

For every `NO_SUITABLE_EXISTING_PAGE`, plausible current candidates must have been reviewed before rejection.

For every unresolved state, provide an executable evidence route; do not hide uncertainty inside a confidence label.

### 6.7 Materialize the complete phrase→page map

After effective cluster ownership is frozen, join the final effective phrase assignments to ownership and create one row per active phrase.

Minimum fields:

```text
phrase
original_assignment_status
original_cluster_id
effective_assignment_status
effective_cluster_id
cluster_user_task
intent_type
business_fit
assignment_confidence
target_url
ownership_state
ownership_confidence
page_mapping_applicability
mapping_reason
evidence_provenance
correction_source
```

Rules:

- every effective `ASSIGNED` phrase must resolve to exactly one effective cluster ownership row;
- `OWNER_EXISTING` requires a non-empty target URL;
- `NO_SUITABLE_EXISTING_PAGE`, unresolved, and outside-scope states keep target URL blank unless the schema explicitly distinguishes a rejected candidate from a target;
- `SEARCH_REQUIRED` phrases have no target URL and remain `PAGE_OWNERSHIP_NOT_APPLICABLE_UNTIL_TASK_RESOLVED`;
- no active phrase may disappear merely because it did not fit a page.

**Why:** this is the client-usable keyword map and the machine-auditable proof that cluster ownership really covers the semantic set. A cluster-only ownership table cannot prove phrase-level completeness or reveal a bad mixed cluster as reliably.

Hard rule:

```text
CLUSTER_OWNERSHIP_COMPLETE != PHRASE_PAGE_MAPPING_COMPLETE
```

### 6.8 Adversarial review of weak or broad decisions

At minimum, re-open every `MEDIUM`/`LOW` ownership decision and every unusually broad cluster. Inspect all member phrases and current page evidence.

Challenge:

- mixed product vs service intent;
- product/model reviews vs company/provider reviews;
- generic task labels whose phrases are object-specific;
- broad technical-information clusters containing multiple product families;
- component repair/replacement mixed with whole-product replacement;
- commercial hub used for a genuinely informational task;
- third-party aftermarket/catalog demand mapped to a site that does not sell those products.

**Why:** these are precisely the cases where a superficially plausible target URL can hide upstream clustering errors.

## 7. Hard boundaries / forbidden shortcuts

```text
LEXICAL_URL_OR_TITLE_MATCH != OWNERSHIP
RANKING_URL != AUTOMATIC_OWNER
SEARCH_ABSENCE != NO_SUITABLE_EXISTING_PAGE
NO_SUITABLE_EXISTING_PAGE != CREATE_DECISION
MULTIPLE_URLS != CANNIBALIZATION
TARGET_URL != PROVEN_YANDEX_RELEVANT_URL
REPRESENTATIVE_QUERY != WHOLE_CLUSTER_EVIDENCE
CLUSTER_OWNERSHIP_COMPLETE != PHRASE_PAGE_MAPPING_COMPLETE
REQUEST_SUCCEEDED != PROJECT_RESULT_COMPLETE
BRIDGE_OR_CODEX_RESULT_IN_CHAT != DURABLE_PROJECT_EVIDENCE
```

Never make Step-12 `KEEP / EXPAND / SPLIT / MERGE / CREATE` decisions in Step 11.  
Never make Step-13 cannibalization verdicts in Step 11.

## 8. Required artifacts and why each exists

A completed Step 11 should preserve:

1. **current URL discovery inventory** — proves what public pages were considered;
2. **current page-profile/read ledger** — proves actual page purpose, not lexical guesses;
3. **cluster→candidate ledger** — shows alternatives and contradictions considered;
4. **cluster ownership ledger** — records final target/no-page state;
5. **post-upstream correction overlay, if needed** — preserves original Step-10 history while making downstream semantics correct;
6. **phrase→page map** — materializes every active phrase against its effective cluster and target state;
7. **unresolved/Search-required handoff** — prevents ambiguous phrases from being silently forced into ownership;
8. **provider/Codex acquisition receipts/checkpoints/results** — preserves execution and reusable evidence;
9. **QA JSON/report** — proves accounting, invariants, limitations and step boundary;
10. **current job-flow update** — prevents the next dialogue from relying on stale step status.

## 9. Mandatory QA gate

Step 11 cannot be accepted until all applicable checks pass:

### Accounting

```text
ACTIVE_INPUT_ROWS == PHRASE_PAGE_MAP_ROWS
ACTIVE_ASSIGNED + ACTIVE_SEARCH_REQUIRED == ACTIVE_INPUT_ROWS
SILENT_ACTIVE_DROPS == 0
UNKNOWN_EFFECTIVE_CLUSTER_IDS == 0
DUPLICATE_PHRASE_MAP_ROWS == 0
```

### Ownership integrity

```text
ASSIGNED_WITHOUT_OWNERSHIP_ROW == 0
OWNER_EXISTING_WITH_BLANK_TARGET_URL == 0
NO_SUITABLE_WITH_TARGET_URL == 0
UNRESOLVED_WITHOUT_EXECUTABLE_ROUTE == 0
OUTSIDE_SCOPE_WITH_TARGET_OWNERSHIP == 0
SEARCH_REQUIRED_WITH_TARGET_URL == 0
MULTIPLE_EFFECTIVE_OWNERS_PER_CLUSTER == 0
```

### Semantic integrity

```text
MEDIUM_LOW_OWNERSHIP_ROWS_REAUDITED == 100%
KNOWN_MIXED_CLUSTERS_LEFT_UNCORRECTED == 0
REPRESENTATIVE_QUERY_USED_TO_SILENTLY_REWRITE_CLUSTER == 0
LEXICAL_ONLY_OWNER_DECISIONS == 0
SEARCH_ABSENCE_USED_AS_NO_PAGE_VERDICT == 0
```

### Evidence durability

```text
BRIDGE_ACQUISITION_RESULTS_SAVED_BEFORE_NEXT_INTERACTION == true
CODEX_ACQUISITION_RESULTS_SAVED_BEFORE_NEXT_INTERACTION == true
FINAL_ARTIFACTS_READ_BACK_FROM_GITHUB == true
PROVIDER_REQUEST_AND_COST_ACCOUNTING_RECONCILES == true   # when provider used
KNOWN_PERSISTENCE_LIMITATIONS_RECORDED == true
```

### Step boundary

```text
PREMATURE_STEP12_STRUCTURAL_ACTIONS == 0
PREMATURE_STEP13_CANNIBALIZATION_VERDICTS == 0
```

Only after the phrase-level map, correction audit, evidence durability checks and quantitative reconciliation pass may Step 11 be marked complete.

## 10. OKNO-MSK correction lesson that must remain attached to this method

The first OKNO-MSK Step-11 pass correctly used cluster→page ownership logic, page reads and Yandex Search behavior, but two methodological gaps remained:

1. **Acquisition evidence was not always persisted immediately after each Bridge/Codex interaction.** This risked losing paid/non-reproducible work. The permanent durability gate in section 5 now blocks the next acquisition interaction until save+readback succeeds.
2. **The step stopped at 59 cluster ownership rows and did not materialize the final active phrase→page map.** That omission also hid several heterogeneous Step-10 clusters. The permanent phrase-level materialization and coherence audit in sections 6.4, 6.7 and 6.8 now make this a blocking QA requirement.

During correction, phrase-level review exposed examples of why the new control is necessary: a supposedly generic glazing cluster contained specific aluminium/panoramic/French-window phrases; a supposedly generic glazing-selection cluster was actually veranda-specific; replacement, review and broad technical-information clusters mixed materially different terminal tasks. The correct response is an explicit correction overlay/split or unresolved handoff, not a convenient URL assignment.

This lesson is reusable. The exact OKNO-MSK phrases/URLs remain job-specific evidence and must not become universal lexical rules.
