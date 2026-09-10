# OKNO_MSK — MK02-only Phase 5 QA

Дата проверки: **2026-09-10**  
Режим: **replay/projection по сохранённым доказательствам; новые provider calls = 0**  
Финальный итог: **G0–G15 PASS**

Независимый валидатор `validate_mk02_rehearsal.py` завершился статусом **PASS: 21/21**, способен завершаться ненулевым кодом и не является частью генераторов данных или XLSX. Машинный протокол: `MK02_INDEPENDENT_QA_2026-09-10.json`.

## G0 — Scope / Yandex-only — PASS

Заказ ограничен существующим `https://okno-msk.ru/`, Москвой и MK02. В семантическом входе 0 из 16 Step5A-фраз; Google/AI/Alice/Neuro evidence и результаты отдельных MK03/MK04/MK06 не используются; CREATE/SPLIT/MERGE/redirect/delete = 0.

## G1 — Acquisition / persistence — PASS

Использованы только сохранённые Wordstat, ordinary Yandex Search и публичные page/site snapshots с их исходными locator/date/region/surface. Новых обращений = 0. Полезные source authorities и hashes перечислены в `SOURCE_AUTHORITY_AUDIT.md` и manifests.

## G2 — Semantic accounting — PASS

`2 185 WORKING + 187 REVIEW/UNCERTAIN + 468 EXCLUDED = 2 840`. Source/output exact phrase set delta = 0; unique source keys = 2 840; duplicate current keys = 0; silent loss = 0. Review и exclusions остаются в полном universe.

## G3 — Semantic decision — PASS

Каждая из 2 840 строк имеет явное принятое состояние; default KEEP = 0. Частотность не используется как самостоятельная причина релевантности, seeds не активируются автоматически, uncertainty не заменена решением.

## G4 — Semantic Search evidence — PASS

Повторно использованы 85 сохранённых Search observations: 69 ownership + 16 competing-page. Query/region/surface/time и bounded meaning сохранены; новых Search calls = 0; Search absence не использована как site absence.

## G5 — Clustering semantic — PASS

59 групп полностью согласованы: 54 рабочие и 5 outside. Working-group membership = 2 185; whole-task/intent граница сохранена; URL-архитектура не использована как причина объединения фраз.

## G6 — Page-ownership accounting and role — PASS after method correction

Active semantic keys = ownership map keys = 2 185; silent drops = 0. Legacy downstream `ASSIGNED` = 2 319, но 134 legacy-only nonactive keys не активированы, legacy-only activations = 0. `OWNER_EXISTING` с пустым target = 0; unresolved rows с выдуманным target = 0. В client map раздельны exact owner, family owner, supporting page и observed Search URL.

Репетиция выявила дефект метода: старый downstream flag мог ошибочно стать authority активного множества. Добавлено правило `CURRENT ACCEPTED SEMANTIC PRODUCT STATE > LEGACY DOWNSTREAM ASSIGNMENT / ACTIVATION FLAG`; обновлены `GENERAL_RULES.md`, Step 10, `ERRORS_AND_LESSONS.md`, `QA_AND_RELEASE.md`, `EXECUTION_ROADMAP.md`; перестроены все Steps 10–15.

## G7 — Page-ownership coherence — PASS

Проверены 160 активных units, 59 candidate ledgers и 105 candidate comparisons. На 2 185 строках: `OWNER_EXISTING` 1 647; `NO_SUITABLE_EXISTING_PAGE` 518; outside ownership 14; unresolved 6. Family owner заполнен для 1 882 строк, supporting page — для 1 015. Representative query не заменяет full-member evidence.

## G8 — Structural-action evidence — PASS

160/160 active units имеют diagnosis/evidence locator/meaning, current evidence state и real-site-change state. Action classes: KEEP 70; semantic mapping 45; DEFER 19; NO_CHANGE 18; CONTENT_CHANGE 8. CREATE/SPLIT/MERGE/redirect/delete = 0; действие не используется как собственное доказательство.

## G9 — Competing-page / cannibalization claim — PASS

21 case family, 199 effective page-pair observations. Product mode = `BASE_PUBLIC_EVIDENCE_MODE`; private history reused = 0 / unavailable; unsupported cannibalization labels, historical claims, harm claims and destructive authorizations = 0.

## G10 — Current-site topology / target architecture — PASS

Current nodes = 2 683, включая независимый current-minus-upstream набор 2 624: material 21, non-material-with-reason 1 932, outside-with-reason 671, unclassified 0. Target units = 160; current/target delta rows = 21 page + 14 unique relation = 35. Literal links: 8 unique present, 6 absent; planned relation не выдана за implemented link. AI evidence = 0.

## G11 — Implementation-spec completeness — PASS after correction

47 packages: READY 3; pending business detail 1; pending technical detail 0; pending placement/context 10; recheck 4; semantic mapping only 19; no site change 9; HOLD 1. Все 3 READY имеют 12 обязательных полей, exact location, acceptance и preservation; placeholders = 0; generic clones = 0.

Первый A–U прогон отклонил четыре исходных READY с альтернативным местом «X или Y» и дублированием why/change. Root cause: полнота полей была ошибочно принята за разрешённость решения. Все четыре строки понижены до pending placement/context, клиентские виды/XLSX перестроены; duplicate why/change устранён. Финально ambiguous READY = 0 и duplicate why/change = 0.

## G12 — Priority / scheduling honesty — PASS

В 47/47 пакетах отсутствуют выдуманные owner/effort/capacity/timeline/business priority/uplift. Нумерация объявлена идентификатором учёта, а не очередностью производства.

## G13 — Client deliverable data / cross-view consistency — PASS

Одна цепочка authorities питает 13 XLSX-листов и три narrative views. Cross-view counts совпадают: universe 2 840; core 2 185; map 2 185; target units 160; delta 35; packages 47; clarification/no-change/HOLD 44; relations 14; READY acceptance 3. Stale 7-READY представлений не осталось.

## G14 — Recipient language / report quality — PASS

Клиентские заголовки/поля русские; internal Stage/Step/action/QA IDs и filenames в XLSX = 0. Аналитический слой отвечает «что показало исследование», план начинается с действий и отвечает «что/почему/где/как/что уточнить/как принять». Report №02 failure classes A–U проверены поштучно; failure count = 0 (`OWNER_FAILURE_CLASS_A_U_CHECKS_2026-09-10.json`).

| Класс | Фактическая проверка | Итог |
|---|---|---|
| A | client internal tokens | 0 / PASS |
| B | 3 READY = 3 уникальных exact changes | PASS |
| C | ambiguous READY; 4 строки понижены | 0 / PASS |
| D | READY с оставленным анализом/уточнением | 0 / PASS |
| E | READY placeholder/TODO | 0 / PASS |
| F | invented schedule fields | 0 / PASS |
| G | 14 visible pairs = 14 unique | PASS |
| H | Wordstat/Yandex/public-site sources и ограничения названы | PASS |
| I | site snapshot 2026-09-02 не перенесён на факт рейтинга 2024 | PASS |
| J | report-time provider calls | 0 / PASS |
| K | process narration in client views | 0 / PASS |
| L | READY заменены отрицательными pseudo-actions | 0 / PASS |
| M | UI/browser filler | 0 / PASS |
| N | duplicate why/change in READY | 0 / PASS |
| O | empty TOC/furniture | 0 / PASS |
| P | orphan headings | 0 / PASS |
| Q | profession-branded identity | 0 / PASS |
| R | topic→page meaning explained | PASS |
| S | page-pair meaning explained | PASS |
| T | standalone defensive preservation section | 0 / PASS |
| U | implementation plan is action-first | PASS |

## G15 — Physical / recipient / persistence — PASS

Physical/recipient части прошли: XLSX открывается и повторно импортируется; 13/13 листов отрисованы и визуально просмотрены; formula errors before/after import = 0; bytes = 565 964; SHA-256 = `acfa7f8337de43fe1499dc002aa2b1c42aee1057e1c2399b609faaf6844a6b69`. Recipient review = PASS. Исправленный QA/data/XLSX опубликован commit `c76314eb23cff27c64c0a58d89d6fd911979c873` и прочитан с remote: QA 21/21, XLSX blob `d74432730f33ed56bb0809e90028d1db5fbe36b7`, Level-1 activation rule присутствует. Local-only completion = false.

## Независимый итог

- independent checks: **21/21 PASS**;
- A–U failures after correction: **0/21**;
- Step5A contamination: **0**;
- provider calls during rehearsal: **0**;
- substantive unresolved FAIL: **0**;
- release state: **PHASE 5 REHEARSAL PASS / G0–G15 PASS**.
