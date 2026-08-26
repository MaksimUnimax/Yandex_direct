import fs from 'node:fs';
import process from 'node:process';

const target = process.argv[2];
if (!target || !fs.existsSync(target)) throw new Error(`RUNTIME_HARNESS_MISSING ${target || '<empty>'}`);
let source = fs.readFileSync(target, 'utf8');

function replaceExact(needle, replacement, marker, expectedCount = 1) {
  const count = source.split(needle).length - 1;
  if (count !== expectedCount) throw new Error(`${marker}_COUNT_${count}_EXPECTED_${expectedCount}`);
  source = source.replaceAll(needle, replacement);
}

replaceExact(
  "  await page.waitForFunction(() => document.querySelector('#versionBadge')?.textContent?.startsWith('v'));\n",
  "  await page.waitForFunction(() => document.querySelector('#versionBadge')?.textContent?.startsWith('v'));\n" +
  "  await page.waitForFunction(() => {\n" +
  "    const save = document.querySelector('#saveWordstatCredential');\n" +
  "    const state = document.querySelector('#wordstatCredentialState');\n" +
  "    return Boolean(save && !save.disabled && state && String(state.textContent || '').trim());\n" +
  "  }, { timeout: 15000 });\n" +
  "  console.log('W19_POPUP_INITIAL_REFRESH_READY_PASS');\n",
  'INITIAL_READY'
);

replaceExact(
  "  await page.click('#saveWordstatCredential');\n  await page.waitForFunction(() => document.querySelector('#wordstatApiKey')?.value === '');\n",
  "  await page.click('#saveWordstatCredential');\n" +
  "  await page.waitForFunction(() => {\n" +
  "    const button = document.querySelector('#saveWordstatCredential');\n" +
  "    const secret = document.querySelector('#wordstatApiKey');\n" +
  "    const folder = document.querySelector('#wordstatFolderId');\n" +
  "    return Boolean(button && !button.disabled && secret?.value === '' && folder?.value === 'browser-word-folder');\n" +
  "  }, { timeout: 15000 });\n" +
  "  {\n" +
  "    const saved = await send(page, { type: 'YMB_GET_CREDENTIALS' });\n" +
  "    assert.equal(saved?.ok, true);\n" +
  "    assert.equal(saved?.credentials?.wordstat?.has_api_key, true);\n" +
  "    assert.equal(saved?.credentials?.wordstat?.has_folder_id, true);\n" +
  "    assert.equal(saved?.credentials?.wordstat?.folder_id, 'browser-word-folder');\n" +
  "    assert.equal(saved?.credentials?.wordstat?.check_state, 'NOT_CHECKED');\n" +
  "  }\n" +
  "  console.log('W19_WORDSTAT_UI_SAVE_AUTHORITATIVE_PASS');\n",
  'WORDSTAT_SAVE'
);

replaceExact(
  "  await page.click('#checkWordstatCredential');\n  await sleep(1200);\n",
  "  await page.click('#checkWordstatCredential');\n" +
  "  await page.waitForFunction(() => {\n" +
  "    const button = document.querySelector('#checkWordstatCredential');\n" +
  "    const state = document.querySelector('#wordstatCredentialState');\n" +
  "    return Boolean(button && !button.disabled && /проверено/i.test(state?.textContent || ''));\n" +
  "  }, { timeout: 15000 });\n" +
  "  {\n" +
  "    const checked = await send(page, { type: 'YMB_GET_CREDENTIALS' });\n" +
  "    assert.equal(checked?.ok, true);\n" +
  "    assert.equal(checked?.credentials?.wordstat?.check_state, 'PRESENT');\n" +
  "  }\n" +
  "  console.log('W19_WORDSTAT_CHECK_UI_QUIESCENT_PASS');\n",
  'WORDSTAT_CHECK'
);

replaceExact(
  "  await page.click('#saveSearchCredential');\n  await page.waitForFunction(() => document.querySelector('#searchApiKey')?.value === '');\n",
  "  await page.click('#saveSearchCredential');\n" +
  "  await page.waitForFunction(() => {\n" +
  "    const button = document.querySelector('#saveSearchCredential');\n" +
  "    const secret = document.querySelector('#searchApiKey');\n" +
  "    const folder = document.querySelector('#searchFolderId');\n" +
  "    return Boolean(button && !button.disabled && secret?.value === '' && folder?.value === 'browser-search-folder');\n" +
  "  }, { timeout: 15000 });\n" +
  "  {\n" +
  "    const saved = await send(page, { type: 'YMB_GET_CREDENTIALS' });\n" +
  "    assert.equal(saved?.ok, true);\n" +
  "    assert.equal(saved?.credentials?.search?.has_api_key, true);\n" +
  "    assert.equal(saved?.credentials?.search?.has_folder_id, true);\n" +
  "    assert.equal(saved?.credentials?.search?.folder_id, 'browser-search-folder');\n" +
  "    assert.equal(saved?.credentials?.search?.check_state, 'NOT_CHECKED');\n" +
  "  }\n" +
  "  console.log('W19_SEARCH_UI_SAVE_AUTHORITATIVE_PASS');\n",
  'SEARCH_SAVE'
);

const webmasterSaveNeedle = "  await page.click('#saveWebmasterCredential');\n  await page.waitForFunction(() => document.querySelector('#webmasterOauthToken')?.value === '');\n";
const webmasterSaveReplacement =
  "  await page.click('#saveWebmasterCredential');\n" +
  "  await page.waitForFunction(() => {\n" +
  "    const button = document.querySelector('#saveWebmasterCredential');\n" +
  "    const secret = document.querySelector('#webmasterOauthToken');\n" +
  "    return Boolean(button && !button.disabled && secret?.value === '');\n" +
  "  }, { timeout: 15000 });\n" +
  "  {\n" +
  "    const saved = await send(page, { type: 'YMB_GET_CREDENTIALS' });\n" +
  "    assert.equal(saved?.ok, true);\n" +
  "    assert.equal(saved?.credentials?.webmaster?.has_oauth_token, true);\n" +
  "    assert.equal(saved?.credentials?.webmaster?.check_state, 'NOT_CHECKED');\n" +
  "  }\n" +
  "  console.log('W19_WEBMASTER_UI_SAVE_AUTHORITATIVE_PASS');\n";
replaceExact(webmasterSaveNeedle, webmasterSaveReplacement, 'WEBMASTER_SAVE', 2);

replaceExact(
  "  await page.waitForFunction(() => /неверный|истёк/i.test(document.querySelector('#webmasterCredentialState')?.textContent || ''));\n",
  "  await page.waitForFunction(() => {\n" +
  "    const button = document.querySelector('#checkWebmasterCredential');\n" +
  "    const state = document.querySelector('#webmasterCredentialState');\n" +
  "    return Boolean(button && !button.disabled && /неверный|истёк/i.test(state?.textContent || ''));\n" +
  "  }, { timeout: 15000 });\n" +
  "  {\n" +
  "    const checked = await send(page, { type: 'YMB_GET_CREDENTIALS' });\n" +
  "    assert.equal(checked?.ok, true);\n" +
  "    assert.equal(checked?.credentials?.webmaster?.check_state, 'INVALID_OR_EXPIRED');\n" +
  "  }\n" +
  "  console.log('W19_WEBMASTER_INVALID_CHECK_UI_QUIESCENT_PASS');\n",
  'WEBMASTER_INVALID_CHECK'
);

replaceExact(
  "  await page.waitForFunction(() => document.querySelector('#webmasterUserId')?.textContent === '321');\n",
  "  await page.waitForFunction(() => {\n" +
  "    const button = document.querySelector('#checkWebmasterCredential');\n" +
  "    return Boolean(button && !button.disabled && document.querySelector('#webmasterUserId')?.textContent === '321');\n" +
  "  }, { timeout: 15000 });\n" +
  "  {\n" +
  "    const checked = await send(page, { type: 'YMB_GET_CREDENTIALS' });\n" +
  "    assert.equal(checked?.ok, true);\n" +
  "    assert.equal(checked?.credentials?.webmaster?.user_id, '321');\n" +
  "    assert.equal(checked?.credentials?.webmaster?.check_state, 'PRESENT');\n" +
  "  }\n" +
  "  console.log('W19_WEBMASTER_VALID_CHECK_UI_QUIESCENT_PASS');\n",
  'WEBMASTER_VALID_CHECK'
);

fs.writeFileSync(target, source);
console.log('PHASE3_RUNTIME_REFRESH_QUIESCENCE_PATCH_PASS');
