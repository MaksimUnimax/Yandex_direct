import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { spawnSync } from 'node:child_process';

const [historicalHarness, chromePath, extensionRoot, keyPath, certPath] = process.argv.slice(2);
for (const value of [historicalHarness, chromePath, extensionRoot, keyPath, certPath]) {
  if (!value || !fs.existsSync(value)) throw new Error(`CURRENT_STAGE4_INPUT_MISSING ${value || '<empty>'}`);
}

// The historical Git blob is verified independently by git object id. Windows
// worktrees may materialize it as CRLF, so normalize only the temporary QA copy
// before applying the exact function-level compatibility patch.
const source = fs.readFileSync(historicalHarness, 'utf8').replace(/\r\n/g, '\n');
const oldBlock = `async function openPopup(worker, browser, key) {
  const existingTargets = new Set(browser.targets());
  const tab = await worker.evaluate(async () => await chrome.tabs.create({ url: chrome.runtime.getURL('popup.html'), active:false }));
  assert(tab?.id, 'POPUP_TAB_CREATE_FAIL');
  const target = await browser.waitForTarget(t => !existingTargets.has(t) && t.url().startsWith('chrome-extension://') && t.url().endsWith('/popup.html'), { timeout:10000 });
  const popup = await target.page(); assert(popup, 'POPUP_PAGE_FAIL');
  await popup.waitForFunction(expected => document.getElementById('conversationMeta')?.textContent === expected, { timeout:10000 }, key);
  await waitUntil(async () => {
    const status = await popup.evaluate(() => document.getElementById('status')?.textContent || '');
    return status === 'Готово.' ? true : false;
  }, 'POPUP_INITIAL_REFRESH_NOT_COMPLETE', 10000);
  return { popup, tabId:tab.id };
}
async function closePopup(worker, tabId) { try { await worker.evaluate(async id => { try { await chrome.tabs.remove(id); } catch {} }, tabId); } catch {} await delay(180); }`;

const newBlock = `async function openPopup(worker, browser, key) {
  const owner = await worker.evaluate(async expectedKey => {
    const tabs = await chrome.tabs.query({ active:true, currentWindow:true });
    const active = tabs?.[0] || null;
    if (!active?.id) return { active:null, identity:null };
    const identity = await new Promise(resolve => chrome.tabs.sendMessage(active.id, { type:'WS_GET_IDENTITY' }, response => {
      resolve({ response:response || null, error:chrome.runtime.lastError?.message || null });
    }));
    return { active:{ id:active.id, url:active.url || '' }, identity, expectedKey };
  }, key);
  assert(owner?.active?.id, 'POPUP_OWNER_ACTIVE_TAB_MISSING');
  assert(owner.identity?.response?.ok === true && owner.identity.response.conversation_key === key,
    \`POPUP_OWNER_CONTEXT_FAIL \${JSON.stringify(owner)}\`);

  const tab = await worker.evaluate(async ownerTabId => {
    const created = await chrome.tabs.create({ url:'about:blank', active:false });
    if (!created?.id) return null;
    await chrome.tabs.update(ownerTabId, { active:true });
    await chrome.tabs.update(created.id, { url:chrome.runtime.getURL('popup.html') });
    return { id:created.id };
  }, owner.active.id);
  assert(tab?.id, 'POPUP_TAB_CREATE_FAIL');

  const popup = await waitUntil(async () => {
    for (const page of await browser.pages()) {
      if (!page.url().startsWith('chrome-extension://') || !page.url().endsWith('/popup.html')) continue;
      const currentTabId = await page.evaluate(() => new Promise(resolve => {
        chrome.tabs.getCurrent(tab => resolve(tab?.id || null));
      })).catch(() => null);
      if (Number(currentTabId) === Number(tab.id)) return page;
    }
    return null;
  }, 'POPUP_TAB_TARGET_FAIL', 10000, 80);

  const bootstrap = await waitUntil(async () => await popup.evaluate(() => {
    const error = globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__ || '';
    const result = globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__ || null;
    if (!error && !result) return null;
    return { error, result, status:document.getElementById('status')?.textContent || '' };
  }), 'POPUP_BOOTSTRAP_OUTCOME_TIMEOUT', 12000, 80);
  if (bootstrap.error) throw new Error(\`POPUP_BOOTSTRAP_ERROR \${bootstrap.error}\`);
  assert(bootstrap.result?.attempted === true, \`POPUP_BOOTSTRAP_NOT_ATTEMPTED \${JSON.stringify(bootstrap)}\`);
  assert(Number(bootstrap.result?.tab_id) === Number(owner.active.id),
    \`POPUP_BOOTSTRAP_WRONG_TAB \${JSON.stringify({bootstrap,owner})}\`);

  await popup.waitForFunction(expected => document.getElementById('conversationMeta')?.textContent === expected, { timeout:12000 }, key);
  await waitUntil(async () => {
    const state = await popup.evaluate(() => ({
      text:document.getElementById('status')?.textContent || '',
      level:document.getElementById('status')?.dataset?.level || ''
    }));
    if (state.level === 'error') throw new Error(\`POPUP_INITIAL_ERROR \${state.text}\`);
    return state.text === 'Готово.' ? state : false;
  }, 'POPUP_INITIAL_REFRESH_NOT_COMPLETE', 12000, 80);
  console.log('CURRENT_POPUP_BOOTSTRAP_VENUE_PASS');
  return { popup, tabId:tab.id };
}
async function closePopup(worker, tabId) {
  try { await worker.evaluate(async id => { try { await chrome.tabs.remove(id); } catch {} }, tabId); } catch {}
  await waitUntil(async () => await worker.evaluate(async id => await new Promise(resolve => {
    chrome.tabs.get(id, () => resolve(Boolean(chrome.runtime.lastError)));
  }), tabId), 'POPUP_TAB_CLOSE_NOT_CONFIRMED', 5000, 80);
}`;

const occurrences = source.split(oldBlock).length - 1;
if (occurrences !== 1) throw new Error(`HISTORICAL_POPUP_LIFECYCLE_ANCHOR_FAIL count=${occurrences}`);
const patched = source.replace(oldBlock, newBlock);
if (patched === source) throw new Error('HISTORICAL_POPUP_LIFECYCLE_PATCH_NOT_APPLIED');

const outDir = path.join(process.cwd(), '.ymb-current-stage4-qa');
const outFile = path.join(outDir, 'browser_phase2_stage4_gate.current.mjs');
fs.rmSync(outDir, { recursive:true, force:true });
fs.mkdirSync(outDir, { recursive:true });
try {
  fs.writeFileSync(outFile, patched, { encoding:'utf8' });
  console.log('HISTORICAL_STAGE4_ASSERTIONS_PRESERVED');
  console.log('CURRENT_STAGE4_POPUP_LIFECYCLE_PATCH_READY');
  const child = spawnSync(process.execPath, [outFile, chromePath, extensionRoot, keyPath, certPath], {
    cwd:process.cwd(),
    stdio:'inherit',
    env:process.env
  });
  if (child.error) throw child.error;
  if (child.status !== 0) throw new Error(`CURRENT_STAGE4_CHILD_FAIL exit=${child.status}`);
} finally {
  fs.rmSync(outDir, { recursive:true, force:true });
}
