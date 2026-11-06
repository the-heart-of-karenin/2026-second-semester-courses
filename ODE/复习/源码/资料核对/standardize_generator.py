from pathlib import Path
p=Path('ODE/复习/源码/make_training.py');s=p.read_text(encoding='utf-8')
s=s.replace('problems = revise(problems)','from standard_questions import standardize\nproblems = standardize(revise(problems))')
a=s.index(r'\textbf{修订说明。}');b=s.index(r'\begingroup\small',a)
s=s[:a]+r'''\textbf{范围与构成。}考试范围截止第 3.1 节（含）。全册 50 题：概念辨析 6 题、代表计算 14 题、基本定理证明 18 题、首次积分综合 6 题、教材应用 6 题。不附答案。
+
+\textbf{符号约定。}除另有规定外，$I$ 为非空开区间，未知向量 $x$ 取值于 $\R^n$，$I_n$ 为 $n$ 阶单位矩阵；$|\cdot|$ 为向量范数，$\|\cdot\|$ 为其诱导矩阵范数。线性相关或无关均指以常数为系数的向量函数关系。函数独立性按对状态变量的 Jacobi 矩阵秩判定。
+
+\textbf{来源。}“2025 卷”指所提供、卷首标有上海交通大学致远班 2025--2026 学年第一学期期中试卷的照片；“2023 卷”指所提供、署编者史瑞普的 2023--2024 学年第一学期试题及部分答案整理稿。教材为《微分方程 I（101 计划）》，习题集为博亚尔丘克、戈洛瓦奇《高等数学例题与习题集（四）常微分方程》。题面按本册要求统一，原题来源与改编标记见各题。
+
+\textbf{页码。}所选习题集题目 PDF 页＝印刷页＋8；教材 PDF 页＝印刷页＋10。试卷按大题、小题号定位。
+
+'''.replace('\n+','\n')+s[b:]
s=s.replace('真题导向修订版 · 截止','标准题面版 · 截止')
s=s.replace("return s.replace(r'\\prime'", "s=s.replace('（1）',r'\\par（1）').replace('（2）',r'\\par（2）').replace('（3）',r'\\par（3）').replace('（4）',r'\\par（4）')\n    return s.replace(r'\\prime'")
p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/build.py');s=p.read_text(encoding='utf-8');s=s.replace('import shutil, subprocess, tempfile','import shutil, subprocess, tempfile, sys');s=s.replace("    logs=root/'build'/stem", "    if len(sys.argv)>1 and stem not in sys.argv[1:]: continue\n    logs=root/'build'/stem");p.write_text(s,encoding='utf-8')
