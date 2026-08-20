import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../src');
const c = { console };
c.globalThis = c;
vm.createContext(c);
vm.runInContext(fs.readFileSync(path.join(root, 'shared/service_registry.js'), 'utf8'), c);

test('Search registry maps SEARCH_API_V1 to search', () => {
  assert.equal(c.YMBServiceRegistry.detect('SEARCH_API_V1\n{"queryText":"x"}').service, 'search');
  assert.equal(c.YMBServiceRegistry.definitionForService('search').prefix, 'SEARCH_API_V1');
  assert.equal(c.YMBServiceRegistry.isKnownService('search'), true);
  assert.equal(c.YMBServiceRegistry.detect('DIRECT_API_V1\n{}'), null);
});
