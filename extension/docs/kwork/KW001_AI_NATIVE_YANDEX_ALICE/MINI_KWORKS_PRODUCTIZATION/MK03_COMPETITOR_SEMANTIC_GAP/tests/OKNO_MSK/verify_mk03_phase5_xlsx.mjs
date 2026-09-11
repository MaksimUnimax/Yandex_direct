#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const here = path.dirname(fileURLToPath(import.meta.url));
const date = "2026-09-11";
const xlsx = path.join(here, "artifacts", `MK03_COMPETITOR_SEMANTIC_GAP_OKNO_MSK_${date}.xlsx`);
const renderDir = path.join(here, "qa", "xlsx_exact_final_rendered");
await fs.mkdir(renderDir, { recursive: true });

const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(xlsx));
const sheetNames = ["Начните здесь", "Разрывы", "Возможности", "Конкуренты", "Страницы конкурентов", "Запросы discovery", "Wordstat", "Проверка выдачи", "Покрытие сайта", "Метод и ограничения"];
const sheetInspect = await wb.inspect({ kind: "sheet,table", maxChars: 12000, tableMaxRows: 3, tableMaxCols: 5, tableMaxCellChars: 80 });
const formulas = await wb.inspect({ kind: "formula", maxChars: 4000, options: { maxResults: 200 } });
const errors = await wb.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 200 }, maxChars: 6000 });
await fs.writeFile(path.join(here, "qa", `MK03_PHASE5_XLSX_EXACT_INSPECT_${date}.txt`), [sheetInspect.ndjson ?? String(sheetInspect), formulas.ndjson ?? String(formulas), errors.ndjson ?? String(errors)].join("\n"), "utf8");

for (const sheetName of sheetNames) {
  const preview = await wb.render({ sheetName, autoCrop: "all", scale: 0.8, format: "png" });
  await fs.writeFile(path.join(renderDir, `${sheetName.replaceAll(" ", "_")}.png`), new Uint8Array(await preview.arrayBuffer()));
}
console.log(JSON.stringify({ xlsx, importedSheets: sheetNames.length, renderedSheets: sheetNames.length }, null, 2));
