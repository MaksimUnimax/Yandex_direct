# B15 — воспроизведённый дефект повторного Send

Run 34694861037, artifact 10297639857, 21322 bytes, SHA256 ae1cb787d999d719216e0e1342265293c0ab2e3a7293f3676602372585c8bf49. Архив скачан, внутренние hashes проверены. Точный пакет e260f35b1d7decf02c18c46103b4072de68270c2bce09e2f51f7462941c48f97 / production tree f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47.

## Доказанный RED

Два быстрых ручных клика Send при готовом файле и auto-send off дали ДВА вызова WS_COMMIT_ATTACHMENT_SEND и ДВА DOM send handler вызова. Первый с текстом, второй с уже пустым composer. File/DataTransfer change был один, ACK один. Assertions ожидали один Send и упали 2 != 1. Это реальный product defect content->worker->DOM в controlled Chrome, не ошибка provider и не прежний OOM.

## Причина в точном коде

file_delivery_content.js commitAndClick не блокирует второй вход, пока ожидает асинхронный commit, и не отличает ответ already_committed от нового разрешения кликнуть. Оба обработчика после await вызывают button.click(). Рядом есть in_flight для poll, но ручной click handler проходит мимо него.

## Ограниченное исправление

Менять только file_delivery_content.js: небольшой Set выполняющихся send commits по delivery_id; повторный вход не отправляет второй commit; already_committed только наблюдается, не кликает; уничтоженный content runtime/отсоединённая кнопка не кликают после запоздалого ответа. Set очищается в finally. Никакого нового payload, storage schema, network или polling. Worker/provider/store/protocol/permissions/version остаются прежними.

Зависимости: manual and automatic Send, delayed worker reply, disposal/navigation, recovery watcher, attachment cleanup, повторный явный клик после отказа. Проверки: тот же browser RED -> GREEN, целевые executable Node функции, повтор всей затронутой primary/supplemental file/resource матрицы на новом exact package. Остальные scoped B14/B15 результаты сохраняются за старым target, не переносятся автоматически.

## Уже успешные независимые supplemental сценарии

Повреждённый chunk остановлен до DataTransfer и не запрошен повторно. Reload с потерянным DOM-вложением не повторяет attachment/send. Реальный worker restart посреди1500 items сохраняет750 raw, переводит1 в UNKNOWN и отменяет749 ещё не отправленных; бюджет751 не обнуляется. Три additional64MiB цикла с5s idle завершены, endpoints1675408/1857528/1678840KiB, peak1931304KiB, никаких оставшихся процессов. Это не всеобщая гарантия отсутствия утечек.

RELEASE_ALLOWED = NO. NEXT = bounded one-file correction and exact-target regression, not a new feature.
