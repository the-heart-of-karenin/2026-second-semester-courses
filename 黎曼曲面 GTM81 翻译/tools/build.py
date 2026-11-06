from pathlib import Path
import subprocess, shutil, tempfile, json, datetime, re, sys
root=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(root/'tools/build_figures.py')],check=True)
stage=Path(tempfile.gettempdir())/'codex-latex'/'forster-gtm81'
stage.mkdir(parents=True,exist_ok=True)
shutil.copytree(root/'LaTeX',stage,dirs_exist_ok=True)
exe=r'D:\Program Files (x86)\texlive\2026\bin\windows\xelatex.exe'
logs=[]
for run in range(2):
 r=subprocess.run([exe,'-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=stage,capture_output=True)
 logs.append(r.stdout.decode('utf-8',errors='replace')+r.stderr.decode('utf-8',errors='replace'))
 if r.returncode: break
build=root/'LaTeX'/'build'; build.mkdir(exist_ok=True)
(build/'build-console.log').write_text('\n'.join(logs),encoding='utf-8')
for ext in ['log','aux','toc','out']:
 if (stage/f'main.{ext}').exists(): shutil.copy2(stage/f'main.{ext}',build/f'main.{ext}')
record={'time':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'success':r.returncode==0,'scope':'全书：§1—§31、全部习题、附录、参考文献、索引、出版资料及丛书目录','visual_review':False}
with (root/'compile-history.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
if r.returncode==0: shutil.copy2(stage/'main.pdf',root/'黎曼曲面讲义_中文译稿.pdf')
else: print(logs[-1][-6000:])
print(json.dumps(record,ensure_ascii=False))
raise SystemExit(r.returncode)

