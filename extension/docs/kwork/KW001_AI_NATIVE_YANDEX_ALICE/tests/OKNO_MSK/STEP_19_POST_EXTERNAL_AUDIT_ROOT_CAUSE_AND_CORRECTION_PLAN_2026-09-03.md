# OKNO_MSK — Step19 post-external-audit root cause and correction plan

Date: 2026-09-03  
Status: **OWNER-DIRECTED CORRECTION / STEP19 REOPENED**

## Why this document exists

Step19 was initially sealed after its internal construction/readback QA because the analytical facts, row counts, claim boundaries and cross-deliverable consistency were correct. The owner then required an independent internet-based review of how client-facing SEO deliverables should actually be packaged and made executable. That external audit found that the analytical package was strong but the last mile from analysis to client use was incomplete.

This document is intentionally causal. It does not merely say what was missing. It records **why the missing pieces survived a pre-step methodology review that already contained many of the right ideas**, which false process assumptions allowed that to happen, and what execution sequence must replace the failed one.

---

# 1. External method evidence used for the post-audit

The correction is grounded in the following external materials in addition to the Level1/Level2 repo rules already used before Step19.

## Search Engine Land — How to make SEO reports more actionable

Source: https://searchengineland.com/make-seo-reports-more-actionable-479746  
Published: 2026-06-10.

Relevant method points:

- correct research is not the final output if stakeholders still do not know what should happen next;
- recommendations should identify the concrete action, business/relevance rationale and first move;
- important work should be sequenced with impact, effort, dependencies and timing in mind;
- execution ownership and acceptance/measurement should be made explicit where known;
- where estimates are not reliable, the report still needs a practical path to obtain them rather than silently stopping at analysis;
- raw exports should support the report rather than force stakeholders to reconstruct the answer themselves.

## Ahrefs — Keyword Mapping for SEO

Source: https://ahrefs.com/blog/keyword-mapping/

Relevant method points:

- group keywords by same/similar intent;
- map topics to existing pages before assuming new URLs are required;
- attach a concrete action to the mapped topic/page;
- a mapping artifact should be directly usable as a spreadsheet, not require the recipient to reconstruct the map from unrelated internal files.

## Ahrefs — How to Build an SEO Topical Map

Source: https://ahrefs.com/blog/seo-topical-map/

Relevant method points:

- separate main/support/sub-topics and map existing/new URLs deliberately;
- assess brand/business relevance and demand rather than expanding the site mechanically;
- follow-up implementation work belongs in an execution workflow after mapping;
- spreadsheet templates are a practical client/team interface for the map.

## Semrush — What is an SEO report?

Source: https://www.semrush.com/blog/what-is-an-seo-report/

Relevant method points:

- executive summary, performance/context, specific recommendations and a readable presentation layer are distinct parts of a useful client report;
- a client report should guide future action instead of exposing only analyst-working files.

## Yandex Webmaster — Search-query monitoring / URL analytics

Sources:

- https://yandex.ru/support/webmaster/ru/service/popular-queries
- https://yandex.ru/support/webmaster/ru/service/queries-export

Relevant method points:

- Yandex Webmaster can provide query/URL-level impressions, clicks, CTR and average position;
- extended URL/query export contains date, host, URL, query, region, clicks, impressions and position;
- therefore a post-implementation measurement protocol can be specified without inventing performance targets, while marking private Webmaster data as a future optional/authorized source.

## Yandex Webmaster — Site structure

Source: https://yandex.ru/support/webmaster/ru/recommendations/site-structure

Relevant method point: page/section roles and internal linking should remain understandable to both users and the search robot, which supports the existing Step19 emphasis on owner boundaries and specific internal-link handoffs.

---

# 2. What was good and is NOT being discarded

The correction does not reopen the semantic research, ordinary Search evidence, current-site architecture, Step17 AI acquisition or Step18 analytical priority.

The following Step19 decisions remain sound:

- one canonical analytical truth instead of multiple manually maintained copies;
- 15 bounded primary client directions;
- 2332 active phrase/page rows with 19 unresolved preserved and zero silent drops;
- 8/8 bounded Search-vs-AI cases without sitewide or longitudinal overclaiming;
- 34/34 analytical actions and 112/112 package trace;
- 0 supported new-page actions and 0 destructive actions under the accepted evidence;
- P1/P2/P3 as analytical importance rather than a fabricated sprint/calendar schedule;
- no guessed owner, effort, capacity, business value or KPI targets;
- zero new provider calls in Step19.

The failure was **not bad upstream analysis**. It was a packaging/execution-schema failure after the analysis.

---

# 3. Root cause: why the first Step19 execution was not finished correctly even though the pre-step research contained the right requirements

## Root cause A — canonical source and materialized client view were conflated

The pre-step methodology explicitly planned a physical `03_SEMANTIC_CORE_WORKBOOK.xlsx` and explicitly said the delivery format must be chosen for client usability.

During execution, however, the following safety idea dominated:

```text
DO NOT MANUALLY COPY 2332 ROWS
BECAUSE A SECOND COPY CAN DIVERGE
```

That safety idea was correct, but I applied it too broadly and silently transformed it into:

```text
DO NOT MATERIALIZE A SECOND CLIENT VIEW AT ALL
```

That was wrong.

The correct distinction is:

```text
CANONICAL SOURCE OF TRUTH
!=
GENERATED / REPRODUCIBLE MATERIALIZED CLIENT VIEW
```

A generated workbook can contain all 2332 current rows without becoming a competing authority if:

1. its source files and source commit/hash are recorded;
2. it is generated mechanically, not hand-maintained;
3. it is labelled DERIVED / MATERIALIZED;
4. corrections are made upstream and the workbook is regenerated;
5. QA proves exact row/ID reconciliation.

Because this distinction was absent as a hard gate, Step19 accepted a Markdown instruction telling the client/analyst how to JOIN Step8+10+11 instead of actually giving the client the joined workbook.

**Failure class:**

```text
CANONICALITY SAFETY
OVERRODE
CLIENT USABILITY
```

**Permanent control:**

```text
CANONICAL SOURCE != MATERIALIZED CLIENT VIEW
MATERIALIZED VIEW MUST BE REPRODUCIBLE, NOT MANUALLY AUTHORITATIVE
```

---

## Root cause B — a logical deliverable was incorrectly allowed to satisfy a physical-artifact requirement

The pre-step planned `03_SEMANTIC_CORE_WORKBOOK.xlsx`, filters/freeze panes/readability and file-openability QA. Yet the execution manifest and final QA did not mechanically require the actual file extension/artifact class to exist before PASS.

The first pass therefore checked:

```text
LOGICAL DELIVERABLE EXISTS
ROW COUNTS RECONCILE
CLAIMS ARE SAFE
```

but did not hard-fail on:

```text
REQUIRED PHYSICAL CLIENT FILE DOES NOT EXIST
```

That is why a Markdown join guide could be counted as logical deliverable 03 even though the client-facing workbook itself was absent.

**Failure class:**

```text
LOGICAL DELIVERABLE != PHYSICAL CLIENT ARTIFACT
```

**Permanent control:** every deliverable contract must separately declare and validate:

```text
logical_name
physical_artifact_type
required_filename_or_equivalent
required_sheets/sections
openability
client-use test
machine reconciliation
```

No substitute file type satisfies the gate unless the contract is explicitly revised before execution with a reason.

---

## Root cause C — `do not guess unknowns` was incorrectly treated as `do not create the calibration interface`

Step18 correctly found that implementation owner, effort, capacity and final calendar sequence were unknown. Step19 correctly refused to fabricate them.

The error was stopping there.

The correct method is:

```text
UNKNOWN VALUE
!=
ABSENT FIELD
!=
ABSENT CALIBRATION PROCESS
```

A client/team-ready package can and should contain the fields even when their current values are:

```text
OWNER = TO_CALIBRATE
EFFORT = TO_CALIBRATE
CAPACITY = TO_CALIBRATE
TIMING = TO_CALIBRATE
```

and should explain exactly who/what evidence is allowed to fill them and what becomes legal after they are filled.

The initial `07_PRIORITY_ACTION_PLAN.tsv` preserved the unknowns honestly, but it did not give the client/implementer a 112-row editable calibration board to turn those unknowns into a real production sequence.

**Failure class:**

```text
NO GUESS
WAS TREATED AS
NO EXECUTION-CALIBRATION INTERFACE
```

**Permanent control:** when execution inputs are unknown, emit a calibration-ready work-package view with explicit unknown values and completion rules. Never omit the fields/process.

---

## Root cause D — Step18 already taught `RECHECK TRIGGER != SUCCESS METRIC`, but Step19 did not operationalize the lesson

Step18 permanent lessons already said that recheck triggers are not a measurement plan. Step19 repeated that sentence in limitations, but did not convert it into a client/team measurement table.

This is an important causal failure: **remembering a rule in prose is not the same as carrying the rule into the output schema**.

A correct Step19 package needs a measurement layer that distinguishes:

1. implementation acceptance — was the requested change actually applied correctly?
2. baseline required — what evidence should be captured before/at implementation where available?
3. early search signals — indexing/role/query-URL association/impressions/clicks/CTR/position when authorized data exists;
4. later business signals — visits/conversions/leads only if the client provides appropriate first-party data;
5. observation window — real implementation/client choice, not invented by the analyst when no basis exists;
6. decision rule — what result would cause keep/revise/reopen/research, without promising ranking or revenue.

**Failure class:**

```text
RULE DISCLOSED IN LIMITATIONS
!=
RULE MATERIALIZED IN EXECUTION SCHEMA
```

---

## Root cause E — internal correctness was used as a proxy for client usability

The internal QA was strong at detecting:

- missing IDs;
- row-count mismatch;
- superseded authority leakage;
- forbidden AI claims;
- guessed implementation variables;
- silent drops.

But it did not ask a sufficiently brutal client-use question:

> Can a normal client/implementer open the supplied package and use the essential semantic map, action queue and next-step workflow without understanding repo lineage or performing manual joins?

If that test had been mandatory, the first-pass Markdown semantic “workbook” would have failed immediately.

**Failure class:**

```text
TRACEABILITY PASS
!=
CLIENT USABILITY PASS
```

**Permanent control:** Step19 QA needs a separate **CLIENT-INDEPENDENT-USE GATE** in addition to analytical/readback QA.

---

## Root cause F — presentation quality was treated as secondary to analytical integrity

The first pass produced correct Markdown/TSV/JSON views, but not one polished external report and one actual workbook that can be handed to a non-repo user.

The error was not “Markdown is bad.” Markdown/TSV/JSON are excellent internal durable artifacts. The error was treating them as sufficient **external delivery surfaces**.

Correct architecture:

```text
INTERNAL DURABLE AUTHORITY / TRACE FILES
+
MATERIALIZED CLIENT WORKBOOK
+
POLISHED CLIENT NARRATIVE REPORT
```

Neither replaces the other.

---

# 4. Correct Step19 execution method — detailed future workflow

The following sequence replaces the failed shortcut.

## Phase 1 — freeze analytical authority and delivery contract separately

First freeze the accepted analytical inputs by exact current state/commit. Then create a delivery contract that lists **logical outputs and physical artifacts independently**.

The contract must answer:

- What is canonical source truth?
- What will be generated from it?
- Which generated file is for the client?
- Which generated file is for implementation/calibration?
- Which raw artifacts remain appendices only?
- Which output is narrative, which is tabular, which is machine-readable?

No writing of the client summary starts until these are frozen.

## Phase 2 — build one normalized canonical client model

Join accepted evidence into a normalized model using stable IDs/keys. For semantic rows the exact phrase is a stable join key only where upstream authorities say so; action/work-package IDs remain their own keys.

The model must preserve unknowns and limitations rather than filling them heuristically.

## Phase 3 — generate, do not hand-copy, the client workbook

Materialize the client workbook automatically from canonical inputs.

At minimum the workbook must contain:

- README / how to use;
- 02 business/page model;
- 03 full materialized semantic core;
- 04 Search-vs-AI matrix;
- 05 page action map;
- 06 observed source/competitor evidence;
- 07 analytical priority plan;
- 112-package execution calibration board;
- measurement protocol.

The semantic sheet must contain the actual rows needed for client work. It must not tell the recipient to reconstruct them elsewhere.

Generated workbook provenance must include source commit/hash and source file names. Upstream sources remain canonical; the workbook is a reproducible view.

## Phase 4 — materialize the execution-calibration board even when execution facts are unknown

Create one row per executable/recheck package, not one row per accounting batch.

Required fields include:

```text
package_id
source_action_id
package_kind
analytical_priority
what_to_do
target/scope
dependency/dependency_role
implementation_owner
effort
capacity/timing
calibration_state
measurement_class
implementation_acceptance_check
baseline_required
future_metric_source
observation_window
decision_rule
recheck/blocker
```

If owner/effort/capacity/timing are not known, store `TO_CALIBRATE`. That is a valid state. It must not be converted to zero/low/easy/first sprint.

A NOW/NEXT/LATER committed sequence is prohibited until real calibration inputs exist. Before calibration, the only valid sequence is dependency-aware analytical readiness, labelled accordingly.

## Phase 5 — build the measurement protocol before claiming “actionable” delivery

For each measurement class, define:

- what implementation completion means;
- what baseline should exist if data is available;
- which metrics are appropriate, not guaranteed;
- what first-party source may be used when authorized;
- what observation window is required or still TO_CALIBRATE;
- what triggers review/revision.

Never manufacture numeric targets merely to make the table look complete.

## Phase 6 — produce the polished narrative report from reconciled tables

Only after 02–08 + calibration + measurement reconcile should the executive/client report be generated.

The report must let a decision-maker understand:

- main opportunity/constraint;
- what current architecture should remain;
- what should change;
- what must not be changed yet;
- which work is analytically most important;
- what is blocked by calibration;
- how implementation will be checked;
- what the analysis does not prove.

Raw exports/technical lineage belong in appendices/supporting files, not in the main narrative unless necessary to justify a decision.

## Phase 7 — client-independent-use QA

Before PASS, ask and mechanically test where possible:

```text
CAN CLIENT OPEN THE WORKBOOK? = true
CAN CLIENT FILTER/SORT CORE TABLES? = true
IS FULL SEMANTIC MAP MATERIALIZED? = true
DOES CLIENT NEED TO MANUALLY JOIN REPO FILES? = false
ARE 112 PACKAGES ADDRESSABLE? = true
ARE UNKNOWN EXECUTION INPUTS EXPLICIT? = true
IS THERE A MEASUREMENT PROTOCOL? = true
IS THERE A POLISHED NARRATIVE REPORT? = true
CAN REPORT BE UNDERSTOOD WITHOUT REPO HISTORY? = true
```

This QA is separate from traceability/reconciliation QA.

## Phase 8 — persistence and readback

Persist:

1. canonical text/machine audit artifacts;
2. generated workbook;
3. generated client report;
4. source/provenance manifest with hashes;
5. generation QA/readback evidence.

Read binary artifacts back or independently verify their hash/size/openability after the commit. A successful local export is not enough.

## Phase 9 — only then reseal Step19

Step19 PASS requires both:

```text
ANALYTICAL/TRACKING INTEGRITY PASS
AND
CLIENT MATERIALIZATION / EXECUTION-HANDOFF PASS
```

Step20 remains a separate final QA step and is not consumed by Step19 correction.

---

# 5. Corrections required in the reopened current job

The reopened Step19 must now add, without new provider calls:

1. a mechanically materialized full semantic client view from accepted Step8/Step11 (and Step10 where needed) authority;
2. an actual `.xlsx` client workbook, with filters/frozen headers/readable sheet names and explicit source provenance;
3. a 112-row execution calibration board with `TO_CALIBRATE` fields rather than guessed values;
4. a measurement protocol that operationalizes the seven Step18 measurement classes and distinguishes acceptance/baseline/metrics/window/decision rule;
5. a polished standalone client narrative report (`.docx` and PDF rendering) that does not require repo knowledge;
6. an updated client delivery message pointing to the physical workbook/report instead of asking the client to join internal files;
7. updated Step19 QA with a separate client-usability gate;
8. final GitHub persistence/readback/checksum verification for text and binary artifacts;
9. a Level1 non-repeat method/lesson record that preserves the causal mechanism without copying current-job specifics.

No new Wordstat/Search/GenSearch/Webmaster/Metrika/Direct call is required to correct these packaging defects.

---

# 6. Non-repeat summary

The core mistake is summarized by five permanent equations:

```text
GOOD RESEARCH + CORRECT CONSTRAINTS != CORRECT EXECUTION SCHEMA
CANONICAL SOURCE != MATERIALIZED CLIENT VIEW
UNKNOWN VALUE != ABSENT FIELD / ABSENT CALIBRATION PROCESS
LOGICAL DELIVERABLE != PHYSICAL CLIENT ARTIFACT
TRACEABILITY PASS != CLIENT USABILITY PASS
```

The first Step19 pass failed because these distinctions were not expressed as hard acceptance gates. The correction must make them executable requirements, not merely explanatory prose.
