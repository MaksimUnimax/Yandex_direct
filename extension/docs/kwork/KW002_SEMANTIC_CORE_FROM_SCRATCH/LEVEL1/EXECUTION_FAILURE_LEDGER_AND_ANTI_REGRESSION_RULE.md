# KW-002 — EXECUTION FAILURE LEDGER AND ANTI-REGRESSION RULE

Status: **OWNER-MANDATED / ACTIVE / MUST BE READ BEFORE EVERY LATER STEP**
Decision date: 2026-09-11
Applies to: all KW-002 jobs and every Main ChatGPT / Work execution pass.

## 1. Purpose

KW-002 must learn from defects that were actually observed in execution. A later step is not allowed to repeat a known failure merely because its mechanical QA passes.

This file is a Level-1 methodology authority. Job-specific failure ledgers may add concrete examples and counts, but may not weaken these rules.

Mandatory pre-step action:

```text
READ THIS FILE
-> identify which historical failure classes can recur in the current step
-> add explicit regression gates to the step prompt/QA
-> only then execute the step
```

A known failure class without an explicit regression gate means the step is not ready for PASS.

---

## 2. Failure class F00 — source/scope freeze admitted superseded inputs

Observed in Blood & Sand Step00:

- an earlier freeze admitted WB + Ozon assortment rows;
- the owner later clarified Ozon-only as the authoritative assortment input;
- dependent planning based on the larger mixed-source set had to be invalidated and rebuilt.

Anti-regression rule:

```text
MATERIAL INPUT MUTATION
-> invalidate all dependent plans/artifacts that used the old input
-> update whitelist / brief / manifests
-> rebuild downstream handoff
-> only then restore PASS
```

Never silently keep an old source because it is convenient or already processed.

Required gate:

```text
ACTIVE_INPUT_SOURCE_SET == CURRENT_OWNER_APPROVED_SOURCE_SET
SUPERSEDED_INPUT_ROWS_USED_DOWNSTREAM = 0
```

---

## 3. Failure class F02 — catalog accounting was mistaken for search-quality coverage

Observed in Blood & Sand Step02 V1:

- 76/76 catalog lineage coverage looked complete;
- noisy bare names and ambiguous exact seller names were too easily promoted to PRIMARY probes;
- HIGH-noise names lacked mandatory refinement strategy;
- automobile/use-context synonyms were not covered systematically;
- information-gain rationales became repetitive;
- adversarial QA checked counts/lineage better than search usefulness;
- Step03 was opened before dedicated search-probe-quality QA.

Anti-regression rule:

```text
CATALOG_LINEAGE_COVERAGE != SEARCH_PROBE_QUALITY
```

Every ambiguous/high-noise seed family must have at least one explicit refinement/qualification route or an explicit defer/control reason.

Do not use provider-call economy as a reason to suppress a probe that materially improves coverage.

Required gates:

```text
BARE_AMBIGUOUS_PRIMARY_WITHOUT_REFINEMENT = 0
HIGH_NOISE_PRIMARY_WITHOUT_QUALIFICATION = 0
SEARCH_QUALITY_QA = PASS
NEXT_STEP_OPENED_BEFORE_SEARCH_QUALITY_QA = false
```

---

## 4. Failure class F03 — provider success was mistaken for durable feed-forward completion

Observed in Blood & Sand Step03:

- provider acquisition could appear complete;
- later readback showed only 60/79 current outcomes reconstructed losslessly from durable GitHub evidence;
- recovery was required to reach 79/79 durable feed-forward;
- `OUTCOME_UNKNOWN` history had to remain preserved rather than being overwritten by blind replay.

Anti-regression rule:

```text
PROVIDER_SUCCESS != STEP_COMPLETION
```

A provider step completes only after:

```text
result received
-> complete required payload persisted
-> durable object/file identity recorded
-> remote readback performed
-> required row/count/provenance fields reconciled
-> then and only then advance
```

`OUTCOME_UNKNOWN` forbids blind replay. A new current observation must receive a new request identity and must not masquerade as the historical original.

Required gates:

```text
AUTHORIZED_ITEMS_WITH_TERMINAL_PROVIDER_OUTCOME = TOTAL_AUTHORIZED_ITEMS
AUTHORIZED_ITEMS_WITH_DURABLE_LOSSLESS_FEED_FORWARD = TOTAL_AUTHORIZED_ITEMS
REMOTE_READBACK = PASS
BLIND_REPLAY_OF_OUTCOME_UNKNOWN = 0
```

---

## 5. Failure class F03A — unsafe normalization can destroy meaning or provenance

The Blood & Sand Step03A independent audit passed, but the audit established the safety boundary that future jobs must preserve.

Anti-regression rules:

- use conservative Unicode normalization (NFC unless a stronger transformation is separately justified);
- trim/collapse whitespace safely;
- case-fold for comparison, not destructive rewriting where the original matters;
- do not erase digits, punctuation, hyphens or word order merely to increase deduplication;
- exact duplicate collapse is analytical only: every RAW occurrence remains traceable;
- implicit duplicates require high-confidence equivalence; otherwise HOLD the group.

Required gates:

```text
RAW_LINEAGE_LOSS = 0
UNEXPLAINED_IMPLICIT_COLLAPSE = 0
ORIGINAL_TEXT_RECOVERABLE = true
```

---

## 6. Failure class F03B-1 — broad substring/regex rules fired before business-context collision guards

Observed in the original Blood & Sand Step03B:

Examples of unsafe pattern behavior included:

- `футбол*` colliding with `футболка`;
- `банк*` colliding with unrelated/ambiguous contexts;
- `четк*` colliding with possible `чётки` morphology/typo;
- `купить.*дом|дом.*купить` colliding with product demand such as `оберег дома купить`;
- generic media verbs (`читать`, `слушать`, `смотреть`, `скачать`, `серия`) firing without enough media referent evidence;
- broad vehicle/model rules firing before supported automobile-use/catalog collision checks;
- generic `игра`, `мод*`, `id`-like patterns acting as conclusive evidence without a named game/in-game referent.

Anti-regression rule:

```text
SUBSTRING MATCH != REFERENT PROOF
TOKEN MATCH != INTENT PROOF
```

Before any AUTO_EXCLUDE decision, require a bounded referent/context rule that proves the foreign meaning.

Business-supported collision guards must be evaluated before destructive negative rules.

Required gates:

```text
SINGLE_AMBIGUOUS_TOKEN_AUTO_EXCLUSIONS = 0
UNBOUNDED_STEM_AUTO_EXCLUSIONS = 0
BUSINESS_COLLISION_GUARD_PRECEDENCE = PASS
```

---

## 7. Failure class F03B-2 — positive business token fallback could override explicit foreign context

Observed in the original Step03B:

A recognized product/business token could still lead to KEEP after an incomplete negative blacklist, allowing games, vehicle parts and media/digital contexts to survive.

Anti-regression rule:

```text
POSITIVE_BUSINESS_TOKEN
DOES NOT OVERRIDE
EXPLICIT_FOREIGN_CONTEXT
```

Before KEEP, independently test explicit foreign contexts such as:

```text
named game / in-game item
vehicle model or part
film/book/chapter/episode/digital media task
foreign person/place/organization/entity
unsupported physical product
```

If both business fit and foreign context remain plausible, use HOLD, not KEEP or EXCLUDE.

Required gate:

```text
FALSE_KEEP_REGRESSION = PASS
```

---

## 8. Failure class F03B-3 — mechanical accounting PASS was mistaken for semantic PASS

Observed in the original Step03B:

- mechanical QA reported complete accounting and a high self-score;
- independent full-volume semantic audit later found 1,710 normalized identities requiring state change;
- 758 exclusions were unsafe (14 -> KEEP, 744 -> HOLD);
- 286 KEEP rows were unsafe (79 -> EXCLUDE, 207 -> HOLD);
- 666 HOLD rows were deterministically resolvable (298 -> KEEP, 368 -> EXCLUDE);
- the original semantic PASS candidate was revoked.

Anti-regression rule:

```text
ACCOUNTING_QA != SEMANTIC_QA
SELF_SCORE != INDEPENDENT_ACCEPTANCE
```

Any high-volume semantic filter must receive adversarial class-level QA against frozen business scope before acceptance.

When a later independent audit finds a systematic defect, the previous PASS is revoked automatically until corrected.

Required gates:

```text
MECHANICAL_ACCOUNTING = PASS
SEMANTIC_ADVERSARIAL_QA = PASS
KNOWN_BUSINESS_COLLISION_REGRESSIONS = 0
OPEN_CRITICAL_SEMANTIC_DEFECTS = 0
```

---

## 9. Failure class F03B-4 — ambiguous demand was destroyed instead of preserved for later evidence

Anti-regression rule:

Step03B is a high-precision pre-filter, not final intent/SERP classification.

```text
CLEAR OFF-TOPIC -> EXCLUDE
DIRECT BUSINESS-SUPPORTED -> KEEP
MATERIAL AMBIGUITY -> HOLD / SERP_REQUIRED_LATER
```

Low frequency never proves irrelevance. High frequency never proves business fit.

Do not use a commercial delivery cap as a relevance rule.

Required gates:

```text
LOW_FREQUENCY_ONLY_EXCLUSIONS = 0
HIGH_FREQUENCY_ONLY_KEEPS = 0
AMBIGUOUS_SILENT_EXCLUSIONS = 0
DELIVERY_CAP_USED_AS_RELEVANCE_RULE = false
```

---

## 10. Failure class F04-1 — aggregate family counts existed without deterministic occurrence -> family reproducibility

Observed in the first Blood & Sand Step04:

- aggregate family totals reconciled;
- but there was no durable occurrence-level assignment ledger proving exactly which occurrence belonged to which family;
- external audit classified this as a material QA/reproducibility defect.

Anti-regression rule:

Every family-triage execution must publish a deterministic full-volume mapping:

```text
occurrence_identity -> normalized_identity -> sanitation_state -> family_id -> assignment_reason
```

Required gates:

```text
OCCURRENCE_LEDGER_ROWS = TOTAL_OCCURRENCES
UNIQUE_OCCURRENCE_IDS = TOTAL_OCCURRENCES
UNASSIGNED_OCCURRENCE_IDS = 0
UNEXPECTED_DUPLICATE_OCCURRENCE_IDS = 0
FAMILY_COUNT_RECONCILIATION = PASS
```

---

## 11. Failure class F04-2 — representative examples were patched instead of the underlying deterministic rule

Observed in the first Step04 rework cycle:

The external audit identified representative family defects, but the correction contract explicitly required fixing the underlying occurrence->family assignment rules and rerunning the full frozen corpus.

Anti-regression rule:

```text
REPRESENTATIVE DEFECT EXAMPLE != PATCH TARGET
REPRESENTATIVE DEFECT EXAMPLE = PROOF OF A RULE FAILURE
```

When a defect demonstrates a rule failure:

```text
identify defective rule
-> identify blast radius
-> correct rule
-> rerun complete affected universe
-> regression-test representative examples
-> report sibling changes
```

Never manually patch only known examples if the same rule can affect siblings.

Required gate:

```text
KNOWN_DEFECT_EXAMPLES_PASS = true
FULL_AFFECTED_UNIVERSE_REPROCESSED = true
RULE_LEVEL_FIX_DOCUMENTED = true
```

---

## 12. Failure class F04-3 — post-sanitation upstream changes invalidate historical family conclusions

Observed after corrected Step03B:

- 1,710 normalized identities changed sanitation state;
- 1,761 RAW occurrences carry those changed identities;
- 23 of 25 historical Step04 families contain corrected-state transitions.

Anti-regression rule:

A downstream PASS is not immutable when an upstream authority materially changes.

```text
MATERIAL_UPSTREAM_STATE_CHANGE
-> deterministic downstream reconciliation
-> identify affected downstream families/artifacts
-> dedicated semantic re-run if conclusions may change
-> downstream step remains blocked until re-accepted
```

Do not continue to Step05 on historical Step04 family/queue conclusions after material Step03B correction.

Required gate before Step05:

```text
POST_SANITATION_STEP04_RECONCILIATION = PASS
POST_SANITATION_STEP04_SEMANTIC_REWRITE = PASS
MAIN_CHATGPT_RETURN_QA = PASS
```

---

## 13. Universal anti-regression procedure

Every later step must include a `KNOWN_FAILURE_REGRESSION_MATRIX` with at least:

```text
failure_class
applicable_to_current_step
regression_test
result
blocking_if_fail
```

A later Work prompt must explicitly name this Level-1 file as mandatory input.

A QA report that omits applicable known-failure tests cannot score PASS even if all row counts reconcile.

---

## 14. PASS policy

A step may be accepted only if:

```text
METHOD_RULES = PASS
FULL_VOLUME_ACCOUNTING = PASS where applicable
SEMANTIC_QA = PASS where applicable
KNOWN_FAILURE_REGRESSION_MATRIX = PASS
PERSISTENCE_AND_REMOTE_READBACK = PASS for durable outputs
OPEN_CRITICAL_DEFECTS = 0
```

Quality scores do not override a failed hard regression gate.