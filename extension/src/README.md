# Yandex Marketing Bridge 0.1.9

Production source for the 0.1.9 Chrome MV3 build. This release keeps the qualified file-delivery/recovery path and Manual deferred Yandex Search transport from 0.1.8, and fixes the Deferred Search popup read model so folder-scoped durable jobs remain visible after start, submit, reload/restart, service switching and successful collection.

## Deferred Search

Protocol: `SEARCH_ASYNC_BATCH_API_V1`. Deferred Search is **Manual-only**. `start` creates a durable local job; `submit/submitN` sends bounded provider operations; `collect/collectN/collectReady` later reads saved operation IDs. Results are persisted before normalization/export.

A deferred Search job is owned by the active Search credential scope (`folder_id`), not by a ChatGPT conversation UUID. The current ChatGPT dialogue is still required as live execution authority: it must be bound, Manual mode must be enabled, Search must be the active service, and the current Search credential must match the job folder. Therefore a new bound dialogue using the same Search folder can continue `status`, `itemsPage`, `exportPage`, local controls, submit and collect against the same durable job without changing job ownership. A different Search folder is rejected by the existing owner/folder guards.

The popup uses the same durable identity (`search-folder:<folder_id>`) when reading the local Deferred Search IndexedDB. Popup refresh is strictly local/read-only: it may read extension state and IndexedDB, but it never performs deferred submit, collect, provider polling, retry or revision mutation. ChatGPT conversation identity remains required separately for action authority.

Paused Autorun accounting remains conversation-owned separately from durable job data: the admission binding records a dedicated run mirror owner while the job itself stays credential-scoped.

The manifest permits both provider origins:
- `https://searchapi.api.cloud.yandex.net/*` for ordinary Search/GenSearch and deferred submit;
- `https://operation.api.cloud.yandex.net/*` for deferred Operation status/result collection.

There is no deferred Autorun, no `chrome.alarms` polling, no hidden retry and no automatic replay after an uncertain request. Collection is explicit.

Large results use the bounded IndexedDB/file-delivery path with duplicate-Send protection, pause/recovery, checksum and cleanup guards. `exportPage` uses the ordinary owner-guarded exporter; there is no cross-owner terminal-export bypass.

Jobs created by the older conversation-owned deferred schema are intentionally not migrated by this release. Recreate those jobs under 0.1.8+.
