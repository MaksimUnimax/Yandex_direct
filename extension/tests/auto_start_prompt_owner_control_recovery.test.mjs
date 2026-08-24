import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const popupSource = fs.readFileSync(path.join(root, 'popup.js'), 'utf8');
const CKEY = 'https://chatgpt.com|77777777-3333-4444-8555-111111111111';
const CID = '77777777-3333-4444-8555-111111111111';

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

const saveHelperPresent = workerSource.includes('async function saveAutoStartPromptFromTab(');
const resetHelperPresent = workerSource.includes('async function resetAutoStartPromptFromTab(');
const selectedSaveName = saveHelperPresent ? 'saveAutoStartPromptFromTab' : 'saveAutoStartPrompt';
const selectedResetName = resetHelperPresent ? 'resetAutoStartPromptFromTab' : 'resetAutoStartPrompt';
const selectedSaveSource = extractAsyncFunction(workerSource, selectedSaveName);
const selectedResetSource = extractAsyncFunction(workerSource, selectedResetName);

function harness({ run = null, operation = null } = {}) {
  let prompt = { text: 'OLD', is_default: false, service: 'search', updated_at: null };
  let writes = 0;
  const identityChecks = [];
  const ctx = vm.createContext({
    normalizeConversationKey: (value) => value,
    KEYS: { AUTO_START_PROMPTS: 'auto_start_prompts', MANUAL_OPERATIONS: 'manual_operations' },
    TERMINAL_MANUAL_STATUSES: new Set(['completed', 'error', 'cancelled']),
    WordstatAutorunModel: { isTerminalStatus: (status) => status === 'stopped' || status === 'error' },
    YMBServiceRegistry: { SERVICES: { SEARCH: 'search', WORDSTAT: 'wordstat' } },
    getServiceContext: async () => ({ active_service: 'search' }),
    getAutoRun: async () => run ? structuredClone(run) : null,
    getAutoStartPrompt: async () => structuredClone(prompt),
    saveAutoStartPrompt: async (_key, text, { service = null } = {}) => {
      prompt = { text: String(text).trim(), is_default: false, service: service || 'search', updated_at: 'now' };
      writes += 1;
      return structuredClone(prompt);
    },
    resetAutoStartPrompt: async (_key, { service = null } = {}) => {
      prompt = { text: service === 'wordstat' ? 'WORDSTAT DEFAULT' : 'SEARCH DEFAULT', is_default: true, service: service || 'search', updated_at: 'now' };
      writes += 1;
      return structuredClone(prompt);
    },
    defaultAutoStartTextForService: (service) => service === 'wordstat' ? 'WORDSTAT DEFAULT' : 'SEARCH DEFAULT',
    storageGet: async (key) => {
      if (key === 'manual_operations') return { manual_operations: operation ? { [CKEY]: structuredClone(operation) } : {} };
      if (key === 'auto_start_prompts') return { auto_start_prompts: { [CKEY]: structuredClone(prompt) } };
      return {};
    },
    storageSet: async (value) => {
      if (value?.auto_start_prompts?.[CKEY]) {
        prompt = structuredClone(value.auto_start_prompts[CKEY]);
        writes += 1;
      }
    },
    nowIso: () => 'now',
    assertTabConversation: async (tabId, key, conversationId = null) => {
      identityChecks.push({ tabId, key, conversationId });
      return { conversation_key: CKEY, conversation_id: CID };
    },
    structuredClone
  });
  vm.runInContext(`${selectedSaveSource}; ${selectedResetSource}; globalThis.saveApi = ${selectedSaveName}; globalThis.resetApi = ${selectedResetName};`, ctx);
  return { saveApi: ctx.saveApi, resetApi: ctx.resetApi, get prompt() { return prompt; }, get writes() { return writes; }, identityChecks };
}

function activeRun(tabId = 1) {
  return { run_id: 'run-prompt-owner', conversation_key: CKEY, conversation_id: CID, tab_id: tabId, status: 'waiting_command' };
}
function activeOperation(tabId = 1) {
  return { operation_id: 'manual-prompt-owner', conversation_key: CKEY, tab_id: tabId, status: 'delivering' };
}

test('start-prompt tab-aware helpers exist', () => {
  assert.equal(saveHelperPresent, true, 'saveAutoStartPromptFromTab must exist');
  assert.equal(resetHelperPresent, true, 'resetAutoStartPromptFromTab must exist');
});

test('same-conversation non-owner tab cannot save start prompt while Autorun owns runtime', async () => {
  const h = harness({ run: activeRun(1) });
  await assert.rejects(() => h.saveApi(CKEY, 'BAD', { service: 'search', tabId: 2 }), (error) => error?.code === 'AUTO_NON_OWNER_TAB');
  assert.equal(h.writes, 0);
});

test('Autorun owner may save future start prompt after live conversation confirmation', async () => {
  const h = harness({ run: activeRun(1) });
  const saved = await h.saveApi(CKEY, 'OWNER NEXT RUN', { service: 'search', tabId: 1 });
  assert.equal(saved.text, 'OWNER NEXT RUN');
  assert.equal(h.writes, 1);
  assert.deepEqual(h.identityChecks, [{ tabId: 1, key: CKEY, conversationId: CID }]);
});

test('same-conversation non-owner tab cannot reset start prompt during Manual operation', async () => {
  const h = harness({ operation: activeOperation(1) });
  await assert.rejects(() => h.resetApi(CKEY, { service: 'search', tabId: 2 }), (error) => error?.code === 'AUTO_NON_OWNER_TAB');
  assert.equal(h.writes, 0);
});

test('Manual operation owner may reset future start prompt after live conversation confirmation', async () => {
  const h = harness({ operation: activeOperation(1) });
  const reset = await h.resetApi(CKEY, { service: 'search', tabId: 1 });
  assert.equal(reset.is_default, true);
  assert.equal(h.writes, 1);
  assert.deepEqual(h.identityChecks, [{ tabId: 1, key: CKEY, conversationId: null }]);
});

test('idle start-prompt mutation requires a concrete live ChatGPT tab', async () => {
  const missing = harness();
  await assert.rejects(() => missing.saveApi(CKEY, 'NO TAB', { service: 'search', tabId: null }), (error) => error?.code === 'OWNER_TAB_REQUIRED');
  assert.equal(missing.writes, 0);

  const h = harness();
  const saved = await h.saveApi(CKEY, 'IDLE OWNER', { service: 'search', tabId: 7 });
  assert.equal(saved.text, 'IDLE OWNER');
  assert.deepEqual(h.identityChecks, [{ tabId: 7, key: CKEY, conversationId: null }]);
});

test('both worker start-prompt mutation paths route through tab-aware helpers', () => {
  const saveCase = workerSource.slice(workerSource.indexOf('case "WS_SAVE_AUTO_START_PROMPT"'), workerSource.indexOf('case "WS_RESET_AUTO_START_PROMPT"'));
  assert.match(saveCase, /saveAutoStartPromptFromTab\(/);
  assert.match(saveCase, /message\.tab_id\s*\?\?\s*sender\?\.tab\?\.id/);
  const resetCase = workerSource.slice(workerSource.indexOf('case "WS_RESET_AUTO_START_PROMPT"'), workerSource.indexOf('case "WS_START_AUTORUN"'));
  assert.match(resetCase, /resetAutoStartPromptFromTab\(/);
  assert.match(resetCase, /message\.tab_id\s*\?\?\s*sender\?\.tab\?\.id/);
});

test('popup transports current tab id for save and reset start prompt', () => {
  const saveStart = popupSource.indexOf('type: "WS_SAVE_AUTO_START_PROMPT"');
  assert.notEqual(saveStart, -1);
  assert.match(popupSource.slice(saveStart, saveStart + 280), /tab_id:\s*context\.tab_id/);
  const resetStart = popupSource.indexOf('type: "WS_RESET_AUTO_START_PROMPT"');
  assert.notEqual(resetStart, -1);
  assert.match(popupSource.slice(resetStart, resetStart + 280), /tab_id:\s*context\.tab_id/);
});
