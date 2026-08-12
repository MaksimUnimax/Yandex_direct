# PROJECT PURPOSE — Yandex Marketing Bridge

Status: current purpose contract.
Updated: 2026-08-12.

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
