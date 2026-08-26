import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

const root = path.resolve(process.argv[2] || '');
if (!process.argv[2] || !fs.existsSync(root)) {
  throw new Error('Usage: node patch_accepted_phase3_additive_compat.mjs <accepted-phase3-root>');
}

const expectedBlobSha = Object.freeze({
  'extension/tests/candidate_readiness_recovery.test.mjs': '9e84861d10c3b3af65d83663a0d4052a88ff49dd',
  'extension/tests/credential_store_model.test.mjs': '2b7cdf4d7e30bb6d065c20b5c0e03a4b72eb287c',
  'extension/tests/permission_scope_recovery.test.mjs': 'a1458a26503fe1f55d931e8780cc4e543cb6849f',
  'extension/tests/phase1_core_regression_recovery.test.mjs': 'fe5a6a4b08c4999e165cf6127448e1eeff46431c',
  'extension/tests/phase3_worker_runtime.test.mjs': 'c138b85316d54311b6b8177f2e3a404b31698e8e',
  'extension/tests/helpers/phase3_runtime_harness.mjs': '9039a144ec830e563c4ae358d2f68c0880b908a8'
});

function gitBlobSha(buffer) {
  const header = Buffer.from(`blob ${buffer.length}\0`);
  return crypto.createHash('sha1').update(header).update(buffer).digest('hex');
}

function verifyAcceptedSource(relativePath) {
  const file = path.join(root, relativePath);
  const bytes = fs.readFileSync(file);
  const actual = gitBlobSha(bytes);
  const expected = expectedBlobSha[relativePath];
  if (actual !== expected) {
    throw new Error(`Accepted Phase-3 source drift for ${relativePath}: expected ${expected}, got ${actual}`);
  }
}

for (const relativePath of Object.keys(expectedBlobSha)) verifyAcceptedSource(relativePath);
console.log('PHASE4_ACCEPTED_PHASE3_COMPAT_SOURCE_IDENTITY_PASS');

function replaceExact(relativePath, from, to, expectedCount = 1) {
  const file = path.join(root, relativePath);
  const source = fs.readFileSync(file, 'utf8');
  const count = source.split(from).length - 1;
  if (count !== expectedCount) {
    throw new Error(`Patch anchor mismatch in ${relativePath}: expected ${expectedCount}, got ${count}`);
  }
  fs.writeFileSync(file, source.split(from).join(to), 'utf8');
}

replaceExact(
  'extension/tests/candidate_readiness_recovery.test.mjs',
  "    'shared/webmaster_protocol.js',\n    'shared/credential_runtime.js',\n    'shared/phase3_provider_runtime.js',\n    'shared/settings_backup_v3_runtime.js'",
  "    'shared/webmaster_protocol.js',\n    'shared/metrika_protocol.js',\n    'shared/credential_runtime.js',\n    'shared/phase3_provider_runtime.js',\n    'shared/phase4_provider_runtime.js',\n    'shared/settings_backup_v3_runtime.js'"
);
replaceExact(
  'extension/tests/candidate_readiness_recovery.test.mjs',
  "    'https://api.webmaster.yandex.net/*'\n  ]);",
  "    'https://api.webmaster.yandex.net/*',\n    'https://api-metrika.yandex.net/*'\n  ]);"
);

replaceExact(
  'extension/tests/credential_store_model.test.mjs',
  "  assert.equal(M.SETTINGS_SCHEMA_VERSION, 3);",
  "  assert.equal(M.SETTINGS_SCHEMA_VERSION, 4);"
);
replaceExact(
  'extension/tests/credential_store_model.test.mjs',
  "  assert.deepEqual([...M.SERVICES], ['wordstat', 'search', 'webmaster']);",
  "  assert.deepEqual([...M.SERVICES], ['wordstat', 'search', 'webmaster', 'metrika']);"
);
replaceExact(
  'extension/tests/credential_store_model.test.mjs',
  "  assert.throws(() => M.withServiceCredential(base, 'metrika', {}), (e) => e?.code === 'UNKNOWN_SERVICE');",
  "  assert.throws(() => M.withServiceCredential(base, 'future-service', {}), (e) => e?.code === 'UNKNOWN_SERVICE');"
);

replaceExact(
  'extension/tests/permission_scope_recovery.test.mjs',
  "    'https://api.webmaster.yandex.net/*'\n  ]);",
  "    'https://api.webmaster.yandex.net/*',\n    'https://api-metrika.yandex.net/*'\n  ]);"
);
replaceExact(
  'extension/tests/permission_scope_recovery.test.mjs',
  "  assert.deepEqual(Array.from(ctx.YMBServiceRegistry.DEFINITIONS, x=>x.service),['wordstat','search','webmaster']);\n  for(const future of ['image','generative','async-search','search-async','metrika','direct']) assert.equal(ctx.YMBServiceRegistry.isKnownService(future),false);",
  "  assert.deepEqual(Array.from(ctx.YMBServiceRegistry.DEFINITIONS, x=>x.service),['wordstat','search','webmaster','metrika']);\n  assert.equal(ctx.YMBServiceRegistry.isKnownService('metrika'),true);\n  for(const future of ['image','generative','async-search','search-async','direct']) assert.equal(ctx.YMBServiceRegistry.isKnownService(future),false);"
);

replaceExact(
  'extension/tests/phase1_core_regression_recovery.test.mjs',
  "    { service: 'webmaster', prefix: 'WEBMASTER_API_V1' }\n  ]);\n  assert.equal(registry.isKnownService('wordstat'), true);\n  assert.equal(registry.isKnownService('search'), true);\n  assert.equal(registry.isKnownService('webmaster'), true);",
  "    { service: 'webmaster', prefix: 'WEBMASTER_API_V1' },\n    { service: 'metrika', prefix: 'METRIKA_API_V1' }\n  ]);\n  assert.equal(registry.isKnownService('wordstat'), true);\n  assert.equal(registry.isKnownService('search'), true);\n  assert.equal(registry.isKnownService('webmaster'), true);\n  assert.equal(registry.isKnownService('metrika'), true);"
);

replaceExact(
  'extension/tests/helpers/phase3_runtime_harness.mjs',
  "    YMBServiceRegistry: { SERVICES: { WORDSTAT: 'wordstat', SEARCH: 'search', WEBMASTER: 'webmaster' } },",
  "    YMBServiceRegistry: { SERVICES: { WORDSTAT: 'wordstat', SEARCH: 'search', WEBMASTER: 'webmaster', METRIKA: 'metrika' } },"
);
replaceExact(
  'extension/tests/helpers/phase3_runtime_harness.mjs',
  "      normalizeWebmasterPolicy: (v = {}) => ({ manual_enabled: true, autorun_enabled: false, allowed_methods: ['listHosts','getSummary','getDiagnostics','getPopularQueries'], max_requests_per_run: 50, max_cost_rub_per_run: 0, method_cost_rub: { listHosts: 0, getSummary: 0, getDiagnostics: 0, getPopularQueries: 0 }, tariff_checked_at: null, tariff_source: null, ...structuredClone(v) })",
  "      normalizeWebmasterPolicy: (v = {}) => ({ manual_enabled: true, autorun_enabled: false, allowed_methods: ['listHosts','getSummary','getDiagnostics','getPopularQueries'], max_requests_per_run: 50, max_cost_rub_per_run: 0, method_cost_rub: { listHosts: 0, getSummary: 0, getDiagnostics: 0, getPopularQueries: 0 }, tariff_checked_at: null, tariff_source: null, ...structuredClone(v) }),\n      normalizeMetrikaPolicy: (v = {}) => ({ manual_enabled: true, autorun_enabled: false, allowed_methods: ['listCounters','getCounter','getTrafficSummary','getTrafficByTime'], max_requests_per_run: 50, max_report_days: 366, max_cost_rub_per_run: 0, method_cost_rub: { listCounters: 0, getCounter: 0, getTrafficSummary: 0, getTrafficByTime: 0 }, tariff_checked_at: null, tariff_source: null, ...structuredClone(v) })"
);

replaceExact(
  'extension/tests/phase3_worker_runtime.test.mjs',
  "  assert.equal(storage.state.ymb_settings_schema_version, 3);",
  "  assert.equal(storage.state.ymb_settings_schema_version, 4);"
);
replaceExact(
  'extension/tests/phase3_worker_runtime.test.mjs',
  "  assert.equal(state.settings_schema_version, 3);",
  "  assert.equal(state.settings_schema_version, 4);"
);

const touched = Object.keys(expectedBlobSha).sort();
for (const relativePath of touched) {
  const current = fs.readFileSync(path.join(root, relativePath));
  if (gitBlobSha(current) === expectedBlobSha[relativePath]) {
    throw new Error(`Expected additive compatibility patch did not modify ${relativePath}`);
  }
}

console.log(`PHASE4_ACCEPTED_PHASE3_COMPAT_PATCHED_FILES=${touched.length}`);
console.log('PHASE4_ACCEPTED_PHASE3_ADDITIVE_COMPAT_PATCH_PASS');
