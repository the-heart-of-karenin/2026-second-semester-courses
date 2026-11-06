# 第13、14章完整中文译本

原书：Bernhard Korte 与 Jens Vygen，*Combinatorial Optimization: Theory and Algorithms*，第三版。

范围：原书第291—342页；第322页为空白。译本含两章完整正文、全部证明、算法、三幅示意图、25+14道习题及两章完整参考文献。书目作者、题名、出版信息保留原文。原书中的跨章引用保留，因此引用到的其他章节不包含在本文件中。没有添加习题解答。

## 文件

- `output/组合优化_第13-14章_完整中文译本.pdf`：独立中文 PDF。
- `main.tex`、`chapter13.tex`、`chapter14.tex`：可编辑的完整 LaTeX 源码。
- `prepare_references.py`：从 `source/` 中逐页提取的原书书目重建参考文献。
- `build.py`：重建参考文献、检查51个非空白原文页和60个陈述编号、编译并导出 PDF。
- `source/`：对应原书页码的提取文本，保留用于对照及重建书目；公式的正确排版请以原书 PDF 为准。
- `build/validation.json`：最后一次构建的覆盖与排版检查结果。

## 重新构建

需要 Python（含 pypdf）、TeX Live/MiKTeX、XeLaTeX 和 latexmk。Windows 下使用 ctex 的系统宋体、黑体、楷体等字体。进入本文件夹运行：

```powershell
python build.py
```

也可以直接编译：

```powershell
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

逐页译文保留原书页码标记和PDF书签；中文内容根据版面可能跨越多个译本页。公式重新录入为数学源码，三幅原理图以 TikZ 重绘。

此译本是基于所提供第三版原文的学习用译稿，不是更新版教材。原书的算法年代、复杂度叙述、问题条件和习题陈述按该版保留；明显缺失的公式括号及秩函数定义域等排印问题在重排时补齐。
