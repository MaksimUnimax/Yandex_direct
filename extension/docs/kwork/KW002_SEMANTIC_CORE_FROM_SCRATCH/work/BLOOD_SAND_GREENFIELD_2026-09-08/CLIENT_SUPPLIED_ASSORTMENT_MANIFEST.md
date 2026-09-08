# KW-002 Blood & Sand — CLIENT-SUPPLIED ASSORTMENT MANIFEST

Status: **FROZEN CLIENT INPUT / PRE-RESEARCH**  
Date: 2026-09-08

## 1. What the client says it sells

Client description for this order:

```text
Амулеты, обереги и талисманы.
В ассортименте есть в том числе товары для автомобиля.
```

Do not replace this client wording with an analyst-invented product category before Step 01.

## 2. Exact product catalogs supplied by the client

### Wildberries

Current seller-card source checked in Blood & Sand:

```text
MaksimUnimax/blood_sand
marketing/data/normalized/marketplace/wildberries/20260908__wb__cards-list__fresh-current108-identities.csv
```

Observed account total: **108 listing cards**.

For the KW-002 site/order the client explicitly marks:

```text
88 listing cards = IN SCOPE
20 listing cards = OTHER SELLER LINES / OUT OF SCOPE FOR THIS SITE
```

The 88 exact in-scope rows are copied into:

```text
CLIENT_SUPPLIED_PRODUCT_CATALOG.csv
```

The 20 explicitly excluded rows are copied into:

```text
CLIENT_SUPPLIED_OUT_OF_SCOPE_SELLER_LINES.csv
```

### Ozon

Full admitted Ozon catalog source checked in Blood & Sand:

```text
MaksimUnimax/blood_sand
marketing/data/raw/marketplace/ozon/20260811T1025Z__ozon__stocks-current__all.json
```

Returned product/listing identities: **76**.

All 76 exact product/listing identity rows are copied into:

```text
CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
```

## 3. What these files mean

They are client-supplied business/product facts only.

```text
MARKETPLACE LISTING ROW != UNIQUE PRODUCT MODEL
SAME NAME ON TWO MARKETPLACES != AUTOMATIC SAME SKU/VARIANT
PRODUCT TITLE != SEARCH QUERY
PRODUCT EXISTS != SEO PRIORITY
PRODUCT EXISTS != SEPARATE SEO PAGE
```

Step 01 must reconcile duplicates, variants, families and true product boundaries from the supplied catalog without importing old Blood & Sand SEO conclusions.

## 4. Examples of actual supplied product names

The catalog itself, not this example block, is authoritative. It contains actual names/variants including:

```text
Макошь
Родимич
Хорс
Мара
Стрибог
Семаргл
Всеславец
Сварог
Чур
Чернобог
Боговник
Триглав
Звезда Лады
Ратиборец
Белобог
Даждьбог
Алатырь (Крест Сварога)
Знак Велеса
Жива
Молвинец
Знич
Печать Велеса
Велес
Перун
Звезда Руси
Вегвизир / Рунический компас
Древо Жизни
Гунгнир
Валькнут
Шлем ужаса / Эгисхьяльм
Инь и Ян
Ом / Аум
Бусидо - Путь Воина
Молитва Иоанна Златоуста
Спаси и Сохрани
Герб России
Русская Община
RSOTM
Soldier Of Fortune
знаки зодиака: Овен, Телец, Близнецы, Рак, Лев, Дева, Весы, Скорпион, Стрелец, Козерог, Водолей, Рыбы
зодиакальные варианты/серии, включая Античность и Символы
```

## 5. No pre-clustering at intake

The client supplies names/listings, not an SEO taxonomy.

Do not pre-label these into permanent SEO groups such as `Slavic`, `Norse`, `automotive`, `religious`, `zodiac` as final search clusters at intake. Such labels may later be derived during Step 01/02 when supported by the catalog and fresh search research.

## 6. Accounting

```text
WB account listing rows observed = 108
WB in-scope listing rows supplied to KW-002 = 88
WB out-of-scope listing rows declared by client = 20
Ozon listing rows supplied = 76
Total admitted in-scope marketplace listing rows before cross-platform reconciliation = 164
Cross-platform unique-product count = NOT YET DETERMINED
```
