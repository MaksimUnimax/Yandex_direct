# KW-002 — INHERITED STEP RULES FROM KW-001

Status: **ACTIVE DRAFT FOR OWNER REVIEW / REQUIRED COMPANION TO STEP_RULES_INDEX**

Purpose: перенести в Level 2 KW-002 реальные правила совпадающих шагов KW-001, а не оставлять подписи вида `inherited from KW-001` без содержания.

```text
LEVEL 2 = правила и методика конкретных шагов KW-002
work/<JOB_ID>/ = данные конкретного заказа
```

Каждый раздел ниже содержит именно правило, причину/ошибку и PASS boundary. Конкретные Blood & Sand значения сюда не входят.

---

# KW002 STEP 00 — scope freeze

Inherited from KW001 Step 0.

### RULE

До первого provider/search/research действия заморозить:

```text
business
region
scope
products/services/assortment boundary
exclusions
commercial goal
promised outputs
allowed input sources
sealed/prohibited prior research
```

Позднее evidence может изменить выводы, но не может незаметно переписать исходный заказ.

### FAILURE BLOCKED

```text
EVOLVING ANALYSIS
WAS ALLOWED TO CHANGE
ORIGINAL SUCCESS CRITERION
```

### PASS

Frozen brief существует до анализа; изменения только как отдельная revision lineage.

---

# KW002 STEP 01 — business / assortment model

Adapted from KW001 Step 1 discovery.

### RULE

Сначала построить фактическую модель того, что бизнес реально продаёт/делает, какие есть товарные/услуговые границы и что вне scope. Для greenfield не требуется current-site completeness, но нельзя строить seed taxonomy из фантазии или старого SEO-исследования.

Если есть большой raw assortment, его полная обработка подчиняется Level-1 Work rule.

### FAILURE BLOCKED

```text
DISCOVERY SUCCESS != DISCOVERY COMPLETENESS
CLIENT/ANALYST VOCABULARY != SEARCH TAXONOMY
```

### PASS

Ассортимент/услуги и out-of-scope границы покрыты настолько, чтобы seed generation не пропустил фактические продуктовые семейства.

---

# KW002 STEP 02 — seed / acquisition plan

Inherited from KW001 Step 2.

### RULE

Каждый seed — измерительный зонд с конкретной целью обнаружения vocabulary/demand family.

```text
SEED != FINAL KEYWORD
SEED != FINAL PAGE
CURRENT/CLIENT TAXONOMY != AUTOMATIC ACQUISITION TAXONOMY
```

Для каждого seed записывается, какую неопределённость/семейство он должен раскрыть.

### FAILURE BLOCKED

```text
MEASUREMENT INSTRUMENT
WAS TREATED AS
FINAL OBJECT OF SELECTION
```

### PASS

Нет seeds без явной информационной цели; seed relevance не используется как доказательство final relevance.

---

# KW002 STEP 03 — primary Wordstat acquisition

Inherited from KW001 Step 3 + Bridge persistence.

### RULE

Для каждого authorised Wordstat item:

```text
DEFINE REQUIRED RESULT
→ EXECUTE
→ RECEIVE COMPLETE RESULT
→ DURABLY SAVE COMPLETE RETURNED ROWS
→ READBACK
→ COUNT/FIELD/PROVENANCE RECONCILIATION
→ ONLY THEN NEXT ITEM
```

Обязательно сохраняются все returned occurrences, включая duplicates, low-frequency, association/similar rows, будущие exclusions/REVIEW.

Минимальная lineage/demand truth по возможности включает:

```text
exact phrase
count
row role
method/report
seed/request
region/IDs
devices
operator/expression
collection time
request/source IDs
raw or durable raw-equivalent
limits/returned totals/pagination/truncation
```

Deduplication создаёт отдельный normalized view и не уничтожает raw occurrences.

### FAILURE BLOCKED

```text
HTTP 200 / SUCCEEDED
WAS TREATED AS
COMPLETE DATA ACQUISITION
```

### PASS

Every returned row durably preserved; available material fields silently lost = 0; returned/saved/verified reconcile.

---

# KW002 STEP 04 — first family triage

Inherited from KW001 Step 4.

### RULE

Первый разбор удаляет очевидный scope/noise, но не притворяется полноценной построчной очисткой.

```text
FAMILY TRIAGE != ROW-LEVEL CLEANUP
LOW FREQUENCY != IRRELEVANCE
HIGH VOLUME / ASSOCIATION != SEMANTIC FIT
```

Разделять как минимум KEEP-CANDIDATE / REVIEW / EXCLUDE reasons без silent drops.

### PASS

Не сделаны page/cluster conclusions; спорные семейства сохранены для дальнейшего evidence.

---

# KW002 STEP 05 — targeted second acquisition / coverage control

Inherited from KW001 Step 5.

### RULE

Второй acquisition запускается только на именованный информационный пробел.

```text
SECOND ACQUISITION
REQUIRES EXPLICIT INFORMATION GAIN
!= RECURSIVE KEYWORD COLLECTION
```

Для каждого нового probe:

```text
what uncertainty remains
why current evidence cannot answer it
what new evidence can change
```

Output schema union-compatible with Step 03; raw second-pass observations не схлопываются при merge.

### PASS

Нет recursive expansion без named information gain; complete occurrence/provenance preserved.

---

# KW002 STEP 06 — real Yandex competitor discovery

Inherited from KW001 Step 5A.1.

### RULE

SEO-конкуренты определяются из текущих Яндекс SERP по representative in-scope query families, а не из списка бизнес-конкурентов клиента.

Record returned domains/URLs and recurrence across materially different families.

Possible analyst classes:

```text
DIRECT BUSINESS COMPETITOR
ORGANIC COMPETITOR OTHER MODEL
MARKETPLACE / AGGREGATOR
INFORMATIONAL SOURCE
MANUFACTURER / BRAND SOURCE
OTHER REVIEW
```

Это project taxonomy, не официальная классификация Яндекса.

Не замораживать универсальное число конкурентов. Расширять пока добавляется material semantic information.

### PASS

Каждый выбранный semantic competitor имеет current Yandex discovery lineage.

---

# KW002 STEP 07 — competitor page semantic discovery

Inherited from KW001 Step 5A.2–5A.3.

### RULE

Предпочитать competitor URLs, которые реально появились в текущем Яндексе. Из страницы извлекать только material topics/use-cases/headings/navigation directions, нужные для поиска пропущенного спроса.

Каждый candidate seed сохраняет lineage:

```text
seed
← competitor domain
← competitor URL
← Yandex query/result that exposed URL
← page element/topic that motivated seed
```

Hard boundary:

```text
COMPETITOR PAGE TOPIC
!= COMPETITOR RANKS FOR THAT EXACT QUERY
!= PROVEN SEARCH DEMAND
```

### PASS

Page-topic-as-ranking overclaim = 0; every new candidate has provenance.

---

# KW002 STEP 08 — competitor-derived Wordstat expansion + decision

Inherited from KW001 Step 5A.4–5A.8.

### RULE

Только genuinely new/information-gaining competitor seeds идут в Wordstat. Все returned occurrences сохраняются по Step03 schema.

Затем business/scope filter + current Search recheck where material.

Every candidate receives one outcome:

```text
ADD_TO_PIPELINE
ALREADY_COVERED
REJECT_OFF_SCOPE
HOLD_EVIDENCE
```

```text
COMPETITOR SIGNAL
+ BUSINESS FIT
+ WORDSTAT DEMAND
+ CURRENT SEARCH INTENT/VISIBILITY WHEN MATERIAL
→ DECISION
```

Stop on diminishing information gain; universal saturation threshold запрещён.

### PASS

Accepted additions merged into same semantic pipeline; decorative competitor silo forbidden; recursive competitor crawling stopped with explicit rationale.

---

# KW002 STEP 09 — candidate semantic master freeze

Adapted from KW001 acquisition durability + Step8 handoff principles.

### RULE

Собрать единый candidate master из всех authorised acquisition lineages без потери raw provenance.

```text
COLLECT ONCE
PRESERVE COMPLETELY
DERIVE MANY VIEWS LATER
```

Каждая phrase-key имеет deterministic join to demand/provenance. Raw acquisition status не переписывается будущим semantic decision.

### PASS

All acquisition lineages accounted; silent phrase/field loss = 0; lineage join coverage = 100% for frozen universe.

---

# KW002 STEP 10 — row-level cleanup + user-task/intent preparation

Inherited from KW001 Step 7 + task-first rules.

### RULE

Каждая unique phrase получает explicit state. KEEP требует положительного semantic/business evidence.

```text
NO REJECTION RULE MATCHED != KEEP
LOW FREQUENCY != IRRELEVANCE
HIGH COUNT != RELEVANCE
ACCOUNTING QA != SEMANTIC QA
```

Ambiguous potentially useful demand → REVIEW/HOLD, а не forced KEEP/EXCLUDE.

Task analysis reads complete request, business scope, expected terminal result, lifecycle/action, intent/execution mode and object boundary.

### PASS

Every input phrase accounted; default KEEP = 0; semantic adversarial QA performed; unresolved truth preserved.

---

# KW002 STEP 11 — Search-stage semantic freeze

Inherited from KW001 Step 8.

### RULE

До Search validation заморозить row-preserving handoff, не выполняя финальную clustering/page ownership.

Allowed equivalent routes:

```text
CORE_CANDIDATE
REVIEW_SEARCH
REVIEW_DEFERRED
EXCLUDED_PRESERVED
```

Только states с реальным executable next action.

```text
EVALUATION DIMENSION != EVIDENCE ROUTE
```

REVIEW не может исчезнуть ради снижения Search workload. Non-exact duplicates не сливаются автоматически до evidence.

### PASS

Every phrase preserved/routed; all REVIEW accounted; no final cluster/page mapping; provenance join 100%; no unsupported routing states.

---

# KW002 STEP 12 — ordinary Yandex Search batch evidence

Inherited from KW001 Step 9 claim boundaries + Level1 provider rules.

### RULE

Search evidence is exact to observed query/region/time/result sample unless explicit evidence justifies a broader generalization.

```text
EXACT QUERY OBSERVATION != UNPROBED QUERY EVIDENCE
EXACT QUERY OBSERVATION != FAMILY COVERAGE BY DEFAULT
NORMALIZED PROJECTION != RAW PROVIDER BODY
```

For every Search batch item preserve complete usable ranked URL/domain/title evidence and declared raw/projection fidelity.

Search batch technical chunk size is not a product keyword limit.

### PASS

Every tested query has durable exact provenance; no unobserved family claims; returned/saved/verified queries reconcile.

---

# KW002 STEP 13 — SERP + task-first clustering

Inherited from KW001 Step 10 methods.

### RULE

Executable clustering:

```text
TASK-FIRST CORE
+ CURRENT DOMAIN PROFILE
+ CURRENT CORPUS
+ CURRENT SEARCH EVIDENCE
+ CURRENT BUSINESS/DELIVERABLE CONSTRAINTS
```

Baseline:

```text
SAME MATERIAL USER TASK → SAME CLUSTER CANDIDATE
MATERIAL USER-TASK DIFFERENCE → SPLIT CANDIDATE
UNCLEAR → REVIEW / EVIDENCE
```

SERP overlap is one signal, not automatic verdict.

```text
ONE RESULT CAN SATISFY BOTH → MERGE EVIDENCE
ONE RESULT CANNOT SATISFY BOTH → SPLIT EVIDENCE
```

Modifiers (brand/geo/material/size/etc.) default to attributes unless current evidence proves material boundary.

No universal Jaccard/shared-URL threshold. If a job-specific threshold is used, it must be declared, scoped and reviewed.

Cluster count is unconstrained unless the sold/current job explicitly imposes a count/range. No analyst-invented tidy number.

Small/singleton cluster may be correct; large cluster may be wrong.

### CORRECTION RULE

```text
CORRECTED CLUSTER ID != CORRECTED ROW
```

After material reassignment rebuild all fields derived from target cluster contract and re-QA impacted consumers.

### PASS

Every retained phrase assigned or explicitly unresolved; split axes recorded; local rules scoped; semantic + deliverable QA PASS.

---

# KW002 STEP 14 — query→page ownership + Search-only IA freeze

Inherited from KW001 Step 11 + Step 14, adapted to greenfield.

### RULE A — phrase→page completeness

```text
CLUSTER OWNERSHIP COMPLETE != PHRASE→PAGE MAP COMPLETE
```

Every active phrase must resolve through effective cluster to exactly one planned primary page or explicit unresolved/no-page state.

Representative query/cluster label is not proof for every member; full-member coherence review required when material.

### RULE B — target page vs observed ranking URL

```text
PLANNED TARGET PAGE != OBSERVED SEARCH RELEVANT URL
```

For greenfield, competitor ranking URLs are evidence about result/page expectation, not owner URLs for the future client site.

### RULE C — Search-only architecture must freeze before AI

```text
FINAL SEARCH-ONLY QUERY→PAGE / IA
→ PERSIST + READBACK
→ ONLY THEN AI CASE SELECTION
```

No AI evidence may influence this baseline.

### RULE D — new planned page needs evidence

Do not create a page merely because a phrase exists or competitor has a page. A page boundary requires coherent user task + clustering/page compatibility + business scope + Search evidence where material.

### PASS

Every active phrase mapped/unresolved; every planned page has a real job; no unsupported micro-pages; Search-only baseline immutable before AI.

---

# KW002 STEP 15 — AI-search diagnostic selection

Inherited from KW001 Step 15.

### RULE

Step selects cases only; it performs zero AI/provider calls.

```text
STEP15 = CASE SELECTION / PREREGISTRATION
STEP16 = AI EVIDENCE ACQUISITION
```

Build candidates by exact upstream lineage, never memory reconstruction.

Selected set may contain:

```text
DIAGNOSTIC_PROBES
+ STABILITY_CONTROLS WHEN NEEDED
```

Diagnostic set is not representative of whole core unless separate sampling method proves it.

Every selected case preregisters:

```text
exact query
frozen Search-only baseline
why selected
what observable AI evidence matters
CHANGE/DE_RISK/NO_CHANGE/INSUFFICIENT conditions
confirmation rule for material architecture delta
```

No universal number of AI cases.

### PASS

Lineage mismatches = 0; provider calls = 0; all cases have frozen baseline and preregistered interpretation.

---

# KW002 STEP 16 — AI-search evidence acquisition

Inherited narrow KW001 Step16 evidence-integrity boundaries; full method requires current pre-step research.

### RULE

```text
AI REQUEST EXECUTED != AI-NATIVE ANALYTICAL VALUE
PROVIDER/PROXY SURFACE != CONSUMER SURFACE
NORMALIZED OBSERVATION != VERBATIM RAW EVIDENCE
NOT PERSISTED + READ BACK != DURABLE EVIDENCE
```

The exact current Yandex AI/GenSearch surface, claim boundary and probing design must be revalidated before execution because KW001 did not promote a universal full Step16 method.

### PASS

All raw/normalized AI evidence durably preserved with surface, query, time and source provenance; proxy/consumer overclaim = 0.

---

# KW002 STEP 17 — Search-vs-AI reconciliation

Inherited from KW001 Step 17.

### RULE

Compare against immutable Search-only baseline. Separate two questions:

```text
ARCHITECTURE EFFECT
CONTENT / PAGE-JOB EFFECT
```

Allowed architecture verdicts:

```text
CHANGE
DE_RISK
NO_CHANGE
INSUFFICIENT
```

AI exact query != whole family by default. One snapshot != stability. Proxy != consumer-surface claim.

```text
NO ARCHITECTURE CHANGE != NO PAGE-JOB/CONTENT CHANGE
SUPPORTED NO_CHANGE / DE_RISK != NO RESULT
```

Every material case preserves causal object:

```text
WHY SELECTED
→ FROZEN SEARCH DECISION
→ AI EVIDENCE
→ COMPARISON
→ VERDICT
→ ARCHITECTURE EFFECT
→ PAGE-JOB/CONTENT EFFECT
→ EXACT DOWNSTREAM ACTION OR EXPLICIT NO-ACTION
→ CLIENT IMPLICATION
→ LIMITATION / RECHECK
```

One bounded AI observation alone cannot authorize architecture-material CHANGE without required confirmation route.

### PASS

All selected cases accounted; no forced AI delta; claim scope/temporal boundary explicit; exact action/no-action preserved.

---

# KW002 STEP 18 — final semantic core + IA + Page Jobs + internal-link model

Adapted from KW001 page ownership / structural coherence / Search-vs-AI lessons.

### RULE

Final materialization must rebuild from current accepted authorities after Step17; do not patch only AI-affected rows while leaving stale dependent fields.

```text
FINAL PHRASE
→ FINAL CLUSTER
→ FINAL PRIMARY PAGE
→ PAGE TYPE
→ PAGE JOB
→ PARENT/CHILD/SUPPORT RELATION
→ INTERNAL LINK ROLE
→ SEARCH/AI DECISION LINEAGE
```

Each important page must have a real user task and business role. Internal links are recommendations/architecture relations, not proof they physically exist on a not-yet-built site.

Any material mutation triggers impact-set rebuild and downstream reconciliation.

### PASS

One current final semantic/page authority; no stale assignments; all retained phrases reconcile; all planned pages have Page Jobs; unresolved states preserved.

---

# KW002 STEP 19 — client deliverables

Inherited KW001 Step19 non-repeat boundary.

### RULE

```text
ONE CURRENT FINAL SEMANTIC MASTER → ALL CLIENT SEMANTIC VIEWS
ONE CURRENT PAGE/IA AUTHORITY → ALL CLIENT STRUCTURE/PAGE-JOB VIEWS
POLISHED DERIVATIVE != AUTHORITY
```

Machine fields and client display fields may differ, but factual meaning/counts/decisions cannot.

Client language explains work/results, not internal stage IDs/protocol jargon.

### PASS

Every deliverable reverse-traces to same current authority; contradictory client views = 0.

---

# KW002 STEP 20 — final QA / recipient acceptance

Inherited KW001 Step20 corrected boundary.

### RULE

Three different QA classes are required:

```text
DATA / CANONICAL QA
WORKBOOK / FILE / RENDER QA
RECIPIENT-USABILITY / PROMISE QA
```

```text
CONSISTENT BUGGY DERIVATIVES != INDEPENDENT VALIDATION
CORRECT DATABASE != CLIENT-USABLE WORKBOOK
PACKAGE PASS != EACH PROMISED ARTIFACT COMPLETE
```

The recipient must be able to understand what was done, why, what was found, what pages/structure are recommended, and what remains uncertain without reading raw evidence.

### PASS

Canonical counts/joins/decisions pass; files open/read; recipient task passes; internal jargon does not substitute explanation.

---

# KW002 STEP 21 — revision rehearsal + Kwork productization measurement

KW001 Step21 full universal method was unvalidated, so KW002 must research/freeze its own method before execution.

Mandatory productization constraints inherited from overall Kwork roadmap:

```text
revision must not silently rewrite original brief/history
only affected evidence/reasoning is reopened when valid
provider replay requires new information gain
measure analyst effort
measure provider calls/cost
measure Work/operator burden
record failure/ambiguity cases
```

### PASS

Revision lineage clear; unaffected work not needlessly replayed; measured truth available for final Kwork scope/price/runbook.

---

# KW002 STEP 22 — job close

Inherited from KW001 lifecycle boundary.

```text
DELIVERABLE PRODUCED != JOB SAFE TO CLOSE
```

Close only when final handoff, revisions/rework and pending provider/operator actions are closed.

### PASS

`safe_to_close=true`; final state/readback preserved; no pending execution dependency.

---

# Mandatory use rule

`STEP_RULES_INDEX.md` is navigation. This file contains inherited executable rule substance. When a KW002 step has a dedicated newer Step method, the newer dedicated method may add detail but may not silently violate an owner-locked inherited rule.

Before modifying an inherited rule:

```text
PROPOSE CHANGE
→ SHOW WHY KW001 RULE DOES NOT FIT / NEW EVIDENCE
→ OWNER AUTHORIZATION
→ UPDATE PERMANENT METHOD
```

## Markers

```text
KW002_DETAILED_KW001_STEP_RULE_INHERITANCE_ACTIVE = true
KW002_STEP_LABEL_ONLY_INHERITANCE_FORBIDDEN = true
KW002_SEED_NOT_FINAL_KEYWORD = true
KW002_COMPLETE_PROVIDER_OCCURRENCE_PERSISTENCE = true
KW002_NO_DEFAULT_KEEP = true
KW002_COMPETITOR_TOPIC_NOT_RANKING_NOT_DEMAND = true
KW002_TASK_FIRST_CLUSTERING = true
KW002_NO_MAGIC_SERP_THRESHOLD = true
KW002_COMPLETE_PHRASE_TO_PAGE_MAP = true
KW002_SEARCH_ONLY_FREEZE_BEFORE_AI = true
KW002_AI_CASE_SELECTION_ZERO_PROVIDER_CALLS = true
KW002_NO_FORCED_AI_DELTA = true
KW002_ONE_CANONICAL_TRUTH_ALL_DELIVERABLES = true
KW002_DATA_WORKBOOK_RECIPIENT_QA_SEPARATE = true
```