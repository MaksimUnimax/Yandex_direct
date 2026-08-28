import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const read = (name) => fs.readFileSync(path.resolve(src, name), 'utf8');

test('D-11 manifest connects Direct protocol and only required Direct host permission', () => {
  const manifest = JSON.parse(read('manifest.json'));
  assert.equal(manifest.host_permissions.includes('https://api.direct.yandex.com/*'), true);
  const scripts = manifest.content_scripts?.[0]?.js || [];
  assert.equal(scripts.includes('shared/direct_protocol.js'), true);
  assert.equal(scripts.filter((item) => item === 'shared/direct_protocol.js').length, 1);
  assert.equal(scripts.includes('content_script.js'), true);
});

test('D-12 popup exposes separate Direct credential/policy controls and explicit Units warning', () => {
  const html = read('popup.html');
  for (const id of [
    'directCredentials', 'directCredentialState', 'directOauthToken', 'directClientLogin',
    'saveDirectCredential', 'checkDirectCredential', 'directCheckMeta',
    'directManualEnabled', 'directMaxRequestsRun', 'directMaxPageSize', 'directMaxReportDays', 'directMaxReportRows'
  ]) assert.match(html, new RegExp(`id=["']${id}["']`));
  assert.match(html, /value=["']direct["']/);
  assert.match(html, /Campaigns\.get/);
  assert.match(html, /FieldNames=\["Id"\]/);
  assert.match(html, /Limit=1/);
  assert.match(html, /Direct Units/);
  assert.match(html, /max=["']20["']/);
  assert.match(html, /max=["']1000["']/);
  assert.match(html, /max=["']31["']/);
});

test('D-13 top and bottom common Save buttons use exactly the same popup handler', () => {
  const html = read('popup.html');
  const js = read('popup.js');
  assert.match(html, /id=["']saveSettingsTop["'][^>]*>Сохранить общие настройки</);
  assert.match(html, /id=["']saveSettings["'][^>]*>Сохранить общие настройки</);
  assert.match(js, /function\s+onSaveSettingsClick\s*\(/);
  assert.match(js, /\$\("saveSettingsTop"\)\.addEventListener\("click",\s*onSaveSettingsClick\)/);
  assert.match(js, /\$\("saveSettings"\)\.addEventListener\("click",\s*onSaveSettingsClick\)/);
  assert.equal((js.match(/function\s+onSaveSettingsClick\s*\(/g) || []).length, 1);
});

test('D-14 production popup locks Direct Autorun while still saving Direct policy', () => {
  const js = read('popup.js');
  assert.match(js, /PRODUCTION_AUTORUN_LOCKED\s*=\s*new Set\(\["webmaster",\s*"metrika",\s*"direct"\]\)/);
  assert.match(js, /YMB_SAVE_DIRECT_POLICY/);
  assert.match(js, /directPolicyFromForm/);
  assert.match(js, /max_requests_per_run:\s*Math\.min\(20/);
  assert.match(js, /max_page_size:\s*Math\.min\(1000/);
  assert.match(js, /max_report_days:\s*Math\.min\(31/);
  assert.match(js, /max_report_rows:\s*Math\.min\(1000/);
});

test('D-15 popup never writes a saved OAuth token back into the password field', () => {
  const js = read('popup.js');
  assert.match(js, /\$\("directOauthToken"\)\.value\s*=\s*""/);
  assert.match(js, /direct\.has_oauth_token\s*\?/);
  assert.doesNotMatch(js, /directOauthToken"\)\.value\s*=\s*direct\.oauth_token/);
});

test('D-16 popup recovery injection and content runtime both recognize Direct protocol', () => {
  const bootstrap = read('popup_context_bootstrap.js');
  const content = read('content_script.js');
  assert.match(bootstrap, /shared\/direct_protocol\.js/);
  assert.match(content, /DirectProtocol/);
  assert.match(content, /YMBServiceRegistry\.SERVICES\.DIRECT\) return DirectProtocol/);
});

test('D-17 Direct credential Save/Check use generic service routes; no token unification path exists in popup', () => {
  const js = read('popup.js');
  assert.match(js, /YMB_SAVE_SERVICE_CREDENTIAL/);
  assert.match(js, /YMB_CHECK_SERVICE_CREDENTIAL/);
  assert.match(js, /credential\.client_login\s*=\s*\$\("directClientLogin"\)\.value\.trim\(\)/);
  assert.doesNotMatch(js, /webmasterOauthToken[^\n]*directOauthToken/);
  assert.doesNotMatch(js, /metrikaOauthToken[^\n]*directOauthToken/);
});
