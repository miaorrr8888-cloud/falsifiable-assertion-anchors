"""Run a rollback counterexample in a temporary copy; never mutate the source tree."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def verify(root, relative, original, rollback, command, timeout=30):
    root=Path(root).resolve()
    target=(root/relative).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        raise ValueError('target must be a file inside root')
    text=target.read_text(encoding='utf-8')
    if not original or text.count(original)!=1 or original==rollback:
        raise ValueError('anchor must match exactly once and change the source')
    with tempfile.TemporaryDirectory(prefix='assertion-anchor-') as tmp:
        copied=Path(tmp)/'project'
        shutil.copytree(root,copied,ignore=shutil.ignore_patterns('.git','.env','.env.*','*profile*','__pycache__','.venv','node_modules'),symlinks=True)
        def run():
            env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'
            result=subprocess.run(command,cwd=copied,capture_output=True,timeout=timeout,env=env)
            return result.returncode
        baseline=run()
        if baseline: return {'status':'FAIL','reason':'baseline failed'}
        mutation=copied/target.relative_to(root)
        # Refuse symlink paths so a temporary mutation cannot change the original.
        if not mutation.resolve().is_relative_to(copied.resolve()) or any(p.is_symlink() for p in [mutation,*mutation.parents]):
            raise ValueError('symlink target is not supported')
        mutation.write_text(text.replace(original,rollback,1),encoding='utf-8')
        rolled_back=run()
        mutation.write_text(text,encoding='utf-8')
        restored=run()
        return {'status':'PASS' if rolled_back==1 and restored==0 else 'FAIL',
                'baseline':baseline,'rollback':rolled_back,'restored':restored}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True)
    parser.add_argument('--anchor',required=True,help='JSON: file, original, rollback, command (argv array)')
    args=parser.parse_args()
    anchor=json.loads(Path(args.anchor).read_text(encoding='utf-8'))
    result=verify(args.root,anchor['file'],anchor['original'],anchor['rollback'],anchor['command'])
    print(json.dumps(result)); return 0 if result['status']=='PASS' else 1


if __name__=='__main__': raise SystemExit(main())
