# KW-001 — STEP RULES INDEX

Updated: 2026-09-10  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / VOLUME-SCALING REVISION ACTIVE**

This is the current executable roadmap index for KW-001.

The complete pre-volume-revision index is preserved as:

`STEP_RULES_INDEX_PRE_VOLUME_SCALING_2026-09-10.md`

All unaffected permanent rules/statuses from that historical base remain in force. This current index supersedes conflicting pre-2026-09-10 language only for acquisition volume, normalization, sanitation, Work/LLM input scale and downstream propagation.

## Mandatory universal authorities

Before execution, use the existing cross-step gates plus:

- `DATA_VOLUME_NORMALIZATION_AND_SANITATION_GATE.md`
- `STEP_05A_VOLUME_SANITATION_ADDENDUM_2026-09-10.md`
- `IMPLEMENTATION_PLAN_VOLUME_SCALING_AMENDMENT_2026-09-10.md`
- current detailed step authorities listed below.

Canonical data-flow distinction:

```text
RAW_OCCURRENCE_POOL
!= NORMALIZED_UNIQUE_POOL
!= SANITIZED_CANDIDATE_POOL
!= STEP7_CLEANED_ACTIVE_SET
!= SEARCH_STAGE_SET
```

## Current execution order

```text
Step 0   order / scope freeze
Step 1   existing-site / business-page discovery
Step 2   bounded seed / acquisition probe plan
Step 3   Wordstat/provider acquisition -> LOSSLESS RAW
Step 3R  conditional repair of incomplete Step3 acquisition
Step 3A  RAW normalization + exact/safe implicit deduplication
Step 3B  high-confidence sanitation / pre-filter
Step 4   first family triage on SANITIZED candidates, not RAW occurrences
Step 5   targeted second acquisition -> immediate Step3A/3B on new rows
Step 5A  competitor semantic expansion -> immediate Step3A/3B on new Wordstat rows
Step 6   demand dynamics / seasonality when method is validated/authorized
Step 6A  acquisition coverage revalidation when method is validated/authorized
Step 7   nuanced row-level semantic cleanup on compact analytical pool
Step 8   Search-stage semantic freeze
Step 9   ordinary Yandex Search validation for decision-relevant retained set
Step 10  user-task / Search clustering
Step 11  page ownership / phrase->page mapping
Step 12  structural/content-routing actions
Step 13  competing-page / cannibalization diagnosis
Step 14  Search-only architecture freeze
Step 15  bounded AI-case selection
Step 16  bounded AI-search evidence acquisition
Step 17  Search-vs-AI comparison
Step 18  prioritization / implementation readiness
Step 19  client deliverables
Step 20  final QA / release assurance
Step 21  handoff / revisions
Step 22  job close
```

`Step3R` is a conditional recovery pattern. It is not a replacement for Step3A/3B.

## Permanent methodology coverage

| Stage | Purpose | Permanent status | Current authority / non-repeat boundary |
|---|---|---|---|
| Step 0 | Order / scope freeze | **APPROVED / ACTIVE** | Existing `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md`; freeze brief/scope before evidence acquisition. |
| Step 1 | Existing-site / business discovery | **APPROVED / ACTIVE** | Existing discovery/freshness authorities; discovery snapshot != timeless completeness. |
| Step 2 | Seed / acquisition probe plan | **APPROVED / ACTIVE + SCALE CONTROL** | `DATA_VOLUME_NORMALIZATION_AND_SANITATION_GATE.md`: `SKU != AUTOMATIC SEED`; use category/subcategory/product-type/use/attribute/brand-model search entities; each seed requires information-gain purpose. |
| Step 3 | Wordstat/provider acquisition | **APPROVED / ACTIVE + SCALE CONTROL** | Preserve every RAW occurrence under existing persistence rules, then obligatorily run Step3A/3B before Step4. Provider success != collection completeness; RAW occurrence != analytical keyword. |
| Step 3R | Repair incomplete Step3 acquisition | **JOB-SPECIFIC RECOVERY PATTERN** | Existing Step3 durability rules; after repair, continue through Step3A/3B. |
| **Step 3A** | **Normalization / deduplication** | **APPROVED / ACTIVE / OWNER-ADDED 2026-09-10** | Exact duplicates collapse analytically with all lineage retained; safe implicit duplicates only where equivalence is high-confidence; RAW is never destroyed. |
| **Step 3B** | **High-confidence sanitation** | **APPROVED / ACTIVE / OWNER-ADDED 2026-09-10** | Clear off-topic -> excluded with reason; duplicate -> canonical; ambiguity -> HOLD; low frequency alone never excludes. |
| Step 4 | First post-acquisition triage | **APPROVED / ACTIVE / INPUT CORRECTED** | Operates on sanitized candidates + relevant HOLD rows and aggregate provenance, not on a semantic partition of every RAW occurrence. Family triage != final Step7 cleanup. |
| Step 5 | Targeted second acquisition | **PARTIALLY DEFINED / SCALE CONTROL ACTIVE** | Existing information-gain rule remains. Every newly acquired row immediately passes Step3A/3B before union with the working semantic pool. |
| **Step 5A** | **Competitor semantic expansion** | **APPROVED / ACTIVE / PROJECT-TEST-VALIDATED / OWNER-CANONIZED + SCALE ADDENDUM** | Existing `STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md` plus `STEP_05A_VOLUME_SANITATION_ADDENDUM_2026-09-10.md`; competitor-derived Wordstat output re-enters Step3A/3B before merge. |
| Step 6 | Demand dynamics / seasonality | **UNVALIDATED AS PERMANENT METHOD** | Fresh research/method review required; any new query acquisition must obey Step3A/3B before union. |
| Step 6A | Acquisition coverage revalidation | **UNVALIDATED AS PERMANENT METHOD** | Fresh research/method review required; any new query acquisition must obey Step3A/3B before union. |
| Step 7 | Row-level semantic cleanup | **APPROVED / ACTIVE AFTER CORRECTION + INPUT CORRECTED** | Existing no-default-KEEP/positive-evidence/adversarial-QA rules remain. Step7 now receives normalized/sanitized analytical phrases, not the complete RAW occurrence ledger. |
| Step 8 | Search-stage semantic freeze | **APPROVED / ACTIVE** | `STEP_08_SEARCH_STAGE_FREEZE_METHOD.md`; retained phrase lineage to full RAW evidence remains 100%, but RAW duplicates are not Search input. |
| Step 9 | Ordinary Yandex Search validation | **UNVALIDATED FULL METHOD / NARROW CONTROLS ACTIVE** | Existing exact-query/generalization controls remain. Search is for retained decision-relevant queries/boundaries, not for the complete RAW acquisition universe. |
| Step 10 | User-task / Search clustering | **APPROVED / ACTIVE** | Existing Step10 authorities; cluster the cleaned Search-stage set, not RAW. |
| Step 11 | Page ownership / phrase->page mapping | **APPROVED / ACTIVE** | Existing Step11 authority. |
| Step 12 | Structural/content-routing actions | **APPROVED / ACTIVE** | Existing Step12 authorities. |
| Step 13 | Competing-page diagnosis | **APPROVED / ACTIVE** | Existing Step13 authority. |
| Step 14 | Search-only architecture freeze | **APPROVED / ACTIVE** | Existing Step14 authorities. |
| Step 15 | AI-case selection | **APPROVED / ACTIVE** | Existing diagnostic/control selection authority; bounded cases, not bulk semantic-core replay. |
| Step 16 | AI-search evidence acquisition | **UNVALIDATED FULL METHOD / NARROW CONTROLS ACTIVE** | Existing provider/claim controls; only selected cases are acquired. |
| Step 17 | Search-vs-AI comparison | **APPROVED / ACTIVE** | Existing Step17 authority. |
| Step 18 | Prioritization / implementation readiness | **APPROVED / ACTIVE AFTER EXTERNAL AUDIT + CORRECTION** | Existing Step18 authorities preserved unchanged. |
| Step 19 | Client deliverables | **UNVALIDATED / OWNER-DIRECTED CORRECTED METHOD CANDIDATE ACTIVE AS NON-REPEAT CONTROL** | Existing Step19 authorities preserved unchanged. |
| Step 20 | Final QA / release assurance | **APPROVED / ACTIVE AFTER OWNER-DIRECTED AUDIT + CORRECTION** | Existing Step20 authorities preserved unchanged. |
| Step 21 | Handoff / revisions | **UNVALIDATED AS PERMANENT METHOD** | Existing boundaries preserved. |
| Step 22 | Job close | **PARTIALLY DEFINED BY JOB_WORKSPACE_LIFECYCLE** | Existing lifecycle authority preserved. |

## Step 2 scale boundary

For large e-commerce/catalog sites:

```text
CATALOG ROW COUNT != ACQUISITION PROBE COUNT
SKU != AUTOMATIC WORDSTAT SEED
```

Initial probes should primarily cover search-relevant category/subcategory/product-type/use/attribute/brand-model families. Individual SKU/model probes are selective and require search identity or decision value.

## Step 3 -> Step 4 mandatory gate

Step4 may not start from a large raw corpus until:

```text
Step3 acquisition complete
-> Step3A normalized unique pool complete
-> Step3B sanitation accounting complete
-> RAW-to-normalized-to-sanitized reconciliation PASS
```

Required funnel fields:

```text
raw_occurrence_rows
normalized_unique_rows
exact_duplicate_occurrences_collapsed
implicit_duplicate_groups
collapsed_implicit_rows
auto_excluded_rows by reason
hold_ambiguous_rows
sanitized_candidate_rows
```

## Expansion loop rule

For Step5, Step5A and any later acquisition extension:

```text
NEW RAW
-> SAME Step3A
-> SAME Step3B
-> only sanitized/HOLD analytical rows union into semantic working set
```

Do not allow the working set to grow merely because the same phrase appears across more provider requests.

## Step 5A insertion boundary

The permanent Step5A sequence is now:

```text
sanitized initial demand families
-> representative Yandex competitor discovery
-> evidence-bearing competitor pages
-> genuinely new candidate topics/seeds
-> Wordstat RAW acquisition
-> Step3A normalization
-> Step3B sanitation
-> material new sanitized candidates
-> bounded Yandex Search confirmation where required
-> ADD / ALREADY_COVERED / REJECT / HOLD
-> common semantic pipeline
-> Step7 cleanup
-> Step8 freeze
```

The existing Step5A claim boundaries remain unchanged:

```text
COMPETITOR PAGE TOPIC != EXACT QUERY RANKING
COMPETITOR RANKING != AUTOMATIC KEYWORD ACCEPTANCE
COMPETITOR-DERIVED SEED != FINAL KEYWORD
TESTED QUERY VISIBILITY != FULL COMPETITOR KEYWORD UNIVERSE
```

## Step 7 role after revision

Step7 remains mandatory.

```text
STEP3B = early conservative mass sanitation
STEP7 = nuanced final semantic/business cleanup
```

Step3B must not try to solve ambiguous intent/business/page questions that belong to Step7 or later Search evidence.

## Work / LLM scaling boundary

```text
FULL RAW LEDGER = machine/audit evidence by default
WORK INPUT = compact normalized/sanitized candidates + summaries + provenance locators
TARGETED RAW SLICE = allowed for disputed cases
```

Do not serialize/paste a multi-megabyte RAW ledger into Work merely because it exists. If compact candidates are still large, process deterministic chunks keyed by stable IDs and reconcile 100% of rows; sampling is not full processing.

## KW-001 commercial boundary

No fixed final phrase ceiling is introduced by this revision.

```text
KW002 1500 standard ceiling != KW001 rule
```

KW-001 may retain more than 1500 active phrases where the site/scope/evidence justifies them. Exact package limits remain a separate KW-001 productization/economics decision.

## Existing accepted outputs

Existing accepted KW-001 outputs are not invalidated solely by this 2026-09-10 scalability revision.

A completed job requires backfill only if upstream acquisition/cleanup is materially reopened or an independent quality/scalability defect requires it.

## Execution checklist

Before Step2–7 material work:

```text
1. Read DATA_VOLUME_NORMALIZATION_AND_SANITATION_GATE.md.
2. Read this current STEP_RULES_INDEX.md.
3. Read the detailed authority for the current step.
4. Read current Level2 job evidence/state separately.
5. State RAW / normalized / sanitized input counts available at the gate.
6. Do not treat provider rows as equal semantic units.
7. Execute only authorized provider work.
8. Persist RAW before derivation.
9. Run normalization/sanitation before semantic family analysis.
10. Reconcile counts and lineage before advancing.
```

All unaffected permanent lessons from `STEP_RULES_INDEX_PRE_VOLUME_SCALING_2026-09-10.md` and their detailed method files remain active.