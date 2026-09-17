# KW-002 / BLOOD & SAND — STEP07 EXECUTION RELEASE REVALIDATION QA

Date: 2026-09-17  
Scope: Main Chat release gate + corrected execution-only Work prompt  
Actual Step07 competitor extraction: **NOT EXECUTED YET**

## 1. Role-boundary QA

```text
MAIN_CHAT_FULL_RULE_REREAD = PASS
MAIN_CHAT_CURRENT_JOB_STATE_READ = PASS
MAIN_CHAT_FAILURE_INCIDENT_REVIEW = PASS
MAIN_CHAT_FRESH_EXTERNAL_RESEARCH = PASS
MAIN_CHAT_CLICKABLE_SOURCE_DISCLOSURE = PASS
MAIN_CHAT_SOURCE_TO_METHOD_TRACE = PASS
MAIN_CHAT_PLAIN_LANGUAGE_SUMMARY = PASS
MAIN_CHAT_WORK_PROMPT_RELEASE = PASS

WORK_FULL_LEVEL1_REREAD_REQUIRED = false
WORK_FRESH_EXTERNAL_RESEARCH_REQUIRED = false
WORK_OWNER_FACING_REPORT_REQUIRED = false
WORK_RELEASE_REAUTHORIZATION_REQUIRED = false
WORK_RULE_READ_LEDGER_REQUIRED = false
WORK_NARROW_CURRENT_HEAD_AND_INPUT_DRIFT_PREFLIGHT = true
```

## 2. Prompt defects corrected

The initial release prompt wrongly duplicated Main Chat governance inside Work. That defect has now been removed.

Corrected prompt properties:

1. Work receives a concrete actual-Step07 execution task.
2. Work does not reread the full Level1 governance stack.
3. Work does not rerun fresh methodology research.
4. Work does not repeat owner-facing source disclosure/plain-language reporting.
5. Work does not decide whether Step07 should be released.
6. Work performs only current-HEAD/release/input/schema/hash drift checks.
7. Work processes all 32 authorized competitors at full bounded volume.
8. Work creates exactly six handoff files.
9. `STEP07_EXECUTION_RULE_READ_LEDGER.md` has been removed from required outputs.
10. Work does not mutate `JOB_FLOW.md` or cursor.
11. Work uses one owner staging target and one transport ZIP.
12. Main Chat retains post-upload readback, acceptance and mutable-state updates.

## 3. Current Work prompt identity

```text
WORK_PROMPT_COMMIT = be0aee668712d1ab04317457b0e8d2b38845b2a0
WORK_PROMPT_BLOB = 3070c6e9e5e75bcc510f04aa09f76d119f69770f
WORK_PROMPT_SCOPE = ACTUAL_STEP07_EXECUTION_ONLY
```

## 4. Step07 hard release invariants

```text
AUTHORIZED_COMPETITOR_UNIVERSE = 32
FULL_VOLUME_NO_SAMPLE = true
SOURCE_REGISTRY_HASH_FROZEN = true
STEP07_PROVIDER_CALLS_AUTHORIZED = 0
STEP08_STARTED = false
FINAL_INTENT_DECISIONS_ALLOWED = 0
FINAL_CLUSTER_DECISIONS_ALLOWED = 0
FINAL_PAGE_DECISIONS_ALLOWED = 0
SINGLE_STAGING_OWNER_RELAY = true
OWNER_FINAL_PATH_ROUTING_REQUIRED = false
WORK_GITHUB_COMMIT_PUSH_PR_ALLOWED = false
```

## 5. Required Work output set

```text
1. COMPETITOR_GAP_CANDIDATES.csv
2. STEP07_COMPETITOR_COVERAGE_LEDGER.csv
3. STEP07_SOURCE_URL_LEDGER.csv
4. STEP07_CANDIDATE_PROVENANCE_LEDGER.csv
5. STEP07_EXECUTION_QA.md
6. STEP07_EXECUTION_HANDOFF_MANIFEST.json
```

Exactly six required handoff files.

## 6. Quality score

Each criterion independently out of 10:

| Criterion | Score / 10 | Basis |
|---|---:|---|
| Goal and output completeness | 10 | Release prompt now contains the concrete full-volume Step07 execution contract without governance duplication. |
| Method and source support | 10 | Main Chat already completed fresh method/source review and preserved claim boundaries. |
| Input evidence and provenance integrity | 10 | 32-authority competitor universe and accepted upstream reconciliation inputs remain unchanged. |
| Coverage and completeness | 10 | All 32 competitors and bounded-frontier exhaustion remain mandatory; no sampling. |
| Analytical correctness and claim boundaries | 10 | Step07 remains candidate discovery only; demand/intent/cluster/page decisions remain downstream. |
| Adversarial QA quality | 10 | Owner correction exposed and removed duplicated Main-governance runtime gates. |
| Persistence, readback and reproducibility | 9 | Current prompt/release files are persisted; actual Work output readback is future work. |
| Owner/client usability and plain language | 10 | Owner relays one prompt and later one staging upload; Work is no longer burdened with unrelated governance. |
| Information gain / cost / execution efficiency | 10 | Removed unnecessary Work rereads/research/reporting while preserving a narrow drift safety check. |
| Downstream readiness | 10 | Actual Step07 is correctly released; Step08 remains blocked until Step07 acceptance. |

```text
QUALITY_TOTAL = 99 / 100
QUALITY_SCORE = 9.9 / 10
HARD_GATE_FAILURES = 0
RELEASE_QA = PASS
```

## 7. Release boundary

```text
STEP07_PREPARATION = ACCEPTED
STEP07_MAIN_CHAT_RELEASE_REVALIDATION = PASS
STEP07_EXECUTION_ALLOWED = true
STEP07_RELEASED_FOR_WORK_RELAY = true
STEP07_EXECUTED = false
STEP08_STARTED = false
```

Next action: relay the corrected execution-only Work prompt and let Work execute Step07 directly after its bounded technical drift preflight.
