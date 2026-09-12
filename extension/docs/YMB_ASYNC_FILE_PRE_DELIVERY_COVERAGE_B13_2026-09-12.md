# B13 — дополнение к прежней карте PD-покрытия

Применять вместе с YMB_ASYNC_FILE_PRE_DELIVERY_COVERAGE_2026-09-12.md, CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md и YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md. Это более поздняя поправка к статусам B12, не отмена требований. Все PD-00…PD-17 остаются обязательными; development evidence не является независимой приёмкой.

Точный B13: f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47, 67 файлов. Отчёт: extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/BLOCK_B13_RESULT.md. Исполнимый runner: qa/b13_available_campaign.py; exact restore: qa/prepare_b13.py. Полные inputs/harness inventory и adapters находятся в qa/B13_QA_INPUTS.tar.xz, raw logs — в evidence/B13_RAW_LOGS/ с проверяемым восстановлением.

## Что именно изменилось в статусах

| Раздел | Новое доступное доказательство | Что остаётся открытым |
|---|---|---|
| PD-00 | Exact 67-file B13, 65 unchanged, pre/post deltas and negative materializer tests | Final independent freeze/package still absent |
| PD-01 | COMPLETE original non-WIP inventory: 158 files. All 18 package Node suites 118 PASS plus supplemental 14 PASS. Three explicit harness/source-marker adaptations retained as diffs; behavior assertions not removed | Independent full campaign and browser scripts not executed; do not rename development PASS as gate PASS |
| PD-02 | 61 JS syntax, 2 JSON, exact tree after fresh campaign | Final deliberate permission/version/package changes require recheck |
| PD-08 | All four Wordstat methods exact request/response/faults; actual Manual/Check/batch/Autorun; inherited envelope and legacy-routing defects reproduced and corrected | Real API/installed worker not tested |
| PD-09/10 | Dedicated-vs-legacy credential isolation; batch counter/one-boundary/UNKNOWN/ack behavior; preserved Search accounting and lifecycle regressions rerun | Real IDB/settings contention and MV3/visible UI lifecycle remain open |
| PD-12 | Debug OFF/ON error visibility/redaction, opt-in diagnostic storage, latest-200 limit and clear tested through real worker functions | Actual popup and every service-specific visible Debug scenario still need mapped final execution |
| PD-14/15 | Full-worker backup V3 checksum/version, all five credentials roundtrip, refuse active work, legacy migration and reload, secret-bearing backup vs redacted public outputs | Real disk/upgrade persistence, actual UI exposure and full independent security campaign not proved |
| PD-04/05/06/07/11/13 | Eight known browser scripts and two campaign runners recovered with hashes/invocation/prerequisites and historical accepted evidence | None run against B13; old target/fixture variations must be explicitly qualified, not blindly copied as PASS |
| PD-03/16/17 | Deferred operation host remains absent; no new network permissions or installable artifact; exact raw evidence persisted | Final authorized activation/capability, independent gate, deterministic package and fresh extraction remain mandatory |

Previous statements that the original suite was not inventoried, or all Wordstat/Debug/backup evidence was missing, are superseded only to the extent shown above. The original B12 map remains history, not evidence that this later work was unperformed.

## Следующая квалификация

Использовать B13, не повторять инвентаризацию и не добавлять новые функции. Следующий блок — подготовка точной финальной квалификации: связать оставшиеся PD assertions с восстановленными исполнимыми сценариями, проверить доступные недостающие случаи, затем отдельная независимая QA-кампания в квалифицированной среде. Старые frozen-target runner и manifest.key fixture не подменяют точный кандидат. Владелец не переносит QA-файлы.

Не запускать повторно заведомо заблокированный браузер и не обходить политики. Реальные 1/10/32/64 MiB file cycles и 10/100/500/1500 batch, process memory/cleanup/reload/IDB remain mandatory where applicable. Никакой Node результат не заменяет эти требования.

RELEASE_ALLOWED = NO. INDEPENDENT_GATE = NOT_RUN.
