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
const SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly';
const STABLE_ID = 'pckmmaodnfeajgigadfaejfjppdbgmpo';

function harness({ configured = true, token = 'oauth-ui-secret', fetchImpl = null } = {}) {
  const storage = {};
  const identityCalls = [];
  const removedTokens = [];
  const connectListeners = [];
  const providerCalls = [];
  const manifest = configured ? {
    manifest_version: 3,
    permissions: ['storage', 'identity'],
    oauth2: {
      client_id: 'phase9-test-client.apps.googleusercontent.com',
      scopes: [SCOPE]
    }
  } : {
    manifest_version: 3,
    permissions: ['storage']
  };
  const identity = configured ? {
    async getAuthToken(options = {}) {
      identityCalls.push(plain(options));
      if (!token) throw new Error('OAuth2 not granted or revoked.');
      return { token, grantedScopes: [SCOPE] };
    },
    async removeCachedAuthToken(details = {}) {
      removedTokens.push(plain(details));
    }
  } : undefined;
  const ctx = {
    console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math, URL, URLSearchParams,
    globalThis: null,
    chrome: {
      runtime: {
        id: STABLE_ID,
        getManifest: () => plain(manifest),
        onConnect: { addListener(fn) { connectListeners.push(fn); } }
      },
      storage: {
        local: {
          async get(keys) {
            if (keys == null) return plain(storage);
            if (typeof keys === 'string') return { [keys]: storage[keys] };
            const list = Array.isArray(keys) ? keys : Object.keys(keys || {});
            return Object.fromEntries(list.map((key) => [key, storage[key]]));
          },
          async set(values) { Object.assign(storage, plain(values)); }
        }
      },
      identity
    },
    fetch: fetchImpl || (async (url, options = {}) => {
      providerCalls.push({ url: String(url), options: plain(options) });
      return {
        ok: true,
        status: 200,
        async text() { return JSON.stringify({ siteEntry: [{ siteUrl: 'sc-domain:example.com', permissionLevel: 'siteOwner' }] }); }
      };
    })
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of [
    'shared/service_registry.js',
    'shared/policy_model.js',
    'shared/google_search_console_protocol.js',
    'shared/google_search_console_runtime.js'
  ]) vm.runInContext(read(file), ctx, { filename: file });

  ctx.protocolForService = () => null;
  ctx.getPolicyForService = async () => ({ prior: true });
  ctx.policyDecisionForService = () => ({ allow: false, reason: 'PRIOR' });
  ctx.executeServiceCommand = async () => ({ prior: true });
  ctx.defaultAutoStartTextForService = (service) => `prior:${service}`;
  ctx.commonPublicSettingsFields = async () => ({ prior_public_state: true });

  vm.runInContext(read('google_search_console_worker_runtime.js'), ctx, { filename: 'google_search_console_worker_runtime.js' });
  return { ctx, storage, identityCalls, removedTokens, connectListeners, providerCalls, manifest };
}

test('P9-06B pre-client: production manifest remains stable-ID only and cannot trigger Google auth/provider traffic yet', async () => {
  const manifest = JSON.parse(read('manifest.json'));
  assert.equal(typeof manifest.key, 'string');
  assert.equal(manifest.permissions.includes('identity'), false);
  assert.equal(manifest.host_permissions.some((item) => String(item).includes('googleapis.com')), false);
  assert.equal(Object.hasOwn(manifest, 'oauth2'), false);

  const { ctx, identityCalls, providerCalls } = harness({ configured: false });
  const status = plain(await ctx.YMBGoogleSearchConsoleWorkerRuntime.authStatus());
  assert.equal(status.configured, false);
  assert.equal(status.check_state, 'UNCONFIGURED');
  assert.equal(status.request_executed, false);
  assert.equal(identityCalls.length, 0);
  assert.equal(providerCalls.length, 0);
  await assert.rejects(
    () => ctx.YMBGoogleSearchConsoleWorkerRuntime.connect(),
    (error) => error.code === 'GSC_AUTH_CONFIG_REQUIRED' && error.request_executed === false
  );
  assert.equal(providerCalls.length, 0);
});

test('P9-06B auth separation: status and provider execution are noninteractive while Connect alone is interactive', async () => {
  const { ctx, identityCalls, providerCalls } = harness();

  const status = plain(await ctx.YMBGoogleSearchConsoleWorkerRuntime.authStatus());
  assert.equal(status.check_state, 'PRESENT');
  assert.deepEqual(identityCalls, [{ interactive: false }]);
  assert.equal(providerCalls.length, 0);

  const connected = plain(await ctx.YMBGoogleSearchConsoleWorkerRuntime.connect());
  assert.equal(connected.check_state, 'PRESENT');
  assert.deepEqual(identityCalls[1], { interactive: true });
  assert.equal(providerCalls.length, 0);

  const command = await ctx.executeServiceCommand('google_search_console', { method: 'listSites' }, { channel: 'manual' });
  assert.equal(command.ok, true);
  assert.deepEqual(identityCalls[2], { interactive: false });
  assert.equal(providerCalls.length, 1);
  assert.equal(command.report_text.includes('oauth-ui-secret'), false);
});

test('P9-06B Check access performs exactly one noninteractive readonly listSites request and returns no token', async () => {
  const { ctx, identityCalls, providerCalls, storage } = harness();
  const result = plain(await ctx.YMBGoogleSearchConsoleWorkerRuntime.checkAccess());
  assert.equal(result.ok, true);
  assert.equal(result.check_state, 'PRESENT');
  assert.equal(result.request_executed, true);
  assert.equal(result.site_count, 1);
  assert.deepEqual(identityCalls, [{ interactive: false }]);
  assert.equal(providerCalls.length, 1);
  assert.equal(providerCalls[0].url, 'https://www.googleapis.com/webmasters/v3/sites');
  assert.equal(providerCalls[0].options.method, 'GET');
  assert.equal(providerCalls[0].options.headers.Authorization, 'Bearer oauth-ui-secret');
  assert.equal(JSON.stringify(result).includes('oauth-ui-secret'), false);
  assert.equal(JSON.stringify(storage).includes('oauth-ui-secret'), false);
});

test('P9-06B Disconnect removes only the cached token noninteractively and performs no provider request', async () => {
  const { ctx, identityCalls, removedTokens, providerCalls, storage } = harness();
  const result = plain(await ctx.YMBGoogleSearchConsoleWorkerRuntime.disconnect());
  assert.equal(result.ok, true);
  assert.equal(result.check_state, 'AUTH_REQUIRED');
  assert.equal(result.request_executed, false);
  assert.deepEqual(identityCalls, [{ interactive: false }]);
  assert.deepEqual(removedTokens, [{ token: 'oauth-ui-secret' }]);
  assert.equal(providerCalls.length, 0);
  assert.equal(JSON.stringify(storage).includes('oauth-ui-secret'), false);
});

test('P9-06B worker exposes a dedicated auth port and extends public state without changing prior fields', async () => {
  const { ctx, connectListeners } = harness();
  assert.equal(ctx.YMBGoogleSearchConsoleWorkerRuntime.PORT_NAME, 'YMB_GSC_AUTH_V1');
  assert.equal(connectListeners.length, 1);
  const publicState = plain(await ctx.commonPublicSettingsFields());
  assert.equal(publicState.prior_public_state, true);
  assert.equal(publicState.google_search_console_policy.autorun_enabled, false);
  assert.equal(publicState.google_search_console_auth_status.check_state, 'PRESENT');
  assert.equal(publicState.google_search_console_auth_status.configured, true);
});

test('P9-06B popup contract exposes GSC as sixth service with no token/password input and locks Autorun', () => {
  const html = read('popup.html');
  const js = read('popup.js');
  assert.match(html, /<option value="google_search_console">Google Search Console<\/option>/);
  const card = html.match(/<details id="google_search_consoleCredentials"[\s\S]*?<\/details>/)?.[0] || '';
  assert.ok(card);
  assert.doesNotMatch(card, /type="password"/i);
  assert.doesNotMatch(card, /oauth[_ -]?token|access[_ -]?token/i);
  assert.match(card, /id="connectGoogleSearchConsole"/);
  assert.match(card, /id="checkGoogleSearchConsoleAccess"/);
  assert.match(card, /id="disconnectGoogleSearchConsole"/);
  assert.match(html, /id="googleSearchConsoleManualEnabled"/);
  assert.match(html, /id="googleSearchConsoleMaxRequestsRun"/);

  assert.match(js, /google_search_console/);
  assert.match(js, /PERSISTENT_CREDENTIAL_SERVICES/);
  assert.match(js, /YMB_GSC_AUTH_V1/);
  assert.match(js, /googleSearchConsolePolicyFromForm/);
  assert.match(js, /connectGoogleSearchConsole/);
  assert.match(js, /checkGoogleSearchConsoleAccess/);
  assert.match(js, /disconnectGoogleSearchConsole/);
});
