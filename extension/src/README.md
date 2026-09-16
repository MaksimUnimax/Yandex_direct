# Yandex Marketing Bridge 0.1.7

Production source for the 0.1.7 Chrome MV3 build. This release contains the qualified file-delivery/recovery path, Manual deferred Yandex Search transport, and bounded read-only cross-chat export for fully successful terminal deferred Search jobs after a ChatGPT project-chat handoff.

## Deferred Search

Protocol: `SEARCH_ASYNC_BATCH_API_V1`. Deferred Search is **Manual-only**. `start` creates a durable local job; `submit/submitN` sends bounded provider operations; `collect/collectN/collectReady` later reads saved operation IDs. Results are persisted before normalization/export.

The manifest permits both provider origins:
- `https://searchapi.api.cloud.yandex.net/*` for ordinary Search/GenSearch and deferred submit;
- `https://operation.api.cloud.yandex.net/*` for deferred Operation status/result collection.

There is no deferred Autorun, no `chrome.alarms` polling, no hidden retry and no automatic replay after an uncertain request. Collection is explicit.

Large results use the bounded IndexedDB/file-delivery path with conversation ownership, duplicate-Send protection, pause/recovery, checksum and cleanup guards. Cross-chat recovery does not transfer job ownership: it is limited to `exportPage` of an exact-revision, exact-folder terminal job with all items `SUCCEEDED`, no unresolved work and no active lease; provider calls remain zero.
