import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const popupSource = fs.readFileSync(path.join(root, 'popup.js'), 'utf8');
const CKEY = 'https://chatgpt.com|11111111-2222-4333-8444-555555555555';
const CID = '11111111-2222-4333-8444-555555555555';

function extractAsyncFunction(source, name) {
  const marker = `async function ${name}(`;
  const start = source.indexOf(marker);
  assert.notEqual(start, -1, `${name} not found`);
  const brace = source.indexOf('{', start);
  let depth = 0;
  let quote = null;
  let escape = false;
  for (let i = brace; i < source.length; i += 1) {
    const c = source[i];
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
      if (depth === 0) return source.slice(start, i + 1);
    }
  }
  throw new Error(`unterminated ${name}`);
}

const guardedHelperPresent = workerSource.includes('async function saveServiceContextFromTab(');
const selectedHelperName = guardedHelperPresent ? 'saveServiceContextFromTab' : 'saveServiceContext';
const selectedHelperSource = extractAsyncFunction(workerSource, selectedHelperName);

function harness({ run = null, operation = null, manualMode = false, currentService = 'wordstat' } = {}) {
  let service = currentService;
  let writes = 0;
  const identityChecks = [];
  const ctx = vm.createContext({
    normalizeConversationKey: (value) => value,
    nowIso: () => '2026-08-24T00:00:00.000Z',
    KEYS: { SERVICE_CONTEXTS: 'service_contexts', MANUAL_OPERATIONS: 'manual_operations' },
    TERMINAL_MANUAL_STATUSES: new Set(['completed', 'error', 'cancelled']),
    YMBServiceRegistry: {
      SERVICES: { WORDSTAT: 'wordstat', SEARCH: 'search' },
      isKnownService: (value) => value === 'wordstat' || value === 'search'
    },
    YMBRunContextModel: {
      normalizeActiveService: (value) => {
        if (value !== 'wordstat' && value !== 'search') throw Object.assign(new Error('invalid service'), { code: 'SERVICE_NOT_AVAILABLE' });
        return value;
      }
    },
    WordstatAutorunModel: {
      isTerminalStatus: (status) => status === 'stopped' || status === 'error'
    },
    storageGet: async (key) => {
      if (key === 'manual_operations') return { manual_operations: operation ? { [CKEY]: structuredClone(operation) } : {} };
      if (key === 'service_contexts') return { service_contexts: { [CKEY]: { active_service: service, updated_at: null } } };
      return {};
    },
    storageSet: async (value) => {
      if (value?.service_contexts?.[CKEY]?.active_service) {
        service = value.service_contexts[CKEY].active_service;
        writes += 1;
      }
    },
    getServiceContext: async () => ({ active_service: service, updated_at: null }),
    saveServiceContext: async (_key, raw) => {
      service = raw.active_service;
      writes += 1;
      return { active_service: service, updated_at: '2026-08-24T00:00:00.000Z' };
    },
    getAutoRun: async () => run ? structuredClone(run) : null,
    getManualMode: async () => manualMode,
    assertTabConversation: async (tabId, key, conversationId = null) => {
      identityChecks.push({ tabId, key, conversationId });
      return { conversation_key: CKEY, conversation_id: CID };
    },
    structuredClone
  });
  vm.runInContext(`${selectedHelperSource}; globalThis.api = ${selectedHelperName};`, ctx);
  return { api: ctx.api, get service() { return service; }, get writes() { return writes; }, identityChecks };
}

function activeRun(tabId = 1) {
  return { run_id: 'run-owner', conversation_key: CKEY, conversation_id: CID, tab_id: tabId, status: 'paused', active_service: 'wordstat' };
}

function activeOperation(tabId = 1) {
  return { operation_id: 'manual-owner', conversation_key: CKEY, tab_id: tabId, status: 'delivering', active_service: 'wordstat' };
}

test('service-context runtime owner fence exists', () => {
  assert.equal(guardedHelperPresent, true, 'saveServiceContextFromTab must exist');
});

test('same-conversation non-owner tab cannot switch active service while Autorun is active', async () => {
  const h = harness({ run: activeRun(1) });
  await assert.rejects(() => h.api(CKEY, { active_service: 'search' }, 2), (error) => error?.code === 'AUTO_NON_OWNER_TAB');
  assert.equal(h.service, 'wordstat');
  assert.equal(h.writes, 0);
});

test('Autorun owner cannot mutate its immutable active service while run is nonterminal', async () => {
  const h = harness({ run: activeRun(1) });
  await assert.rejects(() => h.api(CKEY, { active_service: 'search' }, 1), (error) => error?.code === 'SERVICE_CONTEXT_RUNTIME_LOCKED');
  assert.equal(h.service, 'wordstat');
  assert.equal(h.writes, 0);
  assert.deepEqual(h.identityChecks, [{ tabId: 1, key: CKEY, conversationId: CID }]);
});

test('same-conversation non-owner tab cannot switch active service during Manual operation', async () => {
  const h = harness({ operation: activeOperation(1), manualMode: true });
  await assert.rejects(() => h.api(CKEY, { active_service: 'search' }, 2), (error) => error?.code === 'AUTO_NON_OWNER_TAB');
  assert.equal(h.service, 'wordstat');
  assert.equal(h.writes, 0);
});

test('Manual operation owner cannot switch active service until operation is terminal', async () => {
  const h = harness({ operation: activeOperation(1), manualMode: true });
  await assert.rejects(() => h.api(CKEY, { active_service: 'search' }, 1), (error) => error?.code === 'SERVICE_CONTEXT_RUNTIME_LOCKED');
  assert.equal(h.service, 'wordstat');
  assert.equal(h.writes, 0);
  assert.deepEqual(h.identityChecks, [{ tabId: 1, key: CKEY, conversationId: null }]);
});

test('Manual mode locks active service even when no Manual operation is currently in flight', async () => {
  const h = harness({ manualMode: true });
  await assert.rejects(() => h.api(CKEY, { active_service: 'search' }, 7), (error) => error?.code === 'SERVICE_CONTEXT_RUNTIME_LOCKED');
  assert.equal(h.service, 'wordstat');
  assert.equal(h.writes, 0);
  assert.deepEqual(h.identityChecks, [{ tabId: 7, key: CKEY, conversationId: null }]);
});

test('idle current ChatGPT tab may switch active service after live identity confirmation', async () => {
  const h = harness();
  const saved = await h.api(CKEY, { active_service: 'search' }, 7);
  assert.equal(saved.active_service, 'search');
  assert.equal(h.service, 'search');
  assert.equal(h.writes, 1);
  assert.deepEqual(h.identityChecks, [{ tabId: 7, key: CKEY, conversationId: null }]);
});

test('same-service save is a no-op during active runtime so unrelated settings can still be saved', async () => {
  const h = harness({ run: activeRun(1) });
  const saved = await h.api(CKEY, { active_service: 'wordstat' }, 2);
  assert.equal(saved.active_service, 'wordstat');
  assert.equal(h.service, 'wordstat');
  assert.equal(h.writes, 0);
});

test('both worker service-context mutation paths route through the tab-aware helper', () => {
  const saveSettings = workerSource.slice(workerSource.indexOf('case "WS_SAVE_SETTINGS"'), workerSource.indexOf('case "WS_SAVE_AUTO_START_PROMPT"'));
  assert.match(saveSettings, /saveServiceContextFromTab\(/);
  assert.match(saveSettings, /message\.tab_id\s*\?\?\s*sender\?\.tab\?\.id/);
  const direct = workerSource.slice(workerSource.indexOf('case "WS_SAVE_SERVICE_CONTEXT"'), workerSource.indexOf('case "WS_SAVE_AUTO_START_PROMPT"'));
  assert.match(direct, /saveServiceContextFromTab\(/);
  assert.match(direct, /message\.tab_id\s*\?\?\s*sender\?\.tab\?\.id/);
});

test('popup transports active tab id when saving conversation-scoped settings', () => {
  const saveAll = extractAsyncFunction(popupSource, 'saveAll');
  assert.match(saveAll, /message\.tab_id\s*=\s*context\.tab_id/);
});
