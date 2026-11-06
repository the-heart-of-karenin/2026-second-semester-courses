"""Compile the standalone integral notes in an ASCII-only temporary directory."""
from pathlib import Path
import shutil, subprocess, tempfile

src = Path(__file__).resolve().parent
name = '积分分类与Bernoulli换元限制'
work = Path(tempfile.gettempdir()) / 'codex-ode-integral-notes'
work.mkdir(parents=True, exist_ok=True)
logs = src / 'build' / 'integral-notes'
logs.mkdir(parents=True, exist_ok=True)
shutil.copy2(src / (name + '.tex'), work / 'main.tex')
engine = shutil.which('xelatex')
if not engine:
    raise RuntimeError('XeLaTeX is required.')
for run in range(2):
    result = subprocess.run([engine, '-interaction=nonstopmode', '-halt-on-error', 'main.tex'], cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (logs / f'compile-{run+1}.txt').write_bytes(result.stdout)
    if result.returncode:
        raise RuntimeError('Compilation failed; inspect ' + str(logs))
shutil.copy2(work / 'main.pdf', src.parent / (name + '.pdf'))
shutil.copy2(work / 'main.log', logs / 'main.log')
print('Built integral notes.')
