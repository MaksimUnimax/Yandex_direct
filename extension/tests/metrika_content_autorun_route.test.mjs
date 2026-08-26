import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const CID = '55555555-4444-4333-8222-000000000004';
const ORIGIN = 'https://chatgpt.com';
const CKEY = `${ORIGIN}|${CID}`;
const COMMAND = 'METRIKA_API_V1\n{"method":"listCounters"}';

class FakeElement {
  constructor(tag = 'div') {
    this.tagName = String(tag).toUpperCase();
    this.id = '';
    this.className = '';
    this.dataset = {};
    this.style = {};
    this.isConnected = true;
    this.children = [];
    this.attrs = new Map();
  }
  setAttribute(name, value) { this.attrs.set(String(name), String(value)); }
  getAttribute(name) { return this.attrs.get(String(name)) || ''; }
  append(...items) { this.children.push(...items); }
  appendChild(item) { this.children.push(item); return item; }
  remove() { this.isConnected = false; }
  attachShadow() { return new FakeElement('shadow-root'); }
  querySelector() { return null; }
  addEventListener() {}
  removeEventListener() {}
  contains(other) { return other === this; }
  closest() { return this; }
  getBoundingClientRect() { return { top: 0, bottom: 100, left: 0, right: 100 }; }
}

function harness() {
  const messages = [];
  const listeners = [];
  const candidates = [];
  const identity = { origin: ORIGIN, conversation_id: CID, conversation_key: CKEY, status: 'confirmed', source: 'path', chat_path: `/c/${CID}` };
  const documentElement = new FakeElement('html');
  const document = {
    documentElement,
    body: new FakeElement('body'),
    querySelector() { return null; },
    getElementById() { return null; },
    createElement(tag) { return new FakeElement(tag); },
    addEventListener() {},
    removeEventListener() {}
  };
  const window = { innerWidth: 1280, innerHeight: 800, addEventListener() {} };
  class FakeMutationObserver { constructor(fn) { this.fn = fn; } observe() {} disconnect() {} }

  const ctx = vm.createContext({
    console,
    document,
    window,
    location: { href: `${ORIGIN}/c/${CID}` },
    MutationObserver: FakeMutationObserver,
    CSS: { escape(value) { return String(value); } },
    queueMicrotask,
    setTimeout() { return 1; },
    clearTimeout() {},
    Date,
    URL,
    URLSearchParams,
    structuredClone,
    __YMB_TEST__: true,
    chrome: {
      runtime: {
        lastError: null,
        onMessage: { addListener(fn) { listeners.push(fn); } },
        sendMessage(message, callback) {
          messages.push(structuredClone(message));
          if (message?.type === 'WS_GET_STATE') {
            callback({ ok: true, state: { service_context: { active_service: 'metrika' }, auto_run: null, manual_mode: false } });
            return;
          }
          if (message?.type === 'WS_AUTO_COMMAND') {
            callback({ ok: true, accepted: true });
            return;
          }
          callback({ ok: true });
        }
      }
    },
    BB2ConversationIdentity: { identityFromCandidates() { return identity; } },
    BB2ManualControls: { ACTION_LABEL: 'Яндекс', ACTION_ATTR: 'data-ymb-action', makeId(prefix) { return `${prefix}-1`; } },
    BB2ComposerSend: {
      findComposer() { return null; }, readComposer() { return ''; }, setComposerText() {}, findSendButton() { return null; }, composerReady() { return true; }
    },
    BB2ProvenWritingCapture: {
      candidateBlocks() { return candidates; },
      textFromBlock(block) { return String(block.text || ''); },
      assistantContainerFor(block) { return block.container || null; }
    },
    WordstatProtocol: { isCommandText(value) { return String(value).trim().startsWith('WORDSTAT_API_V1'); } },
    SearchProtocol: { isCommandText(value) { return String(value).trim().startsWith('SEARCH_API_V1'); } }
  });
  ctx.globalThis = ctx;

  for (const relative of ['shared/product.js', 'shared/service_registry.js', 'shared/metrika_protocol.js', 'content_script.js']) {
    vm.runInContext(fs.readFileSync(path.join(root, relative), 'utf8'), ctx, { filename: relative });
  }

  return { ctx, messages, candidates, api: ctx.__YMB_CONTENT_TEST_API__ };
}

test('M-17 content protocol routing maps Metrika to the installed MetrikaProtocol without changing legacy routes', () => {
  const h = harness();
  assert.equal(h.api.protocolForService('metrika'), h.ctx.MetrikaProtocol);
  assert.equal(h.api.protocolForService('wordstat'), h.ctx.WordstatProtocol);
  assert.equal(h.api.protocolForService('search'), h.ctx.SearchProtocol);
  assert.equal(h.api.protocolForService('webmaster'), null);
  assert.equal(h.api.protocolForService('future-service'), null);
});

test('M-17 content Autorun scan dispatches one METRIKA_API_V1 assistant turn exactly once', () => {
  const h = harness();
  const block = new FakeElement('div');
  block.text = COMMAND;
  block.container = {
    getAttribute(name) { return name === 'data-message-id' ? 'assistant-metrika-content-1' : ''; },
    id: ''
  };
  h.candidates.push(block);

  h.api.startAutoWatch({
    conversation_key: CKEY,
    run_id: 'run-metrika-content-1',
    active_service: 'metrika',
    watch_id: 'watch-metrika-content-1',
    assistant_baseline_ids: []
  });
  h.api.scanAutorun();

  const first = h.messages.filter((message) => message.type === 'WS_AUTO_COMMAND');
  assert.equal(first.length, 1);
  assert.deepEqual(first[0], {
    type: 'WS_AUTO_COMMAND',
    conversation_key: CKEY,
    run_id: 'run-metrika-content-1',
    watch_id: 'watch-metrika-content-1',
    assistant_turn_id: 'assistant-metrika-content-1',
    command_text: COMMAND
  });

  h.api.scanAutorun();
  const afterDuplicateScan = h.messages.filter((message) => message.type === 'WS_AUTO_COMMAND');
  assert.equal(afterDuplicateScan.length, 1);
});
