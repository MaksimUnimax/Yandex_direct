# MK01 — DELIVERABLE SPEC

Status: **METHOD CONTRACT + PHYSICAL LAYOUT VALIDATED ON OKNO_MSK**

## 1. Sold result

The client receives a standalone, recipient-readable semantic core for the frozen existing-site scope based on Yandex demand evidence, conservative cleanup and task-first clustering.

The result must answer without repository knowledge:

1. what scope/region was researched;
2. what phrases were preserved;
3. which phrases form the active core;
4. how active phrases are grouped and what each group means;
5. which phrases remain uncertain/deferred and why;
6. what was excluded at a useful client-facing level;
7. what the displayed Wordstat metrics mean;
8. what the client can do next with the result;
9. that Google/page architecture/AI are outside MK01.

## 2. Canonical recipient views

Physical workbook sheet names may be refined after the OKNO_MSK rehearsal, but equivalent views are mandatory.

### A. «Как пользоваться» / scope
Include site, primary region, frozen directions, exclusions, Yandex-only boundary, collection/analysis snapshot, short workflow and limitations.

### B. «Все запросы»
Full preserved client-visible semantic universe. Minimum semantic fields: phrase; displayed Wordstat demand metric(s) available under the method; semantic state; reason/meaning; cluster where applicable; uncertainty/review route where applicable; recipient-appropriate provenance indicator. Technical trace IDs may be secondary.

### C. «Рабочее ядро»
Only final active/accepted phrases with demand metric, cluster, task/intent meaning and useful sorting/filter fields. A technically assigned cluster with confirmed outside-task business fit is excluded from this view and retained in full/audit views. This is the primary working sheet.

### D. «Группы запросов»
Human-readable cluster summary: cluster/group name; task/meaning; member count; representative accepted phrases; useful demand indicators with non-additivity warning; material split/boundary note where needed. Working groups appear before excluded/outside-task groups.

### E. «На проверку»
Unresolved/Search-required/deferred/HOLD rows with reason and current state. No silent uncertainty deletion.

### F. «Исключено» or equivalent audit view
Enough excluded demand/reasons to prove that cleaning occurred deliberately without overwhelming the main working result with internal QA noise.

### G. «Методика и показатели»
Russian explanation of Wordstat metric semantics, region/device/operator/snapshot where applicable, association/role semantics, cluster/state dictionary, limitations and provenance meaning.

## 3. Short delivery summary

Separate recipient-facing text must state exact completed scope/counts from current authority after materialization, not vague «всё ядро» wording. Explain collection → cleaning → uncertainty → targeted Search if used → clustering → delivered result.

## 4. Display-language contract

For a Russian client:

- ordinary visible sheet names, headers, statuses and explanations are Russian;
- internal API/stage/status codes do not become the main display vocabulary;
- technical IDs remain only where useful for traceability;
- «частотность» wording must correspond to the actual Wordstat metric, not imply exact phrase volume unless the acquisition mode proves it.

## 5. Data-truth contract

The deliverable is generated from the current accepted semantic/demand/provenance/cluster authorities. No hand-edited workbook becomes a competing source of truth.

Before generation freeze:

```text
SOURCE FILE/STRUCTURE IDENTITIES
+ SOURCE COUNTS
+ CURRENT VERSION/TIMESTAMP
+ EXPECTED JOIN COUNTS
+ DISPLAY MAPPING VERSION
```

## 6. Explicit exclusions

No final query→URL ownership, architecture, create/split/merge recommendations, cannibalization audit, developer TZ, competitor gap report, Alice/AEO result, Google data or ranking guarantee.

## 7. Physical format

Validated base artifact is XLSX plus short delivery summary. The workbook has exactly these seven recipient sheets in this order: `Как пользоваться`; `Все запросы`; `Рабочее ядро`; `Группы запросов`; `На проверку`; `Исключено`; `Методика`. A full audit TSV may be stored losslessly compressed; it is not a substitute for the workbook. PDF is optional and is not required to make the semantic core usable.

## 8. Acceptance

Deliverable is accepted only after data, semantic, workbook, language, visual and recipient-task QA from `QA_AND_RELEASE.md` all pass. The seven-sheet layout is frozen by the OKNO_MSK standalone rehearsal. Exact commercial phrase/provider/review limits remain pending the economics gate; the rehearsal counts are measurements, not invented package limits.
