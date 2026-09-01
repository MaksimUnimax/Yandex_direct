# KW001 OKNO_MSK — Step 13 competing-page / cannibalization diagnosis

Date: 2026-09-01

Status at write: **SEMANTIC + ACCOUNTING QA PASS / FINAL GITHUB CLOSURE READBACK PENDING**

## Goal

Determine whether Step-12 related-page pairs represent genuine competing-page conflicts, normal coexistence, hierarchy/support relationships, or evidence-insufficient cases. A related pair is not treated as cannibalization by default.

## Final accounting

- historical Step-12 pair universe: 195
- base pairs accounted: 195/195
- Phase-1 normal relationships closed without fresh Search: 168
- Phase-1 surviving pairs: 27
- surviving pairs mapped to query-family cases: 27/27
- query-family cases: 21
- cases closed presearch from current-page + 2332-row evidence: 5
- cases requiring fresh ordinary Yandex Search: 16
- fresh Search cases with usable evidence after reconciliation: 16/16
- current-site freshness discoveries added in QF016/QF017: 2 specialist URLs
- new pair relationships caused by those discoveries: 4
- effective final pair universe: 199
- effective final pair accounting: 199/199
- silent pair drops: 0
- current page-evidence URLs after extensions: 49

## Provider truth

Step 13 used ordinary Yandex Search only. No GenSearch/Alice provider call was used.

The original primary Search job produced 5 successful results and one `OUTCOME_UNKNOWN` for QF007. It was frozen. A separate recovery job completed original manifest items 7-16. After normal work was exhausted, owner-authorized QF007 retry 1/3 was explicitly executed and succeeded. Retries 2/3 are not needed and must not run.

- planned direct Search queries: 16
- usable direct Search results: 16/16
- historical `OUTCOME_UNKNOWN`: 1
- unresolved `OUTCOME_UNKNOWN`: 0
- provider boundaries started: 17
- successful useful results persisted: 16
- total Step-13 provider cost accounted: 8.296 RUB

## Diagnosis result

The canonical case-level diagnosis is `STEP_13_CONFLICT_DIAGNOSIS.tsv`.

No case is classified as confirmed harmful cannibalization. No merge, redirect, noindex, or other destructive remediation is authorized from Step-13 evidence.

The dominant pattern is legitimate coexistence with clearer primary responsibility:

- object/use-case specialist versus broad product/category page;
- specialist service versus product/accessory page;
- special-form page versus broad use-case page;
- narrow troubleshooting article versus broad guide;
- specific comparison/best article versus broad selection guide.

QF019 is intentionally bounded as an evidence limitation: the direct query `как открыть пластиковое окно` drifted toward external/emergency opening intent in the saved SERP and therefore does not strongly adjudicate the intended adjustment-vs-two-position troubleshooting pair. The current narrow-vs-broad page boundary is preserved without a harmful-conflict claim.

## Current-site freshness corrections

QF016 current-site re-read discovered:

`https://okno-msk.ru/okna-rehau/po-tipu-doma/panoramnoe-osteklenie-domov-i-kottedzhej/`

This specialist page is the most specific current owner for panoramic glazing of private/country houses/cottages. Two new specialist-to-original-candidate relationships were added to the Step-13 effective universe.

QF017 current-site re-read discovered:

`https://okno-msk.ru/verandy/panoramnye-okna-na-terrasu/`

This specialist page is the most specific current owner for panoramic terrace/veranda glazing. Two new specialist-to-original-candidate relationships were added.

These corrections change the final Step-13 page graph without rewriting the historical Step-12 195-pair provenance.

## Evidence-strength boundary

Step 13 has public current-page evidence and bounded public Yandex SERP snapshots, but no authorized query×URL historical performance series from Webmaster/Metrika for this site. Therefore:

- current ownership patterns can be diagnosed;
- normal coexistence and mismatch warnings can be identified;
- one snapshot cannot prove historical URL swapping, traffic loss, or harmful cannibalization;
- absence of two okno-msk URLs in one TOP10 snapshot is not proof that harmful cannibalization can never occur;
- destructive remediation is not justified without stronger evidence.

## Final remediation posture

Canonical recommendations are in `STEP_13_REMEDIATION_RECOMMENDATIONS.tsv`.

Result: preserve the related pages, sharpen responsibility where needed, incorporate the newly discovered QF016/QF017 specialist pages in Step 14, and do not perform destructive consolidation from Step-13 evidence.

## QA

`STEP_13_FINAL_PAIR_ACCOUNTING.json` reconciles the 199 effective pairs.

`STEP_13_QA.json` records:

- 199/199 effective pairs accounted;
- 21/21 cases finalized;
- 16/16 fresh-search cases usable;
- unresolved provider outcomes = 0;
- confirmed harmful cannibalization = 0;
- destructive remediation authorized = 0;
- GenSearch/Alice calls = 0;
- Step 14 executed = false;
- QA findings = 0.

`STEP_13_QA_FINDINGS.tsv` is intentionally header-only because the final QA produced zero findings.

## Roadmap handoff

After final GitHub readback of the closure artifacts and synchronized `STEP_13_CURRENT_STATE.json`:

- Step 13 = COMPLETE
- Step 14 = NEXT ALLOWED, NOT YET EXECUTED
- Step 14 must freeze the classic-search architecture using the 49-page current evidence universe and the 199-pair Step-13 effective graph, including the QF016/QF017 specialist discoveries.
