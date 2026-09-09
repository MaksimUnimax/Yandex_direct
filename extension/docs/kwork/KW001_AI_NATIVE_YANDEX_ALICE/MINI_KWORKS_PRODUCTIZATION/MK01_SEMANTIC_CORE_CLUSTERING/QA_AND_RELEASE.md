# MK01 — QA AND RELEASE

Status: **ACTIVE / REQUIRED FOR EVERY MK01 DELIVERY AND PRODUCT REHEARSAL**

MK01 cannot pass on one generic green check. The following gates are independent.

## G0 — Scope / Yandex-only QA
PASS only when frozen site, region, included/excluded directions and business job match the delivered result; Google capability/data is neither required nor implied.

FAIL examples: generic «SEO for Yandex+Google» wording; silent region substitution; client-scope family omitted/added without revision.

## G1 — Acquisition / persistence QA
Verify request manifest vs executed provider actions; every governed returned occurrence is durably preserved; required provenance fields present; raw/equivalent evidence identities retained; provider limits/truncation explicit; readback completed.

`HTTP_SUCCESS_ONLY = FAIL`; `ONLY_ACCEPTED_ROWS_SAVED = FAIL`; destructive dedupe = FAIL.

## G2 — Accounting QA
Reconcile raw occurrences, normalized unique phrases, semantic states and all downstream counts. No unexplained row loss. Every final phrase must deterministically join to preserved demand/provenance.

## G3 — Semantic-cleanup QA
Adversarially sample/challenge KEEP, EXCLUDE and REVIEW states. KEEP needs positive business/semantic evidence; frequency alone cannot decide; uncertainty not erased.

Accounting PASS does not satisfy G3.

## G4 — Targeted Search QA
If Step08 executed, every Search observation has exact query, region/surface/time, preserved result evidence/projection status, routed question and bounded conclusion. No family-wide claim without explicit supported generalization. If no Search was justified, Step08 is explicitly NOT_REQUIRED.

## G5 — Clustering semantic QA
Check whole-phrase task coherence, current-domain profile use, cluster contracts, member consistency, material split/merge boundaries, representative phrase quality and unresolved edge cases. Cluster count must not be presentation-driven unless an explicit constraint is recorded. Corrections rebuild all derived fields/summaries.

## G6 — Deliverable data QA
Workbook/equivalent is generated from current authority. Required views from `DELIVERABLE_SPEC.md` exist. Source counts/joins reconcile. Active core is a subset of full universe; unresolved/excluded sets reconcile; no stale-authority leakage.

## G7 — Wordstat metric QA
Every visible demand metric has correct human meaning. Region, report/operator/device/snapshot semantics are described where material. Broad/no-operator counts are not labelled exact phrase frequency. Overlapping phrase sums are not called unique market volume or traffic forecast.

## G8 — Russian recipient-language QA
Scan sheet names, headers, status labels, explanations and ordinary cells. No unexplained internal English/API/status codes in the primary display layer. Technical IDs may remain as secondary traceability.

## G9 — Workbook physical/visual QA
Open/render the actual workbook; verify filters, frozen headers, widths, wrapping, numeric/text types, absence of broken references, readable long phrases, visible methodology, usable ordering and no hidden critical columns. File-opening alone is not PASS.

## G10 — Recipient-task QA
A reviewer unfamiliar with the repo must be able to answer from the delivered files alone: scope/region; what was collected; what is active; how groups differ; what remains uncertain; what was excluded; what Wordstat numbers mean; what the client should do next; what MK01 does not include.

Automated QA does not replace this gate.

## G11 — Provider-reuse / no-unnecessary-recollection QA
Before any repeat provider call, search persisted evidence. Missing display field in a workbook is not proof that source evidence was never collected. Recollection without a real evidence gap = FAIL.

## G12 — Persistence / remote readback QA
Final method/result artifacts: save → commit → remote readback. For structured client data, verify expected counts/identities and, where practical, blob/hash identity. Local-only completion = FAIL.

## Release classes

```text
METHOD_READY
= scope/input/general/per-step/deliverable/QA contracts complete and read back

REHEARSAL_PASS
= OKNO_MSK re-projected strictly as MK01 + all G0-G12 applicable gates PASS

CARD_READY
= REHEARSAL_PASS + economics/limits/price frozen + market recheck + card/portfolio assets accepted

PUBLISHED
= owner published card + published price/scope captured in repo + readback
```

## Fail handling

Any failure is classified against `ERRORS_AND_LESSONS.md`. Fix root cause/method/generator, identify full impact set, rebuild, rerun applicable gates. One patched example is not closure.

## Final release boundary

No MK01 artifact may claim page architecture, implementation TZ, competitor-gap completion, Alice/AEO, Google SEO, ranking guarantees or traffic/revenue guarantees.
