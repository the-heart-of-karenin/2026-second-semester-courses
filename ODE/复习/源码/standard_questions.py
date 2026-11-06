"""Standard examination wording. Keys are the stable current exercise numbers."""
TEXT = {
1:r'''（1）给出 $n$ 阶常微分方程的解、通解的定义，并写出通解中 $n$ 个任意常数相互独立的 Jacobi 行列式条件。
（2）在 $t>0$ 上，判断函数族 $x=C_1t+C_2t^{-1}+t\ln t$ 是否为方程 $t^2x''+tx'-x-t=0$ 的通解，并说明理由。
（3）将方程组 $x''+y=0,\ y''-x=0$ 化为四维一阶微分方程组。''',
2:r'''设
\[\varphi_1(t)=(1,0,0)^{\mathsf T},\quad\varphi_2(t)=(t,0,0)^{\mathsf T},\quad\varphi_3(t)=(t^2,0,0)^{\mathsf T},\quad t\in\R.\]
（1）判断上述向量函数组在 $\R$ 上是否线性无关。
（2）是否存在连续矩阵函数 $A:\R\to\R^{3\times3}$，使上述三个函数均为 $x'=A(t)x$ 的解？
（3）对任意三个连续三维向量函数，条件 $\det(\varphi_1(t),\varphi_2(t),\varphi_3(t))\equiv0$ 是否足以推出它们线性相关？各问均须说明理由。''',
3:r'''设 $I$ 为区间，$A\in C(I,\R^{n\times n})$，$b\in C(I,\R^n)$ 且 $b\not\equiv0$。记方程 $x'=A(t)x+b(t)$ 在 $I$ 上的全体解为 $\mathcal S$。判断下列命题，正确者给出证明，错误者给出反例或理由：
（1）$\mathcal S$ 是 $n+1$ 维线性空间；（2）$\mathcal S$ 是 $n$ 维仿射空间；（3）$\mathcal S$ 中任意 $n+2$ 个解线性相关；（4）若 $x_1,\ldots,x_k\in\mathcal S$，$c_j\in\R$ 且 $\sum_{j=1}^k c_j=1$，则 $\sum_{j=1}^k c_jx_j\in\mathcal S$。''',
4:r'''设 $g\in C(\R)$ 且 $g(t)>0$。考虑方程
\[x'=g(t)\sqrt[3]{x}.\]
（1）对任意 $(t_0,x_0)\in\R^2$，求一个定义在 $\R$ 上且满足 $x(t_0)=x_0$ 的解。
（2）证明：对任意 $t_0\in\R$，初值条件 $x(t_0)=0$ 对应无穷多个定义在 $\R$ 上的解。
（3）证明：方程的任一全实轴解 $x$ 均满足 $x(t)\ge0\ (\forall t\in\R)$ 或 $x(t)\le0\ (\forall t\in\R)$。''',
5:r'''（1）求初值问题 $x'=x^2,\ x(0)=1$ 的解及其最大存在区间。
（2）设 $a,b\in C(\R)$。证明 $x'=a(t)x+b(t),\ x(0)=1$ 存在唯一的全实轴解。
（3）求 $x'=x/t,\ x(1)=1$ 在原方程定义域内的最大存在区间。所得函数能否延拓为 $\R$ 上的 $C^1$ 函数？延拓后的函数是否为原方程在 $\R$ 上的解？''',
6:r'''（1）在 $D=\R^2\setminus\{(0,0)\}$ 上，令
\[M(t,x)=-\frac{x}{t^2+x^2},\qquad N(t,x)=\frac{t}{t^2+x^2}.\]
证明 $M_x=N_t$，并证明不存在 $U\in C^1(D)$ 同时满足 $U_t=M,U_x=N$。
（2）设 $U(t,x,C)$ 为 $C^2$ 函数。消去 $U=0,U_C=0$ 中的 $C$ 所得曲线是否必为曲线族 $U(t,x,C)=0$ 的包络，或该曲线族对应微分方程的奇解？说明理由，并列出验证包络与奇解所需的条件。''',
7:r'''求微分方程的通解或通积分，并确定解的适用区间：
\[y'=\frac yx+e^x\frac{2xy}{x^2+y^2}.\]''',
8:r'''求微分方程的通积分：
\[(2x-4y+6)\dd x+(x+y-3)\dd y=0.\]''',
9:r'''求微分方程 $y=x(y'-x\cos x)$ 的通解，并分别给出其在 $x>0$ 和 $x<0$ 上的表达式。''',
10:r'''求微分方程的通解或通积分，并给出原方程的定义域及所取解支的适用区间：
\[y'=\frac{y}{3x-y^2}.\]''',
11:r'''求微分方程 $y'+2y=e^xy^2$ 的全部实解。''',
12:r'''在 $x\ne0$ 上求微分方程
\[xy'-2x^2\sqrt y=4y\]
的非负实解。对所得非零解，给出其适用区间；另求出可在区间内部取零值的解。''',
13:r'''在不含 $x=0$ 的区间上，求微分方程
\[2y'=xy+y^2+\frac1{x^2}-3\]
的通解或通积分。''',
14:r'''求微分方程的通积分：
\[(1+y^2\sin2x)\dd x-2y\cos^2x\dd y=0.\]''',
15:r'''求微分方程
\[(x^2+2x+y)\dd x-(x-3x^2y)\dd y=0\]
的一个处处非零的积分因子及相应通积分，并说明积分因子的适用区域。''',
16:r'''求方程 $y'=\sqrt y$ 的全部全实轴非负 $C^1$ 解，并确定其中满足 $y(0)=0$ 的解。判断 $y\equiv0$ 是否为奇解，并说明理由。''',
17:r'''求一阶隐式微分方程
\[(y')^2-(3x-2y)y'+2x^2-xy-3y^2=0\]
的各支通解或通积分。''',
18:r'''求一阶隐式微分方程 $x=y'\sin y'$ 的参数形式解，并写出参数曲线可局部表示为 $y=y(x)$ 的条件。''',
19:r'''已知方程
\[x'=x^2-2tx+t^2+1\]
有特解 $\varphi(t)=t$。
（1）求方程的通解；（2）对任意 $(t_0,x_0)\in\R^2$，求满足 $x(t_0)=x_0$ 的解及其最大存在区间。''',
20:r'''在 $t>0$ 上考虑系统
\[x'=A(t)x,\qquad A(t)=\begin{pmatrix}1/t&t\\0&-1/t\end{pmatrix}.\]
已知 $\varphi(t)=(t,0)^{\mathsf T}$ 为系统的一个解。
（1）求系统通解及一个基本解矩阵 $\Phi(t)$；
（2）计算 $W(t)=\det\Phi(t)$，验证 $W'=\operatorname{tr}A(t)W$；
（3）求满足 $X(1)=I_2$ 的基本解矩阵 $X(t)$。''',
21:r'''设 $I\subset\R$ 为区间，$t_0\in I$，$x_0\in\R^n$，$A\in C(I,\R^{n\times n})$，$b\in C(I,\R^n)$。证明下列两个条件等价：
\begin{enumerate}[label=(\arabic*)]
\item $x\in C^1(I,\R^n)$，$x'=A(t)x+b(t)$，且 $x(t_0)=x_0$；
\item $x\in C(I,\R^n)$，且对任意 $t\in I$，
\[x(t)=x_0+\int_{t_0}^t[A(s)x(s)+b(s)]\dd s.\]
\end{enumerate}''',
22:r'''设 $I$ 为区间，$t_0\in I$，$x_0\in\R^n$，$A\in C(I,\R^{n\times n})$，$b\in C(I,\R^n)$。定义
\[x^{[0]}(t)=x_0,\qquad x^{[k+1]}(t)=x_0+\int_{t_0}^t[A(s)x^{[k]}(s)+b(s)]\dd s.\]
（1）设 $J\subset I$ 为包含 $t_0$ 的紧区间，$\|A(t)\|\le K,|b(t)|\le K$（$t\in J$）。证明对 $k\ge1$，
\[|x^{[k]}(t)-x^{[k-1]}(t)|\le(1+|x_0|)\frac{K^k|t-t_0|^k}{k!}.\]
（2）证明 $x^{[k]}$ 在 $J$ 上一致收敛，且极限为相应初值问题的解。
（3）证明该初值问题的解存在于整个 $I$ 上。本题不得直接引用线性系统的全局存在定理。''',
23:r'''设 $A\in C([t_0,T],\R^{n\times n})$，$t_0<T$，且 $\|A(t)\|\le M$。令 $x$ 为初值问题 $x'=A(t)x,\ x(t_0)=x_0$ 的解，并定义
\[x^{[0]}(t)=x_0,\qquad x^{[k+1]}(t)=x_0+\int_{t_0}^t A(s)x^{[k]}(s)\dd s.\]
求仅依赖于 $M,T-t_0,|x_0|,n$ 的显式量 $E_n$，使
\[\sup_{t\in[t_0,T]}|x(t)-x^{[n]}(t)|\le E_n,\qquad\lim_{n\to\infty}E_n=0,\]
并证明所给估计。''',
24:r'''设 $A\in C(I,\R^{n\times n})$，$b\in C(I,\R^n)$，$t_0\in I$。
（1）证明：若 $x_1,x_2$ 均满足 $x'=A(t)x+b(t)$ 且 $x_1(t_0)=x_2(t_0)$，则 $x_1\equiv x_2$。本问不得直接引用唯一性定理。
（2）证明：若 $x$ 为 $x'=A(t)x$ 的非零解，则对所有 $t\in I$ 均有 $x(t)\ne0$。
（3）给出一个连续系数齐次系统及其非零解，使该解的某个分量在区间内变号。''',
25:r'''设 $A\in C(I,\R^{n\times n})$。记
\[\mathcal S(A)=\{x\in C^1(I,\R^n):x'=A(t)x\}.\]
证明 $\mathcal S(A)$ 是实线性空间，且 $\dim\mathcal S(A)=n$。''',
26:r'''设 $A\in C(I,\R^{n\times n})$，$\varphi_1,\ldots,\varphi_n$ 为系统 $x'=A(t)x$ 的解。令
\[\Phi(t)=(\varphi_1(t),\ldots,\varphi_n(t)),\qquad W(t)=\det\Phi(t).\]
不假设 $\Phi(t)$ 可逆。证明
\[W'(t)=\operatorname{tr}A(t)W(t),\qquad W(t)=W(t_0)\exp\!\left(\int_{t_0}^t\operatorname{tr}A(s)\dd s\right)\quad(t,t_0\in I).\]''',
27:r'''设 $A\in C(I,\R^{n\times n})$，$\varphi_1,\ldots,\varphi_n$ 为同一系统 $x'=A(t)x$ 的解，$W(t)=\det(\varphi_1(t),\ldots,\varphi_n(t))$。证明下列条件等价：
（1）$\varphi_1,\ldots,\varphi_n$ 在 $I$ 上线性无关；
（2）存在 $t_0\in I$ 使 $W(t_0)\ne0$；
（3）对任意 $t\in I$，$W(t)\ne0$。
若 $\varphi_j$ 仅为任意 $C^1$ 向量函数，上述哪些蕴涵仍成立？证明结论或给出反例。''',
28:r'''设 $A\in C(I,\R^{n\times n})$，$\Phi,\Psi$ 均为系统 $x'=A(t)x$ 的基本解矩阵。证明：
（1）存在唯一的常数可逆矩阵 $C$，使 $\Psi(t)=\Phi(t)C$（$t\in I$）；
（2）对任意常数可逆矩阵 $C$，$\Phi(t)C$ 也是该系统的基本解矩阵；
（3）对任意常数可逆矩阵 $C$，$C\Phi(t)$ 是否必为该系统的基本解矩阵？说明理由。''',
29:r'''设 $I$ 为区间。
（1）设 $A,B\in C(I,\R^{n\times n})$，$\Phi$ 同时为系统 $x'=A(t)x$ 与 $x'=B(t)x$ 的基本解矩阵。证明 $A(t)=B(t)$（$t\in I$）。
（2）设 $\Phi\in C^1(I,\R^{n\times n})$ 且 $\det\Phi(t)\ne0$（$t\in I$）。求连续矩阵函数 $A(t)$，并证明 $\Phi$ 是 $x'=A(t)x$ 的基本解矩阵。
（3）若将（1）中的“基本解矩阵”改为“解矩阵”，结论是否仍成立？说明理由。''',
30:r'''设 $A\in C(I,\R^{n\times n})$，$b\in C(I,\R^n)$，$x_p$ 为 $x'=A(t)x+b(t)$ 的一个解，$\mathcal S(A)$ 为对应齐次系统的解空间。证明：
（1）任意两个非齐次解之差属于 $\mathcal S(A)$；
（2）非齐次系统的全体解为 $\mathcal S(A,b)=x_p+\mathcal S(A)$；
（3）若 $x_j\in\mathcal S(A,b)$，$c_j\in\R$ 且 $\sum c_j=1$，则 $\sum c_jx_j\in\mathcal S(A,b)$。
当 $b\not\equiv0$ 时，判断 $\mathcal S(A,b)$ 是否为线性空间，并说明理由。''',
31:r'''设 $A\in C(I,\R^{n\times n})$，$b\in C(I,\R^n)$ 且 $b\not\equiv0$。
（1）证明方程 $x'=A(t)x+b(t)$ 的任意 $n+2$ 个解线性相关。
（2）证明该方程存在 $n+1$ 个线性无关的解。
（3）求该方程解集的仿射维数及其线性张成空间的维数。''',
32:r'''设 $A\in C(I,\R^{n\times n})$，$b\in C(I,\R^n)$，$\Phi$ 为 $x'=A(t)x$ 的任一基本解矩阵。证明非齐次系统 $x'=A(t)x+b(t)$ 的通解为
\[x(t)=\Phi(t)\left(c+\int_{t_*}^t\Phi(s)^{-1}b(s)\dd s\right),\qquad c\in\R^n,\ t_*\in I.\]
并证明满足初值 $x(t_0)=x_0$ 的解为
\[x(t)=\Phi(t)\Phi(t_0)^{-1}x_0+\Phi(t)\int_{t_0}^t\Phi(s)^{-1}b(s)\dd s.\]''',
33:r'''设 $A\in C(I,\R^{n\times n})$，$\Phi$ 为 $x'=A(t)x$ 的基本解矩阵。对 $t,s\in I$ 定义 $U(t,s)=\Phi(t)\Phi(s)^{-1}$。证明 $U$ 与基本解矩阵的选择无关，并证明对任意 $t,r,s\in I$，
\[U(s,s)=I_n,\quad U(t,r)U(r,s)=U(t,s),\quad U(t,s)^{-1}=U(s,t),\]
\[\partial_tU(t,s)=A(t)U(t,s),\qquad \partial_sU(t,s)=-U(t,s)A(s).\]''',
34:r'''设 $I,J$ 为开区间，$M,N\in C^1(I\times J)$。
（1）证明：存在 $U\in C^2(I\times J)$ 满足 $U_t=M,U_x=N$，当且仅当 $M_x=N_t$ 在 $I\times J$ 恒成立。
（2）在 $M_x=N_t$ 时，给出 $U$ 的积分表达式。
（3）若将 $I\times J$ 改为任意单连通开区域，上述等价结论是否仍成立？说明理由。''',
35:r'''设 $D\subset\R^2$ 为单连通开区域，$M,N\in C^1(D)$，$\varphi\in C^1(D)$，$J$ 为包含 $\varphi(D)$ 的开区间。证明下列命题等价：
（1）存在处处非零的 $m\in C^1(J)$，使 $\mu(t,x)=m(\varphi(t,x))$ 为 $M\dd t+N\dd x=0$ 的积分因子；
（2）存在 $h\in C(J)$，使
\[N_t-M_x=(M\varphi_x-N\varphi_t)h(\varphi)\qquad\text{在 }D\text{ 上恒成立}.\]
给出由 $h$ 构造 $m$ 的公式，并分别写出 $\varphi=tx$ 与 $\varphi=t^2+x^2$ 时的条件。''',
36:r'''设 $I$ 为开区间，$p,q\in C(I)$。考虑非负实解满足的 Bernoulli 方程
\[x'+p(t)x=q(t)x^\alpha.\]
（1）设 $\alpha>1$。证明：若 $x(t_0)=0$，$t_0\in I$，则 $x\equiv0$。
（2）设 $0<\alpha<1$。分别给出一组 $p,q$，使初值 $x(t_0)=0$ 有非零解，和一组 $p,q$，使该初值只有零解。''',
37:r'''设 $I$ 为区间，以下各方程的系数均在 $I$ 上连续。
（1）已知 $x_1,x_2$ 是一阶线性方程 $x'+p(t)x=q(t)$ 的两个不同解，证明其通解为
\[x=x_1+C(x_2-x_1),\qquad C\in\R.\]
（2）已知 $x_1,x_2$ 是 Riccati 方程 $x'+p(t)x=q(t)x^2+r(t)$ 的两个不同解。对任意解 $x$，在 $x-x_2\ne0$ 的区间上令 $z=(x-x_1)/(x-x_2)$。证明
\[z'=q(t)(x_1-x_2)z.\]
由此求出 Riccati 方程的通解，并说明所得表达式的适用区间。''',
38:r'''设 $g\in C(\R)$，$d\in C(\R^2)$。令 $x\in C^2(I)$ 为方程
\[x''+d(x,x')x'+g(x)=0\]
的解，并定义
\[E(t)=\tfrac12x'(t)^2+\int_0^{x(t)}g(u)\dd u.\]
（1）证明 $E'(t)=-d(x(t),x'(t))x'(t)^2$。
（2）若 $d\ge0$，证明 $E$ 不增；此时 $E$ 是否一定为首次积分？说明理由。
（3）若 $d\equiv0$，证明能量守恒。''',
39:r'''考虑自治系统
\[x'=x(y^2-z^2),\quad y'=y(z^2-x^2),\quad z'=z(x^2-y^2).\]
（1）求全部平衡点，并判断三个坐标平面是否为不变集合。
（2）求两个不含 $t$ 的首次积分 $F_1,F_2$，确定 $\operatorname{rank}\partial(F_1,F_2)/\partial(x,y,z)=2$ 的区域及秩小于 $2$ 的点集。
（3）在非平衡点的充分小邻域内，分别求不含 $t$ 及允许显含 $t$ 的函数独立首次积分个数的上界。
（4）仅由（2）的两个首次积分能否唯一确定带时间参数的解 $(x(t),y(t),z(t))$？说明理由。''',
40:r'''设 $g\in C^1(\R)$，考虑系统 $x'=2y,\ y'=-g(x)$。
（1）求一个不含 $t$ 的首次积分，并给出其力学解释。
（2）在 $y\ne0$ 的解支上，将时间 $t$ 表示为 $x$ 的积分式。
（3）求系统的全部平衡点，并给出非平衡解在 $x'=0$ 处的转向判据。
（4）给定首次积分常数后，是否已唯一确定初值解？说明理由。''',
41:r'''在 $x\ne0$ 上，$y,z$ 为自变量 $x$ 的函数。求系统
\[y'=\frac{z^2}{x},\qquad z'=\frac{y^2}{x}\]
的一个不含 $x$ 的非恒定首次积分，并确定该首次积分对 $(y,z)$ 的梯度非零的点集。''',
42:r'''考虑自治系统
\[\frac{\dd x}{\dd t}=z^2-y^2,\qquad \frac{\dd y}{\dd t}=z,\qquad \frac{\dd z}{\dd t}=-y.\]
求两个不含 $t$ 的首次积分，并确定它们函数独立的区域。''',
43:r'''设 $D\subset\R^{n+1}$ 为开区域，$f\in C^1(D,\R^n)$，$F\in C^1(D)$，且 $F$ 在 $D$ 的任意非空开子集上均非常数。证明 $F$ 是系统 $x'=f(t,x)$ 的首次积分，当且仅当
\[F_t(t,x)+\sum_{j=1}^nF_{x_j}(t,x)f_j(t,x)=0\qquad((t,x)\in D).\]
若 $F_1,\ldots,F_n$ 为 $C^1$ 首次积分，且在 $(t_0,x_0)$ 处
\[\det\frac{\partial(F_1,\ldots,F_n)}{\partial(x_1,\ldots,x_n)}(t_0,x_0)\ne0,\]
证明方程组 $F_j(t,x)=c_j$ 在该点附近确定系统的一族通解。''',
44:r'''求自治系统
\[x'=y-x(x^2+y^2-1),\qquad y'=-x-y(x^2+y^2-1)\]
的通解，并在适当区域内求两个显含 $t$ 的函数独立首次积分。分别给出非零解、零解及位于 $x^2+y^2=1$ 上的解，并说明各解的存在区间及首次积分的定义区域。''',
45:r'''某封闭人群由易感者、感染者、移出者三类组成，人数分别记为 $S(t),I(t),R(t)$。假设无出生、死亡及人口迁移；单位时间内新增感染人数为 $\beta S(t)I(t)$；感染者以比例 $\gamma$ 移出，其中 $\beta,\gamma>0$。初值为 $S(0)=S_0>0,I(0)=I_0>0,R(0)=R_0\ge0$。
（1）建立 SIR 微分方程组。
（2）求总人口守恒量及一个关于 $S,I$ 的首次积分。
（3）求 $I$ 在初始时刻增长的充要条件；确定 $I$ 在 $t\ge0$ 上的最大值，并分别讨论最大值在 $t=0$ 及 $t>0$ 取得的情形。''',
46:r'''设 $\beta,\gamma>0$，$S_0,I_0>0,R_0\ge0$。设 $(S,I,R)$ 为系统
\[S'=-\beta SI,\quad I'=\beta SI-\gamma I,\quad R'=\gamma I\]
在 $[0,\infty)$ 上的解，初值为 $(S_0,I_0,R_0)$，记 $N=S_0+I_0+R_0$。
（1）证明 $S,I,R$ 保持非负，$S$ 不增，$R$ 不减。
（2）证明 $I(t)\to0$，并推导 $S_\infty=\lim_{t\to\infty}S(t)$ 满足的隐式方程。
（3）将感染发生率改为 $\beta SI/N$，求修改后系统的首次积分、初始感染增长阈值及 $S_\infty$ 满足的方程。''',
47:r'''在 $t$--$x$ 平面中，求曲线族 $x=t\ln(ct)$ 的 $-\pi/4$ 等角轨线族，其中 $c\in\R\setminus\{0\}$，原曲线定义在 $ct>0$ 的区域。有向角约定为：从原曲线沿 $t$ 增大方向的切线转向所求曲线沿 $t$ 增大方向的切线的角度为 $-\pi/4$（模 $\pi$）。写出轨线方程及其解的适用区域。''',
48:r'''在 $t$--$x$ 平面中，考虑过原点的直线族（包括竖直直线）。设 $0<\alpha<\pi/2$。
（1）求该直线族的正交轨线族。
（2）分别求与该直线族成有向角 $+\alpha$、$-\alpha$ 的等角轨线族，并将结果写成极坐标 $t=r\cos\theta,x=r\sin\theta$ 下的形式。
上述轨线均在去心平面中讨论。''',
49:r'''在惯性坐标系中，两个质量分别为 $m_1,m_2>0$ 的质点仅受彼此的 Newton 万有引力作用，引力常数为 $G>0$。设其位置为 $q_1(t),q_2(t)\in\R^3$，且在讨论区间无碰撞。记 $r=q_2-q_1$，$\rho=|r|$，$\mu=G(m_1+m_2)$。
（1）建立 $r$ 的运动方程，证明 $h=r\times r'$ 与 $\varepsilon=|r'|^2/2-\mu/\rho$ 为常量。
（2）设 $h\ne0$。证明轨道位于固定平面内且面积速度为常数，并推导
\[\rho(\theta)=\frac{p}{1+e\cos(\theta-\theta_0)}.\]
求 $p,e$ 与 $|h|,\varepsilon,\mu$ 的关系，写出圆、椭圆、抛物线、双曲线各自对应的条件。
（3）设轨道为椭圆，半长轴为 $a$、周期为 $T$，证明 $T^2=4\pi^2a^3/\mu$。
（4）描述 $h=0$ 时的运动轨迹。''',
50:r'''设地球为半径 $R$、质量 $M$ 的球对称天体，地心固定，忽略空气阻力、地球自转及其他天体的引力。质点于 $t=0$ 从地表以速率 $v_0>0$ 向外发射，速度与当地水平面的夹角为 $0\le\alpha<\pi/2$。取发射点的地心极角为 $\theta=0$，记 $\mu=GM$。
（1）建立质点在地球外部的运动方程和初值条件。
（2）求比角动量、比能量及轨道的极坐标方程，明确方程中的参数和初始相位。
（3）按 $v_0,\alpha$ 判别形式轨道的类型，给出质点能够逃逸至无穷远的充要条件。
（4）确定质点是否在 $t>0$ 再次与地表相交。若相交，给出相交极角满足的方程及有效飞行弧段；若不相交，说明理由。'''
}

def standardize(problems):
    assert len(problems)==len(TEXT)==50
    for n,p in enumerate(problems,1):
        p['text']=TEXT[n]
        p['note']=''
    # Source and adaptation metadata are kept outside the mathematical statement.
    for n in [7,8,9,10,11,12,13,14,15,16,17,18,41,42]:
        p=problems[n-1]
        if '改编' not in p['source']:p['source']+='（本册改编）'
    for n in [19,20,40,47]:
        p=problems[n-1]
        if '改编' not in p['source']:p['source']+='（本册改编）'
    for n in range(7,16): problems[n-1]['topic']='一阶微分方程'
    problems[16-1]['topic']='非唯一性与奇解'
    problems[17-1]['topic']='一阶隐式微分方程'
    problems[18-1]['topic']='一阶隐式方程'
    problems[38-1]['topic']='能量守恒与耗散'
    problems[44-1]['topic']='首次积分与通解'

    extra=[
        ('零次齐次方程',r"在 $t>0$ 上求方程 $x'=(t^2+tx+x^2)/t^2$ 的通解，并求满足 $x(1)=0$ 的解及其最大存在区间。",'教材 2.1 零次齐次类型（自拟）','教材书 p.23--24 / PDF p.33--34'),
        ('一阶微分方程',r"求方程 $x'=(x+t)/(x-t+1)$ 的通解或通积分，并求满足 $x(0)=0$ 的局部解。",'教材习题 2.1 第 1(5) 题（增加初值问）','教材书 p.25 / PDF p.35'),
        ('一阶微分方程',r"求方程 $x'=(2t+2x+1)/(t+x-1)$ 的全部实解，并给出满足 $x(0)=0$ 的解的最大存在区间。",'教材 2.1 一次式比值退化类型（自拟）','教材书 p.24 / PDF p.34'),
        ('一阶微分方程',r"求方程 $x'=\cos(t+2x)$ 的通积分及所有直线解。",'教材 2.1 线性组合类型（自拟）','教材书 p.25 / PDF p.35'),
        ('一阶微分方程',r"在 $t>0$ 上求方程 $x'=2x/t+x^2/t^3$ 的全部实解，并求满足 $x(1)=1$ 的解及其最大存在区间。",'教材习题 2.1 第 4 题类型（自拟）','教材书 p.25 / PDF p.35')]
    for topic,text,source,loc in extra:
        problems.append(dict(group='F. 2.1 节补充训练（5 题）',source=source,page='',location=loc,topic=topic,text=text,note=''))

    more=[
        ('一阶微分方程',r"求方程 $(t^2+3)\cos x\,\dfrac{\dd x}{\dd t}+2t\sin x=t(t^2+3)$ 的通积分，并在实数范围内写出局部显式解的分支条件。",'教材习题 2.2 第 1(3) 题（增加分支条件问）','教材书 p.33 / PDF p.43'),
        ('积分因子与通积分',r"求方程 $(x^3y-2y^2)\dd x+x^4\dd y=0$ 在 $xy\ne0$ 区域内的一个积分因子及通积分，并确定在 $x\ne0$ 的区间上是否存在恒等于零的解。",'用户提供题目','本次对话所给方程（末项按 $x^4\dd y$ 理解）')]
    for topic,text,source,loc in more:
        problems.append(dict(group='G. 线性化与积分因子补充（2 题）',source=source,page='',location=loc,topic=topic,text=text,note=''))

    implicit=[
        (2,r"求一阶隐式微分方程 $(x'(t))^3-(x'(t))^2-x=0$ 的解。"),
        (4,r"在实数范围内求一阶隐式微分方程 $x-tx'(t)-4\sqrt{x'(t)}=0$ 的解。"),
        (6,r"求一阶隐式微分方程 $(x'(t))^3-(x'(t))^2-2t=0$ 的解。")]
    for num,text in implicit:
        problems.append(dict(group='H. 隐式方程补充（3 题）',source=f'教材习题 2.4 第 1({num}) 题',page='',location='教材书 p.46 / PDF p.56',topic='一阶隐式微分方程',text=text,note=''))
    first_integrals=[
        (1,r'''求系统
\[x'=x^2-y^2-z^2,\qquad y'=2xy,\qquad z'=2xz\]
的解。求三个允许显含 $t$ 的函数独立首次积分，并明确各自的定义区域及独立性条件；另求不含 $t$ 的首次积分，给出在所取区域内的独立性判定。若求解中除以 $y$、$z$ 或 $y^2+z^2$，须补充讨论相应零集上的解。'''),
        (2,r'''求系统
\[x'=yz,\qquad y'=xz,\qquad z'=xy\]
的两个不含 $t$ 的首次积分，确定它们函数独立的点集。求全部平衡解，并在非平衡解的适当区间上，以一个坐标为参数，用定积分表示其余坐标及时间 $t$；明确所选实数分支和参数范围。'''),
        (3,r'''在 $x\ne y$ 上，求系统
\[x'=\frac{y}{x-y},\qquad y'=\frac{x}{x-y}\]
的两个函数独立首次积分，并由此求通解及其最大存在区间。确定何种初值对应的解在有限时间趋于直线 $x=y$ 上的有限点，并说明它能否作为原系统的解穿过该直线。'''),
        (4,r'''求系统
\[x'=\frac12,\qquad y'=1+\sqrt{t-x-y}\]
的解。先在开区域 $D=\{(t,x,y):t-x-y>0\}$ 内求两个函数独立的首次积分，给出通解及其在 $D$ 内的最大存在区间；再讨论解能否延伸到 $t-x-y=0$，以及能否在该边界上构成一个非退化时间区间内的实解。''')]
    for num,text in first_integrals:
        problems.append(dict(group='I. 首次积分补充（7 题）',source=f'教材习题 2.5 第 2({num}) 题（增加独立性、定义域等小问）',page='',location='教材书 p.57--58 / PDF p.67--68',topic='首次积分与解的恢复',text=text,note=''))
    book_integrals=[
        (25,r'''考虑自治系统
\[x'=-x^2,\qquad y'=xy-2z^2,\qquad z'=xz.\]
求两个不含 $t$ 的首次积分，并确定它们函数独立的点集；求全部平衡点，说明首次积分独立性失效的点集与平衡点集之间的关系。'''),
        (26,r'''考虑自治系统
\[x'=2y-z,\qquad y'=y,\qquad z'=z.\]
在 $y\ne0$ 的区域内求两个不含 $t$ 的函数独立首次积分，再求一个显含 $t$ 的首次积分，使三个首次积分对 $(x,y,z)$ 的 Jacobi 行列式非零。由它们求系统通解，并补充 $y\equiv0$ 的解。'''),
        (27,r'''考虑四维自治系统
\[x'=z,\qquad y'=u,\qquad z'=x,\qquad u'=y.\]
求三个不含 $t$ 的首次积分，并明确给出一个使它们函数独立的非空开区域。说明仅由这三个积分能否唯一确定带时间参数的解；再求一个显含 $t$ 的首次积分，使所得四个首次积分在适当非空开区域内函数独立。''')]
    for num,text in book_integrals:
        problems.append(dict(group='I. 首次积分补充（7 题）',source=f'第 3 章练习 {num}（对称式改写为自治系统，增加独立性等小问）',page=260,topic='首次积分与独立性',text=text,note=''))
    return problems
