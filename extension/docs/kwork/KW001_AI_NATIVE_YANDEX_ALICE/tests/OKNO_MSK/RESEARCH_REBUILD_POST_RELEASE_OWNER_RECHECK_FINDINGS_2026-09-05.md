# OKNO_MSK — corrected recipient set owner recheck findings

Дата: 2026-09-05  
Статус: **OWNER_RECHECK_ACTIVE / DOCUMENT_01_ANALYST_RECHECK_PASS / DOCUMENT_01_OWNER_REVIEW_PENDING**  
Класс: **POST_RELEASE OWNER RECIPIENT RECHECK / NOT A NEW ROADMAP STAGE**  
Проверяемый выпуск: `OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05`

## 1. Правило текущей работы

После общего correction/materialization pass финальная owner acceptance не восстанавливается автоматически. Проверка ведётся **по одному физическому recipient-документу**, в порядке:

1. №01 — клиентский исследовательский отчёт;
2. №02 — SEO implementation guide;
3. №03 — единый AI knowledge document.

Пока документ не прошёл owner recheck, его нельзя считать окончательно принятым только на основании deterministic QA.

```text
CORRECTION MATERIALIZED
!= OWNER ACCEPTED

DETERMINISTIC QA PASS
!= REAL RECIPIENT TASK PASS
```

## 2. Уже найденные замечания / несоответствия

### OR-01 — №03: clean-context PASS не был проверкой на отдельной модели

**Статус:** CONFIRMED ACCEPTANCE GAP.

Текущий recipient QA изолировал №03 и детерминированно проверил наличие/связность нужных данных, но **не запускал отдельную/local LLM**. Следовательно, этот PASS не доказывает главный recipient contract №03: что реальная совместимая AI-модель, имея только один файл №03, способна самостоятельно понять исследование, ответить на незаранее перечисленные вопросы в пределах evidence и не выдумать отсутствующие детали.

**Что требуется:** отдельная clean-context model validation с `ONLY №03`, без GitHub, live-site, Search, provider/API, previous chat и других release artifacts. До неё AI-recipient acceptance остаётся открытой.

### OR-02 — №02 / shared implementation truth: `S18-A012` помечен READY при недоказанной company-specific детали

**Статус:** CONFIRMED EXECUTION-PRECISION DEFECT -> CORRECTED IN SHARED AUTHORITY AND DOCUMENT №01; №02 OWNER REVIEW REMAINS PENDING.

`S18-A012` требует раскрыть для страницы ПВХ-дверей, в том числе, **что входит и не входит в монтаж**. Сохранённое evidence подтверждает наличие темы монтажа/сложности установки, но не фиксирует фактический состав услуги компании. Одновременно acceptance запрещает обещать работы, не подтверждённые компанией.

Получается противоречие:

```text
READY IMPLEMENTATION TASK
+
COMPANY-SPECIFIC FACT REQUIRED FOR EXECUTION
+
THAT FACT IS NOT PRESERVED IN EVIDENCE
=
EXECUTOR MUST GUESS OR REQUEST NEW BUSINESS DETAIL
```

**Что требуется:** либо ограничить READY-часть только доказанным содержанием, либо вынести недостающий состав услуги в `PENDING_BUSINESS_DETAIL / NEEDS_CONFIRMATION`; не заставлять исполнителя додумывать состав работ.

### OR-03 — №01 / №03: `QF001` показывает потенциальный конфликт family-level owner и exact-query semantic owner

**Статус:** CONFIRMED MATERIAL CONTRADICTION -> CORRECTED; FULL QF AUDIT COMPLETED.

В corrected №01 карточка:

`QF001 — алюминиевые окна на балкон`

указывает:

- основной URL: `/balkony-i-lodzhii`;
- поддерживающий URL: `/alyuminievye-okna`;
- решение: балконная задача основная, алюминиевый раздел поддерживает материал.

При owner recheck в №03 была обнаружена встроенная semantic-запись для точной фразы `алюминиевые окна на балкон`, которая указывает на алюминиевый commercial owner `/alyuminievye-okna/`.

Это может быть законным различием только если документ явно различает:

```text
FAMILY-LEVEL TASK OWNER
!= EXACT-PHRASE SEMANTIC OWNER
```

и объясняет, почему. Если такого разграничения нет или Stage-5 authority подтверждает exact owner, несовместимый с QF-карточкой, текущий `three_view_material_contradictions = 0` неверен.

**Что требуется:** проверить `QF001`, затем тем же правилом все 21 QF-карточки против current semantic authority. Никакое расхождение нельзя маскировать агрегацией family-level.

### OR-04 — №01: для 20 из 21 Search-family cards нет exact Step-09 observation, а основание downstream owner decision не всегда видно внутри самой карточки

**Статус:** CONFIRMED TRACEABILITY DEFECT -> CORRECTED IN DOCUMENT №01.

Corrected №01 честно сообщает, что только одно из 21 material family имеет точное совпадающее Step-09 наблюдение. Для остальных карточка обычно говорит `точного Step-09 наблюдения ... нет`, после чего указывает owner URL и решение.

Это не является автоматически аналитической ошибкой, если решение поддерживается другими сохранёнными слоями. Но для клиентского отчёта нужно проверить, может ли владелец прямо из карточки понять:

```text
ЕСЛИ EXACT SEARCH OBSERVATION НЕТ,
ТО КАКОЕ ИМЕННО ДРУГОЕ СОХРАНЁННОЕ ДОКАЗАТЕЛЬСТВО ПОДДЕРЖИВАЕТ OWNER DECISION?
```

Если ответ приходится восстанавливать вручную из других разделов, это остаточный recipient traceability defect №01.

### OR-05 — №03: фактическая совместимость размера/объёма с реальной локальной моделью не доказана

**Статус:** ACCEPTANCE BOUNDARY, NOT YET CLASSIFIED AS DEFECT.

Corrected №03 имеет размер около 1.12 MB и содержит полный knowledge universe. Самодостаточность по содержанию и пригодность для конкретного model context window — разные проверки.

Не объявлять размер дефектом без теста. Но owner acceptance №03 не должна утверждать, что «любая локальная модель» примет файл целиком, пока это не проверено на заявленном recipient class либо не сформулирована совместимость/минимальный context requirement.

## 3. Снятые ложные замечания

### WD-01 — якобы неправильный домен `okno-moskva.ru` в №01

**Статус:** WITHDRAWN / NOT A DEFECT.

Промежуточный пересказ дал ложное срабатывание. Фактический corrected source из GitHub правильно указывает `https://okno-msk.ru/`. В defect set не включать.

## 4. Gate, зафиксированный при обнаружении дефектов №01

На момент обнаружения №01 нельзя было отдавать владельцу как «готовый» до завершения следующих проверок:

1. все 21 QF-карточки сверены с current semantic authority;
2. family-level и exact-query ownership не противоречат друг другу либо явно разграничены;
3. для Search-family без exact observation видна достаточная доказательная опора решения;
4. все 75 exact Search observations не используются шире своего query scope;
5. 8 AI causal cases сохраняют `before AI -> AI observation -> decision delta -> limitation`;
6. полный action/result map не противоречит current shared implementation authority;
7. positive `KEEP / NO_CHANGE`, uncertainty и reopen rules доступны владельцу без внутренних файлов;
8. финальный PDF соответствует source по содержанию и не имеет материальных layout/render дефектов.

Если все пункты проходят — №01 можно передать владельцу на собственный просмотр и пометить `ANALYST_RECHECK_PASS / OWNER_REVIEW_PENDING`.

Если найден материальный дефект — исправляется №01 (и только необходимая shared authority, если ошибка именно там), затем пересобирается PDF и повторяется №01 QA. №02/№03 не считаются автоматически принятыми из-за исправления №01.

## 5. Статус до исправления №01 (историческая запись)

```text
CORRECTED_RELEASE_EXISTS = TRUE
OWNER_RECHECK = REWORK_REQUIRED
CURRENT_DOCUMENT = 01
DOCUMENT_01_ANALYST_RECHECK = IN_PROGRESS
DOCUMENT_01_OWNER_REVIEW = PENDING
DOCUMENT_02_OWNER_REVIEW = PENDING
DOCUMENT_03_OWNER_REVIEW = PENDING
FINAL_OWNER_RECIPIENT_ACCEPTANCE = OPEN
```

## 6. Закрытие аналитической перепроверки документа №01

**Итог:** `ANALYST_RECHECK_PASS / OWNER_REVIEW_PENDING`. Эта отметка не является owner acceptance и не открывает работу над №02.

### 6.1. Аудит QF001–QF021

Все карточки повторно сопоставлены с `RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv` и `RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv`. После исправления каждая карточка отдельно показывает владельца точной фразы, владельца семейства/структурной единицы и supporting pages; при отсутствии репрезентативной точной фразы владелец не выдумывается.

| QF | Результат | Владелец точной фразы по Stage-5 | Требовалось явное разграничение exact/family |
|---|---|---|---|
| QF001 | `FIX -> PASS` | `/alyuminievye-okna/` | да |
| QF002 | `PASS` | `/balkony-i-lodzhii/holodnoe-osteklenie/` | нет |
| QF003 | `PASS` | нет репрезентативной точной фразы | family-only карточка |
| QF004 | `PASS` | `/alyuminievye-okna/` | нет |
| QF005 | `FIX -> PASS` | `/uslugi/ustanovka-okon/` | да |
| QF006 | `FIX -> PASS` | `/alyuminievye-okna/` | да |
| QF007 | `PASS` | `/balkony-i-lodzhii/panoramnoe-osteklenie-balkona/` | нет |
| QF008 | `PASS` | нет репрезентативной точной фразы | family-only карточка |
| QF009 | `PASS` | нет репрезентативной точной фразы | family-only карточка |
| QF010 | `FIX -> PASS` | `/uslugi/otdelka-otkosov/` | да |
| QF011 | `PASS` | нет репрезентативной точной фразы | family-only карточка |
| QF012 | `PASS` | `/uslugi/remont-okon/` | нет |
| QF013 | `FIX -> PASS` | `/okna-rehau/panoramnoe-osteklenie/` | да |
| QF014 | `PASS` | `/okna-rehau/francuzskie-okna/` | нет |
| QF015 | `FIX -> PASS` | `/uslugi/ustanovka-okon/` | да |
| QF016 | `FIX -> PASS` | `/okna-rehau/po-tipu-doma/okna-v-chastnyj-dom/` | да |
| QF017 | `FIX -> PASS` | `/verandy/` | да |
| QF018 | `PASS` | `/okna-rehau/po-tipu-doma/zamena-okon-v-kvartire/` | нет |
| QF019 | `PASS` | `/stati/okno-otkrylos-v-dvuh-polozheniyah-chto-delat/` | нет |
| QF020 | `PASS` | `/stati/kakie-okna-samye-luchshie/` | нет |
| QF021 | `PASS` | нет репрезентативной точной фразы | family-only карточка |

Результат: `21/21 PASS`; исправлено карточек: `8`; нерешённых: `0`. QF005/QF006 не были приняты по прежнему предположению: их расхождения подтверждены текущей Stage-5 и исправлены. WD-01 остаётся снятым ложным замечанием.

Отдельно снята прежняя неточная формулировка «одно точное Step-09 наблюдение». Ни одна из 21 репрезентативных фраз буквально не совпадает с 75 строками Step-09; для 16 карточек с точной фразой существуют сохранённые поздние exact-Search результаты Stage-13, а QF020 имеет только связанное, но не тождественное наблюдение `SP09-059`. Документ теперь называет реальный слой evidence и не расширяет его scope.

### 6.2. Исправление доказательной трассировки

Перед QF-картами добавлено клиентское правило четырёх сущностей: exact-query owner, family/unit owner, supporting page и physical site action. В каждой карточке теперь указаны точный semantic state, structural unit, user task/intent, canonical URL, supporting URLs, uncertainty, человекочитаемое основание решения, граница физического действия и ограничение доказательства. Ссылки на внутренние стадии сопровождаются объяснением их фактического смысла.

### 6.3. S18-A012 и карта действий

`S18-A012` больше не является полностью `READY`. Текущий статус: `READY_PARTIAL__BUSINESS_DETAIL_REQUIRED`, `CONTENT_BLOCK_PARTIAL`, `site change = PARTIAL`.

- доказанная READY-часть: сохранить цену/калькулятор/замер/CTA и нейтрально объяснить, что профессиональный монтаж — отдельный процесс, детали которого подтверждаются после замера;
- `PENDING_BUSINESS_DETAIL`: состав включённых/исключённых работ, подготовка клиента, демонтаж/вывоз, откосы/отделка, герметизация/регулировка, гарантийные и сервисные обязательства;
- запрещено публиковать эти company-specific факты без подтверждения бизнеса.

Пересчитанная карта из 34 строк: `7` полностью готовых физических действий, `1` частично готовое действие A012, `19` аналитических mapping-only строк и `4` recheck/not-ready строки. Дополнительно сохранены `15` pending link relations, `46` аналитических routing rows и `20` HOLD units. Analytical mapping нигде не выдан за CMS-задачу.

### 6.4. Полные проверки материала №01

- ordinary Yandex Search: `75/75 PASS`; каждое наблюдение ограничено точным запросом и не объявляет доказанными трафик, конверсию, стабильный ранг, family-wide вывод или каннибализацию;
- AI causal cases: `8/8 PASS`; сохранена цепочка `WHY SELECTED BEFORE AI -> SEARCH-ONLY DECISION -> AI OBSERVATION -> DELTA -> VERDICT -> ARCHITECTURE EFFECT -> ACTION -> LIMITATION`; AI не создаёт новую архитектуру и не подменяет Search/Stage-5;
- action/result map: `34/34 PASS` относительно corrected shared implementation authority;
- KEEP / NO_CHANGE и запреты на разрушительные изменения видимы;
- `SEARCH_REQUIRED`, `REVIEW_DEFERRED`, `HOLD`, `NOT_READY__EVIDENCE_REQUIRED`, `PENDING_DETAIL` и `PENDING_BUSINESS_DETAIL` имеют определения и reopen rules;
- детерминированная QA: `285/285 PASS` в `RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_ANALYST_RECHECK_QA_2026-09-05.json`;
- Markdown/DOCX/PDF material equivalence: `PASS`;
- физическая PDF QA: `57/57` страниц просмотрены, clipping/overlap/blank page/missing glyph/сломанных URL или отсутствующего окончания не найдено; шрифты встроены с Unicode.

## 7. Текущий gate после аналитической перепроверки №01

```text
CORRECTED_RELEASE_EXISTS = TRUE
OWNER_RECHECK = ACTIVE
CURRENT_DOCUMENT = 01
DOCUMENT_01_ANALYST_RECHECK = PASS
DOCUMENT_01_OWNER_REVIEW = PENDING
DOCUMENT_02_OWNER_REVIEW = PENDING
DOCUMENT_03_OWNER_REVIEW = PENDING
FINAL_OWNER_RECIPIENT_ACCEPTANCE = OPEN
NEXT_ACTION = OWNER_REVIEW_CORRECTED_DOCUMENT_01
```
