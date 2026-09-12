# B15 — оставшаяся браузерная проверка, начало

Дата: 2026-09-12. Live HEAD прочитан: f31baa4f578f66330aeb0fad23942487eff0f639.
Прочитаны актуальный cursor B14, проверенный launcher/workflow B14 и обязательные resource/PD правила. Ни A/B1–B13, ни пакет не пересоздаются.

В текущей среде уже есть скачанный B14 bundle: SHA256 4c5fb564fcb3fa586f6e779e7120f89ca5ee352a4bf8fdd59e335db8a45018b9, 487812 bytes. Проверены ZIP и все пять внутренних hashes. Используются его готовый QA workspace и exact ZIP e260f35b1d7decf02c18c46103b4072de68270c2bce09e2f51f7462941c48f97, 223380 bytes, 67 файлов. Производственное дерево остаётся f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47.

## Ограниченный план

1. Переиспользовать работающий B14 GitHub-hosted CfT/Puppeteer launcher, pinned dependencies и exact artifact download. Не запускать локальный административно заблокированный Chrome.
2. Controlled ChatGPT DOM fixture: настоящий content script, File/DataTransfer, worker chunk transport, delivery/ACK/cleanup; краткий текст и крупные файлы, повторные/занятые/ошибочные действия. Никакого live ChatGPT upload или пользовательского профиля.
3. Настоящее завершение/повторный запуск service worker с сохранённой IndexedDB. Проверять идентичность нового worker, отсутствие повторной отправки и сохранность результата, не подменять это простой сменой workerId.
4. Реальная IDB 10/100/500/1500: поэлементные переходы, полный учёт строк, ограниченность записи, восстановление. Искусственные исходы провайдера; реальных платных вызовов нет.
5. RSS только дерева созданного QA Chrome, bounded time и аварийная остановка. PASS только достигнутым assertions. Полный независимый Codex gate отдельно.

## Зависимости и границы

QA -> тот же точный пакет -> manifest content/worker -> existing attachment module -> outbox -> IDB. New QA scripts/fixtures не входят в production. Permissions, version, credentials, provider runtime и данные Kwork не изменяются. Реальный operation-host остаётся выключен. Любой обнаруженный defect сначала сохраняется с конкретным RED; исправление — отдельный ограниченный блок с новым exact target.

Сохранять код/тесты до CI, stdout/stderr/JSONL/RSS даже при FAIL, затем raw evidence + report + cursor. Не объявлять отдельные успешные циклы полным resource gate. RELEASE_ALLOWED = NO.
