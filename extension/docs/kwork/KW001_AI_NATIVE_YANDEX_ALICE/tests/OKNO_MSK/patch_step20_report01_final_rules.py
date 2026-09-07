from pathlib import Path

ROOT = Path(__file__).resolve().parent
GATE = (ROOT / '../../STEP_20_REPORT_01_CUSTOMER_RESEARCH_REPORT_GATE.md').resolve()
text = GATE.read_text(encoding='utf-8')
text = text.replace('Updated: 2026-09-06', 'Updated: 2026-09-07')

# Supersede old Alice-as-afterthought wording wherever it still exists.
text = text.replace(
    'Alice-based answers in Yandex are an additional selected verification layer. They do not replace the semantic-core analysis and must not be presented as the author of the research conclusion.',
    'Alice-based answers in Yandex are a core evidence surface of the sold Alice-native semantic rebuild. They do not replace the semantic-core analysis and must not be presented as the author of the research conclusion.'
)
text = text.replace('WHY ALICE WAS USED AFTER ORDINARY YANDEX', 'HOW ALICE WAS USED AS A CORE SURFACE OF THE KWORK')
text = text.replace(
    '→ WHAT THE SELECTED ALICE-BASED CHECKS ADDED',
    '→ HOW THE CORE / PAGE DISTRIBUTION CORRESPONDS TO ALICE\n→ WHY SELECTED ALICE CASES WERE THEN USED FOR DEEPER REFINEMENT'
)

# Append one final canonical subsection rather than relying on old section anchors.
marker = '## 14. Final Alice-native Report 01 contract — 2026-09-07'
section = r'''

## 14. Final Alice-native Report 01 contract — 2026-09-07

This section is authoritative over any older wording above that conflicts with it.

### Product goal

```text
KWORK_GOAL
= REBUILD / RE-EVALUATE THE SEARCH CORE UNDER MODERN YANDEX SEARCH WITH ALICE AS A CORE SURFACE

ALICE
!= OPTIONAL ADDITIONAL CHECK AFTER ORDINARY SEO
```

The customer report must make clear that the product exists for the new search reality in which ordinary Yandex results and Alice output both matter to the semantic/page decision.

### Required narrative order

```text
SEARCH DEMAND / WORDSTAT FOR THE TARGET REGION
→ CLEAN / GROUP THE CORE
→ DISTRIBUTE DEMAND ACROSS PAGES
→ USE ORDINARY YANDEX WHERE SEARCH BOUNDARIES NEED VALIDATION
→ EVALUATE THE RESULTING CORE / PAGE DISTRIBUTION AGAINST ALICE
→ STATE THE OVERALL ALICE-COMPATIBILITY VERDICT FOR THE SITE
→ ONLY THEN EXPLAIN THE 25 CANDIDATE THEMES AND 8 DEEP-DIVE CASES
→ READY IMPROVEMENTS / COMPANY FACTS / FINAL KWORK ANSWER
```

The eight Alice cases are deep dives used to represent different decision types and refine content. They are not the entire scope or entire value of the work with Alice.

### Frequency wording

Report №01 must state only what was actually done: search phrases were collected for the target region together with Wordstat demand/frequency indicators, and those indicators were used in analysing demand. Do not narrate unperformed exact-frequency procedures or operators as a pseudo-limitation when they are not a blocker to the sold result.

### Permanent hard failures

```text
ALICE_PRESENTED_AS_ADDITIONAL_OR_OPTIONAL_POST_CHECK
EIGHT_ALICE_DEEP_DIVES_PRESENTED_AS_TOTAL_ALICE_SCOPE
OVERALL_ALICE_COMPATIBILITY_VERDICT_MISSING_BEFORE_DEEP_DIVES
KWORK_GOAL_REFRAMED_AS_GENERIC_AUDIT_OR_ORDINARY_SEO
UNPERFORMED_FREQUENCY_PROCEDURE_NARRATED_AS_CLIENT_LIMITATION
RAW_75_QUERY_APPENDIX_PRESENT_IN_REPORT_01
POSITIVE_RESULT_EXPANDED_INTO_SMALL_NO_CHANGE_PAGE_CATALOGUE
```

### Permanent PASS additions

```text
ALICE_IS_CORE_PRODUCT_SURFACE = true
ALICE_COMPATIBILITY_VERDICT_VISIBLE_BEFORE_DEEP_DIVES = true
EIGHT_ALICE_CASES_IDENTIFIED_AS_DEEP_DIVES_NOT_TOTAL_SCOPE = true
UNPERFORMED_FREQUENCY_PROCEDURE_NARRATIVE_ABSENT = true
RAW_75_QUERY_APPENDIX_ABSENT = true
POSITIVE_SITE_RESULT_AGGREGATE = true
```
'''
if marker not in text:
    text = text.rstrip() + section + '\n'

# Final gate self-checks must be independent of historical layout.
assert 'Alice-based answers in Yandex are an additional selected verification layer' not in text
assert 'WHY ALICE WAS USED AFTER ORDINARY YANDEX' not in text
assert marker in text
assert 'EIGHT_ALICE_DEEP_DIVES_PRESENTED_AS_TOTAL_ALICE_SCOPE' in text
assert 'ALICE_COMPATIBILITY_VERDICT_VISIBLE_BEFORE_DEEP_DIVES = true' in text
assert 'UNPERFORMED_FREQUENCY_PROCEDURE_NARRATIVE_ABSENT = true' in text

GATE.write_text(text, encoding='utf-8')
print('STEP20_REPORT01_ALICE_NATIVE_RULES_PATCH_PASS', GATE)
