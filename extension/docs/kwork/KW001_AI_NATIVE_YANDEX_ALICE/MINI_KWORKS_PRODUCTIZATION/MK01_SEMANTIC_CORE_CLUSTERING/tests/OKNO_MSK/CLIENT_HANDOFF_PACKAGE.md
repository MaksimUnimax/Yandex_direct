# OKNO_MSK — CLIENT HANDOFF PACKAGE EXAMPLE

Status: **CURRENT ANALYTICAL CLIENT PACKAGE / OWNER REVIEW NEXT**

This file shows the current MK01-only delivery package after the analytical client-report rebuild dated 2026-09-10.

## What is delivered to the client

1. Working semantic-core workbook:
   `MK01_OKNO_MSK_SEMANTIC_CORE_2026-09-09.xlsx`
2. Current analytical report:
   `MK01_OKNO_MSK_CLIENT_REPORT_2026-09-10.pdf`
3. Short marketplace/chat handoff message attaching both files.

A standalone TXT file is not a deliverable. Internal TSV/TSV.GZ, manifests, QA JSON, build receipts, source-authority audits and rule files are production evidence and are not automatically sent.

## Current report identity

```text
PDF SHA-256 = 9faae858b40a5e6617019f0688759d11034f27d4d800b3b46dc180461788764b
DOCX SHA-256 = bcc83a4c350a0144333635d1b2fe989d70907490070ec41fcb2af32a07263057
PDF descriptive pages = 8
ANALYTICAL QA = 25 PASS / 0 FAIL
```

Page count is descriptive only, not a quality target.

## Ready handoff message

Здравствуйте!

Готово семантическое ядро для сайта **okno-msk.ru** по региону **Москва**.

Прикладываю два итоговых документа:

- **Excel с семантическим ядром** — основной рабочий файл;
- **PDF-отчёт** — краткая аналитическая выжимка: что показал собранный спрос, как устроено рабочее ядро, какие группы крупнейшие, что осталось на проверку и что было исключено.

### Итоговые цифры

- исходных наблюдений Яндекс Вордстата: **2 965**;
- уникальных сохранённых фраз: **2 840**;
- рабочее семантическое ядро: **2 185**;
- на дополнительную проверку: **187**;
- исключено с сохранением причины: **468**;
- смысловых групп: **59**;
- рабочих групп: **54**.

В рабочем ядре **1 799 фраз (82,3%)** относятся к коммерческим и сервисным задачам. Десять крупнейших смысловых групп содержат **1 455 фраз (66,6%)** рабочего корпуса по количеству формулировок. Эти доли описывают состав семантики, а не долю рынка или прогноз трафика.

Начните с PDF, чтобы быстро понять выводы исследования, затем используйте Excel для практической работы. В Excel основной лист — **«Рабочее ядро»**, структура групп находится на листе **«Группы запросов»**, спорные формулировки — в **«На проверку»**, исключённые с причиной — в **«Исключено»**.

Показатели Вордстата собраны в широком режиме без операторов, поэтому они помогают сравнивать формулировки внутри исследования, но не являются точной частотностью конкретной фразы, числом уникальных пользователей или прогнозом трафика.

Работа выполнена по поисковому спросу **Яндекса**. Google в результат не входит.

В MK01 также не входят назначение запросов конкретным URL, проект SEO-архитектуры, конкурентный анализ, ТЗ разработчику и анализ Алисы/Яндекс Нейро — это отдельные задачи.

## Current analytical findings reflected in the PDF

```text
WORKING CORE = 2185
COMMERCIAL = 1112 / 15 groups
SERVICE = 687 / 20 groups
INFORMATIONAL = 299 / 14 groups
SELF-SERVICE INFORMATIONAL = 74 / 4 groups
NAVIGATIONAL = 13 / 1 group

TOP-10 GROUPS = 1455 phrases / 66.6% of working corpus

REVIEW = 13 Search-required + 174 deferred = 187
EXCLUDED = 180 scope + 120 irrelevant + 34 mechanical + 134 outside-task = 468
```

## Supersession note

The earlier report source/PDF dated 2026-09-09 is historical evidence only. It is not the current client-report version because its main weakness was analytical: it described process and counts more strongly than actual demand findings.

Current report authority for client review is the 2026-09-10 analytical rebuild and its manifest/QA.
