# 01 — Краткий итог для клиента

Дата: 2026-09-03  
Сайт: `https://okno-msk.ru/`  
Регион анализа: Москва  
Формат: семантика + структура страниц под обычный Yandex Search с ограниченной диагностической проверкой GenSearch

## Что было сделано

Мы собрали и последовательно проверили спрос, пользовательские задачи, текущие страницы сайта, обычную выдачу Yandex, границы между близкими страницами и 8 специально выбранных Search-vs-AI кейсов. После этого рекомендации были ещё раз сверены с текущим сайтом, чтобы не предлагать новые страницы там, где подходящие URL уже существуют.

Итоговый клиентский пакет использует одну текущую модель данных: фраза → задача → текущая/целевая страница → действие → доказательство → аналитический приоритет → ограничение/следующий шаг.

## Главное о текущей архитектуре

### 1. Базовая структура сайта в целом жизнеспособна

После всех проверок не осталось доказанных оснований создавать новые страницы или делать destructive merge/delete/redirect как обязательное действие:

```text
SUPPORTED NEW PAGE ACTIONS = 0
SUPPORTED DESTRUCTIVE ACTIONS = 0
```

Это важный результат: часть ранних «возможных новых страниц» исчезла после свежей проверки сайта, потому что подходящие specialist pages уже существуют.

### 2. Основная работа — не «наделать страниц», а точнее развести роли существующих

Наиболее важные P1-задачи сейчас включают:

- закрепить отдельную страницу отделки балконов за standalone-задачей;
- вести sliding-only balcony intent на dedicated sliding-balcony page, сохраняя cold owner для явно холодного остекления;
- развести роли двух близких panoramic commercial pages без автоматического merge/delete;
- развести broad private-house page и отдельную cottage/country-house same-task page;
- использовать exact wooden-house specialist вместо broad fallback;
- использовать exact commercial glass-unit hub для коммерческой задачи;
- развести две REHAU comparison pages;
- использовать exact sliding-veranda specialist для раздвижного intent.

То есть приоритетный структурный слой — **правильный владелец задачи и понятные границы между уже существующими URL**.

### 3. Есть несколько сильных контентных доработок на существующих страницах

Среди P1:

- `французские окна` — проверить и при необходимости усилить configuration/replacement и French-vs-panoramic selection depth;
- `окна в частный дом` — добавить стандартные/нестандартные размеры проёмов, sizing guidance и объяснение роли индивидуального замера;
- guide по выбору окон — расширить блоки по фурнитуре, конструкции и брендам;
- `двери REHAU` — добавить door-specific installation scope/process и price/price-estimation guidance.

P2 содержит более узкие support/routing и content задачи: Provedal, cold+panoramic intersections, custom glass-unit manufacturing, apartment-selection support, veranda types/frameless support, ventilation guidance, размеры PVC doors, taxonomy портфолио и две bounded AI-content rechecks.

## Search-vs-AI: что реально показала проверка

Проверялось ровно **8 заранее выбранных exact-query cases**.

Итог:

```text
CHANGE = 0
DE_RISK = 4
NO_CHANGE = 3
INSUFFICIENT = 1
```

AI-проверка **не потребовала менять Search-архитектуру ни в одном кейсе**. Но в трёх случаях она помогла сформировать bounded content candidates:

- panoramic aluminium — проверить explanatory/specification depth внутри текущего aluminium owner;
- French windows — усилить definition/selection depth внутри существующей French page;
- best plastic windows — проверить свежесть ranking evidence, критерии сравнения и методологию.

В остальных кейсах AI либо подтвердил текущую границу, либо данных было недостаточно для безопасного content/action вывода.

Эти 8 наблюдений нельзя превращать в «общую AI-видимость сайта» или прогноз бизнес-эффекта.

## Аналитические приоритеты

Step18 дал:

```text
P1_HIGH = 12
P2_MEDIUM = 20
P3_LATER = 1
HOLD = 1
```

Но две последние строки являются accounting batches. Для исполнения они уже разложены на отдельные работы.

Итоговый execution-addressable слой:

```text
31 exact action packages
15 exact internal-link packages
46 exact route-to-existing packages
20 exact HOLD/recheck packages
TOTAL = 112
```

## Важно: это ещё не календарь внедрения

P1/P2/P3 означают **аналитическую важность по доступным данным**.

Для 92 non-HOLD packages в текущем проекте не подтверждены:

- исполнитель;
- трудозатраты;
- доступная capacity;
- производственный календарь.

Поэтому текущий честный статус:

```text
EXPECTED IMPLEMENTATION PRIORITY = PENDING_CALIBRATION
FINAL SPRINT / CALENDAR ORDER = NOT READY
```

Клиенту не стоит читать P1 как «обязательно первый sprint». Сначала исполнитель должен оценить реальные effort/dependencies/capacity.

## HOLD

20 точных units остаются на HOLD из-за конкретно названных пробелов в evidence/business truth/policy.

HOLD не означает:

- низкую ценность;
- отказ от идеи;
- «не делать никогда».

Это означает только: **нельзя принимать сильное решение, пока не появится конкретно недостающее подтверждение**.

## Что делать дальше с этим пакетом

1. Начать с `05_Page_Actions` в `STEP_19_CLIENT_WORKBOOK_CORRECTED.xlsx` — там конкретно написано, что изменить и чего не делать.
2. Затем открыть `07_Priority_Plan` — он показывает аналитическую важность и связь с 112 work packages.
3. Для семантики открыть лист `03_Semantic_Core` в `STEP_19_CLIENT_WORKBOOK_CORRECTED.xlsx`: 2332 active phrase → task → page rows уже материализованы; ручной JOIN внутренних repo-файлов не требуется. Canonical Step8/10/11 tables остаются источником истины и audit layer.
4. `02_Page_Model` даёт верхнеуровневую карту из 15 направлений.
5. `04_Search_vs_AI` показывает все 8 AI-кейсов с ограничениями.
6. Перед планированием sprint открыть `Execution_Calibration` и получить реальную оценку исполнителя по owner/effort/capacity/dependencies.
7. После внедрения использовать `Measurement`: сначала проверить факт корректной реализации, затем — доступные performance metrics без выдуманных KPI.

## Итог

Главный результат анализа: сайту сейчас не нужен механический рост числа посадочных страниц. Более сильная стратегия — **сохранить доказанные владельцы, точнее развести близкие существующие страницы, правильно маршрутизировать узкие задачи и усилить несколько уже работающих по смыслу страниц там, где текущий evidence действительно показал gap**.

Приоритеты готовы как аналитическая очередь, но production schedule сознательно не сфабрикован: для него нужна реальная калибровка команды внедрения.
