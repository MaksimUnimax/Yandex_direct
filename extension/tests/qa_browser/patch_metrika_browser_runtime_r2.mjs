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

replaceOnce(
  "  await page.waitForFunction(() => document.querySelector('#saveMetrikaCredential')?.disabled === false);\n  const rerender = await page.evaluate(() => ({",
  "  await page.waitForFunction(() => document.querySelector('#saveMetrikaCredential')?.disabled === false);\n  await page.waitForFunction(() => /проверено/i.test(document.querySelector('#metrikaCredentialState')?.textContent || '') && document.querySelector('#saveMetrikaCredential')?.disabled === false);\n  const rerender = await page.evaluate(() => ({",
  'popup rerender quiescence'
);

replaceOnce(
  "  console.log('M15_POPUP_GEOMETRY_AND_FOUR_SERVICE_UI_PASS');",
  `  console.log('M15_POPUP_GEOMETRY_AND_FOUR_SERVICE_UI_PASS');

  const scrollProof = await page.evaluate(() => {
    const main = document.querySelector('main');
    const target = document.querySelector('#metrikaMaxReportDays');
    if (!main || !target) return null;
    main.scrollTop = 0;
    const before = main.scrollTop;
    target.scrollIntoView({ block: 'center' });
    const after = main.scrollTop;
    const mainRect = main.getBoundingClientRect();
    const targetRect = target.getBoundingClientRect();
    const result = {
      clientHeight: main.clientHeight,
      scrollHeight: main.scrollHeight,
      before,
      after,
      targetInside: targetRect.top >= mainRect.top && targetRect.bottom <= mainRect.bottom
    };
    main.scrollTop = 0;
    return result;
  });
  assert.ok(scrollProof);
  assert.equal(scrollProof.clientHeight, 560);
  assert.ok(scrollProof.scrollHeight > scrollProof.clientHeight);
  assert.equal(scrollProof.before, 0);
  assert.ok(scrollProof.after > 0);
  assert.equal(scrollProof.targetInside, true);
  console.log('M15_METRIKA_POLICY_INTERNAL_SCROLL_PASS');`,
  'M15 bounded internal scroll proof'
);

replaceOnce(
  "  console.log('M15_CREDENTIAL_SAVE_RERENDER_SECRET_REDACTION_PASS');",
  `  console.log('M15_CREDENTIAL_SAVE_RERENDER_SECRET_REDACTION_PASS');

  const rawCredentialBaseline = await workerEval(workerClient, \`(async () => {
    const c = await globalThis.YMBCredentialRuntime.load();
    return {
      wordstat: { api_key: c.wordstat.api_key, folder_id: c.wordstat.folder_id },
      search: { api_key: c.search.api_key, folder_id: c.search.folder_id },
      webmaster: { oauth_token: c.webmaster.oauth_token },
      metrika: { oauth_token: c.metrika.oauth_token }
    };
  })()\`);
  assert.deepEqual(rawCredentialBaseline, {
    wordstat: { api_key: 'm4-wordstat-secret', folder_id: 'm4-wordstat-folder' },
    search: { api_key: 'm4-search-secret', folder_id: 'm4-search-folder' },
    webmaster: { oauth_token: 'm4-webmaster-oauth' },
    metrika: { oauth_token: 'm4-metrika-oauth' }
  });

  await saveCredentialThroughPopup(page, 'metrika', { '#metrikaOauthToken': '' });
  const rawAfterBlankMetrikaSave = await workerEval(workerClient, \`(async () => {
    const c = await globalThis.YMBCredentialRuntime.load();
    return {
      wordstat: { api_key: c.wordstat.api_key, folder_id: c.wordstat.folder_id },
      search: { api_key: c.search.api_key, folder_id: c.search.folder_id },
      webmaster: { oauth_token: c.webmaster.oauth_token },
      metrika: { oauth_token: c.metrika.oauth_token }
    };
  })()\`);
  assert.deepEqual(rawAfterBlankMetrikaSave, rawCredentialBaseline);
  assert.equal(await page.$eval('#metrikaOauthToken', (node) => node.value), '');
  console.log('M04_M15_BLANK_METRIKA_SAVE_PRESERVES_CREDENTIAL_PASS');

  await page.click('#saveSettings');
  await page.waitForFunction(() => document.querySelector('#saveSettings')?.disabled === false);
  const rawAfterCommonSave = await workerEval(workerClient, \`(async () => {
    const c = await globalThis.YMBCredentialRuntime.load();
    return {
      wordstat: { api_key: c.wordstat.api_key, folder_id: c.wordstat.folder_id },
      search: { api_key: c.search.api_key, folder_id: c.search.folder_id },
      webmaster: { oauth_token: c.webmaster.oauth_token },
      metrika: { oauth_token: c.metrika.oauth_token }
    };
  })()\`);
  assert.deepEqual(rawAfterCommonSave, rawCredentialBaseline);
  console.log('M04_M15_COMMON_SAVE_PRESERVES_CREDENTIALS_PASS');

  for (const service of ['wordstat', 'search', 'webmaster', 'metrika']) {
    const switchState = await page.evaluate((nextService) => {
      const selector = document.querySelector('#activeService');
      selector.value = nextService;
      selector.dispatchEvent(new Event('change', { bubbles: true }));
      return {
        selected: selector.value,
        openCards: [...document.querySelectorAll('.credential-card[open]')].map((node) => node.dataset.service),
        secretInputsBlank: [
          document.querySelector('#wordstatApiKey')?.value || '',
          document.querySelector('#searchApiKey')?.value || '',
          document.querySelector('#webmasterOauthToken')?.value || '',
          document.querySelector('#metrikaOauthToken')?.value || ''
        ].every((value) => value === '')
      };
    }, service);
    assert.equal(switchState.selected, service);
    assert.deepEqual(switchState.openCards, [service]);
    assert.equal(switchState.secretInputsBlank, true);
    const rawAfterSwitch = await workerEval(workerClient, \`(async () => {
      const c = await globalThis.YMBCredentialRuntime.load();
      return {
        wordstat: { api_key: c.wordstat.api_key, folder_id: c.wordstat.folder_id },
        search: { api_key: c.search.api_key, folder_id: c.search.folder_id },
        webmaster: { oauth_token: c.webmaster.oauth_token },
        metrika: { oauth_token: c.metrika.oauth_token }
      };
    })()\`);
    assert.deepEqual(rawAfterSwitch, rawCredentialBaseline);
  }
  console.log('M15_FOUR_SERVICE_SWITCH_CREDENTIAL_ISOLATION_PASS');`,
  'M04/M15 blank save common save and service switching proof'
);

replaceOnce(
  "  const mutate = await send(page, { type: 'YMB_SAVE_SERVICE_CREDENTIAL', service: 'metrika', credential: { oauth_token: 'm4-mutated-token' } });",
  `  const tamperedBackup = structuredClone(backup);
  tamperedBackup.settings.credentials.metrika.oauth_token = 'm4-tampered-token';
  const tamperedImport = await send(page, { type: 'WS_IMPORT_BACKUP', backup: tamperedBackup });
  assert.equal(tamperedImport?.ok, false);
  assert.equal(tamperedImport?.code, 'BACKUP_CHECKSUM_MISMATCH');
  const rawAfterTamperedImport = await workerEval(workerClient, \`(async () => {
    const c = await globalThis.YMBCredentialRuntime.load();
    return {
      wordstat: { api_key: c.wordstat.api_key, folder_id: c.wordstat.folder_id },
      search: { api_key: c.search.api_key, folder_id: c.search.folder_id },
      webmaster: { oauth_token: c.webmaster.oauth_token },
      metrika: { oauth_token: c.metrika.oauth_token }
    };
  })()\`);
  assert.deepEqual(rawAfterTamperedImport, rawCredentialBaseline);
  console.log('M04_M16_BACKUP_CHECKSUM_TAMPER_REJECTS_BEFORE_MUTATION_PASS');

  const mutate = await send(page, { type: 'YMB_SAVE_SERVICE_CREDENTIAL', service: 'metrika', credential: { oauth_token: 'm4-mutated-token' } });`,
  'M04/M16 checksum tamper browser proof'
);

fs.writeFileSync(file, source, 'utf8');
if (gitBlobSha(fs.readFileSync(file)) === expectedBlob) throw new Error('Harness patch produced no change');
console.log('PHASE4_METRIKA_BROWSER_HARNESS_R2_SOURCE_IDENTITY_PASS');
console.log('PHASE4_METRIKA_BROWSER_HARNESS_R2_PARSE_PATCH_PASS');
console.log('PHASE4_METRIKA_BROWSER_HARNESS_R2_BACKUP_V3_CONTRACT_PASS');
console.log('PHASE4_METRIKA_BROWSER_HARNESS_R2_RERENDER_QUIESCENCE_PASS');
console.log('PHASE4_METRIKA_BROWSER_HARNESS_LITERAL_CLOSURE_PATCH_PASS');
