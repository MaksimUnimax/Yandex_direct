import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../src');
const manifest = JSON.parse(fs.readFileSync(path.join(src, 'manifest.json'), 'utf8'));

const EXPECTED_PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyzoi4OKB6jLqWTgqlx3cYjriXg6epGYLwG2Pr/NE9xPIWY6ztbh4xI1SVrW2KdyXqbSF9S6J9H3Rq+7J+kanAINNdzejVEX/5DMAVhoMZiIIEmDFbp/5G4IsqH/KYlTH1ax1eShPmGJcjL1wF67w2+bl6/1ZhLLy5d1IBoii1HID/I0Z4Srsz0epdwlXUC18V/D/nyihiXCvkUKaDKD2qbtJSIHF+qVOgo6h51laZtJpQvnFpXKyoPihewNAAkGP31x1qg+IYboxmSAopLvweLTuNRctZPk2QmltTkR1Z9Qw+quDnsThlRDvf/HT9zFfR5TTKIBk/DDTqtPtS8bPiwIDAQAB';
const EXPECTED_EXTENSION_ID = 'pckmmaodnfeajgigadfaejfjppdbgmpo';

function extensionIdFromManifestKey(base64Key) {
  const der = Buffer.from(base64Key, 'base64');
  const digest = createHash('sha256').update(der).digest().subarray(0, 16);
  let id = '';
  for (const byte of digest) {
    id += String.fromCharCode(97 + ((byte >> 4) & 0x0f));
    id += String.fromCharCode(97 + (byte & 0x0f));
  }
  return id;
}

test('P9-06A: production manifest carries one frozen local stable key and derives the expected extension ID', () => {
  assert.equal(manifest.key, EXPECTED_PUBLIC_KEY);
  assert.equal(extensionIdFromManifestKey(manifest.key), EXPECTED_EXTENSION_ID);
});

test('P9-06A: stable local identity does not yet authorize Google OAuth or provider network access', () => {
  assert.equal(manifest.permissions.includes('identity'), false);
  assert.equal(manifest.host_permissions.some((item) => String(item).includes('googleapis.com')), false);
  assert.equal(Object.hasOwn(manifest, 'oauth2'), false);
});
