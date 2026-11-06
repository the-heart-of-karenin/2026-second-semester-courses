# 复分析第5次作业

- 原件：`HW5.pdf`。
- 答案：`第05次作业答案.pdf`；修改入口为 `源码/main.tex`。
- 题干保留英文，解答为中文。
- 第三题第一问按用户要求暂不证明，作为已知定理使用；第二问直接引用第一问，用去掉奇点的差商函数证明。
- 用户提供的课堂定义与定理截图保存在 `参考资料/同调形式的Cauchy定理.png`。
- 第二题使用 Morera 定理及小三角形剖分，说明公共边界处的拼接；第四题依题面列出有限个全部原像的条件证明，不额外假设存在全局全纯对数。

本次没有向总作业记录添加题目或疑问。

## 编译

使用 XeLaTeX。由于课程路径含中文，先把 `源码/main.tex` 复制到 `%TEMP%/codex-latex/complex-hw05/homework.tex`，在该纯英文临时目录运行 `xelatex -interaction=nonstopmode -halt-on-error homework.tex`。成功后把 `homework.pdf` 复制为本目录的 `第05次作业答案.pdf`，日志等中间文件保存在 `源码/build/`。本次实际使用 TeX Live 2026。
