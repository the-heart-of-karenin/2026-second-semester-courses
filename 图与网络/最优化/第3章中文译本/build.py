"""用 XeLaTeX 编译译本，检查内容标识，并导出 PDF。"""
from pathlib import Path
import json
import re
import shutil
import subprocess
from pypdf import PdfReader

BASE = Path(__file__).resolve().parent
BUILD = BASE / "build"
OUTPUT = BASE / "output" / "组合优化_第3章_完整中文译本.pdf"

def main():
    BUILD.mkdir(exist_ok=True)
    OUTPUT.parent.mkdir(exist_ok=True)
    tex = (BASE / "chapter3.tex").read_text(encoding="utf-8")
    assert list(map(int, re.findall(r"\\srcpage\{(\d+)\}", tex))) == list(range(49, 65))
    numbers = list(map(int, re.findall(r"\\st\{(?:定义|命题|定理|推论|引理)3\.(\d+)", tex)))
    assert numbers == list(range(1, 29)), numbers
    assert re.findall(r"\\tag\{([^}]+)\}", tex) == [f"3.{i}" for i in range(1, 7)]
    run = subprocess.run(
        ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "-outdir=build", "main.tex"],
        cwd=BASE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    (BUILD / "last-build.txt").write_bytes(run.stdout)
    if run.returncode:
        print(run.stdout.decode("utf-8", errors="replace")[-6000:])
        raise SystemExit(run.returncode)
    log = (BUILD / "main.log").read_text(encoding="utf-8", errors="replace")
    warnings = [line for line in log.splitlines() if any(w in line for w in
                ("Overfull", "Missing character:", "undefined references"))]
    reader = PdfReader(BUILD / "main.pdf")
    pages = [p.extract_text() or "" for p in reader.pages]
    assert all(p.strip() for p in pages), "空白页"
    full = "\n".join(pages)
    compact = re.sub(r"\s+", "", full)
    assert all(f"原书第{i}页" in compact for i in range(49, 65))
    assert "�" not in full, "替换字符"
    for number in range(1, 29):
        assert re.search(rf"(?:定义|命题|定理|推论|引理)3\.{number}(?!\d)", compact), number
    start = re.search(r"第\s*3\s*章习题\s*\n1\.", full)
    assert start, "未找到习题正文"
    exercises = full[start.end()-2:]
    exercises = exercises[:exercises.index("章参考文献")]
    labels = re.findall(r"(?m)^\s*(\d+)\.(?!\d)", exercises)
    assert list(map(int, labels)) == list(range(1, 15)), labels
    shutil.copy2(BUILD / "main.pdf", OUTPUT)
    report = dict(pdf_pages=len(pages), source_pages="49–64", numbered_results=28,
                  numbered_equations=6, exercises=14, cited_references=16,
                  general_references=3, warnings=warnings, output=str(OUTPUT))
    (BUILD / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
