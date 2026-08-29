# KW-001 / OKNO-MSK — STEP 07B POST-AUDIT CORRECTION REQUIRED

Date: 2026-08-29  
Status: **CORRECTION REQUIRED / NEXT STEP BLOCKED / JOB-SPECIFIC**

## Why this correction exists

After Step 07B was marked COMPLETE/PASS, the owner required a fresh external methodology audit of the actual cleanup result before allowing the next major step.

That audit found a material analytical defect in the semantic decision layer.

The data-accounting layer remains valid:

```text
source occurrence preservation = PASS
2965 source rows accounted = PASS
exact-string dedupe accounting = PASS
2840 exact phrase keys accounted = PASS
provenance reconciliation = PASS
provider calls during cleanup = 0
```

However the semantic classification layer is not accepted as complete.

## Material defect

`STEP_07B_ROW_LEVEL_CLEANUP_BUILD.py` used a rule-based classifier in which known mechanical / irrelevant / out-of-scope / boundary patterns were intercepted, but remaining result phrases fell through to:

```text
KEEP / SUPPORTED_WINDOW_OR_GLAZING_TASK
```

Therefore `KEEP` frequently meant only "no exclusion/review rule matched" rather than "positive semantic relevance and user intent were established".

Concrete examples already visible in the generated working table include:

```text
1 установка пластиковых окон -> KEEP
6 6 с панорамными окнами -> KEEP
rehau окна 2 -> KEEP
алюминиевые окна 2 -> KEEP
rehau окна анадырский проезд д 47 -> KEEP
rehau микролифт для окна -> KEEP while similar hardware phrases are REVIEW
```

This demonstrates dictionary-completeness dependence and false-KEEP risk.

## External audit conclusion

The fresh audit used current public methodology evidence from:

- Yandex Wordstat documentation: raw/popular/similar demand is acquisition evidence, not an automatically suitable site keyword set;
- Yandex Webmaster targeting guidance: query selection must reflect the user's need and what the site can actually satisfy;
- Topvisor semantic-core cleanup guidance: cleanup must address non-target queries, intent mismatch and non-obvious duplicates, not only exact duplicates;
- Rush Analytics clustering/semantic preparation guidance: automatic processing requires expert correction and ambiguous intent should be checked against SERP;
- Ahrefs keyword-intent methodology: intent is a filter during keyword research and mixed intent requires SERP evidence;
- Semrush keyword-clustering methodology: grouping depends on shared search intent and SERP similarity.

The audit verdict is:

```text
ROW_LEVEL_DATA_ACCOUNTING = PASS
EXACT_DEDUPLICATION_ACCOUNTING = PASS
DETERMINISTIC_PREFILTER = PASS
FULL_SEMANTIC_ROW_REVIEW = CORRECTION_REQUIRED
SEMANTIC_CLEANUP_COMPLETE = false
NEXT_STEP_ALLOWED = false
```

## Required correction

Do not recollect Wordstat and do not discard existing provenance.

Re-use the same 2965 source occurrences / 2840 exact phrase keys, but replace the default-KEEP decision logic with a conservative positive-evidence model:

1. Safe deterministic exclusions may remain deterministic where intent/scope is unambiguous.
2. `KEEP` requires positive evidence that the phrase represents a user need supported by the known OKNO-MSK business/site model.
3. A phrase that is not proven irrelevant but is not positively proven KEEP must become `REVIEW` rather than default KEEP.
4. Non-obvious duplicate candidates must be surfaced separately; they are not silently merged by a lexical heuristic.
5. Ambiguous business/page/search-intent boundaries remain `REVIEW` for later ordinary Yandex Search evidence.
6. Corrected output must preserve the full 2965-occurrence provenance and reconcile all 2840 exact phrase keys.
7. Corrected semantic decisions require post-generation semantic QA, not only arithmetic QA.

## Supersession rule

Until an explicit correction acceptance is created:

```text
STEP_07B_ROW_LEVEL_CLEANUP_ACCEPTANCE_2026-08-29.md = HISTORICAL / SEMANTIC PASS SUPERSEDED
ROW_LEVEL_CLEANUP_COMPLETE = false
NEXT_MAJOR_STEP = BLOCKED
```

The historical artifacts remain preserved for audit and comparison. They must not be deleted or rewritten as if the failed semantic-pass never happened.
