from pathlib import Path

ROOT = Path(__file__).resolve().parent
GATE = (ROOT / '../../STEP_20_REPORT_01_CUSTOMER_RESEARCH_REPORT_GATE.md').resolve()
text = GATE.read_text(encoding='utf-8')

marker = '## 13. Superseding owner corrections — final Report №01 presentation contract'
addition = r'''

## 13. Superseding owner corrections — final Report №01 presentation contract

The rules in this section supersede any older Report №01 wording that conflicts with them.

### 13.1 Site URL belongs in the title

The customer must see the researched site directly in the title. A project name without the site URL is not sufficient.

```text
REPORT_01_TITLE_CONTAINS_RESEARCHED_SITE_URL = true
```

### 13.2 Customer language uses search phrases, not storage-row vocabulary

Internal storage terminology such as `row`, `record`, field names or wire labels must not leak into the non-specialist report when the customer-facing meaning is simply a search phrase or a demand indicator.

```text
INTERNAL: 2415 rows
CUSTOMER: 2415 search phrases

INTERNAL: Wordstat field count
CUSTOMER: numeric demand / frequency indicator returned with the phrase
```

Report №01 must not expose an English internal field name such as `count`.

### 13.3 Frequency work must be visible without inventing exact-frequency measurements

The report must explain that Wordstat collection was performed for the target region and that a numeric demand indicator accompanied the collected phrases. This is part of semantic-core work and must not disappear behind only logical/intent discussion.

At the same time, broad discovery collection must not be mislabeled as operator-exact frequency measurement for every unique phrase.

```text
DEMAND / FREQUENCY WORK VISIBLE = true
EXACT-FREQUENCY CLAIM WITHOUT EXACT-OPERATOR EVIDENCE = false
```

### 13.4 Do not claim that a full rebuild was performed when the research conclusion is that it is unnecessary

Report №01 must distinguish:

```text
COLLECTED / ANALYZED RESEARCH CORE FOR THE JOB
!=
FULL REBUILD OF THE SITE'S EXISTING CORE / STRUCTURE
```

When the research shows that the existing distribution is already broadly correct, the customer-facing conclusion must say that a full rebuild is not required and that only targeted corrections are justified.

### 13.5 Alice case count must arise from the narrative, not appear as a floating number

Before the number of selected Alice checks is stated, the report must explain:

```text
WHY ALICE WAS USED AFTER ORDINARY YANDEX
HOW THE CANDIDATE THEMES WERE FORMED
HOW MANY CANDIDATES EXISTED
WHAT SELECTION QUESTION WAS APPLIED
THEN WHY THE FINAL SELECTED COUNT RESULTED
```

A naked `25 -> 8` transition without this causal bridge is FAIL.

### 13.6 Positive site result must be summarized, not turned into a catalogue of a few correct pages

For a non-specialist customer, Report №01 must not enumerate several already-correct pages merely to prove that positive checks existed. Such a list can falsely imply that only those pages were studied.

The main report should state the site-wide conclusion in aggregate form:

```text
A MATERIAL PART OF THE EXISTING DEMAND-TO-PAGE DISTRIBUTION IS ALREADY CORRECT
THEREFORE MASS RESTRUCTURING IS NOT REQUIRED
WORK SHOULD FOCUS ON THE IDENTIFIED TARGETED IMPROVEMENTS
```

Concrete URLs belong in ready recommendations or where a specific example is necessary to understand a material decision, not in a no-change catalogue.

### 13.7 The raw 75-query appendix is forbidden in Report №01

The 75 exact ordinary-Yandex observations remain preserved in internal evidence authorities. They must not be dumped into the customer report as a raw appendix.

Report №01 may state that 75 targeted checks were performed and explain why they were selected, but the raw observation register belongs to internal evidence / specialist materials.

This supersedes the older `SUPPORTING APPENDIX` recommendation in this gate for the 75-query Search register.

```text
RAW_75_QUERY_APPENDIX_IN_REPORT_01 = FAIL
INTERNAL_75_QUERY_EVIDENCE_PRESERVED = true
```

### 13.8 Alice vocabulary for Report №01

The agreed customer-facing concept is `выдача Алисы`. Do not rotate between `AI`, `ИИ`, `generative`, `neural`, technical provider labels or other aliases in Report №01.

Technical names may remain in provenance/evidence files, but the customer report must use one stable ordinary-language name.

### 13.9 Additional hard FAILs

```text
SITE_URL_ABSENT_FROM_REPORT01_TITLE
RAW_STORAGE_ROW_TERM_USED_WHERE_CUSTOMER_MEANS_SEARCH_PHRASE
ENGLISH_INTERNAL_WORDSTAT_FIELD_NAME_EXPOSED
FREQUENCY_WORK_MISSING_FROM_WORKFLOW_NARRATIVE
FULL_REBUILD_CLAIMED_AS COMPLETED WHEN RESEARCH SAYS FULL REBUILD IS UNNECESSARY
ALICE_FINAL_CASE_COUNT APPEARS BEFORE CANDIDATE / SELECTION LOGIC
POSITIVE_RESULT_EXPANDED_INTO SMALL CATALOGUE OF ALREADY-CORRECT PAGES
RAW_75_QUERY_APPENDIX PRESENT IN REPORT_01
GENERATIVE / AI / NEURAL ALIAS USED INSTEAD OF AGREED ALICE VOCABULARY
```

### 13.10 Updated PASS additions

```text
SITE_URL_VISIBLE_IN_TITLE = true
SEARCH_PHRASE_COUNTS_WRITTEN_AS PHRASES FOR CUSTOMER = true
WORDSTAT_DEMAND_INDICATOR_EXPLAINED_IN RUSSIAN = true
FREQUENCY_WORK_VISIBLE_WITHOUT FALSE EXACTNESS = true
FULL_REBUILD_NOT_CLAIMED_WHEN UNNECESSARY = true
ALICE_SELECTION_CAUSAL_BRIDGE_VISIBLE = true
POSITIVE_SITE_RESULT_SUMMARIZED WITHOUT NO-CHANGE PAGE CATALOGUE = true
RAW_75_QUERY_APPENDIX_ABSENT = true
ALICE_CUSTOMER_VOCABULARY_STABLE = true
```
'''

if marker not in text:
    text = text.rstrip() + addition + '\n'

GATE.write_text(text, encoding='utf-8')
print('STEP20_REPORT01_FINAL_RULES_PATCH_PASS', GATE)
