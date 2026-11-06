# LaTeX 源码

`main.tex` 是编译入口。使用 XeLaTeX 编译两遍以生成目录。

- `ch01-opening.tex`：人工转写的第一章开头，原书第 3–8 页至例 1.2.5 和题型一总结。
- `full-ch01.tex` 至 `full-ch06.tex`：六章正文。
- `full-preface.tex`、`full-references.tex`：前言、资源使用说明和参考文献。
- `images-full/`：尚未转成可编辑公式的局部原图，以及原书图形。编译依赖这些文件，请与源码一起保留。
- `局部原图位置清单.json`：每张局部图在原 PDF 中的页面及裁切坐标，供后续逐处转写时定位。

采用 A4 纸、约 2.45 厘米页边距、中文正文和数学排版。当前字体使用 Windows 的宋体、Times New Roman 与 Segoe UI Symbol；其他系统可按可用字体调整主文件中的字体设置。

Windows 中文路径建议先把这套源码及图片复制到纯英文路径，再编译 `main.tex`，成功后将 PDF 复制回原目录。

本稿是重排初稿，包含大量局部原图，并非所有公式都已变成可编辑 LaTeX。请不要只复制 `.tex` 文件而遗漏图片目录。
