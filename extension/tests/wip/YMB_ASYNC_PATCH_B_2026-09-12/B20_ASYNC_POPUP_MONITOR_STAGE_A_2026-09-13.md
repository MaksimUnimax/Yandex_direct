# B20 — Async popup monitor Stage A checkpoint — 2026-09-13

## Status

- `STAGE_A_READ_ONLY_POPUP_MONITOR = PASS`
- `REAL_CHROME_QUALIFICATION = PASS`
- `PROVIDER_CALLS = 0`
- `STAGE_B = NOT_STARTED`
- `BASELINE = 666251c91dce8cb8a1bed414130409e043a1374b`
- `QUALIFIED_SOURCE_COMMIT = 466da55096bb5c36fd07c6601aba1389a6f1414e`
- `QUALIFIED_EXTENSION_SRC_TREE_SHA256 = c8901b164d1a9c499c229cd9eeaf93e534e7f07ab0ea2b4400497be4fca154ba`
- `QUALIFIED_EXTENSION_SRC_FILES = 68`

This checkpoint closes only Stage A of the async popup monitor work. It does not authorize or imply Stage B changes, provider acquisition, Search execution, polling changes, runtime/admission changes, or file-delivery changes.

## Production scope from baseline

Only these production files differ from baseline:

1. `extension/src/popup.html`
   - loads the isolated monitor script.
2. `extension/src/popup_search_async_monitor.js`
   - read-only deferred Search progress monitor.

The QA harness is separate:

- `.github/workflows/ymb-async-popup-monitor-stage-a.yml`

No changes were made in this Stage A pass to service worker, async runtime, Search transport, admission, file delivery, composer Send logic, credentials, billing policy, or provider protocol.

## Stage A behavior

The popup monitor:

- reads the existing `ymb_search_async_items_v2` IndexedDB only;
- uses `readonly` transactions for jobs/items/results;
- does not call `fetch`;
- does not use `XMLHttpRequest`;
- does not call `chrome.runtime.sendMessage`;
- does not emit `SEARCH_ASYNC_BATCH_API_V1`;
- does not launch polling;
- does not change job state;
- shows job id, state, processed/succeeded counts and percentages, remaining count, waiting count, pending/working, errors/unknown, SERP row count, normalized item count, next local poll time, elapsed time and local revision;
- supports manual local refresh and periodic local refresh.

The missing-database path first checks `indexedDB.databases()` when supported. A missing async database is therefore reported without creating or upgrading the database.

## Historical RED evidence retained

### Run 1 — RED

- run: `34755813893`
- source/workflow commit: `195080acd413006d5014ca87687c24dab191ba22`
- artifact: `10317127304`
- artifact digest: `sha256:9224bd9412ce461ee69b74bbf87f81626286978260288f1e2308e87b2ea760eb`
- static read-only gate: PASS
- real Chrome: FAIL
- preserved terminal error: `JOB_NOT_RENDERED`
- cases completed before failure:
  - exact current source: PASS
  - popup section placement: PASS
  - missing DB does not materialize: PASS

This run was not relabeled as PASS.

### Run 2 — RED

- run: `34756016187`
- workflow-only correction commit: `e8a1cded72184280ef2c83d82ff16f31ece2a085`
- artifact: `10317227292`
- artifact digest: `sha256:c016cc21f9a952b4b2a44e090b5d1337c84c8ca007a7087329e23b2f284c2f06`
- static read-only gate: PASS
- real Chrome: FAIL
- preserved terminal error: `REFRESH_BUTTON_STUCK`
- cases completed before failure:
  - exact current source: PASS
  - popup section placement: PASS
  - missing DB does not materialize: PASS

The second run showed that the first popup-startup-race hypothesis was not sufficient. The repeated missing-DB refresh exposed a real monitor defect: the read-only existence probe used `indexedDB.open()` and aborted an upgrade when the DB did not exist, allowing a subsequent refresh to remain stuck around the open/upgrade path.

## Corrective product change

Commit:

`466da55096bb5c36fd07c6601aba1389a6f1414e`

Message:

`fix(extension): avoid creating missing deferred Search monitor database`

Correction:

- check existing IndexedDB names via `indexedDB.databases()` when supported;
- if `ymb_search_async_items_v2` is absent, return `ASYNC_MONITOR_DB_MISSING` without opening it;
- retain the old abort-on-upgrade path only as compatibility fallback when database enumeration is unavailable.

The correction remains inside `popup_search_async_monitor.js`; no provider/runtime/transport code was touched.

## Final GREEN real-Chrome qualification

Run:

`34756151334`

Artifact:

- id: `10317946336`
- name: `ymb-async-popup-monitor-stage-a`
- digest: `sha256:0da50e0eb24fee89767920c330ea2fbc5a0cb7d4149e4472c631d8f28392eb1c`
- artifact bytes: `61232`

Independent artifact readback result:

```json
{
  "schema_version": 1,
  "commit": "466da55096bb5c36fd07c6601aba1389a6f1414e",
  "source_tree_sha256": "c8901b164d1a9c499c229cd9eeaf93e534e7f07ab0ea2b4400497be4fca154ba",
  "source_files": 68,
  "provider_fetch_calls": 0,
  "cases": 6,
  "failures": 0,
  "pass": true
}
```

All required browser cases PASS:

1. `exact_current_source`
   - 68 files
   - tree SHA-256 `c8901b164d1a9c499c229cd9eeaf93e534e7f07ab0ea2b4400497be4fca154ba`
2. `popup_section_placement`
   - monitor is immediately after `Текущий запуск`
3. `missing_db_does_not_materialize`
   - state `Нет локального deferred Search job`
   - database still absent
4. `read_only_live_progress_37_of_100`
   - processed `40 / 100 — 40%`
   - succeeded `37 / 100 — 37%`
   - remaining `60`
   - waiting `20`
   - pending/working `30 / 7`
   - errors/unknown `3 / 3`
   - SERP rows `347`
   - normalized `37 / 100`
   - next check `через 3м 10с` at captured instant
   - revision `12`
   - DB unchanged after periodic refresh: true
   - DB unchanged after manual refresh: true
5. `completed_one_of_one_100_percent`
   - state `Готово`
   - processed `1 / 1 — 100%`
   - success `1 / 1 — 100%`
   - remaining `0`
   - next `—`
6. `no_provider_network_and_no_page_errors`
   - provider fetch calls `0`
   - page errors `0`

Artifact-internal SHA-256 readback also passed; `run.stderr` is empty. A browser screenshot is preserved in the final artifact.

## Gate conclusion

`STAGE_A = PASS`

Stage A is now evidence-backed as a read-only local popup monitor. The two RED runs remain part of the audit trail. Stage B was intentionally not started before this PASS and remains `NOT_STARTED` at this checkpoint.
