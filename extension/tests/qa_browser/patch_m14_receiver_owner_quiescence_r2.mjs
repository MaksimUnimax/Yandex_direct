import fs from 'node:fs';

const target = process.argv[2];
if (!target || !fs.existsSync(target)) throw new Error(`M14_R2_TARGET_MISSING ${target || '<empty>'}`);

let source = fs.readFileSync(target, 'utf8');

const workerNeedle = `  const worker = await swTarget.worker();
  assert(worker, 'MV3_WORKER_CONTEXT_FAIL');

  const { popup, ownerTabId } = await openPopup(worker, browser);`;

const workerReplacement = `  const worker = await swTarget.worker();
  assert(worker, 'MV3_WORKER_CONTEXT_FAIL');

  const ownerReceiverReady = await worker.evaluate(async ({ expectedKey, files }) => {
    const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    const active = tabs?.[0] || null;
    if (!active?.id) return { ok: false, code: 'OWNER_TAB_MISSING' };
    await chrome.tabs.update(active.id, { active: true });
    const probe = async () => await new Promise((resolve) => {
      chrome.tabs.sendMessage(active.id, { type: 'WS_GET_IDENTITY' }, (response) => {
        const error = chrome.runtime.lastError;
        resolve({ response: response || null, error: error?.message || '' });
      });
    });
    const usable = (p) => {
      const key = String(p?.response?.conversation_key || p?.response?.identity?.conversation_key || '').trim();
      return p?.response?.ok === true && key === expectedKey;
    };
    let last = null;
    let sawLiveReceiver = false;
    for (let attempt = 0; attempt < 3; attempt += 1) {
      last = await probe();
      if (usable(last)) return { ok: true, recovered: false, tab_id: active.id };
      if (!last?.error) sawLiveReceiver = true;
      await delay(120);
    }
    if (sawLiveReceiver) return { ok: false, code: 'OWNER_LIVE_RECEIVER_BAD_IDENTITY', last };
    for (const file of files) await chrome.scripting.executeScript({ target: { tabId: active.id }, files: [file] });
    for (let attempt = 0; attempt < 40; attempt += 1) {
      last = await probe();
      if (usable(last)) return { ok: true, recovered: true, tab_id: active.id };
      await delay(80);
    }
    return { ok: false, code: 'OWNER_RECEIVER_RECOVERY_TIMEOUT', last };
  }, {
    expectedKey: CKEY,
    files: [
      'shared/product.js',
      'shared/conversation_identity.js',
      'shared/service_registry.js',
      'shared/wordstat_protocol.js',
      'shared/search_xml.js',
      'shared/search_protocol.js',
      'shared/metrika_protocol.js',
      'shared/autorun_model.js',
      'shared/manual_controls.js',
      'shared/composer_send.js',
      'shared/proven_writing_block_capture.js',
      'content_script.js'
    ]
  });
  assert(ownerReceiverReady?.ok === true, \`M14_OWNER_RECEIVER_READY_FAIL \${JSON.stringify(ownerReceiverReady)}\`);
  console.log('M14_OWNER_RECEIVER_READY_PASS');

  const { popup, ownerTabId } = await openPopup(worker, browser);`;

if (!source.includes(workerNeedle)) throw new Error('M14_R2_WORKER_NEEDLE_MISSING');
source = source.replace(workerNeedle, workerReplacement);

const metaNeedle = `  await popup.waitForFunction((expected) => document.getElementById('conversationMeta')?.textContent === expected, { timeout: 12000 }, CKEY);`;
const metaReplacement = `  const ownerKeeper = worker.evaluate(async (ownerTabId) => {
    for (let attempt = 0; attempt < 160; attempt += 1) {
      try { await chrome.tabs.update(ownerTabId, { active: true }); } catch {}
      await new Promise((resolve) => setTimeout(resolve, 50));
    }
    return true;
  }, owner.active.id);
  await popup.reload({ waitUntil: 'load', timeout: 12000 });
  const stableBootstrap = await waitUntil(async () => await popup.evaluate(() => {
    const error = globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__ || '';
    const result = globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__ || null;
    if (!error && !result) return null;
    return { error, result, status: document.getElementById('status')?.textContent || '', meta: document.getElementById('conversationMeta')?.textContent || '' };
  }), 'M14_R2_STABLE_POPUP_BOOTSTRAP_OUTCOME_TIMEOUT', 16000, 80);
  if (stableBootstrap.error) throw new Error(\`M14_R2_STABLE_POPUP_BOOTSTRAP_ERROR \${stableBootstrap.error}\`);
  assert(stableBootstrap.result?.attempted === true, \`M14_R2_STABLE_POPUP_BOOTSTRAP_NOT_ATTEMPTED \${JSON.stringify(stableBootstrap)}\`);
  await popup.waitForFunction((expected) => document.getElementById('conversationMeta')?.textContent === expected, { timeout: 20000 }, CKEY);
  const ownerKept = await ownerKeeper;
  assert(ownerKept === true, 'M14_R2_OWNER_KEEPER_FAIL');
  console.log('M14_OWNER_RECEIVER_RELOAD_QUIESCENCE_PASS');`;

const metaCount = source.split(metaNeedle).length - 1;
if (metaCount !== 1) throw new Error(`M14_R2_META_NEEDLE_COUNT ${metaCount}`);
if (!source.includes('__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__')) throw new Error('M14_R2_REQUIRES_PROVEN_BOOTSTRAP_PATCH');
source = source.replace(metaNeedle, metaReplacement);

fs.writeFileSync(target, source, 'utf8');
console.log('M14_RECEIVER_OWNER_QUIESCENCE_R2_PATCHED');
