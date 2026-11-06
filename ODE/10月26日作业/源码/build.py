from pathlib import Path
import shutil, subprocess, tempfile

root = Path(__file__).resolve().parent
work = Path(tempfile.gettempdir()) / 'codex-ode-hw1026'
work.mkdir(parents=True, exist_ok=True)
shutil.copy2(root / 'main.tex', work / 'main.tex')
logs = root / 'build'
logs.mkdir(exist_ok=True)
for i in range(2):
    p = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', 'main.tex'], cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (logs / f'compile-{i+1}.txt').write_bytes(p.stdout)
    if p.returncode:
        raise RuntimeError(f'Compilation failed; see {logs}')
shutil.copy2(work / 'main.pdf', root.parent / '10月26日作业答案.pdf')
shutil.copy2(work / 'main.log', logs / 'main.log')
print('Built 1026')
