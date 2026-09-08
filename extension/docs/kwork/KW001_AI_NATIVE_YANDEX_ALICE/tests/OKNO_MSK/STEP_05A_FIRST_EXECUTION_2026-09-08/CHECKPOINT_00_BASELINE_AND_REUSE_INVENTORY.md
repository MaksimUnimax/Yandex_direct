# KW-001 / OKNO_MSK — Step 5A first execution baseline and reuse inventory

Date: 2026-09-08  
Status: **PASS — BASELINE FROZEN / PRESERVED EVIDENCE ONLY**

## 1. Execution purpose

This isolated Level-2 execution validates the discovery and selection part of the existing Step 5A method against completed OKNO_MSK research. It reconstructs the preserved 75-query / 750-row ordinary-Yandex ledger, measures recurring domains, traces the later analytical impact supported by completed authorities and selects a bounded competitor set for the next authorized subphase.

It does not change historical Step 0–20 decisions and does not modify any client deliverable.

## 2. Git baseline

```text
repository = MaksimUnimax/Yandex_direct
branch = roadmap/kwork-productization-2026-08-28
starting_remote_head = c043fda14c51b18f4016aa26ff3e3f7e7c121a13
handoff_file = STEP_05A_FIRST_EXECUTION_WORK_HANDOFF_2026-09-08.md
```

The live remote branch was fetched before writing. The expected and observed HEAD values matched.

## 3. Canonical method read before execution

- `STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md`
- `STEP_RULES_INDEX.md`
- `STEP_05A_FIRST_EXECUTION_WORK_HANDOFF_2026-09-08.md`

The method remains a roadmap candidate. This execution cannot promote it to `PROJECT_TEST_VALIDATED`; owner review and the later evidence-producing phases remain separate.

## 4. Preserved SERP sources

| Source | Query indexes | Data rows | SHA-256 |
|---|---:|---:|---|
| `STEP_09_SERP_RESULTS.tsv` | 1 | 10 | `3c2bb777982be527808dab06eae045c5c50b5603830681d3f9752c4c44f3460c` |
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_01.tsv` | 2–20 | 190 | `98c5e166feb603b85ca17ecb4f4217b2c6ba03b519dec108d29fed8f6f5dd18c` |
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_02.tsv` | 21–39 | 190 | `31c579dd4c992c6167de896454641424a4a244940a040f041540fd833745df61` |
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_03.tsv` | 40–58 | 190 | `ca75c8577a43dfd3741732ccffecaa4a365f4f4b8897d83f4f19e256a86658cf` |
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_04.tsv` | 59–75 | 170 | `e995d52e24bf655a8e84735a9b545ec87d8a95289f5a1e99a224e1673512a4cf` |

Expected accounting:

```text
SOURCE_QUERIES = 75
SOURCE_RANKED_ROWS = 750
REGION = 213
RANKS_PER_QUERY = 1..10
```

The first canary source has a wider schema. Only the common supported fields are projected into the combined ledger. No unavailable R2 snippets, provider request IDs, HTTP fields or raw XML are invented.

## 5. Reused analytical authorities

| Authority | Reuse purpose |
|---|---|
| `STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv` | exact preserved Step 9 observation and handoff for all 75 probes |
| `STEP_10_CLUSTER_ASSIGNMENTS.tsv` | query/phrase-level downstream task and cluster assignment where an exact phrase join exists |
| `STEP_10_CLUSTER_SUMMARY.tsv` | cluster-level task label, primary query and evidence state |
| `STEP_11_PAGE_OWNERSHIP_CORRECTED.tsv` | latest corrected cluster ownership and structural state |
| `STEP_11_PHRASE_PAGE_MAP.tsv` | exact phrase-to-page mapping where available |
| `RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv` | latest final phrase/unit/page authority when early tables disagree |
| `RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv` | latest canonical structural-unit decision |
| `RESEARCH_REBUILD_STAGE_07_SEARCH_CASE_EXPLANATION_2026-09-05.tsv` | later client-safe Search-case explanation and claim boundary where an exact representative-query join exists |
| `STEP_19_06_SOURCE_COMPETITOR_OBSERVATIONS.tsv` | preserved competitor-observation summary only; no new inference beyond its rows |

Join policy:

```text
exact query/phrase join first
→ explicit probe ID join where preserved
→ latest corrected/canonical authority takes precedence
→ no causal claim without a preserved downstream link
→ unresolved trace remains UNRESOLVED_TRACE
```

## 6. Domain normalization policy

```text
lowercase hostname
→ strip one leading www.
→ strip trailing dot
→ preserve meaningful subdomains
→ do not merge legally/semantically different hosts by brand guess
```

This prevents recurrence inflation while preserving distinct ranked hosts such as regional/service subdomains.

## 7. Competitor classification boundary

Every normalized domain receives one project routing class:

```text
DIRECT_BUSINESS_COMPETITOR
ORGANIC_COMPETITOR_OTHER_MODEL
AGGREGATOR_DIRECTORY
MARKETPLACE
MANUFACTURER_OR_BRAND_SOURCE
INFORMATIONAL_PUBLISHER
YANDEX_PLATFORM
OTHER_REVIEW
UNKNOWN
```

The class is a Step 5A selection aid, not an official Yandex taxonomy. Recurrence alone does not prove business comparability.

## 8. Acquisition and scope freeze

```text
NEW_YANDEX_SEARCH_CALLS = 0
NEW_WORDSTAT_CALLS = 0
NEW_ALICE_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_WEBMASTER_CALLS = 0
NEW_METRIKA_CALLS = 0
NEW_DIRECT_CALLS = 0
NEW_PAID_PROVIDER_COST_RUB = 0
PUBLIC_COMPETITOR_PAGE_INSPECTION_THIS_EXECUTION = false
```

Competitor pages will not be opened in this execution. Exact evidence-bearing URLs are selected only from the preserved SERP ledger for a later separately authorized inspection/seed phase.

## 9. Protected scope baseline

The complete corrected client release tree and historical Step 0–20 outputs are read-only for this task. In particular:

```text
Document 01 SHA-256 = 79450c2f0dc58ea064b72b7c400f6db7b908cb455c72003584c5e59c9b9fad08
Document 03 SHA-256 = d5c90cf187041e975f17d03a2be138eff0b6a06bfe1b7d395a3b24547edc62b0
Semantic core 04 SHA-256 = cee26a8d7d4a8381d4706c7940b739c3afca652034e9e3630053e35bd0184e3a
```

The later branch state no longer contains the earlier Report №02 PDF path; protection therefore applies to the entire current corrected-release tree exactly as it exists at the starting HEAD, not to a reconstructed historical filename.

## 10. Planned durable blocks

1. baseline and reuse checkpoint;
2. deterministic combined 750-row ledger plus accounting QA;
3. domain frequency/classification and real-competitor inventory;
4. 75-query downstream impact trace;
5. bounded candidate selection, first-execution report, final QA and log.

Each block follows `SAVE → COMMIT → REMOTE GITHUB READBACK`.
