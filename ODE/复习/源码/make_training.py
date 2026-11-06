"""Editable exercise data. Run with Python to regenerate training.tex and sources.csv."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parent
problems = []
def add(group, source, page, topic, text, note=''):
    problems.append(dict(group=group, source=source, page=page, topic=topic, text=text, note=note))

g='A. 基本概念与消去任意常数'
add(g,'引言练习 1',8,'1.2：消去一个常数',r'消去常数，求曲线族的微分方程：\[y-\tan(C_1x)=0.\]')
add(g,'引言练习 3',8,'1.2：消去两个常数',r'消去常数，求曲线族的微分方程：\[\frac{x^2}{1+C_1}+\frac{y^2}{2+C_2}-1=0.\]')
add(g,'引言练习 4',8,'1.2：复合函数族与消元',r'消去常数，求曲线族的微分方程：\[y=C_1\sin\varphi(x)+C_2\cos\varphi(x),\qquad \varphi(x)=\int_0^x f(t)\dd t.\]',r'在所需导数存在的区间讨论；若用到除以 $f(x)$，说明局部非零条件。')

g='B. 分离变量、齐次与线性组合换元'
data=[
(3,r'求解初值问题：\[y\dd x+(\sqrt{xy}-\sqrt{x})\dd y=0,\qquad y(1)=1.\]'),
(7,r'求积分：\[y\prime=\frac yx+e^x\frac{2xy}{x^2+y^2}.\]'),
(8,r'求积分：\[y\prime=\frac yx+\sin x\tan\frac yx.\]'),
(9,r'求积分：\[(2x-4y+6)\dd x+(x+y-3)\dd y=0.\]'),
(10,r'求积分：\[(x+y+4)y\prime=2x+3y-5.\]'),
(12,r'求解初值问题：\[\sin\!\left(\frac{2x+8y-3}{x+4y}\right)\dd y+e^{x+4y+5}\dd x=0,\qquad y(0)=2.\]'),
(13,r'求解初值问题：\[(x^2y^3-y)\dd x-(x^4y^3-2x^3y^2+6x)\dd y=0,\qquad y(1)=1.\]'),
(15,r'求解初值问题：\[xy\prime=y\cos\ln\frac yx,\qquad y(1)=e^{\pi/2}.\]')]
for n,s in data:
    note = (r'原题按 $y(x)$ 的经典 $C^1$ 解理解时，初始点代入得 $1+0\cdot y\prime=0$，条件不相容；若以 $y$ 为参数求 $x(y)$，则可求经过该点的几何曲线。保留原题，注意这两种表述的区别。' if n==3 else '')
    add(g,f'第 1 章练习 {n}',135,'2.1：分离及换元；保留原定义域',s,note)

g='C. 线性、Bernoulli 与 Riccati 方程'
data=[
(16,135,r'y=x(y\prime-x\cos x)'),
(17,135,r'y\prime+y\sin x=\sin x'),
(18,135,r'(xy+e^x)\dd x-x\dd y=0'),
(19,135,r'y\prime=\frac{y}{3x-y^2}'),
(20,135,r'y\prime+2y=e^xy^2'),
(21,135,r'xy\prime-2x^2\sqrt y=4y'),
(22,135,r'y\prime+y\frac{1+x^2}{1+x^3}=e^x'),
(23,136,r'y\prime+y(1+x^2)^{-1}\sin x=\cos x'),
(24,136,r'y\prime+y\tan x=\cos x'),
(25,136,r'y\prime+\frac yx=x'),
(29,136,r'2y\prime=xy+y^2+\frac1{x^2}-3'),
(30,136,r'y\prime=\frac yx-\frac{y^2}{x}+x')]
for n,p,s in data: add(g,f'第 1 章练习 {n}',p,'2.2：识别线性化方法',r'求方程的积分或通解：\['+s+r'.\]')
add(g,'第 1 章练习 31',136,'2.2：Riccati 与积分定解条件',r'求满足所给积分条件的解：\[y\prime-2xy+y^2=5-x^2,\qquad\int_0^1 y(x)\dd x=1.\]')

g='D. 全微分与积分因子'
data=[
(33,r'(1+y^2\sin2x)\dd x-2y\cos^2x\dd y=0'),
(34,r'3x^2(1+\ln y)\dd x=\left(2y-\frac{x^3}{y}\right)\dd y'),
(35,r'\left(\frac{x}{\sin y}+2\right)\dd x+\frac{(x^2+1)\cos y}{\cos2y-1}\dd y=0'),
(36,r'xy^2(xy\prime+1)=1'),
(37,r'(x^2+3\ln y)y\dd x=x\dd y'),
(38,r'(x^2+2x+y)\dd x-(x-3x^2y)\dd y=0'),
(39,r'(x^2-y)\dd x+x(y+1)\dd y=0')]
for n,s in data:
    verb='求全微分方程的积分：' if n<=35 else '选择积分因子，求方程的积分：'
    add(g,f'第 1 章练习 {n}',136,'2.3：势函数或积分因子',verb+r'\['+s+r'.\]')

g='E. 零解、非唯一性与积分等价式'
add(g,'第 1 章练习 40',136,'2.1：平方根与奇解',r'求可能的奇点、曲线和奇解：\[y\prime=\sqrt y.\]',r'另作训练小问：给出 $y(0)=0$ 的全部实 $C^1$ 解，并解释非零支的适用半区间。此小问为新增，非原书原问。')
add(g,'第 1 章练习 41',136,'2.1：立方根与拼接',r'求可能的奇点、曲线和奇解：\[y\prime=\sqrt[3]y.\]',r'另作训练小问：给出 $y(0)=0$ 的解族，核验正负两支及连接点导数。此小问为新增。')
add(g,'第 1 章练习 45',136,'1.3：积分方程与初值问题',r'用化为微分方程的方法解方程：\[y(x)=x+\int_0^x e^{x-t}y(t)\dd t.\]')

g='F. 隐式方程、因式分解与参数法'
add(g,'第 1 章例 173',87,'2.4：导数多项式的分支',r'求方程的通积分：\[(y\prime)^2-(3x-2y)y\prime+2x^2-xy-3y^2=0.\]')
add(g,'第 1 章例 174',87,'2.4：三个导数分支',r'求方程的通积分：\[(y\prime)^3-(x^2+xy+y^2)y\prime+xy(x+y)=0.\]')
add(g,'第 1 章例 177',88,'2.4：参数法与丢失分支',r'求方程的解：\[9y(y\prime)^2+4x^3y\prime-4x^2y=0.\]')
add(g,'第 1 章例 179',89,'2.4：解出自变量的参数法',r'求方程的解：\[x=y\prime\sin y\prime.\]')

g='G. 非线性系统与首次积分'
add(g,'第 3 章练习 23',259,'2.5：首次积分判据',r'求方程组的第一积分：\[y\prime=\frac{z^2}{x},\qquad z\prime=\frac{y^2}{x}.\]')
add(g,'第 3 章练习 24',259,'2.5：对称形式与守恒组合',r'求方程组的第一积分：\[\frac{\dd x}{z^2-y^2}=\frac{\dd y}{z}=-\frac{\dd z}{y}.\]')
add(g,'第 3 章练习 25',260,'2.5：对称形式与分母零集',r'求方程组的第一积分：\[-\frac{\dd x}{x^2}=\frac{\dd y}{xy-2z^2}=\frac{\dd z}{xz}.\]')
add(g,'第 3 章练习 26',260,'2.5：相同增长率与组合',r'求方程组的第一积分：\[\frac{\dd x}{2y-z}=\frac{\dd y}{y}=\frac{\dd z}{z}.\]')

g='H. 3.1：基本解矩阵与常数变易法'
add(g,'第 3 章例 409',225,'3.1：解空间、基本解矩阵与初值',r'求方程组的通解：\[\dot x=2x+y,\qquad\dot y=3x+4y.\]',r'原书用消元法；本册新增提示：给出两个齐次解 $e^t(1,-1)^{\mathsf T}$ 与 $e^{5t}(1,3)^{\mathsf T}$。只用 3.1 验证它们构成基本解组，写通解、在 $0$ 归一化的基本解矩阵，并写任意初值解。')
add(g,'第 3 章例 410',225,'3.1：非齐次叠加与常数变易',r'求方程组的通解：\[\dot x+y=t^2+6t+1,\qquad\dot y-x=-3t^2+3t+1.\]',r'新增提示：齐次基本解矩阵可取 $\Phi(t)=\begin{pmatrix}\cos t&-\sin t\\\sin t&\cos t\end{pmatrix}$，先核验。分别对两部分非齐次项求特解并叠加，或直接用常数变易；不用高阶常系数方法。')
add(g,'第 3 章例 411',225,'3.1：三维基本解组与解矩阵变换',r'求方程组的通解：\[\dot x=-x+y+z,\qquad\dot y=x-y+z,\qquad\dot z=x+y-z.\]',r'新增提示：给出原书通解中的三列 $e^t(1,1,1)^{\mathsf T}$、$e^{-2t}(1,0,-1)^{\mathsf T}$、$e^{-2t}(0,1,-1)^{\mathsf T}$。用行列式验证基本解组，再写所有基本解矩阵的表达，并反求系数矩阵。')
add(g,'第 3 章练习 1',258,'3.1：已知基解的线性系统',r'求方程组的通解：\[\frac{\dd x}{\dd t}=x+2y,\qquad\frac{\dd y}{\dd t}=2x-y.\]',r'新增提示：可直接验证两解 $e^{\sqrt5t}(2,\sqrt5-1)^{\mathsf T}$、$e^{-\sqrt5t}(2,-\sqrt5-1)^{\mathsf T}$。新增小问：求 $x(0)=1,y(0)=0$ 的解，并用 Liouville 公式核验 Wronski 行列式。')
add(g,'第 3 章例 430',235,'3.1.3--3.1.4：常数变易',r'用常数变易法求通解：\[\dot x=-4x-2y+\frac2{e^t-1},\qquad\dot y=6x+3y-\frac3{e^t-1}.\]',r'为限定在 3.1，给出原书齐次基本解矩阵 $\Phi(t)=\begin{pmatrix}1&e^{-t}\\-2&-3e^{-t}/2\end{pmatrix}$。先验证再使用，并在 $t>0$ 或 $t<0$ 分别讨论。给定矩阵作为新增提示，原方程未改。')
add(g,'第 3 章例 431',235,'3.1.3--3.1.4：常数变易',r'求方程组的通解：\[\dot x=x-y-\frac1{\cos t},\qquad \dot y=2x-y.\]',r'新增提示：原书给出的齐次基解可组成 $\Phi(t)=\begin{pmatrix}\sin t&\cos t\\\sin t-\cos t&\sin t+\cos t\end{pmatrix}$，不要求用特征值法求它。选不跨越 $\cos t=0$ 的区间。')
add(g,'第 3 章例 434',237,'3.1：变系数基本解矩阵与 Liouville 公式',r'求方程组的通解（$\varphi,\psi$ 为连续函数）：\[\dot x=x\varphi(t)+y\psi(t),\qquad \dot y=-x\psi(t)+y\varphi(t).\]',r'新增训练小问：构造在 $t_0$ 归一化的基本解矩阵，求 $W$ 并核验 Liouville 公式；用它反求 $A(t)$，再写状态转移矩阵。可以把复合三角函数直接求导验证，不需要 3.2 的矩阵指数。')

g='I. 建模与积分的应用'
add(g,'第 1 章例 59',31,'1.1、2.1：质量变化与分离',r'具有全燃料储存的火箭质量为 $M$，它无燃料时的质量为 $m$，燃烧物从火箭中流出的速度为 $c$，火箭的初速度为 $0$。求燃料燃烧后的火箭速度。重力和空气阻力忽略不计。',r'原书的 $c$ 是喷出物相对火箭的速率。建模时先明确运动方向和瞬时质量；不能直接把变质量系统写成固定质量的 $Mv\prime=0$。')

from exam_revision import revise
from standard_questions import standardize
problems = standardize(revise(problems))
assert len(problems)==67, len(problems)
head=r'''\input{preamble.tex}
\newcounter{exercise}
\newcommand{\problem}[3]{\refstepcounter{exercise}\subsection*{\theexercise.\quad #1}\label{ex:#2}\textit{出处：#3}\par}
\title{微分方程 I：期中训练题 67 题\\\large 标准题面版 · 截止第 3.1 节（含）}
\author{}\date{2026 年 10 月 28 日}
\maketitle\vspace{-2em}
\textbf{范围与构成。}考试范围截止第 3.1 节（含）。全册 67 题：前 50 题包括概念辨析 6 题、代表计算 14 题、基本定理证明 18 题、首次积分综合 6 题、教材应用 6 题；第 51--60 题为已有的变量分离、线性化、积分因子与隐式方程补充；第 61--64 题收录教材习题 2.5 第 2 题全部四问，第 65--67 题为习题集首次积分补充题。原有编号不变。不附答案。

\textbf{符号约定。}除另有规定外，$I$ 为非空开区间，未知向量 $x$ 取值于 $\R^n$，$I_n$ 为 $n$ 阶单位矩阵；$|\cdot|$ 为向量范数，$\|\cdot\|$ 为其诱导矩阵范数。线性相关或无关均指以常数为系数的向量函数关系。函数独立性按对状态变量的 Jacobi 矩阵秩判定。

\textbf{来源。}“2025 卷”指所提供、卷首标有上海交通大学致远班 2025--2026 学年第一学期期中试卷的照片；“2023 卷”指所提供、署编者史瑞普的 2023--2024 学年第一学期试题及部分答案整理稿。教材为《微分方程 I（101 计划）》，习题集为博亚尔丘克、戈洛瓦奇《高等数学例题与习题集（四）常微分方程》。题面按本册要求统一，原题来源与改编标记见各题。

\textbf{页码。}所选习题集题目 PDF 页＝印刷页＋8；教材 PDF 页＝印刷页＋10。试卷按大题、小题号定位。

\begingroup\small\setlength{\parskip}{0pt}\tableofcontents\endgroup\newpage
'''
def math_text(s):
    s=s.replace(r'^{\prime\prime}','SECONDPRIME').replace(r'^{\prime}','FIRSTPRIME')
    s=s.replace('（1）',r'\par（1）').replace('（2）',r'\par（2）').replace('（3）',r'\par（3）').replace('（4）',r'\par（4）')
    return s.replace(r'\prime',r'^{\prime}').replace('SECONDPRIME',r'^{\prime\prime}').replace('FIRSTPRIME',r'^{\prime}')
parts=[head]
last=None
for i,p in enumerate(problems,1):
    if p['group']!=last:
        parts.append('\\section{'+p['group']+'}\n');last=p['group']
    page=p['page']
    parts.append(r'\noindent\begin{minipage}{\linewidth}'+'\n')
    parts.append(r'\problem{'+p['topic']+'}{'+f'{i:02}'+'}{'+p['source']+'；'+p.get('location',f'书 p.{page} / PDF p.{page+8}' if isinstance(page,int) else '')+'}\n')
    parts.append(math_text(p['text'])+'\n')
    if p['note']: parts.append(r'\textbf{说明：}'+math_text(p['note'])+'\n')
    parts.append(r'\end{minipage}\par\vspace{5pt}'+'\n')
parts.append(r'\newpage\section*{来源速查表}\addcontentsline{toc}{section}{来源速查表}'+ '\n')
parts.append(r'\small\begin{longtable}{r p{.30\linewidth}rr p{.33\linewidth}}\toprule 本册 & 原书题号 & 书页 & PDF 页 & 章节映射\\\midrule\endhead'+'\n')
for i,p in enumerate(problems,1):
    parts.append(f"{i} & {p['source']} & {p['page'] if isinstance(p['page'],int) else '--'} & {p['page']+8 if isinstance(p['page'],int) else '--'} & {p['topic']}\\\\\n")
parts.append(r'\bottomrule\end{longtable}\end{document}')
(ROOT/'training.tex').write_text(''.join(parts),encoding='utf-8')
with (ROOT/'sources.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['本册题号','分组','原书题号','印刷页','PDF页','考点','补充说明','来源位置'])
    for i,p in enumerate(problems,1):w.writerow([i,p['group'],p['source'],p['page'],p['page']+8 if isinstance(p['page'],int) else '',p['topic'],p['note'],p.get('location','')])
print('Generated 67 exercises.')
