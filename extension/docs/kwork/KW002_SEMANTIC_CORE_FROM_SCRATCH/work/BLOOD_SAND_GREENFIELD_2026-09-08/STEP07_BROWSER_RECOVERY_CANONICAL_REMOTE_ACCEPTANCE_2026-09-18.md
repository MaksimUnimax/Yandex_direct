# KW-002 / BLOOD & SAND — STEP07 BROWSER RECOVERY CANONICAL REMOTE ACCEPTANCE — 2026-09-18

Status: **REMOTE READBACK PASS / CANONICAL BROWSER RECOVERY ACCEPTED / SEMANTIC REWORK MAY BE RELEASED**

Job: `BLOOD_SAND_GREENFIELD_2026-09-08`  
Owner upload base: `fa5b748d10a5a3f2a85e427d316f5856fb124778`  
Owner upload head: `599af13c5007e1c2482e89a63f5d9ff4d9af3491`

## 1. Verdict

```text
OWNER_SINGLE_STAGING_BYTE_RELAY = COMPLETE
OWNER_UPLOAD_COMMIT_COUNT = 1
OWNER_UPLOAD_EXPECTED_FILES = 7
OWNER_UPLOAD_ACTUAL_FILES = 7
UNRELATED_FILE_CHANGES = 0
REMOTE_GIT_BLOB_IDENTITY = 7/7 PASS
REMOTE_BYTE_IDENTITY = PASS
CANONICAL_BROWSER_RECOVERY_ACCEPTED = true
STEP07_SEMANTIC_REWORK_MAY_BE_RELEASED = true
STEP07 = INCOMPLETE_REWORK_REQUIRED
STEP08 = BLOCKED_NOT_STARTED
```

## 2. Exact remote byte identity

| file | bytes | SHA-256 | Git blob SHA-1 |
|---|---:|---|---|
| STEP07_BROWSER_RECOVERY_URL_LEDGER.csv | 1,602,463 | `2fb8a69b6861a1e9934b0976dbf44029a79579d93457c284bd50ba5c392cf0e2` | `463ed40cf70dfe055916e0b5d38fe95b7bb4623d` |
| STEP07_BROWSER_RECOVERY_PAGE_EVIDENCE.jsonl | 22,331,292 | `7eefe0001428c926680faab9218bda9d7ddfd197347dd97b6140e993d7353592` | `950ea55d01d99248c502d13a45c57060d25c0a2d` |
| STEP07_BROWSER_RECOVERY_COVERAGE.csv | 7,286 | `8cd07a7c1b21e9495d276ab8c7a53c4a8f34525dfb305684dcc811411b8433ce` | `bced94f60fcb51bee6cc9c461b2054c21522d4d5` |
| STEP07_BROWSER_RECOVERY_QA.md | 3,456 | `46d8885743a2ae3358a3e6a11ec57c57438c156b0a6d00e1030ae0a5bcb1ee83` | `9d76d243c1dd31cfbec9c058a65a8ac57a8c6bca` |
| STEP07_BROWSER_RECOVERY_RETRY_AUDIT.csv | 49,250 | `1cbe984c47854eeb55eb1a1a07fc3134a030a1a841cd6a7f22e82326a01295a6` | `911da3c06e9f478c28e94e58f1641869689ceb5b` |
| STEP07_BROWSER_RECOVERY_RESIDUAL_RETRY_AUDIT.csv | 70,666 | `ad77bad53a960c6ea37f4689f556e2f92f17bc5a57fcdd0dfaa0d7b6a03faf3d` | `440e4df546720e2dfd7f6ed4a36ab5394f55dca1` |
| STEP07_BROWSER_RECOVERY_HANDOFF_MANIFEST.json | 2,473 | `e5bad200b5f460f266ecc6305db874edc5c92ebcb215baf6eac374c3b4f58b1e` | `4c996b570723a55f7427c7d3d57ebe4a7d42a84f` |

The large page-evidence payload was verified without model retransmission by matching its exact locally computed Git blob identity to the remote Git blob identity.

## 3. Accepted recovery accounting

```text
AUTHORIZED_COMPETITORS = 32
SOURCE_URL_ROWS = 1976
PAGE_EVIDENCE_ROWS = 725
FROZEN_BROWSER_RETRY_ROWS = 90
FROZEN_RECOVERED_INSPECTED = 66
FROZEN_TARGET_BLOCK = 24
FROZEN_EXECUTION_ENVIRONMENT_FAILURE = 0
FROZEN_UNRESOLVED_DYNAMIC_CONTENT = 0

GLOBAL_EXCLUDED_OUT_OF_SCOPE = 1201
GLOBAL_EXCLUDED_DUPLICATE = 24
GLOBAL_RECOVERED_INSPECTED = 432
GLOBAL_REDIRECTED_IN_SCOPE = 293
GLOBAL_TARGET_CAPTCHA_OR_ANTI_BOT = 26
GLOBAL_EXECUTION_ENVIRONMENT_FAILURE = 0
GLOBAL_UNRESOLVED_DYNAMIC_CONTENT = 0
TOTAL = 1976
```

The 26 target-block rows are governed inaccessible evidence, not execution-environment failures. No bypass was attempted.

## 4. Boundaries

```text
NEW_WORDSTAT_CALLS = 0
NEW_YANDEX_SEARCH_CALLS = 0
NEW_AI_SEARCH_CALLS = 0
NEW_GENSEARCH_CALLS = 0
STEP08_STARTED = false
FINAL_INTENT_DECISIONS = NONE
FINAL_CLUSTER_DECISIONS = NONE
FINAL_PAGE_DECISIONS = NONE
```

## 5. Quality score

| Criterion | Score /10 | Basis |
|---|---:|---|
| Goal and output completeness | 10 | Frozen recovery unit is fully terminal and remotely published. |
| Method and source support | 10 | Recovery follows the accepted Step07 public-access/claim boundary. |
| Input evidence and provenance integrity | 10 | Exact frozen IDs, URL lineage and page evidence are preserved. |
| Coverage and completeness | 10 | 90/90 residual rows terminal; 32/32 competitors accounted; target blocks explicit. |
| Analytical correctness and claim boundaries | 10 | Access evidence is not misrepresented as demand/intent/page truth. |
| Adversarial QA quality | 10 | Environment failures were separated from legitimate target blocks and rechecked. |
| Persistence/readback/reproducibility | 10 | 7/7 exact Git blob identities match local bytes. |
| Owner/client usability/plain language | 10 | One staging relay closed the transport boundary without owner routing. |
| Information gain/cost/execution efficiency | 10 | No provider calls or duplicate recovery work remain. |
| Downstream readiness | 10 | Semantic rework can consume the accepted 725-row evidence set. |

```text
QUALITY_TOTAL = 100 / 100
QUALITY_SCORE = 10.0 / 10
HARD_GATE_FAILURES = 0
BROWSER_RECOVERY_ACCEPTANCE = PASS
```

## 6. Transition

```text
STEP07_BROWSER_RECOVERY = CANONICAL_REMOTE_ACCEPTED
STEP07_SEMANTIC_REWORK = ELIGIBLE_FOR_RELEASE
STEP07 = INCOMPLETE_REWORK_REQUIRED
STEP08 = BLOCKED_NOT_STARTED
```

Next physical action: release the current full-volume Step07 semantic rework against the exact accepted browser-recovery inputs.
