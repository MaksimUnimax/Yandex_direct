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

const helperMarker = 'async function saveServiceContextFromTab(';
const helperSource = workerSource.includes(helperMarker) ? extractFunction('saveServiceContextFromTab') : '';

function harness({ currentService = 'search', run = null, manualMode = false } = {}) {
  let context = { active_service: currentService, updated_at: 'old' };
  let writes = 0;
  const identityChecks = [];
  const ctx = vm.createContext({
    normalizeConversationKey: (value) => value,
    getServiceContext: async () => structuredClone(context),
    saveServiceContext: async (_key, raw) => { writes += 1; context = { active_service: raw.active_service, updated_at: 'new' }; return structuredClone(context); },
    getAutoRun: async () => run ? structuredClone(run) : null,
    getManualMode: async () => manualMode,
    assertTabConversation: async (tabId, key) => {
      identityChecks.push({ tabId, key });
      return { conversation_key: CKEY, conversation_id: CID };
    },
    YMBRunContextModel: {
      normalizeActiveService(value, registry, { required = false } = {}) {
        const service = String(value || '').trim().toLowerCase();
        if (!service && required) throw Object.assign(new Error('missing'), { code: 'ACTIVE_SERVICE_MISSING' });
        if (service && !registry.isKnownService(service)) throw Object.assign(new Error('unknown'), { code: 'UNKNOWN_SERVICE' });
        return service;
      }
    },
    YMBServiceRegistry: { isKnownService: (service) => ['wordstat', 'search'].includes(service) },
    WordstatAutorunModel: { isTerminalStatus: (status) => status === 'stopped' || status === 'error' },
    structuredClone
  });
  if (helperSource) vm.runInContext(`${helperSource}; globalThis.api = saveServiceContextFromTab;`, ctx);
  return { api: ctx.api || null, get context() { return context; }, get writes() { return writes; }, identityChecks };
}

function activeRun(service = 'search') {
  return { run_id: 'run-owner', conversation_id: CID, tab_id: 1, active_service: service, status: 'paused' };
}

test('active-service owner/lock helper exists', () => {
  assert.notEqual(helperSource, '', 'saveServiceContextFromTab must exist');
});

test('active Autorun rejects changing conversation active service even from owner tab', async () => {
  const h = harness({ currentService: 'search', run: activeRun('search') });
  await assert.rejects(() => h.api(CKEY, { active_service: 'wordstat' }, 1), (error) => error?.code === 'ACTIVE_SERVICE_LOCKED');
  assert.equal(h.context.active_service, 'search');
  assert.equal(h.writes, 0);
});

test('active Autorun permits idempotent save of the already-active service without rewriting context', async () => {
  const h = harness({ currentService: 'search', run: activeRun('search') });
  const saved = await h.api(CKEY, { active_service: 'search' }, 2);
  assert.equal(saved.active_service, 'search');
  assert.equal(h.writes, 0);
  assert.deepEqual(h.identityChecks, []);
});

test('Manual mode locks active-service changes', async () => {
  const h = harness({ currentService: 'search', manualMode: true });
  await assert.rejects(() => h.api(CKEY, { active_service: 'wordstat' }, 1), (error) => error?.code === 'ACTIVE_SERVICE_LOCKED');
  assert.equal(h.writes, 0);
});

test('without active runtime an actual service change requires live current conversation tab', async () => {
  const h = harness({ currentService: 'wordstat' });
  const saved = await h.api(CKEY, { active_service: 'search' }, 7);
  assert.equal(saved.active_service, 'search');
  assert.equal(h.writes, 1);
  assert.deepEqual(h.identityChecks, [{ tabId: 7, key: CKEY }]);
});

test('service change without a concrete tab fails closed', async () => {
  const h = harness({ currentService: 'wordstat' });
  await assert.rejects(() => h.api(CKEY, { active_service: 'search' }, null), (error) => error?.code === 'OWNER_TAB_REQUIRED');
  assert.equal(h.writes, 0);
});

test('popup transports active tab id with conversation-scoped WS_SAVE_SETTINGS', () => {
  const start = popupSource.indexOf('type: "WS_SAVE_SETTINGS"');
  assert.notEqual(start, -1);
  const source = popupSource.slice(start, start + 900);
  assert.match(source, /tab_id\s*=\s*context\.tab_id|tab_id:\s*context\.tab_id/);
});

test('worker routes both service-context mutation paths through owner/lock helper', () => {
  const saveSettings = workerSource.indexOf('case "WS_SAVE_SETTINGS"');
  assert.notEqual(saveSettings, -1);
  assert.match(workerSource.slice(saveSettings, saveSettings + 1500), /saveServiceContextFromTab\(/);
  const direct = workerSource.indexOf('case "WS_SAVE_SERVICE_CONTEXT"');
  assert.notEqual(direct, -1);
  assert.match(workerSource.slice(direct, direct + 420), /saveServiceContextFromTab\(/);
});
