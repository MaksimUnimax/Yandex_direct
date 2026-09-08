# KW-002 «Кровь и Песок» — STEP 02 EXTERNAL METHOD AUDIT

Дата: 2026-09-08

Статус: **EXTERNAL METHOD AUDIT COMPLETE / STEP 02 REWORK REQUIRED / STEP 03 BLOCKED**

## 1. Зачем выполнен внешний аудит

После первоначального `STEP_02 = COMPLETE / PASS` владелец потребовал заново проверить методику по конкретным внешним материалам и оценить фактические 97 seed-запросов не только по внутреннему QA.

В соответствии с Level-1 rule о том, что поздняя проверка может отменить ранее записанный PASS, этот аудит проверяет не наличие файлов и не строковый accounting, а качество самих discovery probes.

## 2. Проверенные внешние источники

### OFFICIAL_YANDEX — Яндекс Вебмастер: подбор поисковых запросов и анализ рынка

https://yandex.ru/support/webmaster/ru/service/queries-selection

Материал подтверждает:

- начинать следует с основных слов, характеризующих нишу;
- инструмент ищет дополнительные и неочевидные пользовательские формулировки;
- слишком широкую выдачу можно очищать минус-словами;
- спрос и дополнительные запросы затем оцениваются по реальным данным.

### OFFICIAL_YANDEX — Яндекс Директ: как подобрать ключевые фразы

https://yandex.ru/support/direct/ru/keywords/building-keyword-list

Материал подтверждает:

- фраза должна быть тесно связана с реальным товаром/услугой;
- слишком общую или двусмысленную фразу следует конкретизировать;
- нужно учитывать основные синонимы, сленг и профессиональные термины;
- для иностранных названий/брендов важны разные письменности/варианты, когда ими реально пользуются;
- Wordstat используется затем для проверки частоты и похожих запросов.

### OFFICIAL_YANDEX — Wordstat GetTop

https://aistudio.yandex.ru/en/docs/search-api/api-ref/grpc/Wordstat/getTop

Материал подтверждает:

- GetTop возвращает запросы за последние 30 дней, содержащие заданную фразу, плюс похожие запросы;
- `num_phrases` поддерживает 1–2000 результатов;
- seed действительно является входом для раскрытия реальных пользовательских формулировок, но качество входной фразы влияет на полезность получаемого пространства.

### OFFICIAL_YANDEX — Wordstat operators

https://yandex.ru/support2/wordstat/ru/content/operators

Материал подтверждает возможность уточнять измерение операторами `-`, `!`, `+`, кавычками, `[]`, `()` и `|`, когда конкретный исследовательский вопрос требует ограничения шума или формы.

### OFFICIAL_YANDEX — Yandex Search API pricing

https://aistudio.yandex.ru/ru/docs/search-api/pricing

Текущая опубликованная цена GetTop: 20 ₽ за 1000 запросов. Это означает, что прямой Yandex API cost сам по себе не оправдывает отказ от нескольких дополнительных probes, если они реально увеличивают качество/coverage. Фактическая стоимость через Yandex Marketing Bridge может иметь дополнительную provider/bridge экономику и должна считаться отдельно на Step 03.

### INDUSTRY_PRACTICE — Ahrefs: Seed Keywords

https://ahrefs.com/blog/seed-keywords/

Материал подтверждает:

- seed keywords — стартовые входы для раскрытия большего keyword universe, не финальные SEO-решения;
- качество результата зависит от качества и разнообразия seed list;
- важны очевидные вариации/синонимы;
- competitor keywords/SERPs/navigation могут раскрыть пропущенные seed terms.

Competitor-derived expansion в KW-002 сознательно вынесен в Steps 06–08, поэтому отсутствие competitor input на первом Step 02 само по себе не считается ошибкой, если последующие шаги действительно выполняются.

### INDUSTRY_PRACTICE — Semrush: Seed Keywords / Ecommerce Keyword Research

https://www.semrush.com/blog/seed-keywords/
https://www.semrush.com/blog/ecommerce-keyword-research/

Материалы подтверждают:

- seed terms должны быть базовыми/фундаментальными и напрямую связанными с предложением;
- после seed discovery проверяются relevance, volume и intent;
- для ecommerce важна коммерческая релевантность, но commercial/transactional modifiers не обязаны быть каждым initial seed — они могут быть обнаружены и затем оценены как реальные пользовательские запросы.

## 3. Что в нашей работе сделано правильно

### PASS A — `SEED != FINAL KEYWORD`

Все 97 строк имеют `DISCOVERY_PROBE`, нет KEEP/REJECT/cluster/page решений.

Это полностью согласуется с Yandex/Ahrefs/Semrush: seed — старт исследования, а не финальное ключевое слово.

### PASS B — происхождение seed сохранено

Есть `seed_source_type`, source product/client fact, exact source terms и purpose.

Это сильная сторона текущей реализации: analyst-composed probes не выданы за слова клиента.

### PASS C — присутствуют базовые слова бизнеса

`амулет`, `оберег`, `талисман`, `чётки`, `талисман в машину` и отдельные named-product terms дают несколько разных входов, а не один общий root.

### PASS D — не было преждевременного SEO

Step 02 не создавал интент, кластеризацию, page ownership или IA.

### PASS E — competitor expansion не потерян, а отложен методически

Ahrefs рекомендует competitors/SERPs/navigation как источник новых seed ideas. В KW-002 это реализуется позже через Steps 06–08 после первичного demand collection. Это допустимая staged architecture, а не текущий дефект.

## 4. Найденные дефекты

### DEFECT 1 — catalog route coverage был ошибочно принят за search-discovery quality

Текущий QA доказывал:

```text
76 cards
→ each card has at least one primary seed route
```

Но это доказывает только lineage/accounting.

Оно НЕ доказывает:

```text
the route is sufficiently specific
route represents likely user wording
route can reveal relevant product demand without dominant unrelated noise
```

Примеры bare primary seeds с высокой/очевидной неоднозначностью:

```text
RSOTM
Soldier Of Fortune
Древо Жизни
Ом
Жива
Мара
Хорс
Чур
Перун
Сварог
Кровь и Песок
```

Некоторые из этих запросов могут быть полезными diagnostic probes, но наличие такого probe не должно считаться достаточным доказательством качественного покрытия товара.

**Verdict:** substantive defect.

### DEFECT 2 — high-noise bare names оставлены PRIMARY без обязательного refinement route

Яндекс прямо рекомендует конкретизировать слишком общие запросы.

В текущем `STEP_02_SEED_MAP.csv` ряд high-noise names имеет:

```text
priority = PRIMARY
known_noise_risk = HIGH
```

но не имеет обязательного поля:

```text
refinement_strategy
qualified_primary_seed
negative/noise handling plan
```

Это внутренне противоречиво: мы признали высокий риск шума, но не потребовали более релевантного parallel route.

**Verdict:** substantive defect.

### DEFECT 3 — use-context synonym coverage несистемна

Из confirmed business facts мы знаем, что часть ассортимента предназначена для автомобиля.

Текущие analyst-composed primary probes в основном используют форму `в машину`:

```text
чётки в машину
амулет в машину
оберег в машину
```

Но Yandex guidance отдельно рекомендует учитывать основные синонимы/варианты пользовательского языка.

Для автомобильного контекста не проверены как отдельные discovery routes, например:

```text
машина
авто
автомобиль
для машины
для автомобиля
```

Не требуется механически умножать каждое слово на каждую комбинацию. Требуется осмысленный synonym/use-context coverage plan.

**Verdict:** coverage defect.

### DEFECT 4 — exact-name layer перегружает primary set

Из 67 PRIMARY probes значительная доля — exact named products/symbols. Это обеспечивает catalog lineage, но делает acquisition universe сильно зависимым от seller vocabulary.

External guidance рекомендует seeds как фундаментальные входы, а точные names — как один из источников, не единственный центр модели.

Нужен более явный баланс:

```text
broad class
qualified product/use
exact name
alternate wording
brand
```

а не фактическое правило `every distinct seller name -> PRIMARY`.

**Verdict:** design weakness requiring rework before paid acquisition.

### DEFECT 5 — expected_information_gain местами формальный, а не discriminating

У большого числа exact-name seeds практически один и тот же шаблон:

```text
"Высокий для покрытия конкретного ассортиментного названия..."
```

Это объясняет lineage, но не доказывает, почему именно этот bare form должен быть PRIMARY вместо qualified/deferred form.

Level-1 information-gain discipline требует реального различия между:

```text
important now
useful later
likely redundant
high-noise control
```

**Verdict:** QA defect.

### DEFECT 6 — deferred variants нельзя оправдывать экономией provider calls

30 probes были отложены по information-gain логике, что само по себе допустимо.

Но официальный direct Yandex Search API tariff для GetTop составляет 20 ₽ / 1000 requests. Разница между 67 и 97 GetTop requests по этой базовой цене составляет только 0.60 ₽. Поэтому provider cost не должен использоваться как аргумент против distinct lexical probe, если он реально улучшает coverage.

Это НЕ означает «запускаем все 97 обязательно». Это означает: решение PRIMARY/DEFERRED должно опираться прежде всего на information gain и noise, а не на экономию нескольких запросов.

**Verdict:** correction to prioritization rationale.

## 5. Что НЕ считаю дефектом

### Необязательность `купить / цена / заказать` как каждого seed

Semrush/Ahrefs описывают seeds как broad/foundational inputs, а Yandex GetTop сам возвращает containing/similar queries. Поэтому отсутствие blanket-комбинаций `купить + каждый товар` не является ошибкой само по себе.

Однако для конкретных неоднозначных bare names commercial/product qualifiers могут быть полезны именно как refinement probes.

### Отсутствие competitor-derived seeds на Step 02

Внешние материалы считают competitors полезным источником семантики, но KW-002 имеет отдельный controlled loop Steps 06–08. Поэтому это не current-step failure.

### Отсутствие окончательного intent

Intent должен определяться позже на реальных query/SERP evidence. Step 02 правильно не создавал final intent labels.

## 6. Дополнительный handoff item для Step 03

Yandex Wordstat GetTop позволяет задавать `num_phrases` от 1 до 2000.

Следовательно до provider execution Step 03 обязан явно заморозить:

```text
num_phrases/result depth
regions
all-device/default device policy
complete results + associations persistence
pagination/complete-return expectations of the Bridge
```

Это не причина rework Step 02 само по себе, но без этого нельзя считать Step 03 provider contract готовым.

## 7. Внешний аудит — итоговый verdict

```text
STEP_02_PREVIOUS_PASS = INVALIDATED_BY_LATE_EXTERNAL_METHOD_REVIEW
STEP_02_STATUS = REWORK_REQUIRED
STEP_03_ALLOWED = false
```

Сильные части сохраняются:

```text
source lineage
DISCOVERY_PROBE boundary
97-row history
coverage matrix as catalog-lineage accounting
separation of primary/deferred
no old-research contamination
```

Нужно исправить:

```text
1. replace card-route coverage with search-probe-quality coverage;
2. require qualified/refinement route for high-noise bare seeds;
3. add systematic but bounded synonym/use-context coverage;
4. rebalance exact-name vs broad/qualified probe mix;
5. replace boilerplate information-gain text with discriminating rationale;
6. re-evaluate PRIMARY vs DEFERRED independent of trivial direct API cost;
7. rerun adversarial QA and remote readback.
```

## 8. Простыми словами

### Что оказалось правильным

Мы правильно сделали главное: не назвали seeds готовыми ключами, сохранили их происхождение и не полезли раньше времени в кластеры/страницы.

### Что оказалось неправильным

Мы слишком легко считали товар «покрытым», если у него просто есть какой-то seed. Для части товаров этим seed было одно неоднозначное название. Такое слово может привести Wordstat в совсем другую тему и не дать хороший путь к товарному спросу.

### Что нужно сделать

Перед Wordstat нужно пересобрать primary seed set так, чтобы у неоднозначных названий был не только bare-name probe, но и понятный квалифицированный/товарный маршрут, а автомобильная лексика проверялась не одной формой `в машину`.

### Что это даёт

После исправления первый Wordstat-сбор будет меньше зависеть от названий карточек продавца и лучше раскроет реальный язык покупателей. До этого запускать Step 03 нельзя.
