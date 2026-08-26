import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const source = fs.readFileSync(path.join(here, '../src/shared/webmaster_protocol.js'), 'utf8');
const ctx = { console, URL, encodeURIComponent, Date, globalThis: null };
ctx.globalThis = ctx;
ctx.YMBProduct = { VERSION: '0.1.1', BRIDGE_ID: 'yandex-marketing-bridge' };
vm.createContext(ctx);
vm.runInContext(source, ctx, { filename: 'webmaster_protocol.js' });
const P = ctx.WebmasterProtocol;
const plain = (value) => JSON.parse(JSON.stringify(value));

function throwsCode(fn, code) {
  assert.throws(fn, (error) => error?.code === code, `expected ${code}`);
}

test('exports Phase-3 identities and read-only methods', () => {
  assert.equal(P.PREFIX, 'WEBMASTER_API_V1');
  assert.equal(P.RESULT_PREFIX, 'WEBMASTER_RESULT_V1');
  assert.equal(P.BASE_URL, 'https://api.webmaster.yandex.net/v4');
  assert.deepEqual([...P.METHODS], ['listHosts', 'getSummary', 'getDiagnostics', 'getPopularQueries']);
});

test('listHosts command is strict and credential-free', () => {
  assert.deepEqual({ ...P.normalizeCommand({ method: 'listHosts' }) }, { method: 'listHosts' });
  throwsCode(() => P.normalizeCommand({ method: 'listHosts', oauth_token: 'secret' }), 'UNSUPPORTED_FIELD');
  throwsCode(() => P.normalizeCommand({ method: 'listHosts', userId: 1 }), 'UNSUPPORTED_FIELD');
});

test('host methods require hostId and reject unknown fields', () => {
  assert.deepEqual({ ...P.normalizeCommand({ method: 'getSummary', hostId: 'https:example.com:443' }) }, { method: 'getSummary', hostId: 'https:example.com:443' });
  assert.deepEqual({ ...P.normalizeCommand({ method: 'getDiagnostics', hostId: 'https:example.com:443' }) }, { method: 'getDiagnostics', hostId: 'https:example.com:443' });
  throwsCode(() => P.normalizeCommand({ method: 'getSummary' }), 'MISSING_FIELD');
  throwsCode(() => P.normalizeCommand({ method: 'getDiagnostics', hostId: '', extra: 1 }), 'UNSUPPORTED_FIELD');
});

test('popular query defaults and enum/range/date validation are strict', () => {
  const n = P.normalizeCommand({ method: 'getPopularQueries', hostId: 'https:example.com:443', orderBy: 'TOTAL_SHOWS' });
  assert.equal(n.deviceTypeIndicator, 'ALL');
  assert.equal(n.offset, 0);
  assert.equal(n.limit, 500);
  throwsCode(() => P.normalizeCommand({ method: 'getPopularQueries', hostId: 'h', orderBy: 'BAD' }), 'INVALID_ENUM');
  throwsCode(() => P.normalizeCommand({ method: 'getPopularQueries', hostId: 'h', orderBy: 'TOTAL_SHOWS', queryIndicator: 'BAD' }), 'INVALID_ENUM');
  throwsCode(() => P.normalizeCommand({ method: 'getPopularQueries', hostId: 'h', orderBy: 'TOTAL_SHOWS', deviceTypeIndicator: 'PHONE' }), 'INVALID_ENUM');
  throwsCode(() => P.normalizeCommand({ method: 'getPopularQueries', hostId: 'h', orderBy: 'TOTAL_SHOWS', offset: -1 }), 'INVALID_FIELD');
  throwsCode(() => P.normalizeCommand({ method: 'getPopularQueries', hostId: 'h', orderBy: 'TOTAL_SHOWS', limit: 0 }), 'INVALID_FIELD');
  throwsCode(() => P.normalizeCommand({ method: 'getPopularQueries', hostId: 'h', orderBy: 'TOTAL_SHOWS', limit: 501 }), 'INVALID_FIELD');
  throwsCode(() => P.normalizeCommand({ method: 'getPopularQueries', hostId: 'h', orderBy: 'TOTAL_SHOWS', dateFrom: 'not-a-date' }), 'INVALID_DATE');
  throwsCode(() => P.normalizeCommand({ method: 'getPopularQueries', hostId: 'h', orderBy: 'TOTAL_SHOWS', dateFrom: '2026-08-10', dateTo: '2026-08-01' }), 'INVALID_DATE_RANGE');
});

test('parseCommand handles exact prefix and malformed JSON locally', () => {
  const parsed = P.parseCommand('WEBMASTER_API_V1\n{"method":"listHosts"}');
  assert.equal(parsed.method, 'listHosts');
  throwsCode(() => P.parseCommand('SEARCH_API_V1\n{}'), 'NOT_WEBMASTER_COMMAND');
  throwsCode(() => P.parseCommand('WEBMASTER_API_V1'), 'MISSING_JSON');
  throwsCode(() => P.parseCommand('WEBMASTER_API_V1\n{'), 'INVALID_JSON');
});

test('buildRequest uses derived user id and safely encodes host/query values', () => {
  assert.equal(P.buildRequest({ method: 'listHosts' }, 123).url, 'https://api.webmaster.yandex.net/v4/user/123/hosts');
  assert.equal(P.buildRequest({ method: 'getSummary', hostId: 'https:пример.рф:443/a b' }, '123').url,
    'https://api.webmaster.yandex.net/v4/user/123/hosts/https%3A%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80.%D1%80%D1%84%3A443%2Fa%20b/summary');
  const popular = P.buildRequest({
    method: 'getPopularQueries', hostId: 'https:example.com:443', orderBy: 'TOTAL_CLICKS',
    queryIndicator: 'AVG_SHOW_POSITION', deviceTypeIndicator: 'MOBILE', dateFrom: '2026-08-01', dateTo: '2026-08-07', offset: 5, limit: 100
  }, '42');
  assert.equal(popular.method, 'GET');
  assert.match(popular.url, /order_by=TOTAL_CLICKS/);
  assert.match(popular.url, /query_indicator=AVG_SHOW_POSITION/);
  assert.match(popular.url, /device_type_indicator=MOBILE/);
  assert.match(popular.url, /date_from=2026-08-01/);
  assert.match(popular.url, /date_to=2026-08-07/);
  assert.match(popular.url, /offset=5/);
  assert.match(popular.url, /limit=100/);
  throwsCode(() => P.buildRequest({ method: 'listHosts' }, ''), 'WEBMASTER_USER_ID_MISSING');
});

test('normalizes listHosts without leaking unselected fields', () => {
  const result = P.normalizeProviderResult({ method: 'listHosts' }, { hosts: [{
    host_id: 'https:example.com:443', ascii_host_url: 'https://example.com/', unicode_host_url: 'https://example.com/', verified: true,
    main_mirror: { host_id: 'https:www.example.com:443', ascii_host_url: 'https://www.example.com/', unicode_host_url: 'https://www.example.com/', verified: true },
    secret: 'drop-me'
  }] });
  assert.equal(result.hosts.length, 1);
  assert.equal(result.hosts[0].verified, true);
  assert.equal(result.hosts[0].secret, undefined);
  assert.equal(result.hosts[0].main_mirror.host_id, 'https:www.example.com:443');
});

test('normalizes summary, diagnostics and popular queries', () => {
  assert.deepEqual(plain(P.normalizeProviderResult({ method: 'getSummary', hostId: 'h' }, {
    sqi: 77, excluded_pages_count: 2, searchable_pages_count: 30, site_problems: { FATAL: 1 }, other: 'drop'
  })), { sqi: 77, excluded_pages_count: 2, searchable_pages_count: 30, site_problems: { FATAL: 1 } });

  const diagnostics = P.normalizeProviderResult({ method: 'getDiagnostics', hostId: 'h' }, { problems: {
    ROBOTS_TXT: { severity: 'FATAL', state: 'PRESENT', last_state_update: '2026-08-01T00:00:00Z', detail: 'drop' }
  }});
  assert.deepEqual(plain(diagnostics.problems.ROBOTS_TXT), { severity: 'FATAL', state: 'PRESENT', last_state_update: '2026-08-01T00:00:00Z' });

  const popular = P.normalizeProviderResult({ method: 'getPopularQueries', hostId: 'h', orderBy: 'TOTAL_SHOWS' }, {
    queries: [{ query_id: '1', query_text: 'ноутбук', indicators: { TOTAL_SHOWS: 10 } }], date_from: '2026-08-01', date_to: '2026-08-07', count: 1
  });
  assert.equal(popular.queries[0].query_text, 'ноутбук');
  assert.equal(popular.count, 1);
});

test('safe errors, skipped reports and result envelope preserve execution truth', () => {
  const err = P.safeErrorPayload(429, '', { error_code: 'QUOTA_EXCEEDED', error_message: 'quota' });
  assert.deepEqual(plain(err), { http_status: 429, code: 'QUOTA_EXCEEDED', message: 'quota' });
  const skipped = P.buildSkippedEnvelope({ requestId: 'skip-1', command: { method: 'listHosts' }, reason: 'NO_CREDENTIALS' });
  assert.equal(skipped.service, 'webmaster');
  assert.equal(skipped.request_executed, false);
  assert.equal(skipped.automatic_retry, false);
  assert.match(P.formatResultEnvelope(skipped), /^WEBMASTER_RESULT_V1\n/);
  const sent = P.buildResultEnvelope({ requestId: 'r1', command: { method: 'listHosts' }, httpStatus: 200, elapsedMs: 12, result: { hosts: [] }, metadata: { request_executed: true, automatic_retry: false } });
  assert.equal(sent.request_executed, true);
  assert.equal(sent.automatic_retry, false);
});

test('unsupported write-like Webmaster methods are locked', () => {
  for (const method of ['addHost', 'deleteHost', 'verifyHost', 'submitRecrawl', 'addSitemap', 'deleteSitemap']) {
    throwsCode(() => P.normalizeCommand({ method }), 'UNSUPPORTED_METHOD');
  }
});
