import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
function load(...files) {
  const ctx = { console, globalThis: null };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of files) vm.runInContext(fs.readFileSync(path.join(here, '../src/shared', file), 'utf8'), ctx, { filename: file });
  return ctx;
}
const plain = (value) => JSON.parse(JSON.stringify(value));

test('service registry exposes exactly one Webmaster prefix', () => {
  const { YMBServiceRegistry: R } = load('service_registry.js');
  assert.equal(R.SERVICES.WEBMASTER, 'webmaster');
  const defs = R.DEFINITIONS.filter((x) => x.service === 'webmaster');
  assert.equal(defs.length, 1);
  assert.equal(defs[0].prefix, 'WEBMASTER_API_V1');
  assert.equal(R.detect('WEBMASTER_API_V1\n{"method":"listHosts"}').service, 'webmaster');
  assert.equal(R.isKnownService('webmaster'), true);
});

test('Wordstat/Search dedicated credentials override legacy shared credentials', () => {
  const { YMBCredentialRegistry: C } = load('credential_registry.js');
  const legacy = { apiKey: 'legacy-key', folderId: 'legacy-folder' };
  assert.equal(C.wordstatCapability(legacy).state, 'PRESENT');
  assert.equal(C.searchCapability(legacy).state, 'PRESENT');

  const dedicated = {
    ...legacy,
    credentials: {
      wordstat: { api_key: 'wordstat-key', folder_id: 'wordstat-folder' },
      search: { api_key: '', folder_id: 'search-folder' }
    }
  };
  assert.equal(C.wordstatCapability(dedicated).state, 'PRESENT');
  assert.equal(C.searchCapability(dedicated).state, 'MISSING');
  assert.equal(C.searchCapability(dedicated).has_api_key, false);
});

test('Webmaster capability requires OAuth token plus derived numeric user_id', () => {
  const { YMBCredentialRegistry: C } = load('credential_registry.js');
  assert.equal(C.webmasterCapability({}).state, 'MISSING');
  assert.equal(C.webmasterCapability({ credentials: { webmaster: { oauth_token: 'token' } } }).state, 'MISSING');
  assert.equal(C.webmasterCapability({ credentials: { webmaster: { oauth_token: 'token', user_id: '123' } } }).state, 'PRESENT');
  assert.equal(C.webmasterCapability({ credentials: { webmaster: { oauth_token: 'token', user_id: 'abc' } } }).state, 'MISSING');
  assert.equal(C.webmasterCapability({ credentials: { webmaster: { oauth_token: 'token', user_id: '123', check_state: 'INVALID_OR_EXPIRED' } } }).state, 'INVALID_OR_EXPIRED');
  assert.equal(C.webmasterCapability({ credentials: { webmaster: { oauth_token: 'token', user_id: '123', check_state: 'NO_ACCESS' } } }).state, 'NO_ACCESS');
});

test('credential public capability never exposes secret material', () => {
  const { YMBCredentialRegistry: C } = load('credential_registry.js');
  const cap = plain(C.webmasterCapability({ credentials: { webmaster: { oauth_token: 'top-secret', user_id: '42' } } }));
  assert.deepEqual(cap, { state: 'PRESENT', has_oauth_token: true, has_user_id: true });
  assert.equal(JSON.stringify(cap).includes('top-secret'), false);
});

test('Webmaster default policy is read-only, zero-RUB, Manual on, Autorun off', () => {
  const { YMBPolicyModel: P } = load('policy_model.js');
  const policy = plain(P.normalizeWebmasterPolicy({}));
  assert.equal(policy.manual_enabled, true);
  assert.equal(policy.autorun_enabled, false);
  assert.equal(policy.max_requests_per_run, 50);
  assert.equal(policy.max_cost_rub_per_run, 0);
  assert.deepEqual(policy.allowed_methods, ['listHosts', 'getSummary', 'getDiagnostics', 'getPopularQueries']);
  assert.deepEqual(policy.method_cost_rub, { listHosts: 0, getSummary: 0, getDiagnostics: 0, getPopularQueries: 0 });
});

test('Webmaster policy rejects missing creds, Autorun default, disabled method and request ceiling locally', () => {
  const { YMBPolicyModel: P } = load('policy_model.js');
  assert.equal(P.webmasterDecision({ channel: 'manual', method: 'listHosts', credentialState: 'MISSING' }).reason, 'NO_CREDENTIALS');
  assert.equal(P.webmasterDecision({ channel: 'autorun', method: 'listHosts', credentialState: 'PRESENT' }).reason, 'AUTORUN_DISABLED');
  assert.equal(P.webmasterDecision({ channel: 'manual', method: 'writeSomething', credentialState: 'PRESENT' }).reason, 'OPERATION_DISABLED');
  assert.equal(P.webmasterDecision({ channel: 'manual', method: 'listHosts', credentialState: 'PRESENT', run: { requests_executed: 50 } }).reason, 'REQUEST_LIMIT');
  const allow = P.webmasterDecision({ channel: 'manual', method: 'listHosts', credentialState: 'PRESENT', run: { requests_executed: 49, estimated_cost_rub: 0 } });
  assert.equal(allow.allow, true);
  assert.equal(allow.estimated_cost_rub, 0);
});

test('policy routing recognizes Webmaster without changing unknown-service fail closed behavior', () => {
  const { YMBPolicyModel: P } = load('policy_model.js');
  assert.equal(P.decisionForService('webmaster', { channel: 'manual', method: 'getSummary', credentialState: 'PRESENT' }).allow, true);
  assert.equal(P.decisionForService('future-service', {}).reason, 'SERVICE_NOT_AVAILABLE');
});
