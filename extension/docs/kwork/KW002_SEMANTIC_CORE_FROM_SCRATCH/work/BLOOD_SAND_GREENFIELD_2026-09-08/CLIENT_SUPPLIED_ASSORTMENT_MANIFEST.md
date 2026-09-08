# KW-002 Blood & Sand — CLIENT-SUPPLIED ASSORTMENT MANIFEST

Status: **FROZEN CLIENT INPUT / Ozon-ONLY CORRECTION ACTIVE**  
Date: 2026-09-08

## 1. What the client says it sells

```text
Амулеты, обереги и талисманы.
В ассортименте есть в том числе товары для автомобиля.
```

Do not replace this client wording with an analyst-invented SEO/category definition before demand research.

## 2. Owner correction — authoritative catalog source

Latest owner instruction:

```text
USE ONLY OZON PRODUCT CARDS FOR THIS ORDER
REASON = Ozon catalog is the more current assortment authority and does not contain the duplicate-card problem relevant to this intake
WILDBERRIES CATALOG = SUPERSEDED / NOT AN EXECUTION INPUT FOR STEP 01
```

Therefore the client is treated as supplying one authoritative product catalog for the current order:

```text
MaksimUnimax/blood_sand
marketing/data/raw/marketplace/ozon/20260811T1025Z__ozon__stocks-current__all.json
```

Copied job input:

```text
CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
```

Exact Ozon listing/product identities: **76**.

## 3. WB files retained only as superseded history

The previously materialized WB files remain in Git history/job workspace for correction traceability but are NOT current Step-01 inputs:

```text
CLIENT_SUPPLIED_PRODUCT_CATALOG.csv = SUPERSEDED_NOT_ALLOWED
CLIENT_SUPPLIED_OUT_OF_SCOPE_SELLER_LINES.csv = SUPERSEDED_NOT_ALLOWED
```

Do not use them in assortment modeling, matching, seed planning or QA counts.

## 4. What the Ozon catalog means

The 76 rows are client-supplied business/product facts.

```text
OZON LISTING ROW = CURRENT CLIENT-SUPPLIED PRODUCT CARD FOR THIS TEST
PRODUCT TITLE != SEARCH QUERY
PRODUCT EXISTS != SEO PRIORITY
PRODUCT EXISTS != SEPARATE SEO PAGE
```

There is no cross-marketplace matching task in Step 01 after this correction.

## 5. Actual product names present in the supplied Ozon catalog

The file itself is authoritative. It includes exact product names such as:

```text
RSOTM
Soldier Of Fortune
Бусидо - Путь Воина
Шлем ужаса - Эгисхьяльм
Вегвизир - Рунический компас
Гунгнир
Валькнут
Древо Жизни
Ом / Аум
Инь и Ян
Белобог
Чернобог
Велес
Печать Велеса
Алатырь (Крест Сварога)
Триглав
Ратиборец
Молвинец
Колядник
Знич
Громовик
Всеславец
Боговник
Родимич
Молитва Иоанн Златоуст
Жива
Сварог
Перун
Стрибог
Макошь
Семаргл
Хорс
Мара
Звезда Лады
Даждьбог
Спаси и Сохрани
Чур
Герб России
12 знаков зодиака
варианты знаков зодиака «Античность»
варианты знаков зодиака «Символы»
```

The complete 76-row file, not this example block, is the execution universe.

## 6. No pre-clustering at intake

The client supplies products, not SEO taxonomy.

Step 01 may derive a neutral factual assortment model from explicit product names/series/variants, but it must not decide search demand, SEO clusters, page structure or priorities.

## 7. Corrected accounting

```text
AUTHORITATIVE PRODUCT CATALOGS = 1
OZON ROWS ADMITTED = 76
WB ROWS ADMITTED TO STEP 01 = 0
STEP 01 INPUT ROWS = 76
CROSS_PLATFORM RECONCILIATION = NOT APPLICABLE
```