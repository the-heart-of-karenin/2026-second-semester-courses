from pathlib import Path
r=Path('黎曼曲面 GTM81 翻译')
p=r/'LaTeX/sections/08.tex';s=p.read_text(encoding='utf-8-sig');s=s.replace('因此属于Galois群$\\operatorname{Aut}(\\MM(Y)/\\pi^*\\MM(X))$。','因此属于Galois群\n\\[\\operatorname{Aut}(\\MM(Y)/\\pi^*\\MM(X)).\\]');p.write_text(s,encoding='utf-8')
p=r/'LaTeX/sections/22.tex';s=p.read_text(encoding='utf-8-sig');s=s.replace('故$u$为全纯函数$\\frac1{2\\pi i}\\int_{|\\zeta|=R}F(z,\\zeta)f(\\zeta)d\\zeta/\\zeta$的实部，因而调和。留数定理给$\\frac1{2\\pi}\\int_0^{2\\pi}P(z,Re^{i\\theta})d\\theta=1$。固定$\\zeta_0$在边界，则','故$u$为全纯函数\n\\[\\frac1{2\\pi i}\\int_{|\\zeta|=R}F(z,\\zeta)f(\\zeta)\\frac{d\\zeta}{\\zeta}\\]\n的实部，因而调和。留数定理给\n\\[\\frac1{2\\pi}\\int_0^{2\\pi}P(z,Re^{i\\theta})d\\theta=1.\\]\n固定$\\zeta_0$在边界，则');p.write_text(s,encoding='utf-8')
p=r/'LaTeX/sections/29.tex';s=p.read_text(encoding='utf-8-sig').replace('令$\\psi(\\eta,\\xi):=\\beta\\xi$，则$\\psi$紧。','令$\\psi(\\eta,\\xi):=\\beta\\xi$，则$\\psi$紧。\\translatornote{原文此处写作$\\beta(\\eta)$，但$\\beta$的定义域是1上闭链空间，故应为$\\beta(\\xi)$。}');p.write_text(s,encoding='utf-8')
p=r/'LaTeX/sections/appendix.tex';s=p.read_text(encoding='utf-8-sig').replace('若$A\\subset B\\subset E$为向量子空间','设$E$为局部凸拓扑向量空间。若$A\\subset B\\subset E$为向量子空间');p.write_text(s,encoding='utf-8')
p=r/'LaTeX/sections/31.tex';s=p.read_text(encoding='utf-8-sig').replace('若$S\\subset X$闭离散','设$X$为非紧黎曼曲面。若$S\\subset X$闭离散');p.write_text(s,encoding='utf-8')
for stem,title in [('appendix','附录'),('references','参考文献'),('symbols','符号索引'),('index','人名与主题索引'),('series','数学研究生教材丛书目录'),('publication','原版书名页与出版资料'),('preface','前言')]:
 p=r/f'LaTeX/sections/{stem}.tex';s=p.read_text(encoding='utf-8-sig').replace('\\chapter*{'+title+'}','\\chapter*{'+title+'}\n\\markboth{'+title+'}{'+title+'}')
 p.write_text(s,encoding='utf-8')
# Update build scope to explicitly include all back matter.
p=r/'tools/build.py';s=p.read_text(encoding='utf-8-sig').replace("'scope':'累计至§'+str(max(int(x.stem) for x in (root/'LaTeX/sections').glob('*.tex') if x.stem.isdigit()))","'scope':'全书：§1—§31、全部习题、附录、参考文献、索引、出版资料及丛书目录'")
p.write_text(s,encoding='utf-8')
