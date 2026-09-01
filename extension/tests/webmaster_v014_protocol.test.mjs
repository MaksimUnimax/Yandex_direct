import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const hostId = 'https:openscript.ru:443';
const userId = '42';
const plain = (value) => JSON.parse(JSON.stringify(value));

function protocol() {
  const ctx = {
    console, Date, JSON, Math, Object, Array, Set, Map, Promise, Error, String, Number, Boolean, RegExp,
    encodeURIComponent, globalThis: null,
    YMBProduct: { VERSION: '0.1.4', BRIDGE_ID: 'yandex-marketing-bridge' }
  };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(src, 'shared/webmaster_protocol.js'), 'utf8'), ctx, { filename: 'webmaster_protocol.js' });
  return ctx.WebmasterProtocol;
}

const P = protocol();

test('WM14-P01 getHostInfo is an exact single-host GET and accepts only hostId', () => {
  assert.ok(P.METHODS.includes('getHostInfo'));
  const normalized = plain(P.normalizeCommand({ method: 'getHostInfo', hostId }));
  assert.deepEqual(normalized, { method: 'getHostInfo', hostId });
  const req = plain(P.buildRequest(normalized, userId));
  assert.deepEqual(req, {
    method: 'GET',
    url: 'https://api.webmaster.yandex.net/v4/user/42/hosts/https%3Aopenscript.ru%3A443'
  });
  assert.throws(() => P.normalizeCommand({ method: 'getHostInfo', hostId, mutation: true }), (error) => error.code === 'UNSUPPORTED_FIELD');
});

test('WM14-P02 getHostInfo exposes official host_data_status with normalized readiness', () => {
  for (const [hostDataStatus, ready] of [['NOT_LOADED', false], ['NOT_INDEXED', false], ['OK', true]]) {
    const result = plain(P.normalizeProviderResult({ method: 'getHostInfo', hostId }, {
      host_id: hostId,
      ascii_host_url: 'https://openscript.ru/',
      unicode_host_url: 'https://openscript.ru/',
      verified: true,
      host_data_status: hostDataStatus,
      host_display_name: 'OpenScript',
      internal: 'drop'
    }));
    assert.equal(result.host_id, hostId);
    assert.equal(result.verified, true);
    assert.equal(result.host_data_status, hostDataStatus);
    assert.equal(result.webmaster_data_ready, ready);
    assert.equal(result.host_display_name, 'OpenScript');
    assert.equal(Object.hasOwn(result, 'internal'), false);
  }
});

test('WM14-P03 missing host_data_status is fail-closed for readiness without inventing provider state', () => {
  const result = plain(P.normalizeProviderResult({ method: 'getHostInfo', hostId }, {
    host_id: hostId,
    ascii_host_url: 'https://openscript.ru/',
    unicode_host_url: 'https://openscript.ru/',
    verified: false
  }));
  assert.equal(result.host_data_status, null);
  assert.equal(result.webmaster_data_ready, false);
});

test('WM14-P04 getHostInfo keeps only stable main-mirror evidence', () => {
  const result = plain(P.normalizeProviderResult({ method: 'getHostInfo', hostId }, {
    host_id: hostId,
    ascii_host_url: 'https://openscript.ru/',
    unicode_host_url: 'https://openscript.ru/',
    verified: true,
    host_data_status: 'OK',
    main_mirror: {
      host_id: 'https:www.openscript.ru:443',
      ascii_host_url: 'https://www.openscript.ru/',
      unicode_host_url: 'https://www.openscript.ru/',
      verified: true,
      secret: 'drop'
    }
  }));
  assert.deepEqual(result.main_mirror, {
    host_id: 'https:www.openscript.ru:443',
    ascii_host_url: 'https://www.openscript.ru/',
    unicode_host_url: 'https://www.openscript.ru/',
    verified: true
  });
  assert.equal(result.webmaster_data_ready, true);
});
