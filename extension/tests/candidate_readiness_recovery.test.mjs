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
const popupContextBootstrap = fs.readFileSync(path.join(src, 'popup_context_bootstrap.js'), 'utf8');
const phase3Bootstrap = fs.readFileSync(path.join(src, 'phase3_service_worker_bootstrap.js'), 'utf8');
const bootstrap = fs.readFileSync(path.join(src, 'service_worker_bootstrap.js'), 'utf8');
const webmasterRuntime = fs.readFileSync(path.join(src, 'webmaster_worker_runtime.js'), 'utf8');
const worker = fs.readFileSync(path.join(src, 'service_worker.js'), 'utf8');
const product = fs.readFileSync(path.join(src, 'shared/product.js'), 'utf8');

function exists(relativePath) {
  return fs.existsSync(path.join(src, relativePath));
}

function quotedJsSources(html) {
  return [...html.matchAll(/<script\s+src="([^"]+)"\s*><\/script>/g)].map((m) => m[1]);
}

function importedScripts(source) {
  return [...source.matchAll(/importScripts\(([\s\S]*?)\);/g)]
    .flatMap((call) => [...call[1].matchAll(/"([^"]+\.js)"/g)].map((m) => m[1]));
}

test('candidate manifest is MV3 and points only to files present in extension/src', () => {
  assert.equal(manifest.manifest_version, 3);
  assert.equal(manifest.background?.service_worker, 'phase3_service_worker_bootstrap.js');
  assert.equal(manifest.action?.default_popup, 'popup.html');
  assert.equal(exists(manifest.background.service_worker), true);
  assert.equal(exists(manifest.action.default_popup), true);
  for (const block of manifest.content_scripts || []) {
    for (const file of block.js || []) assert.equal(exists(file), true, `manifest content script is missing: ${file}`);
  }
});

test('candidate popup loads local bootstrap scripts and context recovery starts popup runtime only afterwards', () => {
  const scripts = quotedJsSources(popupHtml);
  assert.deepEqual(scripts, ['popup_transfer_guard.js', 'popup_context_bootstrap.js']);
  for (const file of scripts) assert.equal(exists(file), true, `popup script is missing: ${file}`);
  assert.equal(exists('popup.js'), true, 'dynamic popup runtime is missing');
  assert.match(popupContextBootstrap, /chrome\.runtime\.getURL\("popup\.js"\)/);
  assert.match(popupContextBootstrap, /\.finally\(\(\) => loadPopupRuntime\(\)\)/);
});

test('candidate Phase 3 bootstrap preserves accepted worker bootstrap and loads only present runtime modules', () => {
  const outerImports = importedScripts(phase3Bootstrap);
  assert.deepEqual(outerImports, ['service_worker_bootstrap.js', 'webmaster_worker_runtime.js']);
  for (const file of outerImports) assert.equal(exists(file), true, `Phase 3 bootstrap import is missing: ${file}`);

  assert.match(bootstrap, /importScripts\("service_worker\.js"\)/);
  const workerImports = importedScripts(worker);
  assert.ok(workerImports.length >= 10);
  for (const file of workerImports) assert.equal(exists(file), true, `worker importScript is missing: ${file}`);

  const phase3RuntimeImports = importedScripts(webmasterRuntime);
  assert.deepEqual(phase3RuntimeImports, [
    'shared/credential_store_model.js',
    'shared/webmaster_protocol.js',
    'shared/credential_runtime.js',
    'shared/phase3_provider_runtime.js',
    'shared/settings_backup_v3_runtime.js'
  ]);
  for (const file of phase3RuntimeImports) assert.equal(exists(file), true, `Phase 3 runtime import is missing: ${file}`);
});

test('candidate version stays aligned between manifest, package and product module', () => {
  assert.equal(manifest.version, '0.1.1');
  assert.equal(pkg.version, manifest.version);
  assert.match(product, /VERSION:\s*"0\.1\.1"/);
});

test('candidate host permissions stay limited to ChatGPT plus official enabled Yandex API hosts', () => {
  assert.deepEqual(manifest.host_permissions, [
    'https://chatgpt.com/*',
    'https://chat.openai.com/*',
    'https://searchapi.api.cloud.yandex.net/*',
    'https://api.webmaster.yandex.net/*'
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
  assert.ok(tests.includes('phase3_worker_runtime.test.mjs'));
});
