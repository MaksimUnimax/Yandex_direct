import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const manifest = JSON.parse(fs.readFileSync(path.join(src, 'manifest.json'), 'utf8'));
const popupHtml = fs.readFileSync(path.join(src, 'popup.html'), 'utf8');
const bootstrap = fs.readFileSync(path.join(src, 'popup_context_bootstrap.js'), 'utf8');

function extractBootstrapFiles(source) {
  const match = source.match(/const CONTENT_FILES = Object\.freeze\(\[([\s\S]*?)\]\);/);
  assert.ok(match, 'bootstrap CONTENT_FILES declaration must exist');
  return [...match[1].matchAll(/"([^"]+\.js)"/g)].map((row) => row[1]);
}

test('popup context bootstrap has scripting capability and exactly mirrors manifest content bundle', () => {
  assert.ok(manifest.permissions.includes('tabs'));
  assert.ok(manifest.permissions.includes('scripting'));
  assert.equal(manifest.content_scripts.length, 1);
  const manifestFiles = manifest.content_scripts[0].js;
  const bootstrapFiles = extractBootstrapFiles(bootstrap);
  assert.deepEqual(bootstrapFiles, manifestFiles, 'self-recovery must inject the same files in the same order as manifest content_scripts');
});

test('popup runtime starts only after context bootstrap', () => {
  const transfer = popupHtml.indexOf('<script src="popup_transfer_guard.js"></script>');
  const context = popupHtml.indexOf('<script src="popup_context_bootstrap.js"></script>');
  assert.ok(transfer >= 0 && context > transfer, 'context bootstrap must load after transfer guard');
  assert.equal(popupHtml.includes('<script src="popup.js"></script>'), false, 'popup.js must not race context bootstrap as a static script');
  assert.match(bootstrap, /ensureCurrentChatContext\(\)/);
  assert.match(bootstrap, /\.then\(\(result\) => publishBootstrapResult\(result\)\)/);
  assert.match(bootstrap, /\.finally\(\(\) => loadPopupRuntime\(\)\)/);
  assert.match(bootstrap, /chrome\.runtime\.getURL\("popup\.js"\)/);
});

test('missing receiver is recovered by deterministic injection before identity is retried', () => {
  assert.match(bootstrap, /chrome\.tabs\.sendMessage\(tabId, \{ type: "WS_GET_IDENTITY" \}/);
  assert.match(bootstrap, /for \(const file of CONTENT_FILES\)/);
  assert.match(bootstrap, /chrome\.scripting\.executeScript\(\{ target: \{ tabId \}, files: \[file\] \}\)/);
  assert.match(bootstrap, /setBootstrapStatus\("Восстанавливаю связь с текущим ChatGPT…"\)/);
  assert.match(bootstrap, /setBootstrapStatus\("Связь с ChatGPT восстановлена\."/);
});

test('bootstrap publishes only a sanitized recovery outcome for browser verification and diagnostics', () => {
  assert.match(bootstrap, /__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__/);
  assert.match(bootstrap, /attempted: source\.attempted === true/);
  assert.match(bootstrap, /recovered: source\.recovered === true/);
  assert.match(bootstrap, /reason: typeof source\.reason === "string"/);
  assert.match(bootstrap, /tab_id: Number\.isInteger/);
  const publisher = bootstrap.slice(bootstrap.indexOf('function publishBootstrapResult'), bootstrap.indexOf('function loadPopupRuntime'));
  assert.equal(publisher.includes('response'), false, 'published bootstrap outcome must not expose identity response or credentials');
});

test('bootstrap failure remains visible through popup runtime startup instead of reverting to false ready', () => {
  assert.match(bootstrap, /function preserveBootstrapFailureThroughStartup/);
  assert.match(bootstrap, /new MutationObserver/);
  assert.match(bootstrap, /observer\.disconnect\(\);\n      setBootstrapStatus\(expected, "error"\)/);
  assert.match(bootstrap, /globalThis\.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__ = message/);
  assert.match(bootstrap, /preserveBootstrapFailureThroughStartup\(message\)/);
});
