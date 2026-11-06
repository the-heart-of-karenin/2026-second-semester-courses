from pathlib import Path
import re
p=Path('ODE/复习/源码/review.tex');s=p.read_text(encoding='utf-8')
a=s.index(r'\subsection{微分方程模型}');b=s.index(r'\subsection{微分方程概念}',a)
s=s[:a]+r'\setcounter{subsection}{1}'+'\n'+s[b:]
a=s.index(r'\point{8. ');b=s.index(r'\section{第二章',a)
s=s[:a]+s[b:]
assert len(re.findall(r'\\point\{',s))==49
assert r'\point{2.' in s and r'\point{9.' in s
p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/README.md');s=p.read_text(encoding='utf-8').replace('51 个知识点','49 个知识点（保留原编号）');s+='\n本轮依用户截图删除复习重点第 1 条整节及第 8 条；其余知识点编号不变，第一章保留 1.2、1.3 节号。训练题未修改。\n';p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/资料核对/final_check.py');s=p.read_text(encoding='utf-8').replace("review))==51","review))==49").replace('51 个知识点','49 个知识点（保留原编号）').replace('Verified 51 points','Verified 49 points');p.write_text(s,encoding='utf-8')
