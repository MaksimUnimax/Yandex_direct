Yandex Marketing Bridge 0.1.9

Production-сборка с ручным deferred Search, устойчивостью job между ChatGPT-диалогами и исправленным локальным отображением Deferred Search в popup.

start сохраняет задание; submit/submitN отправляет отдельные поисковые запросы и сохраняет operation_id; collect/collectN/collectReady позже получает готовые результаты.

Deferred Search job принадлежит Search credential scope (folder_id), а не UUID конкретного ChatGPT-диалога. Новый привязанный диалог с тем же Search folder может продолжить status/itemsPage/exportPage/pause/resume/submit/collect того же job. Сам диалог по-прежнему обязан пройти live binding + Manual + active Search authority checks. Другой folder получает отказ через owner/folder guards.

Popup теперь читает persisted Deferred Search job по тому же durable owner `search-folder:<folder_id>`. Popup refresh только локально читает extension state и IndexedDB: он не делает submit, collect, provider polling, retry и не меняет revision. Conversation key используется отдельно только для action authority.

Paused Autorun budget mirror хранит отдельного conversation owner и не смешивается с durable owner данных job.

В manifest разрешены оба адреса Яндекса:
- https://searchapi.api.cloud.yandex.net/*
- https://operation.api.cloud.yandex.net/*

Фонового deferred Autorun, chrome.alarms, скрытых retry и автоматического повтора неизвестного платного запроса нет. Получение результата запускается явно.

Cross-owner export bypass отсутствует: exportPage идёт через обычный owner-guarded exporter. Jobs старой conversation-owned схемы не мигрируются; их надо создать заново.
