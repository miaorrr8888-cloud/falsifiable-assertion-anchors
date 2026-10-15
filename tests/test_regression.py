from pathlib import Path
import importlib.util, unittest, tempfile, subprocess, sys, json, zipfile, io, os
R=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

class Anchors(unittest.TestCase):
    def test_counterexample_and_source_preserved(self):
        m=load('anchor',R/'scripts/check_anchor.py')
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'value.py'; p.write_text('VALUE=2\n')
            result=m.verify(d,'value.py','VALUE=2','VALUE=1',[sys.executable,'-c','import value; assert value.VALUE==2'])
            self.assertEqual(result['status'],'PASS'); self.assertEqual(p.read_text(),'VALUE=2\n')
    def test_tautology_fails(self):
        m=load('anchor',R/'scripts/check_anchor.py')
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'value.py').write_text('VALUE=2\n')
            self.assertEqual(m.verify(d,'value.py','VALUE=2','VALUE=1',[sys.executable,'-c','assert True'])['status'],'FAIL')
    def test_missing_anchor_rejected(self):
        m=load('anchor',R/'scripts/check_anchor.py')
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'value.py').write_text('VALUE=2\n')
            with self.assertRaises(ValueError): m.verify(d,'value.py','VALUE=3','VALUE=1',[sys.executable,'-c','assert True'])

if __name__=="__main__": unittest.main(verbosity=2)
