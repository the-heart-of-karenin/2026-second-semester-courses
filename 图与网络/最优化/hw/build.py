from pathlib import Path
import re, shutil, subprocess
from pypdf import PdfReader
B = Path(__file__).resolve().parent
s = (B / "chapter13.tex").read_text(encoding="utf-8")
n = re.findall(r"\\st\{(?:定义|定理|命题|引理|推论)(\d+)", s)
assert list(map(int,n)) == list(range(1,35)), n
assert "第13章习题}" not in s
subprocess.run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "-outdir=build", "main.tex"], cwd=B, check=True)
pdf = B / "build/main.pdf"
assert all((p.extract_text() or "").strip() for p in PdfReader(pdf).pages)
shutil.copy2(pdf, B / "output/拟阵学习笔记.pdf")
