# OKNO_MSK — GitHub readback исправленного получательского выпуска

**Дата:** 2026-09-05  
**Репозиторий:** `MaksimUnimax/Yandex_direct`  
**Ветка:** `roadmap/kwork-productization-2026-08-28`  
**Исходный HEAD:** `a54522282ea417dc7b738da12e15bf98bd0cb2ba`  
**Результат:** `PASS`

## Запись

1. `f99beaea8855d5cd7a0ed5737d5b536b2ee7d912` — основной 25-файловый correction/materialization commit.
2. `a22c4be3298ac3026f43c436a2e29970198db89c` — восстановление полного blob №03 после того, как identity-readback выявил обрезку большого файла транспортным пределом промежуточного base64-канала. Обрезанная версия не была принята как успешная; ветка сразу переведена на полный blob.

Полный №03 после коррекции: Git blob `573a249b847c015edd569fa741b889c824e7bc83`, 1,119,673 bytes, SHA-256 `d5c90cf187041e975f17d03a2be138eff0b6a06bfe1b7d395a3b24547edc62b0`.

## Identity readback

После второго commit remote tree `5e47f9bb162d39ae9918fd210074de91ca9ba752` прочитан через GitHub Git Data API. Все 25 созданных/изменённых путей сравнены с локальным принятым commit по Git blob SHA и размеру:

```text
FILES_CHECKED = 25
BLOB_SHA_OR_SIZE_MISMATCHES = 0
RESULT = PASS
```

## Content readback

Через GitHub connector отдельно прочитаны и проверены:

- обе PDF delivery-формы и обе DOCX editable-формы — base64 content readback + exact Git blob identity PASS;
- полный №03 — blob content readback от заголовка до финальной физической access-границы; секции semantic universe, uncertainty и `SP09-075` присутствуют;
- source Markdown №01 и №02 — обязательные material Search/decision/implementation секции присутствуют;
- `README_RU.md` и corrected release manifest — one-file №03 contract и роли получателей присутствуют;
- shared implementation authority, recipient QA и physical QA — corrected states и PASS-границы присутствуют;
- owner review closure, current post-release state, execution cursor и execution log — correction completion и owner recheck boundary присутствуют.

Final remote state after state/readback finalization must retain:

```text
CORRECTION_MATERIALIZATION = COMPLETE
ANALYST_RECIPIENT_QA = PASS
GITHUB_READBACK = PASS
OWNER_RECHECK = REQUIRED
NEXT_ACTION = OWNER_RECHECK_CORRECTED_RECIPIENT_DOCUMENTS_01_02_03
```

Новые provider-вызовы: 0. Платная стоимость: 0 ₽. Step 21/22 не выполнялись. Исторический выпуск и исторический JSON №03 не переписаны.

## Readback аналитического исправления документа №01

**Исходный remote HEAD перед исправлением:** `d62d356d731adc2b6be2f57cb27c4c4de8576568`  
**Материальный correction commit:** `9ddcbeab6dd07f834c08604f7dbad77b15b1525b`  
**Материальных путей:** 18  
**Результат:** `PASS`

После публикации commit прочитан через GitHub connector. Список изменённых файлов равен локальному принятому набору: canonical source №01, DOCX, PDF, shared implementation authority, generator/build/QA scripts, manifest, QA/state/tracking artifacts. Файлы №02 и №03 не изменялись.

Отдельный content readback подтвердил:

- source №01 показывает QF001 exact owner `https://okno-msk.ru/alyuminievye-okna/` и явное правило exact/family/supporting/action;
- `S18-A012` имеет `READY_PARTIAL__BUSINESS_DETAIL_REQUIRED` и видимую границу `PENDING_BUSINESS_DETAIL`;
- dedicated QA из GitHub содержит `285` checks, `failed = 0`, QF `21/21`, Search `75/75`, AI `8/8`;
- cursor/state содержат `DOCUMENT_01_ANALYST_RECHECK = PASS`, `DOCUMENT_01_OWNER_REVIEW = PENDING`, `CURRENT_DOCUMENT = 01`, `NEXT_ACTION = OWNER_REVIEW_CORRECTED_DOCUMENT_01`;
- manifest содержит актуальные размеры, SHA-256 и `57` страниц документа №01.

Binary identity readback:

```text
PDF  Git blob = f52670450af4fa2b989cfefa54a90e85e292ffd4
DOCX Git blob = 7fd67191357992565204352bb0ae57dcef77911b
PDF  SHA-256 = d7bfe30b988b8a0153e115de149ddc9009399993cca6672c1180c1a4d6d5418e
DOCX SHA-256 = 3abb350815807506ce3223e740a62d125fd2c6c47aaad85531c96758ec9ffecf
SOURCE SHA-256 = 13f0c116cf57061f1325a77be1d07457ca3b0749bd4251b9ccf4714fbf955b10
RESULT = PASS
```

Final document №01 gate after readback:

```text
DOCUMENT_01_ANALYST_RECHECK = PASS
DOCUMENT_01_OWNER_REVIEW = PENDING
DOCUMENT_02_OWNER_REVIEW = PENDING
DOCUMENT_03_OWNER_REVIEW = PENDING
FINAL_OWNER_RECIPIENT_ACCEPTANCE = OPEN
NEXT_ACTION = OWNER_REVIEW_CORRECTED_DOCUMENT_01
```

## Повторный GitHub readback после owner-review исправления QF003

**Исходный remote HEAD перед rework:** `21a2d87e9c8755cfe6fdeb4121637796ae692033`

**Материальный correction commit:** `9f18834d8e7f812cbac3da503a53377dc9c072d0`

**Материальных путей:** 13

**Результат:** `PASS`

Коммит опубликован fast-forward и прочитан обратно через GitHub connector. Remote source №01 подтверждает, что QF003 сохраняет исторически пустое поле `representative_query`, но разрешает буквальное совпадение заголовка с текущей Stage-5-фразой `алюминиевые окна для частного дома`. Карточка показывает `ASSIGNED`, единицу `ALUMINIUM_WINDOWS_COMMERCIAL`, коммерческую задачу, exact owner `https://okno-msk.ru/alyuminievye-okna/`, supporting page `/alyuminievye-okna/provedal`, действие `KEEP_EXISTING_STRUCTURE` и отдельно сообщает об отсутствии выполненного exact Search-прохода.

Независимый QA readback подтвердил:

- `298/298` checks, `failed = 0`;
- QF `21/21`, исправлено `9`, unresolved `0`;
- доказательные классы QF: `16` stored representative + exact Stage-13, `1` Stage-5 exact-title без stored representative (`QF003`), `4` true family-only (`QF008`, `QF009`, `QF011`, `QF021`);
- Search `75/75`, AI `8/8`;
- `S18-A012 = READY_PARTIAL__BUSINESS_DETAIL_REQUIRED` и итоговые action counts не регрессировали;
- PDF №01 имеет `58` страниц; manifest/state/cursor содержат текущие gate и hashes;
- файлы №02 и №03 отсутствуют в 13-путевом diff и не продвигались.

Binary/source identity readback:

```text
PDF    Git blob = dccd14c75fe9520721b468f5690dba31edbd5c63
DOCX   Git blob = cd874e0aab3dd57ac0311c43694f3c752f032a4f
SOURCE Git blob = cbb51296badced35716cd215c78f05f3dc361d45
PDF    SHA-256 = 1af28c2ab65641e9c89baea90054da9cf7bed234421e2beeef1ce697445cbb00
DOCX   SHA-256 = 4a44d1ccc37be4a676599de58818e6c2381b74f79781c1cfbe98fa7b7c019cc8
SOURCE SHA-256 = 19bb1abf0793427b4c339b5533b9aad2f7cb2ebee2d2a3f86cd7ad2e2850fe62
RESULT = PASS
```

Final document №01 gate after repeated readback:

```text
CURRENT_DOCUMENT = 01
DOCUMENT_01_ANALYST_RECHECK = PASS
DOCUMENT_01_OWNER_REVIEW = PENDING
DOCUMENT_02_OWNER_REVIEW = PENDING
DOCUMENT_03_OWNER_REVIEW = PENDING
FINAL_OWNER_RECIPIENT_ACCEPTANCE = OPEN
NEXT_ACTION = OWNER_REVIEW_CORRECTED_DOCUMENT_01
```

Новые provider-вызовы: `0`. Step 21/22 не выполнялись.
