# KW-002 — STEP07 PRE-HANDOFF / INPUT AUTHORITY MANIFEST

Manifest ID: `KW002_STEP07_PREPARATION_2026-09-17`  
Step prepared: `STEP07_COMPETITOR_SEMANTIC_EXPANSION`  
Repository: `MaksimUnimax/Yandex_direct`  
Branch: `roadmap/kwork-productization-2026-08-28`  
Live remote HEAD used: `0630d3f6dbd1962290dc8ab77a454e86c604a795`  
Prepared: 2026-09-17  
Status: **LOCAL PREPARATION COMPLETE / PUBLICATION AND REMOTE READBACK PENDING**

```text
STEP07_PREPARATION = COMPLETE_LOCALLY
STEP07 = NOT_STARTED
STEP08 = NOT_STARTED
MAIN_CHAT_ACCEPTANCE = PENDING
```

---

## 1. Repository locations

```text
PROJECT_ROOT = extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH
LEVEL1_ROOT = extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/LEVEL1
LEVEL2_ROOT = extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/LEVEL2
JOB_ROOT = extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08
```

Future Step07 must fetch the current remote branch first. If live HEAD differs,
apply `WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md` before using this
manifest.

---

## 2. Applicable rule authority read during preparation

Current live rule files read in full or as the current applicable authority:

- `LEVEL1/COMMON_RULES.md`;
- `LEVEL1/INHERITED_KW001_UNIVERSAL_RULES.md`;
- `LEVEL1/WORK_HANDOFF_RULE.md`;
- `LEVEL1/WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md`;
- `LEVEL1/WORK_ARTIFACT_HANDOFF_AND_OWNER_PUBLICATION_RULE.md`;
- cross-Kwork `KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md`;
- `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`;
- `LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md`;
- `LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`;
- `LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md`;
- `LEVEL1/CLIENT_INTAKE_AND_SCOPE_RULE.md`;
- `LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`;
- `LEVEL1/RESULT_QUALITY_SCORING_RULE.md`;
- `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`;
- `LEVEL1/STEP06_ASYNC_TERMINAL_STATE_AND_ANALYTICAL_COMPLETENESS_ANTI_REGRESSION_RULE.md`;
- `LEVEL1/SERP_COVERAGE_MODE_DECISION_2026-09-10.md`;
- `LEVEL1/YANDEX_MARKETING_BRIDGE_EXECUTION_RULE.md`;
- `LEVEL2/INHERITED_KW001_STEP_RULES.md`;
- `LEVEL2/STEP_04_PRELIMINARY_FAMILY_TRIAGE_QUALITY_GATE.md`;
- `LEVEL2/STEP_05_TARGETED_EXPANSION_AND_PROVIDER_EXECUTION_GATE.md`;
- `LEVEL2/STEP_06_SEARCH_COMPETITOR_SERP_ANALYSIS.md`;
- `LEVEL2/STEP_RULES_INDEX.md`;
- current job `JOB_FLOW.md`, accepted upstream manifests, QA and acceptance
  records.

### 2.1 Remembered names that do not exist at live HEAD

Repository tree/search/backlinks were exhausted for the following literal
filenames. They were not invented. Their current authority was resolved as
shown:

| Missing literal filename | Current live equivalent(s) used |
|---|---|
| `CACHE_FIRST_AND_NO_REPEAT_PAID_CALLS_RULE.md` | `INHERITED_KW001_UNIVERSAL_RULES.md` Rules 8–9; `EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`; Step05 Level2 gate |
| `QUERY_UNIVERSE_NO_SAMPLE_AND_ITERATIVE_RESEARCH_RULE.md` | `WORK_HANDOFF_RULE.md`; `DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`; inherited full-volume rules; `STEP_RULES_INDEX.md` |
| `EXECUTION_COMPLETENESS_AND_STATUS_REPORT_RULE.md` | inherited execution-completeness/status rules; `RESULT_QUALITY_SCORING_RULE.md`; `JOB_DATA_SEPARATION_AND_LIFECYCLE.md` |
| `PRODUCT_SEMANTIC_CORE_EXECUTION_ROUTE_RULE.md` | `STEP_RULES_INDEX.md`; `COMMON_RULES.md`; `METHOD_SOURCE_AND_EVIDENCE_RULES.md` |
| `PROJECT_CANONICAL_STATE_SNAPSHOT_RULE.md` | `WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md`; `JOB_DATA_SEPARATION_AND_LIFECYCLE.md`; current accepted manifests |
| `PROJECT_SEMANTIC_CORE_BUILD_STANDARD.md` | `COMMON_RULES.md`; `STEP_RULES_INDEX.md`; `DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md` |
| `RULE_AUTHORITY_AND_ARTIFACT_PLACEMENT.md` | `COMMON_RULES.md`; `ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`; `JOB_DATA_SEPARATION_AND_LIFECYCLE.md` |
| `RULES.md` | `COMMON_RULES.md`; `INHERITED_KW001_UNIVERSAL_RULES.md` |
| `SAFE_ITERATION.md` | `EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`; `WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md` |
| `FIXED_QUERY_DOMAIN_COLLISION_AND_REENTRY_RULE.md` | Step03B collision classes; Step06 anti-regression rule; current Step06 collision ledger; new Step07 Level2 rule |

---

## 3. Verified upstream state

| Stage | Live accepted state used | Full-volume verification |
|---|---|---|
| Step03A | 25,979 raw occurrences; 24,576 normalized identities | Unique occurrence and identity keys; complete mapping |
| Step03B | KEEP 5,100; HOLD 13,035; EXCLUDE 6,441; total 24,576 | Partition has no duplicate identity and equals Step03A identity universe |
| Step04 | 32 families; 24,576 identity rows; 25,979 occurrence rows; 13 queue rows | Identity and occurrence joins equal Step03A; all 32 family gates PASS |
| Step05 | 13/13 queue rows reconciled; one provider candidate executed once; zero returned result/association rows; zero new union rows | Current W10 V2/V3 accepted closure files inspected |
| Step06 | 22 queries; 440 classified SERP rows; 22 Top-10 profiles; 231 pairs; 165 recurrence domains; 32 curated competitors; 5 collision/uncertainty rows | Query/rank uniqueness and all counts mechanically verified |

### 3.1 Step05 orientation conflict

The pre-handoff orientation stated:

```text
CANDIDATES = 13/13 successful
TOTAL_VIEWS = 259600
UNIQUE_PHRASES = 200577
OVERLAP_WITH_STEP03B_KEEP = 2658
```

Those figures are not present in, and are not supported by, the current live
accepted KW-002 Step05 W10 V2/V3 authority at the frozen HEAD. Current accepted
evidence instead proves:

```text
QUEUE_ROWS_RECONCILED = 13/13
NEW_PROVIDER_CANDIDATES = 1
EXECUTED_PROVIDER_CANDIDATES = 1
W10C001_OUTCOME = SUCCESS_WITH_ZERO_ROWS
TOTALCOUNT_AGGREGATE = 3
RETURNED_RESULT_ROWS = 0
RETURNED_ASSOCIATION_ROWS = 0
NEW_UNION_ROWS = 0
```

Per the task instruction, live accepted repository authority prevails. The
unconfirmed orientation figures are excluded from Step07 reconciliation and
recorded as an authority-drift issue rather than silently copied.

---

## 4. Canonical input authority and real schemas

Paths are relative to repository root.

### 4.1 Step03A / Step03B semantic identity and sanitation authority

| Path | Role/status | Rows | Practical key | Relevant fields | SHA-256 |
|---|---|---:|---|---|---|
| `JOB_ROOT/STEP_03A_NORMALIZATION_LEDGER_2026-09-11.tsv` | Canonical occurrence provenance | 25,979 invariant | `occurrence_id` | `raw_phrase`, `raw_count`, `exact_normalized_key`, `normalized_phrase_id`, seed/provider/carrier lineage | `28205ca64f26d219d489b36f102a8923b4a4b635c8b213179bca4a188b24c3df` |
| `JOB_ROOT/STEP_03A_NORMALIZED_UNIQUE_POOL_2026-09-11.tsv` | Canonical normalized identity universe | 24,576 invariant | `normalized_phrase_id`; exact join by `exact_normalized_key` | `canonical_phrase`, raw variants/IDs, seed/provider lineage, duplicate state | `b30c29ff66a56d80bc1aa9ff6b2eade522b27d1e167cbd636ac72fbff211f2a8` |
| `JOB_ROOT/STEP_03B_SANITIZED_CANDIDATE_POOL_CORRECTED_2026-09-11.tsv` | Current corrected KEEP authority | 5,100 invariant | `normalized_phrase_id` | `canonical_phrase`, `sanitation_state`, reason/rule, business fit, ambiguity, lineage | `63b3fc556b388dbac0185f174f79f825dc26d9c51de39698850cdaecb9ca4f58` |
| `JOB_ROOT/STEP_03B_EXCLUDED_HOLD_REGISTER_CORRECTED_2026-09-11.tsv` | Current corrected HOLD+EXCLUDE authority | 19,476 invariant | `normalized_phrase_id` | same state/reason/business/ambiguity basis | `145c5107f40415b4050923f142dab3e83646489da5d74501f659fd87e3ae2916` |
| `JOB_ROOT/STEP_03B_REASON_CODE_ACCOUNTING_CORRECTED_2026-09-11.tsv` | Supporting accepted taxonomy/accounting | 42 invariant | (`corrected_state`,`sanitation_reason_code`) | deterministic basis, confidence, identity/occurrence counts | `685a38a9cf3f712974f01ad87db4e482d82ead70978afb0aecb1fa0a223d81c4` |

Evidence class: acquired search-demand lineage plus accepted deterministic
normalization/sanitation. Historical uncorrected Step03B files are supporting
history only and MUST NOT be used as current authority.

### 4.2 Step04 preliminary semantic authority

| Path | Role/status | Rows | Practical key | Relevant fields | SHA-256 |
|---|---|---:|---|---|---|
| `JOB_ROOT/STEP_04_CURRENT_AUTHORITY_FAMILY_TRIAGE_2026-09-11.tsv` | Current W09 preliminary family authority | 32 invariant | `family_id` | definition/boundaries, representative phrases, counts, task hypothesis, ambiguity, coverage, `final_intent_status`, `serp_cluster_status` | `62e21ed2ae10124496d4043d933a3b8a0bad60306ec6920e0524e255f9e216c9` |
| `JOB_ROOT/STEP_04_CURRENT_AUTHORITY_IDENTITY_SIGNAL_LEDGER_2026-09-11.tsv` | Current identity→family/context ledger | 24,576 invariant | `normalized_phrase_id` | Step03B state/reason, primary preliminary family, signals, ambiguity, later evidence | `419fd6eaf7984c0f53c8772e22a251447193285276995b3fc343b524ab1dd8aa` |
| `JOB_ROOT/STEP_04_CURRENT_AUTHORITY_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv` | Current occurrence provenance/family ledger | 25,979 invariant | `raw_occurrence_id` | normalized identity, raw phrase, Step03B state, W09 family/reason/signals | `cf9c8fbe23c2f4b6504ccd19a698ce99f92a2c2b68caa461981544df91d42fb3` |
| `JOB_ROOT/STEP_04_CURRENT_AUTHORITY_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv` | Current gap-hypothesis queue | 13 invariant | `queue_id` | family, problem, evidence reconciliation, owner fact/provider eligibility, information gain, stop condition | `2a4527360f54f53915eed6c4234074680eb61d22b9a0fbf3dbfc03466e14f262` |

Evidence class: preliminary family/task context only. It is not final intent,
SERP clustering or page authority. `STEP_04_POST_AUDIT_CORRECTED_*` and earlier
Step04 generations are historical/superseded for current joins.

### 4.3 Step05 gap closure authority

| Path | Role/status | Rows | Practical key | Relevant fields | SHA-256 |
|---|---|---:|---|---|---|
| `JOB_ROOT/STEP_05_W10_V2_QUEUE_RECONCILIATION_WORK_2026-09-12.tsv` | Accepted 13-row queue reconciliation | 13 invariant | `queue_id` | disposition, existing evidence, candidate ID/phrase, duplicate/collision checks, later route | `5851276995b31ad5bb919cfed17d7e953ad77a9be0aca982e0d25f13ef0df41d` |
| `JOB_ROOT/STEP_05_W10_V3_PROVIDER_CANDIDATE_MANIFEST_2026-09-12.tsv` | Final one-candidate execution/closure authority | 1 invariant | `candidate_id` | phrase, request scope, depth/outcome contract, raw path, downstream rule, execution status | `eacadc20fcc7305519e0b4b2dfa5a034bbf575ee4db5d7737398b2e9feeefb40` |
| `JOB_ROOT/STEP_03_WORDSTAT_RAW/STEP05__W10C001__wordstat-b3fbe6dd-121b-4e67-81ca-0b03bdc53358.txt` | Durable raw provider evidence; supporting join only | Complete one-request envelope; zero phrase rows | provider request ID | request/response envelope | `3eab6f90b9d69cdeb242bf761619de75e29307191535181e35600723667fd3af` |

Step05 adds no new candidate phrase rows to the accepted identity universe.
Future Step07 still reconciles against Step05 closure to avoid reopening a
closed spelling/scope question or inventing demand from `totalCount=3`.

### 4.4 Step06 search-competitor authority

| Path | Role/status | Rows | Practical key | Relevant fields | SHA-256 |
|---|---|---:|---|---|---|
| `JOB_ROOT/KW002_STEP06_SEARCH_COMPETITOR_REGISTRY_HARDENED.csv` | **Sole competitor-admission authority** | 32 invariant for frozen snapshot | `canonical_site` | `site`, class, priority, inclusion basis, collision dependency, evidence queries, coverage metrics | `b15e601db56d8f3c23d7a8c4a2193fc14000dc9773229d693c200756240efcdb` |
| `JOB_ROOT/KW002_STEP06_SERP_URL_EVIDENCE_440_CLASSIFIED.csv` | Row-level URL/query/rank lineage and semantic evidence | 440 invariant | (`query_id`,`rank`) | URL/domain/title/snippet plus classification fields | `32c9dca0d2c81fd04641803c7243d48021ce6510e5f7d6c4d5c54b47afec0726` |
| `JOB_ROOT/KW002_STEP06_QUERY_TOP10_PROFILE.csv` | Accepted query-level Top-10 profile | 22 invariant | `query_id` | purity, page composition, accepted intent/confidence/basis | `7a1163a9ea7e5501be3836dc1a1b400376fb9a2339ce07fd0894536f574d1c7d` |
| `JOB_ROOT/KW002_STEP06_QUERY_SERP_ASSESSMENT_HARDENED.csv` | Hardened per-query treatment/boundaries | 22 invariant | `query_id` | collision flag, treatment, region/device/snapshot limits, final page state | `d63245026ded5b9c86f25144a46867dd8d4c0a04ffcb2d1b8bce3c57c44aeb74` |
| `JOB_ROOT/KW002_STEP06_COLLISION_AND_UNCERTAINTY_LEDGER_HARDENED.csv` | Collision/uncertainty control | 5 invariant | `query_id` | issue class, counts, treatment, accepted intent/confidence | `508ca38763218009f9302953d62817fe228cb2d1cd6508e819e1c30d940c30fb` |
| `JOB_ROOT/KW002_STEP06_DOMAIN_RECURRENCE_HARDENED.csv` | Complete recurrence universe; supporting only | 165 invariant | `site` | rank/query coverage and safe/collision views | `2c61addb42fad941fd4c5d7e9fde42d29d180c3aa7c6ff85b67ff068644fd599` |
| `JOB_ROOT/KW002_STEP06_SERP_SIMILARITY_MATRIX.csv` | Pairwise query overlap; supporting only | 231 invariant | (`query_a_id`,`query_b_id`) | URL/domain overlap and Jaccard | `011f704f6b1abfe6d2407afc5dd24e818888588a8810fd3209acdc8e29b0ef09` |
| `JOB_ROOT/STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V2_2026-09-12.tsv` | Query design lineage; supporting accepted input | 22 invariant | `query_id` | source family, query role, provider settings/status | `7f26c6ff353bee0ec172a5e98762fcc164b6e5c457d40696dcd9bb086f1d098c` |

Evidence class: bounded observed Yandex SERP snapshot. It does not prove
long-term stability. Raw recurrence rows do not authorize a competitor unless
the domain is also in the 32-row curated registry.

---

## 5. Frozen future Step07 competitor authority

Canonical control file:

`JOB_ROOT/STEP_07_AUTHORIZED_COMPETITOR_UNIVERSE.csv`

It has exactly 32 rows and maps `S07A001`–`S07A032` one-to-one to the 32 current
Step06 registry rows. It preserves registry site/canonical site, class,
priority, inclusion basis, collision dependency, observed query IDs, row/URL
counts and source registry hash.

Authority rules:

```text
AUTHORIZED_COMPETITORS = 32
SOURCE_REGISTRY_ROWS = 32
ONE_TO_ONE_MAPPING = true
UNIQUE_CANONICAL_SITE = true
EVERY_AUTHORIZED_SITE_HAS_STEP06_URL_EVIDENCE = true
RAW_RECURRENCE_DOMAINS_AUTO_ADMITTED = 0
ARBITRARY_EXTERNAL_COMPETITORS = 0
```

Registry composition:

- 7 `BROAD_COMMERCIAL_PLATFORM`;
- 5 `BROAD_INFORMATIONAL`;
- 5 `CLUSTER_SPECIFIC_COMMERCIAL`;
- 1 `SPECIALTY_COMMERCIAL`;
- 2 `SPECIALTY_COMMERCIAL_HYBRID`;
- 1 `THEMATIC_INFORMATIONAL`;
- 4 `THEMATIC_INFORMATIONAL_CHRISTIAN`;
- 5 `THEMATIC_INFORMATIONAL_RUNES`;
- 1 `THEMATIC_INFORMATIONAL_RUNES_SLAVIC`;
- 1 `THEMATIC_INFORMATIONAL_SLAVIC`.

Priority: 28 `PRIMARY_TOP10`, 4 `SECONDARY_DISCOVERY_ONLY`.  
Collision dependency: 26 `NONE`, 6 `PARTIAL_COLLISION_CONTAMINATION`.

### 5.1 Domain/subdomain policy

- `canonical_site` is the authority identity.
- `www` is allowed only as the same host presentation alias.
- IDNA display/canonical equivalence is preserved; for example the Cyrillic
  display host and its Punycode canonical host are one mapped authority row.
- Sibling subdomains, country/language variants and mobile hosts are not
  inherited.
- `market.yandex.ru`, `ru.wikipedia.org`, `ru.ruwiki.ru`,
  `ru.wiktionary.org` and `blog.beregy.ru` authorize those exact subdomains,
  not their parent/sibling domains.

### 5.2 Scope policy

- Broad platforms/information sites: `EVIDENCE_ANCHORED_RELEVANT_SUBTREE`.
- Specialized/thematic sites: `THEME_SCOPED_PUBLIC_TAXONOMY`.

The exact assignment is stored per authority row in the control CSV.

---

## 6. Reconciliation join contract

| Order | Join/action | Exact rule |
|---:|---|---|
| 1 | Candidate comparison key | Use Step03A-compatible NFC + trim + whitespace collapse + casefold comparison; retain raw and normalized candidate separately. |
| 2 | Step03A exact identity lookup | Join candidate comparison key to `exact_normalized_key`; an exact match supplies `normalized_phrase_id`. |
| 3 | Step03B state | Join `normalized_phrase_id` across corrected KEEP and HOLD/EXCLUDE partition; exactly one state must resolve for an upstream match. |
| 4 | Step04 context | Join `normalized_phrase_id` to current W09 identity signal ledger; family/ambiguity is context, not duplicate or final-intent proof. |
| 5 | Step05 closure | Compare exact candidate wording/scope to queue and W10C001 closure; do not transfer aggregate counts or reopen automatically. |
| 6 | Candidate status | Assign exactly one of `ALREADY_PRESENT`, `NEW_CANDIDATE`, `NORMALIZED_DUPLICATE`, `POSSIBLE_VARIANT`, `OUT_OF_SCOPE`, `AMBIGUOUS`. |
| 7 | Step08 route | Only `NEW_CANDIDATE` and eligible `POSSIBLE_VARIANT` may route forward; demand remains unvalidated. |

Historical or superseded files MUST NOT be used to resolve current states.

---

## 7. Future Step07 public-source whitelist

Allowed sources:

1. all Step06-observed URLs in the classified 440-row file whose canonical
   host resolves to one of the 32 authority rows;
2. public links/breadcrumbs/navigation reachable inside the authority row's
   scope policy;
3. public robots/sitemap files and sitemap indexes on the exact authorized
   host, limited to the allowed topical/path scope;
4. public sequential pagination necessary to enumerate an eligible collection;
5. in-scope redirect targets on the same authorized canonical host.

Prohibited sources/actions:

- arbitrary external competitor lists;
- domains present only in the 165-row recurrence table;
- external site-search/provider results used to add competitors;
- authentication/login/private areas;
- CAPTCHA/robots/anti-bot bypass;
- sibling domain/subdomain expansion;
- Wordstat, Yandex Search, AI Search or GenSearch acquisition;
- historical superseded Step06 collectN execution;
- actual Step08 work.

---

## 8. Future output contract

Machine-readable authority:

`JOB_ROOT/STEP_07_OUTPUT_SCHEMA_CONTRACT.json`

Required future Step07 outputs in `JOB_ROOT/`:

| Filename | Primary key | Expected count |
|---|---|---|
| `COMPETITOR_GAP_CANDIDATES.csv` | `candidate_id` | Derived unique candidate identities; may be zero but must reconcile |
| `STEP07_COMPETITOR_COVERAGE_LEDGER.csv` | `competitor_authority_id` | Exactly 32 under this frozen authority; if registry drifts, re-prepare first |
| `STEP07_SOURCE_URL_LEDGER.csv` | `source_url_id`; unique (`competitor_authority_id`,`source_url_canonical`) | Derived complete discovered URL universe |
| `STEP07_CANDIDATE_PROVENANCE_LEDGER.csv` | `provenance_id` | At least one provenance row per candidate; all duplicate occurrences retained |
| `STEP07_EXECUTION_QA.md` | n/a | Exactly one execution QA report |

No production rows were fabricated during preparation.

---

## 9. Deterministic stopping condition

For every authority ID:

```text
frontier exhausted inside frozen scope
AND every discovered URL has exactly one terminal status
AND discovered count reconciles to inspected + excluded + inaccessible
    + redirected-terminal + unresolved
AND every candidate occurrence has provenance
AND every candidate is reconciled against accepted upstream layers
```

If one execution window is insufficient, process deterministic complete chunks
and keep Step07 `INCOMPLETE` until all chunks close. There is no page-count or
top-N convenience stop.

---

## 10. Fresh methodology authority

`JOB_ROOT/STEP_07_PREPARATION_EXTERNAL_METHODOLOGY_AUDIT.md`

The audit records primary/authoritative URL discovery, canonicalization,
robots, sitemap, URI, Unicode and provenance sources plus one industry gap
concept source. It adopts, modifies or rejects each point relative to KW-002.

---

## 11. Handoff acceptance conditions

Future Step07 Work must refuse execution if any is false:

```text
LIVE_REMOTE_FETCHED = true
BASE_DRIFT_RECONCILED = true
AUTHORIZED_COMPETITOR_FILE_ROWS = 32
AUTHORIZED_COMPETITOR_IDS_UNIQUE = true
AUTHORIZED_CANONICAL_SITES_UNIQUE = true
SOURCE_REGISTRY_HASH_MATCH = true
ALL_CANONICAL_INPUTS_PRESENT = true
ALL_CANONICAL_INPUT_HASHES_MATCH_OR_DRIFT_RECONCILED = true
OUTPUT_SCHEMA_JSON_VALID = true
NO_PROHIBITED_PROVIDER_CALL_AUTHORIZED = true
```

---

## 12. Preparation-only status

```text
STEP07_PREPARATION_WORK = COMPLETE_LOCALLY
STEP07_PREPARATION_QA = PASS_LOCALLY
OWNER_UPLOAD_COMPLETE = false
REMOTE_READBACK_PASS = false
MAIN_CHAT_ACCEPTANCE = PENDING
STEP07 = NOT_STARTED
```
