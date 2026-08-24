import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const popupSource = fs.readFileSync(path.join(root, 'popup.js'), 'utf8');
const CKEY = 'https://chatgpt.com|22222222-3333-4444-8555-666666666666';
const CID = '22222222-3333-4444-8555-666666666666';

function extractAsyncFunction(source, name) {
  const marker = `async function ${name}(`;
  const start = source.indexOf(marker);
  assert.notEqual(start, -1, `${name} not found`);
  const signatureEnd = source.indexOf(') {', start);
  assert.notEqual(signatureEnd, -1, `${name} signature end not found`);
  const brace = signatureEnd + 2;
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

const helperPresent = workerSource.includes('async function saveReportPrefixFromTab(');
const selectedHelperName = helperPresent ? 'saveReportPrefixFromTab' : 'saveReportPrefix';
const selectedHelperSource = extractAsyncFunction(workerSource, selectedHelperName);

function normalizePrefix(raw = {}) {
  return {
    enabled: raw.enabled === true,
    text: String(raw.text || ''),
    interval: Number(raw.interval || 1),
    delivered_count: Number(raw.delivered_count || 0),
    last_applied_at_count: Number(raw.last_applied_at_count || 0),
    last_confirmed_delivery_id: raw.last_confirmed_delivery_id || null
  };
}

function harness({ run = null, operation = null, initial = { enabled: false, text: '', interval: 1 } } = {}) {
  let prefix = normalizePrefix(initial);
  let writes = 0;
  const identityChecks = [];
  const ctx = vm.createContext({
    normalizeConversationKey: (value) => value,
    KEYS: { REPORT_PREFIXES: 'report_prefixes', MANUAL_OPERATIONS: 'manual_operations' },
    TERMINAL_MANUAL_STATUSES: new Set(['completed', 'error', 'cancelled']),
    WordstatAutorunModel: {
      normalizePrefixRecord: (raw) => normalizePrefix(raw),
      isTerminalStatus: (status) => status === 'stopped' || status === 'error'
    },
    storageGet: async (key) => {
      if (key === 'report_prefixes') return { report_prefixes: { [CKEY]: structuredClone(prefix) } };
      if (key === 'manual_operations') return { manual_operations: operation ? { [CKEY]: structuredClone(operation) } : {} };
      return {};
    },
    storageSet: async (value) => {
      if (value?.report_prefixes?.[CKEY]) {
        prefix = normalizePrefix(value.report_prefixes[CKEY]);
        writes += 1;
      }
    },
    getAutoRun: async () => run ? structuredClone(run) : null,
    saveReportPrefix: async (_key, raw) => {
      prefix = normalizePrefix({ ...prefix, ...raw });
      writes += 1;
      return structuredClone(prefix);
    },
    assertTabConversation: async (tabId, key, conversationId = null) => {
      identityChecks.push({ tabId, key, conversationId });
      return { conversation_key: CKEY, conversation_id: CID };
    },
    structuredClone
  });
  vm.runInContext(`${selectedHelperSource}; globalThis.api = ${selectedHelperName};`, ctx);
  return { api: ctx.api, get prefix() { return prefix; }, get writes() { return writes; }, identityChecks };
}

function activeRun(tabId = 1) {
  return { run_id: 'run-prefix-owner', conversation_key: CKEY, conversation_id: CID, tab_id: tabId, status: 'waiting_command' };
}

function activeOperation(tabId = 1) {
  return { operation_id: 'manual-prefix-owner', conversation_key: CKEY, tab_id: tabId, status: 'delivering' };
}

test('report-prefix tab-aware helper exists', () => {
  assert.equal(helperPresent, true, 'saveReportPrefixFromTab must exist');
});

test('same-conversation non-owner tab cannot mutate prefix while Autorun owns runtime', async () => {
  const h = harness({ run: activeRun(1) });
  await assert.rejects(() => h.api(CKEY, { enabled: true, text: 'BAD' }, 2), (error) => error?.code === 'AUTO_NON_OWNER_TAB');
  assert.equal(h.writes, 0);
  assert.equal(h.prefix.text, '');
});

test('Autorun owner may update prefix after live conversation confirmation', async () => {
  const h = harness({ run: activeRun(1) });
  const saved = await h.api(CKEY, { enabled: true, text: 'OWNER' }, 1);
  assert.equal(saved.enabled, true);
  assert.equal(saved.text, 'OWNER');
  assert.equal(h.writes, 1);
  assert.deepEqual(h.identityChecks, [{ tabId: 1, key: CKEY, conversationId: CID }]);
});

test('same-conversation non-owner tab cannot mutate prefix during Manual operation', async () => {
  const h = harness({ operation: activeOperation(1) });
  await assert.rejects(() => h.api(CKEY, { enabled: true, text: 'BAD' }, 2), (error) => error?.code === 'AUTO_NON_OWNER_TAB');
  assert.equal(h.writes, 0);
});

test('Manual operation owner may update prefix for future reports', async () => {
  const h = harness({ operation: activeOperation(1) });
  const saved = await h.api(CKEY, { enabled: true, text: 'OWNER-MANUAL' }, 1);
  assert.equal(saved.text, 'OWNER-MANUAL');
  assert.equal(h.writes, 1);
  assert.deepEqual(h.identityChecks, [{ tabId: 1, key: CKEY, conversationId: null }]);
});

test('idle prefix mutation requires a concrete live ChatGPT tab', async () => {
  const missing = harness();
  await assert.rejects(() => missing.api(CKEY, { enabled: true }, null), (error) => error?.code === 'OWNER_TAB_REQUIRED');
  assert.equal(missing.writes, 0);

  const h = harness();
  const saved = await h.api(CKEY, { enabled: true, text: 'IDLE' }, 7);
  assert.equal(saved.text, 'IDLE');
  assert.deepEqual(h.identityChecks, [{ tabId: 7, key: CKEY, conversationId: null }]);
});

test('both report-prefix mutation paths route through tab-aware helper', () => {
  const patchStart = workerSource.indexOf('async function patchToggleSettings(');
  const patchEnd = workerSource.indexOf('\n}\n', patchStart);
  const patchSource = workerSource.slice(patchStart, patchEnd + 3);
  assert.match(patchSource, /saveReportPrefixFromTab\(/);
  assert.match(patchSource, /message\.tab_id\s*\?\?\s*sender\?\.tab\?\.id/);

  const saveSettings = workerSource.slice(workerSource.indexOf('case "WS_SAVE_SETTINGS"'), workerSource.indexOf('case "WS_SAVE_SERVICE_CONTEXT"'));
  assert.match(saveSettings, /saveReportPrefixFromTab\(/);
  assert.match(saveSettings, /message\.tab_id\s*\?\?\s*sender\?\.tab\?\.id/);
});

test('popup immediate prefix toggle transports current tab id', () => {
  const start = popupSource.indexOf('async function persistTogglePatch(');
  const end = popupSource.indexOf('\n  async function withButton', start);
  assert.notEqual(start, -1);
  assert.notEqual(end, -1);
  const source = popupSource.slice(start, end);
  assert.match(source, /tab_id:\s*context\.tab_id/);
});
