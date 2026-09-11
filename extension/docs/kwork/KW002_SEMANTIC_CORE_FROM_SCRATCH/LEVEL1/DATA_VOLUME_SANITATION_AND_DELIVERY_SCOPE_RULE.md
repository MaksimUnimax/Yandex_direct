# KW-002 — DATA VOLUME, SANITATION AND DELIVERY SCOPE RULE

Status: **OWNER-APPROVED / ACTIVE / UNIVERSAL**
Applies to: all KW-002 jobs.

Mandatory companion authorities:

- `EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`

Every Step03A/03B/04+ prompt and QA must include applicable known-failure regressions. Mechanical reconciliation alone is never sufficient semantic acceptance.

## 1. Core data-layer distinction

KW-002 must never confuse provider evidence volume with analytical candidate volume or client-delivered scope.

```text
RAW_OCCURRENCE_POOL
!= NORMALIZED_UNIQUE_POOL
!= SANITIZED_CANDIDATE_POOL
!= VALID_RESERVE_SET
!= DELIVERY_SELECTED_SET
!= FINAL_DELIVERED_CORE
```

### RAW_OCCURRENCE_POOL
Lossless provider evidence with complete provenance. Duplicate text may legitimately appear under multiple requests/seeds.

### NORMALIZED_UNIQUE_POOL
One analytical identity per conservatively normalized phrase, with all RAW lineage preserved.

### SANITIZED_CANDIDATE_POOL
Normalized phrases after conservative high-confidence sanitation. Ambiguous phrases remain explicit HOLD rather than being destroyed.

### VALID_RESERVE_SET
Cleaned relevant/plausibly relevant phrases outside the purchased delivery set. Reserve is not reject.

### DELIVERY_SELECTED_SET
The governed phrase set selected for expensive row-level intent/SERP/clustering under purchased scope.

### FINAL_DELIVERED_CORE
The client-facing final semantic core after all required evidence stages.

## 2. Commercial delivery cap

Every order freezes `DELIVERY_KEYWORD_CAP` at Step00.

```text
RAW_ACQUISITION may exceed delivery cap by any evidence-justified amount
FINAL_DELIVERED_CORE <= DELIVERY_KEYWORD_CAP
VALID_RESERVE_SET is allowed and preserved
```

Current productization safety ceiling:

```text
STANDARD_KWORK_DELIVERY_CEILING = 1500 final phrases
>1500 = custom / separately owner-approved scope
```

Commercial packaging is not SEO truth. `UP TO N` means maximum, not an obligation to pad the result with weak phrases.

## 3. Early sanitation is mandatory

Immediately after every acquisition stage that adds new provider evidence:

```text
preserve complete RAW
→ conservative normalization
→ exact/safe duplicate handling with lineage
→ high-confidence sanitation
→ explicit HOLD for unresolved ambiguity
→ candidate union
```

Do not append later RAW acquisition directly into semantic-family or final-core tables.

## 4. Universal root causes sanitation must prevent

### 4.1 Lexical shortcut overreach

```text
SUBSTRING/PREFIX MATCH != LEXEME PROOF
TOKEN MATCH != REFERENT PROOF
REFERENT PROOF != INTENT PROOF
```

Broad stems/regexes may be discovery signals but not destructive proof unless collision safety is demonstrated.

### 4.2 Positive business vocabulary overriding foreign context

A product/business token does not cancel explicit evidence of another referent. If both remain plausible, HOLD.

### 4.3 Binary-clean-output pressure

The desire for a tidy dataset must not force ambiguous rows into KEEP/EXCLUDE before evidence is sufficient.

### 4.4 Mechanical QA substituted for semantic QA

Complete counts, deterministic rules and a high self-score do not prove semantic correctness. Independent semantic diagnostics are required where the data volume/rule complexity makes systematic bias plausible.

## 5. Asymmetric filtering rule

```text
HIGH-CONFIDENCE OFF-TOPIC -> AUTO_EXCLUDED with reason + lineage
EXACT/SAFE DUPLICATE -> analytical collapse + retained RAW lineage
MATERIAL AMBIGUITY -> HOLD / AMBIGUOUS
DIRECT BUSINESS-SUPPORTED -> KEEP_CANDIDATE
LOW FREQUENCY ALONE -> never AUTO_EXCLUDE
HIGH FREQUENCY ALONE -> never KEEP
```

## 6. Candidate selection when valid pool exceeds purchased cap

Selection is coverage-aware and multi-factor, not frequency-only.

Priority considers:

```text
business/offer fit
coverage of important business directions
user task / intent / ambiguity
Yandex demand signals
competition/rankability where available
canonicality / redundancy
cluster/topic representativeness
incremental coverage value
```

Preserve breadth across material business directions before filling the cap with redundant variants from one head term.

## 7. Paid expansion semantics

A paid `+N` expands delivery scope, not RAW scrape quota.

Default source:

```text
VALID_RESERVE_SET
→ next best coverage-aware candidates
```

Only when reserve is insufficient and broader evidence is justified may new acquisition run. All new evidence must re-enter through normalization/sanitation.

## 8. Machine evidence vs analyst/LLM working set

```text
RAW occurrence ledger -> durable machine/audit evidence
normalized pool -> machine normalization/dedup QA
sanitized candidate pool -> semantic family triage
cleaned/prioritized candidates -> expensive row-level review
DELIVERY_SELECTED_SET -> Search/SERP/clustering
```

Large RAW evidence must not be sampled merely to fit ordinary chat. Use Work for complete large-data transformations.

## 9. Mandatory count accounting

Every transition reports, where applicable:

```text
raw_occurrence_rows
normalized_unique_rows
implicit_duplicate_groups
collapsed_duplicate_rows
auto_excluded_rows_by_reason
hold_ambiguous_rows
sanitized_candidate_rows
valid_reserve_rows
delivery_selected_rows
delivery_cap
```

Required reconciliation:

```text
RAW_LINEAGE_LOSS = 0
SILENT_ROW_LOSS = 0
DELIVERED_ROWS_WITHOUT_CANDIDATE_AND_RAW_LINEAGE = 0
VALID_OUTSIDE_CAP_SILENTLY_DELETED = 0
```

## 10. Mandatory known-failure regression gate

Before accepting sanitation/family work:

```text
READ EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md
→ select every applicable universal failure mechanism
→ materialize KNOWN_FAILURE_REGRESSION_MATRIX
→ run full applicable regressions
→ FAIL if any blocking regression fails
```

At minimum consider:

```text
lexical boundary collisions
business-vs-foreign referent collisions
ambiguity preservation
mechanical-vs-semantic QA separation
rule-order precedence
hidden task patterns inside generic fallbacks
upstream authority invalidation
duplicate evidence acquisition
```

A quality score cannot override a failed hard regression.

## 11. External method support

Official Yandex:
- https://yandex.ru/support/webmaster/ru/service/queries-selection

Cleaning / duplicate handling:
- https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/
- https://topvisor.com/ru/support/implicit-duplicates/
- https://www.key-collector.ru/docs/tools/implicit-duplicates/

Intent / prioritization corroboration:
- https://ahrefs.com/blog/keyword-intent/
- https://ahrefs.com/blog/keyword-strategy/
- https://ahrefs.com/blog/keyword-analysis-for-seo/

Commercial package examples may inform scope packaging but never semantic relevance rules.

## 12. PASS

```text
DATA_LAYER_SEPARATION = PASS
RAW_LINEAGE_LOSS = 0
SANITATION_ASYMMETRY = PASS
AMBIGUITY_PRESERVED = PASS
KNOWN_FAILURE_REGRESSION_MATRIX = PASS
DELIVERY_CAP_NOT_USED_AS_RELEVANCE_RULE = true
JOB_SPECIFIC_EXAMPLES_IN_LEVEL1_RULE_BODY = 0
```
