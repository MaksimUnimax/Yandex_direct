Yandex Marketing Bridge 0.1.7

Production-сборка с ручным deferred Search и bounded read-only cross-chat export для полностью завершённых Search jobs.

start сохраняет задание; submit/submitN отправляет отдельные поисковые запросы и сохраняет operation_id; collect/collectN/collectReady позже получает готовые результаты.

В manifest разрешены оба адреса Яндекса:
- https://searchapi.api.cloud.yandex.net/*
- https://operation.api.cloud.yandex.net/*

Фонового deferred Autorun, chrome.alarms, скрытых retry и автоматического повтора неизвестного платного запроса нет. Получение результата запускается явно.

После handoff в новый ChatGPT-диалог ownership задания не переносится. Другому conversation owner разрешён только exportPage уже полностью SUCCEEDED terminal job при точном revision/folder, без unresolved работы и lease; новых provider calls при таком export нет.
