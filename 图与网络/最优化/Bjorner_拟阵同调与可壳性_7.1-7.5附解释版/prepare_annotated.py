from pathlib import Path
import hashlib,json,re,shutil
B=Path(__file__).resolve().parent
SOURCE=B.with_name('Bjorner_拟阵同调与可壳性_7.1-7.5中文译本')
# Each anchor is preserved verbatim. The red text follows it inline.
notes={
1:[
('它编码了 $\\Delta$ 的基本组合不变量。',r'这里的思路是先把复形分块，再把各块的信息集中到一个多项式中。'),
('作为应用，我们将导出若干拟阵不等式。',r'这些不等式主要来自壳多项式系数的非负性。'),
],
2:[
('若所有刻面等势，称复形为\\textbf{纯}的。',r'（因此纯 $(r-1)$ 维复形的每个刻面都有 $r$ 个顶点。）'),
('令 $f_k$ 为基数为 $k$ 的面的个数。',r'（这里按顶点个数计数，故边计入 $f_2$，三角形计入 $f_3$。）'),
('而奇数基数面一样多，故',r''),
('是其若干极大真面的非空并。',r'也就是说，新刻面沿若干完整的余维一面贴入，而不是只沿孤立的低维面贴入。'),
('称为壳序诱导的 $F_i$ 的\\textbf{限制面}。',r'（删去其中任一顶点后，剩下的面都已在先前出现。）'),
('是 $F_i$ 中唯一极小的“新”面，即属于 $\\Delta_i-\\Delta_{i-1}$ 的极小面。',r'换言之，本步新增的恰是 $F_i$ 中包含整个 $\\RR(F_i)$ 的那些子面。'),
('由命题7.2.2，$f_{r-k}=\\sum_i\\binom{|F_i-\\RR(F_i)|}{k}$。',r'这是因为每块中的面必须保留限制面；要得到大小为 $r-k$ 的面，只需从其余顶点中删去 $k$ 个。'),
('故所有 $h_k\\ge0$。',r'（$h_k$ 按限制面的大小计数，$f_k$ 则按面的大小计数。）'),
('其后的 $h_{k+1},\\ldots,h_r$ 也均为零，故 $(\\alpha)\\Rightarrow(\\delta)$。',r'若存在更大的限制面，反复使用引理删去元素就会得到大小为 $k$ 的限制面，与 $h_k=0$ 矛盾。'),
],
3:[
('称为\\textbf{拟阵复形}。',r'（刻面恰是拟阵的基，所以所有刻面的大小都等于秩 $r$。）'),
('则 $B\\cup p$ 含唯一回路 $\\ci(B,p)$；',r'（$B\\cup p$ 表示 $B\\cup\\{p\\}$，下文 $B-b$ 类似表示删去单个元素。）'),
('唯一余回路（bond）$\\bo(B,b)$。',r'（余回路就是对偶拟阵的回路。）'),
('有限步后得到所需的 $A=A_k$。',r'每次基的字典序都严格下降，而基的个数有限，因此过程必定终止。'),
('且顶点的每个排序都诱导壳序。',r'这里要求每个排序都成立；仅有一个排序给出壳序，并不足以刻画拟阵。'),
('否则称内被动。',r'（由引理7.3.1，内被动意味着该元素可被某个更小的基外元素替换。）'),
('当且仅当 $b$ 在 $B$ 中内被动。',r'确实，替换成更小元素便得到字典序更早的基；反过来，更早的基也提供这样的替换。'),
('区间 $[\\IP(B),S-\\EP(B)]$ 划分布尔代数 $2^S$。',r'在这个区间中，内被动元素必须保留，外被动元素必须排除，其余元素可自由选取；这里也包括相关集。'),
('特别地，Tutte多项式与 $S$ 的次序无关。',r'因为右侧只使用秩函数，并未使用次序；由对偶秩公式，第二个指数还可写成 $|A|-r(A)$。'),
],
4:[
('所得集合称为断路。',r'例如回路 $\\{1,2,3\\}$ 在 $1<2<3$ 下给出断路 $\\{2,3\\}$；它本身独立，却被断路复形额外排除。'),
('断路复形 $\\BC_\\omega(M)$ 与 $\\BC_{\\bar\\omega}(\\bar M)$ 同构。',r'若 $x<y$ 平行，则 $\\{x,y\\}$ 是回路，$\\{y\\}$ 是断路，故每个平行类只留下最小代表。'),
('若 $X\\subseteq S$ 不含断路，则更不含回路，因此独立。',r'因为任一回路都包含删去其最小元素所得到的断路。'),
('因此所有nbc基都含 $e$，得到(iii)、(iv)。',r'任一面都包含于某个nbc基，因而也能加入 $e$ 而仍是面，这正是锥的性质。'),
('而 $B$ 不含断路当且仅当 $e(B)=0$，所以',r'（在 $T_M(x,y)$ 中令 $y=0$，恰好只保留外活性为零的基。）'),
('约化断路复形的壳多项式为',r'（删去的最小元素 $e$ 在每个nbc基中都是内活跃的，故壳多项式少一个因子 $x$）'),
('令 $\\nbc(x)=\\{A\\in\\BC_\\omega(M):\\bar A=x\\}$，则',r'（$\\bar A$ 是 $A$ 的闭包，即它张成的平坦集；这里把面按闭包分类）'),
('需要拟阵 $M(S)$ 的\\textbf{beta不变量}',r'（这是拟阵的不变量，勿与一般的 Betti 数混淆）'),
('(ii)由锥性质立即得到。',r'这里 $\\chi$ 始终表示约化欧拉示性数，所以锥的值为零。'),
],
5:[
('基数 $b(M)=I_r$ 尤其令人关注。',r'围长为 $c$ 意味着大小小于 $c$ 的子集都独立，这会确定 $h$ 向量的前若干项。'),
('在命题7.2.5中令 $\\Delta=\\IN(M)$ 即得不等式。',r'具体地，取其中的 $e=c-1$；在(7.5)中保留已确定的项，并舍去其余非负项即可。'),
('它们组成自由子拟阵 $B_{r-c+1}$。',r'（余圈元属于每个基；自由拟阵的所有子集均独立。）'),
('现在转向断路复形的面数。',r'最小断路的大小为 $c-1$，因此已确定的初始 $h_i$ 比独立复形少一项；这解释了下文求和上限从 $c-1$ 变为 $c-2$。'),
('再由',r''),
]
}
# Empty entries are not used; they serve no insertion role.
notes={i:[(a,n.replace(chr(92)*2,chr(92))) for a,n in ns if n] for i,ns in notes.items()}
def han(s):return len(re.findall(r'[\u3400-\u9fff]',s))
def main():
 baseline={};orig_count=added_count=0
 for i in range(1,6):
  name=f'section7{i}.tex';original=(SOURCE/name).read_text(encoding='utf-8');current=original
  baseline[name]=hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
  for anchor,note in notes[i]:
   assert original.count(anchor)==1,(name,anchor,original.count(anchor))
   current=current.replace(anchor,anchor+r'\redinsert{'+note+'}',1)
   added_count+=han(note)
  # Match inserted macros, including their nested TeX braces, exactly.
  recovered=current
  for _,note in notes[i]:recovered=recovered.replace(r'\redinsert{'+note+'}','',1)
  assert recovered==original
  (B/name).write_text(current,encoding='utf-8');orig_count+=han(original)
 cover='本版在原译文句间和括号中插入红色解释；红色文字不属于作者原文。'
 added_count+=han(cover)
 ratio=added_count/orig_count;assert ratio<=.2,ratio
 s=(SOURCE/'main.tex').read_text(encoding='utf-8')
 s=s.replace(r'\begin{document}',r'\newcommand{\redinsert}[1]{{\color{red}#1}}'+'\n'+r'\begin{document}',1)
 s=s.replace('第7.1--7.5节中文译本\\par','第7.1--7.5节中文译本（附解释版）\\par')
 s=s.replace(r'\end{minipage}',r'\redinsert{'+cover+'}\n'+r'\end{minipage}',1)
 (B/'main.tex').write_text(s,encoding='utf-8')
 report=dict(original_project=str(SOURCE),original_han_chars=orig_count,added_han_chars=added_count,ratio=ratio,notes=sum(map(len,notes.values())),original_body_preserved=True,style='inline red insertions',source_sha256=baseline)
 (B/'build/annotation-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 (B/'README.md').write_text('# 第7.1--7.5节附解释版\n\n所有新增内容以 redinsert 宏在原文句间或括号中插入，统一显示为红色。原译文正文逐字保留，原项目不改动。prepare_annotated.py 可重建插入版并核对正文完整性，build.py 编译 PDF。统计见 build/annotation-audit.json。\n',encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
