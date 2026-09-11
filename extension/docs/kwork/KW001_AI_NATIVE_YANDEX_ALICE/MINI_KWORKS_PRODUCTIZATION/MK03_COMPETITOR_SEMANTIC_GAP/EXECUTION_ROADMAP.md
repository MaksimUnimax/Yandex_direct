# MK03 — EXECUTION ROADMAP

Status: **PHASE 4 PASS CANDIDATE / LEVEL-1 EXECUTION CONTRACT**

## 0. Product execution identity

MK03 is the standalone Yandex competitor-derived semantic-gap product defined by `PRODUCT_SCOPE.md`.

Canonical execution chain:

```text
PUBLIC CLIENT SITE + TARGET REGION
→ CURRENT-SITE SCOPE / COVERAGE BASELINE
→ REPRESENTATIVE IN-SCOPE YANDEX QUERY FAMILIES
→ REAL ORGANIC SEARCH COMPETITORS
→ EVIDENCE-BEARING COMPETITOR PAGES
→ COMPETITOR-DERIVED TOPIC / SEED HYPOTHESES WITH LINEAGE
→ WORDSTAT DEMAND VALIDATION
→ NORMALIZATION / SANITATION / BUSINESS-FIT FILTER
→ SELECTIVE CURRENT-SEARCH CONFIRMATION FOR MATERIAL CLAIMS
→ CLIENT COVERAGE RECONCILIATION
→ EXPLICIT GAP STATE
→ BOUNDED OPPORTUNITY INTERPRETATION
→ CLIENT XLSX + ANALYTICAL PDF + HANDOFF
→ ANALYTICAL / ACCOUNTING / PHYSICAL / RECIPIENT QA
```

This roadmap is autonomous. It does not require an executor to reconstruct the full KW-001 method from memory.

## 1. Global authorities

Before execution read, in order:

1. `PRODUCT_SCOPE.md`
2. `CLIENT_INPUT_CONTRACT.md`
3. `GENERAL_RULES.md`
4. `ERRORS_AND_LESSONS.md`
5. `SERP_COVERAGE_MODE_DECISION_2026-09-11.md`
6. `STEP_RULES_INDEX.md`
7. all `steps/STEP_00_*.md` through `steps/STEP_09_*.md`
8. `DELIVERABLE_SPEC.md`
9. `QA_AND_RELEASE.md`

Per-step rules may strengthen but may not weaken the cross-step rules.

## 2. Input contract

Required ordinary V1 client input:

```text
PUBLIC SITE URL
+ TARGET REGION
```

Optional hints may include competitor names or known priorities. Hints are not accepted as organic-competitor truth.

If a material business ambiguity cannot be resolved from the current public site, preserve one explicit `HOLD_EVIDENCE` / business clarification rather than inventing scope.

## 3. Execution sequence

### STEP 00 — Scope + current-site baseline

Freeze domain, region, business boundary and current public coverage sufficient for later gap comparison.

Mandatory outputs:
- scope record;
- current-site evidence inventory or equivalent baseline;
- explicit unresolved business ambiguities.

Gate:
`OLD ABSENCE != CURRENT SITE ABSENCE`; historical inventory alone cannot prove a current gap.

### STEP 01 — Representative Yandex discovery baseline

Build only the representative in-scope query families needed to expose material search jobs and discover real competitors.

This is not a hidden MK01 rebuild.

Gate:

```text
MK03 DISCOVERY BASELINE != FULL MK01 SEMANTIC CORE
```

Expand only where a named uncovered direction prevents defensible competitor/gap conclusions.

### STEP 02 — Real organic competitor discovery

Use current regional ordinary Yandex Search to identify domains that actually compete for the representative families.

Record enough evidence to trace:

```text
QUERY FAMILY / QUERY
→ REGION
→ OBSERVED RESULT
→ DOMAIN
→ RESULT URL
→ RESULT TYPE / ROUTING CLASS
```

Client-supplied competitor hints, business familiarity, ads or marketplaces do not establish organic-competitor truth by themselves.

### STEP 03 — Evidence-bearing competitor-page inspection

Inspect only public competitor pages that carry decision-relevant evidence. Record page type, topic/service/product/use-case axes and material visible page elements as needed.

Hard boundary:

```text
COMPETITOR PAGE TOPIC != EXACT QUERY RANKING
```

A page may be a seed source without proving visibility for an exact query.

### STEP 04 — Competitor-derived topic/seed hypotheses

Derive traceable in-scope candidate directions from evidence-bearing competitor pages.

Each seed/probe preserves source lineage. It is a hypothesis, not an accepted keyword.

```text
COMPETITOR-DERIVED SEED != ACCEPTED KEYWORD
```

### STEP 05 — Wordstat expansion + normalization/sanitation

Run Wordstat only for genuinely new information-gain probes permitted by the execution contract. Persist useful raw evidence before material subsequent acquisition.

Mandatory funnel:

```text
RAW OCCURRENCES
→ NORMALIZED UNIQUE IDENTITIES
→ HIGH-CONFIDENCE SANITATION
→ BUSINESS-FIT / SCOPE CHECK
→ COMPARE WITH EXISTING NORMALIZED POOL
→ NEW_SANITIZED_CANDIDATE | ALREADY_COVERED | REJECT | HOLD
```

Duplicate semantic identity keeps merged provenance; it does not become a duplicate keyword merely because a competitor supplied a new lineage.

### STEP 06 — Material current-Search confirmation

SERP mode is:

```text
SERP_COVERAGE_MODE = SELECTIVE_DECISION_SERP
```

Use current Search for material decisions and any exact query→competitor visibility claim. Do not bulk-run Search for every raw Wordstat occurrence.

Every exact visibility statement must be distinguishable as `SEARCH_TESTED` or not tested. Unprobed rows may not be generalized into Search-confirmed evidence.

### STEP 07 — Client coverage comparison + gap classification

Reconcile accepted candidates against sufficiently current client-site/semantic coverage.

Every material candidate ends in exactly one visible state or an explicitly documented deterministic duplicate collapse:

```text
CONFIRMED_GAP
ALREADY_COVERED
REJECT_OFF_SCOPE
HOLD_EVIDENCE
```

No silent drop is allowed.

### STEP 08 — Bounded structural opportunity interpretation

Translate confirmed gaps into bounded client opportunities only to the extent supported by evidence.

Allowed examples include:
- content/topic expansion opportunity;
- page-type or section opportunity;
- strengthening an existing page/direction;
- route for later MK02/MK04/MK05 work;
- no structural action when evidence does not justify one.

Hard boundary:

```text
CONFIRMED_GAP != AUTOMATIC CREATE PAGE
COMPETITOR HAS PAGE != CLIENT MUST COPY THAT PAGE
```

MK03 does not silently materialize full target architecture, phrase→page ownership or implementation-ready TZ.

### STEP 09 — Client materialization + QA

Materialize the physical package defined by `DELIVERABLE_SPEC.md`, then run all gates from `QA_AND_RELEASE.md`.

Source/generator authority is corrected before rendered artifacts. Any final-byte change invalidates prior physical QA for the affected artifact.

## 4. Provider-call policy

Before any new Search or Wordstat call:

```text
NAMED INFORMATION GAP
+ WHY PRESERVED EVIDENCE IS INSUFFICIENT
+ WHICH MK03 DECISION MAY CHANGE
+ ALLOWED ACCESS / COST STATE
```

Reuse preserved current evidence before a new provider call. Stop expansion when marginal evidence no longer changes material decisions.

There is no fixed universal competitor, page, seed, Wordstat-row or SERP-check count.

## 5. Evidence-state discipline

At minimum distinguish:

```text
OBSERVED CURRENT SEARCH FACT
PUBLIC PAGE FACT
WORDSTAT DEMAND FACT
NORMALIZATION / ROUTING ASSIGNMENT
ANALYTICAL CONCLUSION
STRUCTURAL OPPORTUNITY RECOMMENDATION
BUSINESS FACT
UNKNOWN / HOLD
```

Page-topic evidence and exact-query Search evidence remain separate through final materialization.

## 6. No-silent-drop accounting

Every material acquired candidate must be reconstructable from acquisition to final state.

Required reconciliation concept:

```text
RAW / DISCOVERED INPUT
= DETERMINISTIC DUPLICATE COLLAPSE WITH LINEAGE
+ NEW SANITIZED CANDIDATES
+ ALREADY COVERED
+ REJECTED OFF-SCOPE / SANITIZED
+ HOLD / EVIDENCE REQUIRED
```

Exact schema names may differ in Level 2, but the accounting identity may not disappear.

## 7. Product exclusions

Base MK03 does not include:
- full semantic-core rebuild;
- full target site architecture;
- complete phrase→page mapping;
- dedicated cannibalization audit;
- implementation-ready SEO TZ;
- backlink / technical / CWV / schema / conversion competitor audit;
- traffic/revenue estimation;
- full reverse-domain keyword universe;
- Google research;
- Alice/Neuro/AEO layer.

## 8. Rehearsal rule

Phase 5 executes MK03 on OKNO_MSK as if the client bought **only MK03**.

Existing KW-001 evidence may be reused only when its evidence type, freshness, region and provenance are compatible with this contract. Excluded downstream stages must not contaminate the MK03 answer.

Large-data Phase 5 is executed in Work only after Phase-4 Level-1 PASS and remote readback.

## 9. Final PASS definition

MK03 execution passes only when:

1. actual Yandex organic competitors are evidence-traceable;
2. inspected competitor pages and derived seeds preserve lineage;
3. Wordstat-derived demand is normalized/sanitized and business-scoped;
4. tested Search claims are visibly separated from unprobed page-topic evidence;
5. every material candidate has an explicit final state;
6. current-site coverage used for gap claims is current enough for the claim;
7. opportunities do not overclaim downstream architecture/TZ;
8. client XLSX and analytical PDF expose inspectable findings, not counts only;
9. analytical, accounting, physical and recipient QA all pass;
10. material authorities/artifacts are committed/published and remote-read back.
