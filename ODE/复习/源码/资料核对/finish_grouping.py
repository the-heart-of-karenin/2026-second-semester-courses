from pathlib import Path
p=Path('ODE/复习/README.md');s=p.read_text(encoding='utf-8').replace('期中训练题55题','期中训练题57题').replace('修订版，55 题','修订版，57 题').replace('为 17 页','为 18 页');s+='\n本轮第 27 条增加分组积分因子充分条件及用户例题的完整计算。题集增加第 56 题（习题 2.2 第 1(3) 题）与第 57 题（用户方程）；原题编号保留。当前复习 18 页，训练 57 题、15 页。后续追加题位于 `standard_questions.py` 的 `more`。\n';p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/资料核对/final_check.py');s=p.read_text(encoding='utf-8').replace('补充，17 页','补充，18 页');p.write_text(s,encoding='utf-8')
old=Path('ODE/复习/期中训练题55题_截止3.1.pdf');target=Path('ODE/复习/源码/build/旧版55题.pdf')
if old.exists() and not target.exists():old.rename(target)
