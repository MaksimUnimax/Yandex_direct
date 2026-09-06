# OKNO_MSK — document №01 owner-review checkpoint

Дата checkpoint: 2026-09-06  
Класс: `POST_RELEASE OWNER REVIEW / DOCUMENT_01_ONLY`  
Статус: `IN_PROGRESS__CHECKPOINT_COMMITTED`  
Документы №02 и №03: `NOT_STARTED_BY_THIS_OWNER_REVIEW`

## 1. Live GitHub authority

Проверка начата от remote branch HEAD:

```text
d1026e64a344321201831622601bd02cad334270
```

Это readback-commit поверх материального исправления:

```text
9f18834d8e7f812cbac3da503a53377dc9c072d0
```

Материальный diff `21a2d87e9c8755cfe6fdeb4121637796ae692033 -> 9f18834d8e7f812cbac3da503a53377dc9c072d0` содержит 13 путей и не содержит recipient-файлов документа №02 или №03. Граница targeted rework соблюдена.

## 2. Уже независимо подтверждено owner review

### QF003

Recipient source показывает для `QF003 — алюминиевые окна для частного дома`:

- историческое `representative_query` не заполнено и не переписано;
- display title буквально разрешён против current Stage-5;
- semantic state `ASSIGNED`, uncertainty `NONE`;
- structural unit `ALUMINIUM_WINDOWS_COMMERCIAL`;
- exact semantic owner `https://okno-msk.ru/alyuminievye-okna/`;
- supporting page `https://okno-msk.ru/alyuminievye-okna/provedal`;
- structural action `KEEP_EXISTING_STRUCTURE`;
- отдельно сказано, что exact Stage-13 Search для этого текста не сохранён и semantic assignment не является выдуманным Search-наблюдением;
- отдельная CMS-команда из QF-карточки не выводится.

### Generalized generator rule

`tools/post_release_correction/generate_recipient_correction.py` больше не трактует пустой `representative_query` как автоматический family-only. Текущий resolver:

1. использует stored representative query, если он есть;
2. иначе проверяет normalized display title против current Stage-5;
3. только при отсутствии обоих совпадений разрешает `TRUE_FAMILY_ONLY`.

Это обобщённая коррекция класса дефекта, а не QF003-only hardcode.

### Independent deterministic QA

`tools/post_release_correction/qa_document_01.py` не импортирует resolver генератора. Он независимо строит semantic lookup, независимо задаёт/проверяет display titles для historically blank representative cases и fail-closed проверяет exact-title semantic owner, provenance и Search boundary.

Committed deterministic result:

```text
status = PASS
checks = 298
failed = 0
QF = 21/21
corrected = 9
unresolved = 0
```

Evidence classes:

```text
16 = stored representative + exact Stage-13
1  = QF003, Stage-5 exact-title without stored representative
4  = QF008/QF009/QF011/QF021 true family-only
```

QF003 больше не имеет ложного `NOT_APPLICABLE` exact owner.

## 3. Physical materialization evidence read back

Committed physical QA после QF003 rework является новым, а не повторно использованным 57-page результатом:

```text
DOCUMENT_01_PHYSICAL_PDF_QA = PASS__58_OF_58_PAGES
```

В authority зафиксированы новая пересборка Markdown -> DOCX -> PDF, `58/58` page render review, QF003 на страницах 6–7, сохранённая partial-boundary S18-A012, отсутствие clipping/overlap/blank-page defects и raster edge/blank scan `58/58 PASS`.

Owner-review environment не смог выполнить второй независимый binary render: локальный container не имеет DNS-доступа к GitHub, а GitHub connector не отдаёт repository PDF/DOCX bytes как локальный файл. Это ограничение среды проверки, а не обнаруженный дефект recipient artifact. Поэтому owner verdict на этом checkpoint ещё не повышается до PASS.

## 4. Что ещё должно быть закрыто перед owner PASS

- дочитать и сверить все owner gate criteria по №01, включая Search 75/75, AI 8/8, action map 34/34, uncertainty/reopen rules и positive KEEP/NO_CHANGE;
- подтвердить S18-A012 и итоговые action counts по current authority;
- сверить manifest/state/cursor/readback и material hashes/blob identity;
- убедиться, что текущие owner-review/state artifacts не содержат противоречивого gate;
- после полного owner verdict записать отдельный owner PASS либо REWORK commit и сделать remote readback.

## 5. Defect-retention rule

В owner-review сохраняется правило:

```text
DEFECT
-> affected artifact
-> violated authority
-> root cause
-> correction
-> generalized prevention rule
-> independent regression / QA invariant
-> affected documents
-> verification result
-> correction commit
```

QF003 классифицирован как `EMPTY_REPRESENTATIVE_QUERY_MASKED_EXACT_STAGE5_TITLE_MATCH`; root cause и generalized prevention rule подтверждены в generator + independent QA.

## 6. Gate на checkpoint

```text
CURRENT_DOCUMENT = 01
DOCUMENT_01_ANALYST_RECHECK = PASS
DOCUMENT_01_OWNER_REVIEW = IN_PROGRESS__CHECKPOINT_COMMITTED
DOCUMENT_02_OWNER_REVIEW = PENDING
DOCUMENT_03_OWNER_REVIEW = PENDING
FINAL_OWNER_RECIPIENT_ACCEPTANCE = OPEN
NEXT_ACTION = CONTINUE_OWNER_REVIEW_DOCUMENT_01
```

Новые Yandex/Wordstat/GenSearch/Alice/provider-вызовы: `0`.
