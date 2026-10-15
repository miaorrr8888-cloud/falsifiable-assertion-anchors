from pathlib import Path
import importlib.util,unittest,tempfile,json,sys,subprocess,os
ROOT=Path(__file__).resolve().parents[1]
def load(path):
    sys.path.insert(0,str(ROOT/'scripts'))
    spec=importlib.util.spec_from_file_location('extension',ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class FailureReason(unittest.TestCase):
    def run_anchor(self,pattern):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'v.py').write_text('VALUE=2\n')
            return load('scripts/check_anchor.py').verify(d,'v.py','VALUE=2','VALUE=1',[sys.executable,'-c','import v; assert v.VALUE==2, "TARGET_VALUE_ASSERTION"'],expected_failure=pattern)
    def test_expected_assertion_passes(self):self.assertEqual(self.run_anchor('TARGET_VALUE_ASSERTION')['status'],'PASS')
    def test_wrong_failure_rejected(self):self.assertEqual(self.run_anchor('DIFFERENT_FAILURE')['status'],'FAIL')
