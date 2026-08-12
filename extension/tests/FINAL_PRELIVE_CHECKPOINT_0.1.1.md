# FINAL PRE-LIVE CHECKPOINT — Yandex Marketing Bridge 0.1.1

Date: 2026-08-12
Status: **PRE-LIVE PASS / PRODUCTION LIVE PENDING**

Exact artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-repair-candidate.zip
SHA-256 311353e2671052b7170e12db3e1318dfed4f59ccf945c7eda6ec59152ee3abfb
size 172705 bytes
files 41
```

Final automated evidence:

```text
source tests:              311/311 PASS
fresh ZIP tests:           311/311 PASS
source↔ZIP byte identity:   41/41
JS/MJS syntax:              36/36 PASS
manifest/package JSON:       2/2 PASS
versions:                  0.1.1 / 0.1.1
Chromium 144 load smoke:   PASS
```

Final safety repairs included after 0.1.0 live failure:

- remove mandatory `job_id` and GitHub coupling from Bridge runtime;
- preserve legacy `wsmb_*` storage compatibility;
- add Export/Import secret settings backup with SHA-256 validation;
- preserve active RUN/manual-operation safety context during import;
- always-on ChatGPT error delivery independent of Debug Mode;
- Debug Mode adds redacted logs only;
- durable error claim/commit/reconciliation and no duplicate Send;
- recoverable Autorun continuation;
- unknown request outcome no blind retry;
- Manual validation errors delivered to ChatGPT;
- accurate `error_report_queued` contract;
- Manual on PAUSED RUN shares RUN request/cost budget and cannot bypass it.

Canonical current docs:

```text
extension/docs/PROJECT_PURPOSE.md
extension/docs/SPECIFICATION.md
extension/docs/ROADMAP.md
extension/docs/DEVELOPMENT_CONTEXT_APPEND_ONLY.md
extension/docs/DEVELOPMENT_CONTEXT_APPEND_ONLY_CONTINUATION_0.1.1.md
extension/docs/PHASE_1_0.1.1_LIVE_ACCEPTANCE.md
```

Machine-readable evidence:

```text
extension/tests/PHASE_1_0.1.1_PRELIVE_TEST_EVIDENCE.json
```

Search remains blocked until owner real-Chrome/current-ChatGPT live acceptance passes.

No paid Yandex request was executed during this development/pre-live test cycle.
