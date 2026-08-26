# PROJECT PURPOSE — Yandex Marketing Bridge

Status: current purpose contract.
Updated: 2026-08-26.

## 1. Цель

Создать одно Chrome/Chromium-расширение **Yandex Marketing Bridge**, через которое ChatGPT сможет безопасно и воспроизводимо работать с официальными маркетинговыми API Яндекса.

Планируемые сервисы:

- Wordstat;
- Yandex Search / SERP;
- Webmaster;
- Metrika;
- Direct.

Расширение отвечает за локальное безопасное исполнение API-команд, credential storage, Manual/Autorun lifecycle, conversation ownership, policy/cost guards, result/error delivery и recovery.

## 2. Критическое разделение Bridge и GitHub

GitHub **не является runtime-сервисом расширения**.

Правильная архитектура:

```text
ChatGPT conversation
        ↕
Yandex Marketing Bridge
        ↕
Yandex APIs

ChatGPT / development workflow
        ↕
GitHub repository MaksimUnimax/Yandex_direct
```

В расширении запрещены как обязательный runtime-контракт:

- `job_id`;
- GitHub token;
- GitHub API;
- repository/branch/commit metadata;
- `work/<job_id>/` path;
- требование существования заказа в GitHub перед API-вызовом.

GitHub используется **снаружи расширения** самим ChatGPT/development workflow для сохранения кода, документации, тестовых checkpoint и рабочих данных заказов.

## 3. Один RUN = один SERVICE

Каждый Autorun RUN принадлежит одному `active_service`.

```text
Start Wordstat RUN
→ Wordstat commands
→ Finish
→ Start Search RUN
→ ...
```

Чтобы сменить сервис, текущий RUN завершается. Assistant text не может сам переключить `active_service`.

`run_id` — внутренний идентификатор безопасного lifecycle расширения. Он не является Job ID и не связывает Bridge с GitHub.

## 4. Manual / Autorun

Bridge сохраняет доказанные reference-механизмы Wordstat/Business Bridge:

- native local Copy остаётся native Copy;
- generic `Copy response` не является API trigger;
- Manual и Autorun взаимно безопасны;
- owner-tab и conversation binding fail-closed;
- один принятый command/transaction не создаёт второй внешний initiation;
- user composer не перезаписывается молча;
- после необратимой границы нет blind retry;
- Pause / Resume / Finish сохраняют lifecycle semantics reference.

Manual на PAUSED RUN использует тот же request/cost budget этого RUN и не может обходить лимит переключением режима.

## 5. Ошибки и Debug Mode

**Любая обнаруженная ошибка во всех режимах автоматически доставляется в связанный ChatGPT conversation.**

Это не зависит от Debug Mode.

- Debug OFF → обязательный компактный `YMB_ERROR_V1`;
- Debug ON → тот же error delivery + дополнительные redacted diagnostic logs.

Recoverable error не должен молча завершать Autorun. Если продолжение безопасно, Bridge возвращает RUN к ожиданию следующей команды.

Если исход внешнего запроса неизвестен, automatic retry запрещён; в ChatGPT отправляется диагностика для reconciliation.

## 6. Credentials и перенос настроек

Credentials хранятся локально в `chrome.storage.local` и не включаются в обычные команды, результаты или error/debug reports.

Для переноса между unpacked installations Bridge должен иметь:

```text
Export settings
Import settings
```

Export intentionally содержит secrets и является секретным backup-файлом.

Import обязан:

- проверять format/version;
- проверять canonical SHA-256;
- merge-ить совместимые настройки;
- сохранять активные RUN/manual-operation safety bindings;
- не заменять активный RUN импортированным состоянием.

При обычном in-place upgrade должны сохраняться proven legacy `wsmb_*` storage keys, включая `wsmb_api_key`.

## 7. GitHub как рабочая память проекта и заказов

Репозиторий делится на:

```text
extension/  — код, reference, tests, docs
work/       — рабочие каталоги реальных заказов
```

Создание и ведение `work/<job_id>/` выполняет ChatGPT/development workflow через подключённый GitHub, **не Chrome extension**.

Туда можно сохранять raw evidence, normalized data, analysis, deliverables и cost/run logs, но никогда secret credentials.

## 8. Source of truth

Для разработки продукта source of truth — live GitHub repository `MaksimUnimax/Yandex_direct` плюс owner-supplied reference artifacts.

Перед продолжением разработки необходимо проверить live HEAD и актуальные docs/gates. Chat history или remembered SHA не заменяют live GitHub.

## 9. Исследование внешних источников и роль Codex

**Запрещено заполнять пробелы в API-контракте догадками.** Если для проектирования, реализации или проверки требуется внешний факт, он должен быть установлен по проверяемому источнику или явно отмечен как неизвестный.

Рабочий порядок получения фактов:

```text
1. live GitHub source of truth проекта
2. актуальная официальная документация/сайт провайдера, доступные ChatGPT
3. Codex как исследовательский инструмент: браузерный поиск, чтение официальных страниц, переходы по документации, скачивание доступных публичных материалов/спецификаций/артефактов и фиксация evidence
4. если нужную информацию не удаётся достать через ChatGPT или Codex — запросить у владельца проекта конкретное действие или конкретный материал
```

Codex в этом проекте **не ограничен ролью QA-исполнителя**. Его разрешено использовать для read-only исследования и сбора информации, в том числе чтобы:

- ходить по официальным сайтам и документации;
- находить актуальные API reference/authorization/quota/error pages;
- проверять browser-only или login-visible страницы, если у Codex есть разрешённый доступ;
- скачивать доступные публичные документы, OpenAPI/spec files, архивы и иные reference materials;
- фиксировать точные URL, заголовки страниц, даты/время проверки и проверяемые факты;
- собирать research snapshot/package для последующего независимого анализа ChatGPT.

Исследовательская задача Codex по умолчанию read-only. Она не даёт разрешения менять production, credentials, настройки внешнего аккаунта или продуктовые bytes. Любое такое изменение требует отдельной явной авторизации.

ChatGPT остаётся владельцем архитектуры и решений: результаты Codex являются evidence/input, а не автоматическим основанием для изменения контракта. Критичные факты должны быть прослеживаемы до источника и перепроверены настолько, насколько это практически возможно.

Если источник отсутствует, недоступен или противоречив, в документации следует писать `UNKNOWN`, `NOT VERIFIED` или явно фиксировать конфликт, а не выбирать удобное значение без доказательств.
