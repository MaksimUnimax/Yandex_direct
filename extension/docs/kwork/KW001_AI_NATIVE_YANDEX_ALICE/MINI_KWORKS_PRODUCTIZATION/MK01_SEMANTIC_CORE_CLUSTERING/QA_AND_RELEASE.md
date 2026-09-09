# MK01 — QA AND RELEASE

Status: **ACTIVE / REQUIRED FOR EVERY MK01 DELIVERY AND PRODUCT REHEARSAL**

MK01 cannot pass on one generic green check. The following gates are independent.

## G0 — Scope / Yandex-only QA
PASS only when frozen site, region, included/excluded directions and business job match the delivered result; Google capability/data is neither required nor implied.

## G1 — Acquisition / persistence QA
Verify request manifest vs executed provider actions; every governed returned occurrence is durably preserved; required provenance fields present; raw/equivalent evidence identities retained; provider limits/truncation explicit; readback completed.

## G2 — Accounting QA
Reconcile raw occurrences, normalized unique phrases, semantic states and all downstream counts. No unexplained row loss.

## G3 — Semantic-cleanup QA
Adversarially sample/challenge KEEP, EXCLUDE and REVIEW states. KEEP needs positive business/semantic evidence; frequency alone cannot decide; uncertainty not erased.

## G4 — Targeted Search QA
If targeted Search executed, every observation has exact query, region/surface/time, routed question and bounded conclusion. Reconcile exact-universe joins vs outside-universe controls. If not justified, Search is explicitly NOT_REQUIRED.

## G5 — Clustering semantic QA
Check whole-phrase task coherence, current-domain profile use, cluster contracts, member consistency, representative phrase quality and unresolved edge cases. Corrections rebuild all derived fields/summaries.

## G6 — Deliverable data QA
Required XLSX views and client PDF exist. All headline PDF counts/examples reconcile with current manifest/cluster authority. Active core, review and excluded partitions reconcile. No stale-authority leakage.

## G7 — Wordstat metric QA
Every visible demand metric in XLSX and PDF has correct human meaning. Broad/no-operator counts are not labelled exact phrase frequency; overlapping sums are not called unique market volume or traffic forecast.

## G8 — Russian recipient-language QA
Scan sheet names, headers, PDF headings, explanations and ordinary display text. No unexplained internal English/API/status/repository jargon. Terms such as Stage, Step IDs, authority, provenance, route state, failure class, exact-universe join, phrase key and request IDs are prohibited in ordinary client text unless explicitly needed and explained.

## G9 — Workbook + PDF physical/visual QA
Open/render the actual workbook and final PDF.

Workbook: filters, frozen headers, widths, wrapping, data types, readable long phrases, working-first ordering, no hidden critical columns.

PDF: render every page and inspect for clipping, overlap, broken glyphs, unreadable tables, bad page breaks, placeholders and inconsistent counts. File-opening alone is not PASS.

## G10 — Recipient-task QA
A reviewer unfamiliar with the repo must be able to answer from the delivered XLSX + PDF alone: scope/region; what was collected; what is active; how groups differ; what remains uncertain; what was excluded; what Wordstat numbers mean; what the client should do next; what MK01 does not include.

Automated QA does not replace this gate.

## G11 — Provider-reuse / no-unnecessary-recollection QA
Before any repeat provider call, search persisted evidence. Missing display field in a report is not proof that source evidence was never collected.

## G12 — Persistence / remote readback QA
Final method/result artifacts: save → commit → remote readback. Verify XLSX/PDF existence and expected identities/hashes where practical. Local-only completion = FAIL.

## Release classes

```text
METHOD_READY
= scope/input/general/per-step/deliverable/report/QA contracts complete and read back

REHEARSAL_PASS
= current job projected strictly as MK01 + semantic/workbook/report applicable gates PASS

CARD_READY
= REHEARSAL_PASS + economics/limits/price frozen + market recheck + card/portfolio assets accepted

PUBLISHED
= owner published card + published price/scope captured in repo + readback
```

## Fail handling

Any failure is classified against `ERRORS_AND_LESSONS.md`. Fix root cause/method/generator, identify full impact set, rebuild, rerun applicable gates. One patched example is not closure.

## Final release boundary

No MK01 artifact may claim page architecture, implementation TZ, competitor-gap completion, Alice/AEO, Google SEO, ranking guarantees or traffic/revenue guarantees.
