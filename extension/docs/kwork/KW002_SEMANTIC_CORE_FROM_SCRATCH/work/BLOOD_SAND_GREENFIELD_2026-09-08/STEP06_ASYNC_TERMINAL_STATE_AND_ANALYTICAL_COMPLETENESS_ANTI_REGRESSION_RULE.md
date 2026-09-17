# KW-002 — STEP06 ASYNC TERMINAL STATE AND ANALYTICAL COMPLETENESS ANTI-REGRESSION RULE

Status: **OWNER-MANDATED / ACTIVE / UNIVERSAL FOR STEP06 AND REUSABLE FOR ASYNC PROVIDER STEPS**  
Decision date: 2026-09-17

## Purpose

Step06 exposed execution-state, analysis-completeness and artifact-schema failures that can recur even when provider acquisition is mechanically correct.

Keep these states separate:

```text
PROVIDER_TERMINAL
!= FINAL_EXPORT_RECEIVED
!= FULL_ROW_SEMANTIC_CLASSIFICATION
!= ANALYTICAL_HARDENING_COMPLETE
!= STEP_ACCEPTED
```

## A. Latest durable async state always wins

Before every submit/collect/retry/export action, reconcile the newest durable queue/export state. An older conversational cursor has zero action authority.

```text
IF all_successful=true
AND unresolved=0
AND final_export_received=true
THEN submit/collect/retry/export-again = FORBIDDEN
UNLESS an explicit recovery authority exists.
```

## B. Acquisition completeness is not analytical completeness

```text
FULL_SERP_ROWS != FINISHED_SERP_ANALYSIS
```

Step06 requires full-volume semantic classification, Top-10 profiles, collision control, domain recurrence, exact-URL/domain pairwise similarity, hardened competitor registry, limitations and zero final page decisions.

## C. Preliminary labels are provenance, not immutable truth

Preserve `source_serp_class`, but derive accepted intent from actual Top-10 evidence. Later evidence may revise the preliminary class.

## D. Top-10 is primary; Top-20 is discovery

```text
TOP3 = strength amplifier
TOP10 = primary analytical layer
11-20 = secondary discovery/evidence
```

Do not narrate a rank-18 presence as equivalent to first-page competitive strength.

## E. Domain overlap is not cluster proof

```text
SAME DOMAIN != SAME RANKING PAGE
DOMAIN OVERLAP != FINAL CLUSTER PROOF
```

Exact URL overlap must be reported separately. Step06 produces clustering evidence, not final page ownership.

## F. Collision evidence must be preserved but isolated

Never delete collision rows to make the market look cleaner. Keep raw recurrence and explicitly distinguish collision-heavy exposure from target-usable evidence.

## G. Metric granularity must be explicit

A metric that excludes whole collision-heavy/uncertain queries is **query-level filtering**. It must never be called or interpreted as row-level relevance filtering.

Required naming/provenance:

```text
safe_query_subset_* = query-level subset metric
row_target_filtered_* = allowed only if row relevance was actually applied
```

Unqualified `clean_*` labels are prohibited when the filtering unit is ambiguous.

## H. Denominators must follow the accepted analytical population

After Top-10 reclassification, downstream fields must be recomputed against the accepted class counts. Preliminary denominators may be retained only with explicit `source_preliminary_*` provenance.

For current KW-002 hardening:

```text
accepted commercial = 6
accepted informational = 11
accepted hybrid = 1
accepted uncertain = 1
accepted collision/mismatch = 3
collision-heavy audit flags = 4
safe query subset = 17
```

A hardened registry containing unlabeled stale `commercial_*_8` / `informational_*_9` metrics is a FAIL.

## I. Page-type taxonomy must be extensible

A fixed generic enum may hide recurring SERP surfaces. If a materially recurring type appears (for example audio/listening surfaces), either:

1. add a specific type such as `AUDIO`; or
2. explicitly disclose that those surfaces are collapsed into `OTHER` by the frozen classification schema.

Do not silently imply that `OTHER` is analytically homogeneous.

## J. SERP features cannot be inferred when not captured

```text
SERP_FEATURE_COVERAGE = NOT_CAPTURED_BY_CURRENT_SOURCE
```

Absence in normalized organic rows is not evidence of absence in live SERP.

## K. Region/device and snapshot scope are mandatory

Step06 conclusions must identify the acquisition region and device scope when known. Unknown device segmentation must be recorded as unknown/not captured.

One acquisition snapshot does not prove long-term Yandex stability.

## L. Final page decisions remain outside Step06

No `CREATE`, `MERGE`, `KEEP`, final query→page ownership or automatic page decision may be derived solely inside Step06.

## M. Work transport rule must not be generalized to Main

The owner-mediated ZIP workflow applies to delegated Work. Main ChatGPT normally publishes Main-created/edited artifacts itself unless the owner explicitly chooses otherwise for the bounded task or a real technical limitation exists.

## N. Existing published Work artifacts must not be reconstructed without a defect

Before publication work, inventory remote state first. If a Work artifact already exists and is accepted as input, downstream hardening should reference it; do not recreate/re-upload it merely because new derived artifacts are being added.

## O. Low-level staging is not publication

Orphan blobs or temporary upload objects not attached to a commit/ref are not project state. Do not create/stage transport objects before the final file set is proven.

## PASS gates

```text
LATEST_STATE_RECONCILED = PASS
ACTION_FROM_STALE_CURSOR = 0
POST_TERMINAL_PROVIDER_ACTION = 0
FULL_ROW_CLASSIFICATION = PASS
TOP10_QUERY_PROFILES = COMPLETE
PAIRWISE_SERP_COMPARISON = COMPLETE
COLLISION_CONTROL = PASS
METRIC_GRANULARITY_EXPLICIT = true
STALE_ACCEPTED_DENOMINATORS = 0
PAGE_TYPE_LIMITATIONS_DISCLOSED = true
REGION_SCOPE_DISCLOSED = true
DEVICE_SCOPE_DISCLOSED = true
SERP_FEATURE_LIMITATION_DISCLOSED = true
SNAPSHOT_LIMITATION_DISCLOSED = true
FINAL_PAGE_DECISIONS = NONE
STEP07_STARTED = false
```
