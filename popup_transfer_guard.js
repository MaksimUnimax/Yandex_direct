(() => {
  "use strict";

  const MAX_BACKUP_BYTES = 5 * 1024 * 1024;

  function status(text, level = "") {
    const node = document.getElementById("status");
    if (!node) return;
    node.textContent = String(text || "");
    if (node.dataset) node.dataset.level = level;
  }

  function stop(event) {
    event?.preventDefault?.();
    event?.stopImmediatePropagation?.();
  }

  function confirmExport() {
    return globalThis.confirm("Экспортировать секретный backup настроек? JSON будет содержать сохранённый Yandex API key.");
  }

  function confirmImport() {
    return globalThis.confirm("Импортировать секретный backup? Совместимые настройки будут объединены; активный запуск не заменяется.");
  }

  function install() {
    const exportButton = document.getElementById("exportSettings");
    const importFile = document.getElementById("importFile");

    exportButton?.addEventListener("click", (event) => {
      if (confirmExport()) return;
      stop(event);
      status("Экспорт отменён.");
    }, true);

    importFile?.addEventListener("change", (event) => {
      const file = importFile.files?.[0] || null;
      if (!file) return;
      if (Number(file.size || 0) > MAX_BACKUP_BYTES) {
        stop(event);
        importFile.value = "";
        status("Backup слишком большой. Максимум 5 МБ.", "error");
        return;
      }
      if (confirmImport()) return;
      stop(event);
      importFile.value = "";
      status("Импорт отменён.");
    }, true);
  }

  install();

  if (globalThis.__YMB_POPUP_TRANSFER_GUARD_TEST__ === true) {
    globalThis.__YMB_POPUP_TRANSFER_GUARD_TEST_API__ = Object.freeze({
      MAX_BACKUP_BYTES,
      confirmExport,
      confirmImport
    });
  }
})();