# OKNO_MSK — corrected recipient set owner recheck findings

Дата: 2026-09-05  
Статус: **OWNER_RECHECK_ACTIVE / REWORK_REQUIRED / DOCUMENT_01_REVIEW_IN_PROGRESS**  
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

**Статус:** CONFIRMED EXECUTION-PRECISION DEFECT.

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

**Статус:** MATERIAL CONTRADICTION CANDIDATE — AUTHORITY CHECK REQUIRED BEFORE ACCEPTANCE.

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

**Статус:** TRACEABILITY / DEPTH CANDIDATE — MATERIALITY CHECK IN DOCUMENT 01 REVIEW.

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

## 4. Текущий gate по документу №01

№01 нельзя отдавать владельцу как «готовый» до завершения следующих проверок:

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

## 5. Current status

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
