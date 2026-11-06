from pathlib import Path
import json,re,shutil,subprocess
from pypdf import PdfReader
B=Path(__file__).resolve().parent
tex='\n'.join((B/f'section7{i}.tex').read_text(encoding='utf-8') for i in range(1,6))
expected=[f'7.{s}.{n}' for s,k in [(2,6),(3,7),(4,8),(5,8)] for n in range(1,k+1)]
actual=re.findall(r'\\st\{(?:例|命题|定理|引理|推论)(7\.\d+\.\d+)',tex)
assert actual==expected,(actual,expected)
assert re.findall(r'\\tag\{(7\.\d+)\}',tex)==[f'7.{i}' for i in range(1,27)]
result=subprocess.run(['latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error','-outdir=build','main.tex'],cwd=B,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(B/'build/console.log').write_bytes(result.stdout)
if result.returncode:
 print(result.stdout.decode('utf-8',errors='replace')[-4000:]); raise SystemExit(result.returncode)
log=(B/'build/main.log').read_text(encoding='utf-8',errors='replace')
warnings=[x for x in log.splitlines() if any(k in x for k in ['Overfull','Missing character:','undefined references'])]
pdf=B/'build/main.pdf'; pages=PdfReader(pdf).pages
assert all((p.extract_text() or '').strip() for p in pages)
out=B/'output/pdf/Bjorner_拟阵与几何格的同调及可壳性_7.1-7.5附解释版.pdf'
shutil.copy2(pdf,out)
report=dict(pages=len(pages),numbered_items=len(expected),equations=26,figures=4,warnings=warnings,output=str(out))
(B/'build/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
