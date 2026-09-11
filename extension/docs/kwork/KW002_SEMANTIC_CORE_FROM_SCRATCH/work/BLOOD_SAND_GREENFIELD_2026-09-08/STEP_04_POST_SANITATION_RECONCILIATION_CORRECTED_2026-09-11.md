# KW-002 Blood & Sand — corrected Step03B to historical Step04 reconciliation

Date: 2026-09-11
Status: **PASS / RECONCILIATION RECEIPT ONLY / DEDICATED STEP04 SEMANTIC WORK NOT EXECUTED**

## Scope

This receipt joins the corrected Step03B state of every normalized identity to the already-published historical corrected Step04 occurrence authority. It does not rewrite Step04 family semantics, the targeted-expansion queue, or any later roadmap step.

## Reconciliation totals

```text
STEP04_OCCURRENCE_ROWS = 25979
STEP04_UNIQUE_OCCURRENCE_IDS = 25979
STEP04_UNMAPPED_OCCURRENCES = 0
STEP04_MISSING_OCCURRENCES = 0
STEP04_UNEXPECTED_DUPLICATE_OCCURRENCE_IDS = 0

CORRECTED_ACTIVE_CANDIDATE_OCCURRENCES = 5263
CORRECTED_HOLD_OCCURRENCES = 13823
CORRECTED_EXCLUDED_OCCURRENCES = 6893
CORRECTED_TOTAL_RECONCILED_OCCURRENCES = 25979

STEP04_OBSERVED_FAMILIES = 25
STEP04_FAMILIES_WITH_CORRECTED_STATE_TRANSITIONS = 23
ROWS_CHANGING_NORMALIZED_STATE = 1710
RAW_OCCURRENCES_CARRIED_BY_CHANGED_IDENTITIES = 1761
```

## Family impact

| family_id | historical family label | occurrence rows | corrected KEEP | corrected HOLD | corrected EXCLUDE | changed occurrence rows | later semantic rewrite affected |
|---|---|---:|---:|---:|---:|---:|---|
| F001 | Прямые общие наименования «амулет», «оберег», «талисман» | 3 | 3 | 0 | 0 | 0 | NO |
| F002 | Общие товарные слова с явным коммерческим модификатором | 70 | 68 | 1 | 1 | 4 | YES |
| F003 | Амулеты, обереги, талисманы и чётки для автомобиля | 146 | 141 | 5 | 0 | 1 | YES |
| F004 | Чётки как предмет | 691 | 653 | 30 | 8 | 19 | YES |
| F005 | Название из каталога вместе с «амулет/оберег/талисман/чётки» | 200 | 191 | 7 | 2 | 7 | YES |
| F006 | Знаки зодиака с товарным или коммерческим уточнением | 106 | 105 | 0 | 1 | 103 | YES |
| F007 | Прямое название товара/символа из Ozon без явного чужого контекста | 249 | 0 | 223 | 26 | 19 | YES |
| F008 | Название из каталога с наблюдаемыми омонимами | 2042 | 7 | 1829 | 206 | 163 | YES |
| F009 | Форма или материал, не указанные в разрешённом каталоге | 506 | 257 | 241 | 8 | 122 | YES |
| F010 | Информационная/визуальная зонтичная семья: значения, история, мифология, руны и тату/body-art | 1263 | 397 | 858 | 8 | 28 | YES |
| F011 | Заявленные эффекты, защита и аудитории | 244 | 189 | 49 | 6 | 5 | YES |
| F012 | Знак зодиака без достаточного товарного уточнения | 5022 | 124 | 4747 | 151 | 170 | YES |
| F013 | Ассоциации провайдера без достаточного контекста | 1094 | 95 | 956 | 43 | 13 | YES |
| F014 | Морфологический и лексический шум | 1314 | 0 | 104 | 1210 | 6 | YES |
| F015 | Автомобильные модели, детали, краска/цвет и иные не-клиентские автотовары | 489 | 0 | 4 | 485 | 3 | YES |
| F016 | Игры и игровые предметы | 234 | 0 | 68 | 166 | 6 | YES |
| F017 | Книги, аудиокниги, сериалы, фильмы и музыка | 1680 | 0 | 470 | 1210 | 288 | YES |
| F018 | Города, адреса, организации и имена людей | 809 | 1 | 208 | 600 | 216 | YES |
| F019 | AUM: промышленное оборудование и Аум Синрикё | 127 | 0 | 58 | 69 | 1 | YES |
| F020 | Мантры, молитвы и религиозная практика без товарного указания | 143 | 0 | 56 | 87 | 10 | YES |
| F021 | Гороскопы, совместимость, даты и характеристики знаков | 5673 | 64 | 3339 | 2270 | 410 | YES |
| F022 | Другие явно несвязанные товары и сущности | 104 | 0 | 3 | 101 | 3 | YES |
| F023 | Остаточные фразы с недостаточным смысловым контекстом | 294 | 0 | 253 | 41 | 30 | YES |
| F024 | Молитвенная формулировка вместе с товарным словом | 116 | 5 | 111 | 0 | 0 | NO |
| F025 | Общее товарное слово в неразрешённом контексте | 3360 | 2963 | 203 | 194 | 134 | YES |

## Decision

The join is complete and one-to-one. Because corrected Step03B changes 1,710 normalized identities across 23 historical Step04 families, the existing family and expansion-queue conclusions require a later dedicated post-sanitation Step04 Work pass. This receipt does not perform that semantic rewrite.

```text
STEP04_RECONCILIATION = PASS
DEDICATED_POST_SANITATION_STEP04_WORK_PASS_REQUIRED = true
DEDICATED_POST_SANITATION_STEP04_WORK_EXECUTED = false
STEP05_ALLOWED = false
```
