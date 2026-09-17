# KW-002 / BLOOD & SAND — STEP07 MAIN CHAT RETURN QA — 2026-09-17

Status: **REJECTED FOR STEP PASS / REWORK REQUIRED / FAILED ATTEMPT PRESERVED**

Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Owner-upload commit: `4b596b048d87a7e657bf3b84b715e7ee95980a3f`
Owner-upload base: `00230d7f1a8f83bb2aebfcbad89b896b122879d5`

## 1. Publication / transport QA

Owner relay itself passed.

`00230d7f... -> 4b596b...` is one fast-forward commit and contains exactly the six expected Step07 files, with no unrelated changes:

```text
COMPETITOR_GAP_CANDIDATES.csv                 686 data rows
STEP07_CANDIDATE_PROVENANCE_LEDGER.csv       1417 data rows
STEP07_COMPETITOR_COVERAGE_LEDGER.csv        32 data rows
STEP07_SOURCE_URL_LEDGER.csv                  1976 data rows
STEP07_EXECUTION_QA.md
STEP07_EXECUTION_HANDOFF_MANIFEST.json
```

Current Git blob identities:

```text
COMPETITOR_GAP_CANDIDATES.csv           5ce30e69a285abb8ece2d0a361329a7467d7bb87
STEP07_COMPETITOR_COVERAGE_LEDGER.csv   cfecaccae771cbe14e422c23aaf7a18ed3cff1c9
STEP07_SOURCE_URL_LEDGER.csv            d0e66c64d156d8f0eab028070c0efbb5241ebafd
STEP07_CANDIDATE_PROVENANCE_LEDGER.csv  54172cbd1a747899b7b19aae7d595109525a8fde
STEP07_EXECUTION_QA.md                   dbfc45b82b92a80e156fd87b181b51d039c99342
STEP07_EXECUTION_HANDOFF_MANIFEST.json  69b089e3432ad296e5b003e72835268344b414a2
```

Because the frozen staging directory equals the canonical final directory for all six files:

```text
OWNER_UPLOAD_COMPLETE = true
STAGING_READBACK_PASS = true
FINAL_PLACEMENT_COMPLETE = true
STAGING_CLEANUP = NOT_APPLICABLE
REMOTE_PUBLICATION_COMPLETE = true
```

Publication success does NOT imply analytical acceptance.

## 2. Work-declared execution state

Work correctly did not claim PASS.

```text
DISCOVERED_URLS = 1976
INSPECTED_URLS = 24
EXCLUDED_URLS = 1201
INACCESSIBLE_URLS = 751
UNRESOLVED_URLS = 0
ERROR_URLS = 0

PROVENANCE_ROWS = 1417
CANDIDATE_IDENTITIES = 686
```

Candidate statuses:

```text
ALREADY_PRESENT = 10
NEW_CANDIDATE = 400
NORMALIZED_DUPLICATE = 0
POSSIBLE_VARIANT = 3
OUT_OF_SCOPE = 207
AMBIGUOUS = 66
```

Only `S07A010 / kartaslov.ru` yielded inspected pages/candidates. The other authorized competitor surfaces yielded no inspected candidate evidence in this run.

Work hard QA already failed:

```text
COMPLETE_BOUNDED_COMPETITOR_UNIVERSE_PROCESSED = FAIL
EXECUTION_COMPLETENESS_DEMONSTRABLE = FAIL
STEP07 = INCOMPLETE
```

That alone blocks Step08.

## 3. Main Chat independent defect A — access failure was largely execution-environment failure

A material part of the 751 inaccessible rows is not source-controlled inaccessibility. The Work ledgers preserve failures such as:

```text
ClientHttpProxyError:403
url='http://127.0.0.1:...'
```

That is a Work/runtime proxy failure before reliable target-site inspection, not evidence that the competitor surface itself is unavailable.

Main Chat performed a lawful public-access control check after the Work return. Public pages were retrievable for multiple authorized competitors that the Work run had recorded as zero-inspected/network-inaccessible, including:

```text
https://slavyanskieoberegi.ru/
https://slavyanskieoberegi.ru/slavyanskie-oberegi/
https://happywitch.ru/catalog/products/amulety_i_talismany/
https://simvolroda.ru/
https://simvolroda.ru/catalog/ot-bolezney/
```

These surfaces expose material taxonomy such as male/female charms, runes, halls/`чертоги`, specific symbols, amulets/talismans, automotive charms and use-case categories.

Therefore:

```text
EXECUTION_ENVIRONMENT_NETWORK_FAILURE
!=
SOURCE SEMANTIC COVERAGE COMPLETE
```

For rows where no target response/access decision was actually obtained because the execution environment proxy failed, the next run must retry through a legitimate browser/cloud-browser route. Until retry, those cases are not a semantic closure.

## 4. Main Chat independent defect B — systematic candidate-semantic precision failure

The Work QA missed a second blocking defect: the candidate producer admitted arbitrary prose / literary quotations / broken dictionary fragments / metadata-like wording as `NEW_CANDIDATE` and routed them toward Step08.

Examples from the actual 686-row candidate authority include:

```text
10 схем вышивки крестиком для дизайна детской
[Муров:] Добрые люди обещали мне никогда не снимать с него [сына] медальона.
amuletum, с араб.].
amuletum]
А на груди висел серебряный медальон в виде перевёрнутой пентаграммы.
Антон Платов, «Славянские руны», 2001 г.
```

These examples are not patch targets. They prove a producer-level failure class.

Step07 is supposed to materialize semantic directions such as terminology, category/subcategory, product/service naming, use case, attribute, naming variant, problem/service/informational formulation. The Level2 contract allows concise contextual formulations, not arbitrary sentence-corpus material merely because an in-scope token appears.

Required correction:

```text
REPRESENTATIVE BAD ROWS != MANUAL PATCH TARGET
→ FIX / STRENGTHEN CANDIDATE-ELIGIBILITY PRODUCER
→ REPROCESS THE FULL AFFECTED 686-CANDIDATE / 1417-PROVENANCE UNIVERSE
→ THEN ADD NEWLY RETRIED COMPETITOR EVIDENCE
```

A candidate must be an independently meaningful semantic object suitable for later demand validation. Raw source prose remains provenance/context, not automatically a candidate identity.

At minimum, full-volume rework must distinguish:

```text
VALID COMPACT SEMANTIC DIRECTION
vs
LITERARY / EXAMPLE SENTENCE
BROKEN ETYMOLOGY / FRAGMENT
AUTHOR / BOOK / CITATION METADATA
GENERIC UI / NAVIGATION NOISE
INCIDENTAL TOKEN MENTION
UNRELATED CONTENT
```

Long body text may yield a derived candidate only when a reproducible concise source span/formulation exists and the transformation is explicit. The original full wording must remain in provenance.

Because this is systematic, the present `NEW_CANDIDATE = 400` set is NOT safe as a Step08 queue.

## 5. Main Chat independent defect C — Work QA document self-contradiction

The current Work contract and handoff correctly contain six files, but `STEP07_EXECUTION_QA.md` still contains stale wording referring to:

```text
All seven deliverables
Single-directory seven-file handoff
```

The actual handoff manifest and remote commit contain six files.

This does not corrupt the CSV payload, but it proves the QA document was not fully reconciled after the Work/Main role-boundary correction.

```text
QA_SELF_CONSISTENCY = FAIL
```

## 6. Main Chat acceptance verdict

```text
OWNER_UPLOAD_COMPLETE = true
REMOTE_READBACK_PASS = true
REMOTE_PUBLICATION_COMPLETE = true

WORK_HARD_QA = FAIL / INCOMPLETE
MAIN_CHAT_SEMANTIC_QA = FAIL
MAIN_CHAT_ACCEPTANCE = REJECTED_REWORK_REQUIRED

STEP07_ATTEMPT_1 = PRESERVED_FAILED_ATTEMPT
STEP07 = INCOMPLETE / REWORK_REQUIRED
STEP08 = BLOCKED / NOT_STARTED
```

The six uploaded files remain in Git as the exact failed-attempt evidence. Do not delete or rewrite history. A corrected Work run may REPLACE the current file paths; Git history preserves Attempt 1.

## 7. Main Chat quality score for returned result

Each criterion is independently scored 0–10.

| Criterion | Score /10 | Return-QA basis |
|---|---:|---|
| Goal and output completeness | 4 | Files exist, but actual competitor semantic expansion is not complete. |
| Method and source support | 8 | Core Step07 method is sound; execution/access and candidate-eligibility implementation failed. |
| Input evidence and provenance integrity | 9 | Frozen input authority and provenance mechanics are strong. |
| Coverage and completeness | 2 | Only 24 URLs inspected and only one authorized competitor produced candidate evidence. |
| Analytical correctness and claim boundaries | 3 | Demand boundary was respected, but many invalid prose/noise rows were promoted to `NEW_CANDIDATE`. |
| Adversarial QA quality | 4 | Work caught coverage failure but missed obvious semantic producer contamination and stale 7-file wording. |
| Persistence/readback/reproducibility | 9 | Six-file upload is remotely preserved and mechanically traceable. |
| Owner/client usability/plain language | 7 | Work report disclosed INCOMPLETE truth, but QA contains stale handoff wording. |
| Information gain/cost/execution efficiency | 5 | No provider cost, but the access route failed broadly and produced a contaminated candidate queue. |
| Downstream readiness | 1 | Step08 must not consume this result. |

```text
QUALITY_TOTAL = 52 / 100
QUALITY_SCORE = 5.2 / 10
HARD_FAILURE_OVERRIDE = true
FINAL_RETURN_VERDICT = FAIL / REWORK_REQUIRED
```

## 8. Required rework boundary

The next Work unit must do BOTH:

1. retry missing competitor coverage through legitimate browser/cloud-browser access without bypassing robots/CAPTCHA/login;
2. rerun semantic candidate eligibility across the full existing affected candidate/provenance universe and all newly collected evidence.

It must NOT:

- start Step08;
- make Wordstat/Search/AI-search/GenSearch provider calls;
- manually patch only the examples above;
- treat Work proxy failure as competitor semantic closure;
- retain the current 400 `NEW_CANDIDATE` rows without full-volume re-evaluation.

## 9. Plain-language conclusion

The upload itself is good: all six files reached GitHub exactly as one handoff and no unrelated repository files were touched. But the analytical result is not good enough to continue.

Work itself correctly noticed that almost all competitor pages were inaccessible from its run. Main Chat additionally found that many of those failures came from the Work runtime/proxy rather than from the websites: several supposedly inaccessible competitor sites are publicly retrievable through another normal public route. So those competitors still need legitimate collection, not closure.

The second problem is more serious: inside the only site that produced data, Work converted ordinary sentences, quotations and fragments into new semantic candidates. Therefore the current list of 400 new candidates cannot be sent to Wordstat/Step08.

The correct next action is one full Step07 rework in Work: retry the missing public competitors with a browser-capable route and reclassify the entire existing candidate/provenance universe under a stricter candidate-eligibility producer. Step08 stays blocked until that rework passes.