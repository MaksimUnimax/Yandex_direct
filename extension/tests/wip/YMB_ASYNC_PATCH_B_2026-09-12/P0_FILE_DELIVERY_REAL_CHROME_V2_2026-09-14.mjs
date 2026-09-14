import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const require = createRequire(pathToFileURL(path.resolve(process.env.YMB_PPTR_HOME, 'package.json')));
const puppeteer = require('puppeteer');
const root = fs.realpathSync(process.env.YMB_BROWSER_CANDIDATE);
const fixturePath = path.resolve(process.env.YMB_CHATGPT_FIXTURE);
const out = path.resolve(process.env.YMB_BROWSER_EVIDENCE);
const expectedTree = String(process.env.YMB_EXPECTED_TREE || '').trim();
const expectedFiles = Number(process.env.YMB_EXPECTED_FILES || 0);
const fixture = fs.readFileSync(fixturePath, 'utf8');
fs.mkdirSync(out, { recursive: true });

const hash = (b) => crypto.createHash('sha256').update(b).digest('hex');
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const CID = '70707070-7171-4727-8323-909090909090';
const KEY = `https://chatgpt.com|${CID}`;
const PAGE_URL = `https://chatgpt.com/c/${CID}`;
let browser = null, worker = null, workerTarget = null, page = null, pid = null, monitor = null, peak = 0, failed = 0, tabId = null;
const observedPids = new Set();

function tree() {
  const rows = [];
  function walk(dir) {
    for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
      const file = path.join(dir, item.name);
      assert.equal(item.isSymbolicLink(), false);
      if (item.isDirectory()) walk(file);
      else { assert.ok(item.isFile()); rows.push([path.relative(root, file).split(path.sep).join('/'), hash(fs.readFileSync(file))]); }
    }
  }
  walk(root); rows.sort((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0); assert.equal(rows.length, expectedFiles);
  return hash(Buffer.from(rows.map(([p, h]) => `${h}  ${p}\n`).join('')));
}
function emit(row) { const line = JSON.stringify({ ...row, time: new Date().toISOString() }) + '\n'; fs.appendFileSync(path.join(out, 'browser.jsonl'), line); process.stdout.write(line); }
async function until(fn, label, timeout = 20000) { const end = Date.now() + timeout; while (Date.now() < end) { if (await fn()) return; await delay(100); } throw new Error(label); }
function memory() {
  if (!pid) return { rss_kib: 0, pids: [] };
  const raw = execFileSync('ps', ['-eo', 'pid=,ppid=,rss='], { encoding: 'utf8', timeout: 1500 }).trim();
  const rows = raw ? raw.split('\n').map((line) => line.trim().split(/\s+/).map(Number)) : [];
  const owned = new Set([pid]); let changed = true;
  while (changed) { changed = false; for (const [p, pp] of rows) if (owned.has(pp) && !owned.has(p)) { owned.add(p); changed = true; } }
  const selected = rows.filter(([p]) => owned.has(p)); for (const [p] of selected) observedPids.add(p);
  const rss = selected.reduce((sum, row) => sum + row[2], 0); peak = Math.max(peak, rss); return { rss_kib: rss, pids: selected.map(([p]) => p) };
}
async function runCase(name, fn) { try { emit({ case: name, status: 'PASS', ...(await fn()), memory: memory() }); } catch (error) { failed += 1; emit({ case: name, status: 'FAIL_QUALIFICATION', error: String(error?.stack || error), release_allowed: false }); } }
async function getWorker() {
  workerTarget = await browser.waitForTarget((target) => target.type() === 'service_worker' && target.url().startsWith('chrome-extension://') && target.url().endsWith('/phase3_service_worker_bootstrap.js'), { timeout: 20000 });
  worker = await workerTarget.worker(); assert.ok(worker);
}
async function outbox() {
  return worker.evaluate(async (key) => { const e = await getConversationOutbox(key); return e ? { id: e.delivery_id, phase: e.phase, paused: e.delivery_paused === true, report_text: e.report_text, filenames: (e.artifact_descriptors || []).map((x) => x.filename) } : null; }, KEY);
}
async function resetPageAndOutbox() {
  await worker.evaluate(async (key) => { await clearOutbox(key); const data = await chrome.storage.local.get('wsmb_manual_operations'); const map = data.wsmb_manual_operations || {}; delete map[key]; await chrome.storage.local.set({ wsmb_manual_operations: map }); }, KEY);
  await page.evaluate(() => { const composer = document.getElementById('prompt-textarea'); if (composer) composer.value = ''; document.getElementById('previews')?.replaceChildren(); const input = document.getElementById('upload-files'); if (input) input.value = ''; if (globalThis.__fixture) { __fixture.files = []; __fixture.arm?.(); } });
  await delay(250);
}
async function stage(label) {
  return worker.evaluate(async ({ key, tabId, label }) => {
    const deliveryId = `p0-real-chrome-${label}`, artifactKey = `artifact-${deliveryId}`, filename = `${deliveryId}.txt`;
    const descriptor = await YMBFileArtifactStore.stageTextArtifact({ artifactKey, deliveryId, filename, text: `P0 ${label} browser evidence` });
    const ops = (await chrome.storage.local.get('wsmb_manual_operations')).wsmb_manual_operations || {};
    ops[key] = { operation_id: deliveryId, delivery_id: deliveryId, status: 'delivering', conversation_key: key, tab_id: tabId, active_service: 'search', request_executed: false };
    await chrome.storage.local.set({ wsmb_manual_operations: ops });
    const protocol = `SEARCH_ASYNC_BATCH_RESULT_V1\n${JSON.stringify({ action: 'exportPage', job_id: label, ok: true })}`;
    await putOutbox(key, { delivery_id: deliveryId, operation_id: deliveryId, type: 'manual', tab_id: tabId, phase: 'claimed', report_text: protocol, delivery_mode: 'attachment_v2', artifact_descriptors: [descriptor], provider_executions: 0 });
    return { deliveryId, artifactKey, filename, protocol };
  }, { key: KEY, tabId, label });
}

try {
  assert.ok(expectedTree); assert.ok(Number.isInteger(expectedFiles) && expectedFiles > 0); assert.equal(tree(), expectedTree);
  browser = await puppeteer.launch({ headless: false, pipe: true, enableExtensions: true, protocolTimeout: 120000, args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--disable-background-networking', '--host-resolver-rules=MAP * ~NOTFOUND', `--disable-extensions-except=${root}`, `--load-extension=${root}`] });
  pid = browser.process()?.pid; assert.ok(pid); monitor = setInterval(() => { try { memory(); } catch {} }, 250); await getWorker();
  await worker.evaluate(() => { globalThis.__p0_provider_fetches = 0; globalThis.fetch = async () => { __p0_provider_fetches += 1; throw new Error('P0_REAL_CHROME_NO_PROVIDER_NETWORK'); }; });
  page = await browser.newPage(); await page.setRequestInterception(true);
  page.on('request', (request) => { if (request.isNavigationRequest() && request.url() === PAGE_URL) void request.respond({ status: 200, contentType: 'text/html; charset=utf-8', body: fixture }); else void request.abort(); });
  await page.goto(PAGE_URL, { waitUntil: 'domcontentloaded', timeout: 20000 });
  await until(async () => worker.evaluate(async (url) => { const tab = (await chrome.tabs.query({})).find((x) => x.url === url); if (!tab) return false; return new Promise((resolve) => chrome.tabs.sendMessage(tab.id, { type: 'WS_GET_IDENTITY' }, (response) => { void chrome.runtime.lastError; resolve(response?.ok === true); })); }, PAGE_URL), 'CONTENT_NOT_READY');
  tabId = await worker.evaluate(async (url) => (await chrome.tabs.query({})).find((x) => x.url === url)?.id, PAGE_URL); assert.ok(Number.isInteger(tabId));
  await worker.evaluate(async ({ key, cid, tabId }) => { await chrome.storage.local.set({ wsmb_conversation_bindings: { [key]: { binding_id: 'p0-real-chrome', revision: 1, origin: 'https://chatgpt.com', conversation_id: cid, conversation_key: key } }, wsmb_manual_modes: { [key]: true }, ymb_service_contexts: { [key]: { active_service: 'search' } }, wsmb_auto_send: false, ymb_settings_schema_version: 5 }); await new Promise((resolve) => chrome.tabs.sendMessage(tabId, { type: 'WS_APPLY_MANUAL_MODE', conversation_key: key, enabled: true, active_service: 'search' }, resolve)); }, { key: KEY, cid: CID, tabId });

  await runCase('internal_protocol_never_enters_real_chrome_composer', async () => {
    await resetPageAndOutbox(); const staged = await stage('safe');
    await until(async () => (await outbox())?.phase === 'attachment_ready', 'SAFE_ATTACHMENT_NOT_READY');
    await until(async () => page.evaluate(() => String(document.getElementById('prompt-textarea')?.value || '').length > 0), 'SAFE_MARKER_NOT_STAGED');
    const composer = await page.evaluate(() => String(document.getElementById('prompt-textarea')?.value || ''));
    assert.ok(composer.includes(staged.filename)); assert.ok(!composer.includes('SEARCH_ASYNC_BATCH_RESULT_V1')); assert.ok(!composer.includes('"action":"exportPage"'));
    assert.equal(await worker.evaluate(() => __p0_provider_fetches), 0);
    return { protocol_leak: 0, safe_filename_marker: true, provider_calls: 0 };
  });

  await runCase('user_draft_conflict_after_attachment_ready_durably_pauses_without_reinsert', async () => {
    await resetPageAndOutbox(); const staged = await stage('draft-conflict');
    await until(async () => (await outbox())?.phase === 'attachment_ready', 'CONFLICT_ATTACHMENT_NOT_READY');
    await page.$eval('#prompt-textarea', (element) => { element.value = 'МОЙ ЧЕРНОВИК'; element.dispatchEvent(new Event('input', { bubbles: true })); });
    await until(async () => (await outbox())?.paused === true, 'DURABLE_PAUSE_NOT_PERSISTED');
    const beforeClear = await page.$eval('#prompt-textarea', (element) => element.value);
    assert.equal(beforeClear, 'МОЙ ЧЕРНОВИК'); assert.ok(!beforeClear.includes('SEARCH_ASYNC_BATCH_RESULT_V1'));
    await page.$eval('#prompt-textarea', (element) => { element.value = ''; element.dispatchEvent(new Event('input', { bubbles: true })); });
    await delay(1800);
    const afterClear = await page.$eval('#prompt-textarea', (element) => element.value); const durable = await outbox();
    assert.equal(afterClear, ''); assert.equal(durable?.id, staged.deliveryId); assert.equal(durable?.paused, true); assert.ok(!afterClear.includes('SEARCH_ASYNC_BATCH_RESULT_V1'));
    assert.equal(await worker.evaluate(() => __p0_provider_fetches), 0);
    return { user_draft_overwrites: 0, durable_pause: true, reinsertion_after_clear: 0, provider_calls: 0 };
  });

  assert.equal(tree(), expectedTree);
  emit({ case: 'p0_real_chrome_candidate_identity', status: 'PASS', tree: expectedTree, files: expectedFiles, version: await worker.evaluate(() => chrome.runtime.getManifest().version), provider_calls: await worker.evaluate(() => __p0_provider_fetches) });
} catch (error) { failed += 1; emit({ case: 'p0_real_chrome_harness', status: 'FAIL_QUALIFICATION', error: String(error?.stack || error), release_allowed: false }); }
finally {
  if (monitor) clearInterval(monitor); if (browser) try { await browser.close(); } catch {}
  const remaining = []; for (const p of observedPids) { try { const stat = fs.readFileSync(`/proc/${p}/stat`, 'utf8'); if (stat.slice(stat.lastIndexOf(')') + 2).split(' ')[0] !== 'Z') remaining.push(p); } catch {} }
  emit({ case: 'owned_browser_cleanup', status: remaining.length ? 'FAIL' : 'PASS', remaining, peak_owned_rss_kib: peak, failed, release_allowed: false });
  if (remaining.length || failed) process.exitCode = 1;
}
