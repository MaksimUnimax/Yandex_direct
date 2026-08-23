import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../src');
const source=fs.readFileSync(path.join(root,'content_script.js'),'utf8');

function fn(name){
  const marker=`function ${name}(`;
  const start=source.indexOf(marker);
  assert.notEqual(start,-1,`missing function ${name}`);
  let brace=source.indexOf('{',start),depth=0,string=null,escape=false;
  for(let i=brace;i<source.length;i++){
    const c=source[i];
    if(string){if(escape){escape=false;continue;}if(c==='\\'){escape=true;continue;}if(c===string)string=null;continue;}
    if(c==='"'||c==="'"||c==='`'){string=c;continue;}
    if(c==='{')depth++;
    if(c==='}'&&--depth===0)return source.slice(start,i+1);
  }
  throw new Error(`unterminated ${name}`);
}

test('Autorun transport failure releases local seen marker so an unaccepted command can be retried safely',()=>{
  const scan=fn('scanAutorun');
  const catchIndex=scan.indexOf('.catch((error)');
  assert.ok(catchIndex>=0,'scanAutorun transport catch is missing');
  const catchBody=scan.slice(catchIndex);
  assert.match(catchBody,/autorunSeen\.delete\(turnId\)/);
  assert.ok(catchBody.indexOf('autorunSeen.delete(turnId)') < catchBody.indexOf('setStatus('),'seen marker must be released immediately on transport failure');
});
