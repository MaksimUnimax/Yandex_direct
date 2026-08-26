import fs from 'node:fs';
import crypto from 'node:crypto';

const file = process.argv[2];
if (!file || !fs.existsSync(file)) throw new Error('Usage: node patch_m14_metrika_from_w14.mjs <proven-w14-harness>');

function gitBlobSha(buffer) {
  const header = Buffer.from(`blob ${buffer.length}\0`);
  return crypto.createHash('sha1').update(header).update(buffer).digest('hex');
}

const expectedBlob = 'ea8f3ab6bae9a0e14423133b4654c31f86a3d51a';
const original = fs.readFileSync(file);
const actual = gitBlobSha(original);
if (actual !== expectedBlob) throw new Error(`M14 proven W14 harness drift: expected ${expectedBlob}, got ${actual}`);
let source = original.toString('utf8');

function replaceExact(from, to, label, expectedCount = 1) {
  const count = source.split(from).length - 1;
  if (count !== expectedCount) throw new Error(`${label}: expected ${expectedCount} anchors, got ${count}`);
  source = source.split(from).join(to);
}

source = source.replaceAll('Webmaster', 'Metrika').replaceAll('WEBMASTER', 'METRIKA').replaceAll('webmaster', 'metrika');
source = source.replaceAll('W14_METRIKA', 'M14_METRIKA');

replaceExact('api.metrika.yandex.net', 'api-metrika.yandex.net', 'Metrika provider hostname', 4);
replaceExact('{"method":"listHosts"}', '{"method":"listCounters","page":1,"perPage":1}', 'Metrika fixture command');
replaceExact("req.url === '/v4/user/42/hosts'", "req.url === '/management/v1/counters?offset=1&per_page=1'", 'Metrika provider route');
replaceExact('JSON.stringify({ hosts: [] })', 'JSON.stringify({ rows: 0, counters: [] })', 'Metrika provider response');
replaceExact("metrika: { oauth_token: 'qa-fake-oauth', user_id: '42', verified_at: '2026-08-26T00:00:00.000Z', check_state: 'PRESENT' }", "metrika: { oauth_token: 'qa-fake-oauth', checked_at: '2026-08-26T00:00:00.000Z', check_state: 'PRESENT' }", 'Metrika credential record');
replaceExact("providerHits[0].url === '/v4/user/42/hosts'", "providerHits[0].url === '/management/v1/counters?offset=1&per_page=1'", 'Metrika provider assertion');

fs.writeFileSync(file, source, 'utf8');
const patchedBlob = gitBlobSha(fs.readFileSync(file));
if (patchedBlob === expectedBlob) throw new Error('M14 Metrika patch produced no change');
console.log(`M14_PROVEN_W14_SOURCE_BLOB=${expectedBlob}`);
console.log(`M14_METRIKA_PATCHED_BLOB=${patchedBlob}`);
console.log('M14_METRIKA_PROVEN_ROUTE_ADAPTATION_PASS');
console.log('M14_METRIKA_MARKER_NAMESPACE_PASS');
