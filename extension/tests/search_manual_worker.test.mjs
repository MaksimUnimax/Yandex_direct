import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { webcrypto } from 'node:crypto';
import { performance } from 'node:perf_hooks';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const workerSource = fs.readFileSync(path.join(root, 'service_worker.js'), 'utf8');
const FN_NAMES = [...workerSource.matchAll(/^(?:async )?function\s+([A-Za-z0-9_]+)/gm)].map((m) => m[1]);
const CID = '99999999-8888-4777-8666-555555555555';
const ORIGIN = 'https://chatgpt.com';
const CKEY = `${ORIGIN}|${CID}`;
const IDENTITY = { origin: ORIGIN, conversation_id: CID, status: 'confirmed', source: 'path', chat_path: `/c/${CID}` };
function binding() { return { binding_id:'b-search', revision:1, origin:ORIGIN, conversation_id:CID, conversation_key:CKEY, bound_at:'2026-08-20T00:00:00Z', updated_at:'2026-08-20T00:00:00Z' }; }
function waitingSearchRun(activeService='search') { return {
  run_id:'search-run', active_service:activeService, permission_profile:activeService.toUpperCase(), requests_attempted:0, requests_executed:0, requests_skipped:0, estimated_cost_rub:0,
  conversation_key:CKEY, origin:ORIGIN, conversation_id:CID, binding_snapshot:{binding_id:'b-search',binding_revision:1,origin:ORIGIN,conversation_id:CID,conversation_key:CKEY}, tab_id:1,
  status:'waiting_command', sequence:0, pause_requested:false, finish_requested:false, assistant_baseline_ids:[], watch_id:'watch-search', start_delivery:{phase:'confirmed',message_text:'START'}, delivery:null
}; }

function clone(value) {
  return value === undefined ? undefined : structuredClone(value);
}

function searchCommand(queryText = 'оберег в машину') {
  return `SEARCH_API_V1\n${JSON.stringify({ method: 'search', queryText })}`;
}

function searchXmlBase64() {
  const xml = `<?xml version="1.0" encoding="UTF-8"?><yandexsearch><response><results><grouping><group><doc><url>https://example.test/a</url><domain>example.test</domain><title>Пример &amp; тест</title><passages><passage>Первый <hlword>фрагмент</hlword></passage><passage>Второй</passage></passages><modtime>20260820T010203</modtime></doc></group></grouping></results></response></yandexsearch>`;
  return Buffer.from(xml, 'utf8').toString('base64');
}

function harness(initial = {}, opts = {}) {
  const store = clone(initial);
  let listener = null;
  let fetchImpl = opts.fetchImpl || (async () => new Response(JSON.stringify({ rawData: searchXmlBase64() }), { status: 200 }));
  const fetchCalls = [];
  const runtime = { id: 'test-extension', lastError: null, onMessage: { addListener(fn) { listener = fn; } } };
  const storage = {
    async get(keys) {
      if (keys == null) return clone(store);
      if (typeof keys === 'string') return Object.hasOwn(store, keys) ? { [keys]: clone(store[keys]) } : {};
      if (Array.isArray(keys)) {
        const out = {};
        for (const key of keys) if (Object.hasOwn(store, key)) out[key] = clone(store[key]);
        return out;
      }
      if (typeof keys === 'object') {
        const out = clone(keys);
        for (const key of Object.keys(keys)) if (Object.hasOwn(store, key)) out[key] = clone(store[key]);
        return out;
      }
      return {};
    },
    async set(values) { Object.assign(store, clone(values)); },
    async remove(keys) { for (const key of (Array.isArray(keys) ? keys : [keys])) delete store[key]; }
  };
  const chrome = {
    storage: { local: storage },
    runtime,
    tabs: {
      async query() { return [{ id:1, url:`${ORIGIN}/c/${CID}` }]; },
      async get(id) { return Number(id)===1 ? { id:1, url:`${ORIGIN}/c/${CID}` } : null; },
      sendMessage(_id, message, callback) {
        if (["WS_GET_IDENTITY","WS_PAGE_CONTEXT"].includes(message?.type)) return callback({ok:true,identity:IDENTITY,conversation_key:CKEY});
        callback({ ok: true });
      }
    }
  };
  const ctx = vm.createContext({
    console,
    chrome,
    crypto: webcrypto,
    TextEncoder,
    TextDecoder,
    AbortController,
    performance,
    setTimeout,
    clearTimeout,
    URL,
    structuredClone,
    Response,
    Request,
    Headers,
    ReadableStream,
    Buffer,
    fetch: async (...args) => {
      fetchCalls.push(args);
      return fetchImpl(...args);
    },
    importScripts: () => {}
  });
  ctx.globalThis = ctx;
  for (const file of [
    'shared/product.js',
    'shared/conversation_identity.js',
    'shared/manual_controls.js',
    'shared/service_registry.js',
    'shared/block_command_discovery.js',
    'shared/run_context_model.js',
    'shared/credential_registry.js',
    'shared/policy_model.js',
    'shared/cost_ledger_model.js',
    'shared/wordstat_protocol.js',
    'shared/search_xml.js',
    'shared/search_protocol.js',
    'shared/autorun_model.js'
  ]) {
    vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx, { filename: file });
  }
  vm.runInContext(workerSource, ctx, { filename: 'service_worker.js' });
  assert.equal(typeof listener, 'function');
  vm.runInContext(`globalThis.__STAGE2_API = Object.freeze({${FN_NAMES.join(',')},KEYS});`, ctx, { filename: 'stage2_export.js' });
  return {
    api: ctx.__STAGE2_API,
    ctx,
    store,
    fetchCalls,
    setFetch(fn) { fetchImpl = fn; }
  };
}

test('Manual Search executes one provider request and stages one delivery', async () => {
  const h = harness({
    wsmb_api_key:'ascii-key', wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding()},
    wsmb_manual_modes:{[CKEY]:true},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{manual_enabled:true,autorun_enabled:false,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10,method_cost_rub:{search:0.488}}
  });
  const r = await h.api.executeManualBlock(searchCommand('ручной поиск'), CKEY, {tab:{id:1}}, 'manual-1');
  assert.equal(r.accepted,true);
  assert.equal(r.request_executed,true);
  assert.equal(h.fetchCalls.length,1);
  assert.match(r.report_text,/^SEARCH_RESULT_V1\n/);
  const outbox=h.store.wsmb_outbox[CKEY];
  assert.equal(outbox.type,'manual');
  assert.equal(outbox.delivery_id,r.delivery_id);
  assert.match(outbox.report_text,/^SEARCH_RESULT_V1\n/);
});

test('Manual wrong-service block is rejected before claim and before fetch', async () => {
  const h = harness({
    wsmb_api_key:'ascii-key', wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding()},
    wsmb_manual_modes:{[CKEY]:true},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{manual_enabled:true}
  });
  const r = await h.api.executeManualBlock('WORDSTAT_API_V1\n{"method":"getRegionsTree"}', CKEY, {tab:{id:1}}, 'manual-wrong');
  assert.equal(r.accepted,false);
  assert.equal(r.code,'SERVICE_NOT_ACTIVE');
  assert.equal(r.request_executed,false);
  assert.equal(h.fetchCalls.length,0);
  assert.equal(h.store.wsmb_manual_operations,undefined);
  assert.equal(h.store.wsmb_outbox,undefined);
});

test('Manual block without supported command produces bridge error with zero provider requests', async () => {
  const h = harness({
    wsmb_api_key:'ascii-key', wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding()},
    wsmb_manual_modes:{[CKEY]:true},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{manual_enabled:true}
  });
  const r=await h.api.executeManualBlock('обычный текст без команды', CKEY, {tab:{id:1}}, 'manual-empty');
  assert.equal(r.accepted,true);
  assert.equal(r.request_executed,false);
  assert.equal(h.fetchCalls.length,0);
  assert.match(r.report_text,/^YMB_ERROR_V1\n/);
  assert.match(r.report_text,/NO_SUPPORTED_COMMAND/);
  const errorPayload=JSON.parse(r.report_text.split('\n').slice(1).join('\n'));
  assert.equal(errorPayload.service,'search');
  assert.equal(errorPayload.channel,'manual');
  assert.equal(errorPayload.stage,'COMMAND_DISCOVERY');
  assert.equal(errorPayload.recoverable,true);
  assert.equal(errorPayload.request_executed,false);
  assert.equal(errorPayload.automatic_retry,false);
  assert.equal(errorPayload.operation,null);
  assert.equal(errorPayload.autorun_continues,false);
  assert.match(errorPayload.timestamp,/^\d{4}-\d{2}-\d{2}T/);
});

test('Manual single-flight prevents a second provider request while first delivery is pending', async () => {
  const h = harness({
    wsmb_api_key:'ascii-key', wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding()},
    wsmb_manual_modes:{[CKEY]:true},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{manual_enabled:true,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10}
  });
  const first=await h.api.executeManualBlock(searchCommand('один раз'), CKEY, {tab:{id:1}}, 'same-token');
  assert.equal(first.accepted,true);
  const second=await h.api.executeManualBlock(searchCommand('один раз'), CKEY, {tab:{id:1}}, 'same-token');
  assert.equal(second.accepted,false);
  assert.equal(h.fetchCalls.length,1);
});

test('Manual Search on paused Search run uses the same request budget and blocks before fetch', async () => {
  const run=waitingSearchRun('search');
  run.status='paused';
  run.requests_executed=1;
  run.estimated_cost_rub=0.488;
  const h=harness({
    wsmb_api_key:'ascii-key',wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding()},
    wsmb_manual_modes:{[CKEY]:true},
    wsmb_auto_runs:{[CKEY]:run},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{manual_enabled:true,autorun_enabled:true,allowed_methods:['search'],max_requests_per_run:1,max_cost_rub_per_run:10,method_cost_rub:{search:0.488}}
  });
  const r=await h.api.executeManualBlock(searchCommand('лимит'),CKEY,{tab:{id:1}},'paused-budget');
  assert.equal(r.accepted,true);
  assert.equal(r.request_executed,false);
  assert.equal(h.fetchCalls.length,0);
  assert.match(r.report_text,/REQUEST_LIMIT/);
  assert.equal(h.store.wsmb_auto_runs[CKEY].requests_executed,1);
});

test('Manual provider HTTP error is delivered once and not retried', async () => {
  const h=harness({
    wsmb_api_key:'ascii-key',wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding()},
    wsmb_manual_modes:{[CKEY]:true},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{manual_enabled:true,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10}
  }, {fetchImpl: async()=>new Response(JSON.stringify({message:'denied'}),{status:403})});
  const r=await h.api.executeManualBlock(searchCommand('ошибка'),CKEY,{tab:{id:1}},'http-error');
  assert.equal(r.accepted,true);
  assert.equal(h.fetchCalls.length,1);
  assert.match(r.report_text,/^SEARCH_RESULT_V1\n/);
  assert.match(r.report_text,/"http_status": 403/);
  assert.match(r.report_text,/"automatic_retry": false/);
});

test('Manual ambiguous network failure creates error delivery and never retries', async () => {
  const h=harness({
    wsmb_api_key:'ascii-key',wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding()},
    wsmb_manual_modes:{[CKEY]:true},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{manual_enabled:true,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10}
  }, {fetchImpl: async()=>{throw new TypeError('connection lost')}});
  const r=await h.api.executeManualBlock(searchCommand('unknown'),CKEY,{tab:{id:1}},'unknown');
  assert.equal(r.accepted,true);
  assert.equal(h.fetchCalls.length,1);
  assert.equal(r.request_executed,'UNKNOWN');
  assert.equal(h.store.wsmb_manual_operations[CKEY].request_executed,'UNKNOWN');
  assert.match(r.report_text,/^YMB_ERROR_V1\n/);
  assert.match(r.report_text,/REQUEST_OUTCOME_UNKNOWN_NO_RETRY/);
  assert.match(r.report_text,/"request_executed": "UNKNOWN"/);
  assert.match(r.report_text,/"automatic_retry": false/);
  const errorPayload=JSON.parse(r.report_text.split('\n').slice(1).join('\n'));
  assert.equal(errorPayload.channel,'manual');
  assert.equal(errorPayload.operation,'search');
  assert.equal(errorPayload.recoverable,false);
  assert.equal(errorPayload.autorun_continues,false);
});

test('saved report prefix is exposed in state and applies only to executed Manual API result', async () => {
  const h = harness({
    wsmb_api_key:'ascii-key', wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding()},
    wsmb_manual_modes:{[CKEY]:true},
    wsmb_report_prefixes:{[CKEY]:{enabled:true,text:'PREFIX',interval:1,delivered_count:0,last_applied_at_count:0}},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{manual_enabled:true,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10,method_cost_rub:{search:0.488}}
  });
  const state=await h.api.publicSettingsState(CKEY);
  assert.equal(state.report_prefix.enabled,true);
  assert.equal(state.report_prefix.text,'PREFIX');
  const r=await h.api.executeManualBlock(searchCommand('с префиксом'),CKEY,{tab:{id:1}},'prefix-manual');
  assert.equal(r.accepted,true);
  assert.match(r.report_text,/^PREFIX\n\nSEARCH_RESULT_V1\n/);
  assert.equal(h.store.wsmb_outbox[CKEY].report_prefix_applied,true);
  await h.api.completeDelivery({conversation_key:CKEY,delivery_id:r.delivery_id,confirmation_basis:'microphone'},{tab:{id:1}});
  assert.equal(h.store.wsmb_report_prefixes[CKEY].delivered_count,1);
  assert.equal(h.store.wsmb_report_prefixes[CKEY].last_applied_at_count,1);
});

test('zero-provider Manual bridge error does not receive API-result prefix', async () => {
  const h = harness({
    wsmb_api_key:'ascii-key', wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding()},
    wsmb_manual_modes:{[CKEY]:true},
    wsmb_report_prefixes:{[CKEY]:{enabled:true,text:'PREFIX',interval:1,delivered_count:0,last_applied_at_count:0}},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{manual_enabled:true}
  });
  const r=await h.api.executeManualBlock('обычный текст',CKEY,{tab:{id:1}},'prefix-no-provider');
  assert.equal(r.request_executed,false);
  assert.match(r.report_text,/^YMB_ERROR_V1\n/);
  assert.doesNotMatch(r.report_text,/^PREFIX/);
  assert.equal(h.store.wsmb_outbox[CKEY].report_prefix_applied,false);
});

test('report prefix enabled toggle changes only enabled state and preserves saved text', async () => {
  const h=harness({wsmb_report_prefixes:{[CKEY]:{enabled:false,text:'KEEP ME',interval:1,delivered_count:2,last_applied_at_count:1}}});
  const state=await h.api.patchToggleSettings({conversation_key:CKEY,report_prefix_enabled:true});
  assert.equal(state.report_prefix.enabled,true);
  assert.equal(state.report_prefix.text,'KEEP ME');
  assert.equal(h.store.wsmb_report_prefixes[CKEY].text,'KEEP ME');
  assert.equal(h.store.wsmb_report_prefixes[CKEY].delivered_count,2);
});
