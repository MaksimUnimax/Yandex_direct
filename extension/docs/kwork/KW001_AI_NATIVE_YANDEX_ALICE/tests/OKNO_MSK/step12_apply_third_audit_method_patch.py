from pathlib import Path

R=Path(__file__).resolve().parent
ROOT=R.parents[2]
METHOD=ROOT/'STEP_12_STRUCTURAL_ACTION_METHOD.md'
INDEX=ROOT/'STEP_RULES_INDEX.md'

m=METHOD.read_text(encoding='utf-8')
old='Status: **APPROVED / ACTIVE AFTER SECOND EXTERNAL METHOD AUDIT — OWNER GOAL + CURRENT-SITE FRESHNESS + CONTENT REUSE + INDEPENDENT QA**'
new='Status: **REOPENED / THIRD EXTERNAL METHOD CORRECTION IN PROGRESS — GAP TYPE + PERFORMANCE BOUNDARY + TARGET-VS-RELEVANT + SERP FORMAT + OWNER-GOAL SOURCE + EXISTING-PAGE INTERNAL LINKS**'
if old in m:
    m=m.replace(old,new,1)
elif new not in m:
    raise RuntimeError('Unexpected Step12 method status')

marker='\n# 4. Correct Step-12 working model\n'
section=r'''

# 3A. Third external audit — six additional defects that must not be hidden by a technically clean V3

The third external literature review compared the current V3 method against current Yandex, Semrush, Ahrefs, Topvisor and Rush guidance. V3 fixed false CREATE decisions and business-goal mistakes, but six evidence layers were still too compressed. These are tracked as D12-21..D12-26.

## Defect 21 — content-gap type was implicit instead of explicit

### What V3 did
V3 stored `current_page_fit`, `existing_content_reuse` and the final structural action. The analyst could often infer why an action existed.

### Why that seemed sufficient
If the action is `EXPAND`, the page is presumably incomplete; if it is `CREATE`, something is presumably missing. The action appeared to encode the diagnosis.

### Why it is insufficient
Current content-gap methodology distinguishes fundamentally different failures: missing topic, wrong intent, weak/incomplete quality, lack of original value, or mixed/uncertain evidence. Those causes can produce different implementation even when the high-level action label looks similar. An ownership gap is also not automatically a content gap.

### Permanent rule
Every structural unit must state:

```text
GAP_TYPE =
  NONE
  TOPIC_GAP
  INTENT_GAP
  QUALITY_GAP
  ORIGINALITY_GAP
  MIXED_GAP
  EVIDENCE_INSUFFICIENT

GAP_EVIDENCE = why this diagnosis follows from current evidence
```

`CREATE` is allowed only after a verified `TOPIC_GAP` survives current-site, reuse, business-goal, demand and Search-boundary gates.

**Why:** the method must diagnose the problem before prescribing the page action.

## Defect 22 — structural KEEP could be misread as "do nothing" without performance evidence

### What V3 did
`KEEP_EXISTING_STRUCTURE` correctly meant the current URL is the best structural owner. In human reporting it could still sound like the page itself needs no improvement.

### Why that seemed reasonable
Step 12 is primarily structural. A strong task/page fit is enough to avoid unnecessary CREATE/SPLIT/MERGE.

### Why it is insufficient
Content-audit methods use traffic, visibility trends, conversions and business outcomes when deciding whether content is actually performing well enough to keep unchanged. The base Kwork order explicitly does not include Yandex Webmaster/Metrika account access, so Step 12 cannot honestly certify page performance.

### Permanent rule
Separate:

```text
STRUCTURAL_OWNER_DECISION
!=
OPTIMIZATION/PERFORMANCE_STATE
```

Required fields:

```text
PERFORMANCE_EVIDENCE_STATE
OPTIMIZATION_READINESS
```

When analytics are outside scope:

```text
PERFORMANCE_EVIDENCE_STATE = NOT_AVAILABLE_IN_BASE_SCOPE_NO_WEBMASTER_METRIKA
KEEP_EXISTING_STRUCTURE = KEEP THE URL/ROLE, NOT "NO OPTIMIZATION NEEDED"
```

**Why:** absence of analytics must constrain the claim, not be silently treated as good performance.

## Defect 23 — intended target and Yandex-selected relevant URL were not materialized together

### What V3 did
It stored the intended primary page plus a compressed `search_boundary_support` state.

### Why that seemed reasonable
Step 11 had already documented that target URL means intended owner, and ordinary Search evidence was sampled rather than exhaustive.

### Why it is insufficient
The page an analyst wants to rank and the page Yandex actually selects are different facts. A mismatch or non-observation can change confidence and determine what Step 13 must inspect.

### Permanent rule
For every unit preserve:

```text
INTENDED_TARGET_URL
CURRENT_YANDEX_RELEVANT_URL
RELEVANT_URL_MATCH_STATE =
  MATCH
  MISMATCH
  SITE_NOT_OBSERVED
  NOT_DIRECTLY_CHECKED
```

Only persisted ordinary-Search evidence may populate the observed URL. Never infer a ranking URL from page semantics.

**Why:** target ownership is a recommendation; relevant URL is observed search behaviour.

## Defect 24 — broad intent/support fields hid SERP content type / format / angle

### What V3 did
It stored broad intent and Search support strength.

### Why that seemed reasonable
For many commercial pages, broad intent plus obvious page fit is enough for structural ownership.

### Why it is insufficient
When page boundary is disputed, "informational" does not distinguish a how-to, comparison, list, calculator, review/forum result, product/category page or service landing. Current Search methodology uses the actual SERP to understand content type, format and angle.

### Permanent rule
For direct material Search evidence preserve separately:

```text
SERP_EXPECTED_CONTENT_TYPE
SERP_EXPECTED_FORMAT
SERP_EXPECTED_ANGLE
SERP_FORMAT_EVIDENCE_STATE
```

If the persisted evidence did not record a dimension, write `NOT_SEPARATELY_OBSERVED_IN_PERSISTED_EVIDENCE`; do not fabricate it from broad intent.

**Why:** evidence incompleteness is information and must remain visible.

## Defect 25 — owner-goal evidence source strength was not explicit enough

### What V3 did
It added owner goal, desired user outcome, business potential and content role. Many goals were inferred from the public commercial site.

### Why that seemed reasonable
A commercial site often makes its lead/sales objective obvious, and the base order does not include client interviews or CRM/support research.

### Why it is insufficient
A public-site inference is not the same evidence as an explicit client instruction, analytics, sales calls or support evidence. Some businesses deliberately publish low-direct-conversion content for authority/top-of-funnel strategy.

### Permanent rule
Add:

```text
OWNER_GOAL_EVIDENCE_SOURCE =
  CLIENT_STATED
  ANALYTICS_OBSERVED
  SALES_SUPPORT_EVIDENCE
  PUBLIC_SITE_EXPLICIT
  PUBLIC_SITE_INFERRED
  UNKNOWN

OWNER_POLICY_MATERIALITY = HIGH / MEDIUM / LOW / NOT_APPLICABLE
```

If a policy-sensitive action depends on an inferred/unknown goal, preserve that uncertainty. Never label inference as client-stated truth.

**Why:** business strategy is evidence, not a model assumption.

## Defect 26 — internal linking was treated mainly as a new-page hierarchy problem

### What V3 did
It had detailed hierarchy plans for proposed new pages, but most `ROUTE`, `SECTION` and `EXPAND` actions among existing pages were represented only by primary/supporting URLs.

### Why that seemed reasonable
The page relationship was conceptually visible and the initial hierarchy concern was orphaned new pages.

### Why it is insufficient
After all five CREATE concepts were withdrawn, the implementation value of Step 12 sits largely in relationships between existing pages. A route is not fully implementable if the client cannot see source, destination and purpose.

### Permanent rule
Material existing-page relationships must be written to an internal-link action ledger with:

```text
structural_unit_id
source_url
target_url
link_action_state
relation_type
placement_context
anchor_concept
user_journey_purpose
business_handoff
evidence_origin
```

When no distinct source/target link is justified, record an explicit `NOT_APPLICABLE` or `DEFER_SOURCE_CONTEXT_NOT_MATERIALIZED` rather than inventing a link.

**Why:** internal linking is part of implementing a routing decision, not decorative SEO after the architecture is finished.

## Third-audit source-derived execution overlay

The following order is mandatory because each stage constrains the next one:

```text
1. OWNER GOAL + EVIDENCE SOURCE
2. FULL PHRASE SET / COHERENT STRUCTURAL UNIT
3. FRESH CURRENT-SITE + CONTENT-REUSE CHECK
4. GAP TYPE DIAGNOSIS
5. STRUCTURAL OWNER FIT
6. PERFORMANCE EVIDENCE STATE (AVAILABLE / OUT OF SCOPE / MISSING)
7. REAL DEMAND
8. INTENDED TARGET vs OBSERVED YANDEX RELEVANT URL
9. SERP CONTENT TYPE / FORMAT / ANGLE WHEN MATERIAL
10. KEEP/EXPAND/SECTION/ROUTE/REUSE BEFORE CREATE
11. ACTION + STRUCTURAL-ONLY vs OPTIMIZATION-READY MEANING
12. EVIDENCE-DERIVED CONFIDENCE / MATURITY
13. INTERNAL-LINK IMPLEMENTATION FOR MATERIAL EXISTING-PAGE RELATIONS
14. FULL PHRASE MAP
15. DERIVED STEP-13 PAIR UNIVERSE
16. INDEPENDENT QA + OWNER CHALLENGE
17. GITHUB SAVE + STRUCTURED READBACK
18. PLAIN-LANGUAGE OWNER REPORT
```

### Third-audit fail-closed checks

```text
STRUCTURAL_UNITS_WITHOUT_GAP_TYPE = 0
CREATE_WITHOUT_VERIFIED_TOPIC_GAP = 0
KEEP_PRESENTED_AS_NO_OPTIMIZATION_NEEDED_WITHOUT_PERFORMANCE_EVIDENCE = 0
STRUCTURAL_UNITS_WITHOUT_PERFORMANCE_EVIDENCE_STATE = 0
STRUCTURAL_UNITS_WITHOUT_RELEVANT_URL_MATCH_STATE = 0
OBSERVED_RELEVANT_URL_WITHOUT_PERSISTED_SEARCH_EVIDENCE = 0
DIRECT_SERP_EVIDENCE_WITHOUT_EXPLICIT_TYPE_FORMAT_ANGLE_STATE = 0
STRUCTURAL_UNITS_WITHOUT_OWNER_GOAL_EVIDENCE_SOURCE = 0
POLICY_SENSITIVE_UNKNOWN_OWNER_GOAL_PRESENTED_AS_FINAL = 0
MATERIAL_ROUTE_WITHOUT_LINK_ACTION_OR_EXPLICIT_NA_DEFER = 0
INTERNAL_LINK_TO_WITHDRAWN_PROPOSED_NEW_PAGE = 0
```

'''
if '# 3A. Third external audit' not in m:
    if marker not in m: raise RuntimeError('method marker missing')
    m=m.replace(marker,section+marker,1)
METHOD.write_text(m,encoding='utf-8')

i=INDEX.read_text(encoding='utf-8')
oldrow='| **Step 12** | **Structural actions (keep/expand/split/merge/create)** | **APPROVED / ACTIVE AFTER SECOND EXTERNAL METHOD AUDIT** | **`STEP_12_STRUCTURAL_ACTION_METHOD.md` + `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`** — owner goal first; fresh current-site/content check before CREATE; existing-content reuse; business-potential/content-role gate; current routing; evidence-derived confidence/maturity; derived Step-13 pairs; independent QA and owner-challenge cases. |'
newrow='| **Step 12** | **Structural actions (keep/expand/split/merge/create)** | **REOPENED / THIRD METHOD CORRECTION IN PROGRESS** | **`STEP_12_STRUCTURAL_ACTION_METHOD.md` + `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`** — add explicit gap type, separate structural ownership from performance/optimization claims, materialize intended-vs-Yandex-relevant URL, preserve SERP content-type/format/angle states, label owner-goal evidence source, and materialize implementable internal links for existing-page actions. D12-21..D12-26 remain open until current-job V4 revalidation. |'
if oldrow in i:
    i=i.replace(oldrow,newrow,1)
elif newrow not in i:
    raise RuntimeError('Step12 index row missing')
INDEX.write_text(i,encoding='utf-8')
print('STEP12_THIRD_AUDIT_METHOD_PATCH_APPLIED')
