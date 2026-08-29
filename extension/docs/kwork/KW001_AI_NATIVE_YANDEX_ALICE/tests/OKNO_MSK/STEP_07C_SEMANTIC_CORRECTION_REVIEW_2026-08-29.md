# KW-001 / OKNO-MSK — STEP 07C SEMANTIC CORRECTION REVIEW

Date: 2026-08-29  
Status: **CORRECTION CANDIDATE READY / OWNER REVIEW PENDING / NOT ACCEPTED AS FINAL**

## 1. Why this correction was required

The historical Step 07B data-accounting layer was valid, but its semantic PASS was reopened after a fresh external-methodology audit found a default-KEEP defect.

Historical behavior effectively allowed many result phrases to become KEEP when no known exclusion/review dictionary matched. That made KEEP depend on dictionary completeness rather than positive evidence of user need + business/site fit.

The correction therefore preserves all historical data/provenance while replacing the semantic decision layer.

Authority for reopening the step:

`STEP_07B_POST_AUDIT_CORRECTION_REQUIRED_2026-08-29.md`

## 2. Unchanged trustworthy accounting

The correction reuses the same complete source corpus and does not recollect Wordstat.

```text
source occurrences = 2965
exact phrase keys = 2840
provider requests during correction = 0
provider cost during correction = 0 RUB
```

All occurrence-level provenance remains preserved.

## 3. Historical classification versus corrected candidate

Historical Step 07B:

```text
KEEP = 1760
REVIEW = 749
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 31
TOTAL = 2840
```

Current Step 07C correction candidate:

```text
KEEP = 1388
REVIEW = 1118
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 34
TOTAL = 2840
```

Transitions from historical status:

```text
KEEP -> KEEP = 1388
KEEP -> REVIEW = 369
KEEP -> EXCLUDE_MECHANICAL = 3
REVIEW -> REVIEW = 749
EXCLUDE_SCOPE -> EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT -> EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL -> EXCLUDE_MECHANICAL = 31
historical non-KEEP promoted to KEEP = 0
```

The correction is intentionally conservative: uncertainty is moved to REVIEW rather than silently removed or accepted.

## 4. Corrected decision contract

Current candidate enforces:

```text
KEEP requires a POSITIVE_* reason tied to an accepted Step-01 business/site family
default KEEP fallthrough = false
low frequency alone never excludes a phrase
associations are never auto-promoted to KEEP
historical REVIEW/EXCLUDE rows are not promoted upward in this correction
uncertain intent/business/page boundaries -> REVIEW
safe explicit scope/irrelevance/mechanical exclusions remain explicit
```

Positive KEEP families are grounded in the accepted Step-01 site model: PVC/REHAU windows, PVC doors, balcony/loggia glazing, veranda/terrace/gazebo glazing, aluminium glazing, installation, repair, price/conversion, financing, manufacturer/production, the existing window-selection guide, panoramic-window product demand and private-house window demand.

## 5. Semantic correction classes added after the external audit

The correction explicitly catches/demotes material classes that the historical default-KEEP logic missed, including:

```text
ambiguous numeric/query fragments
navigation/entity/domain intent
DIY/procedural intent
technical/informational intent
brand/material comparison intent
components/accessories and fittings-brand boundaries
heating/adjacent-system intent
architecture/design/inspiration intent
panoramic real-estate/inspiration intent
PVC-door subtype uncertainty
private-house adjacent/regulatory tasks
balcony regulatory/negated intent
installation-adjacent/job intent
repair navigation/entity/DIY/fragment intent
demolition as an unproven service boundary
REHAU diagnostic/repair intent found inside product acquisition
window state/context fragments
incomplete tail fragments such as queries ending in `без`
```

Examples corrected from historical false/unsafe KEEP include:

```text
1 установка пластиковых окон -> EXCLUDE_MECHANICAL
6 6 с панорамными окнами -> REVIEW
rehau окна 2 -> REVIEW
алюминиевые окна 2 -> REVIEW
rehau окна анадырский проезд д 47 -> REVIEW
rehau микролифт для окна -> REVIEW
окна rehau сайт -> REVIEW
окна rehau официальный -> REVIEW
окна rehau сравнение -> REVIEW
окна rehau внутри на стекле конденсат починить -> REVIEW
ремонт сетки для пластиковых окон -> REVIEW
демонтаж алюминиевых окон -> REVIEW
демонтаж остекления балкона -> REVIEW
квартира с панорамными окнами -> REVIEW
панорамные окна в лесу / на море / в здании -> REVIEW
французские окна название / это какие -> REVIEW
окна в рассрочку без -> EXCLUDE_MECHANICAL
```

## 6. QA evidence

The correction was not accepted on arithmetic alone.

It went through four semantic saturation passes. Intermediate runs failed when QA exposed real defects, including:

```text
Russian inflection mismatch: `окон` vs literal `окн`
window-state word-order miss: `окно пластиковое закрыто`
```

The current candidate has:

```text
builder QA cases = 21
builder QA failures = 0
expanded semantic QA cases = 72
expanded semantic QA failures = 0
manual semantic saturation passes = 4
```

The expanded QA intentionally contains both MUST_KEEP and MUST_NOT_KEEP examples across the main business families and the previously observed false-KEEP classes.

## 7. Non-exact duplicate handling

Exact-string accounting remains unchanged, but Step 07C additionally surfaces non-obvious duplicate candidates.

```text
non-exact duplicate candidate groups = 9
candidate rows = 18
automatic non-exact merges = 0
```

Examples include spelling/order variants such as REHAU/Рехау and Provedal/Проведал. These are only candidates. They are not silently merged because lexical similarity alone does not prove identical search intent/page ownership.

Artifact:

`STEP_07C_NONEXACT_DUPLICATE_CANDIDATES.tsv`

## 8. Current artifacts

```text
STEP_07C_SEMANTIC_CORRECTION_BUILD.py
STEP_07C_SEMANTIC_CORRECTION_RUN.py
STEP_07C_SEMANTIC_CORRECTION_WORKING.tsv
STEP_07C_SEMANTIC_CORRECTION_OCCURRENCES.tsv
STEP_07C_NONEXACT_DUPLICATE_CANDIDATES.tsv
STEP_07C_SEMANTIC_QA_CASES.tsv
STEP_07C_SEMANTIC_QA_CASES_V2.tsv
STEP_07C_SEMANTIC_CORRECTION_SUMMARY.json
```

Current verified hashes from the generated summary:

```text
corrected working TSV SHA-256 = 753e2875d0ac4090ae4db6df4e2ecc162d6598948adeecca011b2dbdb8b60bbb
corrected occurrences TSV SHA-256 = 8b89585f479d6c3d42c45fcccdfe2eacebabc54adef18eb59b992628b4dff26e
non-exact duplicate candidates SHA-256 = f68626523ab007b58f71a4c18630547dbffa85043ee2a41c532b16ed6628bb7b
expanded semantic QA SHA-256 = 0fa73aee1508cd14190febdb0b5f4ea7eebfb8469db8d672771058404b20d324
```

## 9. Methodology basis used for the correction

The correction applies the conclusions of the owner-requested fresh external audit rather than treating the project script as proof of its own method.

Current public references used in that audit:

- Yandex Wordstat: https://yandex.ru/support2/wordstat/ru/interface/new
- Yandex Webmaster targeting/user-needs guidance: https://yandex.ru/support/webmaster/en/recommendations/targeting
- Topvisor semantic-core cleanup / non-obvious duplicates: https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/
- Rush Analytics semantic preparation / clustering: https://www.rush-analytics.ru/blog/chto-takoe-klasterizacziya-zaprosov
- Ahrefs keyword intent: https://ahrefs.com/blog/keyword-intent/
- Semrush keyword clustering: https://www.semrush.com/blog/keyword-clustering/

Project-specific five-status classification remains an owner-approved project control, not an external industry standard.

## 10. Important remaining limits

This correction candidate is materially stronger than historical Step 07B, but it is **not being self-accepted as final**.

Still true:

```text
REVIEW is intentionally large and must not be treated as rejected
KEEP does not imply one landing page per phrase
KEEP does not prove final SERP/page ownership
non-exact duplicate candidates are not yet resolved
ordinary Yandex Search has not yet been used to resolve mixed intent/page boundaries
page architecture is not complete
AI evidence has not been used
```

The candidate is deliberately conservative: when positive business relevance is not established strongly enough, the phrase remains REVIEW for later Search evidence instead of being forced into KEEP/EXCLUDE.

## 11. Candidate verdict

```text
ROW_LEVEL_DATA_ACCOUNTING = PASS
PROVENANCE_RECONCILIATION = PASS
DEFAULT_KEEP_DEFECT = CORRECTED
KEEP_POSITIVE_EVIDENCE_GATE = PASS
LOW_FREQUENCY_ONLY_EXCLUSION = 0
ASSOCIATION_AUTO_KEEP = false
SEMANTIC_QA = PASS_AS_CANDIDATE
NONEXACT_DUPLICATES_AUTO_MERGED = 0
CORRECTION_CANDIDATE_READY = true
OWNER_REVIEW_PENDING = true
ROW_LEVEL_CLEANUP_FINAL_ACCEPTANCE = false
NEXT_STEP_ALLOWED = false
```

No next workflow step is authorized by this review file. The owner and assistant should inspect this corrected candidate and decide whether to accept it, request another correction, or change the next-step method.
