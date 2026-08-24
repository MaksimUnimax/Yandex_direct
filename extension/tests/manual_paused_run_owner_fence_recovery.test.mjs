import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');

function extractFunction(name) {
  const marker = `async function ${name}(`;
  const start = workerSource.indexOf(marker);
  assert.notEqual(start, -1, `${name} not found`);
  const brace = workerSource.indexOf('{', start);
  let depth = 0;
  let quote = null;
  let escape = false;
  let lineComment = false;
  let blockComment = false;
  for (let i = brace; i < workerSource.length; i += 1) {
    const c = workerSource[i];
    const n = workerSource[i + 1];
    if (lineComment) { if (c === '\n') lineComment = false; continue; }
    if (blockComment) { if (c === '*' && n === '/') { blockComment = false; i += 1; } continue; }
    if (quote) {
      if (escape) { escape = false; continue; }
      if (c === '\\') { escape = true; continue; }
      if (c === quote) quote = null;
      continue;
    }
    if (c === '/' && n === '/') { lineComment = true; i += 1; continue; }
    if (c === '/' && n === '*') { blockComment = true; i += 1; continue; }
    if (c === '"' || c === "'" || c === '`') { quote = c; continue; }
    if (c === '{') depth += 1;
    if (c === '}') {
      depth -= 1;
      if (depth === 0) return workerSource.slice(start, i + 1);
    }
  }
  throw new Error(`unterminated ${name}`);
}

const executeManualBlockSource = extractFunction('executeManualBlock');
const CKEY = 'https://chatgpt.com|99999999-8888-4777-8666-555555555555';
const CID = '99999999-8888-4777-8666-555555555555';

function harness() {
  const store = {};
  const ctx = vm.createContext({
    console,
    normalizeConversationKey: (value) => value,
    assertTabConversation: async () => ({ conversation_id: CID }),
    getBinding: async () => ({ conversation_id: CID }),
    getManualMode: async () => true,
    getServiceContext: async () => ({ active_service: 'search' }),
    discoverManualBlockItems: () => ({ items: [], marker_count: 0 }),
    getAutoRun: async () => ({ run_id: 'run-owner', active_service: 'search', status: 'paused', tab_id: 1 }),
    WordstatAutorunModel: {
      RUN_STATUSES: { PAUSED: 'paused' },
      isTerminalStatus: () => false
    },
    YMBRunContextModel: { assertServiceMatch: () => true },
    KEYS: { MANUAL_OPERATIONS: 'manual_ops' },
    storageGet: async () => ({ manual_ops: store.manual_ops || {} }),
    storageSet: async (values) => { if (values.manual_ops) store.manual_ops = structuredClone(values.manual_ops); },
    TERMINAL_MANUAL_STATUSES: new Set(['completed', 'error', 'cancelled']),
    uid: (prefix) => `${prefix}-1`,
    YMBBlockCommandDiscovery: { textFingerprint: () => 'fp' },
    nowIso: () => '2026-08-24T00:00:00.000Z',
    formatBridgeError: ({ code }) => `YMB_ERROR_V1\n${JSON.stringify({ code })}`,
    putOutbox: async () => ({}),
    getSettings: async () => ({}),
    getPolicyForService: async () => ({}),
    policyDecisionForService: () => ({ allow: false, reason: 'NO', estimated_cost_rub: 0, policy: {} }),
    publicCapability: () => ({ state: 'OK' }),
    assertProtocolForService: () => ({ formatSkippedReport: () => '' }),
    patchAutoRun: async () => ({}),
    executeServiceCommand: async () => { throw new Error('provider must not be reached'); },
    applyPrefixToReport: async (_key, text) => ({ text, applied: false }),
    structuredClone
  });
  vm.runInContext(`${executeManualBlockSource}; globalThis.executeManualBlock = executeManualBlock;`, ctx);
  return { api: ctx.executeManualBlock, store };
}

test('Manual cannot attach to a paused Autorun owned by another same-conversation tab', async () => {
  const h = harness();
  const result = await h.api('plain text', CKEY, { tab: { id: 2 } }, 'manual-tab-2');
  assert.equal(result.accepted, false);
  assert.equal(result.code, 'AUTO_NON_OWNER_TAB');
  assert.equal(h.store.manual_ops, undefined);
});
