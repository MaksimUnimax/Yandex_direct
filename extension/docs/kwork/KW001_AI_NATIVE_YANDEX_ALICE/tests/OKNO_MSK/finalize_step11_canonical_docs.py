from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
KWROOT = ROOT.parent.parent
RULES_INDEX = KWROOT / "STEP_RULES_INDEX.md"
LESSONS = KWROOT / "STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md"
JOB_FLOW = ROOT / "JOB_FLOW.md"
JOB_MANIFEST = ROOT / "JOB_MANIFEST.md"
BUILDER = ROOT / "step11_correct_page_ownership.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


# 1. Permanently fix the report-template defect caught by GitHub readback.
builder = BUILDER.read_text(encoding="utf-8")
needle = '    OUT_REPORT.write_text(report, encoding="utf-8")\n'
replacement = (
    '    report = report.replace("{len(search_required)}", str(len(search_required)))\n'
    '    if "{len(" in report:\n'
    '        raise RuntimeError("unrendered dynamic placeholder remains in Step11 report")\n'
    '    OUT_REPORT.write_text(report, encoding="utf-8")\n'
)
if replacement not in builder:
    builder = replace_once(builder, needle, replacement, "builder report-template patch")
BUILDER.write_text(builder, encoding="utf-8")


# 2. Register the owner-approved corrected reusable Step-11 method.
idx = RULES_INDEX.read_text(encoding="utf-8")
old_row = "| Step 11 | Page ownership mapping | **UNVALIDATED** | Must define evidence required to map a cluster/task to an existing URL and when no current page is suitable. |"
new_row = "| **Step 11** | **Page ownership / keyword-to-page mapping** | **APPROVED / ACTIVE AFTER EXTERNAL METHOD AUDIT + PHRASE-LEVEL CORRECTION** | **`STEP_11_PAGE_OWNERSHIP_METHOD.md`** — cluster→owner is necessary but not sufficient; inspect member phrases, persist every Bridge/Codex acquisition immediately to GitHub with readback before the next interaction, distinguish target URL from proven Yandex relevant URL, and materialize/QA every active phrase→effective cluster→target URL/state row. |"
if new_row not in idx:
    idx = replace_once(idx, old_row, new_row, "Step11 rules-index row")
RULES_INDEX.write_text(idx, encoding="utf-8")


# 3. Add the causal Step-11 lesson to the permanent lessons ledger.
lessons = LESSONS.read_text(encoding="utf-8")
lesson_marker = "# Step 11 — page ownership / phrase-to-page mapping permanent lesson"
if lesson_marker not in lessons:
    lesson = r'''# Step 11 — page ownership / phrase-to-page mapping permanent lesson

Status: **APPROVED / ACTIVE AFTER EXTERNAL METHOD AUDIT + OWNER-INSTRUCTED CORRECTION**.

Canonical detailed method:

```text
STEP_11_PAGE_OWNERSHIP_METHOD.md
```

## What went wrong in the first OKNO-MSK run

### Known error 1 — Bridge/Codex evidence was not persisted immediately after every acquisition interaction

Wrong action:

Evidence returned by Yandex Marketing Bridge and Codex/site-reading passes was allowed to remain temporarily in conversational/tool state before the complete useful result had been written to the canonical GitHub workspace and read back.

Consequence:

The run came close to losing already acquired evidence. A later context, browser, tool or extension interruption could have destroyed work that had already consumed provider requests and analyst time. Replaying a paid or stateful acquisition later may cost money and may not reproduce the same result exactly.

Root cause:

The older generic rule `REQUEST_SUCCEEDED != PROJECT_RESULT_COMPLETE` described the distinction but did not operationally block the **next** acquisition interaction until durable persistence was verified.

Why the previous method was insufficient:

A provider status, HTTP 200, successful Codex pass, summary in chat, or visible tool result proves only transient execution. It does not prove that the project can recover that evidence later.

Corrected method:

```text
BRIDGE_OR_CODEX_INTERACTION_COMPLETES
-> COMPLETE_REQUIRED_RESULT_AVAILABLE
-> IMMEDIATE_WRITE_TO_CANONICAL_GITHUB_JOB_WORKSPACE
-> GITHUB_READBACK / PARSE / COMPLETENESS CHECK
-> ONLY THEN NEXT ACQUISITION INTERACTION
```

This applies to Bridge provider calls, Bridge batch chunks, Codex URL/page acquisition passes and any equivalent evidence-producing interaction.

Non-repeat control:

```text
BRIDGE_OR_CODEX_RESULT_IN_CHAT != DURABLE_PROJECT_EVIDENCE
NEXT_ACQUISITION_BLOCKED_UNTIL_GITHUB_PERSISTENCE_AND_READBACK = true
```

### Known error 2 — cluster ownership was accepted without materializing the final phrase→page map

Wrong action:

The first pass stopped after producing 59 `cluster → owner/state` rows. The Step-10 phrase ledger made it theoretically possible to derive the page for each phrase, but the actual `phrase → cluster → target URL/state` result was not materialized as a final Step-11 artifact.

Consequence:

The deliverable was harder to audit and use, and more importantly the missing join hid heterogeneous upstream clusters. A cluster label could look reasonable while its actual member phrases did not share one terminal task.

Root cause:

The method treated cluster-level ownership as equivalent to completed keyword mapping.

Why the previous method was insufficient:

Cluster-level reasoning is the right way to avoid one-page-per-keyword fragmentation, but it is only an intermediate abstraction. The final SEO map still has to expose every active phrase against its effective cluster and target/no-target state.

Corrected method:

```text
CLUSTER OWNERSHIP DECISION
-> MATERIALIZE EVERY ACTIVE PHRASE
-> PHRASE + ORIGINAL CLUSTER + EFFECTIVE CLUSTER + TARGET URL/STATE
-> FULL ACCOUNTING + DUPLICATE + MISSING-OWNER QA
```

Hard rule:

```text
CLUSTER_OWNERSHIP_COMPLETE != PHRASE_PAGE_MAPPING_COMPLETE
```

### Known error 3 — a representative query or cluster label can hide a bad upstream cluster

Observed consequence in OKNO-MSK:

- `GENERAL_GLAZING_SERVICE` was labelled generic, but all seven member phrases were actually aluminium, panoramic, French-window or outside-brand tasks;
- `GLAZING_SELECTION_INFO` was described as generic/non-balcony, but its actual member phrases were veranda-specific;
- replacement, reviews, balcony-info, broad technical-info and comparison clusters contained materially different terminal tasks.

Root cause:

Step 11 inspected representative query behaviour and cluster summaries without making full member-phrase coherence a blocking ownership check.

Corrected method:

Every cluster must remain inspectable at phrase level. `MEDIUM`/`LOW` ownership and broad/heterogeneous clusters require all-member review. If a cluster is wrong, preserve the historical upstream artifact and apply an explicit correction overlay/split or unresolved handoff; do not hide the defect by assigning a convenient URL.

Hard rule:

```text
REPRESENTATIVE_QUERY_BEHAVIOR != PERMISSION_TO_REWRITE_CLUSTER_BOUNDARY
BAD_UPSTREAM_CLUSTER != VALID_PAGE_OWNER_PROBLEM
```

### Known error 4 — target URL terminology can be overstated

A page selected by the analyst as the intended SEO owner is not automatically the URL that Yandex currently ranks/associates with the query.

Corrected terminology:

```text
TARGET_URL = intended SEO owner selected from current page/task evidence
YANDEX_RELEVANT_URL = directly observed Yandex query↔URL/ranking evidence
TARGET_URL != PROVEN_YANDEX_RELEVANT_URL
```

This matters especially when the target domain is absent from observed TOP results or authorized Webmaster query↔URL data is unavailable.

## Why this method is supported externally

Current external method audit used:

- Semrush — keyword mapping: https://www.semrush.com/blog/keyword-mapping/
- Ahrefs — keyword mapping: https://ahrefs.com/blog/keyword-mapping/
- Ahrefs — keyword clustering: https://ahrefs.com/blog/keyword-clustering/
- Rush Analytics — relevant URLs for clusters: https://www.rush-analytics.ru/faq/klasterizaciya/opredelenie-relevantnyh-url-dlya-klasterov
- Topvisor — target URL terminology: https://topvisor.com/ru/support/rankings/target-url/
- Yandex Webmaster — page targeting and query↔URL analytics: https://yandex.ru/support/webmaster/ru/recommendations/targeting and https://yandex.ru/support/webmaster/ru/service/queries-export

The sources support cluster→page mapping, intent/page fit and explicit target-URL mapping. The exact internal statuses, correction-overlay schema and GitHub durability gate are project/owner controls created from the failure mode observed in this work.

## Required Step-11 completion gate

Step 11 cannot pass until:

```text
ALL_ACTIVE_PHRASES_MATERIALIZED = true
SILENT_ACTIVE_DROPS = 0
DUPLICATE_PHRASE_MAP_ROWS = 0
ASSIGNED_WITHOUT_EFFECTIVE_CLUSTER = 0
ASSIGNED_WITHOUT_OWNERSHIP_ROW = 0
OWNER_EXISTING_WITH_BLANK_TARGET_URL = 0
SEARCH_REQUIRED_WITH_TARGET_URL = 0
MEDIUM_LOW_OWNERSHIP_REAUDIT = 100%
KNOWN_MIXED_CLUSTERS_LEFT_UNCORRECTED = 0
BRIDGE_CODEX_ACQUISITION_PERSISTENCE_GATE = PASS
FINAL_GITHUB_READBACK = PASS
PREMATURE_STEP12_ACTIONS = 0
PREMATURE_STEP13_CANNIBALIZATION_VERDICTS = 0
```

The exact OKNO-MSK phrases, URLs and correction rows remain job-specific Layer-C evidence. The causal method above is reusable Layer-B methodology.

---

'''
    anchor = "# Permanent-update policy"
    if anchor not in lessons:
        raise RuntimeError("Permanent-update policy anchor missing in lessons ledger")
    lessons = lessons.replace(anchor, lesson + anchor, 1)
LESSONS.write_text(lessons, encoding="utf-8")


# 4. Replace stale Step-11 job-flow state with the corrected authoritative state.
flow = JOB_FLOW.read_text(encoding="utf-8")
start = flow.index("## Completed step — Step 11 page ownership")
end = flow.index("## Full roadmap status", start)
new_step11 = '''## Completed step — Step 11 page ownership / phrase-to-page mapping

Status: **✅ COMPLETE AFTER EXTERNAL METHOD AUDIT + PHRASE-LEVEL CORRECTION**

Permanent methodology status:

```text
STEP_11_PERMANENT_METHOD = APPROVED / ACTIVE AFTER EXTERNAL METHOD AUDIT + OWNER-INSTRUCTED CORRECTION
```

Canonical method authority:

```text
../../STEP_11_PAGE_OWNERSHIP_METHOD.md
```

Current job authorities:

```text
STEP_11_POST_AUDIT_CORRECTIONS.tsv
STEP_11_PHRASE_PAGE_MAP.tsv
STEP_11_EFFECTIVE_CLUSTER_SUMMARY.tsv
STEP_11_PAGE_OWNERSHIP_CORRECTED.tsv
STEP_11_WEAK_OWNERSHIP_REAUDIT.md
STEP_11_REPORT.md
STEP_11_QA.json
```

### Corrected Step-11 goal

For the complete active semantic set, determine a truthful intended existing-page owner (or an explicit no-owner/outside/unresolved state) at effective user-task-cluster level **and materialize the result for every active phrase**.

Step 11 still does not make Step-12 structural `KEEP / EXPAND / SPLIT / MERGE / CREATE` actions and does not make Step-13 cannibalization verdicts.

### Historical acquisition truth preserved

```text
ORIGINAL_FINAL_STEP10_CLUSTERS = 59
CURRENT_PAGE_PROFILE_LEDGER_ROWS = 23
FRESH_SEARCH_BATCH_QUERIES = 68
FRESH_SEARCH_BATCH_SUCCEEDED = 68
FRESH_SEARCH_BATCH_COST_RUB = 33.184
FRESH_SEARCH_CANARY_REQUESTS = 1
FRESH_SEARCH_CANARY_COST_RUB = 0.488
FRESH_SEARCH_TOTAL_REQUESTS = 69
FRESH_SEARCH_TOTAL_COST_RUB = 33.672
AUTHORIZED_WEBMASTER_PROPERTY_AVAILABLE = false
NEW_BRIDGE_REQUESTS_DURING_CORRECTION = 0
NEW_BRIDGE_COST_RUB_DURING_CORRECTION = 0.0
```

The live Bridge reported version `0.1.1` during the original Step-11 Search execution. That historical runtime provenance remains unchanged.

Observed target-domain TOP10 hits in the original 68-query batch were `0`. Therefore corrected `TARGET_URL` means intended SEO owner and is not represented as a proven Yandex relevant/ranking URL.

The historical persistence limitation remains explicit: a single consolidated full 680-ranked-row Step-11 TSV was not produced. No paid replay was performed solely to reconstruct bookkeeping.

### External audit corrections

The original cluster→owner approach was retained, but two missing controls became permanent:

```text
BRIDGE/CODEX RESULT
-> IMMEDIATE GITHUB SAVE
-> GITHUB READBACK + COMPLETENESS QA
-> ONLY THEN NEXT ACQUISITION INTERACTION

CLUSTER OWNERSHIP
-> FULL PHRASE-LEVEL MATERIALIZATION
-> FULL MEMBER-PHRASE COHERENCE QA
```

Phrase-level review exposed upstream cluster defects. Historical Step-10 artifacts remain unchanged; downstream truth uses `STEP_11_POST_AUDIT_CORRECTIONS.tsv` as an explicit correction overlay.

### Corrected effective accounting

```text
SOURCE_ACTIVE_ROWS = 2332
SOURCE_ASSIGNED_ROWS = 2319
SOURCE_SEARCH_REQUIRED_ROWS = 13
POST_STEP11_CORRECTION_ROWS = 121
EFFECTIVE_ASSIGNED_ROWS = 2313
EFFECTIVE_SEARCH_REQUIRED_ROWS = 19
PHRASE_PAGE_MAP_ROWS = 2332
EFFECTIVE_ACTIVE_CLUSTERS = 75
SILENT_ACTIVE_DROPS = 0
DUPLICATE_PHRASE_MAP_ROWS = 0
```

Corrected ownership states across effective assigned clusters:

```text
OWNER_EXISTING = 44
NO_SUITABLE_EXISTING_PAGE = 25
OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP = 6
OWNER_UNRESOLVED_EVIDENCE_REQUIRED = 0
```

Six historical Step-10 clusters became zero-member after explicit phrase-level reclassification:

```text
BALCONY_GLAZING_INFO
GENERAL_GLAZING_SERVICE
GLAZING_SELECTION_INFO
WINDOW_COMPARISON_INFO
WINDOW_PRODUCT_TECH_INFO
WINDOW_REVIEWS_INFO
```

Their disappearance is not a silent drop: every one of their active member phrases remains in the 2332-row phrase map under a corrected effective cluster or explicit `SEARCH_REQUIRED` state.

### Search-required handoff

```text
ORIGINAL_STEP10_SEARCH_REQUIRED = 13
ADDED_BY_STEP11_COHERENCE_AUDIT = 6
EFFECTIVE_SEARCH_REQUIRED = 19
SEARCH_REQUIRED_WITH_TARGET_URL = 0
```

The six added rows are ambiguous bare DIY/instruction phrases that could not truthfully remain in the repair-DIY cluster without stronger evidence. They must be resolved before any structural action is assigned to them.

### Step-11 PASS gate result

```text
ACTIVE_ROWS_ACCOUNTED = 2332/2332
SILENT_ACTIVE_DROPS = 0
DUPLICATE_PHRASE_MAP_ROWS = 0
ASSIGNED_WITHOUT_EFFECTIVE_CLUSTER = 0
SEARCH_REQUIRED_WITH_TARGET_URL = 0
OWNER_EXISTING_WITH_BLANK_TARGET_URL = 0
NON_OWNER_STATE_WITH_TARGET_URL = 0
ORIGINAL_MEDIUM_LOW_OWNERSHIP_CLUSTERS_REAUDITED = 11/11
BRIDGE_PAID_REPLAY_FOR_BOOKKEEPING = 0
NEW_BRIDGE_REQUESTS_DURING_CORRECTION = 0
FULL_PHRASE_LEVEL_MAP_MATERIALIZED = true
CLUSTER_COHERENCE_GATE_ADDED = true
BRIDGE_CODEX_IMMEDIATE_PERSISTENCE_RULE_ADDED = true
PREMATURE_STEP12_STRUCTURAL_ACTIONS = 0
PREMATURE_STEP13_CANNIBALIZATION_VERDICTS = 0
STEP11_COMPLETE = true
NEXT_STEP_ALLOWED = true
```

---

'''
flow = flow[:start] + new_step11 + flow[end:]
flow = flow.replace(
    "| **11. Page ownership** | **Map clusters to best existing URLs** | **✅ COMPLETE / PASS WITH EXPLICIT UNRESOLVED EVIDENCE ROUTE** |",
    "| **11. Page ownership** | **Map effective clusters and every active phrase to intended existing URL/state** | **✅ COMPLETE AFTER EXTERNAL METHOD AUDIT + PHRASE-LEVEL CORRECTION** |",
)
marker_replacements = {
    "KW001_OKNO_MSK_STEP11_OWNER_EXISTING = 34": "KW001_OKNO_MSK_STEP11_OWNER_EXISTING = 44",
    "KW001_OKNO_MSK_STEP11_NO_SUITABLE_EXISTING_PAGE = 18": "KW001_OKNO_MSK_STEP11_NO_SUITABLE_EXISTING_PAGE = 25",
    "KW001_OKNO_MSK_STEP11_OWNER_UNRESOLVED_EVIDENCE_REQUIRED = 1": "KW001_OKNO_MSK_STEP11_OWNER_UNRESOLVED_EVIDENCE_REQUIRED = 0",
    "KW001_OKNO_MSK_STEP11_SEARCH_REQUIRED_ACCOUNTED = 13": "KW001_OKNO_MSK_STEP11_SEARCH_REQUIRED_ACCOUNTED = 19",
    "KW001_OKNO_MSK_STEP11_SEARCH_REQUIRED_SEMANTIC_REVIEW = 3": "KW001_OKNO_MSK_STEP11_SEARCH_REQUIRED_SEMANTIC_REVIEW = 19",
}
for old, new in marker_replacements.items():
    if old in flow:
        flow = flow.replace(old, new, 1)
extra_markers = '''
KW001_OKNO_MSK_STEP11_METHOD_APPROVED_AFTER_EXTERNAL_AUDIT = true
KW001_OKNO_MSK_STEP11_PHRASE_PAGE_MAP_ROWS = 2332
KW001_OKNO_MSK_STEP11_POST_AUDIT_CORRECTION_ROWS = 121
KW001_OKNO_MSK_STEP11_EFFECTIVE_ASSIGNED = 2313
KW001_OKNO_MSK_STEP11_EFFECTIVE_SEARCH_REQUIRED = 19
KW001_OKNO_MSK_STEP11_EFFECTIVE_ACTIVE_CLUSTERS = 75
KW001_OKNO_MSK_STEP11_BRIDGE_CODEX_IMMEDIATE_PERSISTENCE_RULE_ACTIVE = true'''
marker_anchor = "KW001_OKNO_MSK_STEP11_COMPLETE = true"
if extra_markers.strip() not in flow:
    flow = replace_once(flow, marker_anchor, extra_markers + "\n" + marker_anchor, "job-flow Step11 marker anchor")
JOB_FLOW.write_text(flow, encoding="utf-8")


# 5. Reconcile the stale job manifest without deleting useful historical evidence.
manifest = JOB_MANIFEST.read_text(encoding="utf-8")
manifest = manifest.replace("Date updated: 2026-08-29", "Date updated: 2026-08-31", 1)
manifest = manifest.replace(
    "current_major_step = STEP_10_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW",
    "current_major_step = STEP_11_COMPLETE_AFTER_EXTERNAL_METHOD_AUDIT_AND_PHRASE_LEVEL_CORRECTION",
    1,
)
manifest = manifest.replace(
    "next_major_step = STEP_10_USER_TASK_SERP_CLUSTERING_EXECUTION_AFTER_METHOD_GATE",
    "next_major_step = STEP_12_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW",
    1,
)
# Add current Step10/11 authorities inside the explicit Current job authorities fence.
authority_add = """STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv
STEP_10_FRESH_R1_CLUSTER_SUMMARY_FINAL.tsv
../../STEP_11_PAGE_OWNERSHIP_METHOD.md
STEP_11_POST_AUDIT_CORRECTIONS.tsv
STEP_11_PHRASE_PAGE_MAP.tsv
STEP_11_EFFECTIVE_CLUSTER_SUMMARY.tsv
STEP_11_PAGE_OWNERSHIP_CORRECTED.tsv
STEP_11_WEAK_OWNERSHIP_REAUDIT.md
STEP_11_REPORT.md
STEP_11_QA.json
"""
if "STEP_11_PHRASE_PAGE_MAP.tsv" not in manifest:
    auth_heading = manifest.index("Current job authorities:")
    auth_fence_start = manifest.index("```text", auth_heading)
    auth_fence_end = manifest.index("```", auth_fence_start + len("```text"))
    manifest = manifest[:auth_fence_end] + authority_add + manifest[auth_fence_end:]

current_start = manifest.index("## Current major step — Step 10 user-task / SERP clustering")
remaining_start = manifest.index("## Remaining roadmap", current_start)
current_block = '''## Current accepted major step — Step 11 page ownership / phrase-to-page mapping

Status: **COMPLETE AFTER EXTERNAL METHOD AUDIT + PHRASE-LEVEL CORRECTION**

```text
STEP_10_HISTORICAL_FINAL_ACTIVE_ROWS = 2332
STEP_10_HISTORICAL_ASSIGNED = 2319
STEP_10_HISTORICAL_SEARCH_REQUIRED = 13
STEP_10_HISTORICAL_ACTIVE_CLUSTERS = 59
STEP_11_POST_AUDIT_CORRECTION_ROWS = 121
STEP_11_EFFECTIVE_ASSIGNED = 2313
STEP_11_EFFECTIVE_SEARCH_REQUIRED = 19
STEP_11_PHRASE_PAGE_MAP_ROWS = 2332
STEP_11_EFFECTIVE_ACTIVE_CLUSTERS = 75
STEP_11_OWNER_EXISTING = 44
STEP_11_NO_SUITABLE_EXISTING_PAGE = 25
STEP_11_OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP = 6
STEP_11_OWNER_UNRESOLVED_EVIDENCE_REQUIRED = 0
STEP_11_NEW_BRIDGE_REQUESTS_DURING_CORRECTION = 0
STEP_11_NEW_BRIDGE_COST_RUB_DURING_CORRECTION = 0.0
STEP_11_COMPLETE = true
```

The historical Step-10 artifacts remain immutable evidence of what was originally accepted. `STEP_11_POST_AUDIT_CORRECTIONS.tsv` is the authoritative downstream correction overlay discovered by phrase-level ownership QA. `STEP_11_PHRASE_PAGE_MAP.tsv` is the current canonical active keyword→page/state map.

The corrected Step-11 method permanently requires every Bridge/Codex acquisition result to be saved to GitHub and read back before the next acquisition interaction. It also makes the complete phrase-level map a blocking completion requirement.

Step 12 has **not** started. Its methodology remains separately gated by `STEP_RULES_INDEX.md` and the normal pre-step review process.

'''
manifest = manifest[:current_start] + current_block + manifest[remaining_start:]
manifest = manifest.replace(
    "Step 10 — user-task / SERP clustering\nStep 11 — page ownership\nStep 12 — structural actions",
    "Step 12 — structural actions",
    1,
)
manifest = manifest.replace("USER_TASK_SERP_CLUSTERING_COMPLETE = false", "USER_TASK_SERP_CLUSTERING_COMPLETE = true", 1)
manifest = manifest.replace("PAGE_OWNERSHIP_COMPLETE = false", "PAGE_OWNERSHIP_COMPLETE = true", 1)
markers_start = manifest.index("## Markers")
close_start = manifest.index("```", markers_start)
close_end = manifest.index("```", close_start + 3) + 3
new_markers = '''## Markers

```text
KW001_OKNO_MSK_STEP08_COMPLETE_AFTER_METHOD_CORRECTION = true
KW001_OKNO_MSK_SEARCH_STAGE_INPUT_FROZEN = true
KW001_OKNO_MSK_STEP09_COMPLETE = true
KW001_OKNO_MSK_STEP10_COMPLETE = true
KW001_OKNO_MSK_STEP10_HISTORICAL_ACTIVE_ROWS = 2332
KW001_OKNO_MSK_STEP10_HISTORICAL_FINAL_ASSIGNED = 2319
KW001_OKNO_MSK_STEP10_HISTORICAL_FINAL_SEARCH_REQUIRED = 13
KW001_OKNO_MSK_STEP10_HISTORICAL_ACTIVE_CLUSTERS = 59
KW001_OKNO_MSK_STEP11_METHOD_APPROVED_AFTER_EXTERNAL_AUDIT = true
KW001_OKNO_MSK_STEP11_POST_AUDIT_CORRECTION_ROWS = 121
KW001_OKNO_MSK_STEP11_EFFECTIVE_ASSIGNED = 2313
KW001_OKNO_MSK_STEP11_EFFECTIVE_SEARCH_REQUIRED = 19
KW001_OKNO_MSK_STEP11_PHRASE_PAGE_MAP_ROWS = 2332
KW001_OKNO_MSK_STEP11_EFFECTIVE_ACTIVE_CLUSTERS = 75
KW001_OKNO_MSK_STEP11_OWNER_EXISTING = 44
KW001_OKNO_MSK_STEP11_NO_SUITABLE_EXISTING_PAGE = 25
KW001_OKNO_MSK_STEP11_OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP = 6
KW001_OKNO_MSK_STEP11_OWNER_UNRESOLVED_EVIDENCE_REQUIRED = 0
KW001_OKNO_MSK_STEP11_NEW_BRIDGE_REQUESTS_DURING_CORRECTION = 0
KW001_OKNO_MSK_STEP11_COMPLETE = true
KW001_OKNO_MSK_NEXT_STEP = STEP_12_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW
KW001_OKNO_MSK_SAFE_TO_DELETE = false
```'''
manifest = manifest[:markers_start] + new_markers + manifest[close_end:]
JOB_MANIFEST.write_text(manifest, encoding="utf-8")


# 6. Remove accidental/stale correction scaffolding; retain the meaningful session note and plan.
for name in [
    ".step11_audit_write_probe.tmp",
    "STEP_11_CORRECTION_WORKLOG.tmp",
    "STEP_11_CORRECTION_README.md",
    "STEP_11_CORRECTION_STATUS.md",
    "STEP_11_CORRECTION_CHECKPOINT.json",
    "STEP_11_CORRECTION_EXECUTION_LOCK.md",
    "STEP_11_CORRECTION_META.json",
    "STEP_11_CORRECTION_NOTE_2.md",
    "STEP_11_CORRECTION_AUDIT_MARKER.md",
    "STEP_11_CORRECTION_FINALIZATION_PENDING.md",
    "STEP_11_CORRECTION_DO_NOT_SKIP.md",
    "STEP_11_CORRECTION_TRIGGER.md",
]:
    p = ROOT / name
    if p.exists():
        p.unlink()

print("STEP11_CANONICAL_FINALIZATION_PATCHED")
