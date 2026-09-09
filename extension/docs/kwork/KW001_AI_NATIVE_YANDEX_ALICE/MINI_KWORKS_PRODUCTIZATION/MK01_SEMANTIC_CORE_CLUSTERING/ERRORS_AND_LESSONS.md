# MK01 — ERRORS AND LESSONS EXTRACTED FROM KW-001

Status: **ACTIVE NON-REPEAT LEDGER FOR MK01**

This file records only failure classes that can materially affect MK01. Concrete OKNO_MSK examples remain Level 2.

| ID | Failure class | Root cause / false assumption | Corrected MK01 control | Main step |
|---|---|---|---|---|
| E01 | Evidence silently changed the sold task | evolving analysis rewrote success criteria | freeze site/region/scope/exclusions/output before acquisition | 00 |
| E02 | One discovery pass treated as complete current site | success confused with completeness | timestamp site model; do not prove broad absence from one weak route | 01 |
| E03 | Seed treated as final relevant keyword | probe treated as object of selection | seed has information purpose; judge returned phrases downstream | 02 |
| E04 | Provider success treated as completed acquisition | request success confused with durable dataset | preserve every occurrence + provenance; read back and reconcile | 03 |
| E05 | Only examples/accepted phrases preserved | schema optimized for immediate analysis | preserve full returned universe | 03 |
| E06 | Dedupe destroyed occurrence history | normalized phrase replaced raw observations | raw occurrences remain; normalized layer separate | 03 |
| E07 | Family screening claimed as full cleanup | category coverage replaced member accounting | Step04 is triage only; Step06 accounts rows | 04/06 |
| E08 | Low-frequency phrase auto-excluded | volume mistaken for relevance | low count alone never excludes | 04/06 |
| E09 | High count/association auto-kept | demand signal mistaken for semantic fit | KEEP requires positive evidence | 04/06 |
| E10 | Second acquisition became recursive collection | more collection assumed more completeness | Step05 only for named unresolved information gain | 05 |
| E11 | Default KEEP fallthrough | no rejection interpreted as relevance | no default KEEP; ambiguity remains REVIEW | 06 |
| E12 | Arithmetic QA substituted for semantic QA | counts mistaken for decision correctness | independent semantic QA required | 06/09 |
| E13 | Unsupported symmetric REVIEW taxonomy invented | evaluation dimension confused with evidence route | only states with real source/action are allowed | 07 |
| E14 | REVIEW rows simplified away | uncertainty treated as process noise | executable Search route or explicit deferred state | 07 |
| E15 | Non-exact duplicates auto-merged | lexical similarity treated as same task | preserve unresolved until evidence justifies merge | 07/09 |
| E16 | Exact Search observation generalized | bounded observation treated as family evidence | exact claim stays exact unless generalization declared | 08 |
| E17 | Normalized Search export treated as raw evidence | projection conflated with provider body | raw/projection state explicit | 08 |
| E18 | Visible keyword token drove clustering | lexical clue replaced full user task | whole phrase + expected result/task first | 09 |
| E19 | Universality stripped necessary domain rules | reusable method treated as domain-free | current site/business/domain profile mandatory | 09 |
| E20 | Cluster count invented for neatness | presentation preference became evidence | count emerges unless external constraint declared | 09 |
| E21 | Corrected cluster ID but stale dependent fields remained | identifier-only patch | atomically rebuild all derived fields/summaries | 09 |
| E22 | Correct data existed but promised standalone workbook did not | data somewhere in repo treated as deliverable | generate recipient-ready core from current authority | 10 |
| E23 | Historical pretty workbook reused | right columns mistaken for current truth | current authority wins; test stale-authority leakage | 10 |
| E24 | Missing visible frequency triggered recollection risk | not visible mistaken for not collected | audit preserved evidence before provider recall | 10 |
| E25 | Broad Wordstat count labelled exact | any number treated as exact frequency | expose method/region/operator/snapshot semantics | 10 |
| E26 | Cluster sums read as market volume | overlapping query sums treated as unique demand | label non-additive aggregates as relative only | 10 |
| E27 | Internal English/API enums leaked | traceability mistaken for client language | Russian display layer; technical codes secondary | 10 |
| E28 | Cell-language QA missed sheet titles | cell scan treated as whole workbook | scan sheet names, headers, cells, explanations | 10 |
| E29 | Automated QA treated as recipient acceptance | formal checks replaced actual task review | independent recipient-use review | 10 |
| E30 | Representative phrase chosen for convenience | internal ID/largest number replaced semantic meaning | representative must be real accepted suitable member | 10 |
| E31 | Technically assigned outside-task cluster leaked into active core | successful clustering was mistaken for business-fit acceptance | reconcile every assigned cluster with frozen offer; preserve OUTSIDE members in excluded/audit views | 09/10 |
| E32 | Search-control decision reported as an exact-universe join | total executed probes was conflated with phrase-level join coverage | report all decisions, exact-universe joins and outside-universe control anchors separately | 08/10 |
| E33 | Later workbook block destroyed earlier column widths | range styling was treated as block-local although width belongs to the whole column | define geometry once per sheet, render all sheets and correct at class level | 10 |
| E34 | Generic client handoff claimed optional Search had been performed | conditional method step was converted into unconditional past-tense delivery wording | use a required Search-status block with separate USED vs NOT_REQUIRED wording tied to current QA | packaging |
| E35 | Post-rehearsal product files still described validated decisions as future/pending | lifecycle state changed in roadmap but dependent contracts were not reconciled | after each product phase, audit status/future-tense statements across scope/input/deliverable/packaging authorities and commit the synchronized state | productization |
| E36 | Commercial phrase cap caused silent evidence truncation | package limit was mistaken for permission to discard provider-returned demand or keep only convenient rows | persist all useful authorized evidence; measure exact-deduped candidate universe; if over capacity expand paid review or freeze a documented scope revision before deep cleanup | commercial gate |

## Root-cause groups

A scope/observation overclaim; B transient/incomplete evidence; C signal != semantic decision; D accounting != semantic QA; E uncertainty erasure; F local patch != class fix; G generated view != authority; H internal traceability != client usability; I formal QA != recipient acceptance; J lifecycle/state drift across product artifacts; K commercial constraint != evidence destruction.

## Closure rule

`ONE BAD ROW FIXED != DEFECT CLASS CLOSED`. Closure requires root cause understood + control materialized + impact set rebuilt + regression passed + recipient effect checked where applicable.