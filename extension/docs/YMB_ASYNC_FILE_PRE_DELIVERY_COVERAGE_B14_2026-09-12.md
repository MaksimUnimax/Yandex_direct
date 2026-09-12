# B14 — точная упаковка и квалифицированный браузерный venue

Применять вместе с исходным PD gate, resource rule и B13 coverage. Это development evidence, не независимый полный PASS. Точное production-дерево B13 не менялось: f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47.

PD-00/02/03: теперь существует exact internal QA ZIP e260f35b1d7decf02c18c46103b4072de68270c2bce09e2f51f7462941c48f97, 223380 bytes. Canonical metadata, local/CI deterministic identity, all67 fresh files и14 guards реально прошли. Это текущий внутренний пакет, не автоматически будущий activated/versioned release.

PD-01: сохранённые available suites повторены из распакованного ZIP локально и в Actions; original132,78,99,254,84. Полный Codex PD campaign не запускался.

PD-04: реальный Chrome152.0.7977.75 в fresh GitHub runner загрузил точный MV3 artifact и его модули. Только startup/load readiness; завершение/возобновление worker и прочая lifecycle matrix НЕ доказаны.

PD-09/14: настоящая IndexedDB прошла ограниченный two-item ownership/UNKNOWN/recovery-function smoke. Это НЕ real worker termination, disk durability или вся матрица10/100/500/1500.

PD-11/resource: настоящий artifact store проверен на1/10/32/64/64/64MiB, read/checksum/delete, чтение1record/chunk. Измерены summed Chrome RSS и cleanup. File/DataTransfer/DOM/upload/cancel/reload ещё не пройдены. Нельзя объявлять весь resource gate PASS.

PD-05/06/07/10/11/13 и остальные browser-owned части: раньше отсутствовал квалифицированный текущий browser venue; теперь qa/b14_browser_venue.mjs и workflow ymb-b14-browser-venue.yml реально работают на точном пакете. Политики локального Chrome не обходились. Нужно адаптировать/исполнить оставшиеся восстановленные browser scenarios в этом venue, а не списывать их как навсегда недоступные.

PD-16: operation host по-прежнему выключен. PD-17: evidence/transport доступны, release/independent acceptance не даны.

Exact reusable artifact: run34692833348/artifact10298216105, outerSHA4c5fb564fcb3fa586f6e779e7120f89ca5ee352a4bf8fdd59e335db8a45018b9,487812bytes,expires2026-12-11T12:07:52Z. Он содержит готовые candidate и QA workspace; не восстанавливать цепочку A/B1–B13 при наличии этого exact input. Browser proof: run34693351244/artifact10298391517; actual pass is scoped as above.

Следующий блок — недостающая controlled browser/IDB/resource qualification на exact artifact. Независимый Codex gate отдельно после полного mapping/venue proof; владелец не переносит QA-файлы. RELEASE_ALLOWED = NO.
