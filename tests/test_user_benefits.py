from pathlib import Path
import importlib.util, unittest, tempfile, subprocess, sys, json, zipfile, io, struct, os
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

class AnchorErrors(unittest.TestCase):
    def setUp(self): self.m=load('anchors',ROOT/'scripts/check_anchor.py')
    def test_syntax_error_is_not_counterexample_proof(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'m.py').write_text('VALUE=2\n')
            report=self.m.verify(d,'m.py','VALUE=2','VALUE=(',[sys.executable,'-c','assert True'])
            self.assertEqual(report['status'],'FAIL'); self.assertIn('syntax',report['reason'])
    def test_string_command_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'m.py').write_text('VALUE=2\n')
            with self.assertRaises(ValueError): self.m.verify(d,'m.py','VALUE=2','VALUE=1','python -m unittest')
    def test_timeout_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'m.py').write_text('VALUE=2\n')
            with self.assertRaises(subprocess.TimeoutExpired): self.m.verify(d,'m.py','VALUE=2','VALUE=1',[sys.executable,'-c','import time;time.sleep(1)'],timeout=.05)

if __name__=="__main__": unittest.main()
