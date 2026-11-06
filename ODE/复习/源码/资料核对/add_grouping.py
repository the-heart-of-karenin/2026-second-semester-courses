from pathlib import Path
p=Path('ODE/复习/源码/review.tex');s=p.read_text(encoding='utf-8');a=s.index(r'\subsection{2.4') if r'\subsection{2.4' in s else s.index(r'\subsection{隐式微分方程}')
s=s[:a]+r'''
\textbf{分组求积分因子：需寻找一个对两组同时适用的因子。}
记 $\omega=\omega_1+\omega_2$，$\omega_i=P_i\dd x+Q_i\dd y$，且已知
\[
\dd\Phi_1=\mu_1\omega_1,\qquad \dd\Phi_2=\mu_2\omega_2.
\]
若能找到连续单变量函数 $f,g$，使同一处处非零函数满足
\[
\boxed{\mu=\mu_1 f(\Phi_1)=\mu_2 g(\Phi_2),}
\]
且乘积具有所需的 $C^1$ 正则性，则
\[
\mu\omega=f(\Phi_1)\dd\Phi_1+g(\Phi_2)\dd\Phi_2
=\dd\!\left[\int^{\Phi_1}f(u)\dd u+\int^{\Phi_2}g(v)\dd v\right].
\]
因此 $\mu$ 是整体的积分因子。这是一个\textbf{充分条件}；只知道两组分别有因子，并没有完成整体因子的构造，尤其不能直接把 $\mu_1\mu_2$ 当作整体因子，也不能无条件断言存在全区域非零因子。

\textbf{常用可操作形式：}若能将比值分解为
\[
\frac{\mu_1}{\mu_2}=A(\Phi_1)B(\Phi_2),\qquad A,B\ne0,
\]
则取 $f=1/A,g=B$，可得
\[
\boxed{\mu=\frac{\mu_1}{A(\Phi_1)}=\mu_2B(\Phi_2).}
\]
上述公式只在各函数有定义、因子非零且等式成立的区域使用。

\textbf{例（用户提供）：}$ (x^3y-2y^2)\dd x+x^4\dd y=0$。
在 $xy\ne0$ 上分组为
\[
\omega_1=x^3y\dd x+x^4\dd y=x^3\dd(xy),\qquad
\omega_2=-2y^2\dd x.
\]
可取 $\mu_1=x^{-3},\Phi_1=xy$ 以及 $\mu_2=-1/(2y^2),\Phi_2=x$。此时
\[
\frac{\mu_1}{\mu_2}=-\frac{2y^2}{x^3}
=(xy)^2\left(-\frac2{x^5}\right),
\]
故 $A(u)=u^2,B(v)=-2/v^5$，整体积分因子为
\[
\boxed{\mu(x,y)=\frac1{x^5y^2}.}
\]
乘回原式，得到
\[
\frac{\dd(xy)}{(xy)^2}-\frac2{x^5}\dd x
=\dd\!\left(-\frac1{xy}+\frac1{2x^4}\right)=0.
\]
通积分可写为 $1/(xy)-1/(2x^4)=C$，即
\[
y=\frac{2x^3}{1+2Cx^4},\qquad x\ne0,\quad 1+2Cx^4\ne0.
\]
另外 $y\equiv0$ 是原方程的解，须单独补回。若考察跨过 $x=0$ 的解，原式在该点退化，须在原方程中另验，不能直接使用此处奇异的积分因子。

'''+s[a:]
s=s.replace('27. 积分因子的非唯一性与比值','27. 积分因子的非唯一性、比值与分组法').replace('训练题 55 题','训练题 57 题');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/standard_questions.py');s=p.read_text(encoding='utf-8');s=s.replace('    return problems',r'''
    more=[
        ('一阶微分方程',r"求方程 $(t^2+3)\cos x\,\dfrac{\dd x}{\dd t}+2t\sin x=t(t^2+3)$ 的通积分，并在实数范围内写出局部显式解的分支条件。",'教材习题 2.2 第 1(3) 题（增加分支条件问）','教材书 p.33 / PDF p.43'),
        ('积分因子与通积分',r"求方程 $(x^3y-2y^2)\dd x+x^4\dd y=0$ 在 $xy\ne0$ 区域内的一个积分因子及通积分，并确定在 $x\ne0$ 的区间上是否存在恒等于零的解。",'用户提供题目','本次对话所给方程（末项按 $x^4\dd y$ 理解）')]
    for topic,text,source,loc in more:
        problems.append(dict(group='G. 线性化与积分因子补充（2 题）',source=source,page='',location=loc,topic=topic,text=text,note=''))
    return problems''');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/make_training.py');s=p.read_text(encoding='utf-8').replace('len(problems)==55','len(problems)==57').replace('训练题 55 题','训练题 57 题').replace('全册 55 题','全册 57 题').replace('另附 2.1 节补充题 5 题。','另附 2.1 节补充题 5 题、线性化与积分因子补充题 2 题。').replace('Generated 55','Generated 57');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/build.py');s=p.read_text(encoding='utf-8').replace('期中训练题55题','期中训练题57题');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/资料核对/final_check.py');s=p.read_text(encoding='utf-8').replace('training))==55','training))==57').replace('len(rows)==55','len(rows)==57').replace('range(1,56)','range(1,58)').replace('55 exercises','57 exercises').replace('55 道，15 页','57 道').replace('55 条','57 条');p.write_text(s,encoding='utf-8')
