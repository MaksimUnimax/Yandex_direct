# OKNO_MSK — инструкция к self-contained AI knowledge document

**Дата:** 2026-09-05  
**Статус:** CURRENT / SELF-CONTAINED / QA PASS

Основной AI-артефакт: `RESEARCH_REBUILD_STAGE_11_AI_KNOWLEDGE_DOCUMENT_2026-09-05.json`.

## Назначение

Документ рассчитан на AI-систему без доступа к GitHub, прежним чатам, Yandex/provider API и live-сайту. Он встраивает весь текущий семантический master (2 840 строк), 168 канонических единиц, 34 действия и их реализационные спецификации, Search/AI evidence layer, 21 Search-case explanation, 15 ссылок, 46 маршрутов, текущие page-validations и 221 запись неопределённости.

## Как отвечать

Для каждого вывода использовать схему:

**факт → объект доказательства → поддержанный вывод → ограничение → действие или явное отсутствие действия**.

Нельзя:

- брать исторический клиентский пакет как текущую истину;
- заменять задачу/intent/role полями от старой единицы после correction;
- превращать неопределённость в решение;
- переносить exact-query Search observation на всё семейство без записанной границы;
- считать AI-ответ ценностью без decision delta;
- выполнять NOT_READY/HOLD;
- советовать merge/delete/redirect для overlap-кейса без нового доказательства.

## Приоритет данных

1. `semantic_master`;
2. `canonical_units`;
3. `implementation_specifications`;
4. link/routing specs;
5. evidence register и AI causal cases;
6. residual uncertainty.

## Проверенная сводка

- 2 840 исходных уникальных фраз сохранены;
- 2 313 назначены;
- 19 SEARCH_REQUIRED;
- 174 REVIEW_DEFERRED;
- 334 EXCLUDED_PRESERVED;
- 168 структурных единиц;
- 69 атомарных semantic corrections;
- 34 действия;
- 0 new-page actions;
- AI: 0 CHANGE / 4 DE_RISK / 3 NO_CHANGE / 1 INSUFFICIENT;
- 0 AI architecture changes.

Любой иной итог должен быть объяснён новым, явно предоставленным authority, а не догадкой.
