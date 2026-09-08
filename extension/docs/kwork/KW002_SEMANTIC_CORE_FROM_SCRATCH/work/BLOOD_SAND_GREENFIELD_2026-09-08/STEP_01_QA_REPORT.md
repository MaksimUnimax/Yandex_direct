# KW-002 «Кровь и Песок» — STEP 01 QA

Дата: 2026-09-08

Проверяемый источник: `CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv`

Локальный QA: **PASS**

Финальный статус до GitHub readback: **PENDING_REMOTE_READBACK**

## 1. Подход к проверке

QA пытался найти пропущенные и добавленные строки, изменения исходной идентичности, недопустимые выводы из названий, принудительно заполненные неизвестные факты, ошибочное членство нейтральных направлений и следы запрещённых источников.

Проверка выполнялась по полному набору, не по выборке:

- исходный CSV разобран стандартным CSV-парсером;
- каждая из 76 исходных строк сопоставлена с выходом по позиции, `listing_id`, SKU и точному заголовку;
- нормализованные заголовки сравнены с исходными по всем буквенно-цифровым знакам;
- проверены все 84 выделенных фрагмента названий/алиасов;
- каждое явно выделенное слово формы/назначения и каждый маркер варианта проверены на буквальное присутствие в исходном заголовке;
- списки `product_id` и SKU в модели направлений сверены с 76-строчной таблицей;
- все ссылки реестра неопределённостей проверены на существование в разрешённом источнике;
- отдельно выполнен ручной контроль границ утверждений.

В ходе QA найдена и до принятия результата исправлена одна ошибка: у строки 76 в выделенное название попала лишняя кавычка. После исправления все проверки повторены и прошли.

## 2. Обязательное количественное сверение

```text
OZON_INPUT_ROWS_EXPECTED = 76
OZON_INPUT_ROWS_OBSERVED = 76
OZON_INPUT_ROWS_ACCOUNTED = 76
UNIQUE_SOURCE_ROW_NUMBERS = 76
UNIQUE_PRODUCT_ID_ROWS_EXPECTED = 76  # вычислено из источника
UNIQUE_PRODUCT_ID_ROWS_OBSERVED = 76
UNIQUE_SKU_ROWS_EXPECTED = 76  # вычислено из источника
UNIQUE_SKU_ROWS_OBSERVED = 76
UNIQUE_SOURCE_TITLES = 76
SILENT_DROPS = 0
DUPLICATE_OUTPUT_ROWS_CREATED = 0
ORIGINAL_PRODUCT_IDS_PRESERVED = true
ORIGINAL_SKUS_PRESERVED = true
ORIGINAL_TITLES_PRESERVED = true
OUTPUT_ROWS_WITH_ALL_REQUIRED_FIELDS = 76
SOURCE_ROW_ACCOUNTED_TRUE = 76
```

Идентичности сохранены так: требуемое выходное поле `product_id` содержит исходное значение поля `listing_id`; никакая новая товарная идентичность не создавалась.

## 3. Сверка нейтральной модели

```text
NAC-01 Чётки = 4
NAC-02 Знаки зодиака = 37
NAC-03 Явное слово «Оберег» = 1
NAC-04 Название без физической формы = 34
CONCEPT_MEMBERSHIP_TOTAL = 76
CONCEPT_MEMBERSHIP_MISSING = 0
CONCEPT_MEMBERSHIP_EXTRA = 0
CONCEPT_SOURCE_ID_LIST_MISMATCHES = 0
CONCEPT_SOURCE_SKU_LIST_MISMATCHES = 0
CANONICAL_SOURCE_ROWS_DUPLICATED_FOR_MULTIPLE_DIMENSIONS = 0
```

Сверка вариантов:

```text
NOT_STATED = 50
Античность = 12
Античность 2 = 1
Символы = 12
Логотип = 1
TOTAL = 76
```

Сверка явных слов формы/назначения:

```text
Чётки + Талисман в машину = 3
Чётки = 1
Знак зодиака = 37
Оберег = 1
NOT_STATED = 34
TOTAL = 76
```

## 4. Проверка доказательности

```text
EXPLICIT_NAME_OR_ALIAS_FRAGMENTS_CHECKED = 84
EXPLICIT_NAME_OR_ALIAS_FRAGMENTS_NOT_LITERAL_IN_TITLE = 0
EXPLICIT_USE_OR_FORM_VALUES_NOT_LITERAL_IN_TITLE = 0
EXPLICIT_VARIANT_MARKERS_NOT_LITERAL_IN_TITLE = 0
NORMALIZATION_ALPHANUMERIC_CONTENT_CHANGES = 0
UNSUPPORTED_FACTUAL_INFERENCES = 0
UNKNOWN_FACTS_FORCED_TO_CERTAINTY = 0
ROWS_WITH_VISIBLE_UNKNOWN_OR_LIMIT = 76
AMBIGUITY_LEDGER_ISSUES = 10
AMBIGUITY_REFERENCES_TO_UNKNOWN_PRODUCT_IDS = 0
AMBIGUITY_REFERENCES_TO_UNKNOWN_SKUS = 0
```

Ручной adversarial-review подтвердил:

- автомобильный контекст не перенесён со строк 1–3 на строку 4;
- скобки `Gungner`, `Valknut`, `санскр. ॐ` и `Крест Сварога` не объявлены сериями или доказанными эквивалентами;
- `Античность`, `Античность 2`, `Символы` и `Логотип` сохранены только как явные маркеры заголовков;
- физическая форма, материалы, размеры, аудитория, история и эффекты не придуманы;
- близкие названия не слиты в один физический товар без клиентского подтверждения.

## 5. Проверка запретов

```text
WORK_SOURCE_WHITELIST = PASS
WB_ROWS_USED = 0
CROSS_PLATFORM_JOINS_PERFORMED = 0
PROHIBITED_OLD_RESEARCH_USED = 0
OLD_RESEARCH_CONTAMINATION = 0
WEB_REQUESTS = 0
PROVIDER_OR_API_REQUESTS = 0
WORDSTAT_REQUESTS = 0
ORDINARY_SEARCH_REQUESTS = 0
AI_SEARCH_REQUESTS = 0
SEO_KEYWORD_DECISIONS_CREATED = 0
SEO_CLUSTER_DECISIONS_CREATED = 0
PAGE_OR_IA_DECISIONS_CREATED = 0
CATALOG_CONCEPT_AS_SEO_CLUSTER_CLAIMS = 0
HISTORICAL_OR_MYSTICAL_TRUTH_CLAIMS_CREATED = 0
```

Слова о будущих SEO-этапах встречаются только как явные ограничения или маршрутизация неизвестного, а не как принятые SEO-решения.

## 6. Проверка обязательных файлов

```text
STEP_01_OZON_LISTING_MODEL.csv = PRESENT / 76 DATA ROWS
STEP_01_ASSORTMENT_CONCEPT_MODEL.csv = PRESENT / 4 DATA ROWS / MEMBERSHIP 76
STEP_01_BUSINESS_AND_ASSORTMENT_MODEL.md = PRESENT
STEP_01_UNKNOWN_OR_AMBIGUITY_LEDGER.csv = PRESENT / 10 DATA ROWS
STEP_01_QA_REPORT.md = PRESENT
BUSINESS_AND_ASSORTMENT_MODEL_MATERIALIZED = true
```

## 7. Локальный PASS gate

```text
WORK_SOURCE_WHITELIST = PASS
OZON_INPUT_ROWS_EXPECTED = 76
OZON_INPUT_ROWS_ACCOUNTED = 76
WB_ROWS_USED = 0
SILENT_DROPS = 0
ORIGINAL_IDENTITIES_PRESERVED = true
UNSUPPORTED_FACTUAL_INFERENCES = 0
UNKNOWN_OR_AMBIGUOUS_FACTS_VISIBLE = true
CATALOG_CONCEPT_AS_SEO_CLUSTER_CLAIMS = 0
OLD_RESEARCH_CONTAMINATION = 0
BUSINESS_AND_ASSORTMENT_MODEL_MATERIALIZED = true
LOCAL_QA = PASS
REMOTE_GITHUB_READBACK = PENDING
```

До удалённого чтения:

```text
STEP_01 = COMPLETE_LOCALLY / PENDING_REMOTE_READBACK
NEXT_STEP_ALLOWED = false
NEXT_STEP = STEP_02_SEED_ACQUISITION_MAP
```

Финальный `COMPLETE / PASS` и разрешение Step 02 могут быть зафиксированы только после коммита, отправки и проверки файлов из удалённой ветки GitHub.
