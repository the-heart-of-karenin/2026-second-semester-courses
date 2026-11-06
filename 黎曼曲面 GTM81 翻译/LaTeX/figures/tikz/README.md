# TikZ插图

fig01.tex—fig06.tex是六幅插图的可编辑主文件，使用standalone文档类。

在项目根目录运行：

- `python tools/build_figures.py`：编译六幅插图，更新上级目录中的fig01-tikz.pdf—fig06-tikz.pdf。
- `python tools/build.py`：先编译六幅图，再编译整本译稿。

原图裁剪PDF仍保留在上级目录的fig01.pdf—fig06.pdf；正文引用的是带-tikz后缀的重绘图。
