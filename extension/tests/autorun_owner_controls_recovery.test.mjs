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

const lifecycleSource = ['pauseAutoRun', 'resumeAutoRun', 'finishAutoRun'].map(extractFunction).join('\n');

function harness(status = 'waiting_command') {
  let run = {
    run_id: 'run-owner',
    conversation_key: CKEY,
    conversation_id: CID,
    active_service: 'search',
    tab_id: 1,
    status,
    pause_requested: false,
    finish_requested: false
  };
  const identityChecks = [];
  const ctx = vm.createContext({
    normalizeConversationKey: (value) => value,
    getAutoRun: async () => structuredClone(run),
    patchAutoRun: async (_key, fn) => { run = fn(structuredClone(run)); return structuredClone(run); },
    assertTabConversation: async (tabId, key, conversationId) => {
      identityChecks.push({ tabId, key, conversationId });
      return { conversation_id: CID, conversation_key: CKEY };
    },
    WordstatAutorunModel: {
      RUN_STATUSES: { WAITING_COMMAND: 'waiting_command', PAUSED: 'paused', STOPPED: 'stopped' },
      pauseDecision: (value) => value === 'waiting_command' ? 'immediate' : value === 'paused' ? 'already_paused' : 'deferred',
      isTerminalStatus: (value) => value === 'stopped' || value === 'error'
    },
    structuredClone
  });
  vm.runInContext(`${lifecycleSource}; globalThis.api = { pauseAutoRun, resumeAutoRun, finishAutoRun };`, ctx);
  return { api: ctx.api, get run() { return run; }, identityChecks };
}

async function expectNonOwnerRejected(call) {
  await assert.rejects(call, (error) => error?.code === 'AUTO_NON_OWNER_TAB');
}

test('same-conversation non-owner tab cannot pause owner Autorun', async () => {
  const h = harness('waiting_command');
  await expectNonOwnerRejected(() => h.api.pauseAutoRun(CKEY, 2));
  assert.equal(h.run.status, 'waiting_command');
});

test('same-conversation non-owner tab cannot resume owner Autorun', async () => {
  const h = harness('paused');
  await expectNonOwnerRejected(() => h.api.resumeAutoRun(CKEY, 2));
  assert.equal(h.run.status, 'paused');
});

test('same-conversation non-owner tab cannot finish owner Autorun', async () => {
  const h = harness('waiting_command');
  await expectNonOwnerRejected(() => h.api.finishAutoRun(CKEY, 2));
  assert.equal(h.run.status, 'waiting_command');
});

test('owner lifecycle control confirms live tab identity before mutation', async () => {
  const h = harness('waiting_command');
  const paused = await h.api.pauseAutoRun(CKEY, 1);
  assert.equal(paused.status, 'paused');
  assert.deepEqual(h.identityChecks, [{ tabId: 1, key: CKEY, conversationId: CID }]);
});

test('popup transports active tab id for pause, resume and finish lifecycle commands', () => {
  for (const type of ['WS_PAUSE_AUTORUN', 'WS_RESUME_AUTORUN', 'WS_FINISH_AUTORUN']) {
    const index = popupSource.indexOf(`type: "${type}"`);
    assert.notEqual(index, -1, `${type} popup message not found`);
    const slice = popupSource.slice(index, index + 180);
    assert.match(slice, /tab_id:\s*context\.tab_id/, `${type} must transport active tab id`);
  }
});
