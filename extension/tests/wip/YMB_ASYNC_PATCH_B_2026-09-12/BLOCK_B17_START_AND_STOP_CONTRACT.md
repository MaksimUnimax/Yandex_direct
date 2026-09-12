# B17 — безопасная остановка локальной файловой доставки

2026-09-12. Live base: 890fcf91aaf308e5dc86c91b5487aa81f2e849cd.
Exact ready B16 artifact reused, not rebuilt: package dd6d1ef016d4df3d9b4789cd2806f4d0a36202f93c4655e196e2eeda439f7c73, 223870 bytes; tree83ae1351ab057f7cd768243c91060d2dc77e8fe0f5b378055437e47a110012b7,67 files. Local outer artifact and26inner hashes verified before work.

Read current cursor, resource rule and PD-11 cancellation boundary. A destructive Cancel that forgets requesting/committed work would violate the existing rule. Manual OFF remains a safety fence, NOT a cancel button.

## Confirmed missing capability / bounded resolution

The B16 content path has no user action to interrupt its own pending large-file preparation. Its callback wait can retain preparation until a response arrives. Add an explicit **local delivery pause**, not cancellation of a provider request and not deletion of committed evidence.

- Page-owned button pauses current file delivery immediately and requests durable pause on the exact owned outbox entry.
- Durable pause survives reload/worker restart. No future chunks, ready/Send authorization or automatic reattachment while paused.
- Existing source results, artifact bytes, outbox identity, phase and Manual/provider accounting are retained. No false delivered/cancelled-provider status.
- Already authorized Send cannot be revoked reliably; preserve committed evidence and report that limitation. Do not pretend to recall a submitted message.
- Explicit resume is phase-aware: claimed may start normal preparation; attachment_committed/ready may only continue the existing watch/ready path, NEVER automatically recreate a potentially attached file. Missing DOM attachment remains fail-closed.
- Local AbortSignal releases the waiting continuation and stops further DOM writes; it does not claim to cancel Chrome runtime transport or the Yandex API.
- Pause-write failure remains visibly unconfirmed and locally stopped. No implicit retry, no fabricated durable success.
- Local pause/resume does not authorize a new provider call or bypass owner/tab binding. The control cannot delete arbitrary artifacts.

This resolves stop versus destructive cancellation without weakening owner-locked rules. UI removal of already committed/missing server attachments is not invented. Such outcomes remain explicitly unresolved rather than forgotten.

## Dependency matrix / protected behavior

Expected production scope: file_delivery_content.js and file_delivery_worker_transport.js only, plus accurate candidate README wording if needed. No manifest/permissions/version/provider/store schema change.

content control -> pending message/sleep -> local buffers/DOM -> Manual Send: exact-function tests and real paused64MiB/late reply/navigation scenarios.
worker pause -> outbox ownership + serialized file transitions/chunk recheck: real-worker tests for foreign/stale/committed/racing calls and write failure.
resume -> existing phase contract: no hidden reattachment/replay; original Send/ACK behavior preserved.
restart -> durable pause/raw/artifact: real reload/worker restart checks.
all affected binary delivery -> existing B15/B16 full-file/resource regression on changed bytes; scoped evidence only, no independent PASS transfer.

## Sources checked for mechanism, not product correctness

https://developer.chrome.com/docs/extensions/develop/concepts/messaging — callback-based one-time runtime messages; no assumed transport cancellation.
https://developer.chrome.com/docs/extensions/get-started/tutorial/service-worker-events — persist state across ephemeral workers.
https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal — explicit cancellation of local promise APIs and removal of abort listeners on normal completion.

NEXT: implement exact bounded change, preserve executable RED/GREEN and run qualified server Chrome. RELEASE_ALLOWED=NO;REAL_PROVIDER_CALLS=0;INDEPENDENT_GATE=NOT_RUN.
