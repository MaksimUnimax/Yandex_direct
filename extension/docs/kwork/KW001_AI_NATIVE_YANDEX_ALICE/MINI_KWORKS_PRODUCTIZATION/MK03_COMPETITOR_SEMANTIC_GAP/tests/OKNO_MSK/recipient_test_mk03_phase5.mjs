#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const here = path.dirname(fileURLToPath(import.meta.url));
const date = "2026-09-11";
const pkg = path.join(here, `CLIENT_DELIVERY_PHASE_5_MK03_OKNO_MSK_${date}`);
const xlsx = path.join(pkg, `MK03_COMPETITOR_SEMANTIC_GAP_OKNO_MSK_${date}.xlsx`);
const pdf = path.join(pkg, `MK03_COMPETITOR_SEMANTIC_GAP_OKNO_MSK_${date}.pdf`);
const handoff = path.join(pkg, "README_FIRST.md");

const checks = [];
function check(id, ok, evidence) { checks.push({ id, status: ok ? "PASS" : "FAIL", evidence }); }

const packageFiles = (await fs.readdir(pkg)).sort();
check("R01_PACKAGE_NAVIGATION", packageFiles.length === 3 && packageFiles.filter(n => n.endsWith(".xlsx")).length === 1 && packageFiles.filter(n => n.endsWith(".pdf")).length === 1 && packageFiles.filter(n => n.endsWith(".md")).length === 1, packageFiles.join(" | "));

const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(xlsx));
const sheetNames = ["Начните здесь", "Разрывы", "Возможности", "Конкуренты", "Страницы конкурентов", "Запросы discovery", "Wordstat", "Проверка выдачи", "Покрытие сайта", "Метод и ограничения"];
const overview = await wb.inspect({ kind: "sheet", maxChars: 6000 });
const overviewText = overview.ndjson ?? String(overview);
check("R02_FIND_REQUIRED_VIEWS", sheetNames.every(n => overviewText.includes(n)), `Visible sheets ${sheetNames.length}/10`);

const gaps = wb.worksheets.getItem("Разрывы").getRange("A5:N47").values;
const statuses = gaps.map(r => r[11]);
const count = value => statuses.filter(v => v === value).length;
check("R03_CLASSIFY_ANY_DIRECTION", gaps.length === 43 && count("Подтверждённый разрыв") === 7 && count("Уже покрыто") === 23 && count("Вне подтверждённого предложения") === 3 && count("Нужны данные") === 10, `43 rows; 7/23/3/10; one visible terminal state per row`);

const opps = wb.worksheets.getItem("Возможности").getRange("A5:K11").values;
check("R04_VERIFY_CONFIRMED_GAP", opps.length === 7 && opps.every(r => Number(r[2]) > 0 && String(r[3]).includes("[") && r[9] && r[10] === "Не принято"), `7/7 have individual Wordstat, phrase evidence, owner validation and no page decision`);

const competitors = wb.worksheets.getItem("Конкуренты").getRange("A5:H13").values;
const compPages = wb.worksheets.getItem("Страницы конкурентов").getRange("A5:P48").values;
check("R05_TRACE_COMPETITOR_TO_PAGE", competitors.length === 9 && compPages.length === 44 && competitors.every(c => compPages.some(p => p[0] === c[0])), `9/9 competitors trace to 44 page observations`);

const matrix = wb.worksheets.getItem("Проверка выдачи").getRange("A5:H85").values;
check("R06_READ_SELECTIVE_SERP_BOUNDARY", matrix.length === 81 && matrix.filter(r => r[3] === "Выдача получена").length === 63 && matrix.filter(r => r[3] === "Результат неизвестен").length === 18 && matrix.every(r => String(r[7]).includes("провер") || String(r[7]).includes("сохранённый")), `81 pairs = 63 tested + 18 unknown; boundary visible per row`);

const method = wb.worksheets.getItem("Метод и ограничения").getRange("A1:C25").values.flat().filter(Boolean).join(" ");
check("R07_DISTINGUISH_GAP_FROM_PAGE_DECISION", method.includes("не означает создание страницы") && method.includes("До URL/страницы") && method.includes("не равно графику"), `Client can distinguish gap, URL/page decision and analytical attention`);

const pdfText = execFileSync("pdftotext", ["-layout", pdf, "-"], { encoding: "utf8" });
const pdfInfo = execFileSync("pdfinfo", [pdf], { encoding: "utf8" });
check("R08_READ_ANALYTICAL_PDF", /Pages:\s+13/.test(pdfInfo) && ["Главный вывод", "Фактические конкуренты", "Подтверждённые возможности", "Что осталось на проверку", "Ограничения и следующий шаг"].every(t => pdfText.includes(t)), `13 pages; executive result, competitors, opportunities, holds and limitations all present`);

const handoffText = await fs.readFile(handoff, "utf8");
check("R09_USE_HANDOFF_WITHOUT_INTERNAL_HELP", handoffText.includes("7 подтверждённых") && handoffText.includes("23 уже покрытых") && handoffText.includes("3 вне") && handoffText.includes("10") && handoffText.toLowerCase().includes("огранич"), `Counts, file route and limitations visible in README_FIRST.md`);

const report = { status: checks.every(c => c.status === "PASS") ? "PASS" : "FAIL", test_mode: "FINAL_CLIENT_FILES_ONLY", pass_count: checks.filter(c => c.status === "PASS").length, fail_count: checks.filter(c => c.status === "FAIL").length, checks };
console.log(JSON.stringify(report, null, 2));
await fs.writeFile(path.join(here, "qa", `MK03_PHASE5_RECIPIENT_QA_${date}.json`), JSON.stringify(report, null, 2) + "\n", "utf8");
if (report.status !== "PASS") process.exit(1);
