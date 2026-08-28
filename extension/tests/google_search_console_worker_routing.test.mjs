import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const read = (relative) => fs.readFileSync(path.join(src, relative), 'utf8');
const plain = (value) => JSON.parse(JSON.stringify(value));

function harness({ identity = null, fetchImpl = null } = {}) {
  const storage = {};
  const priorProtocol = Object.freeze({ name: 'prior-protocol' });
  const priorDecision = Object.freeze({ allow: false, reason: 'PRIOR_SENTINEL' });
  const priorResult = Object.freeze({ prior: true });
  const ctx = {
    console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math, URL, URLSearchParams,
    globalThis: null,
    chrome: {
      storage: {
        local: {
          async get(keys) {
            if (typeof keys === 'string') return { [keys]: storage[keys] };
            const list = Array.isArray(keys) ? keys : Object.keys(keys || {});
            return Object.fromEntries(list.map((key) => [key, storage[key]]));
          },
          async set(values) { Object.assign(storage, plain(values)); }
        }
      },
      identity: identity || undefined
    },
    fetch: fetchImpl || (async () => { throw new Error('UNEXPECTED_FETCH'); })
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of [
    'shared/service_registry.js',
    'shared/policy_model.js',
    'shared/google_search_console_protocol.js',
    'shared/google_search_console_runtime.js'
  ]) vm.runInContext(read(file), ctx, { filename: file });

  ctx.protocolForService = (service) => service === 'wordstat' ? priorProtocol : null;
  ctx.getPolicyForService = async () => Object.freeze({ prior: true });
  ctx.policyDecisionForService = () => priorDecision;
  ctx.executeServiceCommand = async () => priorResult;
  ctx.defaultAutoStartTextForService = (service) => `prior:${service}`;

  vm.runInContext(read('google_search_console_worker_runtime.js'), ctx, { filename: 'google_search_console_worker_runtime.js' });
  return { ctx, storage, priorProtocol, priorDecision, priorResult };
}

test('P9-05 bootstrap loads GSC protocol/runtime/worker after accepted Phase 5 overlay and before Search batch overlay', () => {
  const bootstrap = read('phase3_service_worker_bootstrap.js');
  const accepted = bootstrap.indexOf('webmaster_worker_runtime.js');
  const protocol = bootstrap.indexOf('shared/google_search_console_protocol.js');
  const runtime = bootstrap.indexOf('shared/google_search_console_runtime.js');
  const worker = bootstrap.indexOf('google_search_console_worker_runtime.js');
  const searchBatch = bootstrap.indexOf('shared/search_batch_protocol.js');
  assert.ok(accepted >= 0 && accepted < protocol);
  assert.ok(protocol < runtime && runtime < worker);
  assert.ok(worker < searchBatch);
});

test('P9-05 worker overlay adds GSC protocol routing without changing prior-service delegation', () => {
  const { ctx, priorProtocol } = harness();
  assert.equal(ctx.protocolForService('google_search_console'), ctx.GoogleSearchConsoleProtocol);
  assert.equal(ctx.protocolForService('wordstat'), priorProtocol);
  assert.equal(ctx.protocolForService('unknown'), null);
  assert.equal(ctx.YMBGoogleSearchConsoleWorkerRuntime.SERVICE, 'google_search_console');
});

test('P9-05 GSC policy is stored separately, defaults autorun off, and prior policy routing remains delegated', async () => {
  const { ctx, storage } = harness();
  const defaults = plain(await ctx.getPolicyForService('google_search_console'));
  assert.equal(defaults.manual_enabled, true);
  assert.equal(defaults.autorun_enabled, false);
  assert.deepEqual(defaults.allowed_methods, ['listSites', 'searchAnalytics']);
  assert.equal(defaults.max_cost_rub_per_run, 0);
  assert.equal(storage.ymb_google_search_console_policy, undefined);

  const saved = plain(await ctx.YMBGoogleSearchConsoleWorkerRuntime.savePolicy({
    manual_enabled: true,
    autorun_enabled: false,
    allowed_methods: ['listSites'],
    max_requests_per_run: 7
  }));
  assert.deepEqual(saved.allowed_methods, ['listSites']);
  assert.equal(saved.max_requests_per_run, 7);
  assert.deepEqual(storage.ymb_google_search_console_policy.allowed_methods, ['listSites']);
  assert.deepEqual(plain(await ctx.getPolicyForService('wordstat')), { prior: true });
});

test('P9-05 generic policy admission defers only GSC credential truth to identity runtime while prior services remain untouched', () => {
  const { ctx, priorDecision } = harness();
  const gscManual = plain(ctx.policyDecisionForService('google_search_console', {
    policy: {}, channel: 'manual', method: 'listSites', credentialState: 'NO_ACCESS', run: { requests_executed: 0 }
  }));
  assert.equal(gscManual.allow, true);
  const gscAutorun = plain(ctx.policyDecisionForService('google_search_console', {
    policy: {}, channel: 'autorun', method: 'listSites', credentialState: 'NO_ACCESS', run: { requests_executed: 0 }
  }));
  assert.equal(gscAutorun.allow, false);
  assert.equal(gscAutorun.reason, 'AUTORUN_DISABLED');
  assert.equal(ctx.policyDecisionForService('wordstat', {}), priorDecision);
});

test('P9-05 absent Chrome Identity fails GSC execution before fetch and never falls back to persistent credentials', async () => {
  let fetches = 0;
  const { ctx } = harness({ fetchImpl: async () => { fetches += 1; throw new Error('must not fetch'); } });
  await assert.rejects(
    () => ctx.executeServiceCommand('google_search_console', { method: 'listSites' }, { policy: { channel: 'manual' } }),
    (error) => error.code === 'GSC_AUTH_REQUIRED' && error.request_executed === false && error.automatic_retry === false
  );
  assert.equal(fetches, 0);
});

test('P9-05 worker execution uses Chrome Identity non-interactively and exactly one business fetch', async () => {
  const identityCalls = [];
  const fetchCalls = [];
  const identity = {
    async getAuthToken(options) {
      identityCalls.push(plain(options));
      return { token: 'worker-gsc-secret' };
    }
  };
  const { ctx } = harness({
    identity,
    fetchImpl: async (url, options) => {
      fetchCalls.push({ url, options: plain(options) });
      return { ok: true, status: 200, async text() { return JSON.stringify({ siteEntry: [{ siteUrl: 'sc-domain:example.com', permissionLevel: 'siteOwner' }] }); } };
    }
  });
  const result = await ctx.executeServiceCommand('google_search_console', { method: 'listSites' }, { policy: { channel: 'manual' } });
  assert.deepEqual(identityCalls, [{ interactive: false }]);
  assert.equal(fetchCalls.length, 1);
  assert.equal(fetchCalls[0].url, 'https://www.googleapis.com/webmasters/v3/sites');
  assert.equal(fetchCalls[0].options.headers.Authorization, 'Bearer worker-gsc-secret');
  assert.equal(result.ok, true);
  assert.equal(result.report_envelope.service, 'google_search_console');
  assert.equal(result.report_text.includes('worker-gsc-secret'), false);
});

test('P9-05 explicit test adapter seam is unavailable unless worker test mode is enabled', async () => {
  const { ctx } = harness();
  assert.throws(
    () => ctx.YMBGoogleSearchConsoleWorkerRuntime.configureForTest({ identity: { getAccessToken: async () => 'x' } }),
    (error) => error.code === 'GSC_TEST_MODE_REQUIRED'
  );
  ctx.__YMB_GSC_TEST__ = true;
  let calls = 0;
  ctx.YMBGoogleSearchConsoleWorkerRuntime.configureForTest({
    identity: { async getAccessToken(options) { assert.equal(options.interactive, false); return 'test-seam-token'; } },
    fetchImpl: async () => {
      calls += 1;
      return { ok: true, status: 200, async text() { return '{"siteEntry":[]}'; } };
    }
  });
  const result = await ctx.YMBGoogleSearchConsoleWorkerRuntime.executeGoogleSearchConsoleCommand({ method: 'listSites' }, { channel: 'manual' });
  assert.equal(result.ok, true);
  assert.equal(calls, 1);
  assert.equal(result.report_text.includes('test-seam-token'), false);
  ctx.YMBGoogleSearchConsoleWorkerRuntime.configureForTest(null);
});

test('P9-05 GSC default autorun text is service-specific while prior text remains delegated', () => {
  const { ctx } = harness();
  const gsc = ctx.defaultAutoStartTextForService('google_search_console');
  assert.match(gsc, /GOOGLE_SEARCH_CONSOLE_API_V1/);
  assert.match(gsc, /read-only/i);
  assert.equal(ctx.defaultAutoStartTextForService('wordstat'), 'prior:wordstat');
});

test('P9-05 persistent credential and backup models do not gain a Google token field', () => {
  const credentialStore = read('shared/credential_store_model.js');
  const backup = read('shared/settings_backup_v3_runtime.js');
  assert.doesNotMatch(credentialStore, /google_search_console/i);
  assert.doesNotMatch(credentialStore, /webmasters\.readonly/i);
  assert.doesNotMatch(backup, /google_search_console/i);
  assert.doesNotMatch(backup, /webmasters\.readonly/i);
});
