"""B18 QA-only assembler. Consumes ready B17 + ready cleanup artifacts, NOT code patches.
Usage: b18_prepare.py READY_B17 READY_CLEANUP NEW_OUTPUT
Does not rebuild a product or grant acceptance. Every product byte is verified.
"""
from pathlib import Path, PurePosixPath
import hashlib, json, shutil, sys, zipfile
H=lambda b:hashlib.sha256(b).hexdigest()
TARGET='b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508'
ZIP_SHA='1560599adfcfdb2c3180ec9103005b1584bcd39709b8fc45e233f6c1bdd11ee1'

def members(folder):
 for line in (folder/'SHA256SUMS').read_text().splitlines():
  h,n=line.split('  ',1);p=PurePosixPath(n)
  if p.is_absolute() or '..' in p.parts or H((folder/n).read_bytes())!=h:raise ValueError('Member mismatch '+n)

def main():
 if len(sys.argv)!=4:raise SystemExit(__doc__)
 b,r,out=[Path(p).resolve() for p in sys.argv[1:]]
 if out.exists():raise ValueError('Refuse existing output')
 members(b);members(r)
 z=b/'candidate-b17-internal.zip'
 if z.stat().st_size!=225660 or H(z.read_bytes())!=ZIP_SHA:raise ValueError('Not ready B17 package')
 with zipfile.ZipFile(z) as a:
  if a.testzip() is not None:raise ValueError('CRC failure')
  files={}
  for e in a.infolist():
   if e.is_dir():continue
   p=PurePosixPath(e.filename)
   if p.is_absolute() or '..' in p.parts or len(p.parts)<2:raise ValueError('Unsafe package')
   n='/'.join(p.parts[1:])
   if n in files:raise ValueError('Duplicate file')
   files[n]=a.read(e)
 if len(files)!=67 or H(''.join(H(v)+'  '+n+'\n' for n,v in sorted(files.items())).encode())!=TARGET:raise ValueError('Tree mismatch')
 source=(b/'tests/b16.generated.mjs').read_bytes();cleanup=(r/'remaining.mjs').read_bytes()
 # Precise retained QA inputs. No new launch semantics and no weakened product assertions.
 expected={'b16.generated.mjs':'7505a79f955673c7f122b18c0c64ee3dd49de3696d27dbdfb92c3ee9fce49390','remaining.mjs':'2e22bdfdae17b2302701da02db483bcab8509a618abf759a7d2457e1ffec0501'}
 if H(source)!=expected['b16.generated.mjs'] or H(cleanup)!=expected['remaining.mjs']:raise ValueError('Unknown helper bytes')
 prefix=source.decode().split('try{\n await launchOwned();',1)[0]
 tail=cleanup.decode().split('finally {\n clearInterval(monitor); clearTimeout(deadline);',1)
 if len(tail)!=2:raise ValueError('Unknown cleanup boundary')
 tail='finally {\n clearInterval(monitor); clearTimeout(deadline);'+tail[1]
 body=(Path(__file__).parent/'b18_missing_browser_cases.js').read_text()
 script=prefix+body+'\n'+tail
 out.mkdir()
 for n,v in files.items():p=out/'candidate'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(v)
 tests=out/'tests';tests.mkdir()
 (tests/'b18.generated.mjs').write_text(script)
 shutil.copyfile(b/'tests/b15_fixture.html',tests/'b15_fixture.html')
 shutil.copyfile(b/'package-lock.json',out/'package-lock.json')
 shutil.copyfile(z,out/'candidate-b17-internal.zip')
 evidence={'candidate':TARGET,'zip':ZIP_SHA,'files':67,'product_modified':False,'source_prequel':H(source),'cleanup':H(cleanup),'body':H(body.encode()),'generated':H(script.encode()),'independent_gate':False,'release_allowed':False}
 (out/'IDENTITY.json').write_text(json.dumps(evidence,indent=2)+'\n')
 print(json.dumps(evidence))
if __name__=='__main__':main()
