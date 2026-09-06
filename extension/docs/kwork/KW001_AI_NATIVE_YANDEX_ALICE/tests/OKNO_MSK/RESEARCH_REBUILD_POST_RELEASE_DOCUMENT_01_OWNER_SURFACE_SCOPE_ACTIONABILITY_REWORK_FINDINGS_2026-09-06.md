# OKNO_MSK — Document №01 owner rework: result-surface wording, Alice scope and actionability

Date: 2026-09-06

Status: **OWNER_REVIEW_REOPENED__REWORK_REQUIRED**

Current document: **01**

Document №02: **NOT STARTED**

Document №03: **NOT STARTED**

New provider calls authorized: **false**

New provider calls required for this correction: **0**

## 1. Why the previous 12-page owner-report version is reopened

The previous version remains analytically grounded but fails the owner-facing product contract in five material ways discovered during owner review.

The defects are not treated as isolated wording edits. They expose a client-materialization failure class and therefore require correction of the client-report source/generator, QA and Level-1 Step-20 controls before the document can return to owner review.

## 2. Owner finding 1 — title and terminology describe “search” when the compared client-visible result is “выдача”

The report must compare the two result surfaces in the owner-approved client wording.

Required client-facing title wording:

`ОКНО МОСКВА — исследование спроса в Яндексе: обычная выдача и выдача Алисы`

Do not replace `выдача` with `поиск` where the text is describing the result/output seen for a query.

## 3. Owner finding 2 — the eight Alice cases were incorrectly framed as “not the whole research volume”

This is materially misleading.

The Alice stage had one complete approved selected set of **8 cases**. Those eight cases are the complete Alice verification scope actually executed for the job.

The selection was not an arbitrary quota. Before selection, **25 decision candidates were reviewed**. The corrected Step-15 V2 selection retained:

- **6 diagnostic cases** where Alice could materially change, refine or make safer a real page/content decision;
- **2 stable control cases** where ordinary Yandex already gave a clear result and Alice was used to check that it did not spuriously overturn that clear conclusion.

Final Step-15 accounting:

- reviewed: **25**;
- selected for Alice: **8**;
- rejected as not adding sufficient distinct decision value: **16**;
- held: **1**.

The 8 selected cases cover distinct decision questions rather than repeating near-identical phrases. The selection was considered sufficient for the declared Alice verification purpose because it covered the material high-value decision types plus stable controls; additional repetitive cases were not required merely to increase the number.

Client-facing explanation must communicate sufficiency and selection logic in ordinary language. It must not claim statistical representativeness of all site demand and must not imply that the Alice stage was incomplete.

## 4. Exact eight Alice queries and why each was selected

1. `панорамные алюминиевые окна` — check whether Alice shifts the answer away from the commercial aluminium-windows page toward a broader explanatory panoramic page.
2. `алюминиевые окна для веранды` — check whether Alice keeps the veranda use-case as the main user task or narrows it to a material/mechanism page.
3. `панорамное остекление балкона` — stable control: ordinary Yandex strongly supported the specialist balcony page; Alice checks whether that clear result remains stable.
4. `установка подоконника на пластиковые окна` — check a mixed product/service/how-to task and whether Alice changes which type of page should answer it.
5. `французские панорамные окна` — check whether Alice preserves a distinct French-window task rather than collapsing it into generic panoramic glazing.
6. `замена окна на пластиковое цена москва` — stable transactional control: ordinary Yandex clearly supported replacement intent; Alice checks whether that clear commercial task remains stable.
7. `как открыть пластиковое окно` — check an ambiguous formulation that could mean troubleshooting, emergency opening or adjustment.
8. `лучшие пластиковые окна` — check whether Alice preserves the distinction between a “best windows” comparison, a broad choice guide and narrower profile/manufacturer comparisons.

These reasons come from the accepted Step-15 V2 selection authority and the rebuilt Alice causal ledger. They must be translated into normal owner language, not internal labels.

## 5. Owner finding 3 — vague words such as “весь массив” are forbidden when exact numbers exist

The report must use accepted exact counts and explain the relationship between them.

Current canonical counts relevant to the client narrative:

- **2,840** accepted search phrases in the final semantic master;
- **2,313** phrases assigned to an accepted page/task result;
- **168** canonical user-task / structural units;
- **75** preserved exact ordinary-Yandex result observations;
- **25** candidates reviewed for the Alice selection;
- **8** complete selected Alice cases;
- **34** material action/decision rows in the implementation authority.

The report must not present these as a disconnected list. It must explain which number is the full accepted semantic scope, which is an assigned subset, which is a targeted ordinary-Yandex validation layer, which is the candidate pool for Alice, which is the complete selected Alice scope, and which is the final material decision/action universe.

## 6. Owner finding 4 — the 21-item page-routing catalogue should not occupy the main client report when it does not create a client action

The section previously titled `Как распределены основные группы поискового спроса` is not acceptable as a long 21-item main-report dump if most entries only restate already-correct routing and require no site change.

Required correction:

- remove the exhaustive 21-item routing catalogue from the main client narrative;
- keep the underlying mapping in canonical structured evidence / workbook / specialist reference where it remains useful;
- summarize only the material positive conclusion that existing pages already cover the validated themes where no change is required;
- surface a detailed no-change case in the main report only when it explains why an apparently tempting change would be wasteful/harmful or when it is needed to understand a material recommendation;
- main report must concentrate on **what to change, why, where, what to preserve, expected result and how to check**.

The report must not rewrite the entire site merely to prove that it was reviewed.

## 7. Owner finding 5 — client-facing name is only “Алиса”

For this client report, the canonical client-facing surface name is:

`Алиса`

Do not rotate among:

- `ИИ`;
- `AI`;
- `нейросетевой поиск`;
- `генеративный поиск`;
- `Алиса/ИИ`;
- other technical aliases.

Internal evidence files may retain their technical names. The client-facing report must consistently say `Алиса` so one tested surface is not presented as several different systems.

## 8. Required rewrite structure for Document №01

The next source/generator version must be rebuilt around the owner decision path:

1. **Title:** `ОКНО МОСКВА — исследование спроса в Яндексе: обычная выдача и выдача Алисы`.
2. **No prominent date on the first screen.**
3. **What was done, with exact numbers:** explain the 2,840 accepted phrases, 2,313 assigned phrases, 168 user tasks/units and how that led to validation in Yandex.
4. **Why 75 ordinary-Yandex observations:** explain that these are targeted exact-query validations used where result evidence was needed, not the total number of phrases studied.
5. **Why exactly 8 Alice cases and why this is sufficient:** explain 25 reviewed candidates → 6 decision-sensitive cases + 2 stable controls → 8 complete Alice cases; explain non-redundancy and purpose in ordinary owner language.
6. **What ordinary Yandex and Alice changed/confirmed:** show only the material cases needed to explain real recommendations or valuable retained decisions.
7. **What must be changed on the site:** each recommendation must show finding → why it matters → exact change → why this change → location → what to preserve → target result → acceptance check.
8. **What is already correct:** concise positive summary, not a 21-item routing dump.
9. **What specific company facts are still needed:** only concrete inputs that unlock a real next improvement.
10. **Priority / handoff:** what to implement first and why.

## 9. QA regressions required before return to owner review

Document №01 cannot return to owner review unless independent QA verifies:

- title contains `обычная выдача` and `выдача Алисы`;
- title/client prose does not substitute `поиск` where result-surface wording is intended;
- client-facing Alice label is consistently `Алиса` and does not rotate through technical aliases;
- the 8 Alice cases are described as the complete selected Alice scope for the job, not as an incomplete research fragment;
- the report explains 25 reviewed → 8 selected and the six decision-sensitive + two stable-control design in ordinary language;
- exact canonical numbers are used where available; vague `весь массив` wording is absent;
- the relationship among 2,840 / 2,313 / 168 / 75 / 25 / 8 / 34 is understandable;
- no exhaustive 21-item no-action routing catalogue remains in the main client narrative;
- main-report detailed items are action/decision-relevant;
- every recommended change explains why;
- Document №02 and №03 remain untouched.

## 10. Current status

`DOCUMENT_01_ANALYST_RECHECK = REOPENED__REWORK_REQUIRED`

`DOCUMENT_01_OWNER_REVIEW = REWORK_REQUIRED`

`DOCUMENT_02_OWNER_REVIEW = PENDING__NOT_STARTED`

`DOCUMENT_03_OWNER_REVIEW = PENDING__NOT_STARTED`

`NEXT_ACTION = REBUILD_DOCUMENT_01_FROM_CANONICAL_EVIDENCE_WITH_OWNER_SURFACE_SCOPE_ACTIONABILITY_RULES`
