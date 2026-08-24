import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const popupSource = fs.readFileSync(path.join(root, 'popup.js'), 'utf8');
const CKEY = 'https://chatgpt.com|33333333-4444-4555-8666-777777777777';
const CID = '33333333-4444-4555-8666-777777777777';

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

const helperPresent = workerSource.includes('async function saveAutoStartPromptFromTab(');
const selectedHelperName = helperPresent ? 'saveAutoStartPromptFromTab' : 'saveAutoStartPrompt';
const selectedHelperSource = extractAsyncFunction(workerSource, selectedHelperName);

function harness({ currentService = 'search', record = null } = {}) {
  let saved = record ? structuredClone(record) : null;
  let writes = 0;
  const identityChecks = [];
  const ctx = vm.createContext({
    normalizeConversationKey: (value) => value,
    nowIso: () => '2026-08-24T00:00:00.000Z',
    KEYS: { AUTO_START_PROMPTS: 'auto_start_prompts' },
    YMBServiceRegistry: { SERVICES: { SEARCH: 'search', WORDSTAT: 'wordstat' } },
    defaultAutoStartTextForService: (service) => service === 'search' ? 'SEARCH DEFAULT' : 'WORDSTAT DEFAULT',
    storageGet: async (key) => key === 'auto_start_prompts'
      ? { auto_start_prompts: saved ? { [CKEY]: structuredClone(saved) } : {} }
      : {},
    storageSet: async (value) => {
      if (value?.auto_start_prompts?.[CKEY]) {
        saved = structuredClone(value.auto_start_prompts[CKEY]);
        writes += 1;
      }
    },
    getServiceContext: async () => ({ active_service: currentService }),
    getAutoStartPrompt: async (_key, { service = null } = {}) => {
      const resolved = service || currentService;
      if (saved?.text && saved.is_default !== true && saved.service === resolved) return { ...structuredClone(saved), service: resolved };
      return { text: resolved === 'search' ? 'SEARCH DEFAULT' : 'WORDSTAT DEFAULT', is_default: true, service: resolved, updated_at: saved?.updated_at || null };
    },
    saveAutoStartPrompt: async (_key, text, { service = null } = {}) => {
      const resolved = service || currentService;
      const value = String(text || '').trim();
      if (!value) throw Object.assign(new Error('empty'), { code: 'AUTO_START_PROMPT_EMPTY' });
      saved = { text: value, is_default: value === (resolved === 'search' ? 'SEARCH DEFAULT' : 'WORDSTAT DEFAULT'), service: resolved, updated_at: '2026-08-24T00:00:00.000Z' };
      writes += 1;
      return structuredClone(saved);
    },
    assertTabConversation: async (tabId, key) => {
      identityChecks.push({ tabId, key });
      return { conversation_key: CKEY, conversation_id: CID };
    },
    structuredClone
  });
  vm.runInContext(`${selectedHelperSource}; globalThis.api = ${selectedHelperName};`, ctx);
  return { api: ctx.api, get saved() { return saved; }, get writes() { return writes; }, identityChecks };
}

test('Autorun start-prompt tab-aware helper exists', () => {
  assert.equal(helperPresent, true, 'saveAutoStartPromptFromTab must exist');
});

test('actual start-prompt mutation requires a concrete live ChatGPT tab', async () => {
  const missing = harness();
  await assert.rejects(() => missing.api(CKEY, 'CUSTOM', { service: 'search' }, null), (error) => error?.code === 'OWNER_TAB_REQUIRED');
  assert.equal(missing.writes, 0);

  const h = harness();
  const saved = await h.api(CKEY, 'CUSTOM', { service: 'search' }, 7);
  assert.equal(saved.text, 'CUSTOM');
  assert.equal(saved.service, 'search');
  assert.equal(h.writes, 1);
  assert.deepEqual(h.identityChecks, [{ tabId: 7, key: CKEY }]);
});

test('same custom prompt is a no-op and does not require a tab', async () => {
  const existing = { text: 'CUSTOM', is_default: false, service: 'search', updated_at: 'old' };
  const h = harness({ record: existing });
  const saved = await h.api(CKEY, 'CUSTOM', { service: 'search' }, null);
  assert.equal(saved.text, 'CUSTOM');
  assert.equal(saved.service, 'search');
  assert.equal(h.writes, 0);
  assert.deepEqual(h.identityChecks, []);
});

test('live non-owner tab is not runtime-locked because prompt only affects a future Autorun', async () => {
  const h = harness();
  const saved = await h.api(CKEY, 'FUTURE', { service: 'search' }, 2);
  assert.equal(saved.text, 'FUTURE');
  assert.deepEqual(h.identityChecks, [{ tabId: 2, key: CKEY }]);
});

test('save and reset worker routes both pass a concrete tab to the tab-aware helper', () => {
  const save = workerSource.slice(workerSource.indexOf('case "WS_SAVE_AUTO_START_PROMPT"'), workerSource.indexOf('case "WS_START_AUTORUN"'));
  assert.match(save, /saveAutoStartPromptFromTab\(/);
  assert.match(save, /message\.tab_id\s*\?\?\s*sender\?\.tab\?\.id/);
  assert.match(save, /resetAutoStartPromptFromTab\(/);
});

test('popup save and reset start-prompt actions transport current tab id', () => {
  const saveStart = popupSource.indexOf('type: "WS_SAVE_AUTO_START_PROMPT"');
  assert.notEqual(saveStart, -1);
  assert.match(popupSource.slice(saveStart, saveStart + 300), /tab_id:\s*context\.tab_id/);
  const resetStart = popupSource.indexOf('type: "WS_RESET_AUTO_START_PROMPT"');
  assert.notEqual(resetStart, -1);
  assert.match(popupSource.slice(resetStart, resetStart + 300), /tab_id:\s*context\.tab_id/);
});
