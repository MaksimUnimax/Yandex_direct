# B5 — общий допуск старого и отложенного Search

Дата: 2026-09-12. Начальный live HEAD: `816186db1479ce0be9ef8c41b3b3cd88c522a9cf`.

Прочитаны актуальный continuation cursor, обязательное правило зависимости/ресурсов и сохранённый B4 policy. Точный предоставленный ZIP 0.1.4 проверен локально: SHA-256 `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`, 53 файла. Старые A/B1/B2/B3/B4 не разрабатываются заново.

## Цель блока

Закрыть подтверждённый в B4 разрыв: legacy sync Search/GenSearch и deferred должны резервировать разрешение до сети через одну атомарную процедуру. Простое чтение прежних run counters не является общим резервированием. Требуется сохранить старые формат ответа, маршрутизацию других сервисов, credentials и quota/policy запреты.

## Область влияния

- B4 admission store: общий бюджет/попытки и исходы для sync, genSearch, deferred submit/collect.
- Фактический legacy отправитель `shared/phase3_provider_runtime.js` из owner 0.1.4: узкий hook до fetch и settlement после результата; Wordstat/Webmaster без изменений поведения.
- Связанный worker: доверенная привязка metadata к owner/run; credential Check рассматривается отдельно, не подменяется обычным чат-запросом.
- Полные provider ответы не попадают в admission records; одна попытка — небольшая запись.
- Проверки: одновременное резервирование разных режимов, no double count с прежними totals, no request on denial, unknown/recovery, permission/channel/credential boundary, повтор settlement, exact baseline provider regression.

## Состояние

Код B5 ещё не принят. Существующие браузерные/resource ограничения не закрыты. Ни установленная сборка, ни готовый ZIP в этом блоке не выдаются.

RELEASE_ALLOWED = NO
NEW_PROVIDER_CALLS = 0

## Материалы

Перепроверены официальные страницы Search API pricing и limits, IndexedDB transaction contract. Day estimates: sync 0.488 RUB, deferred 0.0305 RUB, genSearch 5.08 RUB. Это оценки, не счёт. Перечень неизменяемых legacy контрактов берётся из фактических исходников owner ZIP.
