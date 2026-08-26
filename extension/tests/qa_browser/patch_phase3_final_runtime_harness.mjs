import fs from 'node:fs';
import process from 'node:process';

const target = process.argv[2];
if (!target || !fs.existsSync(target)) throw new Error(`FINAL_RUNTIME_HARNESS_MISSING ${target || '<empty>'}`);
let source = fs.readFileSync(target, 'utf8');

function replaceOnce(needle, replacement, marker) {
  if (!source.includes(needle)) throw new Error(`${marker}_NEEDLE_MISSING`);
  source = source.replace(needle, replacement);
}

replaceOnce(
`      const headers = options.headers || {};
      let hasAuthorization = false;
      try {
        hasAuthorization = headers instanceof Headers
          ? headers.has('Authorization')
          : Object.keys(headers).some((key) => String(key).toLowerCase() === 'authorization');
      } catch {}
      globalThis.__YMB_BROWSER_FETCHES.push({
        url: target,
        method: String(options.method || 'GET').toUpperCase(),
        has_authorization: hasAuthorization
      });`,
`      const headers = options.headers || {};
      let authorization = '';
      try {
        if (headers instanceof Headers) authorization = String(headers.get('Authorization') || '');
        else {
          const key = Object.keys(headers).find((item) => String(item).toLowerCase() === 'authorization');
          authorization = key ? String(headers[key] || '') : '';
        }
      } catch {}
      const expectedWebmasterAuthorization = target.includes('/v4/')
        ? (globalThis.__YMB_BROWSER_MODE === 'webmaster401' ? 'OAuth browser-invalid-oauth' : 'OAuth browser-valid-oauth')
        : '';
      globalThis.__YMB_BROWSER_FETCHES.push({
        url: target,
        method: String(options.method || 'GET').toUpperCase(),
        has_authorization: Boolean(authorization),
        webmaster_authorization_exact: expectedWebmasterAuthorization ? authorization === expectedWebmasterAuthorization : null
      });`,
'FINAL_W05_AUTH'
);

replaceOnce(
`  const publicCredentials = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  assert.equal(publicCredentials.ok, true);`,
`  const credentialUiAfterRerender = await page.evaluate(() => {
    const wordstat = document.querySelector('#wordstatCredentials');
    const search = document.querySelector('#searchCredentials');
    const webmaster = document.querySelector('#webmasterCredentials');
    wordstat.open = true; search.open = false; webmaster.open = false;
    const wordstatSnapshot = {
      folder: document.querySelector('#wordstatFolderId')?.value || '',
      secret: document.querySelector('#wordstatApiKey')?.value || ''
    };
    wordstat.open = false; search.open = true;
    const searchSnapshot = {
      folder: document.querySelector('#searchFolderId')?.value || '',
      secret: document.querySelector('#searchApiKey')?.value || ''
    };
    search.open = false; webmaster.open = true;
    const webmasterSnapshot = {
      user_id: document.querySelector('#webmasterUserId')?.textContent || '',
      secret: document.querySelector('#webmasterOauthToken')?.value || ''
    };
    return { wordstat: wordstatSnapshot, search: searchSnapshot, webmaster: webmasterSnapshot };
  });
  assert.deepEqual(credentialUiAfterRerender, {
    wordstat: { folder: 'browser-word-folder', secret: '' },
    search: { folder: 'browser-search-folder', secret: '' },
    webmaster: { user_id: '321', secret: '' }
  });
  console.log('W15_CREDENTIAL_SWITCH_RERENDER_ISOLATION_PASS');

  const publicCredentials = await send(page, { type: 'YMB_GET_CREDENTIALS' });
  assert.equal(publicCredentials.ok, true);`,
'FINAL_W15_SWITCH'
);

replaceOnce(
`  assert.equal(fetches.every((entry) => entry.has_authorization === true), true);

  console.log('PHASE3_BROWSER_RUNTIME_PASS');`,
`  assert.equal(fetches.every((entry) => entry.has_authorization === true), true);
  assert.equal(fetches.slice(1).every((entry) => entry.webmaster_authorization_exact === true), true);
  assert.equal(JSON.stringify(fetches).includes('browser-valid-oauth'), false);
  assert.equal(JSON.stringify(fetches).includes('browser-invalid-oauth'), false);
  console.log('W05_WEBMASTER_EXACT_OAUTH_HEADER_PASS');

  console.log('PHASE3_BROWSER_RUNTIME_PASS');`,
'FINAL_W05_ASSERT'
);

fs.writeFileSync(target, source);
console.log('PHASE3_FINAL_RUNTIME_HARNESS_PATCH_PASS');
