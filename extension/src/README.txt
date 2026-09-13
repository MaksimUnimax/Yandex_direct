Yandex Marketing Bridge 0.1.6

Production-сборка с ручным deferred Search.

start сохраняет задание; submit/submitN отправляет отдельные поисковые запросы и сохраняет operation_id; collect/collectN/collectReady позже получает готовые результаты.

В manifest разрешены оба адреса Яндекса:
- https://searchapi.api.cloud.yandex.net/*
- https://operation.api.cloud.yandex.net/*

Фонового deferred Autorun, chrome.alarms, скрытых retry и автоматического повтора неизвестного платного запроса нет. Получение результата запускается явно.
