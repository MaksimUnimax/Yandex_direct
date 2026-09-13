# Yandex Marketing Bridge 0.1.6

Production source for the 0.1.6 Chrome MV3 build. This release contains the qualified file-delivery/recovery path and Manual deferred Yandex Search transport.

## Deferred Search

Protocol: `SEARCH_ASYNC_BATCH_API_V1`. Deferred Search is **Manual-only**. `start` creates a durable local job; `submit/submitN` sends bounded provider operations; `collect/collectN/collectReady` later reads saved operation IDs. Results are persisted before normalization/export.

The manifest permits both provider origins:
- `https://searchapi.api.cloud.yandex.net/*` for ordinary Search/GenSearch and deferred submit;
- `https://operation.api.cloud.yandex.net/*` for deferred Operation status/result collection.

There is no deferred Autorun, no `chrome.alarms` polling, no hidden retry and no automatic replay after an uncertain request. Collection is explicit.

Large results use the bounded IndexedDB/file-delivery path with conversation ownership, duplicate-Send protection, pause/recovery, checksum and cleanup guards.
