const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');
const source = fs.readFileSync(path.resolve(__dirname, '../../../src/file_delivery_content.js'), 'utf8');
const workerSource = fs.readFileSync(path.resolve(__dirname, '../../../src/file_delivery_worker_transport.js'), 'utf8');

const normalize = (value) => String(value || '').replace(/\u00a0/g, ' ').replace(/\r\n/g, '\n').trim().replace(/\s+/g, ' ');

function makeHarness({ initialComposer = '', autoSend = false } = {}) {
  const listeners = {};
  const storageListeners = new Set();
  const statusNodes = new Map();
  let composerText = initialComposer;
  let setComposerCalls = [];
  let pauseCalls = 0;
  let getOutboxCalls = 0;
  let outbox = {
    conversation_key: 'https://chatgpt.com|conv-1',
    delivery_id: 'delivery-p0',
    delivery_mode: 'attachment_v2',
    phase: 'attachment_ready',
    delivery_paused: false,
    report_text: 'SEARCH_ASYNC_BATCH_RESULT_V1\n{"action":"exportPage","job_id":"ram_smoke_20260914","ok":true}',
    artifact_descriptors: [{ filename: 'search-ram_smoke_20260914-r5-0-0.json' }]
  };

  const composer = { isConnected: true, contains: (node) => node === composer };
  const fakeButton = { isConnected: true, addEventListener() {}, removeEventListener() {} };
  const makeElement = () => ({
    isConnected: true, style: {}, textContent: '', disabled: false, onclick: null,
    setAttribute() {}, getAttribute() { return ''; }, addEventListener() {}, removeEventListener() {},
    remove() { this.isConnected = false; }
  });
  const document = {
    documentElement: { appendChild(node) { node.isConnected = true; if (node.id) statusNodes.set(node.id, node); } },
    querySelector(selector) {
      if (selector === 'link[rel="canonical"]') return { href: 'https://chatgpt.com/c/conv-1' };
      return null;
    },
    querySelectorAll() { return []; },
    createElement() { return makeElement(); },
    getElementById(id) { return statusNodes.get(id) || null; },
    addEventListener(type, fn) { (listeners[type] ||= new Set()).add(fn); },
    removeEventListener(type, fn) { listeners[type]?.delete(fn); }
  };

  const chrome = {
    runtime: {
      lastError: null,
      sendMessage(message, cb) {
        if (message.type === 'WS_GET_OUTBOX') {
          getOutboxCalls++;
          cb({ ok: true, outbox: { ...outbox } });
          return;
        }
        if (message.type === 'WS_GET_STATE') { cb({ ok: true, state: { auto_send: autoSend, send_button_profile: null } }); return; }
        if (message.type === 'WS_SET_ATTACHMENT_PAUSED') {
          pauseCalls++;
          outbox = { ...outbox, delivery_paused: message.paused === true };
          for (const fn of storageListeners) fn({ wsmb_outbox: { newValue: { [outbox.conversation_key]: outbox } } }, 'local');
          cb({ ok: true, paused: outbox.delivery_paused, delivery_id: outbox.delivery_id, phase: outbox.phase });
          return;
        }
        cb({ ok: true });
      }
    },
    storage: {
      onChanged: {
        addListener(fn) { storageListeners.add(fn); },
        removeListener(fn) { storageListeners.delete(fn); }
      }
    }
  };

  const context = {
    console,
    setTimeout,
    clearTimeout,
    AbortController,
    Element: class {},
    HTMLElement: class {},
    location: { href: 'https://chatgpt.com/c/conv-1' },
    document,
    chrome,
    BB2ConversationIdentity: {
      identityFromCandidates() { return { status: 'confirmed', conversation_key: 'https://chatgpt.com|conv-1' }; }
    },
    BB2ComposerSend: {
      normalize,
      findComposer() { return composer; },
      readComposer() { return composerText; },
      setComposerText(_composer, value) {
        setComposerCalls.push(String(value));
        composerText = `  ${String(value).replace(/ /g, '\u00a0  ')}  `;
        return true;
      },
      resolveContext() { return { composer, form: null, root: { isConnected: true, contains: () => true } }; },
      findSendButton() { return fakeButton; },
      sendCandidates() { return [fakeButton]; },
      visible() { return true; },
      disabled() { return false; },
      targetFingerprint() { return 'fp'; },
      async waitForValidatedTarget() { return null; },
      validateTarget() { return { ok: true }; },
      clickSynchronously() { throw new Error('not used'); }
    },
    YMBChatGPTFileAttachment: {
      attachmentReady() { return true; },
      fileInput() { return { isConnected: true }; },
      sha256Hex: async () => '00',
      base64ToBytes: () => new Uint8Array(),
      createFile: () => ({}),
      setInputFiles() {}
    }
  };
  context.globalThis = context;
  vm.createContext(context);
  vm.runInContext(source, context, { filename: 'file_delivery_content.js' });

  return {
    async wait(ms) { await new Promise((r) => setTimeout(r, ms)); },
    setComposer(text) { composerText = text; },
    fireInput() { for (const fn of listeners.input || []) fn({ target: composer }); },
    getComposer: () => composerText,
    getOutbox: () => ({ ...outbox }),
    getSetComposerCalls: () => [...setComposerCalls],
    getPauseCalls: () => pauseCalls,
    getOutboxCalls: () => getOutboxCalls,
    dispose() { context.__YMB_FILE_DELIVERY_CONTENT_V4__?.dispose?.(); }
  };
}

(async () => {
  const h1 = makeHarness({ initialComposer: '' });
  await h1.wait(350);
  const staged = h1.getSetComposerCalls();
  assert(staged.length >= 1, 'safe marker should be staged for ready attachment');
  assert(!staged.some((v) => v.includes('SEARCH_ASYNC_BATCH_RESULT_V1')), 'internal protocol leaked into composer');
  assert(staged.some((v) => v.includes('search-ram_smoke_20260914-r5-0-0.json')), 'safe filename marker missing');
  assert.strictEqual(h1.getPauseCalls(), 0, 'normalized contenteditable readback must not falsely pause');
  h1.dispose();

  const h2 = makeHarness({ initialComposer: 'МОЙ ЧЕРНОВИК' });
  await h2.wait(350);
  assert.strictEqual(h2.getSetComposerCalls().length, 0, 'user draft must never be overwritten');
  assert.strictEqual(h2.getPauseCalls(), 1, 'fatal pre-send ownership conflict must persist pause exactly once');
  assert.strictEqual(h2.getOutbox().delivery_paused, true, 'outbox must be durably paused');

  h2.setComposer('');
  h2.fireInput();
  await h2.wait(200);
  assert.strictEqual(h2.getSetComposerCalls().length, 0, 'paused delivery must not reinsert after user clears composer');
  assert.strictEqual(h2.getPauseCalls(), 1, 'paused delivery must not re-pause/re-enter');
  assert(!h2.getComposer().includes('SEARCH_ASYNC_BATCH_RESULT_V1'), 'internal protocol reappeared after pause');
  h2.dispose();

  assert(!/entry\.send_marker\s*\|\|\s*entry\.report_text/.test(source), 'send reconciliation still falls back to report_text');
  assert(!/setComposerText\([^\n]*entry\.report_text/.test(source), 'stageMarker still writes report_text');
  assert(/PRE_SEND_PHASES\.has\(entry\?\.phase\)/.test(source), 'durable pause is not fenced to pre-send phases');
  assert(/pause\?\.code === "ATTACHMENT_SEND_ALREADY_COMMITTED"/.test(source), 'post-commit race does not preserve reconciliation-only mode');
  assert(/RECOVERY_POLL_MS\s*=\s*60_000/.test(source), '900ms permanent polling was not removed');
  assert(/\[SEND_COMMITTED_PHASE, "committed"\]\.includes\(owned\.entry\.phase\)/.test(workerSource), 'worker no longer fences pause after the Send barrier');

  console.log(JSON.stringify({
    ok: true,
    cases: 5,
    protocol_leak: 0,
    user_draft_overwrites: 0,
    durable_pause_calls: 1,
    reinsertion_after_pause: 0,
    recovery_poll_ms: 60000
  }, null, 2));
})().catch((error) => { console.error(error.stack || error); process.exit(1); });
