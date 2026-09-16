import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const source=fs.readFileSync(new URL('../../../../src/shared/search_async_policy.js',import.meta.url),'utf8');

test('deferred durable owner and paused-run mirror owner remain separate policy fields',()=>{
  assert.match(source,/runOwner\s*=\s*null/);
  assert.match(source,/run_owner:\s*mirrorOwner/);
  assert.match(source,/getAutoRun\(binding\.run_owner\s*\|\|\s*binding\.owner\)/);
  assert.match(source,/publishRunTotals\(\{\s*owner:\s*binding\.run_owner\s*\|\|\s*binding\.owner/);
  assert.doesNotMatch(source,/const legacy = runId \? await getAutoRun\(owner\)/);
});
