# KW-001 — STEP 20 STANDALONE SEMANTIC CORE ACCEPTANCE GATE

Updated: 2026-09-07  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**  
Scope: **separate client XLSX semantic-core deliverable**

## 1. Recipient and physical result

Recipient: SEO, semantic or implementation specialist.

Physical result: a standalone XLSX semantic core. It is a separate deliverable, not Report №02 and not a promise that the recipient will reconstruct a workbook from repository tables.

Purpose: filtering, sorting, cluster review, phrase→page work, unresolved-case review, prioritization and implementation use.

```text
REPORT №02 SPECIALIST GUIDE
!=
STANDALONE SEMANTIC CORE XLSX
```

The guide explains how to implement conclusions. The semantic core is the full working phrase/cluster/page dataset used by the specialist.

## 2. Required authority and views

The workbook must be generated reproducibly from the current accepted phrase, structural-unit, demand/provenance and page/action authorities. A historical materialization may supply provenance only; it cannot override a later final authority.

Before generation, declare an explicit precedence manifest:

```text
CURRENT FINAL PHRASE / SEMANTIC AUTHORITY
+
CURRENT STRUCTURAL-UNIT AUTHORITY
+
CURRENT DEMAND / FREQUENCY / PROVENANCE AUTHORITY
+
CURRENT PAGE / ACTION AUTHORITY WHEN APPLICABLE
=
ONLY EXECUTABLE CLIENT-MATERIALIZATION TRUTH
```

A prior CSV/XLSX generated before later corrections is never silently promoted back to authority merely because it already looks like a semantic core.

Unless the sold contract defines an equally usable equivalent, the workbook exposes:

1. all preserved phrases;
2. the active core;
3. a cluster summary;
4. a page summary including governed no-page groups;
5. unresolved / Search-required work;
6. a dictionary explaining fields, metrics, decisions and technical traceability.

All phrase states must reconcile. Active, assigned, unresolved, excluded, deferred, URL and governed no-URL totals must be mechanically derived from current authority. Phrase keys and stable IDs must remain unique where their contract requires uniqueness.

## 3. Mandatory owner-reviewed build protocol

A future execution entering this section must follow this order rather than improvising the workbook from whatever table is easiest to open.

### 3.1 Read current methodology before touching the workbook

Before materialization:

1. read this gate;
2. read current Step19 packaging rules;
3. read current Step3 / Step5 / Step8 acquisition-preservation rules;
4. review current official Yandex terminology relevant to the collected metric;
5. review current professional semantic-core / clustering / mapping presentation guidance when the output design may have changed materially;
6. identify current job-specific canonical authorities separately from universal methodology.

```text
OLD MEMORY OF HOW A SEMANTIC CORE LOOKS
!=
CURRENT METHOD REVIEW
```

### 3.2 Audit existing data before collecting anything new

First answer from persisted evidence:

- do we already have every phrase occurrence / unique phrase needed for the promised core?
- do we already have phrase-level demand/frequency values?
- do we have region, device, operator/method semantics and acquisition date?
- do we have source IDs / provenance and raw or durable raw-equivalent evidence?
- do we have final status, cluster/task, intent, business boundary and page mapping from current authority?
- which values are genuinely absent versus merely not surfaced in the current client view?

Do not call a provider merely because an old workbook omitted a field.

```text
FIELD NOT VISIBLE IN OLD CLIENT FILE
!=
FIELD NOT PRESENT IN PROJECT EVIDENCE
```

New acquisition is allowed only for a genuinely new information requirement, not to repair our own earlier persistence/materialization omission.

### 3.3 Preserve the full research universe

The full semantic core is not only the final active subset.

The workbook must preserve the acquired universe required by the sold contract, including excluded, deferred and unresolved rows when they remain part of audit/review truth.

The active-core sheet is a derived working view, not a replacement for the full phrase universe.

```text
FULL PRESERVED UNIVERSE
!=
ACTIVE CORE ONLY
```

No phrase may disappear merely because it is low-frequency, excluded, deferred, association-only, uncertain or currently unresolved.

### 3.4 Join current semantic truth to demand/provenance mechanically

Use stable phrase keys / normalized exact phrase joins as declared by the current project contract.

Required coverage for every retained phrase includes, when available/request-defined:

- phrase text;
- observed count(s);
- popular/result vs similar/association role;
- region / region ID;
- device filter;
- operator mode;
- acquisition method/report type;
- acquisition/snapshot date;
- source/request IDs;
- raw/durable evidence lineage;
- source occurrence count/history;
- aggregation rule.

```text
PHRASE KEY JOIN COVERAGE = 100%
SILENT DEMAND / PROVENANCE LOSS = 0
```

### 3.5 Derive display fields without inventing analytical truth

Allowed client-view derivations include:

- Russian display labels for existing machine codes;
- representative phrase chosen only from real members of the accepted cluster;
- readable cluster name based on a real representative/member phrase;
- deterministic rank inside an already accepted cluster/page;
- cluster/page summaries from accepted rows;
- operational display priority derived from accepted status/action/readiness/uncertainty under an explicitly bounded rule.

Forbidden:

- inventing a cluster/page decision because the workbook needs a value;
- translating an internal unit ID into a made-up semantic label unrelated to real member phrases;
- filling a missing URL when current authority intentionally says no standalone page / outside scope / deferred / unresolved;
- silently changing intent, business boundary, page ownership or structural action during formatting.

### 3.6 No-page and unresolved are first-class outcomes

A blank final URL may be an intentional governed result, not a missing join.

The client view must distinguish at least:

```text
HAS FINAL URL
NO STANDALONE PAGE
OUTSIDE SCOPE / NO ACTION
DEFERRED PENDING EVIDENCE
SEARCH / EVIDENCE REQUIRED
```

Never fill these rows with a convenient page simply to make the workbook look complete.

### 3.7 Build the client display layer separately from machine truth

For a Russian client artifact:

```text
CLIENT_DISPLAY_LANGUAGE = RUSSIAN
CANONICAL MACHINE VALUE != CLIENT DISPLAY VALUE
TECHNICAL API TERM != CLIENT TERM
PROJECT ENUM != CLIENT EXPLANATION
```

Primary sheet titles, headers, statuses, intent, business boundaries, page roles, recommendations, readiness, uncertainty, priorities, metric descriptions and explanatory notes must use clear Russian professional language.

Stable IDs, URLs, filenames, source IDs and explicit technical-code fields may retain machine/Latin values for traceability only.

Every client-visible enum requires an explicit deterministic display map. Unknown unmapped enum = build failure.

### 3.8 Materialize through code, not manual workbook patching

The workbook must be generated from current authority by a reproducible materializer.

If owner review finds a defect:

```text
FIX GENERATOR / DISPLAY MAP / VALIDATOR
-> REGENERATE XLSX
-> RE-RUN QA
```

Do not hand-edit a few XLSX cells and leave the generator capable of reproducing the same defect.

### 3.9 QA must have separate layers

A semantic core cannot PASS from one generic QA flag.

Required independent layers:

1. **Data QA** — row counts, uniqueness, authority equivalence, phrase→demand/provenance joins, unresolved/no-page accounting, stale-authority leakage.
2. **Workbook QA** — required sheets, order, filters, freeze panes, widths, wrapping, numeric fields, formulas/openability, hidden-column checks.
3. **Recipient-language QA** — worksheet titles + headers + ordinary client cells + human explanations; technical fields use explicit allowlist only.
4. **Visual QA** — actual rendered/visible inspection of every required sheet, not only PNG existence.
5. **Owner/recipient review** — the real specialist task can be performed without repository archaeology or interpretation of internal codes.
6. **Persistence QA** — commit, remote readback, binary identity/hash/size and current-state update.

```text
AUTOMATED QA PASS
!=
OWNER ACCEPTANCE
```

### 3.10 Persist methodology references with the deliverable

The project must preserve direct links and a short explanation of what each source governed:

- official Yandex terminology / metric semantics;
- operator/measurement boundaries;
- clustering practice;
- keyword/page mapping practice;
- intent boundaries;
- cannibalization/overlap caution where applicable.

Generic SEO sources do not override project-specific accepted analytical authority.

## 4. Frequency semantics

Every displayed demand value must state the actual report/method, region, device filter, operator mode, snapshot and aggregation rule. A value collected without operators must not be called exact frequency or a traffic forecast.

Official Russian client terminology takes precedence in the display layer: «Вордстат», «Топы запросов», «популярные запросы», «похожие запросы», «число запросов», «регион», «тип устройства», «все устройства», «без операторов».

Technical acquisition identifiers such as `GetTop`, `DEVICE_ALL`, `results[]`, `associations[]`, `phrase` and `count` may remain in a clearly technical note, code column or provenance row. They must not replace the Russian client explanation.

When broad/no-operator counts are aggregated by cluster/page, overlapping queries mean simple sums are not unique market volume. If such a sum is shown, it must be clearly labelled as a non-additive relative indicator.

```text
BROAD / NO-OPERATOR COUNT
!=
EXACT PHRASE FREQUENCY
!=
TRAFFIC FORECAST

SUM OF OVERLAPPING QUERY COUNTS
!=
UNIQUE MARKET VOLUME
```

Demand may support filtering, rough sorting, representative selection and relative comparison inside an already accepted semantic structure. It must not override intent/business/page authority merely because the number is larger.

## 5. Client display language and traceability

For a Russian client artifact:

```text
CLIENT_DISPLAY_LANGUAGE = RUSSIAN
CANONICAL MACHINE VALUE != CLIENT DISPLAY VALUE
TECHNICAL API TERM != CLIENT TERM
PROJECT ENUM != CLIENT EXPLANATION
```

Primary headers, statuses, intent, business boundaries, page roles, recommendations, readiness, uncertainty, priorities, metric descriptions and explanatory notes must use clear Russian professional language.

A visible worksheet title is part of client presentation language:

```text
WORKSHEET TITLE IS PART OF CLIENT PRESENTATION LANGUAGE
CELL LANGUAGE QA != WHOLE-WORKBOOK LANGUAGE QA
```

Visible sheet names must use the recipient language and must not expose an internal project/API enum as their primary meaning.

Stable phrase/unit/source IDs, URLs, filenames, product names and explicit technical-code fields may retain Latin characters or machine codes. They are secondary traceability. The recipient must not need them to understand the decision.

Every client-visible categorical value must use a deterministic display map. An unknown enum without a Russian display label is a build failure.

## 6. Workbook usability

PASS requires:

- required sheets in the declared order;
- usable filters/tables and frozen headers;
- readable widths, wrapped long text and visible URLs;
- no hidden critical meaning;
- numeric demand cells and no broken formulas;
- correct Cyrillic rendering and no workbook repair warning;
- representative visual inspection of every required sheet;
- a recipient can understand phrase, cluster, intent, page/no-page reason and recommendation without repository knowledge.

The workbook should prioritize practical work over decoration. Main phrase tables must not depend on merged cells or presentation tricks that obstruct filtering/sorting.

## 7. Owner-reviewed known failure ledger

### Failure 1 — promised semantic core existed only as an incomplete/secondary materialization

**What failed:** a broader research workbook or historical export could exist while the promised standalone semantic core was not a complete recipient-ready artifact.

**Root cause:**

```text
DATA EXISTS SOMEWHERE IN PROJECT
WAS TREATED AS
PROMISED STANDALONE DELIVERABLE EXISTS
```

**Correct method:** create a distinct standalone XLSX from current final authorities, with full phrase, active, cluster, page, unresolved and dictionary views.

---

### Failure 2 — historical materialization risked becoming final semantic/page authority

**What failed:** an older generated semantic-core table contained useful demand/provenance but stale cluster/task/intent/page fields after later rebuild corrections.

**Root cause:**

```text
OLD FILE ALREADY HAS THE RIGHT COLUMNS
WAS TREATED AS
OLD FILE STILL HAS CURRENT TRUTH
```

**Correct method:** use old materialization only for fields whose authority remains valid; current final semantic/page authority always wins. Explicitly test stale-authority leakage.

---

### Failure 3 — apparent missing frequency was not first distinguished from unsurfaced persisted frequency

**What failed:** the client view did not expose frequency, creating a risk of unnecessary recollection even though phrase-level Wordstat counts/provenance were already preserved elsewhere.

**Root cause:**

```text
NOT PRESENT IN CLIENT VIEW
WAS TREATED AS
NOT COLLECTED
```

**Correct method:** run a data audit before provider calls. Search all current preserved authorities/raw-normalized evidence and reconcile by phrase key first.

---

### Failure 4 — broad Wordstat measurement could be misunderstood as exact frequency

**What failed:** raw acquisition semantics such as no-operator `GetTop` can look like ordinary phrase frequency if not explained.

**Root cause:**

```text
NUMBER ATTACHED TO PHRASE
WAS TREATED AS
EXACT PHRASE FREQUENCY
```

**Correct method:** always expose metric/report type, region, devices, operators, snapshot and claim boundary. Never call broad/no-operator counts exact-match frequency or traffic forecast.

---

### Failure 5 — overlapping broad counts could be over-interpreted when summed

**What failed:** a cluster/page sum can look like total market volume even though member queries overlap.

**Root cause:**

```text
ARITHMETIC SUM
WAS TREATED AS
UNIQUE DEMAND
```

**Correct method:** label such sums explicitly as non-additive relative indicators and accompany them with count/max/median/top-phrase context.

---

### Failure 6 — internal technical schema leaked into client-facing semantic core

**What failed:** a workbook passed phrase reconciliation, final-authority equivalence, demand equivalence, stale-materialization protection, sheet/filter/freeze checks and visual rendering, but still exposed internal English API/project codes as normal recipient terminology.

**Root cause:**

```text
INTERNAL REPRESENTATION WAS TREATED AS CLIENT PRESENTATION
TECHNICAL TRACEABILITY WAS CONFUSED WITH CLIENT READABILITY
SPECIALIST RECIPIENT WAS TREATED AS PERMISSION TO DUMP INTERNAL SCHEMA
```

**Correct method:** client display uses clear Russian professional wording; machine/API/project codes remain secondary traceability only. Language QA scans every client-visible enum and ordinary presentation surface.

---

### Failure 7 — cell-language QA missed worksheet titles

**What failed:** the first language correction translated headers/cells but still left an internal English status code in a visible sheet name.

**Root cause:**

```text
CELL LANGUAGE QA
WAS TREATED AS
WHOLE-WORKBOOK LANGUAGE QA
```

**Correct method:** recipient-language QA covers:

```text
SHEET TITLES
+ HEADERS
+ ORDINARY CLIENT CELLS
+ HUMAN EXPLANATIONS
```

---

### Failure 8 — automated QA could PASS before owner-recipient use was actually tested

**What failed:** data, formatting and visual checks did not guarantee that the workbook was natural and immediately understandable for a Russian SEO specialist.

**Root cause:**

```text
FORMAL QA PASS
WAS TREATED AS
RECIPIENT TASK PASS
```

**Correct method:** after automated QA, perform owner/recipient review of the actual workbook as a working instrument: terminology, sheet navigation, filtering, cluster/page interpretation, unresolved/no-page reasons, metric meaning and technical-code burden.

---

### Failure 9 — future packaging could require recollection because early acquisition discarded useful fields

**What failed class:** a late semantic-core build can discover that provider data once returned was never preserved completely.

**Root cause:**

```text
EARLY ACQUISITION OPTIMIZED FOR IMMEDIATE ANALYSIS
INSTEAD OF
PRESERVING REUSABLE FINAL-DELIVERABLE DATA
```

**Correct method:** Step3/Step5 preserve every returned occurrence and all available request/metric/provenance/completeness fields; Step8 carries a 100% phrase→demand/provenance handoff.

```text
COLLECT ONCE
PRESERVE COMPLETELY
DERIVE MANY VIEWS LATER
```

---

### Failure 10 — representative/cluster display risked being chosen from convenience rather than accepted membership

**Failure prevented:** a display label or main phrase could be invented from an internal structural ID or selected only by the largest count, distorting semantic meaning.

**Correct method:** representative phrase must be a real accepted member. Selection may consider semantic centrality, readability and bounded demand; demand does not redefine the accepted cluster. Any manual override must still choose a real member.

---

### Failure 11 — intentionally absent URL could be mistaken for missing mapping

**Failure prevented:** rows governed as no-standalone/outside/deferred could be “completed” with an invented page.

**Correct method:** preserve and display the governed reason. Missing URL is only a defect when authority says a URL should exist.

## 8. Permanent non-repeat controls

Before materialization:

```text
CURRENT AUTHORITIES DECLARED = true
STALE MATERIALIZATION FINAL AUTHORITY = false
EXISTING DATA AUDIT = PASS
NEW PROVIDER CALL REQUIRED BY GENUINELY NEW INFORMATION = true | false
FULL PHRASE UNIVERSE ACCOUNTED = true
DEMAND / PROVENANCE JOIN PLAN = 100%
RECIPIENT DISPLAY LANGUAGE DECLARED = true
```

During materialization:

```text
SEMANTIC / PAGE TRUTH CHANGED BY FORMATTER = 0
UNRESOLVED SILENTLY RESOLVED = 0
INTENTIONAL NO-PAGE ROWS FILLED = 0
REPRESENTATIVE NOT REAL CLUSTER MEMBER = 0
UNKNOWN CLIENT ENUM DISPLAY = 0
MANUAL XLSX PATCH AS CANONICAL FIX = false
```

Before delivery:

```text
DATA QA = PASS
WORKBOOK QA = PASS
RUSSIAN CLIENT-LANGUAGE QA = PASS
WORKSHEET TITLE LANGUAGE QA = PASS
VISUAL QA ALL REQUIRED SHEETS = PASS
OWNER / RECIPIENT TASK REVIEW = PASS
TECHNICAL TRACEABILITY = PRESERVED
UNEXPLAINED INTERNAL ENGLISH = 0
UNKNOWN UNMAPPED CLIENT ENUMS = 0
REMOTE GITHUB READBACK = PASS
```

## 9. Acquisition-to-deliverable continuity

Late materialization must not discover that fields already returned by the provider were discarded. The governing principle is:

```text
COLLECT ONCE
PRESERVE COMPLETELY
DERIVE MANY VIEWS LATER
```

Step 20 does not normalize provider recollection caused by earlier persistence loss. New acquisition is justified only by a genuinely new information requirement.

## 10. External source boundary

- Yandex Wordstat interface: https://yandex.ru/support2/wordstat/ru/interface/new
- Yandex Wordstat operators: https://yandex.ru/support2/wordstat/ru/content/operators
- Yandex AI Studio Wordstat GetTop API: https://aistudio.yandex.ru/ru/docs/search-api/operations/wordstat-gettop
- Yandex Webmaster query/site fit: https://yandex.ru/support/webmaster/ru/recommendations/targeting
- Semrush keyword clustering: https://www.semrush.com/blog/keyword-clustering/
- Semrush keyword mapping: https://www.semrush.com/blog/keyword-mapping/
- Ahrefs keyword intent: https://ahrefs.com/blog/keyword-intent/
- Ahrefs keyword cannibalization: https://ahrefs.com/blog/keyword-cannibalization/

Official sources govern Yandex terminology and product semantics. Professional SEO sources support clustering, intent and mapping practice. Neither may override accepted project authority.

## 11. Final gate

```text
CURRENT METHOD REVIEW = PASS
CURRENT AUTHORITY MANIFEST = PASS
EXISTING DATA AUDIT BEFORE RECOLLECTION = PASS
CANONICAL AUTHORITY RECONCILIATION = PASS
FULL PHRASE ACCOUNTING = PASS
DEMAND / PROVENANCE EQUIVALENCE = PASS
STALE AUTHORITY LEAKAGE = 0
INTENTIONAL NO-PAGE / UNRESOLVED GOVERNANCE = PASS
REPRESENTATIVE MEMBERSHIP = PASS
REQUIRED VIEWS = PASS
FREQUENCY CLAIM BOUNDARY = PASS
NON-ADDITIVE AGGREGATE LABELLING = PASS WHEN USED
WORKBOOK USABILITY = PASS
VISUAL QA OF EVERY SHEET = PASS
RUSSIAN CLIENT-LANGUAGE QA = PASS
CLIENT-FACING WORKSHEET TITLES = RECIPIENT LANGUAGE
UNEXPLAINED INTERNAL ENGLISH IN WORKSHEET TITLES = 0
UNEXPLAINED INTERNAL ENGLISH = 0
UNKNOWN UNMAPPED CLIENT ENUMS = 0
TECHNICAL TRACEABILITY = PRESERVED
OWNER / RECIPIENT TASK REVIEW = PASS
PERSISTED REMOTE READBACK = PASS
```
