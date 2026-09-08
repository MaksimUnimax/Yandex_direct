# KW-002 Blood & Sand — STEP 02 V1 QUALITY SCORE

Date: 2026-09-08

Evaluated version: original 97-probe Step-02 result before external-method rework.

Verdict:

```text
QUALITY_SCORE = 6.5 / 10
STATUS = REWORK_REQUIRED
STEP_03_ALLOWED = false
```

## Dimension score

| Dimension | Score | Reason |
|---|---:|---|
| Goal/output completeness | 1.0/1.0 | Seed map, coverage, deferred list, report and QA existed. |
| Method/source support | 0.7/1.0 | Core `seed = discovery probe` was supported, but quality-specific refinement rules were missing. |
| Evidence/provenance integrity | 1.0/1.0 | Client/Ozon lineage and analyst-composed labels were preserved. |
| Coverage/completeness | 0.6/1.0 | 76/76 catalog rows had routes, but quality coverage was conflated with catalog accounting coverage. |
| Analytical correctness/claim boundaries | 0.8/1.0 | No premature SEO decisions, but noisy bare names were over-promoted to PRIMARY. |
| Adversarial QA quality | 0.4/1.0 | QA checked counts/lineage but failed to challenge search usefulness/noise sufficiently. |
| Persistence/readback/reproducibility | 1.0/1.0 | Remote GitHub readback passed. |
| Owner/client usability/plain language | 0.7/1.0 | Report was understandable, but it overstated readiness by presenting PASS. |
| Information gain/cost/efficiency | 0.2/1.0 | Many exact-name rationales were boilerplate; provider-cost saving could influence deferral too much. |
| Downstream readiness | 0.1/1.0 | Step 03 should not have been opened before reworking high-noise/refinement/synonym coverage. |
| **TOTAL** | **6.5/10** | **Material rework required.** |

## What lost points

```text
- bare ambiguous names counted as sufficient quality routes;
- no mandatory refinement strategy for HIGH-noise names;
- automobile synonym/use-context coverage was not systematic;
- exact seller names dominated PRIMARY by default;
- expected information gain was repetitive/weakly discriminating;
- Step 03 was opened before a search-probe-quality QA existed.
```

## What raises the score

```text
- separate catalog-lineage coverage from search-quality coverage;
- add refinement/qualification routes for ambiguous names;
- add bounded machine/automobile/auto wording coverage;
- rebalance exact names versus qualified/broad probes;
- rewrite information-gain rationale;
- materialize a deterministic corrected primary acquisition manifest;
- rerun adversarial QA and remote readback.
```
