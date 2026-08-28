import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');

function read(relative) { return fs.readFileSync(path.join(src, relative), 'utf8'); }

function load(files) {
  const ctx = { console, JSON, Object, Array, Set, String, Number, Boolean, RegExp, Date, Error, Math, URL, globalThis: null };
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  for (const file of files) vm.runInContext(read(file), ctx, { filename: file });
  return ctx;
}

test('Search batch transport stays inside search service while GSC remains the separate sixth service', () => {
  const ctx = load([
    'shared/service_registry.js',
    'shared/block_command_discovery.js',
    'shared/wordstat_batch_protocol.js',
    'shared/wordstat_batch_transport.js',
    'shared/search_protocol.js',
    'shared/search_batch_protocol.js',
    'shared/search_batch_transport.js'
  ]);
  assert.deepEqual(
    Array.from(ctx.YMBServiceRegistry.DEFINITIONS, (item) => item.service),
    ['wordstat', 'search', 'webmaster', 'metrika', 'direct', 'google_search_console']
  );
  const detected = ctx.YMBSearchBatchTransport.detect('SEARCH_BATCH_API_V1 {"action":"status","jobId":"j"}', ctx.YMBServiceRegistry);
  assert.equal(detected.service, 'search');
  assert.equal(detected.search_batch, true);
  assert.equal(detected.prefix, 'SEARCH_BATCH_API_V1');
  assert.equal(ctx.YMBServiceRegistry.definitionForService('google_search_console').prefix, 'GOOGLE_SEARCH_CONSOLE_API_V1');
});

test('Search batch discovery composes with ordinary registry discovery and Wordstat batch without duplication', () => {
  const ctx = load([
    'shared/service_registry.js',
    'shared/block_command_discovery.js',
    'shared/wordstat_batch_protocol.js',
    'shared/wordstat_batch_transport.js',
    'shared/search_protocol.js',
    'shared/search_batch_protocol.js',
    'shared/search_batch_transport.js'
  ]);
  const text = [
    'SEARCH_API_V1 {"method":"search","queryText":"alpha"}',
    'SEARCH_BATCH_API_V1 {"action":"status","jobId":"j"}',
    'WORDSTAT_BATCH_API_V1 {"action":"status","jobId":"w"}'
  ].join('\n');
  const found = ctx.YMBSearchBatchTransport.discover(text, ctx.YMBBlockCommandDiscovery, ctx.YMBServiceRegistry);
  assert.equal(found.length, 3);
  assert.deepEqual(Array.from(found, (item) => item.prefix), ['SEARCH_API_V1', 'SEARCH_BATCH_API_V1', 'WORDSTAT_BATCH_API_V1']);
  assert.equal(found[1].service, 'search');
  assert.equal(found[1].search_batch, true);
  assert.equal(found[2].service, 'wordstat');
  assert.equal(found[2].batch, true);
});

test('Search content bridge extends only Search command recognition and preserves ordinary Search protocol API', () => {
  const ctx = load([
    'shared/service_registry.js',
    'shared/block_command_discovery.js',
    'shared/search_protocol.js',
    'shared/search_batch_protocol.js',
    'shared/search_batch_transport.js',
    'shared/search_batch_content_bridge.js'
  ]);
  assert.equal(ctx.SearchProtocol.isCommandText('SEARCH_API_V1 {"method":"search","queryText":"alpha"}'), true);
  assert.equal(ctx.SearchProtocol.isCommandText('SEARCH_BATCH_API_V1 {"action":"status","jobId":"j"}'), true);
  assert.equal(ctx.SearchProtocol.PREFIX, 'SEARCH_API_V1');
  assert.equal(ctx.SearchBatchProtocol.PREFIX, 'SEARCH_BATCH_API_V1');
  assert.equal(ctx.YMBServiceRegistry.DEFINITIONS.length, 6);
  assert.equal(ctx.YMBServiceRegistry.definitionForService('google_search_console').prefix, 'GOOGLE_SEARCH_CONSOLE_API_V1');
});

test('manifest loads Search batch content modules after SearchProtocol and before content_script', () => {
  const manifest = JSON.parse(read('manifest.json'));
  const scripts = manifest.content_scripts[0].js;
  const search = scripts.indexOf('shared/search_protocol.js');
  const protocol = scripts.indexOf('shared/search_batch_protocol.js');
  const transport = scripts.indexOf('shared/search_batch_transport.js');
  const bridge = scripts.indexOf('shared/search_batch_content_bridge.js');
  const content = scripts.indexOf('content_script.js');
  assert.ok(search >= 0 && search < protocol);
  assert.ok(protocol < transport && transport < bridge && bridge < content);
});

test('worker bootstrap loads Search batch only after final provider runtime overlay', () => {
  const source = read('phase3_service_worker_bootstrap.js');
  const provider = source.indexOf('webmaster_worker_runtime.js');
  const protocol = source.indexOf('shared/search_batch_protocol.js');
  const projection = source.indexOf('shared/search_batch_projection.js');
  const runtime = source.indexOf('shared/search_batch_runtime.js');
  const transport = source.indexOf('shared/search_batch_transport.js');
  const worker = source.indexOf('search_batch_worker_transport.js');
  assert.ok(provider >= 0);
  assert.ok(provider < protocol && protocol < projection && projection < runtime && runtime < transport && transport < worker);
});

test('Search batch worker adapter uses existing Search provider executor and preserves fail-closed routing/no-retry invariants', () => {
  const source = read('search_batch_worker_transport.js');
  assert.match(source, /YMBServiceRegistry\.SERVICES\.SEARCH/);
  assert.match(source, /executeServiceCommand\(SEARCH, command/);
  assert.match(source, /getSearchPolicy\(\)/);
  assert.match(source, /method:\s*"search"/);
  assert.match(source, /serviceContext\.active_service !== SEARCH/);
  assert.match(source, /currentRun\.active_service !== SEARCH/);
  assert.match(source, /search_batch_requesting/);
  assert.match(source, /REQUEST_OUTCOME_UNKNOWN_NO_RETRY/);
  assert.match(source, /automatic_retry:\s*false/);
  assert.doesNotMatch(source, /\bfetch\s*\(/);
  assert.doesNotMatch(source, /genSearch/);
});
