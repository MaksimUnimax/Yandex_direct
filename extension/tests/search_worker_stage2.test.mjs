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

test('Search credential capability reuses local API key + folderId without exposing a new assistant credential field', () => {
  const h = harness();
  const registry = h.ctx.YMBCredentialRegistry;
  assert.deepEqual(clone(registry.searchCapability({ apiKey: '', folderId: 'f' })), { state: 'MISSING', has_api_key: false, has_folder_id: true });
  assert.deepEqual(clone(registry.searchCapability({ apiKey: 'k', folderId: '' })), { state: 'MISSING', has_api_key: true, has_folder_id: false });
  assert.equal(registry.capabilityForService('search', { apiKey: 'k', folderId: 'f' }).state, 'PRESENT');
  assert.equal(registry.capabilityForService('wordstat', { apiKey: 'k', folderId: 'f' }).state, 'PRESENT');
  assert.equal(registry.capabilityForService('unknown', { apiKey: 'k', folderId: 'f' }).state, 'NO_ACCESS');
});

test('Search policy has conservative 0.488 RUB guard and enforces request/cost/method/channel limits', () => {
  const h = harness();
  const policy = h.ctx.YMBPolicyModel;
  const normalized = policy.normalizeSearchPolicy({ autorun_enabled: true });
  assert.deepEqual(Array.from(normalized.allowed_methods), ['search']);
  assert.equal(normalized.method_cost_rub.search, 0.488);
  assert.equal(normalized.tariff_checked_at, '2026-08-19');
  assert.equal(policy.searchDecision({ policy: normalized, channel: 'autorun', method: 'search', credentialState: 'MISSING', run: {} }).reason, 'NO_CREDENTIALS');
  assert.equal(policy.searchDecision({ policy: { ...normalized, autorun_enabled: false }, channel: 'autorun', method: 'search', credentialState: 'PRESENT', run: {} }).reason, 'AUTORUN_DISABLED');
  assert.equal(policy.searchDecision({ policy: { ...normalized, manual_enabled: false }, channel: 'manual', method: 'search', credentialState: 'PRESENT', run: {} }).reason, 'MANUAL_DISABLED');
  assert.equal(policy.searchDecision({ policy: { ...normalized, allowed_methods: [] }, channel: 'manual', method: 'search', credentialState: 'PRESENT', run: {} }).reason, 'OPERATION_DISABLED');
  assert.equal(policy.searchDecision({ policy: { ...normalized, max_requests_per_run: 1 }, channel: 'autorun', method: 'search', credentialState: 'PRESENT', run: { requests_executed: 1 } }).reason, 'REQUEST_LIMIT');
  assert.equal(policy.searchDecision({ policy: { ...normalized, max_cost_rub_per_run: 0.48 }, channel: 'autorun', method: 'search', credentialState: 'PRESENT', run: {} }).reason, 'COST_LIMIT');
  assert.equal(policy.decisionForService('search', { policy: normalized, channel: 'autorun', method: 'search', credentialState: 'PRESENT', run: {} }).allow, true);
});

test('worker Search admission reserves request and RUB totals before provider initiation', () => {
  const h = harness();
  const a = h.api;
  const settings = { apiKey: 'ascii-key', folderId: 'folder' };
  const policy = h.ctx.YMBPolicyModel.normalizeSearchPolicy({ autorun_enabled: true, max_requests_per_run: 3, max_cost_rub_per_run: 2 });
  const allowed = a.serviceExecutionAdmission('search', { settings, policy, channel: 'autorun', command: { method:'search', queryText:'брендовый запрос' }, run: { requests_executed:0, estimated_cost_rub:0 } });
  assert.equal(allowed.allow, true);
  assert.equal(allowed.estimated_cost_rub, 0.488);
  assert.equal(allowed.reserved_totals.requests_executed, 1);
  assert.equal(allowed.reserved_totals.estimated_cost_rub, 0.488);
  const blocked = a.serviceExecutionAdmission('search', { settings, policy:{ ...policy, max_requests_per_run:1 }, channel:'autorun', command:{method:'search',queryText:'x'}, run:{requests_executed:1,estimated_cost_rub:0.488} });
  assert.equal(blocked.allow, false);
  assert.equal(blocked.reason, 'REQUEST_LIMIT');
});

test('worker persists Search policy separately from Wordstat policy', async () => {
  const h = harness({ ymb_wordstat_policy:{autorun_enabled:false,max_requests_per_run:2}, ymb_search_policy:{autorun_enabled:true,max_requests_per_run:5,max_cost_rub_per_run:4} });
  assert.equal((await h.api.getPolicyForService('search')).autorun_enabled,true);
  assert.equal((await h.api.getPolicyForService('search')).max_requests_per_run,5);
  assert.equal((await h.api.getPolicyForService('wordstat')).max_requests_per_run,2);
  await h.api.saveSearchPolicy({autorun_enabled:false,max_requests_per_run:7,max_cost_rub_per_run:6});
  assert.equal(h.store.ymb_search_policy.max_requests_per_run,7);
  assert.equal(h.store.ymb_wordstat_policy.max_requests_per_run,2);
});

test('accepted Search provider execution performs exactly one POST and normalizes XML into SEARCH_RESULT_V1', async () => {
  const h = harness({ wsmb_api_key: 'ascii-key', wsmb_folder_id: 'folder' });
  const result = await h.api.executeSearchCore(searchCommand('брендовый запрос'), { run_id:'r-search', conversation_key:CKEY, cost_estimate:{estimated_rub:0.488}, policy:{channel:'autorun',active_service:'search'} });
  assert.equal(h.fetchCalls.length, 1);
  assert.equal(h.fetchCalls[0][0], 'https://searchapi.api.cloud.yandex.net/v2/web/search');
  assert.equal(h.fetchCalls[0][1].method, 'POST');
  assert.match(h.fetchCalls[0][1].headers.Authorization, /^Api-Key /);
  const body = JSON.parse(h.fetchCalls[0][1].body);
  assert.equal(body.query.queryText, 'брендовый запрос');
  assert.equal(body.folderId, 'folder');
  assert.equal(body.responseFormat, 'FORMAT_XML');
  assert.equal(result.ok, true);
  assert.match(result.report_text, /^SEARCH_RESULT_V1\n/);
  assert.equal(result.report_envelope.service, 'search');
  assert.equal(result.report_envelope.operation, 'search');
  assert.equal(result.report_envelope.request_executed, true);
  assert.equal(result.report_envelope.automatic_retry, false);
  assert.equal(result.report_envelope.result.documents[0].url, 'https://example.test/a');
});

test('Search validation and credential rejection happen before fetch', async () => {
  const invalid = harness({ wsmb_api_key: 'ascii-key', wsmb_folder_id: 'folder' });
  await assert.rejects(() => invalid.api.executeSearchCore('SEARCH_API_V1\n{"method":"search","queryText":""}'));
  assert.equal(invalid.fetchCalls.length, 0);
  const missing = harness({ wsmb_api_key: '', wsmb_folder_id: 'folder' });
  await assert.rejects(() => missing.api.executeSearchCore(searchCommand()), (error) => error.code === 'API_KEY_MISSING');
  assert.equal(missing.fetchCalls.length, 0);
});

test('Search HTTP error is truthful, executed once, and never retries', async () => {
  const h = harness({ wsmb_api_key: 'ascii-key', wsmb_folder_id: 'folder' }, { fetchImpl: async () => new Response(JSON.stringify({ code: 429, message:'too many' }), { status: 429 }) });
  const result = await h.api.executeSearchCore(searchCommand());
  assert.equal(h.fetchCalls.length, 1);
  assert.equal(result.ok, false);
  assert.equal(result.report_envelope.request_executed, true);
  assert.equal(result.report_envelope.automatic_retry, false);
  assert.equal(result.report_envelope.http_status, 429);
});

test('Search ambiguous network failure is UNKNOWN and no second provider initiation occurs', async () => {
  const h = harness({ wsmb_api_key: 'ascii-key', wsmb_folder_id: 'folder' }, { fetchImpl: async () => { throw new TypeError('connection lost'); } });
  await assert.rejects(() => h.api.executeSearchCore(searchCommand()), (error) => {
    assert.equal(error.code, 'REQUEST_OUTCOME_UNKNOWN_NO_RETRY');
    assert.equal(error.request_executed, 'UNKNOWN');
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(h.fetchCalls.length, 1);
});

test('Search response-normalization failure remains executed=true and no retry', async () => {
  const h = harness({ wsmb_api_key: 'ascii-key', wsmb_folder_id: 'folder' }, {
    fetchImpl: async () => new Response(JSON.stringify({ rawData: 'not-base64!' }), { status: 200 })
  });
  await assert.rejects(() => h.api.executeServiceCore('search', searchCommand()), (error) => {
    assert.equal(error.code, 'INVALID_SEARCH_BASE64');
    assert.equal(error.request_executed, true);
    assert.equal(error.automatic_retry, false);
    return true;
  });
  assert.equal(h.fetchCalls.length, 1);
});

test('worker service routing keeps Search and Wordstat protocols isolated', async () => {
  const h = harness({ wsmb_api_key: 'ascii-key', wsmb_folder_id: 'folder' });
  assert.equal(h.api.protocolForService('search').PREFIX, 'SEARCH_API_V1');
  assert.equal(h.api.protocolForService('wordstat').PREFIX, 'WORDSTAT_API_V1');
  assert.equal(h.api.protocolForService('unknown'), null);
  await assert.rejects(() => h.api.executeServiceCore('unknown', searchCommand()), (error) => error.code === 'SERVICE_NOT_AVAILABLE');
  assert.equal(h.fetchCalls.length, 0);
});

test('Phase-2 Search Autorun accepts one Search command, stages one delivery, and duplicate cannot initiate again', async () => {
  const h = harness({
    wsmb_api_key:'ascii-key', wsmb_folder_id:'folder',
    wsmb_conversation_bindings:{[CKEY]:binding()},
    wsmb_auto_runs:{[CKEY]:waitingSearchRun('search')},
    ymb_service_contexts:{[CKEY]:{active_service:'search'}},
    ymb_search_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['search'],max_requests_per_run:10,max_cost_rub_per_run:10,method_cost_rub:{search:0.488},tariff_checked_at:'2026-08-19',tariff_source:'test'}
  });
  const first=await h.api.handleAutoCommand({conversation_key:CKEY,run_id:'search-run',assistant_turn_id:'a-search-1',command_text:searchCommand('авто поиск')},{tab:{id:1}});
  assert.equal(first.accepted,true);
  assert.equal(h.fetchCalls.length,1);
  assert.match(first.report_text,/^SEARCH_RESULT_V1\n/);
  assert.equal(h.store.wsmb_auto_runs[CKEY].active_service,'search');
  assert.equal(h.store.wsmb_auto_runs[CKEY].requests_executed,1);
  const second=await h.api.handleAutoCommand({conversation_key:CKEY,run_id:'search-run',assistant_turn_id:'a-search-1',command_text:searchCommand('авто поиск')},{tab:{id:1}});
  assert.equal(second.accepted,false);
  assert.equal(h.fetchCalls.length,1);
});

test('Autorun service isolation rejects Search command in Wordstat RUN and Wordstat command in Search RUN before fetch', async () => {
  const searchRun=harness({
    wsmb_api_key:'ascii-key',wsmb_folder_id:'folder',wsmb_conversation_bindings:{[CKEY]:binding()},wsmb_auto_runs:{[CKEY]:waitingSearchRun('search')},ymb_service_contexts:{[CKEY]:{active_service:'search'}},ymb_search_policy:{autorun_enabled:true}
  });
  const wrongWordstat=await searchRun.api.handleAutoCommand({conversation_key:CKEY,run_id:'search-run',assistant_turn_id:'x',command_text:'WORDSTAT_API_V1\n{"method":"getRegionsTree"}'},{tab:{id:1}});
  assert.equal(wrongWordstat.code,'SERVICE_NOT_ACTIVE');
  assert.equal(searchRun.fetchCalls.length,0);

  const wordstatRun=harness({
    wsmb_api_key:'ascii-key',wsmb_folder_id:'folder',wsmb_conversation_bindings:{[CKEY]:binding()},wsmb_auto_runs:{[CKEY]:waitingSearchRun('wordstat')},ymb_service_contexts:{[CKEY]:{active_service:'wordstat'}},ymb_wordstat_policy:{autorun_enabled:true}
  });
  const wrongSearch=await wordstatRun.api.handleAutoCommand({conversation_key:CKEY,run_id:'search-run',assistant_turn_id:'y',command_text:searchCommand('wrong service')},{tab:{id:1}});
  assert.equal(wrongSearch.code,'SERVICE_NOT_ACTIVE');
  assert.equal(wordstatRun.fetchCalls.length,0);
});

test('Search settings backup/export-import surface includes separate Search policy without exposing credentials in policy', async () => {
  const h=harness({wsmb_api_key:'secret-ascii',wsmb_folder_id:'folder',ymb_search_policy:{autorun_enabled:true,manual_enabled:true,allowed_methods:['search'],max_requests_per_run:7,max_cost_rub_per_run:3,method_cost_rub:{search:0.488},tariff_checked_at:'2026-08-19',tariff_source:'test'}});
  const backup=await h.api.exportSettingsBackup();
  assert.equal(backup.settings.search_policy.autorun_enabled,true);
  assert.equal(backup.settings.search_policy.max_requests_per_run,7);
  assert.equal(backup.settings.search_policy.method_cost_rub.search,0.488);
  assert.equal(Object.hasOwn(backup.settings.search_policy,'api_key'),false);
  const imported=harness({wsmb_api_key:'keep',wsmb_folder_id:'keep-folder'});
  const result=await imported.api.importSettingsBackup(backup);
  assert.equal(result.imported,true);
  assert.equal(imported.store.ymb_search_policy.max_requests_per_run,7);
  assert.equal(imported.store.wsmb_api_key,'secret-ascii');
});
