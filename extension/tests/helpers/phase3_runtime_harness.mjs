import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { webcrypto } from 'node:crypto';
import { performance } from 'node:perf_hooks';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../../src');

function storageHarness(initial = {}) {
  const state = structuredClone(initial);
  return {
    state,
    api: {
      async get(keys) {
        if (keys == null) return structuredClone(state);
        if (typeof keys === 'string') return state[keys] === undefined ? {} : { [keys]: structuredClone(state[keys]) };
        if (Array.isArray(keys)) return Object.fromEntries(keys.filter((key) => state[key] !== undefined).map((key) => [key, structuredClone(state[key])]));
        const out = {}; for (const [key, fallback] of Object.entries(keys || {})) out[key] = state[key] === undefined ? structuredClone(fallback) : structuredClone(state[key]); return out;
      },
      async set(values) { Object.assign(state, structuredClone(values)); },
      async remove(keys) { for (const key of Array.isArray(keys) ? keys : [keys]) delete state[key]; }
    }
  };
}

export function createPhase3Runtime(initial = {}) {
  const storage = storageHarness(initial);
  const listeners = [];
  const requests = [];
  const ctx = {
    console, Date, JSON, Math, Object, Array, Set, Map, Promise, Error, String, Number, Boolean, RegExp,
    TextEncoder, Uint8Array, URL, URLSearchParams, performance, crypto: webcrypto, structuredClone,
    globalThis: null,
    chrome: { runtime: { id: 'test-extension', onMessage: { addListener(fn) { listeners.push(fn); } } }, storage: { local: storage.api } },
    fetch: async (url, options = {}) => { requests.push({ url: String(url), options: structuredClone(options) }); return { ok: true, status: 200, text: async () => '{}' }; },
    YMBProduct: { VERSION: '0.1.1', BRIDGE_ID: 'yandex-marketing-bridge' },
    YMBServiceRegistry: { SERVICES: { WORDSTAT: 'wordstat', SEARCH: 'search', WEBMASTER: 'webmaster' } },
    YMBPolicyModel: {
      normalizeWordstatPolicy: (v = {}) => ({ manual_enabled: true, autorun_enabled: false, allowed_methods: [], max_requests_per_run: 50, max_cost_rub_per_run: 0, method_cost_rub: {}, tariff_checked_at: null, tariff_source: null, ...structuredClone(v) }),
      normalizeSearchPolicy: (v = {}) => ({ manual_enabled: true, autorun_enabled: false, allowed_methods: [], max_requests_per_run: 50, max_cost_rub_per_run: 0, method_cost_rub: {}, tariff_checked_at: null, tariff_source: null, ...structuredClone(v) }),
      normalizeWebmasterPolicy: (v = {}) => ({ manual_enabled: true, autorun_enabled: false, allowed_methods: ['listHosts','getSummary','getDiagnostics','getPopularQueries'], max_requests_per_run: 50, max_cost_rub_per_run: 0, method_cost_rub: { listHosts: 0, getSummary: 0, getDiagnostics: 0, getPopularQueries: 0 }, tariff_checked_at: null, tariff_source: null, ...structuredClone(v) })
    },
    YMBCredentialRegistry: {
      capabilityForService(service, settings) {
        const r = settings?.credentials?.[service] || {};
        if (service === 'webmaster') return { state: r.oauth_token && /^\d+$/.test(String(r.user_id || '')) ? 'PRESENT' : 'MISSING', has_oauth_token: Boolean(r.oauth_token), has_user_id: /^\d+$/.test(String(r.user_id || '')) };
        return { state: r.api_key && r.folder_id ? 'PRESENT' : 'MISSING', has_api_key: Boolean(r.api_key), has_folder_id: Boolean(r.folder_id) };
      }
    },
    SearchProtocol: {
      normalizeCommand: (c) => ({ ...c }), buildRequest: (_c, folder) => ({ url: `https://search.example/${folder}`, body: { q: 'x' } }),
      safeErrorPayload: (status) => ({ http_status: status, code: 'ERR', message: 'err' }), normalizeProviderResult: (parsed) => parsed,
      buildResultEnvelope: (x) => x, formatResultEnvelope: (x) => `SEARCH_RESULT_V1\n${JSON.stringify(x)}`
    },
    WordstatProtocol: {
      normalizeCommand: (c) => ({ ...c }), buildRequest: (_c, folder) => ({ method: 'POST', url: `https://wordstat.example/${folder}`, body: { x: 1 } }),
      safeErrorPayload: (status) => ({ http_status: status, code: 'ERR', message: 'err' }), buildResultEnvelope: (x) => x,
      formatResultEnvelope: (x) => `WORDSTAT_RESULT_V1\n${JSON.stringify(x)}`
    },
    getSettings: async () => ({ apiKey: String(storage.state.wsmb_api_key || ''), folderId: String(storage.state.wsmb_folder_id || ''), autoSend: true, debugMode: false }),
    protocolForService: (service) => service === 'search' ? ctx.SearchProtocol : service === 'wordstat' ? ctx.WordstatProtocol : null,
    getPolicyForService: async (service) => ({ service }),
    executeServiceCommand: async () => { throw new Error('legacy dispatcher should not be used'); },
    commonPublicSettingsFields: async () => ({ credential_capabilities: {} }),
    defaultAutoStartTextForService: (service) => `legacy:${service}`,
    publicPolicy: (policy) => structuredClone(policy)
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  ctx.importScripts = (...items) => { for (const item of items) vm.runInContext(fs.readFileSync(path.resolve(src, item), 'utf8'), ctx, { filename: item }); };
  vm.runInContext(fs.readFileSync(path.join(src, 'webmaster_worker_runtime.js'), 'utf8'), ctx, { filename: 'webmaster_worker_runtime.js' });
  return { ctx, storage, listeners, requests };
}
