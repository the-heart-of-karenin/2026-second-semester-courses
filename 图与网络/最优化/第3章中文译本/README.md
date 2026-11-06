# 第3章《线性规划》完整中文译本

原著：Bernhard Korte、Jens Vygen，*Combinatorial Optimization: Theory and Algorithms*，第三版。

范围：原书印刷第49–64页。包括3.1多面体、3.2单纯形算法、3.3对偶性、3.4凸包与多胞体，全部编号结果及证明、算法、14道习题和参考文献。保留原书编号及原书页码提示。参考文献保留英文著录，不含习题解答。

- `main.tex`：主文件和排版设置。
- `chapter3.tex`：中文正文；通常在这里修改内容。
- `references3.tex`：引用文献。
- `output/组合优化_第3章_完整中文译本.pdf`：编译后的译本。
- `source/`：原书对应页的提取文本及少量核对用图片。
- `build/`：编译中间文件及检查记录。

## 编译

安装含中文字体支持的 TeX Live（XeLaTeX、latexmk）后，在此目录运行：

```text
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

或者在安装了 `pypdf` 的 Python 环境运行 `python build.py`，自动编译、检查编号和习题完整性，并将 PDF 导出到 `output/`。

`extract_source.py 原书.pdf` 可以重新提取原书对应页的文本；它只写入 `source/`，不会修改中文译稿。
