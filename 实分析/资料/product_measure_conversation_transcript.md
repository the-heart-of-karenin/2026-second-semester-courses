# 对话记录：乘积测度、外测度、可测切片与 Fubini 定理

> 说明：本记录只保留用户与助手的可见对话内容。原始 PDF 文件不附在记录中；对话中出现的图片均改写为文字/公式。

---

## 用户

【图片文字】

> On the rectangles we define the function \(\mu_0\) by
> \[
> \mu_0(A\times B)=\mu_1(A)\mu_2(B).
> \]
> Now the fact that \(\mu_0\) has a unique extension to the algebra \(\mathcal A\) for which \(\mu_0\) becomes a premeasure is a consequence of the following fact: whenever a rectangle \(A\times B\) is the disjoint union of a countable collection of rectangles \(\{A_j\times B_j\}\),
> \[
> A\times B=\bigcup_{j=1}^{\infty}A_j\times B_j,
> \]
> then
> \[
> \mu_0(A\times B)=\sum_{j=1}^{\infty}\mu_0(A_j\times B_j). \tag{6}
> \]
>
> To prove this, observe that if \(x_1\in A\), then for each \(x_2\in B\) the point \((x_1,x_2)\) belongs to exactly one \(A_j\times B_j\). Therefore \(B\) is the disjoint union of the \(B_j\) for which \(x_1\in A_j\). By countable additivity of \(\mu_2\),
> \[
> \chi_A(x_1)\mu_2(B)
> =
> \sum_{j=1}^{\infty}\chi_{A_j}(x_1)\mu_2(B_j).
> \]

【另一张图片文字】

> We then let \(\mathcal A\) denote the collection of all sets in \(X\) that are finite unions of disjoint measurable rectangles. It is easy to check that \(\mathcal A\) is an algebra of subsets of \(X\). (Indeed, the complement of a measurable rectangle is the union of three disjoint such rectangles, while the union of two measurable rectangles is the disjoint union of at most six such rectangles.) From now on we abbreviate our terminology by referring to measurable rectangles simply as “rectangles.”

在定义乘积测度的时候，\(\mathcal A\) 只是有限个 rectangle 的并，那么第一张图片在证明什么？为什么要把 \(A\times B\) 拆成可数个并（而不是有限个）？

---

## 助手

对，关键就在这里：**“\(\mathcal A\) 中的集合是有限个 rectangle 的并”**，并不意味着我们只需要证明有限可加性。第一张图实际上是在为“\(\mu_0\) 是一个 premeasure”做准备，而 premeasure 要求的是**可数可加性**。

书里的构造可以分成三个层次看：

\[
\text{rectangles}
\longrightarrow
\mathcal A=\{\text{有限个互不相交 rectangles 的并}\}
\longrightarrow
\sigma(\mathcal A).
\]

书先在单个 rectangle 上定义

\[
\mu_0(A\times B)=\mu_1(A)\mu_2(B).
\]

然后希望把它扩张到 \(\mathcal A\)，最后再用 extension theorem 扩张到 \(\sigma(\mathcal A)\)。

### 最容易混淆的一点

“\(\mathcal A\) 是有限个 rectangles 的并”说的是：

\[
E=R_1\sqcup\cdots\sqcup R_N.
\]

它**绝对不意味着** \(E\) 不能同时写成可数个 rectangles 的并。

例如一个 rectangle \(A\times B\) 本身当然属于 \(\mathcal A\)，甚至只需要 1 个 rectangle。

但假设

\[
B=\bigsqcup_{j=1}^{\infty}B_j,
\]

那么同时又有

\[
A\times B
=
\bigsqcup_{j=1}^{\infty}(A\times B_j).
\]

所以同一个属于 \(\mathcal A\) 的集合，可以一方面是“有限个 rectangle 的并”（甚至一个），另一方面又被拆成**可数无穷个** rectangle。

第一张图就是在证明这种情况下

\[
\mu_0(A\times B)
=
\sum_{j=1}^{\infty}
\mu_0(A_j\times B_j).
\]

为什么非得证明这个，而不能只证明有限个呢？因为 **premeasure 的定义本身就是可数可加的**。

在 algebra \(\mathcal A\) 上，一个 premeasure \(\mu_0\) 要满足：

如果

\[
E_1,E_2,\ldots\in\mathcal A
\]

两两不交，并且

\[
E=\bigsqcup_{n=1}^{\infty}E_n
\]

碰巧仍然属于 \(\mathcal A\)，那么必须有

\[
\mu_0(E)=\sum_{n=1}^{\infty}\mu_0(E_n).
\]

注意这里并没有要求 \(\mathcal A\) 对可数并封闭。通常

\[
\bigcup_{n=1}^{\infty}E_n
\]

可能不在 \(\mathcal A\)。**但只要这次可数并碰巧落回 \(\mathcal A\)，就必须满足可数可加性。**

这正是“algebra”和“premeasure”两个概念的区别：

\[
\begin{array}{c|c}
\mathcal A\text{ 是 algebra} & \text{集合运算层面的性质}\\
\hline
\mu_0\text{ 是 premeasure} & \text{测度函数层面的性质}
\end{array}
\]

---

## 用户

【图片文字】

> For later use we record the following observation about the premeasure \(\mu_0\) on the algebra \(\mathcal A\) and the resulting measure \(\mu_*\) that is implicit in the argument given above. The details of the proof may be left to the reader.
>
> We define \(\mathcal A_\sigma\) as the collection of sets that are countable unions of sets in \(\mathcal A\), and \(\mathcal A_{\sigma\delta}\) as the sets that arise as countable intersections of sets in \(\mathcal A_\sigma\).
>
> **Proposition 1.6** For any set \(E\) and any \(\epsilon>0\), there are sets \(E_1\in\mathcal A_\sigma\) and \(E_2\in\mathcal A_{\sigma\delta}\), such that
> \[
> E\subset E_1,\qquad E\subset E_2,
> \]
> and
> \[
> \mu_*(E_1)\le \mu_*(E)+\epsilon,
> \qquad
> \mu_*(E_2)=\mu_*(E).
> \]

告诉我：1. 这里的“外逼近”“内逼近”是否本质上是一样的，也就是对于 \(\mathcal A_\sigma\) 集合能任意小外逼近和内逼近（只要考虑被逼近集合取补集）

---

## 助手

不完全是。这里有一个很重要的区分：

**集合论意义上，外逼近和内逼近确实通过取补集互为对偶；但测度意义上的“误差可以任意小”并不总能仅靠取补集自动得到。**

而且你截图里的 Proposition 1.6 其实**只在讲外逼近**，不是一外一内。因为它找的是

\[
E\subset E_1,\qquad E\subset E_2.
\]

两者都是从外面包住 \(E\)。

如果

\[
E\subset G,
\]

那么

\[
G^c\subset E^c.
\]

所以集合关系上

\[
\text{\(E\) 的外逼近}
\Longleftrightarrow
\text{\(E^c\) 的内逼近}.
\]

但有两个问题。

第一，逼近集合所属的类会变。如果

\[
G\in\mathcal A_\sigma,
\]

则

\[
G^c\in\mathcal A_\delta,
\]

一般不一定仍然属于 \(\mathcal A_\sigma\)。

第二，测度误差通过补集转换时要小心无穷测度。如果总空间有无限测度，可能出现 \(\infty-\infty\) 的问题。

不过如果 \(E\in\mathcal A_\sigma\)，本身就有直接的内逼近：写成

\[
E=\bigcup_{n=1}^{\infty}A_n,\qquad A_n\in\mathcal A,
\]

令

\[
F_n=A_1\cup\cdots\cup A_n,
\]

则

\[
F_n\uparrow E.
\]

如果 \(\mu(E)<\infty\)，则

\[
\mu(F_n)\uparrow \mu(E),
\]

所以可以从内部用 \(\mathcal A\) 中的集合任意逼近。

---

## 用户

2. 查找这个命题在之前有没有论述，尤其是 \(\mathbb R^d\) 上的部分。

---

## 助手

有，而且 Chapter 1 的 \(\mathbb R^d\) 情形基本上已经把 Proposition 1.6 的思想都出现过了。

最直接的是 Chapter 1 的外测度正则性：

\[
m^*(E)
=
\inf\{m^*(O):E\subset O,\ O\text{ open}\}.
\]

也就是说，对任意 \(\varepsilon>0\)，存在 open \(O\supset E\)，使得

\[
m^*(O)\le m^*(E)+\varepsilon.
\]

这和抽象版本

\[
E\subset E_1\in\mathcal A_\sigma,\qquad
\mu^*(E_1)\le \mu^*(E)+\varepsilon
\]

是同一结构。

在 \(\mathbb R^d\) 中，每个 open set 都可以写成可数个 almost disjoint cubes 的并，因此 open set 对应抽象框架中的 \(\mathcal A_\sigma\)。

进一步，对每个 \(n\) 取 open \(O_n\supset E\) 满足

\[
m^*(O_n)\le m^*(E)+\frac1n,
\]

令

\[
G=\bigcap_{n=1}^{\infty}O_n,
\]

则 \(G\) 是 \(G_\delta\)，并且

\[
E\subset G,\qquad m^*(G)=m^*(E).
\]

这和

\[
E\subset E_2\in\mathcal A_{\sigma\delta},
\qquad
\mu^*(E_2)=\mu^*(E)
\]

完全对应。

---

## 用户

这个论述能直接搬到我们这里来吗？假如可以，给出证明。假如不行，解释。

---

## 助手

可以，而且这里几乎就是把 \(\mathbb R^d\) 中那个论证的骨架原样搬过来。只是不能把“open set”字面搬过来，因为抽象空间 \(X\) 没有拓扑；要把它替换成 \(\mathcal A_\sigma\)。

外测度定义为

\[
\mu^*(E)
=
\inf\left\{
\sum_{j=1}^{\infty}\mu_0(A_j):
E\subset\bigcup_{j=1}^{\infty}A_j,\ A_j\in\mathcal A
\right\}.
\]

### 第一部分：\(\varepsilon\)-外逼近

若 \(\mu^*(E)<\infty\)，由定义可取 \(A_j\in\mathcal A\) 使得

\[
E\subset\bigcup_{j=1}^{\infty}A_j
\]

且

\[
\sum_{j=1}^{\infty}\mu_0(A_j)
\le
\mu^*(E)+\varepsilon.
\]

令

\[
E_1=\bigcup_{j=1}^{\infty}A_j.
\]

则

\[
E_1\in\mathcal A_\sigma,\qquad E\subset E_1,
\]

并且

\[
\mu^*(E_1)
\le
\sum_{j=1}^{\infty}\mu_0(A_j)
\le
\mu^*(E)+\varepsilon.
\]

### 第二部分：精确外包络

对每个 \(n\)，取

\[
E_n\in\mathcal A_\sigma,\qquad E\subset E_n,
\]

且

\[
\mu^*(E_n)\le \mu^*(E)+\frac1n.
\]

定义

\[
E_2=\bigcap_{n=1}^{\infty}E_n.
\]

那么

\[
E_2\in\mathcal A_{\sigma\delta},
\qquad
E\subset E_2.
\]

由单调性，

\[
\mu^*(E)\le \mu^*(E_2)\le \mu^*(E_n)
\le \mu^*(E)+\frac1n.
\]

令 \(n\to\infty\)，得到

\[
\mu^*(E_2)=\mu^*(E).
\]

---

## 用户

【图片文字】

> **Proposition 3.1** If \(E\) belongs to \(\mathcal A_{\sigma\delta}\), then \(E^{x_2}\) is \(\mu_1\)-measurable for every \(x_2\); moreover, \(\mu_1(E^{x_2})\) is a \(\mu_2\)-measurable function. In addition
> \[
> \int_{X_2}\mu_1(E^{x_2})\,d\mu_2
> =
> (\mu_1\times\mu_2)(E). \tag{7}
> \]
>
> Proof. One notes first that all the assertions hold immediately when \(E\) is a measurable rectangle. Next suppose \(E\) is a set in \(\mathcal A_\sigma\). Then we can decompose it as a countable union of disjoint rectangles \(E_j\). ...

这里我们把 \(E\) 写成可数 rectangle 的 union，是不是首先分成 \(\mathcal A\) 中元素的并，然后把 \(\mathcal A\) 中元素分成每个有限份？先解释这个。

---

## 助手

是的，你理解的顺序基本正确。这里作者把中间两三步压缩成了一句话。

因为

\[
E\in\mathcal A_\sigma,
\]

所以首先存在

\[
F_n\in\mathcal A,\qquad
E=\bigcup_{n=1}^{\infty}F_n.
\]

而每个 \(F_n\in\mathcal A\) 都是有限个互不相交 rectangles 的并：

\[
F_n=\bigsqcup_{k=1}^{N_n}R_{n,k}.
\]

于是

\[
E
=
\bigcup_{n=1}^{\infty}
\bigcup_{k=1}^{N_n}R_{n,k}.
\]

因为可数多个有限集的并仍然可数，可以重新编号：

\[
E=\bigcup_{j=1}^{\infty}R_j.
\]

但这些 \(R_j\) 还不一定彼此不交。

所以再做 disjointization：

\[
D_1=R_1,\qquad
D_j
=
R_j-\bigcup_{k<j}R_k.
\]

则

\[
E=\bigsqcup_{j=1}^{\infty}D_j.
\]

每个 \(D_j\in\mathcal A\)，所以又可以拆成有限个 disjoint rectangles。重新编号之后得到

\[
E=\bigsqcup_{m=1}^{\infty}E_m,
\]

其中每个 \(E_m\) 真正都是 rectangle。

---

## 用户

“We then let \(\mathcal A\) denote the collection of all sets in \(X\) that are finite unions of disjoint measurable rectangles.”

能不能一开始的时候就定义为可数并？可数并的话能形成一个 sigma 代数吗？

---

## 助手

可以定义，但**通常不能直接把它当成 \(\sigma\)-代数**。

如果定义

\[
\mathcal C
=
\left\{
\text{可数个两两不交 measurable rectangles 的并}
\right\},
\]

它基本就是书后面记的 \(\mathcal A_\sigma\)。

它对可数并是封闭的，但一般**不对补集封闭**。

例如在

\[
X_1=X_2=\mathbb R
\]

里考虑对角线

\[
\Delta=\{(x,x):x\in\mathbb R\}.
\]

它的补集可以写成可数个 rectangles 的并，例如利用有理数分割：

\[
\Delta^c
=
\bigcup_{q\in\mathbb Q}
\Big(
(-\infty,q)\times(q,\infty)
\cup
(q,\infty)\times(-\infty,q)
\Big).
\]

所以

\[
\Delta^c\in\mathcal C.
\]

但 \(\Delta\notin\mathcal C\)。

因为任何满足

\[
A\times B\subset \Delta
\]

的非空 rectangle 都只能是单点

\[
\{x\}\times\{x\}.
\]

可数个这样的 rectangle 最多覆盖对角线上的可数多个点，不可能覆盖整个不可数的 \(\Delta\)。

因此

\[
\Delta^c\in\mathcal C,
\qquad
\Delta\notin\mathcal C.
\]

所以 \(\mathcal C\) 不是 \(\sigma\)-代数。

---

## 用户

【图片文字】

> Then for each \(x_2\) we have
> \[
> E^{x_2}=\bigcup_{j=1}^{\infty}E_j^{x_2},
> \]
> and we observe that \(\{E_j^{x_2}\}\) are disjoint sets. Thus by (7) applied to each rectangle \(E_j\) and the monotone convergence theorem we get our conclusion for each set \(E\in\mathcal A_\sigma\).

monotone convergence theorem 上一次出现介绍的地方。

---

## 助手

最近一次在第六章中正式重新列出的地方，是 Chapter 6, Section 2，书本页 275：

如果

\[
f_n\uparrow f,\qquad f_n\ge0,
\]

则

\[
\lim_{n\to\infty}\int f_n\,d\mu
=
\int f\,d\mu.
\]

如果问最早正式介绍并证明的地方，则是在 Chapter 2, Section 1，书本页 62，Corollary 1.9：

\[
f_n\uparrow f
\quad\Longrightarrow\quad
\lim_{n\to\infty}\int f_n=\int f.
\]

紧接着 Corollary 1.10 给出：

\[
\int\sum_{k=1}^{\infty}a_k
=
\sum_{k=1}^{\infty}\int a_k,
\qquad a_k\ge0.
\]

你这里实际用的正是这个“把无穷和与积分交换”的形式。

---

## 用户

告诉我：在第六章的时候是不是省略了对于积分的具体构造（比如为什么可测函数在可测集合上面有积分）？

---

## 助手

是的。**第六章这里基本省略了积分从头到尾的具体构造**，因为作者明确说 Chapter 1 关于可测函数的结果以及 Chapter 2 的整个积分理论都可以几乎逐字搬到一般测度空间，所以不再重复证明，只列主要结论。

第六章只提醒：

若 \(f\ge0\) 可测，就存在简单函数

\[
\phi_k\uparrow f.
\]

然后直接说 Chapter 2 从 simple functions 开始的 four-step construction 在一般 \(\sigma\)-finite measure space 上照样成立。

所以更准确地说：

- 若 \(f\ge0\) 可测，则 \(\int f\,d\mu\) 总可以定义，值允许为 \(+\infty\)；
- 一般实值可测函数要写成
  \[
  f=f^+-f^-;
  \]
- 若正负两部分同时为 \(+\infty\)，则不能定义成 \(+\infty-\infty\)；
- 若
  \[
  \int |f|\,d\mu<\infty,
  \]
  才称为 integrable。

在可测集 \(E\) 上积分定义为

\[
\int_E f\,d\mu
:=
\int_X f\chi_E\,d\mu.
\]

---

## 用户

【图片文字】

> **Proposition 3.2** If \(E\) is an arbitrary measurable set in \(X\), then the conclusion of Proposition 3.1 are still valid except that we only assert that \(E^{x_2}\) is \(\mu_1\)-measurable and \(\mu_1(E^{x_2})\) is defined for almost every \(x_2\in X_2\).

这里 assert 之后的东西都是假设吗？

---

## 助手

不是。这里的 **assert** 是“断言 / 声称 / 得出结论”的意思，不是“假设”。

真正的假设只有：

\[
E\text{ is an arbitrary measurable set in }X.
\]

assert 后面的内容是较弱的结论：

\[
E^{x_2}\text{ is }\mu_1\text{-measurable for a.e. }x_2,
\]

以及

\[
\mu_1(E^{x_2})\text{ is defined for a.e. }x_2.
\]

---

## 用户

\(E^{x_2}\) is \(\mu_1\)-measurable and \(\mu_1(E^{x_2})\) is defined，这两个是不是一个东西？

---

## 助手

在这本书的语境里，二者几乎是同一件事，但逻辑上不是完全同一个陈述。

因为

\[
\mu_1:\mathcal M_1\to[0,\infty]
\]

只定义在 \(\mu_1\)-measurable sets 上。

所以

\[
E^{x_2}\text{ is }\mu_1\text{-measurable}
\Longrightarrow
\mu_1(E^{x_2})\text{ is defined}.
\]

这里 “defined” 不表示有限；可能

\[
\mu_1(E^{x_2})=+\infty.
\]

作者把第二句单独写出来，是为了后面把

\[
x_2\mapsto \mu_1(E^{x_2})
\]

当作函数来积分。

---

## 用户

Theorem 3.3 In the setting above, suppose \(f(x_1,x_2)\) is an integrable function on \((X_1\times X_2,\mu_1\times\mu_2)\).

(i) For almost every \(x_2\in X_2\), the slice
\[
f_{x_2}(x_1)=f(x_1,x_2)
\]
is integrable on \((X_1,\mu_1)\).

(ii)
\[
\int_{X_1}f(x_1,x_2)\,d\mu_1
\]
is an integrable function on \(X_2\).

(iii)
\[
\int_{X_2}\left(\int_{X_1}f(x_1,x_2)\,d\mu_1\right)d\mu_2
=
\int_{X_1\times X_2}f\,d(\mu_1\times\mu_2).
\]

这里定理 3.3 是不是基本使用之前的两个 proposition 就能证出来了？

---

## 助手

是的，**Theorem 3.3 基本就是把 Proposition 3.2 从特征函数推广到一般 integrable function**。

证明链条是：

\[
\text{Prop. 3.2}
\Rightarrow
\chi_E
\Rightarrow
\text{simple functions}
\Rightarrow
f\ge0
\Rightarrow
\text{general integrable }f.
\]

先看 \(f=\chi_E\)，其中 \(E\) measurable 且

\[
(\mu_1\times\mu_2)(E)<\infty.
\]

Proposition 3.2 已经给出切片可测性和

\[
\int_{X_2}\mu_1(E^{x_2})\,d\mu_2
=
(\mu_1\times\mu_2)(E).
\]

而

\[
(\chi_E)^{x_2}
=
\chi_{E^{x_2}},
\]

所以

\[
\int_{X_1}(\chi_E)^{x_2}\,d\mu_1
=
\mu_1(E^{x_2}).
\]

然后推广到 simple function，再用 monotone convergence theorem 推到非负可测函数。

最后一般 integrable \(f\) 写成

\[
f=f^+-f^-.
\]

由于

\[
\int |f|<\infty,
\]

所以 \(f^+\) 和 \(f^-\) 都是 non-negative integrable functions。分别应用刚才的结果，再相减，就得到 Theorem 3.3。

严格地说，Theorem 3.3 直接调用的核心是 Proposition 3.2；而 Proposition 3.1 是 Proposition 3.2 的技术基础。

---

## 用户

把对话记录输出出来。不用输出原始 pdf，但是把图片换成文字。
