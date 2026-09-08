# KW-002 «Кровь и Песок» — STEP 02 REWORK V2

Дата: 2026-09-08

Статус: **REWORK EXECUTED / LOCAL QA PENDING FINAL REMOTE READBACK**

## 1. Почему Step 02 был открыт заново

Первая версия Step 02 формально покрывала 76/76 карточек и содержала 97 discovery probes, но внешний аудит показал, что это доказывало в основном происхождение и учёт, а не качество поискового маршрута.

V1 quality score:

```text
6.5 / 10
REWORK_REQUIRED
```

Главные ошибки V1:

```text
- bare high-noise name мог считаться достаточным primary route;
- catalog coverage подменяло search-probe-quality coverage;
- автомобильный контекст почти целиком зависел от формулировки «в машину»;
- точные названия продавца слишком автоматически становились PRIMARY;
- information-gain rationale часто был шаблонным;
- provider cost мог влиять на deferral сильнее, чем реальный information gain.
```

## 2. Какая постоянная методика теперь действует

Новый Level-2 authority:

`LEVEL2/STEP_02_SEED_ACQUISITION_QUALITY_GATE.md`

Он требует:

```text
CATALOG_LINEAGE_COVERAGE != SEARCH_PROBE_QUALITY_COVERAGE
HIGH-NOISE BARE PRIMARY -> refinement/control governance required
systematic but bounded synonym/use-context plan
seller title/name != automatic PRIMARY
information gain must discriminate now/later/redundant/control
primary acquisition manifest must be deterministic
Step-02 score >= 9/10 + all hard gates
```

## 3. Что изменено в текущей работе

### 3.1 High-noise / ambiguous names

19 bare V1 probes переведены из основного маршрута в deferred/control.

Для них созданы 19 новых qualified primary probes:

- 18 — через диагностический OR-контекст `(амулет|оберег|талисман) + name`;
- 1 — `оберег Родимич`, потому что эта квалификация буквально присутствует в клиентской карточке.

Qualified probe не объявляет конкретный товар амулетом/оберегом/талисманом. Для analyst-composed строк это только диагностическая конструкция для отделения товарного слоя спроса от общей информационной/омонимичной темы.

### 3.2 Автомобильные формулировки

Сохранены исходные/первичные routes `в машину`.

Добавлен bounded synonym axis:

```text
для машины
для автомобиля
для авто
```

для четырёх фактических roots:

```text
талисман
амулет
оберег
чётки
```

Итого новых use-context probes = 12.

Это намеренно ограниченный план, а не декартово перемножение всех слов.

### 3.3 Exact seller names

19 неоднозначных bare names больше не являются основным quality route.

Distinct/сравнительно низкошумные названия сохранены как primary discovery probes.

Более шумные bare формы остаются audit/control material и могут быть активированы позже, если qualified результаты создадут конкретный вопрос.

### 3.4 Zodiac

`знак зодиака` остаётся broad control, но не считается единственным качественным маршрутом.

12 scoped sign probes остаются primary.

Variant markers `Античность / Античность 2 / Символы` остаются deferred до появления базового demand evidence.

## 4. V2 accounting

```text
V1 retained primary probes = 48
V2 qualified refinement probes = 19
V2 automobile synonym probes = 12
V2 PRIMARY MANIFEST TOTAL = 79

V1 original deferred probes = 30
V1 bare probes newly demoted to control = 19
V2 DEFERRED/CONTROL TOTAL = 49

V2 new probes created = 31
```

## 5. Durable V2 artifacts

```text
STEP_02_V2_DECISION_OVERLAY.csv
STEP_02_V2_ADDITIONAL_PROBES.csv
STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv
STEP_02_DEFERRED_CONTROL_MANIFEST_V2.csv
STEP_02_SEARCH_PROBE_QUALITY_COVERAGE_V2.csv
STEP_02_REWORK_REPORT_V2_2026-09-08.md
STEP_02_QA_REPORT_V2_2026-09-08.md
```

Original V1 artifacts remain preserved as history and must not be mistaken for the current Step-03 execution manifest.

## 6. Current primary authority for Step 03

Only this file defines the current executable primary set:

`STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`

Expected rows:

```text
79
```

Step 03 must not reconstruct current priorities from the old 97-row V1 file.

## 7. What still is NOT decided

Step 02 V2 still does not claim:

```text
search demand exists
frequency
KEEP/REJECT
intent
cluster
page
site IA
SEO priority
competitor evidence
AI-search behavior
```

Those require later evidence.

## 8. Provider state

```text
WORDSTAT CALLS DURING STEP 02 REWORK = 0
SEARCH CALLS = 0
AI SEARCH CALLS = 0
PROVIDER COST = 0 RUB
```

## 9. Quality scoring

Final scoring is governed by `LEVEL1/RESULT_QUALITY_SCORING_RULE.md`.

Target for acceptance:

```text
QUALITY_SCORE >= 9.0 / 10
ALL HARD GATES = PASS
REMOTE READBACK = PASS
```

The final score and pass verdict are recorded in `STEP_02_QA_REPORT_V2_2026-09-08.md` after remote readback.

## ПРОСТЫМИ СЛОВАМИ

**Зачем исправляли:** первый список был аккуратно оформлен, но некоторые стартовые запросы могли увести Wordstat в общий информационный шум вместо товарного спроса.

**Что фактически исправили:** для неоднозначных названий добавили уточнённые товарные probes, расширили автомобильные формулировки, отделили broad control от реального quality coverage и сформировали новый точный список того, что должен запускать Step 03.

**Что получаем:** Wordstat теперь будет запускаться не по «любому запросу на карточку», а по проверенному набору маршрутов, где шум и уточнение управляются заранее.
