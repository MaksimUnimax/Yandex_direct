from pathlib import Path

ROOT = Path(__file__).resolve().parent
GATE = (ROOT / '../../STEP_20_REPORT_01_CUSTOMER_RESEARCH_REPORT_GATE.md').resolve()
text = GATE.read_text(encoding='utf-8')

text = text.replace('Updated: 2026-09-06', 'Updated: 2026-09-07')

# Remove older wording that made Alice look like an optional post-check.
text = text.replace(
    'Alice-based answers in Yandex are an additional selected verification layer. They do not replace the semantic-core analysis and must not be presented as the author of the research conclusion.',
    'Alice-based answers in Yandex are a core evidence surface of the sold Alice-native semantic rebuild. They do not replace the semantic-core analysis and must not be presented as the author of the research conclusion.'
)
text = text.replace('WHY ALICE WAS USED AFTER ORDINARY YANDEX', 'HOW ALICE WAS USED AS A CORE SURFACE OF THE KWORK')
text = text.replace('→ WHAT THE SELECTED ALICE-BASED CHECKS ADDED', '→ HOW THE CORE / PAGE DISTRIBUTION CORRESPONDS TO ALICE\n→ WHY SELECTED ALICE CASES WERE THEN USED FOR DEEPER REFINEMENT')

# Report 01 must describe completed work, not advertise procedures that were not performed.
old_frequency = '''### 13.3 Frequency work must be visible without inventing exact-frequency measurements

The report must explain that Wordstat collection was performed for the target region and that a numeric demand indicator accompanied the collected phrases. This is part of semantic-core work and must not disappear behind only logical/intent discussion.

At the same time, broad discovery collection must not be mislabeled as operator-exact frequency measurement for every unique phrase.

```text
DEMAND / FREQUENCY WORK VISIBLE = true
EXACT-FREQUENCY CLAIM WITHOUT EXACT-OPERATOR EVIDENCE = false
```'''
new_frequency = '''### 13.3 Frequency work must be visible in positive client language

Report №01 must state what was actually done: Wordstat demand was collected for the target region, search phrases were obtained together with their demand/frequency indicators, and those values were used when analysing the semantic core.

Do not turn the client narrative into a list of procedures that were not performed when their absence is not a real limitation of the sold result.

```text
DEMAND / FREQUENCY WORK VISIBLE = true
UNPERFORMED_PROCEDURE_NARRATIVE_USED_AS_PSEUDO_LIMITATION = false
```'''
if old_frequency in text:
    text = text.replace(old_frequency, new_frequency, 1)

old_alice_count = '''### 13.5 Alice case count must arise from the narrative, not appear as a floating number

Before the number of selected Alice checks is stated, the report must explain:

```text
WHY ALICE WAS USED AFTER ORDINARY YANDEX
HOW THE CANDIDATE THEMES WERE FORMED
HOW MANY CANDIDATES EXISTED
WHAT SELECTION QUESTION WAS APPLIED
THEN WHY THE FINAL SELECTED COUNT RESULTED
```

A naked `25 -> 8` transition without this causal bridge is FAIL.'''
new_alice_count = '''### 13.5 Alice case count must be subordinate to the overall Alice-compatibility verdict

Report №01 must first explain that checking the semantic core against Alice is a core part of the Kwork and state the site-wide conclusion about whether the current demand-to-page distribution corresponds to Alice output.

Only after that conclusion is clear may the report explain the bounded deep-dive set:

```text
ALICE IS A CORE PRODUCT SURFACE
→ OVERALL ALICE-COMPATIBILITY VERDICT FOR THE SITE
→ 25 THEMES WHERE A DEEPER CHECK COULD REFINE A DECISION
→ 8 DEEP-DIVE CASES = 6 DECISION-SENSITIVE + 2 CONTROLS
```

The eight cases must never read as the entire amount or entire value of the work with Alice.'''
if old_alice_count in text:
    text = text.replace(old_alice_count, new_alice_count, 1)

# Hard-fail additions are idempotent.
anchor = 'GENERATIVE / AI / NEURAL ALIAS USED INSTEAD OF AGREED ALICE VOCABULARY\n'
extra = ('ALICE_PRESENTED_AS_ADDITIONAL_OR_OPTIONAL_POST_CHECK\n'
         'EIGHT_ALICE_DEEP_DIVES_PRESENTED_AS_TOTAL_ALICE_SCOPE\n'
         'OVERALL_ALICE_COMPATIBILITY_VERDICT_MISSING_BEFORE_DEEP_DIVES\n'
         'UNPERFORMED_FREQUENCY_PROCEDURE_NARRATED_AS_CLIENT_LIMITATION\n')
if anchor in text and 'EIGHT_ALICE_DEEP_DIVES_PRESENTED_AS_TOTAL_ALICE_SCOPE' not in text:
    text = text.replace(anchor, anchor + extra, 1)

pass_anchor = 'ALICE_CUSTOMER_VOCABULARY_STABLE = true\n'
pass_extra = ('ALICE_IS_CORE_PRODUCT_SURFACE = true\n'
              'ALICE_COMPATIBILITY_VERDICT_VISIBLE_BEFORE_DEEP_DIVES = true\n'
              'EIGHT_ALICE_CASES_IDENTIFIED_AS_DEEP_DIVES_NOT_TOTAL_SCOPE = true\n'
              'UNPERFORMED_FREQUENCY_PROCEDURE_NARRATIVE_ABSENT = true\n')
if pass_anchor in text and 'ALICE_IS_CORE_PRODUCT_SURFACE = true' not in text:
    text = text.replace(pass_anchor, pass_anchor + pass_extra, 1)

# Final self-checks: the gate itself must no longer teach the wrong narrative.
assert 'Alice-based answers in Yandex are an additional selected verification layer' not in text
assert 'WHY ALICE WAS USED AFTER ORDINARY YANDEX' not in text
assert 'EIGHT_ALICE_DEEP_DIVES_PRESENTED_AS_TOTAL_ALICE_SCOPE' in text
assert 'UNPERFORMED_FREQUENCY_PROCEDURE_NARRATIVE_ABSENT = true' in text

GATE.write_text(text, encoding='utf-8')
print('STEP20_REPORT01_ALICE_NATIVE_RULES_PATCH_PASS', GATE)
