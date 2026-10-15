"""Run a rollback counterexample in a temporary copy; never mutate the source tree."""
import argparse
import ast
import json
import os
import re
import math
import sys
from pathlib import Path
import shutil
import subprocess
import tempfile


def verify(root, relative, original, rollback, command, timeout=30, expected_failure=None):
    if expected_failure is not None:
        if not isinstance(expected_failure,str) or not expected_failure.strip(): raise ValueError('expected_failure must be a nonempty regex')
        re.compile(expected_failure)
    root=Path(root).resolve()
    raw_target=root/relative
    if raw_target.is_symlink() or any(p.is_symlink() for p in raw_target.parents if p != root.parent):
        raise ValueError('symlink source is not supported')
    if not isinstance(command,list) or not command or not all(isinstance(x,str) for x in command):
        raise ValueError('command must be a nonempty argv array')
    command=[sys.executable if index==0 and value=='{python}' else value for index,value in enumerate(command)]
    if type(timeout) not in {int,float} or not math.isfinite(timeout) or timeout <= 0: raise ValueError('timeout must be positive')
    target=raw_target.resolve()
    if not target.is_relative_to(root) or not target.is_file():
        raise ValueError('target must be a file inside root')
    text=target.read_text(encoding='utf-8')
    if not original or text.count(original)!=1 or original==rollback:
        raise ValueError('anchor must match exactly once and change the source')
    mutated=text.replace(original,rollback,1)
    if target.suffix == '.py':
        try: ast.parse(mutated)
        except SyntaxError: return {'status':'FAIL','reason':'rollback contains invalid Python syntax'}
    for parent,dirs,files in os.walk(root,followlinks=False):
        dirs[:]=[d for d in dirs if d not in {'.git','.venv','node_modules','__pycache__'} and not d.lower().endswith('profile')]
        if any((Path(parent)/entry).is_symlink() for entry in dirs+files):
            raise ValueError('project symlinks are not supported')
    with tempfile.TemporaryDirectory(prefix='assertion-anchor-') as tmp:
        copied=Path(tmp)/'project'
        shutil.copytree(root,copied,ignore=shutil.ignore_patterns('.git','.env','.env.*','*profile*','__pycache__','.venv','node_modules'),symlinks=True)
        def run():
            env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'
            result=subprocess.run(command,cwd=copied,capture_output=True,timeout=timeout,env=env)
            return result.returncode, (result.stdout+result.stderr).decode('utf-8',errors='replace')
        baseline,_=run()
        if baseline: return {'status':'FAIL','reason':'baseline failed'}
        mutation=copied/target.relative_to(root)
        # Refuse symlink paths so a temporary mutation cannot change the original.
        if not mutation.resolve().is_relative_to(copied.resolve()) or any(p.is_symlink() for p in [mutation,*mutation.parents]):
            raise ValueError('symlink target is not supported')
        mutation.write_text(mutated,encoding='utf-8')
        rolled_back,rollback_output=run()
        mutation.write_text(text,encoding='utf-8')
        restored,_=run()
        matched=bool(re.search(expected_failure,rollback_output)) if expected_failure else None
        return {'status':'PASS' if rolled_back==1 and restored==0 and matched is not False else 'FAIL',
                'expected_failure_matched':matched,'evidence_level':'EXPECTED_FAILURE_PATTERN' if expected_failure else 'EXIT_CODES_ONLY',
                'baseline':baseline,'rollback':rolled_back,'restored':restored}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True)
    parser.add_argument('--anchor',required=True,help='JSON: file, original, rollback, command (argv array)')
    args=parser.parse_args()
    try:
        anchor=json.loads(Path(args.anchor).read_text(encoding='utf-8'))
        result=verify(args.root,anchor['file'],anchor['original'],anchor['rollback'],anchor['command'],timeout=anchor.get('timeout',30),expected_failure=anchor.get('expected_failure'))
    except (ValueError,KeyError,OSError,subprocess.TimeoutExpired,re.error) as exc:
        print(json.dumps({'status':'ERROR','reason':type(exc).__name__})); return 2
    print(json.dumps(result)); return 0 if result['status']=='PASS' else 1


if __name__=='__main__': raise SystemExit(main())
