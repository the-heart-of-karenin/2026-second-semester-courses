from pathlib import Path
p=Path('ODE/复习/源码/review.tex');s=p.read_text(encoding='utf-8');a=s.index(r'\point{12.');b=s.index(r'\point{15.',a)
s=s[:a]+r'''\point{12. 第一类：零次齐次方程}{homogeneous}
+\core 以下第 12--14 条分类列出可化为变量分离方程的主要类型。式中 $x=x(t)$，$F,g$ 为给定函数；换元只在原式及新变量均有定义的区间上使用。
+
+\textbf{类型：}$x'=g(x/t)$，或右端 $f(t,x)$ 满足 $f(\lambda t,\lambda x)=f(t,x)$。令 $v=x/t$（$t\ne0$），则
+\[
+x'=v+tv',\quad tv'=g(v)-v,\quad
+\int\frac{\dd v}{g(v)-v}=\ln|t|+C.
+\]
+方程 $g(v_0)=v_0$ 的每个实根另给直线解 $x=v_0t$；分离时除去的这些解须补回。“零次齐次”与“线性齐次”含义不同。
+
+\textbf{例：}$x'=x/t+(x/t)^2$。换元后 $tv'=v^2$，非零支满足 $-1/v=\ln|t|+C$，即
+\[
+x(t)=-\frac{t}{\ln|t|+C};\qquad x\equiv0\text{ 另列。}
+\]
+各解在不跨越 $t=0$ 及分母零点的区间上讨论。
+
+\point{13. 第二、三类：两个一次式之比}{affine-ratio}
+统一类型为
+\[
+x'=F\!\left(\frac{at+bx+c}{mt+nx+d}\right),\qquad mt+nx+d\ne0.
+\]
+\textbf{第二类：$\Delta=an-bm\ne0$，先平移再作比值换元。}解
+\[
+at_*+bx_*+c=0,\qquad mt_*+nx_*+d=0,
+\]
+令 $T=t-t_*,X=x-x_*$，则 $\dd X/\dd T=F((aT+bX)/(mT+nX))$。在 $T\ne0$ 上再令 $v=X/T$，得
+\[
+T\frac{\dd v}{\dd T}=F\!\left(\frac{a+bv}{m+nv}\right)-v.
+\]
+右边的零点对应 $X=v_0T$ 的直线解，均须代回原式核验。
+
+\textbf{例（作业习题 2.1 第 1(3) 题）：}
+\[
+x'=\frac{2t+3x-1}{t-x+1}.
+\]
+交点为 $(-2/5,3/5)$。取 $T=t+2/5,X=x-3/5,v=X/T$，得到
+\[
+T v'=\frac{v^2+2v+2}{1-v},\qquad
+\frac{1-v}{v^2+2v+2}\dd v=\frac{\dd T}{T}.
+\]
+这里 $v'$ 指对 $T$ 求导。原分母为零的点不属于原方程定义域；$T=0$ 只是本次比值换元的限制，原解能否跨过它须回原式判断。
+
+\textbf{第三类：$\Delta=0$，用共同线性组合。}若 $b,n$ 不同时为零，则存在 $\lambda$ 使 $a=\lambda b,m=\lambda n$。令 $z=\lambda t+x$，得
+\[
+z'=\lambda+F\!\left(\frac{bz+c}{nz+d}\right),
+\]
+为自治、可分离方程。若 $b=n=0$，右端仅含 $t$，直接积分；若两个一次式恒成比例且比值有定义，右端为常数。这些退化情形不能强行使用交点平移法。
+
+\textbf{例：}$x'=(t+x+1)/(2t+2x-1)$。取 $z=t+x$，得
+\[
+z'=\frac{3z}{2z-1},\qquad
+\frac{2z-1}{3z}\dd z=\dd t.
+\]
+非零支满足 $2z-\ln|z|=3t+C$，即 $2(t+x)-\ln|t+x|=3t+C$；另有 $z\equiv0$ 对应的解 $x=-t$。始终要求 $2z-1\ne0$。
+
+\point{14. 第四、五类：线性组合与加权齐次方程}{weighted}
+\textbf{第四类：}$x'=F(at+bx+c)$。令 $z=at+bx+c$，则
+\[
+z'=a+bF(z).
+\]
+当 $b\ne0$ 时由 $x=(z-at-c)/b$ 回代；当 $b=0$ 时原方程直接对 $t$ 积分。$a+bF(z_0)=0$ 所对应的常值 $z$ 解不可遗漏。
+
+\textbf{例（教材例 2.1.5）：}$x'=\sin(3t+2x)$。取 $z=3t+2x$，得 $z'=3+2\sin z$，故
+\[
+\int\frac{\dd z}{3+2\sin z}=t+C,\qquad z=3t+2x.
+\]
+由于 $3+2\sin z>0$，此处分离不排除常值解。作业中的 $x'=e^{-x+2t}+2$ 则取 $z=x-2t$，化成 $z'=e^{-z}$，得 $e^{x-2t}=t+C$。
+
+\textbf{第五类（补充）：加权齐次方程。}在 $t>0$ 上，若
+\[
+f(\lambda^{s_1}t,\lambda^{s_2}x)=\lambda^k f(t,x),\quad
+s_1\ne0,\quad k=s_2-s_1,
+\]
+则 $f(t,x)=t^{q-1}H(x/t^q)$，其中 $q=s_2/s_1,H(v)=f(1,v)$。令 $x=t^qv$，得
+\[
+tv'=H(v)-qv,\qquad\frac{\dd v}{H(v)-qv}=\frac{\dd t}{t}.
+\]
+右边根 $H(v_0)=qv_0$ 给幂函数解 $x=v_0t^q$，须另列。负半轴上的实幂及符号条件另行处理。
+
+\textbf{例：}$x'=x/t+x^2/t^3$（$t>0$）。取 $x=t^2v$，得 $tv'=v(v-1)$，故非平衡支满足
+\[
+\ln\left|\frac{v-1}{v}\right|=\ln t+C,
+\qquad x=\frac{t^2}{1-C_1t}.
+\]
+另列 $x\equiv0$；$v\equiv1$ 给 $x=t^2$，已包含在最后一式的 $C_1=0$ 中。
+
+\textbf{分类边界。}并非任意换元都会得到分离方程。检验的目标是把新方程真正化为 $v'=A(t)B(v)$，并保留原定义域以及分离时除去的常值支。
+
+'''.replace('\n+','\n')+s[b:]
p.write_text(s,encoding='utf-8')
