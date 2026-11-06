from pathlib import Path
import shutil
import subprocess
import tempfile

source = Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='codex-ode-reader-') as directory:
    work = Path(directory)
    shutil.copy2(source / '小作文2.tex', work / 'main.tex')
    subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', 'main.tex'],
                   cwd=work, check=True)
    shutil.copy2(work / 'main.pdf', source.parent / '小作文2.pdf')
    (source / 'build').mkdir(exist_ok=True)
    for suffix in ('log', 'aux'):
        shutil.copy2(work / f'main.{suffix}', source / 'build' / f'essay2.{suffix}')
