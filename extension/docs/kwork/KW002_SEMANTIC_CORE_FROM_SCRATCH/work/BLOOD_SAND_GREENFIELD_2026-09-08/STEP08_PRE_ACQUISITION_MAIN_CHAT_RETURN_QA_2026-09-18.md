# KW-002 / BLOOD & SAND — STEP08 PRE-ACQUISITION MAIN CHAT RETURN QA

Date: 2026-09-18
Status: **PASS_ACCEPTED**
Work ID: `KW002_STEP08_PRE_ACQUISITION_RECONCILIATION_2026-09-18`

## 1. Publication/readback

```text
WORK_START_REMOTE_HEAD = 74dd421ec5c38bedcce9ed25b9d86aa71b00beee
WORK_PRE_HANDOFF_REMOTE_HEAD = 74dd421ec5c38bedcce9ed25b9d86aa71b00beee
AUTHORITY_DRIFT_STATUS = NONE

OWNER_STAGING_UPLOAD = OBSERVED
STAGING_FILES = 6/6
STAGING_SHA256_MATCH = 6/6
CANONICAL_PLACEMENT = COMPLETE
CANONICAL_GIT_BLOB_MATCH = 6/6
STAGING_CLEANUP = COMPLETE
REMOTE_READBACK = PASS
```

Canonical files:

- `STEP08_CANDIDATE_PRE_ACQUISITION_RECONCILIATION.csv`
- `STEP08_EXISTING_EVIDENCE_REUSE_REGISTER.csv`
- `STEP08_PROVIDER_SEED_MANIFEST.csv`
- `STEP08_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX.csv`
- `STEP08_PRE_ACQUISITION_QA.md`
- `STEP08_PREPARATION_HANDOFF_MANIFEST.json`

All six canonical Git blobs equal their staged Git blobs and the externally reported SHA-256 values were independently recomputed by Main Chat from GitHub bytes and matched 6/6.

## 2. Full-volume mechanical acceptance

```text
STEP08_ELIGIBLE = 794
ACCOUNTED = 794/794
DISTINCT_CANDIDATE_IDS = 794
SILENT_SKIP = 0

REUSE_EXISTING_EVIDENCE = 38
ALREADY_COVERED_NO_NEW_INFORMATION_GAIN = 7
PROVIDER_REQUIRED_RECALL_FIRST = 437
PROVIDER_REQUIRED_PRECISION_VALIDATION = 312
HOLD_AMBIGUOUS_OR_SCOPE = 0
STEP07_REWORK_REQUIRED = 0

PROVIDER_REQUIRED_CANDIDATES = 749
PROVIDER_SEEDS = 386
PROVIDER_SEED_MEMBER_LINKS = 749
UNIQUE_PROVIDER_MEMBER_IDS = 749
DUPLICATE_PROVIDER_MEMBER_LINKS = 0
UNMAPPED_PROVIDER_REQUIRED_CANDIDATES = 0
EXTRA_PROVIDER_MEMBER_IDS = 0
UNIQUE_PROVIDER_PHRASES = 386
DUPLICATE_PROVIDER_PHRASES = 0
```

## 3. Provider-contract acceptance

All 386 seed rows were checked mechanically.

```text
PROVIDER_EXECUTION_RELEASED_TRUE = 0
BAD_REGION = 0
BAD_DEVICE = 0
MISSING_PHRASE = 0
MISSING_INFORMATION_GAIN = 0
MISSING_OUTCOME_CONTRACT_FIELDS = 0
MISSING_DEPTH_RATIONALE = 0
MISSING_OPERATOR_RATIONALE = 0
BAD_ESTIMATED_COST = 0
```

Depth:

```text
500 = 22
1000 = 250
2000 = 114
```

Research mode:

```text
COLLISION_DIAGNOSTIC = 22
PRECISION_VALIDATION = 250
DISCOVERY_RECALL_FIRST = 114
```

The arithmetic cost remains:

`386 × 0.02 RUB = 7.72 RUB`

under the provider tariff verified for the preparation snapshot.

## 4. Reuse/evidence truth checks

```text
REUSE_ROWS_WITHOUT_DURABLE_LOCATOR = 0
RELATED_BUT_INSUFFICIENT_CLOSED_AS_REUSE = 0
STEP07_RAW_MUTATIONS = 0
PROVIDER_EXECUTION_STARTED = false
WORDSTAT_CALLS = 0
YMB_SEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
GENSEARCH_CALLS = 0
```

Broad or adjacent prior evidence is retained as context but is not used to close narrower qualified questions.

## 5. Adversarial grouping review

Main Chat separately inspected the largest acquisition groups rather than accepting aggregate counts alone.

Examples checked:

- `S08Q0365` — 74 product-name candidates around one `Молот Тора / Мьёльнир` demand-discovery question;
- `S08Q0137` — 29 candidates around `удача / счастье / везение`;
- `S08Q0150` — Muslim amulet/obereg branch;
- `S08Q0250` — rune Othala/Odal branch;
- `S08Q0320` — Slavic amulet branch;
- `S08Q0006` — qualified Alatyr precision-validation branch;
- `S08Q0214` — Algiz rune branch;
- `S08Q0231` — Fehu/Feu rune branch.

These are acquisition-question groups only. The underlying candidate IDs remain separate. No reviewed high-concentration group showed an unrelated cross-topic merge that would justify rejecting the Work result.

## 6. Execution-plan correction found by Main Chat

Work's `execution_chunk` planning produced four quota-sized groups:

```text
CHUNK_001 = 100
CHUNK_002 = 100
CHUNK_003 = 100
CHUNK_004 = 86
```

but those chunks mix provider depths:

```text
CHUNK_001: 91×1000 + 9×2000
CHUNK_002: 22×500 + 46×1000 + 32×2000
CHUNK_003: 52×1000 + 48×2000
CHUNK_004: 61×1000 + 25×2000
```

The current `WORDSTAT_BATCH_API_V1 start` contract accepts one `numPhrases` value for an entire batch job.

Therefore the four Work chunks are **not direct Bridge job definitions**.

This is not a defect in the 794-row semantic reconciliation because the released Step08 preparation explicitly allowed later execution subdivision. Main Chat corrects only the execution transport plan:

```text
JOB D500  = 22 seeds  / numPhrases=500
JOB D1000 = 250 seeds / numPhrases=1000
JOB D2000 = 114 seeds / numPhrases=2000
```

The canonical Work seed manifest remains unchanged as analytical preparation evidence.

## 7. Execution strategy correction

Do not unconditionally execute all 386 requests at once.

Order:

```text
D500 collision diagnostics
-> persist every response before next request
-> after D500 completion, normalize/sanitize/reconcile acquired evidence
-> reassess remaining provider queue
-> only then release D1000

D1000
-> same persistence + reconciliation boundary
-> reassess
-> only then release D2000
```

This preserves information-gain discipline and allows earlier new evidence to eliminate later requests if it genuinely answers them.

## 8. Quality score — Main Chat acceptance

| Criterion | Score |
|---|---:|
| Goal/output completeness | 10/10 |
| Method/source support | 10/10 |
| Input evidence/provenance integrity | 10/10 |
| Coverage/completeness | 10/10 |
| Analytical correctness/claim boundaries | 10/10 |
| Adversarial QA quality | 10/10 |
| Persistence/readback/reproducibility | 10/10 |
| Owner/client usability/plain language | 10/10 |
| Information gain/cost/execution efficiency | 10/10 |
| Downstream readiness | 9/10 |

```text
QUALITY_TOTAL = 99/100
QUALITY_SCORE = 9.9/10
HARD_GATE_FAILURES = 0
OPEN_CRITICAL_DEFECTS = 0
```

The single point withheld is the execution-chunk transport mismatch. It is corrected by the depth-homogeneous execution plan before provider traffic, so it does not invalidate the accepted pre-acquisition reconciliation.

## 9. Acceptance

```text
STEP08_PRE_ACQUISITION_RECONCILIATION = PASS_ACCEPTED
PROVIDER_QUEUE_ANALYTICAL_AUTHORITY = ACCEPTED
PROVIDER_EXECUTION = NOT_STARTED
NEXT = STEP08_PROVIDER_D500_LOCAL_BATCH_START
STEP09_ALLOWED = false
```
