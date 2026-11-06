"""Build both PDFs in an ASCII-only temporary folder; source stays in this folder."""
from pathlib import Path
import shutil, subprocess, tempfile, sys

root=Path(__file__).resolve().parent
work=Path(tempfile.gettempdir())/'codex-ode-midterm-31'
work.mkdir(parents=True,exist_ok=True)
engine=shutil.which('xelatex')
if not engine: raise RuntimeError('XeLaTeX is required.')
for name in ['preamble.tex','review.tex','training.tex']:
    shutil.copy2(root/name,work/name)
for stem,target in [('review','期中考试复习重点_截止3.1.pdf'),('training','期中训练题67题_截止3.1.pdf')]:
    if len(sys.argv)>1 and stem not in sys.argv[1:]: continue
    logs=root/'build'/stem
    logs.mkdir(parents=True,exist_ok=True)
    # Two passes resolve the table of contents and internal references.
    for run in range(2):
        result=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error',stem+'.tex'],cwd=work,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (logs/f'compile-{run+1}.txt').write_bytes(result.stdout)
        if result.returncode:
            raise RuntimeError(f'{stem} failed; inspect {logs}')
    shutil.copy2(work/(stem+'.pdf'),root.parent/target)
    for suffix in ['log','aux','toc','out']:
        p=work/(stem+'.'+suffix)
        if p.exists(): shutil.copy2(p,logs/p.name)
    print('Built '+stem)
