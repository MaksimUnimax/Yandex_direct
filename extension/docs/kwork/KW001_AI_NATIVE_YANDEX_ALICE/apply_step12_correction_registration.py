from pathlib import Path

ROOT = Path('extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE')
JOB = ROOT / 'tests/OKNO_MSK'

# 1) Register Step 12 canonical method in the permanent index.
index_path = ROOT / 'STEP_RULES_INDEX.md'
index = index_path.read_text(encoding='utf-8')
old_row = '| Step 12 | Structural actions (keep/expand/split/merge/create) | **UNVALIDATED** | Must separate evidence-backed structural action from analyst preference. |'
new_row = '| **Step 12** | **Structural actions (keep/expand/split/merge/create)** | **OWNER-APPROVED CORRECTION METHOD / ACTIVE FOR REWORK / FINAL VALIDATION PENDING** | **`STEP_12_STRUCTURAL_ACTION_METHOD.md`** — structural actions must operate on explicit coherent structural units, not hidden lexical overrides; new pages require business truth + demand/Search evidence appropriate to the boundary; confidence must be evidence-derived; QA must verify real properties rather than self-assert pass constants; Step-13 overlap candidates must be derived from the final routing graph. |'
if old_row in index:
    index = index.replace(old_row, new_row, 1)
elif new_row not in index:
    raise RuntimeError('STEP_RULES_INDEX Step12 row anchor not found')
index_path.write_text(index, encoding='utf-8')

# 2) Add owner-approved reusable causal lesson. Keep it generic; current job rows stay in Layer C.
ledger_path = ROOT / 'STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md'
ledger = ledger_path.read_text(encoding='utf-8')
heading = '## Step 12 — structural actions: causal correction after external audit'
if heading not in ledger:
    section = r'''

---

## Step 12 — structural actions: causal correction after external audit

### Step purpose

Turn a phrase-level semantic/page map into a practical, evidence-backed site-structure plan: what to keep, strengthen, add, create, split, merge or deliberately not create.

### Why this step needs its own method

A structurally tidy recommendation can still be wrong if the analyst skips the user-task boundary, uses lexical matching as proof, equates phrase count with demand, invents commercial pages the business cannot fulfil, or lets the same script both create and certify its own result.

Step 12 therefore has to preserve the reasoning chain that turns search demand into a page decision. The output is not merely a taxonomy of action labels.

### Known errors that caused the correction

1. **Hidden lexical overrides were treated as architecture.** Individual phrases were routed to specific pages by substring/token rules without first creating an explicit user-task structural unit.
2. **Phrase visibility was mistaken for semantic coherence.** A full phrase list existed, but mixed objects/tasks could still survive and receive one action.
3. **New-page creation was under-evidenced.** Phrase count + page gap + narrative usefulness were treated as enough without a per-candidate demand/Search evidence matrix.
4. **Confidence defaulted to HIGH.** Confidence reflected the absence of a manual downgrade rather than evidence strength.
5. **QA partly self-certified the desired result.** Some pass properties were constants or weak proxies, and any SPLIT/MERGE was counted as failure rather than only unsupported actions.
6. **The next-step overlap universe was hand-curated.** Candidate page pairs were not derived from the complete final routing graph.
7. **New-page hierarchy was incomplete.** A proposed slug/parent label did not fully specify how the page belongs in navigation and internal linking.
8. **`NO_STANDALONE_PAGE` could strand useful subtasks.** Rejecting one generic page was treated as if it answered where each useful phrase should go.
9. **Useful rows could remain trapped inside rejected groups.** Cluster-level protection against an unsupported page could hide phrases that belonged to a valid different task/page.
10. **Phrase count was used as a demand proxy.** Vocabulary size was allowed to strengthen demand narratives without materialized frequency/traffic evidence.
11. **Downstream dependencies were hidden by final-looking actions.** A recommendation could depend on later conflict testing while still looking implementation-ready.

### Root cause

The first method correctly understood the broad principle — do not create a page for every phrase — but moved too quickly from cluster/page evidence to a structural action. Several intermediate proof steps were implicit rather than materialized.

Canonical causal error:

```text
PLAUSIBLE ROUTE / PLAUSIBLE PAGE IDEA
!=
EVIDENCE-BACKED STRUCTURAL UNIT + VERIFIED PAGE ROLE
```

The same pattern also affected QA:

```text
DESIRED INVARIANT WRITTEN INTO THE SCRIPT
!=
INVARIANT INDEPENDENTLY VERIFIED FROM DATA / PROVENANCE / REVIEW LEDGER
```

### Corrected method / non-repeat controls

The approved corrected sequence is:

```text
FULL PHRASE SET
→ COHERENCE AUDIT
→ EXPLICIT STRUCTURAL UNITS / CORRECTIONS
→ BUSINESS TRUTH
→ CURRENT PAGE FIT
→ DEMAND EVIDENCE
→ SEARCH/SERP EVIDENCE WHEN MATERIAL TO THE PAGE BOUNDARY
→ COMPARE STRUCTURAL ALTERNATIVES
→ ACTION
→ EVIDENCE-DERIVED CONFIDENCE + PROVISIONAL/FINAL MATURITY
→ SITE-HIERARCHY / INTERNAL-LINK ROLE
→ COMPLETE PHRASE→UNIT→PAGE/ACTION MAP
→ DERIVED STEP-13 CANDIDATE PAIRS
→ INDEPENDENT QA
→ GITHUB SAVE + READBACK
```

Why this order matters:

- coherence must come before demand aggregation, otherwise different tasks are measured together;
- business truth must come before a commercial CREATE, because search demand cannot create a product/service the business does not offer;
- current page fit must come before CREATE, otherwise the method can duplicate an existing useful page;
- phrase count is coverage, not demand; actual demand evidence is required for demand-strength claims;
- lexical tokens may discover a candidate subunit but may not silently become the final page assignment;
- confidence is a conclusion from evidence dimensions, never a default value;
- `NO_STANDALONE_PAGE` still requires routing/defer logic for useful subparts;
- SPLIT/MERGE are allowed when supported; QA checks evidence for them rather than requiring their count to be zero;
- Step 13 receives a complete candidate-pair universe but makes the cannibalization diagnosis itself.

### Canonical evidence dimensions for confidence

At minimum preserve:

```text
TASK_COHERENCE
BUSINESS_TRUTH
CURRENT_PAGE_FIT
DEMAND_SUPPORT
SEARCH_BOUNDARY_SUPPORT WHEN MATERIAL
HIERARCHY_CLARITY
```

A missing material dimension downgrades confidence or makes the action provisional. `HIGH` must never be the default simply because no rejection rule fired.

### QA origin rule

Every material Step-12 QA claim must be traceable to one of:

```text
COMPUTED_FROM_DATA
VERIFIED_FROM_PROVENANCE / EXECUTION RECEIPT
MANUAL_REVIEW_LEDGER WITH EXPLICIT CASES
```

Hard-coded expected zero/true values are not QA evidence.

### Why these controls are reusable

The failure was not specific to one window site. Any semantic-architecture job can over-trust a cluster label, a matching word, a page slug, a row count or a self-authored QA script. The correction therefore applies to future Step-12 executions regardless of domain; current-job vocabulary and exact boundaries remain configured from that job's evidence.

### Method origin / external support

- Yandex user-need targeting: https://yandex.ru/support/webmaster/ru/recommendations/targeting
- Yandex site structure: https://yandex.ru/support/webmaster/ru/recommendations/site-structure
- Yandex logical content splitting: https://yandex.ru/support/webmaster/ru/recommendations/presentation
- Yandex low-value/low-demand pages: https://yandex.ru/support/webmaster/ru/site-indexing/low-demand
- Yandex useful content: https://yandex.ru/support/webmaster/ru/threat/useless-content
- Semrush Keyword Mapping (2026-07-27): https://www.semrush.com/blog/keyword-mapping/
- Ahrefs Keyword Mapping: https://ahrefs.com/blog/keyword-mapping/
- Ahrefs Keyword Clustering: https://ahrefs.com/blog/keyword-clustering/
- Rush Analytics semantic structure / clustering / relevant URL methodology: https://www.rush-analytics.ru/faq/kak-sozdat-strukturu-sayta-na-osnove-semanticheskogo-yadra and related clustering/relevant-URL guides
- Semrush cannibalization boundary (2026-07-14): https://www.semrush.com/blog/keyword-cannibalization-guide/

### Pass gate

Step 12 cannot pass while any of these are true:

```text
HIDDEN_LEXICAL_OVERRIDE_RULES_IN_FINAL_ARCHITECTURE > 0
KNOWN_MIXED_STRUCTURAL_UNITS_LEFT_UNCORRECTED > 0
ACCEPTED_NEW_PAGE_WITHOUT_REQUIRED_DEMAND/BUSINESS/PAGE-BOUNDARY_EVIDENCE > 0
DEFAULT_HIGH_CONFIDENCE = true
CONFIDENCE_WITHOUT_EVIDENCE_DIMENSIONS > 0
QA_SELF_ASSERTED_PASS_FIELDS > 0
UNSUPPORTED_SPLIT > 0
UNSUPPORTED_MERGE > 0
USEFUL_PHRASES_STRANDED_BY_NO_STANDALONE_PAGE > 0
ACCEPTED_NEW_OR_SPLIT_PAGES_WITHOUT_HIERARCHY_PLAN > 0
STEP13_CANDIDATE_UNIVERSE_DERIVED = false
```

Final acceptance additionally requires complete phrase accounting and GitHub persistence/readback.

Status: **OWNER-APPROVED CORRECTION METHOD / ACTIVE FOR REWORK / FINAL VALIDATION PENDING**.

Markers:

```text
STEP12_HIDDEN_LEXICAL_OVERRIDE_IS_NOT_ARCHITECTURE = true
STEP12_PHRASE_VISIBILITY_NOT_EQUAL_COHERENCE = true
STEP12_PHRASE_COUNT_NOT_EQUAL_DEMAND = true
STEP12_CONFIDENCE_MUST_BE_EVIDENCE_DERIVED = true
STEP12_QA_SELF_CERTIFICATION_FORBIDDEN = true
STEP12_SPLIT_MERGE_SUPPORTED_NOT_ZERO_FORCED = true
STEP12_NO_STANDALONE_PAGE_REQUIRES_USEFUL_SUBTASK_ROUTING = true
STEP12_STEP13_CANDIDATE_UNIVERSE_MUST_BE_DERIVED = true
STEP12_HIERARCHY_PLAN_REQUIRED_FOR_NEW_OR_SPLIT_PAGES = true
```
'''
    marker = '\n---\n\nMarkers:\n'
    if marker in ledger:
        ledger = ledger.replace(marker, section + marker, 1)
    else:
        ledger += section
ledger_path.write_text(ledger, encoding='utf-8')

# 3) Withdraw current-job first-pass acceptance and block Step 13 until correction passes.
flow_path = JOB / 'JOB_FLOW.md'
flow = flow_path.read_text(encoding='utf-8')
flow = flow.replace(
    '## Completed step — Step 12 structural actions\n\nStatus: **✅ COMPLETE / PASS AFTER FULL STRUCTURAL ACTION AUDIT**',
    '## Historical first pass — Step 12 structural actions\n\nStatus: **🔁 CORRECTION REQUIRED AFTER EXTERNAL METHOD AUDIT / HISTORICAL PASS WITHDRAWN**',
    1,
)
flow = flow.replace(
    '| **12. Structural actions** | **Decide what to keep, strengthen, add, create or deliberately not create** | **✅ COMPLETE / PASS AFTER FULL STRUCTURAL ACTION AUDIT** |',
    '| **12. Structural actions** | **Decide what to keep, strengthen, add, create or deliberately not create** | **🔁 CORRECTION / EXTERNAL AUDIT FOUND MATERIAL DEFECTS** |',
    1,
)
flow = flow.replace(
    '| 13. Cannibalization diagnosis | Confirm real competing-page conflicts | ⬜ NOT STARTED |',
    '| 13. Cannibalization diagnosis | Confirm real competing-page conflicts | ⛔ BLOCKED UNTIL STEP 12 CORRECTION PASSES |',
    1,
)
# Replace obsolete Step12 completion markers if present.
flow = flow.replace('KW001_OKNO_MSK_STEP12_COMPLETE = true', 'KW001_OKNO_MSK_STEP12_COMPLETE = false')
flow = flow.replace('KW001_OKNO_MSK_NEXT_STEP_ALLOWED = true', 'KW001_OKNO_MSK_NEXT_STEP_ALLOWED = false')
correction_block = r'''

---

## CURRENT OVERRIDE — Step 12 correction after external audit

This block overrides the historical first-pass Step-12 PASS above.

```text
STEP12_CORRECTION_REQUIRED_AFTER_EXTERNAL_METHOD_AUDIT = true
STEP12_HISTORICAL_FIRST_PASS_PRESERVED = true
STEP12_HISTORICAL_PASS_WITHDRAWN = true
STEP12_OPEN_DEFECTS = D12-01,D12-02,D12-03,D12-04,D12-05,D12-06,D12-07,D12-08,D12-09,D12-10,D12-11
STEP12_CURRENT_CORRECTION_ITEM = D12-01
STEP13_BLOCKED_BY_STEP12_CORRECTION = true
STEP12_CORRECTED_ACCEPTANCE = pending
```

Current correction authorities:

```text
../../STEP_12_STRUCTURAL_ACTION_METHOD.md
STEP_12_EXTERNAL_METHOD_AUDIT_2026-08-31.md
STEP_12_CORRECTION_PLAN_2026-08-31.md
STEP_12_CORRECTION_DEFECT_LEDGER.tsv
STEP_12_CORRECTION_CURRENT_STATE.json
```

A defect is not closed because a new file exists. It is closed only after its corrective artifact is produced, its defect-specific verification passes, and GitHub readback confirms the saved result.
'''
if 'STEP12_CORRECTION_REQUIRED_AFTER_EXTERNAL_METHOD_AUDIT = true' not in flow:
    anchor = '\n---\n\n## Full roadmap status\n'
    if anchor in flow:
        flow = flow.replace(anchor, correction_block + anchor, 1)
    else:
        flow += correction_block
flow_path.write_text(flow, encoding='utf-8')

# 4) Make manifest point at correction, not Step 13.
manifest_path = JOB / 'JOB_MANIFEST.md'
manifest = manifest_path.read_text(encoding='utf-8')
manifest = manifest.replace(
    'current_major_step = STEP_12_COMPLETE_AFTER_FULL_STRUCTURAL_ACTION_AUDIT',
    'current_major_step = STEP_12_CORRECTION_AFTER_EXTERNAL_METHOD_AUDIT',
    1,
)
manifest = manifest.replace(
    'next_major_step = STEP_13_PRE_STEP_METHODOLOGY_RESEARCH_AND_REVIEW',
    'next_major_step = STEP_12_CORRECTION_EXECUTION_D12_01',
    1,
)
add_auth = [
    '../../STEP_12_STRUCTURAL_ACTION_METHOD.md',
    'STEP_12_EXTERNAL_METHOD_AUDIT_2026-08-31.md',
    'STEP_12_CORRECTION_PLAN_2026-08-31.md',
    'STEP_12_CORRECTION_DEFECT_LEDGER.tsv',
    'STEP_12_CORRECTION_CURRENT_STATE.json',
]
for item in add_auth:
    if item not in manifest:
        marker = '```\n\nWhere older Step-09 planning state'
        if marker not in manifest:
            raise RuntimeError('JOB_MANIFEST authority block end anchor not found')
        manifest = manifest.replace(marker, item + '\n' + marker, 1)
manifest_path.write_text(manifest, encoding='utf-8')
