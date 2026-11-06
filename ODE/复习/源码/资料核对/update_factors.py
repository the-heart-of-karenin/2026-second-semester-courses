from pathlib import Path
p=Path('ODE/复习/源码/review.tex');s=p.read_text(encoding='utf-8');a=s.index(r'\point{25.');b=s.index(r'\point{27.',a)
s=s[:a]+r'''\point{25. 积分因子的一般方程与两个特殊结论}{factor}
+\core 设 $M,N\in C^1(D)$，在单连通开区域 $D$ 上考虑
+\[
+M(t,x)\dd t+N(t,x)\dd x=0.
+\]
+处处非零的 $C^1$ 函数 $\mu$ 为积分因子的充要条件是
+\[
+(\mu M)_x=(\mu N)_t,
+\qquad M\mu_x-N\mu_t=(N_t-M_x)\mu.
+\]
+
+\textbf{特殊结论一：只依赖自变量 $t$ 的积分因子。}
+若 $N\ne0$，且
+\[
+\frac{M_x(t,x)-N_t(t,x)}{N(t,x)}=h(t)
+\]
+是仅依赖 $t$ 的连续函数，则存在只依赖 $t$ 的积分因子，可取
+\[
+\boxed{\mu(t)=\exp\!\left(\int_{t_0}^t h(s)\dd s\right).}
+\]
+其对应的一元方程为 $\mu'(t)/\mu(t)=h(t)$。反之，若存在只依赖 $t$ 的非零 $C^1$ 积分因子，则上述商在 $N\ne0$ 处必为 $\mu'(t)/\mu(t)$，因而只依赖 $t$。
+
+\textbf{特殊结论二：只依赖未知量 $x$ 的积分因子。}
+若 $M\ne0$，且
+\[
+\frac{N_t(t,x)-M_x(t,x)}{M(t,x)}=g(x)
+\]
+是仅依赖 $x$ 的连续函数，则存在只依赖 $x$ 的积分因子，可取
+\[
+\boxed{\mu(x)=\exp\!\left(\int_{x_0}^x g(u)\dd u\right).}
+\]
+其对应的一元方程为 $\mu'(x)/\mu(x)=g(x)$。反之，若存在只依赖 $x$ 的非零 $C^1$ 积分因子，则上述商在 $M\ne0$ 处必为 $\mu'(x)/\mu(x)$，因而只依赖 $x$。
+
+\textbf{适用条件。}两式中的 $t_0,x_0$ 分别取在所讨论的变量区间内；积分因子可乘任意非零常数。若分母在区域内有零点，应使用不作除法的条件
+\[
+M_x-N_t=N h(t)\quad\text{或}\quad N_t-M_x=M g(x)
+\]
+检验其能否在整个区域成立，并确认 $h$ 或 $g$ 在相应区间连续。原方程的定义域限制始终保留；乘因子不能将原式无定义的点变成原方程的解。
+
+'''.replace('\n+','\n')+s[b:]
p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/README.md');s=p.read_text(encoding='utf-8').replace('49 个知识点','48 个知识点');s+='\n依本轮要求删除复习第 26 条（复合形式积分因子），其余编号保留。第 25 条分别列出只依赖 t、只依赖 x 的积分因子判据与公式。训练题本轮未修改。\n';p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/资料核对/final_check.py');s=p.read_text(encoding='utf-8').replace('review))==49','review))==48').replace('49 个知识点','48 个知识点').replace('Verified 49 points','Verified 48 points');p.write_text(s,encoding='utf-8')
