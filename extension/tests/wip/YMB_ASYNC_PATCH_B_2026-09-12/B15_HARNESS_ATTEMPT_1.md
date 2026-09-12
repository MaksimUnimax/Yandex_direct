# B15 — первый запуск и ограниченное исправление QA

Run 34694466079, artifact 10297923782. Архив скачан и проверен: SHA256 1f1d4a55beff955d9e8f69e1d253eafb1b1e5928ac6eda134127253084f7bdbd, 15409 bytes; все внутренние hashes совпали. QA script совпал с локальным: b464224139ac2fe0ff7e194f76d4e38e1c5ec9ef144f075df3aafb9d3ec9423d.

Точный пакет загрузился в Chrome152.0.7977.75. При первом chrome.tabs вызове после открытия fixture получено Chrome error `No SW`; ни один новый DOM/file/large-IDB assertion не был достигнут. Cleanup прошёл, оставшихся owned процессов нет, resource stop не срабатывал. Классификация: FAIL_HARNESS / extension-context readiness; это не доказанный product FAIL и не memory regression. Старые scoped B14 PASS не отменяются, новые PASS не объявляются.

Проверен исходник Puppeteer25.10 BrowserLauncher.ts: enableExtensions:[path] вызывает browser.installExtension(path). В унаследованном B14 launcher одновременно были CLI --load-extension и enableExtensions:[path], то есть два механизма установки. Для изоляции этой переменной QA-only b15_single_install.py заменяет ровно один фрагмент на enableExtensions:true и сохраняет прежние CLI flags — вариант, уже использованный историческими browser harness. Это гипотеза причины No SW, подлежащая проверке следующим запуском, а не утверждение о доказанной причине без результата.

Product/manifest/credentials/permission bytes не меняются. Исходный failing script и его run/artifact сохраняются. Повторяется ранее не достигнутая матрица, не успешные B14 циклы. Следующий результат надо прочитать прежде дальнейших изменений.

Источники: puppeteer/puppeteer @ puppeteer-v25.10.0 packages/puppeteer-core/src/node/BrowserLauncher.ts; https://groups.google.com/a/chromium.org/g/chromium-extensions/c/rHFKotXbm-0 (Chrome DevRel относит No SW к браузерному dispatcher, не к тексту расширения). Эти материалы не доказывают конкретную корневую причину данного запуска.

RELEASE_ALLOWED = NO.
