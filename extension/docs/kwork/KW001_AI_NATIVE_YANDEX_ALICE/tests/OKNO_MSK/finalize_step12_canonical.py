import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent

CANDIDATE_QA = ROOT / 'STEP_12_QA_CANDIDATE.json'
CHECKS = ROOT / 'STEP_12_QA_CHECKS.tsv'
FINDINGS = ROOT / 'STEP_12_QA_FINDINGS.tsv'
REVIEW_RESULTS = ROOT / 'STEP_12_QA_REVIEW_RESULTS.tsv'
SM_RESULTS = ROOT / 'STEP_12_SPLIT_MERGE_REGRESSION_RESULTS.tsv'
ACTIONS_V1 = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv'
ACTIONS_V2 = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv'
FINAL_MAP = ROOT / 'STEP_12_PHRASE_ACTION_MAP_FINAL.tsv'
PAIRS = ROOT / 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv'
HIER = ROOT / 'STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv'
NEW_EVIDENCE = ROOT / 'STEP_12_NEW_PAGE_EVIDENCE_V2.tsv'
GEN_QA = ROOT / 'STEP_12_D12_11_D12_06_GENERATOR_QA.json'
PAIR_QA = ROOT / 'STEP_12_D12_11_D12_06_QA.json'
CONF_QA = ROOT / 'STEP_12_CONFIDENCE_QA_V1.json'
D14 = ROOT / 'STEP_12_D12_14_TARGET_RESOLUTIONS.tsv'
LEDGER = ROOT / 'STEP_12_CORRECTION_DEFECT_LEDGER.tsv'
STATE = ROOT / 'STEP_12_CORRECTION_CURRENT_STATE.json'
QA_FINAL = ROOT / 'STEP_12_QA.json'
REPORT = ROOT / 'STEP_12_REPORT.md'
METHOD = BASE / 'STEP_12_STRUCTURAL_ACTION_METHOD.md'
RULES = BASE / 'STEP_RULES_INDEX.md'
FLOW = ROOT / 'JOB_FLOW.md'
MANIFEST = ROOT / 'JOB_MANIFEST.md'
ACCEPTANCE = ROOT / 'STEP_12_FINAL_ACCEPTANCE_2026-08-31.md'


def read_tsv(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write_tsv(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected one exact anchor, found {count}')
    return text.replace(old, new, 1)


def regex_replace_once(text, pattern, repl, label, flags=0):
    new_text, count = re.subn(pattern, repl, text, count=1, flags=flags)
    if count != 1:
        raise RuntimeError(f'{label}: expected one regex anchor, found {count}')
    return new_text


# ---------------------------------------------------------------------------
# 1. Revalidate the persisted independent QA and defect-specific evidence.
# ---------------------------------------------------------------------------
q = read_json(CANDIDATE_QA)
checks = read_tsv(CHECKS)
findings = read_tsv(FINDINGS)
reviews = read_tsv(REVIEW_RESULTS)
sm = read_tsv(SM_RESULTS)
a1 = read_tsv(ACTIONS_V1)
a2 = read_tsv(ACTIONS_V2)
final_map = read_tsv(FINAL_MAP)
pairs = read_tsv(PAIRS)
hier = read_tsv(HIER)
new_evidence = read_tsv(NEW_EVIDENCE)
g = read_json(GEN_QA)
pq = read_json(PAIR_QA)
cq = read_json(CONF_QA)
d14 = read_tsv(D14)

assert q['status'] == 'D12_05_CANDIDATE_PASS'
assert q['checks_total'] == 46
assert q['checks_failed'] == 0
assert q['failed_check_ids'] == []
assert q['findings_rows'] == 0 and findings == []
assert len(checks) == 46 and all(r['pass'] == 'true' for r in checks)
assert all(r['evidence_origin'] in {'COMPUTED_FROM_DATA','VERIFIED_FROM_PROVENANCE','MANUAL_REVIEW_LEDGER'} for r in checks)
assert all(r['source_artifacts'].strip() and r['computation_or_review_method'].strip() for r in checks)
assert q['source_phrase_rows'] == 2332
assert q['assignment_rows'] == 2332
assert q['final_phrase_action_rows'] == 2332 == len(final_map)
assert q['assigned_rows'] == 2313
assert q['search_required_rows'] == 19
assert q['structural_units'] == 160
assert q['structural_action_rows'] == 160 == len(a2)
assert q['manual_review_cases'] == 10 == len(reviews)
assert q['manual_review_failures'] == 0 and all(r['pass'] == 'true' for r in reviews)
assert q['split_merge_regression_cases'] == 4 == len(sm)
assert q['split_merge_regression_failures'] == 0 and all(r['pass'] == 'true' for r in sm)
assert q['unsupported_split_rows'] == 0
assert q['unsupported_merge_rows'] == 0
assert q['qa_self_asserted_pass_fields'] == 0
assert q['actions_requiring_target_but_blank'] == 0
assert q['stale_materialized_hierarchy_reason_rows'] == 0
assert q['step13_artifact_files'] == []
assert q['step13_executed'] is False
assert len(a1) == 160
assert len(pairs) == q['candidate_pair_rows']
assert len(hier) == q['hierarchy_candidate_pages'] == 5
assert len(new_evidence) == 5
assert len(d14) == 4

# D12-14 / D12-15 source-specific closure proof.
assert cq['d12_14_resolution_rows'] == 4
assert cq['d12_14_resolution_mismatch_rows'] == 0
assert cq['d12_14_implementable_blank_targets'] == 0
assert cq['d12_14_deferred_rows'] == 1
assert g['d12_15_reason_regenerated_rows'] == 160
assert g['d12_15_stale_materialized_hierarchy_reason_rows'] == 0
assert pq['stale_materialized_hierarchy_reason_rows'] == 0
assert pq['status'] == 'STEP12_D12_11_D12_06_INDEPENDENT_PASS'
assert pq['missing_pair_keys'] == 0
assert pq['extra_pair_keys'] == 0
assert pq['duplicate_pair_rows'] == 0
assert pq['dependency_high_rows'] == 0
assert pq['dependency_final_maturity_rows'] == 0
assert pq['step13_executed'] is False

# The current pair count is a derived fact, not an acceptance constant.
pair_count = len(pairs)
future_search_pairs = sum(r['later_direct_search_check_needed'] == 'true' for r in pairs)
dependency_units = sum(r['step13_dependency_required'] == 'true' for r in a2)
assert pair_count == pq['actual_pair_rows'] == pq['expected_pair_keys']
assert future_search_pairs == pq['pairs_requiring_direct_step13_search_check']
assert dependency_units == pq['actual_dependency_units'] == pq['expected_dependency_units']

# No later-step execution is allowed during Step-12 finalization.
assert not [p.name for p in ROOT.iterdir() if p.is_file() and p.name.startswith('STEP_13_')]

# ---------------------------------------------------------------------------
# 2. Close the remaining defects only after the independent proof above.
# ---------------------------------------------------------------------------
ledger_rows = read_tsv(LEDGER)
fields = list(ledger_rows[0].keys())
by_defect = {r['defect_id']: r for r in ledger_rows}
assert set(by_defect) == {f'D12-{i:02d}' for i in range(1,16)}
assert by_defect['D12-05']['status'] == 'OPEN'
assert by_defect['D12-14']['status'] == 'OPEN'
assert by_defect['D12-15']['status'] == 'OPEN'
assert all(by_defect[f'D12-{i:02d}']['status'] == 'VERIFIED_FIXED' for i in range(1,14) if i not in {5})

by_defect['D12-05']['status'] = 'VERIFIED_FIXED'
by_defect['D12-05']['correction_artifact'] = 'STEP_12_QA_REVIEW_LEDGER.tsv | STEP_12_SPLIT_MERGE_REGRESSION_CASES.tsv | STEP_12_PHRASE_ACTION_MAP_FINAL.tsv | STEP_12_QA_CHECKS.tsv | STEP_12_QA_REVIEW_RESULTS.tsv | STEP_12_SPLIT_MERGE_REGRESSION_RESULTS.tsv | STEP_12_QA_FINDINGS.tsv | STEP_12_QA_CANDIDATE.json | STEP_12_FINAL_ACCEPTANCE_2026-08-31.md'
by_defect['D12-05']['notes'] += ' | Closed only after durable independent QA recomputed 46/46 checks from persisted source artifacts, findings=0, QA self-asserted fields=0, four SPLIT/MERGE positive/negative controls passed, actual unsupported SPLIT/MERGE=0/0, pair universe was dynamically recomputed rather than fixed to a historical count, and diagnostics were saved/read back before the final PASS gate.'

by_defect['D12-14']['status'] = 'VERIFIED_FIXED'
by_defect['D12-14']['correction_artifact'] = 'STEP_12_D12_14_IMPLEMENTABLE_ACTION_WITHOUT_PRIMARY_TARGET_2026-08-31.md | STEP_12_D12_14_REVIEW_PACKET.tsv | STEP_12_D12_14_REVIEW_SUMMARY.tsv | STEP_12_D12_14_TARGET_RESOLUTIONS.tsv | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv | STEP_12_CONFIDENCE_QA_V1.json | STEP_12_PHRASE_ACTION_MAP_FINAL.tsv | STEP_12_QA_CANDIDATE.json | STEP_12_FINAL_ACCEPTANCE_2026-08-31.md'
by_defect['D12-14']['notes'] += ' | Closed after all four blank-target cases received evidence-reviewed resolutions: door installation -> existing door hub section; PVC operation DIY -> section in proposed DIY repair guide with repair service supporting; other-brand Rehau comparison -> explicit defer/LOW; demolition -> installation-service section. Final independent QA found actions_requiring_target_but_blank=0.'

by_defect['D12-15']['status'] = 'VERIFIED_FIXED'
by_defect['D12-15']['correction_artifact'] = 'STEP_12_D12_15_STALE_HIERARCHY_CONFIDENCE_REASON_2026-08-31.md | STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv | STEP_12_D12_11_D12_06_GENERATOR_QA.json | STEP_12_D12_11_D12_06_QA.json | STEP_12_QA_CANDIDATE.json | STEP_12_FINAL_ACCEPTANCE_2026-08-31.md'
by_defect['D12-15']['notes'] += ' | Closed after all 160 confidence explanations were regenerated from current V2 evidence after hierarchy/dependency overlays and independent QA found stale_materialized_hierarchy_reason_rows=0.'

write_tsv(LEDGER, ledger_rows, fields)
assert all(r['status'] == 'VERIFIED_FIXED' for r in ledger_rows)

state = read_json(STATE)
assert state['open_defects'] == ['D12-14','D12-15','D12-05']
state.update({
    'status': 'STEP12_COMPLETE_AFTER_EXTERNAL_METHOD_AUDIT_FAIL_CLOSED_CORRECTION_AND_INDEPENDENT_QA',
    'step13_blocked': False,
    'step13_executed': False,
    'step13_status': 'NOT_STARTED_NEXT_ALLOWED',
    'open_defects': [],
    'verified_fixed_defects': [f'D12-{i:02d}' for i in range(1,16)],
    'current_correction_item': None,
    'step12_complete': True,
    'next_step_allowed': True,
    'next_major_step': 'STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW',
    'next_action': 'Step 12 is complete. Step 13 is NOT STARTED. If the owner authorizes continuation, first run fresh Step-13 pre-step methodology research/review because Step 13 remains UNVALIDATED in STEP_RULES_INDEX.md.',
})
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# ---------------------------------------------------------------------------
# 3. Replace the historical self-certified QA with canonical independent QA.
# ---------------------------------------------------------------------------
origin_counts = Counter(r['evidence_origin'] for r in checks)
action_counts = Counter(r['structural_action'] for r in a2)
confidence_counts = Counter(r['final_confidence'] for r in a2)
maturity_counts = Counter(r['recommendation_maturity'] for r in a2)
qa_final = dict(q)
qa_final.update({
    'status': 'PASS_AFTER_EXTERNAL_METHOD_AUDIT_FAIL_CLOSED_CORRECTIONS_AND_INDEPENDENT_QA',
    'step12_complete': True,
    'next_step_allowed': True,
    'next_step': 'STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW',
    'step13_status': 'NOT_STARTED_NEXT_ALLOWED',
    'step13_executed': False,
    'step14_executed': False,
    'historical_first_pass_qa_superseded': True,
    'historical_first_pass_qa_status': 'PASS_AFTER_FULL_STRUCTURAL_ACTION_AUDIT_WITHDRAWN_AFTER_EXTERNAL_METHOD_AUDIT',
    'verification_origin': 'INDEPENDENT_RECOMPUTATION_FROM_PERSISTED_SOURCE_ARTIFACTS_PLUS_MANUAL_REVIEW_LEDGER',
    'qa_evidence_origin_counts': dict(sorted(origin_counts.items())),
    'action_counts_by_structural_unit': dict(sorted(action_counts.items())),
    'confidence_counts_by_structural_unit': dict(sorted(confidence_counts.items())),
    'maturity_counts_by_structural_unit': dict(sorted(maturity_counts.items())),
    'candidate_pair_rows_current_derived': pair_count,
    'candidate_pairs_requiring_future_step13_search_check': future_search_pairs,
    'step13_dependency_units': dependency_units,
    'all_defects_verified_fixed': True,
    'defect_count': 15,
    'open_defects': [],
    'new_bridge_requests_during_final_correction': 0,
    'new_bridge_cost_rub_during_final_correction': 0.0,
    'note': 'Step 12 is complete. Current candidate-pair count is derived from the corrected routing graph and is not a universal/hard-coded threshold. Step 13 is only next allowed; it has not been executed.'
})
QA_FINAL.write_text(json.dumps(qa_final, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# ---------------------------------------------------------------------------
# 4. Corrected final report.
# ---------------------------------------------------------------------------
new_page_lines = []
for r in new_evidence:
    page = r['proposed_page']
    maturity = r['candidate_maturity_after_existing_evidence']
    gap = r['search_boundary_gap']
    new_page_lines.append(f"- `{r['candidate_id']}` → `{page}` — evidence maturity `{maturity}`; Search boundary: `{gap}`.")

d14_lines = []
for r in d14:
    target = r['reviewed_primary_page_candidate'] or 'NO TARGET / DEFERRED'
    d14_lines.append(f"- `{r['structural_unit_id']}` → `{r['reviewed_structural_action']}` → `{target}`. {r['resolution_reason']}")

report = f'''# Step 12 — Structural actions report

Date: 2026-08-31
Status: **PASS AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA**

## Executive result

Step 12 is complete. The historical first-pass `PASS_AFTER_FULL_STRUCTURAL_ACTION_AUDIT` is preserved only as superseded provenance and is **not** the current acceptance authority.

The corrected final authority is based on explicit structural units, phrase-level materialization, evidence-derived confidence/maturity, implementable hierarchy, a deterministic Step-13 candidate-pair handoff, and independent QA that is computed from persisted source artifacts rather than self-asserted constants.

Step 13 is **NOT STARTED**. It is only the next allowed major step and still requires its own pre-step methodology research/review before execution.

## Final accounting

```text
SOURCE_ACTIVE_PHRASES = 2332
FINAL_PHRASE_ACTION_MAP_ROWS = 2332
ASSIGNED_TO_STRUCTURAL_UNITS = 2313
SEARCH_REQUIRED / DEFER_UNRESOLVED = 19
FINAL_STRUCTURAL_UNITS = 160
FINAL_STRUCTURAL_ACTION_ROWS = 160
UNIQUE_PROPOSED_NEW_PAGES = 5
HIERARCHY_CANDIDATE_PAGES_MATERIALIZED = 5/5
CURRENT_DERIVED_STEP13_CANDIDATE_PAIRS = {pair_count}
PAIRS_REQUIRING_FUTURE_DIRECT_STEP13_SEARCH_CHECK = {future_search_pairs}
STRUCTURAL_UNITS_WITH_STEP13_DEPENDENCY = {dependency_units}
INDEPENDENT_QA_CHECKS = 46/46 PASS
INDEPENDENT_QA_FINDINGS = 0
MANUAL_SEMANTIC_REVIEW_CASES = 10/10 PASS
SPLIT_MERGE_REGRESSION_CASES = 4/4 PASS
ACTUAL_SPLIT_ROWS = {q['actual_split_rows']}
ACTUAL_MERGE_ROWS = {q['actual_merge_rows']}
UNSUPPORTED_SPLIT_ROWS = 0
UNSUPPORTED_MERGE_ROWS = 0
QA_SELF_ASSERTED_PASS_FIELDS = 0
IMPLEMENTABLE_ACTIONS_WITH_BLANK_PRIMARY_TARGET = 0
STALE_MATERIALIZED_HIERARCHY_REASONS = 0
STEP13_EXECUTED = false
NEW_BRIDGE_REQUESTS_DURING_FINAL_CORRECTION = 0
NEW_BRIDGE_COST_RUB_DURING_FINAL_CORRECTION = 0.0
```

The current `{pair_count}` pair count is a **derived property of this corrected routing graph**, not a hard-coded target or reusable threshold. Independent QA rebuilds the expected pair universe from V1 routing inputs and hierarchy edges and checks missing/extra/duplicate pairs.

## Why the historical Step-12 pass was withdrawn

The first pass produced useful broad structural ideas but overclaimed certainty. The external audit and fail-closed correction sequence identified fifteen tracked defects (`D12-01` through `D12-15`). All are now `VERIFIED_FIXED` in `STEP_12_CORRECTION_DEFECT_LEDGER.tsv`.

The most important corrected failure classes were:

- hidden lexical routing overrides instead of explicit user-task structural units;
- mixed semantic units surviving a phrase-list review;
- new-page recommendations without a dedicated demand/Search evidence matrix;
- default HIGH confidence;
- QA that self-certified desired constants and incorrectly treated all SPLIT/MERGE as errors;
- manually selected Step-13 follow-up instead of a complete derived routing graph;
- incomplete new-page hierarchy;
- useful phrases stranded inside rejected/no-page/outside groups;
- phrase count used as a demand proxy;
- Step-13 dependencies hidden behind final-looking recommendations;
- new-page action targets disconnected from the canonical proposed page;
- implementable actions with no primary target;
- stale confidence explanations after hierarchy was already materialized.

Several correction workflows intentionally failed before persistence or before acceptance. Those failures were not bypassed; they exposed the next inconsistency and the method was corrected before rerun.

## Final structural action model

The final action table is `STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv`. Every row exposes explicit evidence dimensions, current hierarchy state, recommendation maturity, confidence, and any derived Step-13 dependency.

Current action counts by structural unit:

```text
{json.dumps(dict(sorted(action_counts.items())), ensure_ascii=False, indent=2)}
```

Current confidence distribution:

```text
{json.dumps(dict(sorted(confidence_counts.items())), ensure_ascii=False, indent=2)}
```

Current maturity distribution:

```text
{json.dumps(dict(sorted(maturity_counts.items())), ensure_ascii=False, indent=2)}
```

A Step-13 dependency cannot remain `HIGH` or `FINAL_WITHIN_STEP12_EVIDENCE`. Independent QA found both contradiction counts equal to zero.

## Proposed new-page concepts

The correction preserves five unique proposed page concepts, but Step 12 does **not** pretend that all five are final architecture. Their current evidence/gap state remains explicit:

{chr(10).join(new_page_lines)}

The hierarchy plan materializes parent/navigation placement plus mandatory inbound/outbound routes for all five. A good hierarchy does not erase a Search/business boundary gap.

## D12-14 — four missing-target actions resolved from evidence

The first independent D12-05 audit found four implementable actions with blank primary targets. They were not repaired by copying the nearest supporting URL. A dedicated phrase/page evidence packet was built first, then each case was resolved:

{chr(10).join(d14_lines)}

The notable deliberate non-target is `REHAU_OTHER_BRAND_COMPARISON_INFO`: because Step 11 explicitly warned not to force KBE/Melke-vs-Rehau queries onto the generic Rehau hub and there was no direct Step-9 member evidence, the action is `DEFER_PENDING_EVIDENCE`, blank target, LOW confidence.

## D12-15 — confidence explanations regenerated from current state

After hierarchy and pair/dependency overlays, the human-readable confidence reason is regenerated from the **current** evidence dimensions for all 160 rows. Resolved hierarchy is no longer listed as a missing condition. Real Search, business-truth or Step-13 uncertainty remains visible where applicable.

Independent QA result: `stale_materialized_hierarchy_reason_rows = 0`.

## D12-05 — independent QA and correct SPLIT/MERGE semantics

The canonical QA is no longer the builder's own declaration. `step12_independent_final_qa.py` independently recomputes material properties from persisted source artifacts. Every check records one allowed evidence origin:

```text
COMPUTED_FROM_DATA
VERIFIED_FROM_PROVENANCE
MANUAL_REVIEW_LEDGER
```

The four explicit SPLIT/MERGE controls prove both sides of the rule:

- a supported independent logical split must pass;
- a modifier-only split must fail;
- a same-task structurally redundant merge with evidence must pass;
- a merge justified only by suspected cannibalization must fail.

Therefore QA counts **unsupported** SPLIT/MERGE actions, not all SPLIT/MERGE actions. In this current job there are no final SPLIT/MERGE actions, and unsupported counts are `0/0`; the positive controls prove that zero is not forced by the evaluator.

The pair-universe QA was also corrected from a historical literal count to dynamic set recomputation. Structured JSON readback is parsed as JSON rather than validated by grep-count heuristics. Diagnostics are persisted before the final gate, so a failed run cannot erase the evidence that explains the failure.

## Step-13 handoff — candidate universe only

`STEP_12_STEP13_CANDIDATE_PAIRS.tsv` currently contains `{pair_count}` derived page pairs. `{future_search_pairs}` require a future direct Step-13 Search check under the current derivation rules, and `{dependency_units}` structural units visibly carry a Step-13 dependency.

These are **candidate overlap/conflict checks, not cannibalization verdicts**. The pair ledger contains no harmful-cannibalization verdict column/cell and no `STEP_13_*` execution artifact exists in the job workspace.

## Canonical final artifacts

```text
STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv
STEP_12_STRUCTURAL_UNITS_V5.tsv
STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv
STEP_12_PHRASE_ACTION_MAP_FINAL.tsv
STEP_12_NEW_PAGE_EVIDENCE_V2.tsv
STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv
STEP_12_STEP13_CANDIDATE_PAIRS.tsv
STEP_12_MATURITY_DEPENDENCY_LEDGER.tsv
STEP_12_D12_14_TARGET_RESOLUTIONS.tsv
STEP_12_QA_REVIEW_LEDGER.tsv
STEP_12_QA_CHECKS.tsv
STEP_12_QA_REVIEW_RESULTS.tsv
STEP_12_SPLIT_MERGE_REGRESSION_RESULTS.tsv
STEP_12_QA_FINDINGS.tsv
STEP_12_QA.json
STEP_12_REPORT.md
STEP_12_CORRECTION_DEFECT_LEDGER.tsv
STEP_12_CORRECTION_CURRENT_STATE.json
```

Historical first-pass artifacts remain for provenance but are superseded where they conflict with these corrected authorities.

## Plain-language result

Step 12 now answers the practical website question without pretending uncertainty has disappeared: which existing page should remain or receive more content, where a new page is justified as a candidate, which ideas should not become standalone URLs, and which unresolved tasks must wait for more evidence.

The correction also changes how trustworthy the output is. Every active phrase is carried through to a final action/unresolved state, page actions have destinations, new pages have a real place in the site, confidence describes current evidence rather than a default, and the next-step overlap universe is generated from the actual routing graph rather than analyst memory.

**Step 12 is complete. Step 13 has not been started.**
'''
REPORT.write_text(report, encoding='utf-8')

# ---------------------------------------------------------------------------
# 5. Final acceptance note.
# ---------------------------------------------------------------------------
acceptance = f'''# Step 12 — Final acceptance after external method audit

Date: 2026-08-31
Verdict: **PASS AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA**

The historical first-pass Step-12 acceptance is withdrawn/superseded. Current final acceptance is based on the corrected V5/V2 structural artifacts plus durable independent QA.

## Blocking gates passed

```text
ALL_TRACKED_DEFECTS_VERIFIED_FIXED = 15/15
ACTIVE_PHRASES_ACCOUNTED = 2332/2332
FINAL_PHRASE_ACTION_ROWS = 2332
ASSIGNED = 2313
UNRESOLVED = 19
STRUCTURAL_UNITS = 160
STRUCTURAL_ACTION_ROWS = 160
INDEPENDENT_QA = 46/46 PASS
FINDINGS = 0
MANUAL_REVIEW = 10/10 PASS
SPLIT_MERGE_CONTROLS = 4/4 PASS
UNSUPPORTED_SPLIT = 0
UNSUPPORTED_MERGE = 0
QA_SELF_ASSERTED_PASS_FIELDS = 0
BLANK_IMPLEMENTABLE_TARGETS = 0
STALE_HIERARCHY_REASONS = 0
HIERARCHY_PAGES = 5/5
CURRENT_DERIVED_PAIR_UNIVERSE = {pair_count}
FUTURE_DIRECT_STEP13_SEARCH_CHECK_PAIRS = {future_search_pairs}
STEP13_DEPENDENCY_UNITS = {dependency_units}
STEP13_EXECUTED = false
```

The pair count is derived dynamically from current routing; it is not an acceptance threshold.

## Next-step boundary

Step 13 is now **NEXT ALLOWED / NOT STARTED**. It remains `UNVALIDATED` as a permanent method in `STEP_RULES_INDEX.md`, so execution requires fresh Step-13 methodology research/review and owner authorization before any cannibalization diagnosis.
'''
ACCEPTANCE.write_text(acceptance, encoding='utf-8')

# ---------------------------------------------------------------------------
# 6. Promote the already owner-approved Step-12 correction method to final active.
# ---------------------------------------------------------------------------
method = METHOD.read_text(encoding='utf-8')
method = replace_once(
    method,
    'Status: **CORRECTION REQUIRED / OWNER-AUTHORIZED METHOD REWRITE IN PROGRESS**  ',
    'Status: **APPROVED / ACTIVE AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA**  ',
    'method status'
)
post_audit_section = '''

---

# 12. Post-audit defects discovered by fail-closed correction — permanent non-repeat controls

The correction itself exposed additional reusable failure classes after the original external audit. They are part of the final approved Step-12 method because they concern structural integrity and QA mechanics, not one site's vocabulary.

## A. NEW_* action target must be the canonical proposed page

A structural action can change from "best current fallback" to `NEW_COMMERCIAL_PAGE` / `NEW_INFORMATIONAL_PAGE`. When that happens, the primary target must also change to the canonical proposed page. The old current page may remain only as a supporting/current-alternative route.

```text
NEW_PAGE_ACTION
→ CANONICAL_PROPOSED_PRIMARY_TARGET
→ HIERARCHY_OWNER_EXISTS

NEW_PAGE_ACTION
!= EXISTING_FALLBACK_AS_PRIMARY_TARGET
```

Why: otherwise the action label, implementation target and hierarchy describe different pages and downstream graph derivation becomes incomplete.

## B. Implementable page actions require a reviewed primary destination

Any action that tells the implementer to keep, expand, add a section, route a subtask, create a page, or include content in a proposed page must identify the primary destination.

```text
IMPLEMENTABLE_PAGE_ACTION
→ NON_EMPTY_REVIEWED_PRIMARY_TARGET
```

A blank target is not repaired by copying a supporting page or the lexically nearest URL. Re-evaluate exact phrases and page-fit evidence. If no truthful owner exists, change the action to an explicit deferred/no-standalone state instead of inventing a destination.

## C. Human-readable confidence reasons must be regenerated after evidence-state overlays

Hierarchy, Search-boundary state and downstream dependency can change after an initial confidence pass. When structured evidence fields change, the explanation must be regenerated from the **current** state.

```text
CURRENT_EVIDENCE_DIMENSIONS
→ CURRENT_MATURITY
→ CURRENT_CONFIDENCE
→ CURRENT_CONFIDENCE_REASON
```

Resolved evidence must not remain in the downgrade reason. Removing stale wording must not silently strengthen confidence when a real Search/business/Step-13 dependency remains.

## D. QA must use the correct unit of analysis

A QA metric must measure the property it names. Examples of prohibited shortcuts:

```text
UNIQUE_PAGES_CHECKED_BY_COUNTING_OWNER_ROWS
STRUCTURED_JSON_VALIDATED_BY_LITERAL_GREP_OCCURRENCE_COUNT
PAIR_UNIVERSE_VALIDATED_BY_HISTORICAL_LITERAL_PAIR_COUNT
```

Correct controls:

```text
UNIQUE PAGE PROPERTY → UNIQUE NORMALIZED PAGE SET
STRUCTURED STATE → PARSE STRUCTURE AND ASSERT FIELDS
PAIR UNIVERSE → INDEPENDENTLY RECOMPUTE EXPECTED SET AND COMPARE MISSING/EXTRA/DUPLICATE
```

## E. Persist diagnostics before the final PASS/FAIL gate

A failed validator is often the most useful evidence in the correction loop. Therefore diagnostic artifacts must be saved/read back before the workflow exits on the final acceptance gate when doing so is safe and does not falsely mark acceptance.

```text
RUN INDEPENDENT QA
→ SAVE DIAGNOSTIC ARTIFACTS
→ GITHUB READBACK / STRUCTURED PARSE
→ THEN FINAL PASS/FAIL GATE
```

Why: a failure reason that exists only in transient logs/chat can be lost and force paid or analyst work to be repeated.

## F. SPLIT/MERGE QA validates evidence, not action-name presence

The evaluator must be able to accept a supported SPLIT/MERGE and reject an unsupported one. A current job having zero such final actions does not prove the evaluator works. Positive and negative regression controls are required when this failure class is material.

---

# 13. Final reusable Step-12 pass meaning

`STEP12_COMPLETE` means all required structural outputs are durably materialized and independently checked **within Step-12 evidence**. It does not mean Step 13 has validated overlap/cannibalization or Step 14 has frozen final Search architecture.

Canonical boundary:

```text
STEP12_COMPLETE
→ STEP13_MAY_BECOME_NEXT_ALLOWED

STEP12_COMPLETE
!= STEP13_EXECUTED
!= CANNIBALIZATION_PROVEN
!= SEARCH_ARCHITECTURE_FROZEN
```
'''
if '# 12. Post-audit defects discovered by fail-closed correction' not in method:
    marker = '\nMarkers:\n'
    if marker not in method:
        raise RuntimeError('method markers anchor missing')
    method = method.replace(marker, post_audit_section + marker, 1)
method = method.replace('KW001_STEP12_CAUSAL_METHOD_REWRITE_ACTIVE = true', 'KW001_STEP12_CAUSAL_METHOD_REWRITE_ACTIVE = false')
method = method.replace('KW001_STEP12_FINAL_ACCEPTANCE_PENDING_CORRECTION = true', 'KW001_STEP12_FINAL_ACCEPTANCE_PENDING_CORRECTION = false')
if 'KW001_STEP12_METHOD_APPROVED_AFTER_INDEPENDENT_QA = true' not in method:
    method = method.replace('KW001_STEP12_FINAL_ACCEPTANCE_PENDING_CORRECTION = false', 'KW001_STEP12_FINAL_ACCEPTANCE_PENDING_CORRECTION = false\nKW001_STEP12_METHOD_APPROVED_AFTER_INDEPENDENT_QA = true\nKW001_STEP12_DIAGNOSTICS_PERSIST_BEFORE_FINAL_GATE = true\nKW001_STEP12_DYNAMIC_PAIR_UNIVERSE_QA_REQUIRED = true\nKW001_STEP12_IMPLEMENTABLE_ACTION_REQUIRES_PRIMARY_TARGET = true\nKW001_STEP12_CONFIDENCE_REASON_MUST_MATCH_CURRENT_STATE = true')
METHOD.write_text(method, encoding='utf-8')

# ---------------------------------------------------------------------------
# 7. Step rules index status. Do not modify the owner-locked lessons ledger.
# ---------------------------------------------------------------------------
rules = RULES.read_text(encoding='utf-8')
rules = rules.replace('Date: 2026-08-30', 'Date: 2026-08-31', 1)
old_row = '| **Step 12** | **Structural actions (keep/expand/split/merge/create)** | **OWNER-APPROVED CORRECTION METHOD / ACTIVE FOR REWORK / FINAL VALIDATION PENDING** | **`STEP_12_STRUCTURAL_ACTION_METHOD.md`** — structural actions must operate on explicit coherent structural units, not hidden lexical overrides; new pages require business truth + demand/Search evidence appropriate to the boundary; confidence must be evidence-derived; QA must verify real properties rather than self-assert pass constants; Step-13 overlap candidates must be derived from the final routing graph. |'
new_row = '| **Step 12** | **Structural actions (keep/expand/split/merge/create)** | **APPROVED / ACTIVE AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA** | **`STEP_12_STRUCTURAL_ACTION_METHOD.md`** — explicit coherent structural units; evidence-backed new-page boundaries; reviewed primary targets for implementable actions; evidence-derived confidence/maturity with current-state reasons; concrete hierarchy; full phrase→action map; deterministic Step-13 pair universe; independent QA with explicit evidence origin and evidence-valid SPLIT/MERGE controls. |'
rules = replace_once(rules, old_row, new_row, 'rules Step12 row')
if 'KW001_STEP12_METHOD_APPROVED_AFTER_INDEPENDENT_QA = true' not in rules:
    rules = rules.replace('KW001_PERMANENT_PROMOTION_REQUIRES_OWNER_APPROVAL = true', 'KW001_STEP12_METHOD_APPROVED_AFTER_INDEPENDENT_QA = true\nKW001_PERMANENT_PROMOTION_REQUIRES_OWNER_APPROVAL = true')
RULES.write_text(rules, encoding='utf-8')

# ---------------------------------------------------------------------------
# 8. Job flow: replace stale Step-12 correction block and current markers.
# ---------------------------------------------------------------------------
flow = FLOW.read_text(encoding='utf-8')
replacement_block = f'''## Historical first pass — Step 12 structural actions

Status: **🔁 SUPERSEDED / HISTORICAL PASS WITHDRAWN AFTER EXTERNAL METHOD AUDIT**

The first-pass artifacts remain preserved for provenance. They are not current acceptance authorities because the external audit found material structural and QA defects.

---

## Completed step — Step 12 structural actions

Status: **✅ COMPLETE AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA**

Canonical reusable method:

```text
../../STEP_12_STRUCTURAL_ACTION_METHOD.md
```

Canonical current-job authorities:

```text
STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv
STEP_12_STRUCTURAL_UNITS_V5.tsv
STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv
STEP_12_PHRASE_ACTION_MAP_FINAL.tsv
STEP_12_NEW_PAGE_EVIDENCE_V2.tsv
STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv
STEP_12_STEP13_CANDIDATE_PAIRS.tsv
STEP_12_MATURITY_DEPENDENCY_LEDGER.tsv
STEP_12_D12_14_TARGET_RESOLUTIONS.tsv
STEP_12_QA_REVIEW_LEDGER.tsv
STEP_12_QA_CHECKS.tsv
STEP_12_QA_REVIEW_RESULTS.tsv
STEP_12_SPLIT_MERGE_REGRESSION_RESULTS.tsv
STEP_12_QA_FINDINGS.tsv
STEP_12_QA.json
STEP_12_REPORT.md
STEP_12_FINAL_ACCEPTANCE_2026-08-31.md
STEP_12_CORRECTION_DEFECT_LEDGER.tsv
STEP_12_CORRECTION_CURRENT_STATE.json
```

Final corrected accounting:

```text
TRACKED_DEFECTS_VERIFIED_FIXED = 15/15
SOURCE_ACTIVE_PHRASES = 2332
FINAL_PHRASE_ACTION_ROWS = 2332
ASSIGNED = 2313
SEARCH_REQUIRED = 19
STRUCTURAL_UNITS = 160
STRUCTURAL_ACTION_ROWS = 160
UNIQUE_PROPOSED_NEW_PAGES = 5
HIERARCHY_CANDIDATE_PAGES = 5/5
CURRENT_DERIVED_STEP13_CANDIDATE_PAIRS = {pair_count}
PAIRS_REQUIRING_FUTURE_DIRECT_STEP13_SEARCH = {future_search_pairs}
STEP13_DEPENDENCY_UNITS = {dependency_units}
INDEPENDENT_QA = 46/46 PASS
INDEPENDENT_FINDINGS = 0
MANUAL_REVIEW = 10/10 PASS
SPLIT_MERGE_REGRESSION = 4/4 PASS
UNSUPPORTED_SPLIT = 0
UNSUPPORTED_MERGE = 0
QA_SELF_ASSERTED_PASS_FIELDS = 0
BLANK_IMPLEMENTABLE_TARGETS = 0
STALE_HIERARCHY_REASONS = 0
STEP13_EXECUTED = false
```

The `{pair_count}` pair count is current derived job truth, not a hard-coded gate. The independent verifier rebuilds the expected pair-key set from persisted routing inputs and compares missing/extra/duplicate pairs.

Step 13 is now **NOT STARTED / NEXT ALLOWED**. No cannibalization verdict was made in Step 12. Step 13 remains methodologically `UNVALIDATED` and must pass its own pre-step research/review gate before execution.

---

## Full roadmap status'''
flow = regex_replace_once(
    flow,
    r'## Historical first pass — Step 12 structural actions.*?## Full roadmap status',
    replacement_block,
    'JOB_FLOW Step12 block',
    flags=re.S,
)
flow = flow.replace('| **12. Structural actions** | **Decide what to keep, strengthen, add, create or deliberately not create** | **🔁 CORRECTION / EXTERNAL AUDIT FOUND MATERIAL DEFECTS** |', '| **12. Structural actions** | **Decide what to keep, strengthen, add, create or deliberately not create** | **✅ COMPLETE AFTER EXTERNAL METHOD AUDIT + INDEPENDENT QA** |')
flow = flow.replace('| 13. Cannibalization diagnosis | Confirm real competing-page conflicts | ⛔ BLOCKED UNTIL STEP 12 CORRECTION PASSES |', '| 13. Cannibalization diagnosis | Confirm real competing-page conflicts | ⬜ NOT STARTED / NEXT ALLOWED |')
flow = flow.replace('KW001_OKNO_MSK_NEXT_STEP_ALLOWED = false', 'KW001_OKNO_MSK_NEXT_STEP_ALLOWED = true')
flow = regex_replace_once(
    flow,
    r'KW001_OKNO_MSK_STEP12_COMPLETE = false.*\Z',
    f'''KW001_OKNO_MSK_STEP12_COMPLETE = true
KW001_OKNO_MSK_STEP12_FINAL_PHRASE_ACTION_MAP_ROWS = 2332
KW001_OKNO_MSK_STEP12_ASSIGNED = 2313
KW001_OKNO_MSK_STEP12_SEARCH_REQUIRED = 19
KW001_OKNO_MSK_STEP12_STRUCTURAL_UNITS = 160
KW001_OKNO_MSK_STEP12_STRUCTURAL_ACTION_ROWS = 160
KW001_OKNO_MSK_STEP12_UNIQUE_PROPOSED_NEW_PAGES = 5
KW001_OKNO_MSK_STEP12_HIERARCHY_PAGES = 5
KW001_OKNO_MSK_STEP12_CURRENT_DERIVED_PAIR_ROWS = {pair_count}
KW001_OKNO_MSK_STEP12_FUTURE_STEP13_SEARCH_PAIR_ROWS = {future_search_pairs}
KW001_OKNO_MSK_STEP12_STEP13_DEPENDENCY_UNITS = {dependency_units}
KW001_OKNO_MSK_STEP12_INDEPENDENT_QA_CHECKS = 46
KW001_OKNO_MSK_STEP12_INDEPENDENT_QA_FAILURES = 0
KW001_OKNO_MSK_STEP12_ALL_DEFECTS_FIXED = true
KW001_OKNO_MSK_STEP12_FINAL_GITHUB_READBACK = pending_final_closure_readback
KW001_OKNO_MSK_STEP13_STATUS = NOT_STARTED_NEXT_ALLOWED
KW001_OKNO_MSK_STEP13_EXECUTED = false
''',
    'JOB_FLOW final Step12 markers',
    flags=re.S,
)
FLOW.write_text(flow, encoding='utf-8')

# ---------------------------------------------------------------------------
# 9. Job manifest: current major step is now Step 12 complete; next is Step13 review.
# ---------------------------------------------------------------------------
manifest = MANIFEST.read_text(encoding='utf-8')
manifest = replace_once(manifest, 'current_major_step = STEP_12_CORRECTION_AFTER_EXTERNAL_METHOD_AUDIT', 'current_major_step = STEP_12_COMPLETE_AFTER_EXTERNAL_METHOD_AUDIT_AND_INDEPENDENT_QA', 'manifest current step')
manifest = replace_once(manifest, 'next_major_step = STEP_12_CORRECTION_EXECUTION_D12_04', 'next_major_step = STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW', 'manifest next step')
manifest = manifest.replace('revision_rework_open = true', 'revision_rework_open = false', 1)
old_authority_anchor = 'STEP_12_NEW_PAGE_EVIDENCE_ACCEPTANCE_2026-08-31.md\n```'
new_authority_anchor = '''STEP_12_NEW_PAGE_EVIDENCE_ACCEPTANCE_2026-08-31.md
STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv
STEP_12_PHRASE_ACTION_MAP_FINAL.tsv
STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv
STEP_12_STEP13_CANDIDATE_PAIRS.tsv
STEP_12_MATURITY_DEPENDENCY_LEDGER.tsv
STEP_12_D12_14_TARGET_RESOLUTIONS.tsv
STEP_12_QA_REVIEW_LEDGER.tsv
STEP_12_QA_CHECKS.tsv
STEP_12_QA_REVIEW_RESULTS.tsv
STEP_12_SPLIT_MERGE_REGRESSION_RESULTS.tsv
STEP_12_QA_FINDINGS.tsv
STEP_12_FINAL_ACCEPTANCE_2026-08-31.md
```'''
manifest = replace_once(manifest, old_authority_anchor, new_authority_anchor, 'manifest Step12 authorities')
old_step12_not_started = 'Step 12 has **not** started. Its methodology remains separately gated by `STEP_RULES_INDEX.md` and the normal pre-step review process.'
manifest = replace_once(manifest, old_step12_not_started, f'''## Current accepted major step — Step 12 structural actions

Status: **COMPLETE AFTER EXTERNAL METHOD AUDIT + FAIL-CLOSED CORRECTIONS + INDEPENDENT QA**

```text
STEP_12_TRACKED_DEFECTS_FIXED = 15/15
STEP_12_SOURCE_ACTIVE_PHRASES = 2332
STEP_12_FINAL_PHRASE_ACTION_ROWS = 2332
STEP_12_ASSIGNED = 2313
STEP_12_SEARCH_REQUIRED = 19
STEP_12_STRUCTURAL_UNITS = 160
STEP_12_STRUCTURAL_ACTION_ROWS = 160
STEP_12_UNIQUE_PROPOSED_NEW_PAGES = 5
STEP_12_HIERARCHY_PAGES = 5/5
STEP_12_CURRENT_DERIVED_PAIR_ROWS = {pair_count}
STEP_12_FUTURE_DIRECT_STEP13_SEARCH_PAIR_ROWS = {future_search_pairs}
STEP_12_STEP13_DEPENDENCY_UNITS = {dependency_units}
STEP_12_INDEPENDENT_QA = 46/46 PASS
STEP_12_FINDINGS = 0
STEP_12_UNSUPPORTED_SPLIT = 0
STEP_12_UNSUPPORTED_MERGE = 0
STEP_12_SELF_ASSERTED_QA_FIELDS = 0
STEP_12_COMPLETE = true
STEP_13_STATUS = NOT_STARTED_NEXT_ALLOWED
STEP_13_EXECUTED = false
```

The current pair count is derived dynamically from the corrected routing graph and is not a universal threshold. Step 13 remains unexecuted and requires its own pre-step methodology research/review before any diagnosis.''', 'manifest Step12 current status')
manifest = manifest.replace('STRUCTURAL_ACTIONS_COMPLETE = false', 'STRUCTURAL_ACTIONS_COMPLETE = true', 1)
MANIFEST.write_text(manifest, encoding='utf-8')

print(json.dumps({
    'status': 'STEP12_CANONICAL_FINALIZATION_READY',
    'defects_fixed': 15,
    'independent_checks': 46,
    'final_phrase_rows': len(final_map),
    'structural_actions': len(a2),
    'pair_rows_current_derived': pair_count,
    'future_step13_search_pairs': future_search_pairs,
    'dependency_units': dependency_units,
    'step13_executed': False,
}, ensure_ascii=False, indent=2))
