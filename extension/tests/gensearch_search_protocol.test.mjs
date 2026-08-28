import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');

function context() {
  const ctx = { console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math, globalThis: null };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  return ctx;
}

function loadSearchProtocol({ xmlNormalizer } = {}) {
  const ctx = context();
  if (xmlNormalizer) ctx.YMBSearchXml = xmlNormalizer;
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/search_protocol.js'), 'utf8'), ctx, { filename: 'search_protocol.js' });
  return ctx.SearchProtocol;
}

function loadPolicyModel() {
  const ctx = context();
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/policy_model.js'), 'utf8'), ctx, { filename: 'policy_model.js' });
  return ctx.YMBPolicyModel;
}

function loadServiceRegistry() {
  const ctx = context();
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/service_registry.js'), 'utf8'), ctx, { filename: 'service_registry.js' });
  return ctx.YMBServiceRegistry;
}

test('ordinary SEARCH_API_V1 search request remains on /v2/web/search with existing defaults', () => {
  const protocol = loadSearchProtocol();
  const command = protocol.parseCommand('SEARCH_API_V1 {"method":"search","queryText":"печать велеса"}');
  const request = protocol.buildRequest(command, 'folder-1');
  assert.equal(command.method, 'search');
  assert.equal(command.searchType, 'SEARCH_TYPE_RU');
  assert.equal(command.region, '225');
  assert.equal(request.url, 'https://searchapi.api.cloud.yandex.net/v2/web/search');
  assert.equal(request.body.query.queryText, 'печать велеса');
  assert.equal(request.body.responseFormat, 'FORMAT_XML');
  assert.equal(Object.hasOwn(request.body, 'messages'), false);
});

test('genSearch is a bounded method on the existing SEARCH_API_V1 protocol', () => {
  const protocol = loadSearchProtocol();
  const command = protocol.parseCommand('SEARCH_API_V1 {"method":"genSearch","queryText":"печать велеса","confirmBillable":true}');
  assert.equal(command.method, 'genSearch');
  assert.equal(command.queryText, 'печать велеса');
  assert.equal(command.confirmBillable, true);
  assert.equal(Object.hasOwn(command, 'searchType'), false);
  assert.equal(Object.hasOwn(command, 'region'), false);
});

test('genSearch fails closed without explicit per-command billable confirmation', () => {
  const protocol = loadSearchProtocol();
  assert.throws(
    () => protocol.normalizeCommand({ method: 'genSearch', queryText: 'печать велеса' }),
    (error) => error.code === 'GEN_SEARCH_CONFIRM_REQUIRED'
  );
  assert.throws(
    () => protocol.normalizeCommand({ method: 'genSearch', queryText: 'печать велеса', confirmBillable: 'true' }),
    (error) => error.code === 'GEN_SEARCH_CONFIRM_REQUIRED'
  );
});

test('genSearch rejects ordinary Search-only fields instead of inventing unsupported provider semantics', () => {
  const protocol = loadSearchProtocol();
  assert.throws(
    () => protocol.normalizeCommand({ method: 'genSearch', queryText: 'печать велеса', confirmBillable: true, searchType: 'SEARCH_TYPE_RU' }),
    (error) => error.code === 'UNSUPPORTED_FIELD'
  );
  assert.throws(
    () => protocol.normalizeCommand({ method: 'genSearch', queryText: 'печать велеса', confirmBillable: true, region: '225' }),
    (error) => error.code === 'UNSUPPORTED_FIELD'
  );
});

test('genSearch builds exactly one synchronous official provider request body without credentials', () => {
  const protocol = loadSearchProtocol();
  const request = protocol.buildRequest({ method: 'genSearch', queryText: 'печать велеса', confirmBillable: true }, 'folder-1');
  assert.equal(request.url, 'https://searchapi.api.cloud.yandex.net/v2/gen/search');
  assert.deepEqual(JSON.parse(JSON.stringify(request.body)), {
    messages: [{ content: 'печать велеса', role: 'ROLE_USER' }],
    folderId: 'folder-1',
    fixMisspell: true,
    getPartialResults: false
  });
  assert.equal(JSON.stringify(request.body).includes('api_key'), false);
  assert.equal(JSON.stringify(request.body).includes('Authorization'), false);
});

test('GenSearch response preserves answer, used-source truth and refined queries as GenSearch provenance', () => {
  const protocol = loadSearchProtocol();
  const result = protocol.normalizeProviderResult({
    message: { content: 'Значение символа', role: 'ROLE_ASSISTANT' },
    sources: [
      { url: 'https://example.test/a', title: 'A', used: true },
      { url: 'https://example.test/b', title: 'B', used: false }
    ],
    searchQueries: [{ text: 'печать велеса значение', reqId: 'req-1' }],
    fixedMisspellQuery: '',
    isAnswerRejected: false,
    isBulletAnswer: false,
    hints: ['hint'],
    problematicAnswer: null
  });
  assert.equal(result.mode, 'generative');
  assert.equal(result.message.content, 'Значение символа');
  assert.equal(result.sources[0].used, true);
  assert.equal(result.sources[1].used, false);
  assert.equal(result.searchQueries[0].text, 'печать велеса значение');
  assert.equal(Object.hasOwn(result, 'aliceFanout'), false);
  assert.equal(Object.hasOwn(result, 'ALICE_FANOUT_OBSERVED'), false);
});

test('ordinary Search rawData normalization remains delegated to the existing XML normalizer', () => {
  let observed = null;
  const protocol = loadSearchProtocol({
    xmlNormalizer: {
      normalizeBase64RawData(value) {
        observed = value;
        return { ordinary: true };
      }
    }
  });
  assert.deepEqual(protocol.normalizeProviderResult({ rawData: 'Zm9v' }), { ordinary: true });
  assert.equal(observed, 'Zm9v');
});

test('Search policy accounts for GenSearch cost while preserving stored method allowlists', () => {
  const policy = loadPolicyModel();
  const defaults = policy.normalizeSearchPolicy({});
  assert.deepEqual([...defaults.allowed_methods], ['search', 'genSearch']);
  assert.equal(defaults.method_cost_rub.search, 0.488);
  assert.equal(defaults.method_cost_rub.genSearch, 5.08);
  assert.equal(defaults.tariff_checked_at, '2026-08-28');

  const allowed = policy.searchDecision({
    policy: {},
    channel: 'manual',
    method: 'genSearch',
    credentialState: 'PRESENT',
    run: { requests_executed: 0, estimated_cost_rub: 0 }
  });
  assert.equal(allowed.allow, true);
  assert.equal(allowed.estimated_cost_rub, 5.08);

  const costBlocked = policy.searchDecision({
    policy: {},
    channel: 'manual',
    method: 'genSearch',
    credentialState: 'PRESENT',
    run: { requests_executed: 1, estimated_cost_rub: 5.08 }
  });
  assert.equal(costBlocked.allow, false);
  assert.equal(costBlocked.reason, 'COST_LIMIT');

  const explicitAllowlist = policy.searchDecision({
    policy: { allowed_methods: ['search'] },
    channel: 'manual',
    method: 'genSearch',
    credentialState: 'PRESENT',
    run: { requests_executed: 0, estimated_cost_rub: 0 }
  });
  assert.equal(explicitAllowlist.allow, false);
  assert.equal(explicitAllowlist.reason, 'OPERATION_DISABLED');
});

test('legacy stored Search policy migrates once without breaking a later explicit GenSearch disable', () => {
  const policy = loadPolicyModel();
  const legacyStored = {
    autorun_enabled: false,
    manual_enabled: true,
    allowed_methods: ['search'],
    max_requests_per_run: 100,
    max_cost_rub_per_run: 10,
    method_cost_rub: { search: 0.488 },
    tariff_checked_at: '2026-08-19',
    tariff_source: 'https://aistudio.yandex.ru/docs/ru/search-api/pricing.html'
  };
  const migrated = policy.normalizeSearchPolicy(legacyStored);
  assert.deepEqual([...migrated.allowed_methods], ['search', 'genSearch']);
  assert.equal(migrated.method_cost_rub.genSearch, 5.08);
  assert.equal(migrated.tariff_checked_at, '2026-08-19');

  const explicitlyDisabledAfterUpgrade = policy.normalizeSearchPolicy({
    ...JSON.parse(JSON.stringify(migrated)),
    allowed_methods: ['search'],
    tariff_checked_at: '2026-08-28'
  });
  assert.deepEqual([...explicitlyDisabledAfterUpgrade.allowed_methods], ['search']);
  assert.equal(explicitlyDisabledAfterUpgrade.method_cost_rub.genSearch, 5.08);

  const reread = policy.normalizeSearchPolicy(JSON.parse(JSON.stringify(explicitlyDisabledAfterUpgrade)));
  assert.deepEqual([...reread.allowed_methods], ['search']);
});

test('GenSearch does not create a sixth service', () => {
  const registry = loadServiceRegistry();
  assert.equal(registry.DEFINITIONS.length, 5);
  assert.deepEqual(JSON.parse(JSON.stringify(registry.DEFINITIONS.map((item) => item.service))), ['wordstat', 'search', 'webmaster', 'metrika', 'direct']);
  assert.equal(registry.definitionForService('search').prefix, 'SEARCH_API_V1');
});
