Yandex Marketing Bridge 0.1.8

Production-сборка с ручным deferred Search и нормальной устойчивостью job между ChatGPT-диалогами.

start сохраняет задание; submit/submitN отправляет отдельные поисковые запросы и сохраняет operation_id; collect/collectN/collectReady позже получает готовые результаты.

Deferred Search job теперь принадлежит Search credential scope (folder_id), а не UUID конкретного ChatGPT-диалога. Новый привязанный диалог с тем же Search folder может продолжить status/itemsPage/exportPage/pause/resume/submit/collect того же job. Сам диалог по-прежнему обязан пройти live binding + Manual + active Search authority checks. Другой folder получает отказ через owner/folder guards.

Paused Autorun budget mirror хранит отдельного conversation owner и не смешивается с durable owner данных job.

В manifest разрешены оба адреса Яндекса:
- https://searchapi.api.cloud.yandex.net/*
- https://operation.api.cloud.yandex.net/*

Фонового deferred Autorun, chrome.alarms, скрытых retry и автоматического повтора неизвестного платного запроса нет. Получение результата запускается явно.

В 0.1.8 нет cross-owner export bypass: exportPage идёт через обычный owner-guarded exporter. Jobs старой conversation-owned схемы не мигрируются; их надо создать заново.
