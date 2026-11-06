from pathlib import Path
import subprocess,tempfile,shutil,json,sys
r=Path(__file__).resolve().parents[1]
stage=Path(tempfile.gettempdir())/'codex-latex'/'forster-figures';stage.mkdir(parents=True,exist_ok=True)
exe=r'D:\Program Files (x86)\texlive\2026\bin\windows\pdflatex.exe'
results=[]
for p in sorted((r/'LaTeX/figures/tikz').glob('fig*.tex')):
 shutil.copy2(p,stage/p.name)
 q=subprocess.run([exe,'-interaction=nonstopmode','-halt-on-error',p.name],cwd=stage,capture_output=True)
 log=q.stdout.decode('utf-8',errors='replace')+q.stderr.decode('utf-8',errors='replace')
 (r/'source/redraw-review'/f'{p.stem}-build.log').write_text(log,encoding='utf-8')
 if q.returncode:
  print(log[-5000:]);sys.exit(q.returncode)
 shutil.copy2(stage/f'{p.stem}.pdf',r/f'LaTeX/figures/{p.stem}-tikz.pdf')
 results.append(p.stem)
print(json.dumps({'success':True,'figures':results}))
