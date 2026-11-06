from pathlib import Path
import sys
root=Path(__file__).resolve().parents[1]
p=root/'LaTeX/main.tex';s=p.read_text(encoding='utf-8-sig');n=int(sys.argv[1]);line=f'\\input{{sections/{n:02}.tex}}'
if line not in s:s=s.replace('\\end{document}',line+'\n\\end{document}')
p.write_text(s,encoding='utf-8')
