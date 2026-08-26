import fs from 'node:fs';
import crypto from 'node:crypto';

const file = process.argv[2];
if (!file || !fs.existsSync(file)) throw new Error('Usage: node patch_metrika_browser_runtime_r2.mjs <harness-file>');

function gitBlobSha(buffer) {
  const header = Buffer.from(`blob ${buffer.length}\0`);
  return crypto.createHash('sha1').update(header).update(buffer).digest('hex');
}

const expectedBlob = 'ae77710520c70f769a51b170ca2880e19f8f57d1';
const originalBytes = fs.readFileSync(file);
const actualBlob = gitBlobSha(originalBytes);
if (actualBlob !== expectedBlob) throw new Error(`Metrika browser harness drift: expected ${expectedBlob}, got ${actualBlob}`);
let source = originalBytes.toString('utf8');

function replaceOnce(from, to, label) {
  const count = source.split(from).length - 1;
  if (count !== 1) throw new Error(`${label}: expected one patch anchor, got ${count}`);
  source = source.replace(from, to);
}

replaceOnce(
  "  if (result.exceptionDetails) throw new Error(result.exceptionDetails.text || 'service worker evaluation failed');",
  "  if (result.exceptionDetails) {\n    const detail = result.exceptionDetails.exception?.description || result.exceptionDetails.text || 'service worker evaluation failed';\n    throw new Error(detail);\n  }",
  'workerEval diagnostics'
);

replaceOnce(
  "      if (/\\/management\\/v1\\/counter\\/123(?:\\\\?|$)/.test(target)) return json({ counter: { id: 123, name: 'QA counter', site: 'qa.invalid', status: 'Active', permission: 'own' } });\n",
  "",
  'unused getCounter regex branch'
);

replaceOnce(
  "  assert.match(String(backup.integrity?.sha256 || ''), /^[a-f0-9]{64}$/);",
  "  assert.match(String(backup.settings_sha256 || ''), /^[a-f0-9]{64}$/);",
  'backup v3 checksum contract'
);

fs.writeFileSync(file, source, 'utf8');
if (gitBlobSha(fs.readFileSync(file)) === expectedBlob) throw new Error('Harness patch produced no change');
console.log('PHASE4_METRIKA_BROWSER_HARNESS_R2_SOURCE_IDENTITY_PASS');
console.log('PHASE4_METRIKA_BROWSER_HARNESS_R2_PARSE_PATCH_PASS');
console.log('PHASE4_METRIKA_BROWSER_HARNESS_R2_BACKUP_V3_CONTRACT_PASS');
