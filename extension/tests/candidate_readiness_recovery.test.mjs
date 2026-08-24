import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const testDir = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(testDir, '../src');
const manifest = JSON.parse(fs.readFileSync(path.join(src, 'manifest.json'), 'utf8'));
const pkg = JSON.parse(fs.readFileSync(path.join(src, 'package.json'), 'utf8'));
const popupHtml = fs.readFileSync(path.join(src, 'popup.html'), 'utf8');
const bootstrap = fs.readFileSync(path.join(src, 'service_worker_bootstrap.js'), 'utf8');
const worker = fs.readFileSync(path.join(src, 'service_worker.js'), 'utf8');
const product = fs.readFileSync(path.join(src, 'shared/product.js'), 'utf8');

function exists(relativePath) {
  return fs.existsSync(path.join(src, relativePath));
}

function quotedJsSources(html) {
  return [...html.matchAll(/<script\s+src="([^"]+)"\s*><\/script>/g)].map((m) => m[1]);
}

function importedScripts(source) {
  const call = source.match(/importScripts\(([\s\S]*?)\);/);
  if (!call) return [];
  return [...call[1].matchAll(/"([^"]+\.js)"/g)].map((m) => m[1]);
}

test('candidate manifest is MV3 and points only to files present in extension/src', () => {
  assert.equal(manifest.manifest_version, 3);
  assert.equal(manifest.background?.service_worker, 'service_worker_bootstrap.js');
  assert.equal(manifest.action?.default_popup, 'popup.html');
  assert.equal(exists(manifest.background.service_worker), true);
  assert.equal(exists(manifest.action.default_popup), true);
  for (const block of manifest.content_scripts || []) {
    for (const file of block.js || []) assert.equal(exists(file), true, `manifest content script is missing: ${file}`);
  }
});

test('candidate popup loads every referenced local script and transfer guard runs before popup runtime', () => {
  const scripts = quotedJsSources(popupHtml);
  assert.deepEqual(scripts, ['popup_transfer_guard.js', 'popup.js']);
  for (const file of scripts) assert.equal(exists(file), true, `popup script is missing: ${file}`);
});

test('candidate worker bootstrap loads production worker and every worker importScript exists', () => {
  assert.match(bootstrap, /importScripts\("service_worker\.js"\)/);
  const imports = importedScripts(worker);
  assert.ok(imports.length >= 10);
  for (const file of imports) assert.equal(exists(file), true, `worker importScript is missing: ${file}`);
});

test('candidate version stays aligned between manifest, package and product module', () => {
  assert.equal(manifest.version, '0.1.1');
  assert.equal(pkg.version, manifest.version);
  assert.match(product, /VERSION:\s*"0\.1\.1"/);
});

test('candidate host permissions stay limited to ChatGPT and official Yandex Search API', () => {
  assert.deepEqual(manifest.host_permissions, [
    'https://chatgpt.com/*',
    'https://chat.openai.com/*',
    'https://searchapi.api.cloud.yandex.net/*'
  ]);
  const serialized = JSON.stringify(manifest);
  assert.equal(serialized.includes('yandex.ru/*'), false);
  assert.equal(serialized.includes('https://yandex.ru/'), false);
});

test('candidate npm test command covers all top-level regression test files automatically', () => {
  assert.equal(pkg.scripts?.test, 'node --test ../tests/*.test.mjs');
  const tests = fs.readdirSync(testDir).filter((name) => name.endsWith('.test.mjs'));
  assert.ok(tests.includes('candidate_readiness_recovery.test.mjs'));
  assert.ok(tests.includes('phase1_core_regression_recovery.test.mjs'));
  assert.ok(tests.includes('search_worker_stage2.test.mjs'));
});
