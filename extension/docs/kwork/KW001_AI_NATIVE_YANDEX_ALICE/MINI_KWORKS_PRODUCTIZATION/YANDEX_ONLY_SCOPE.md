# MINI-KWORKS — YANDEX-ONLY SCOPE BOUNDARY

Status: **MANDATORY / CROSS-PRODUCT / OWNER-DIRECTED**

## 1. Главная коммерческая граница

Все семь mini-kwork этой серии выполняются **только под экосистему Яндекса**.

Базовая формулировка для клиентских материалов:

> Работа выполняется только для экосистемы Яндекса: Яндекс Wordstat, обычная выдача Яндекса и, в тех продуктах, где это прямо входит в состав, Алиса / Яндекс Нейро / GenSearch. Google Ads / Google Keyword Planner, Google Search, Google Search Console и другие Google-инструменты в работу не входят.

## 2. Что разрешено как рабочее evidence в серии

В зависимости от конкретного mini-kwork могут использоваться:

- Яндекс Wordstat — спрос/частотность и расширение семантики;
- обычная выдача Яндекса — Search evidence, конкуренты, интент, владельцы страниц и иные решения только в пределах доказанного метода;
- Алиса / Яндекс Нейро / GenSearch — только в продуктах, где AI-layer входит в обещание, с сохранением установленных claim boundaries;
- публичные страницы сайта клиента и конкурентов;
- Яндекс Вебмастер / Метрика / Директ — только как optional private evidence, когда это отдельно доступно, разрешено и действительно требуется конкретному продукту.

## 3. Что НЕ входит

Без отдельной новой методики, теста и коммерческого решения запрещено включать или обещать:

- Google Ads;
- Google Keyword Planner;
- Google Search как provider/validation surface исследования;
- Google Search Console;
- Google Trends;
- Google Analytics как обязательный источник;
- SEO/семантику «под Яндекс и Google»;
- объединённую частотность Яндекс + Google;
- проверку позиций/интентов/кластеров по Google SERP;
- любые выводы о Google, полученные по аналогии из Яндекс evidence.

## 4. Обязательные места явного указания Yandex-only boundary

Одной ссылки на этот файл недостаточно. Явная клиентская формулировка должна присутствовать в каждом будущем продукте минимум в:

```text
PRODUCT_ROADMAP.md
PRODUCT_SCOPE.md
CLIENT_INPUT_CONTRACT.md
DELIVERABLE_SPEC.md
KWORK_CARD.md
FAQ / ограничения карточки
TEST_ORDER.md
CLIENT_DELIVERABLE.md
QA_AND_RELEASE.md / QA.md
```

Если создаётся XLSX/DOCX/PDF, область исследования должна быть понятна получателю и там; нельзя полагаться только на внутренний markdown.

## 5. QA gate

Мини-кворк не готов к публикации, если выполняется хотя бы одно:

```text
CARD_SAYS_GENERIC_SEO_WITHOUT_YANDEX_SCOPE = FAIL
CARD_IMPLIES_GOOGLE_SUPPORT = FAIL
CLIENT_INPUT_REQUESTS_GOOGLE_DATA_AS_REQUIRED_BASE_INPUT = FAIL
METHOD_USES_GOOGLE_PROVIDER_WITHOUT_SEPARATE_APPROVED_METHOD = FAIL
REPORT_MIXES_YANDEX_AND_GOOGLE_EVIDENCE = FAIL
MARKET_ANALOG_MENTION_OF_GOOGLE_IS_REFRAMED_AS_OUR_CAPABILITY = FAIL
```

PASS требует:

```text
YANDEX_ONLY_SCOPE_EXPLICIT_IN_CARD
+ YANDEX_ONLY_SCOPE_EXPLICIT_IN_CLIENT_INPUT
+ YANDEX_ONLY_SCOPE_EXPLICIT_IN_DELIVERABLE
+ NO_UNAPPROVED_GOOGLE_PROVIDER_DEPENDENCY
+ NO_GOOGLE_CAPABILITY_PROMISE
```

## 6. Рыночные аналоги

При изучении Kwork/FL.ru можно использовать реальный аналог, который сам предлагает Яндекс + Google, **только как рыночный ориентир**. В нашей карточке его Google-часть не наследуется и не считается нашей возможностью.

## 7. Будущее расширение

Если позже будет решено продавать Google-направление, оно не добавляется одной строкой в текущие продукты. Сначала требуется отдельная методика, provider/evidence model, тестовый заказ, failure-class audit, deliverable QA и owner acceptance. До этого текущая серия остаётся Yandex-only.
