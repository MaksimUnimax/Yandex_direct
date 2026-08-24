import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const popupSource = fs.readFileSync(path.join(root, 'popup.js'), 'utf8');
const CKEY = 'https://chatgpt.com|99999999-8888-4777-8666-555555555555';
const CID = '99999999-8888-4777-8666-555555555555';

function extractFunction(name) {
  const marker = `async function ${name}(`;
  const start = workerSource.indexOf(marker);
  assert.notEqual(start, -1, `${name} not found`);
  const brace = workerSource.indexOf('{', start);
  let depth = 0;
  let quote = null;
  let escape = false;
  for (let i = brace; i < workerSource.length; i += 1) {
    const c = workerSource[i];
    if (quote) {
      if (escape) { escape = false; continue; }
      if (c === '\\') { escape = true; continue; }
      if (c === quote) quote = null;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') { quote = c; continue; }
    if (c === '{') depth += 1;
    if (c === '}') {
      depth -= 1;
      if (depth === 0) return workerSource.slice(start, i + 1);
    }
  }
  throw new Error(`unterminated ${name}`);
}

const helperMarker = 'async function setManualModeFromTab(';
const helperSource = workerSource.includes(helperMarker) ? extractFunction('setManualModeFromTab') : '';

function harness(run = null, manualOperation = null) {
  let manual = false;
  const identityChecks = [];
  const ctx = vm.createContext({
    normalizeConversationKey: (value) => value,
    getAutoRun: async () => run ? structuredClone(run) : null,
    storageGet: async () => ({ wsmb_manual_operations: manualOperation ? { [CKEY]: structuredClone(manualOperation) } : {} }),
    KEYS: { MANUAL_OPERATIONS: 'wsmb_manual_operations' },
    TERMINAL_MANUAL_STATUSES: new Set(['completed', 'error', 'cancelled']),
    setManualMode: async (_key, enabled) => { manual = enabled === true; return manual; },
    assertTabConversation: async (tabId, key, conversationId = null) => {
      identityChecks.push({ tabId, key, conversationId });
      return { conversation_key: CKEY, conversation_id: CID };
    },
    WordstatAutorunModel: {
      RUN_STATUSES: { PAUSED: 'paused' },
      isTerminalStatus: (status) => status === 'stopped' || status === 'error'
    },
    structuredClone
  });
  if (helperSource) vm.runInContext(`${helperSource}; globalThis.api = setManualModeFromTab;`, ctx);
  return { api: ctx.api || null, get manual() { return manual; }, identityChecks };
}

function pausedRun(tabId = 1) {
  return { run_id: 'run-owner', conversation_key: CKEY, conversation_id: CID, tab_id: tabId, status: 'paused' };
}

function activeManualOperation(tabId = 1) {
  return { operation_id: 'manual-owner', conversation_key: CKEY, tab_id: tabId, status: 'delivering' };
}

test('Manual mode owner fence exists', () => {
  assert.notEqual(helperSource, '', 'setManualModeFromTab must exist');
});

test('same-conversation non-owner tab cannot enable Manual mode for paused Autorun', async () => {
  const h = harness(pausedRun(1));
  await assert.rejects(() => h.api(CKEY, true, 2), (error) => error?.code === 'AUTO_NON_OWNER_TAB');
  assert.equal(h.manual, false);
});

test('owner tab may enable Manual mode only after live conversation confirmation', async () => {
  const h = harness(pausedRun(1));
  const enabled = await h.api(CKEY, true, 1);
  assert.equal(enabled, true);
  assert.equal(h.manual, true);
  assert.deepEqual(h.identityChecks, [{ tabId: 1, key: CKEY, conversationId: CID }]);
});

test('owner cannot enable Manual mode while Autorun is not paused', async () => {
  const h = harness({ ...pausedRun(1), status: 'waiting_command' });
  await assert.rejects(() => h.api(CKEY, true, 1), (error) => error?.code === 'AUTORUN_NOT_PAUSED');
  assert.equal(h.manual, false);
});

test('without active Autorun current ChatGPT tab can toggle Manual mode after identity confirmation', async () => {
  const h = harness(null);
  const enabled = await h.api(CKEY, true, 7);
  assert.equal(enabled, true);
  assert.deepEqual(h.identityChecks, [{ tabId: 7, key: CKEY, conversationId: null }]);
});

test('same-conversation non-owner tab cannot toggle Manual mode during active Manual operation', async () => {
  const h = harness(null, activeManualOperation(1));
  await assert.rejects(() => h.api(CKEY, false, 2), (error) => error?.code === 'AUTO_NON_OWNER_TAB');
  assert.equal(h.manual, false);
});

test('owner cannot toggle Manual mode while its Manual operation is nonterminal', async () => {
  const h = harness(null, activeManualOperation(1));
  await assert.rejects(() => h.api(CKEY, false, 1), (error) => error?.code === 'MANUAL_OPERATION_ACTIVE');
  assert.equal(h.manual, false);
});

test('popup transports active tab id for Manual mode commit and rollback', () => {
  const first = popupSource.indexOf('type: "WS_SET_MANUAL_MODE"');
  assert.notEqual(first, -1);
  assert.match(popupSource.slice(first, first + 220), /tab_id:\s*context\.tab_id/);
  const second = popupSource.indexOf('type: "WS_SET_MANUAL_MODE"', first + 1);
  assert.notEqual(second, -1, 'rollback WS_SET_MANUAL_MODE not found');
  assert.match(popupSource.slice(second, second + 220), /tab_id:\s*context\.tab_id/);
});

test('worker routes both Manual mutation message paths through owner-aware helper', () => {
  const setCase = workerSource.indexOf('case "WS_SET_MANUAL_MODE"');
  assert.notEqual(setCase, -1);
  assert.match(workerSource.slice(setCase, setCase + 320), /setManualModeFromTab\(/);
  const patchStart = workerSource.indexOf('async function patchToggleSettings(');
  const patchEnd = workerSource.indexOf('\n}\n', patchStart);
  const patchSource = workerSource.slice(patchStart, patchEnd + 3);
  assert.doesNotMatch(patchSource, /await setManualMode\(/);
  assert.match(patchSource, /setManualModeFromTab\(/);
});
