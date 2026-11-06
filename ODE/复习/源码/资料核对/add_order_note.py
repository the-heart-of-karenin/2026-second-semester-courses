from pathlib import Path
p=Path('ODE/复习/源码/review.tex');s=p.read_text(encoding='utf-8');a=s.index(r'\subsection{微分方程形式}')
new=r'''
\textbf{例：由通解反求方程时，阶数必须符合通解的定义。}
题设称
\[
y=\sqrt{c_1x^2+c_2}
\]
为某微分方程的通解。该族含两个独立任意常数，因此应构造\textbf{二阶微分方程}，不能任意升阶后仅凭代入成立便称已满足题意。
由 $y^2=c_1x^2+c_2$ 连续求导，得
\[
yy'=c_1x,\qquad (y')^2+yy''=c_1.
\]
消去 $c_1$ 得到
\[
\boxed{x\bigl((y')^2+yy''\bigr)-yy'=0.}
\]
在 $x\ne0$、$y>0$ 的局部区间上，令 $u=y^2$，上述方程等价于 $xu''-u'=0$，其通解为 $u=C_1x^2+C_2$，取正平方根即恢复题给函数族。此时
\[
\det\frac{\partial(y,y')}{\partial(c_1,c_2)}=-\frac{x}{2y^2}\ne0,
\]
故两个参数确实独立。根号零点及 $x=0$ 处需另查可微性与退化情形。
对所求二阶方程继续求导虽可能得到三阶方程，但题给两参数族仅是其解的一部分，不能仅凭这一操作认定它是三阶方程的通解。\textbf{“该族满足方程”与“该族是方程的通解”是不同要求。}

'''
s=s[:a]+new+s[a:];p.write_text(s,encoding='utf-8')
