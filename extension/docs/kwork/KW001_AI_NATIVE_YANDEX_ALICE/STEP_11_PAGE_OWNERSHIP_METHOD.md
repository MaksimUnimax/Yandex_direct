# KW-001 — STEP 11 PAGE OWNERSHIP / PHRASE-TO-PAGE MAPPING METHOD

Updated: 2026-09-03  
Status: **APPROVED / ACTIVE / UNIVERSAL**  
Scope: decide which current public page should own each accepted user-task cluster and materialize the complete phrase→page mapping.  
Boundary: structural actions belong to Step12; competing-page/harm diagnosis belongs to Step13.

Companion authorities:

- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`
- `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md`
- `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`
- `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`

Concrete job domains, URLs, cluster IDs, phrases, counts, provider receipts and correction results belong in Level-2 evidence.

---

## 1. Required result

Step11 answers two different questions:

1. **Cluster ownership:** does the current public site have a page that truthfully satisfies the user task represented by the current effective cluster/unit?
2. **Phrase-level map:** after ownership is decided, which exact active phrases inherit that owner and which remain unresolved/no-page/outside?

```text
PHRASE
→ EFFECTIVE USER-TASK CLUSTER
→ TARGET PAGE / EXPLICIT NO-PAGE OR UNRESOLVED STATE
```

A cluster-only ownership ledger is not a complete keyword-to-page map.

---

## 2. External grounding

- Semrush Keyword Mapping: https://www.semrush.com/blog/keyword-mapping/
- Ahrefs Keyword Mapping: https://ahrefs.com/blog/keyword-mapping/
- Ahrefs Keyword Clustering: https://ahrefs.com/blog/keyword-clustering/
- Rush Analytics relevant URLs: https://www.rush-analytics.ru/faq/klasterizaciya/opredelenie-relevantnyh-url-dlya-klasterov
- Topvisor target URLs: https://topvisor.com/ru/support/rankings/target-url/
- Yandex user-need guidance: https://yandex.ru/support/webmaster/ru/recommendations/targeting
- Yandex query↔URL evidence: https://yandex.ru/support/webmaster/ru/service/queries-export

These support grouping same-task queries, assigning a target page after current-page review, and separating analyst-assigned target URL from search-engine-selected relevant URL.

---

## 3. Mandatory terminology

### TARGET / OWNER

`OWNER_EXISTING` means the current site has a page verified as a truthful intended owner for the user task. It is an analytical mapping decision.

### SEARCH-ENGINE RELEVANT URL

A current Search/Webmaster-observed relevant URL is an observed search behavior fact.

```text
TARGET_URL != PROVEN_SEARCH_ENGINE_RELEVANT_URL
```

### NO_SUITABLE_EXISTING_PAGE

Means only that current plausible pages were reviewed and none truthfully owns the full task.

Because this is a negative current-site claim, it must satisfy the current-site freshness/existence gate.

```text
NO_SUITABLE_EXISTING_PAGE != CREATE_DECISION
```

Creation belongs to Step12.

---

## 4. Permanent failure history — what failed, why, control

### M11-01 — acquisition evidence was allowed to remain transient

**Failure:** provider/browser/code results could exist in conversation/tool state while additional acquisition continued, before useful evidence had been durably written and read back from the canonical job workspace.

**Root cause:**

```text
REQUEST / TOOL EXECUTION SUCCESS
WAS TREATED AS
PROJECT EVIDENCE DURABILITY
```

A general “request succeeded != project complete” statement was not operational enough because it did not block the next acquisition interaction.

**Control:**

```text
ACQUISITION INTERACTION
→ COMPLETE REQUIRED RESULT AVAILABLE
→ IMMEDIATE GITHUB WRITE
→ GITHUB READBACK / PARSE / COMPLETENESS CHECK
→ ONLY THEN NEXT ACQUISITION INTERACTION
```

This applies especially to paid, stateful or non-reproducible acquisition.

---

### M11-02 — cluster ownership was mistaken for complete phrase mapping

**Failure:** the step could produce a clean cluster→page ownership table without materializing every active phrase against its effective cluster and page state.

**Root cause:**

```text
CLUSTER-LEVEL DECISION COMPLETENESS
WAS TREATED AS
PHRASE-LEVEL DELIVERY / ACCOUNTING COMPLETENESS
```

This also hid heterogeneous clusters because the final mapping was not forced to expose every member row.

**Control:** one final phrase→page row per current active phrase, with exact accounting and explicit unresolved/no-page states.

---

### M11-03 — a cluster label/representative query was trusted more than full member phrases

**Failure:** an apparently coherent cluster could contain materially different terminal tasks, yet page ownership was assigned to the label or representative query.

**Root cause:**

```text
REPRESENTATIVE QUERY / CLUSTER LABEL
WAS TREATED AS
PROOF OF EVERY MEMBER'S TERMINAL TASK
```

**Control:** before accepting ownership, inspect all members for broad/weak/mixed clusters and allow explicit correction overlays/splits or unresolved handoff.

```text
REPRESENTATIVE_QUERY_BEHAVIOR != PERMISSION_TO_REWRITE_CLUSTER_BOUNDARY
```

---

### M11-04 — lexical URL/title similarity could dominate page-fit reasoning

**Failure:** a similarly named page can look like the obvious owner even when it serves a different object, lifecycle stage, intent or subtask.

**Root cause:**

```text
LEXICAL MATCH
WAS TREATED AS
CURRENT USER-TASK FIT
```

**Control:** current content/page purpose and user outcome are mandatory; lexical similarity is only candidate discovery evidence.

---

### M11-05 — search absence could be confused with site absence

**Failure:** a target-domain page not observed in current Search can be mistakenly treated as proof that the site has no suitable page.

**Root cause:**

```text
SEARCH VISIBILITY OBSERVATION
WAS TREATED AS
CURRENT SITE INVENTORY FACT
```

**Control:** Search and current-site discovery remain separate evidence routes.

---

### M11-06 — unresolved semantic/search boundaries could be forced into convenient ownership

**Failure:** pressure for a complete map can cause ambiguous phrases/tasks to be assigned to a page without sufficient evidence.

**Root cause:**

```text
OUTPUT COMPLETENESS
WAS PRIORITIZED OVER
TRUTHFUL UNCERTAINTY
```

**Control:** explicit `OWNER_UNRESOLVED_EVIDENCE_REQUIRED` / `SEARCH_REQUIRED` or equivalent state with no fabricated target.

---

## 5. Required inputs

Before execution read/reconcile:

```text
current branch/HEAD and job workspace
current Level-1 rules and Step11 method
current job scope/business/region constraints
final upstream phrase assignment ledger
final upstream cluster/unit summary
unresolved/Search-required handoffs
current public-site discovery/page evidence
persisted Search/Webmaster evidence when required
previous Step11 failure classes + controls
```

Start from the phrase ledger, not the cluster summary alone.

---

## 6. Correct execution sequence

### 6.1 Freeze phrase-level input

For every active phrase preserve upstream assignment status, effective cluster/unit, user task/intent/business fit, confidence/evidence mode and unresolved state.

### 6.2 Refresh current public-site evidence

Apply `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`.

For material candidate pages preserve equivalent observations:

```text
current/final URL
title/H1
visible task/page purpose
product/service/information role
CTA/transaction capability when material
important inclusions/exclusions
parent/child/sibling relation when it affects ownership
read/discovery provenance
```

A named positive check can be narrow. A material negative “no suitable page exists” claim requires sufficient current discovery coverage.

### 6.3 Persist acquisition immediately

Every useful provider/browser/code acquisition batch follows the durability gate before another acquisition begins.

### 6.4 Build candidate ledger

For each effective task/cluster list plausible current candidate pages with evidence for/against each. Do not select by URL/title token alone.

### 6.5 Audit cluster coherence

For broad, heterogeneous, medium/low-confidence or contradicted clusters:

```text
READ ALL MEMBERS
→ TEST ONE STABLE TERMINAL USER TASK
→ IF MATERIAL SUBTASK DIFFERS, CREATE EXPLICIT CORRECTION OVERLAY/SPLIT
→ IF AMBIGUOUS, MOVE TO EXPLICIT UNRESOLVED/SEARCH REQUIRED
→ PRESERVE ORIGINAL UPSTREAM HISTORY
```

### 6.6 Use Search only where it resolves a real boundary

Search may help determine result type, task/object boundary or page expectation. It does not prove site absence and must not be generalized beyond its actual query evidence.

### 6.7 Decide ownership

Allowed equivalent states:

```text
OWNER_EXISTING
NO_SUITABLE_EXISTING_PAGE
OWNER_UNRESOLVED_EVIDENCE_REQUIRED
OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP
```

Decision chain:

```text
FULL MEMBER-PHRASE COHERENCE
+ CURRENT PAGE TASK FIT
+ BUSINESS SCOPE
+ SEARCH BEHAVIOR WHEN MATERIAL
+ CONTRADICTION REVIEW
→ OWNERSHIP VERDICT
```

### 6.8 Materialize complete phrase→page map

Minimum equivalent fields:

```text
phrase
original_assignment_status
original_cluster_or_unit_id
effective_assignment_status
effective_cluster_or_unit_id
user_task
intent_type
business_fit
assignment_confidence
target_url
ownership_state
ownership_confidence
mapping_applicability
mapping_reason
evidence_provenance
correction_source
```

Every effective assigned phrase resolves to exactly one effective ownership row. Unresolved/Search-required phrases have no fabricated target.

### 6.9 Adversarial review

Re-open at minimum:

```text
medium/low ownership decisions
unusually broad task units
mixed product/service/info/DIY/review tasks
whole object vs component tasks
current pages that are plausible only lexically
third-party/aftermarket/catalog demand outside actual business offer
```

The verifier must try to find misassigned members, not merely confirm selected URLs.

### 6.10 Persist, QA, read back, report

Write all final/diagnostic artifacts, read them back from GitHub, reconcile counts and then give the mandatory plain-language end summary.

---

## 7. Hard boundaries

```text
LEXICAL_URL_OR_TITLE_MATCH != OWNERSHIP
RANKING_URL != AUTOMATIC_OWNER
SEARCH_ABSENCE != NO_SUITABLE_EXISTING_PAGE
NO_SUITABLE_EXISTING_PAGE != CREATE_DECISION
MULTIPLE_URLS != CANNIBALIZATION
TARGET_URL != PROVEN_SEARCH_ENGINE_RELEVANT_URL
REPRESENTATIVE_QUERY != WHOLE_CLUSTER_EVIDENCE
CLUSTER_OWNERSHIP_COMPLETE != PHRASE_PAGE_MAPPING_COMPLETE
REQUEST_SUCCEEDED != PROJECT_RESULT_COMPLETE
TRANSIENT TOOL RESULT != DURABLE PROJECT EVIDENCE
```

Do not execute Step12 structural actions or Step13 cannibalization verdicts inside Step11.

---

## 8. Required job artifacts

Equivalent outputs should preserve:

```text
CURRENT URL DISCOVERY INVENTORY
CURRENT PAGE READ/PROFILE LEDGER
CLUSTER/UNIT CANDIDATE LEDGER
OWNERSHIP LEDGER
POST-UPSTREAM CORRECTION OVERLAY when needed
PHRASE→PAGE MAP
UNRESOLVED / SEARCH-REQUIRED HANDOFF
ACQUISITION RECEIPTS / CHECKPOINTS / RESULTS
QA
REPORT
CURRENT STATE / JOB FLOW UPDATE
```

---

## 9. QA gates

### Accounting

```text
CURRENT_ACTIVE_INPUT_ROWS == FINAL_PHRASE_PAGE_MAP_ROWS
SILENT_ACTIVE_DROPS = 0
UNKNOWN_EFFECTIVE_CLUSTER_IDS = 0
DUPLICATE_FINAL_PHRASE_ROWS = 0
```

### Ownership integrity

```text
ASSIGNED_WITHOUT_OWNERSHIP_ROW = 0
OWNER_EXISTING_WITH_BLANK_TARGET = 0
OWNER_EXISTING_WITHOUT_CURRENT_PAGE_READ = 0
NO_SUITABLE_EXISTING_PAGE_WITHOUT_CURRENT_NEGATIVE_EVIDENCE = 0
SEARCH_REQUIRED_WITH_TARGET_URL = 0
TARGET_URL_LABELLED_AS_SEARCH_RELEVANT_WITHOUT DIRECT EVIDENCE = 0
```

### Coherence/corrections

```text
BROAD_OR_WEAK_UNITS_REVIEWED = true
MATERIAL MIXED UNITS LEFT UNCORRECTED = 0
REPRESENTATIVE_QUERY_USED_TO_REWRITE_UNPROBED MEMBERS = 0
ORIGINAL UPSTREAM HISTORY SILENTLY OVERWRITTEN = 0
```

### Evidence durability

```text
USEFUL ACQUISITION BATCHES PERSISTED = true
READBACK COMPLETE = true
NEXT ACQUISITION STARTED BEFORE PRIOR SAVE/READBACK = 0
```

### Step boundary

```text
PREMATURE STEP12 ACTIONS = 0
PREMATURE STEP13 HARM VERDICTS = 0
```

Only after all applicable gates pass may Step11 complete.

---

## 10. Pass meaning

```text
STEP11_COMPLETE
= CURRENT OWNERSHIP DECISIONS + COMPLETE PHRASE→PAGE MAP + DURABLE EVIDENCE + QA

STEP11_COMPLETE
!= STRUCTURAL ACTIONS EXECUTED
!= CANNIBALIZATION PROVEN
```

---

## 11. Permanent markers

```text
KW001_STEP11_METHOD_ACTIVE = true
KW001_STEP11_JOB_SPECIFIC_RESULTS_FORBIDDEN_IN_PERMANENT_METHOD = true
KW001_STEP11_TRANSIENT_ACQUISITION_NOT_DURABLE_EVIDENCE = true
KW001_STEP11_SAVE_READBACK_BEFORE_NEXT_ACQUISITION = true
KW001_STEP11_CLUSTER_OWNERSHIP_NOT_EQUAL_PHRASE_MAP = true
KW001_STEP11_FULL_MEMBER_COHERENCE_REVIEW_REQUIRED_WHEN_MATERIAL = true
KW001_STEP11_REPRESENTATIVE_QUERY_NOT_EQUAL_WHOLE_CLUSTER = true
KW001_STEP11_TARGET_NOT_EQUAL_SEARCH_RELEVANT_URL = true
KW001_STEP11_SEARCH_ABSENCE_NOT_EQUAL_SITE_ABSENCE = true
KW001_STEP11_NO_SUITABLE_PAGE_NOT_EQUAL_CREATE = true
KW001_STEP11_UNRESOLVED_STATE_MUST_NOT_BE_FORCED_TO_TARGET = true
```

## ПРОСТЫМИ СЛОВАМИ

Step11 нужен, чтобы понять, какая существующая страница должна отвечать на каждую реальную задачу пользователя, и затем показать это для каждой отдельной фразы. Нельзя выбрать страницу только по похожему названию, по одному показательному запросу или потому, что так удобнее заполнить таблицу. Сначала проверяются все фразы и текущие страницы, спорные случаи остаются спорными, а каждое полезное внешнее наблюдение сохраняется в GitHub до следующего сбора данных.
