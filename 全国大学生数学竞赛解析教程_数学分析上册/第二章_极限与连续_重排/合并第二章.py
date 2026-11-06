from pathlib import Path
import re


folder = Path(__file__).resolve().parent
parts = [
    folder / "第二章_2.1极限.tex",
    folder / "第二章_2.2连续性.tex",
    folder / "第二章_2.4真题选讲.tex",
]

first = parts[0].read_text(encoding="utf-8")
preamble = first.split(r"\begin{document}", 1)[0]
bodies = []
for path in parts:
    source = path.read_text(encoding="utf-8")
    body = source.split(r"\begin{document}", 1)[1].rsplit(r"\end{document}", 1)[0]
    body = body.replace("\\section*{第2章 极限与连续}", "", 1).strip()
    if path.name.startswith("第二章_2.4"):
        body = re.sub(
            r"\\ex\{(2\.4\.\d+)\}\{([^{}]*)\}",
            r"\\ex{\1}（\2）",
            body,
        )
    bodies.append(body)

output = (
    preamble
    + "\\begin{document}\n"
    + "\\section*{第2章 极限与连续}\n"
    + "\n\\clearpage\n".join(bodies)
    + "\n\\end{document}\n"
)
(folder / "第二章_极限与连续.tex").write_text(output, encoding="utf-8")
