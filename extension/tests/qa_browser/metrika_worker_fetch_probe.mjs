import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createHash, generateKeyPairSync } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer';

const here = path.dirname(fileURLToPath(import.meta.url));
const source = fs.realpathSync(path.resolve(here, '../../src'));
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'ymb-m4-worker-probe-'));
const ext = path.join(tmp, 'extension');
fs.cpSync(source, ext, { recursive: true });
const { publicKey } = generateKeyPairSync('rsa', { modulusLength: 2048, publicKeyEncoding: { type: 'spki', format: 'der' }, privateKeyEncoding: { type: 'pkcs8', format: 'pem' } });
const digest = createHash('sha256').update(publicKey).digest().subarray(0, 16);
let extensionId = '';
for (const byte of digest) extensionId += String.fromCharCode(97 + ((byte >> 4) & 15), 97 + (byte & 15));
const manifestPath = path.join(ext, 'manifest.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
manifest.key = Buffer.from(publicKey).toString('base64');
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));

const browser = await puppeteer.launch({ headless: false, pipe: true, enableExtensions: true, args: ['--no-sandbox','--disable-gpu','--disable-dev-shm-usage',`--disable-extensions-except=${ext}`,`--load-extension=${ext}`] });
try {
  const target = await browser.waitForTarget((t) => t.type() === 'service_worker' && t.url().startsWith(`chrome-extension://${extensionId}/`), { timeout: 15000 });
  const client = await target.createCDPSession();
  async function probe(name, expression) {
    const r = await client.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    const detail = r.exceptionDetails ? {
      text: r.exceptionDetails.text || '',
      description: r.exceptionDetails.exception?.description || '',
      value: r.exceptionDetails.exception?.value,
      lineNumber: r.exceptionDetails.lineNumber,
      columnNumber: r.exceptionDetails.columnNumber
    } : null;
    console.log(`M4_WORKER_PROBE_${name}`, JSON.stringify({ value: r.result?.value, type: r.result?.type, detail }));
    if (detail) throw new Error(`${name}: ${detail.description || detail.text}`);
    return r.result?.value;
  }
  await probe('GLOBALS', `({fetch:typeof fetch,Response:typeof Response,Headers:typeof Headers,descriptor:(()=>{const d=Object.getOwnPropertyDescriptor(globalThis,'fetch');return d?{writable:d.writable,configurable:d.configurable,hasSet:typeof d.set==='function'}:null})()})`);
  await probe('ARRAY', `(()=>{globalThis.__YMB_M4_FETCHES=[];return Array.isArray(globalThis.__YMB_M4_FETCHES)})()`);
  await probe('ASSIGN_SIMPLE_FETCH', `(()=>{globalThis.fetch=async()=>new Response('{}',{status:200});return typeof globalThis.fetch})()`);
  await probe('REGEX', `(()=>({auth:/^OAuth [^\\s].*$/.test('OAuth token'),route:/\\/management\\/v1\\/counter\\/123(?:\\?|$)/.test('/management/v1/counter/123')}))()`);
  await probe('FULL_STUB', `(() => {
    globalThis.__YMB_M4_FETCHES = [];
    globalThis.fetch = async (url, options = {}) => {
      const target = String(url || '');
      const method = String(options.method || 'GET').toUpperCase();
      const headers = options.headers || {};
      let auth = '';
      try {
        if (headers instanceof Headers) auth = headers.get('Authorization') || '';
        else { const key = Object.keys(headers).find((name) => String(name).toLowerCase() === 'authorization'); auth = key ? String(headers[key] || '') : ''; }
      } catch {}
      globalThis.__YMB_M4_FETCHES.push({ url: target, method, has_authorization: auth.startsWith('OAuth ') && auth.length > 6, auth_scheme_exact: /^OAuth [^\\s].*$/.test(auth) });
      const json = (value, status = 200) => new Response(JSON.stringify(value), { status, headers: { 'Content-Type': 'application/json' } });
      if (!target.startsWith('https://api-metrika.yandex.net/')) throw new Error('CONTROLLED_BROWSER_UNEXPECTED_PROVIDER_HOST');
      if (target.includes('/management/v1/counters?per_page=1')) return json({ rows: 0, counters: [] });
      if (target.includes('/management/v1/counters?')) return json({ rows: 1, counters: [] });
      if (target.includes('/stat/v1/data?')) return json({ totals: [12,8,30] });
      if (target.includes('/stat/v1/data/bytime?')) return json({ data: [] });
      if (/\\/management\\/v1\\/counter\\/123(?:\\?|$)/.test(target)) return json({ counter: { id: 123 } });
      throw new Error('CONTROLLED_BROWSER_UNEXPECTED_METRIKA_ROUTE');
    };
    return true;
  })()`);
  console.log('PHASE4_METRIKA_WORKER_FETCH_PROBE_PASS');
} finally {
  await browser.close();
  fs.rmSync(tmp, { recursive: true, force: true });
}
