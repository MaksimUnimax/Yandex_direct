# KW-001 — серия из 7 коммерческих мини-кворков

Status: **ACTIVE PRODUCTIZATION / MK01 V1 FROZEN / MK02 ACTIVE**

## 1. Зачем создаётся эта серия

Исходный KW-001 доказал полный end-to-end процесс на пилоте OKNO_MSK. Теперь из него выделяются семь самостоятельных коммерческих продуктов, которые можно продавать отдельно, не заставляя клиента покупать весь большой KW-001.

Главное правило серии:

```text
ОДИН БОЛЬШОЙ ПРОВЕРЕННЫЙ KW-001
→ ВЫДЕЛЕНИЕ ОГРАНИЧЕННОГО РЕЗУЛЬТАТА
→ ВЫБОР ТОЛЬКО НУЖНЫХ ШАГОВ И ПРАВИЛ
→ ОТДЕЛЬНЫЙ MINI-KWORK METHOD
→ ОТДЕЛЬНЫЙ OKNO_MSK REHEARSAL
→ ОТДЕЛЬНЫЙ CLIENT DELIVERABLE
→ QA
→ KWORK CARD
→ ПУБЛИКАЦИЯ
```

Мини-кворк не является сокращённым рекламным текстом полного KW-001. Это самостоятельный продукт с собственным входом, обещанием, дорожной картой, границами, выдачей и Definition of Done.

## 2. Две независимые двухуровневые архитектуры

### 2.1. Уровни данных

```text
LEVEL 1 = универсальная методика конкретного mini-kwork
LEVEL 2 = данные конкретного заказа / теста
```

OKNO_MSK используется только как Level-2 rehearsal/evidence example. Его URL, запросы, решения и бизнес-факты не становятся универсальными правилами следующего клиента.

### 2.2. Уровни правил внутри каждого mini-kwork

```text
RULE LEVEL A = COMMON / CROSS-STEP RULES
RULE LEVEL B = PER-STEP RULES
```

Общие правила действуют на весь mini-kwork. Каждый шаг дополнительно получает собственную подробную методику и pass gate.

## 3. Общие правила, наследуемые из KW-001

Каждый mini-kwork обязан сохранить релевантные правила исходного KW-001, в том числе:

1. Scope freeze до acquisition/анализа.
2. Business boundary: не исследовать спрос в отрыве от реального бизнеса клиента.
3. Current-site freshness: старый inventory не доказывает текущее состояние сайта.
4. Evidence-first: FACT / OBSERVATION / ASSIGNMENT / CONCLUSION / RECOMMENDATION / BUSINESS FACT / UNKNOWN различаются.
5. Provenance: значимый вывод должен иметь источник и трассировку.
6. Provider call делается только ради конкретного information gap.
7. Evidence сохраняется; повторный платный вызов без необходимости запрещён.
8. Wordstat подтверждает спрос, но сам по себе не доказывает intent/page ownership/новую страницу.
9. Ordinary Yandex Search используется там, где решение требует Search-grounded проверки.
10. AI не заменяет Ordinary Search.
11. GenSearch/Alice не смешиваются без доказанного основания.
12. UNKNOWN / HOLD / SEARCH_REQUIRED / PENDING_BUSINESS_DETAIL — допустимые результаты.
13. KEEP / NO_CHANGE — полноценные результаты.
14. FAMILY ROUTE != EXACT QUERY OWNER != SUPPORTING PAGE.
15. SEMANTIC MAPPING != PHYSICAL SITE ACTION.
16. Новая страница/структурное изменение не создаётся простой эвристикой.
17. Поздняя canonical authority имеет приоритет над ранним discovery inventory.
18. Любое изменение authority должно пройти downstream propagation.
19. Найденный defect исправляется как класс: root cause → rule → regression, а не только один пример.
20. Partial correction запрещена.
21. Uncertainty должна сохраняться downstream.
22. Client-facing deliverable должен быть понятен без внутреннего репозитория.
23. Analytical QA, deterministic QA, physical QA и recipient QA — разные gates.
24. Green deterministic QA != owner/recipient acceptance.
25. Source/generator исправляется раньше финального PDF/выгрузки.
26. Значимый завершённый блок: SAVE → COMMIT → REMOTE READBACK.

## 4. Обязательная структура каждого mini-kwork

Когда начинаем конкретный mini-kwork, в его директории материализуются как минимум:

```text
PRODUCT_SCOPE.md
CLIENT_INPUT_CONTRACT.md
GENERAL_RULES.md
STEP_RULES_INDEX.md
steps/STEP_XX_*.md
DELIVERABLE_SPEC.md
QA_AND_RELEASE.md
ERRORS_AND_LESSONS.md
KWORK_CARD.md
PORTFOLIO_ASSET_SPEC.md

tests/OKNO_MSK/TEST_ORDER.md
tests/OKNO_MSK/TEST_EXECUTION.md
tests/OKNO_MSK/TEST_RESULT.md
tests/OKNO_MSK/CLIENT_DELIVERABLE.md
tests/OKNO_MSK/QA.md
```

Дополнительные structured-data файлы создаются там, где они нужны конкретному продукту.

## 5. Что обязано быть в каждом per-step rule

Каждый шаг mini-kwork должен содержать:

```text
STEP PURPOSE
WHY THIS STEP EXISTS
INPUTS
REQUIRED EVIDENCE
METHOD
OUTPUTS
SOURCE KW-001 STEP / AUTHORITY
KNOWN KW-001 FAILURE CLASSES
ROOT CAUSES
NON-REPEAT CONTROLS
CLAIM BOUNDARIES
UNKNOWN / BLOCKER BEHAVIOR
PASS GATE
CLIENT-FACING MEANING
```

Нельзя просто написать «использовать Step N из KW-001». Нужная часть переносится в автономный mini-kwork method с сохранением происхождения и исправлений.

## 6. Универсальный цикл productization одного mini-kwork

### Phase 0 — Product promise freeze
Фиксируем, что именно продаётся и что не продаётся.

### Phase 1 — Market reality check
Для карточки сохраняем реальные существующие аналоги/заказы, цены, пересечение и различия. Если точного аналога нет — так и пишем; не выдаём составной аналог за точный.

### Phase 2 — Client input contract
Определяем минимально необходимые входы клиента, optional inputs, недопустимые секреты, что происходит при неполных данных.

### Phase 3 — KW-001 extraction
Из полного KW-001 выбираем только необходимые steps/gates. Для каждого извлекаем накопленные failure classes, исправления и non-repeat controls.

### Phase 4 — Mini-kwork roadmap
Строим автономный последовательный roadmap. Удалённые шаги полного KW-001 не должны оставлять скрытые зависимости.

### Phase 5 — OKNO_MSK rehearsal projection
Берём уже собранный OKNO_MSK evidence, не делаем лишние provider calls и выполняем mini-kwork так, будто клиент купил только его. Нельзя отдавать результат полного KW-001 под видом результата mini-kwork.

### Phase 6 — Mini-kwork client deliverable
Перестраиваем материал под обещание конкретного mini-kwork: другой scope → другой отчёт → другой набор таблиц → другой вывод.

### Phase 7 — QA
Проверяем аналитическую корректность, counts/schema, независимую реконструкцию критических решений, физическую читаемость и recipient usefulness.

### Phase 8 — Pricing/package freeze
На основании реального объёма теста фиксируем base price, limits, add-ons, срок, revision boundary, provider-cost boundary.

### Phase 9 — Kwork card
Готовим название, описание, «что нужно от покупателя», результат, FAQ, ограничения, дополнительные опции.

### Phase 10 — Portfolio illustration
Создаём иллюстрацию/обложку и безопасный демонстрационный фрагмент результата без ложных обещаний и закрытых данных.

### Phase 11 — Owner publication
Владелец проверяет карточку и публикует её на площадке.

### Phase 12 — Freeze / readback
Фиксируем опубликованную версию, цену и package boundaries в репозитории.

## 7. Семь продуктов

| ID | Рабочее название | Основной продаваемый результат | Ключевые KW-001 этапы | Статус |
|---|---|---|---|---|
| MK01 | Семантическое ядро + кластеризация | очищенное, подтверждённое спросом ядро и кластеры | 0–8 + targeted 9 + 10 + 19–20 | **OWNER ACCEPTED / V1 FROZEN** |
| MK02 | Семантическое ядро + SEO-архитектура + ТЗ разработчику | ядро → владельцы/структура → конкретное ТЗ | MK01 + 11–14 + 18–20 | **ACTIVE / NEXT** |
| MK03 | SEO-анализ конкурентов + семантические/структурные пробелы | реальные Search-конкуренты → missed demand → подтверждённые gaps | 0–5A + demand/Search validation + 7–8 + 19–20 | PLANNED |
| MK04 | Запрос → страница + интенты + каннибализация | mapping запросов/семейств к страницам и конфликтам | 0–1 + 8–14 + 19–20 | PLANNED |
| MK05 | SEO-ТЗ на внедрение | implementation-ready действия для специалиста | current-site recheck + canonical inputs + 12 + 18–20 | PLANNED |
| MK06 | Яндекс Нейро / Алиса / AEO-аудит | Search baseline → AI cases → delta → действия | 0–1 + 8–10/11/14 + 15–20 | PLANNED |
| MK07 | Полный комплекс KW-001 | полный современный Яндекс/Alice semantic rebuild | полный применимый KW-001 roadmap включая 5A и AI | PLANNED |

Точные подшаги каждого mini-kwork замораживаются только в его собственном STEP_RULES_INDEX после extraction-аудита полного KW-001.

## 8. Границы между семью продуктами

### MK01 vs MK02
MK01 заканчивается готовым ядром/кластерами. MK02 добавляет page ownership, архитектуру и ТЗ только на изменения, полученные из этого исследования.

### MK02 vs MK05
MK02 исследует семантику и из неё выводит архитектуру. MK05 продаёт перевод уже существующей утверждённой decision authority в исполнимые website tickets; он не должен незаметно включать полный повторный semantic research.

### MK03 vs MK07
MK03 — конкурентный acquisition/gap продукт. Он не обещает полный аудит всех ключей всех конкурентов и не включает полный AI-layer.

### MK04 vs MK02
MK04 может работать от уже имеющегося у клиента semantic set и решает ownership/cannibalization. Полный новый сбор спроса в его base scope не входит.

### MK06 vs MK07
MK06 проверяет Search↔AI различия для достаточного набора meaningful cases. Полная пересборка семантического ядра входит только в MK07 или отдельный add-on.

## 9. Реальные рыночные anchors, которые надо хранить честно

- MK01: существуют Kwork-продукты `семантика + кластеризация/структура` около 8–12 тыс. руб.; существует FL.ru задача около 15 тыс. руб. на ~2000 запросов с ручной проверкой ТОПа.
- MK02: точный Kwork-аналог `семантическое ядро + SEO-архитектура + ТЗ разработчику` в текущем поиске не подтверждён. Есть близкий реальный проект FL.ru с бюджетом 40 тыс. руб. на семантическое ядро + кластеризацию + ТЗ на доработку сайта. Нельзя маркировать его как Kwork-аналог.
- MK03: существуют отдельные конкурентные анализы на Kwork и SEO-аудиты конкурента на FL.ru.
- MK04: существуют реальные задания на clustering/page mapping/cannibalization и ручной анализ SERP; точное совпадение состава надо проверять при финализации карточки.
- MK05: на Kwork встречается ТЗ как часть/дополнение SEO-аудита; standalone implementation-ready продукт нужно позиционировать отдельно.
- MK06: на Kwork реально продаются AEO/GEO/нейропоиск-аудиты от нескольких тысяч до крупных комплексных пакетов; состав сильно различается.
- MK07: реальные комплексные SEO/audit/semantic/structure/TZ проекты существуют примерно в диапазоне 40–60 тыс. руб. и выше в зависимости от состава.

Перед публикацией каждого mini-kwork его market evidence обновляется заново.

## 10. Definition of Done mini-kwork перед публикацией

```text
PROMISE FROZEN
+ MARKET ANALOGS VERIFIED
+ CLIENT INPUT CONTRACT COMPLETE
+ KW001 STEPS EXTRACTED
+ FAILURE CLASSES EXTRACTED
+ GENERAL RULES COMPLETE
+ PER-STEP RULES COMPLETE
+ OKNO_MSK REHEARSAL COMPLETE
+ MINI-KWORK-SPECIFIC DELIVERABLE COMPLETE
+ QA PASS
+ OWNER RECIPIENT REVIEW PASS
+ PRICE/LIMITS FROZEN
+ CARD COPY COMPLETE
+ PORTFOLIO ASSET COMPLETE
+ REPO READBACK PASS
= READY_FOR_OWNER_PUBLICATION
```

## 11. Последовательность работы

Работаем строго по одному продукту:

```text
MK01 COMPLETE + PUBLISHED/FROZEN
→ MK02
→ MK03
→ MK04
→ MK05
→ MK06
→ MK07
```

Не начинаем детальную productization следующего mini-kwork до owner gate текущего.

Owner accepted/froze MK01 V1 on 2026-09-10. MK01 visual/publication work is deferred and does not block MK02 productization.

## 12. Текущая точка

```text
CURRENT_MINI_KWORK = MK02_SEMANTIC_CORE_ARCHITECTURE_DEV_TZ
MK01_STATE = OWNER_ACCEPTED__V1_FROZEN
NEXT_ACTION = BUILD_MK02_PRODUCT_SCOPE__MARKET_REFRESH__CLIENT_INPUT_CONTRACT__KW001_STEP_EXTRACTION
```
