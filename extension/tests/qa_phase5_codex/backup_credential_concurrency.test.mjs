import test from 'node:test';
import assert from 'node:assert/strict';

// This guard is intentionally source-level until the product fix exposes the
// credential mutation lock to the backup runtime. It prevents a future backup
// path from bypassing the same serialization used by per-service credential saves.
test('backup runtime must use the credential mutation serialization primitive', async () => {
  const fs = await import('node:fs');
  const path = await import('node:path');
  const { fileURLToPath } = await import('node:url');
  const here = path.dirname(fileURLToPath(import.meta.url));
  const src = path.resolve(here, '../../src');
  const credentialRuntime = fs.readFileSync(path.join(src, 'shared/credential_runtime.js'), 'utf8');
  const backupRuntime = fs.readFileSync(path.join(src, 'shared/settings_backup_v3_runtime.js'), 'utf8');
  assert.match(credentialRuntime, /withExclusiveMutation/);
  assert.match(backupRuntime, /CredentialRuntime\.withExclusiveMutation/);
});
