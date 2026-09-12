"""QA for the exact package guard; does not execute or install the extension.
Usage: b14_package_test.py QUALIFICATION_OUTPUT [SOURCE_REPO]
"""
import copy, importlib.util, io, json, shutil, sys, tempfile, unittest, warnings, zipfile
from pathlib import Path
sys.dont_write_bytecode=True
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('b14_qualify',here/'b14_qualify.py');q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
root=Path(sys.argv.pop(1)).absolute()
repo=Path(sys.argv.pop(1)).absolute() if len(sys.argv)>1 else None
artifact=root/'payload/candidate-internal-qa.zip'
source=q.inventory(root/'fresh_qa/candidate/full')
class PackageGuards(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.work=Path(self.tmp.name)
    def mutant(self, fn):
        p=self.work/'mutant.zip'
        with zipfile.ZipFile(artifact) as before,zipfile.ZipFile(p,'w') as after:
            entries=[(copy.copy(i),before.read(i)) for i in before.infolist()]
            fn(entries,after)
            for i,b in entries: after.writestr(i,b)
        return p
    def reject_structure(self,p):
        with self.assertRaises((ValueError,zipfile.BadZipFile)): q.verify_package(p,source,None,None)
    def test_01_full_path_and_byte_identity(self): self.assertEqual(q.verify_package(artifact,source),source)
    def test_02_repeated_pack_identical(self): self.assertEqual(artifact.read_bytes(),(root/'work/repeat.zip').read_bytes())
    def test_03_baseline_not_needed_from_user(self):
        self.assertTrue(repo is not None);base,packer=q.load_inputs(repo);self.assertEqual(len(base),53);self.assertEqual(q.sha(packer),q.PACKER_SHA)
    def test_04_tampered_zip_rejected(self):
        b=bytearray(artifact.read_bytes());b[len(b)//2]^=1;p=self.work/'bad.zip';p.write_bytes(b)
        with self.assertRaises(ValueError):q.verify_package(p,source)
    def test_05_truncated_zip_rejected(self):
        p=self.work/'truncated.zip';p.write_bytes(artifact.read_bytes()[:-10])
        with self.assertRaises(ValueError):q.verify_package(p,source)
    def test_06_extra_traversal_path_rejected(self):
        self.reject_structure(self.mutant(lambda e,z:e.append((zipfile.ZipInfo('../escaped.js'),b'x'))));self.assertFalse((self.work.parent/'escaped.js').exists())
    def test_07_duplicate_path_rejected(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore');p=self.mutant(lambda e,z:e.append(e[-1]))
        self.reject_structure(p)
    def test_08_member_bytes_rejected(self):
        def mutate(e,z):e[-1]=(e[-1][0],b'X'+e[-1][1][1:])
        self.reject_structure(self.mutant(mutate))
    def test_09_permission_metadata_rejected(self):
        def mutate(e,z):e[-1][0].external_attr=0o100777<<16
        self.reject_structure(self.mutant(mutate))
    def test_10_comment_metadata_rejected(self): self.reject_structure(self.mutant(lambda e,z:setattr(z,'comment',b'unexpected')))
    def test_11_wrong_source_refused(self):
        s=dict(source);s['README.txt']+=b'\n'
        with self.assertRaises(ValueError):q.verify_package(artifact,s)
    def test_12_symlink_tree_refused(self):
        (self.work/'alias').symlink_to(artifact)
        with self.assertRaises(ValueError):q.inventory(self.work)
    def test_13_source_unchanged_and_no_permission_activation(self):
        self.assertEqual(q.identity(source),q.TARGET)
        self.assertNotIn('https://operation.api.cloud.yandex.net/*',json.loads(source['manifest.json'])['host_permissions'])
        self.assertFalse(json.loads((root/'payload/PACKAGE_IDENTITY.json').read_text())['release_allowed'])
    def test_14_all_preserved_QA_inputs_present(self):
        m=json.loads((repo/q.WIP/'evidence/B13_INPUTS.json').read_text())
        for n,h in m['qa_archive_members'].items():self.assertEqual(q.sha((root/'fresh_qa'/n).read_bytes()),h,n)
if __name__=='__main__':unittest.main(verbosity=2)
