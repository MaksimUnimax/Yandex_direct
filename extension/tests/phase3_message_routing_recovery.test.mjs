import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const bootstrap = fs.readFileSync(path.join(src, 'phase3_service_worker_bootstrap.js'), 'utf8');
const runtime = fs.readFileSync(path.join(src, 'webmaster_worker_runtime.js'), 'utf8');

test('Phase 3 bootstrap leaves YMB_* messages exclusively to the Phase 3 listener', () => {
  assert.match(bootstrap, /function isPhase3RuntimeMessage\(message\)/);
  assert.match(bootstrap, /startsWith\("YMB_"\)/);
  assert.match(bootstrap, /if \(isPhase3RuntimeMessage\(message\)\) return false;/);
  assert.match(runtime, /if \(!String\(message\?\.type \|\| ""\)\.startsWith\("YMB_"\)\) return false;/);
});

test('accepted worker is wrapped before Phase 3 runtime registers its dedicated listener', () => {
  const acceptedWorker = bootstrap.indexOf('importScripts("service_worker_bootstrap.js")');
  const phase3Worker = bootstrap.indexOf('importScripts("webmaster_worker_runtime.js")');
  const restoreNativeListener = bootstrap.indexOf('runtimeEvent.addListener = nativeAddListener');

  assert.ok(acceptedWorker >= 0, 'accepted worker bootstrap must still load');
  assert.ok(phase3Worker > acceptedWorker, 'Phase 3 runtime must load after accepted worker');
  assert.ok(restoreNativeListener > acceptedWorker && restoreNativeListener < phase3Worker,
    'native addListener must be restored before the dedicated Phase 3 listener registers');
});

test('managed WS_* imports remain owned by the compatibility wrapper', () => {
  assert.match(bootstrap, /"WS_IMPORT_BACKUP", "WS_IMPORT_SETTINGS"/);
  assert.match(bootstrap, /if \(!isManagedSettingsImport\(message\)\) return listener\(message, sender, sendResponse\);/);
  assert.match(bootstrap, /runtime\.importSettingsBackup/);
});
