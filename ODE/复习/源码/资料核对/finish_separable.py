from pathlib import Path
p=Path('ODE/复习/源码/review.tex');s=p.read_text(encoding='utf-8').replace('由于 $3+2\sin z>0$，此处分离不排除常值解。','由于 $3+2\sin z>0$，不存在常值 $z$ 解，此步除法不会漏解。');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/README.md');s=p.read_text(encoding='utf-8').replace('训练 14 页','训练 15 页').replace('为 15 页','为 17 页');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/资料核对/final_check.py');s=p.read_text(encoding='utf-8').replace('及真题导向补充，15 页','及真题导向补充，17 页').replace('训练题：55 道；','训练题：55 道，15 页；');p.write_text(s,encoding='utf-8')
old=Path('ODE/复习/期中训练题50题_截止3.1.pdf')
if old.exists():
 target=Path('ODE/复习/源码/build/旧版50题.pdf')
 if not target.exists():old.rename(target)
