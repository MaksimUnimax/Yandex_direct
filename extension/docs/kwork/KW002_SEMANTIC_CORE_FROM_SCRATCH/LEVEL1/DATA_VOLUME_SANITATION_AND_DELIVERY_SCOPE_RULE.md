# KW-002 — DATA VOLUME, SANITATION AND DELIVERY SCOPE RULE

Status: **OWNER-APPROVED / ACTIVE**
Decision date: 2026-09-10
Applies to: all KW-002 jobs, not only Blood & Sand.

Mandatory companion authority added 2026-09-11:

`LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`

Every Step03A/03B/04+ prompt and QA must read that file and include the applicable `KNOWN_FAILURE_REGRESSION_MATRIX`. Mechanical count reconciliation alone is never sufficient semantic acceptance.

## 1. Core distinction

KW-002 must never confuse provider evidence volume with the number of client-delivered keywords.

```text
RAW_OCCURRENCE_POOL
!= NORMALIZED_UNIQUE_POOL
!= SANITIZED_CANDIDATE_POOL
!= DELIVERY_SELECTED_SET
!= FINAL_DELIVERED_CORE
```

### RAW_OCCURRENCE_POOL
Lossless provider evidence. The same phrase may occur under several seeds/runs/channels. RAW is retained for provenance and QA and may contain tens of thousands of occurrences.

### NORMALIZED_UNIQUE_POOL
One analytical phrase identity with all occurrence lineage aggregated. Exact duplicates are collapsed analytically but not deleted from RAW evidence.

### SANITIZED_CANDIDATE_POOL
Normalized phrases after conservative high-confidence sanitation: obvious non-target contexts, explicit foreign entities, technical/morphological garbage and safe implicit-duplicate compression are removed or held with reasons.

### DELIVERY_SELECTED_SET
The valid phrases selected for expensive intent/SERP/clustering work under the purchased order scope.

### VALID_RESERVE_SET
Relevant or plausibly relevant cleaned phrases that are not included only because the purchased delivery cap has been reached. They are not `REJECT`; they remain available for paid expansion or later revision.

## 2. Commercial delivery cap

Every KW-002 order must freeze a `DELIVERY_KEYWORD_CAP` at Step00.

The cap applies to the final client-delivered phrase rows, not to RAW acquisition.

```text
RAW_ACQUISITION = may exceed the delivery cap by any evidence-justified amount
FINAL_DELIVERED_CORE <= DELIVERY_KEYWORD_CAP
VALID_RESERVE_SET = allowed and preserved internally
```

Current productization safety rule:

```text
STANDARD_KWORK_DELIVERY_CEILING = 1500 phrases
>1500 = custom/owner-approved scope, not ordinary KW-002 package behavior
```

The exact base package and paid increments are commercial packaging parameters, not SEO truth. A common package model may be base +500 increments, but the order must record the actual purchased cap.

`UP TO N` means a maximum, not an obligation to pad the file to N. If only 730 phrases survive evidence-based cleaning for a 1000-phrase package, deliver 730 rather than invent or preserve junk.

## 3. Early sanitation is mandatory

Immediately after primary Wordstat acquisition and after every later acquisition union, run the same lossless-to-candidate transformation.

Mandatory operations:

```text
1. preserve complete RAW occurrence evidence;
2. canonicalize whitespace/case/technical punctuation without changing meaning;
3. collapse exact duplicates into one analytical phrase while retaining all lineage;
4. detect safe implicit duplicates / word-order or inflection variants;
5. apply frozen business exclusions and high-confidence stop topics;
6. separate explicit foreign entities/media/games/vehicle models/places/organizations/etc.;
7. separate obvious morphology/lexical garbage;
8. do NOT auto-reject unresolved ambiguous phrases;
9. do NOT auto-reject solely because frequency is low;
10. publish counts and reason codes for every transition.
```

The result of sanitation is the working candidate layer. LLM/Work semantic analysis must not receive the entire RAW occurrence ledger unless a specific audit requires it.

## 4. Asymmetric filtering rule

Automatic filtering must be conservative.

```text
HIGH-CONFIDENCE OFF-TOPIC -> AUTO_EXCLUDED with reason + lineage
EXACT/SAFE IMPLICIT DUPLICATE -> COLLAPSED_TO canonical phrase + lineage
MATERIAL AMBIGUITY -> HOLD / AMBIGUOUS
DIRECT BUSINESS-SUPPORTED TERM -> KEEP_CANDIDATE even if low-frequency
LOW FREQUENCY ALONE -> never AUTO_EXCLUDE
HIGH FREQUENCY ALONE -> never KEEP
```

## 5. How phrases are selected when valid pool exceeds purchased cap

Selection is coverage-aware and multi-factor. Do NOT sort only by Wordstat count.

Priority must consider, in order:

```text
A. business/assortment fit and purchased scope;
B. coverage of core product/service/use families;
C. search intent / user-job fit and ambiguity state;
D. Yandex demand signals (demand/frequency; clicks where available);
E. competition/rankability evidence where available;
F. canonicality / redundancy — avoid spending cap on near-duplicates;
G. cluster/topic representativeness and later SERP evidence;
H. incremental information/coverage value of the phrase.
```

A high-frequency irrelevant phrase must not outrank a lower-frequency directly sellable phrase merely because of count.

Selection must preserve breadth across important business families before filling the cap with many redundant variants from one head term.

## 6. Paid +N expansion semantics

An add-on such as `+500 phrases` expands the **delivery scope**, not the RAW scrape quota.

Default source of the additional phrases:

```text
VALID_RESERVE_SET
-> next highest coverage-aware priority phrases
-> preserve cluster completeness and business breadth
```

Only if the cleaned reserve is insufficient and the purchased scope legitimately requires more coverage may targeted/competitor expansion acquire additional evidence. Any new acquisition must pass through the same normalization/sanitation pipeline before it can enter the extra delivery tranche.

Additional +N phrases are therefore NOT automatically:
- the next N by frequency;
- N more raw Wordstat rows;
- N arbitrary long-tail variants;
- N duplicates from the same cluster.

## 7. Machine evidence vs analyst/LLM working set

Large occurrence ledgers are machine/audit evidence.

```text
RAW occurrence ledger -> machine storage / QA / provenance
normalized candidate table -> algorithmic filters + analyst review
sanitized candidate table -> family triage / nuanced review
DELIVERY_SELECTED_SET -> expensive Search/SERP/clustering
```

Work/LLM must receive compact candidate tables and targeted evidence locators. Full multi-megabyte occurrence payloads must not be pasted through chat/tool arguments merely to prove persistence.

## 8. Mandatory count accounting

Every transition must publish:

```text
raw_occurrence_rows
unique_exact_phrase_rows
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
RAW is never silently lost.
Every normalized/candidate/excluded/hold row has lineage to RAW.
Every delivered row has lineage to candidate + RAW.
Every valid phrase outside cap is explicitly RESERVE, not silently deleted.
```

## 9. Mandatory anti-regression gate after observed execution defects

The following is a hard methodology requirement, not optional QA advice:

```text
READ LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md
-> select every failure class applicable to the current step
-> materialize KNOWN_FAILURE_REGRESSION_MATRIX
-> run full applicable regressions
-> FAIL the step if any blocking regression fails
```

In particular for sanitation/family stages:

```text
SUBSTRING MATCH != REFERENT PROOF
TOKEN MATCH != INTENT PROOF
ACCOUNTING_QA != SEMANTIC_QA
REPRESENTATIVE DEFECT EXAMPLE != PATCH TARGET
MATERIAL UPSTREAM CHANGE INVALIDATES AFFECTED DOWNSTREAM PASS
```

The known Blood & Sand defects (business-token collisions, broad stems/regexes, semantic false KEEP/EXCLUDE, missing occurrence-level family mapping, example-only patches, and upstream sanitation changes affecting downstream family decisions) are permanent regression classes for later KW-002 jobs.

A high quality score cannot override a failed known-failure regression gate.

## 10. External method support

Official Yandex Webmaster:
- https://yandex.ru/support/webmaster/ru/service/queries-selection
  - use minus words to exclude non-target queries;
  - analyze demand, clicks and competition to choose suitable/promising queries;
  - discover additional non-obvious wording.

Topvisor:
- https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/
- https://topvisor.com/ru/support/implicit-duplicates/
  - progressive cleaning; remove obvious junk/duplicates/non-target phrases before expensive downstream analysis;
  - implicit duplicate normalization is a standard machine-assisted operation.

Key Collector:
- https://www.key-collector.ru/docs/tools/implicit-duplicates/
  - implicit duplicate detection and rule-based automatic marking for large lists.

Ahrefs:
- https://ahrefs.com/blog/keyword-intent/
- https://ahrefs.com/blog/keyword-strategy/
- https://ahrefs.com/blog/keyword-analysis-for-seo/
  - keyword intent is an early research filter;
  - prioritize with business potential, traffic potential/rankability and topic clusters, not volume alone.

Kwork market examples used for commercial-scope distinction:
- https://kwork.ru/keywords/53185723/soberu-semanticheskoe-yadro-dlya-sayta-sbor-i-klasterizatsiya-klyuchey
  - base 100, paid expansion to 500 and 1500 client-delivered keys.
- https://kwork.ru/keywords/51997366/semanticheskoe-yadro
  - up to 500 grouped high/mid/low-frequency phrases after manual cleaning.
- https://kwork.ru/keywords/45633833/sbor-chistka-i-klasterizatsiya-semanticheskogo-yadra-pod-klyuch
  - 1000 cleaned and clustered phrases.

These market examples support package design; they do not define SEO relevance rules.