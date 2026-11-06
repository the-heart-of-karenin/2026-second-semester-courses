from pathlib import Path
p=Path('ODE/复习/源码/review.tex');s=p.read_text(encoding='utf-8').replace('《训练题 57 题》','《训练题》');p.write_text(s,encoding='utf-8')
old=Path('ODE/复习/期中训练题57题_截止3.1.pdf');target=Path('ODE/复习/源码/build/旧版57题.pdf')
if old.exists() and not target.exists():old.rename(target)
