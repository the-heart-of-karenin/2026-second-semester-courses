from pathlib import Path
r=Path('黎曼曲面 GTM81 翻译');d=r/'LaTeX/figures/tikz'
p=d/'fig03.tex';s=p.read_text(encoding='utf-8');s=s.replace('\\draw[outline] (a) .. controls (1.5,-2.1) and (4.35,.6) .. (b);','\\draw[outline] (a) .. controls (1.5,-2.1) and (4.35,.6) .. (b) node[pos=.67,below=5pt] {$u_0$};').replace('\\draw[outline] (a) .. controls (1.5,2.1) and (4.35,4.8) .. (b);','\\draw[outline] (a) .. controls (1.5,2.1) and (4.35,4.8) .. (b) node[pos=.35,above=5pt] {$u_1$};')
s=s.replace('\\node[fill=white,inner sep=2pt] at (3.9,1.1) {$u_0$};','').replace('\\node[fill=white,inner sep=2pt] at (2.2,2.8) {$u_1$};','').replace('\\node[fill=white,inner sep=2pt] at (2.9,1.6) {$u_s$};','\\node at (2.5,1.35) {$u_s$};');p.write_text(s,encoding='utf-8')
p=d/'fig04.tex';s=p.read_text(encoding='utf-8').replace('\\node[fill=white,inner sep=1pt] at (3.52,1.52) {$u_0$};','\\node at (3.18,1.55) {$u_0$};');p.write_text(s,encoding='utf-8')
p=d/'fig05.tex';s=p.read_text(encoding='utf-8')
s=s.replace('.. (3.3,1.35) .. controls','.. (3.3,1.35) coordinate[pos=.43] (t1) coordinate[pos=.83] (t2) .. controls').replace('.. (6.15,2.5);','.. (6.15,2.5) coordinate[pos=.35] (t3);')
s=s.replace('\\node[point] at (.15,.2) {};\\node[above left=2pt] at (.15,.2) {$a=u(0)$};','\\node[point] at (.15,.2) {};\\node at (.12,.55) {$a=u(0)$};')
s=s.replace('(-.05,1.05)','(.05,.92)').replace('(1.7,1.9)','(1.72,1.45)').replace('(3.25,2.7)','(3.2,2.35)')
s=s.replace('\\node[point] at (1.45,.04) {};\\node[above=4pt,fill=white,inner sep=1pt] at (1.45,.04) {$u(t_1)$};','\\node[point] at (t1) {};\\node[below right=3pt] at (t1) {$u(t_1)$};')
s=s.replace('\\node[point] at (2.73,.97) {};\\node[below=5pt,fill=white,inner sep=1pt] at (2.73,.97) {$u(t_2)$};','\\node[point] at (t2) {};\\node[above left=3pt] at (t2) {$u(t_2)$};')
s=s.replace('\\node[point] at (4.23,1.94) {};\\node[above left=2pt,fill=white,inner sep=1pt] at (4.23,1.94) {$u(t_3)$};','\\node[point] at (t3) {};\\node[above right=3pt] at (t3) {$u(t_3)$};')
p.write_text(s,encoding='utf-8')
# Replace only six graphic dependencies, preserving original crops.
for p in (r/'LaTeX/sections').glob('*.tex'):
 s=p.read_text(encoding='utf-8-sig');new=s
 for i in range(1,7):new=new.replace(f'figures/fig{i:02}.pdf',f'figures/fig{i:02}-tikz.pdf')
 if new!=s:p.write_text(new,encoding='utf-8')
p=r/'LaTeX/main.tex';s=p.read_text(encoding='utf-8').replace('插图沿用原图，图内标签保留。','六幅编号插图依据原图用TikZ重绘为矢量图，保留原有数学标记与图意。');p.write_text(s,encoding='utf-8')
# Build figures from editable TikZ sources whenever the book is rebuilt.
p=r/'tools/build.py';s=p.read_text(encoding='utf-8-sig').replace('import subprocess, shutil, tempfile, json, datetime, re','import subprocess, shutil, tempfile, json, datetime, re, sys');s=s.replace("root=Path(__file__).resolve().parents[1]","root=Path(__file__).resolve().parents[1]\nsubprocess.run([sys.executable,str(root/'tools/build_figures.py')],check=True)");p.write_text(s,encoding='utf-8')
