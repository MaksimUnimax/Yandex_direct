# OKNO_MSK — Document №01 owner surface/scope/actionability remote readback

Date: 2026-09-06

Status: **PASS__OWNER_REVIEW_PENDING**

Current document: **01**

Document №02: **NOT STARTED / UNTOUCHED**

Document №03: **NOT STARTED / UNTOUCHED**

New provider calls during this rebuild: **0**

## 1. Persisted physical release

Owner-ready Document №01 was deterministically rebuilt from the corrected Markdown source, converted to DOCX/PDF, independently recipient-tested, committed and pushed to the active roadmap branch.

Physical persistence commit:

`6d88d793ed2ab7cadc4fddae668194f89d1a62d4`

Successful rebuild / QA workflow run:

`34028094643`

The workflow completed all material steps with `success`, including:

- freeze check proving Document №02 and №03 stayed byte-identical to their prior accepted artifacts;
- deterministic Document №01 DOCX build;
- PDF conversion;
- independent recipient QA;
- persistence of Document №01 physical files only;
- post-commit confirmation that no `02_OKNO` or `03_OKNO` file changed.

## 2. Remote readback of Document №01

Remote source:

`OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05/sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md`

- size: `47,941` bytes;
- SHA-256: `105ff37bd98afec875986b79c8d9220b074bc6118e40a61d3190ce1357702742`.

Remote editable DOCX:

`OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05/editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.docx`

- size: `52,370` bytes;
- SHA-256: `795de08bc9757e74c12c3a5bc7d5be42e40532071bc17f09911854c3a4c10cb3`.

Remote recipient PDF:

`OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.pdf`

- size: `205,594` bytes;
- SHA-256: `917c9910108668aaee008a973c94b0a87802ee9e4ca06b5b1522251a60f601ef`;
- pages: `10`;
- PDF openability / non-encryption / render QA: `10_OF_10_PAGES_PASS`.

## 3. Owner corrections verified in the persisted source

Exact client title is now:

`ОКНО МОСКВА — исследование спроса в Яндексе: обычная выдача и выдача Алисы`

Client-facing terminology uses `выдача` for the observed Yandex result surface and uses one client-facing name for the additional surface: `Алиса`.

Forbidden client-facing aliases checked absent from the corrected report include:

- `генеративный поиск`;
- `нейросетевой поиск`;
- `Алиса/ИИ`;
- `AI` as a client label;
- vague scope wording `весь массив`.

## 4. Scope chain verified

The report now explains the research with exact accepted counts and their relationship:

`2,840 accepted queries`
→ `2,313 assigned queries`
→ `168 user tasks / structural units`
→ `75 exact ordinary-Yandex output observations`
→ `25 Alice selection candidates reviewed`
→ `8 complete Alice cases`
→ `34 material results / decisions`.

The 75 ordinary-Yandex observations are explicitly explained as targeted exact-query validation inside the larger 2,840-query research scope, not as the total research volume.

## 5. Alice selection and sufficiency verified

The corrected client report states that the eight Alice checks are the **complete executed Alice verification stage for this job**, not an incomplete fragment.

Selection accounting is explicit:

- `25` candidates reviewed;
- `6` decision-sensitive cases selected;
- `2` stable control cases selected;
- `8` total complete Alice checks;
- `16` rejected because they did not add a distinct decision question;
- `1` held.

The report explains why this is sufficient for the declared purpose: the selected set covers materially different decision questions where Alice could affect the conclusion, plus stable controls, without adding near-duplicate checks merely to inflate the count.

## 6. Main-report actionability verified

The prior exhaustive 21-item page-routing catalogue was removed from the main client narrative.

The exhaustive 34-result internal/result dump was also removed from the main narrative while the structured 34-result authority remains preserved in the project.

The main report now contains:

- `7` ready page improvements, each with finding → why it matters → change → location → what to preserve → expected result → acceptance check;
- a concise positive summary of already-correct site decisions instead of a no-action catalogue;
- `2` concrete company facts needed before two additional improvements;
- the full appendix of `75` exact ordinary-Yandex observations;
- all `8` Alice checks with selection reason, observed result and effect on the site decision.

## 7. Document №02 and №03 freeze proof

Document №02 remained unchanged:

- PDF SHA-256: `3f589c03bc44f5127aa9f93697e3120729149f8f6985c11fa921424c867ec61a`;
- editable DOCX SHA-256: `4c9f4aeded8b23c8ed7741d10a989ba79696d8fac3fa10a48de11cdd01df2d3c`;
- source Markdown SHA-256: `764f697fb5ad7ca6f5982b000b6053652460f854c8bb7b937a2041688fff80d8`.

Document №03 remained unchanged:

- Markdown SHA-256: `d5c90cf187041e975f17d03a2be138eff0b6a06bfe1b7d395a3b24547edc62b0`.

Workflow result: `DOCUMENT_02_03_UNTOUCHED_PASS`.

## 8. Final state

`DOCUMENT_01_ANALYST_RECHECK = PASS`

`DOCUMENT_01_OWNER_REVIEW = PENDING__AWAITING_OWNER_RECHECK`

`DOCUMENT_02_OWNER_REVIEW = PENDING__NOT_STARTED`

`DOCUMENT_03_OWNER_REVIEW = PENDING__NOT_STARTED`

`NEW_PROVIDER_CALLS = 0`

`NEXT_ACTION = OWNER_REVIEW_CORRECTED_DOCUMENT_01`

Do not start Document №02 or Document №03 until Document №01 is accepted by the owner.