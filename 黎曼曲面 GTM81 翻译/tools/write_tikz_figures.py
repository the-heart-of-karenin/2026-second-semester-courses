from pathlib import Path
import shutil
r=Path('黎曼曲面 GTM81 翻译');out=r/'LaTeX/figures/tikz';out.mkdir(exist_ok=True)
backup=r/'备份';backup.mkdir(exist_ok=True)
p=backup/'黎曼曲面讲义_中文译稿_重绘前.pdf'
if not p.exists():shutil.copy2(r/'黎曼曲面讲义_中文译稿.pdf',p)
head=r'''\documentclass[tikz,border=7pt]{standalone}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows.meta,patterns,decorations.markings,calc}
\tikzset{outline/.style={line width=.7pt,line cap=round,line join=round},
 map/.style={outline,-{Stealth[length=2.1mm,width=1.5mm]}},
 point/.style={circle,draw,fill=white,inner sep=1.4pt,line width=.6pt},
 along/.style={postaction={decorate},decoration={markings,mark=at position .52 with {\arrow{Stealth[length=1.8mm,width=1.2mm]}}}}}
\begin{document}
\begin{tikzpicture}[font=\normalsize]
'''
end='\n\\end{tikzpicture}\n\\end{document}\n'
figs={}
figs[1]=r'''
\def\leftregion{(-.15,2.15) .. controls (-1.4,1.55) and (-2.65,2.05) .. (-2.7,2.75) .. controls (-3.9,3.3) and (-3.25,4.7) .. (-2.15,4.7) .. controls (-1.15,4.95) and (-.4,4.2) .. (.2,3.8) .. controls (.85,3.2) and (.65,2.75) .. (-.15,2.15) -- cycle}
\def\rightregion{(-.9,3.45) .. controls (-.6,4.05) and (.8,4.8) .. (1.65,4.75) .. controls (3.2,4.9) and (3.8,3.8) .. (3.45,2.7) .. controls (3.1,2.2) and (2.6,2.7) .. (1.9,2.5) .. controls (.7,2.05) and (.25,2.35) .. (-.15,2.65) .. controls (-.55,2.95) and (-1.1,2.9) .. (-.9,3.45) -- cycle}
\begin{scope}\clip \leftregion;\fill[pattern=north east lines,pattern color=black!45] \rightregion;\end{scope}
\draw[outline] \leftregion;\draw[outline] \rightregion;
\node at (-2,4.25) {$U_1$};\node at (1.8,4.25) {$U_2$};
\node[fill=white,inner sep=1.5pt] at (-.18,3.35) {$U_1\cap U_2$};
\draw[outline] (-2,-.35) ellipse (1.8 and 1.05);
\draw[outline] (2.3,-.35) ellipse (1.8 and 1.05);
\begin{scope}\clip (-2,-.35) ellipse (1.8 and 1.05);
\fill[pattern=north east lines,pattern color=black!45] (-.75,.7) .. controls (-1.65,.05) and (-.7,-.5) .. (-1.1,-1.4) -- (.1,-1.4) -- (.1,.8) -- cycle;
\draw[outline] (-.75,.7) .. controls (-1.65,.05) and (-.7,-.5) .. (-1.1,-1.4);\end{scope}
\begin{scope}\clip (2.3,-.35) ellipse (1.8 and 1.05);
\fill[pattern=north east lines,pattern color=black!45] (.8,.7) .. controls (1.65,.1) and (1.35,-.7) .. (.95,-1.4) -- (.1,-1.4) -- (.1,.8) -- cycle;
\draw[outline] (.8,.7) .. controls (1.65,.1) and (1.35,-.7) .. (.95,-1.4);\end{scope}
\node at (-2.7,-.92) {$V_1$};\node at (2.5,-.92) {$V_2$};
\draw[map] (-2.05,2.65) .. controls (-2.8,1.5) and (-2.65,.8) .. (-2.45,.12) node[pos=.55,left] {$\varphi_1$};
\draw[map] (2.2,2.9) .. controls (2.95,1.95) and (2.55,.9) .. (2.58,.13) node[pos=.56,right] {$\varphi_2$};
\draw[map] (-1.08,-.2) -- (1.08,-.2) node[midway,above=5pt,fill=white,inner sep=1pt] {$\varphi_2\circ\varphi_1^{-1}$};
'''
figs[2]=r'''
\begin{scope}[x={(1.65cm,.42cm)},y={(-.22cm,1.12cm)}]
\foreach \j in {-1,...,3}{\draw[line width=.4pt,black!65] (-1.25,\j)--(2.3,\j);}
\foreach \i in {-1,...,2}{\draw[line width=.4pt,black!65] (\i,-1.25)--(\i,3.25);}
\draw[map,line width=1.1pt] (0,0)--(1,0);
\draw[map,line width=1.1pt] (0,0)--(0,1);
\foreach \i in {-1,...,2}{\foreach \j in {-1,...,3}{\node[point] at (\i,\j) {};}}
\node[below right=1pt] at (0,0) {$0$};
\node[right=4pt] at (1,0) {$\omega_1$};
\node[right=4pt] at (0,1) {$\omega_2$};
\node[right=4pt] at (1,1) {$\omega_1+\omega_2$};
\node[below right=2pt] at (0,-1) {$-\omega_2$};
\node[right=4pt] at (1,-1) {$\omega_1-\omega_2$};
\end{scope}
'''
figs[3]=r'''
\coordinate (a) at (0,0);\coordinate (b) at (6,2.7);
\foreach \s in {0,.2,.4,.6,.8,1}{
\pgfmathsetmacro{\h}{-2.1+4.2*\s}
\draw[line width=.45pt,black!65] (a) .. controls (1.5,\h) and (4.35,{2.7+\h}) .. (b);}
\draw[outline] (a) .. controls (1.5,-2.1) and (4.35,.6) .. (b);
\draw[outline] (a) .. controls (1.5,2.1) and (4.35,4.8) .. (b);
\node[fill=white,inner sep=2pt] at (3.9,1.1) {$u_0$};
\node[fill=white,inner sep=2pt] at (2.2,2.8) {$u_1$};
\node[fill=white,inner sep=2pt] at (2.9,1.6) {$u_s$};
\node[point,label=left:$a$] at (a) {};\node[point,label=right:$b$] at (b) {};
'''
figs[4]=r'''
\foreach \s in {0,.2,.4,.6,.8,1}{
\pgfmathsetmacro{\x}{1.65*\s}\pgfmathsetmacro{\y}{.65*\s}
\draw[line width=.4pt,black!65] (\x,\y) .. controls ({\x+1}, {\y-.8}) and ({\x+3.5},{\y-.5}) .. ({\x+3.65},{\y+1.25}) .. controls ({\x+3.7},{\y+3.4}) and ({\x+.8},{\y+3.4}) .. (\x,\y);}
\foreach \s in {0,1}{
\pgfmathsetmacro{\x}{1.65*\s}\pgfmathsetmacro{\y}{.65*\s}
\draw[outline,along] (\x,\y) .. controls ({\x+1}, {\y-.8}) and ({\x+3.5},{\y-.5}) .. ({\x+3.65},{\y+1.25}) .. controls ({\x+3.7},{\y+3.4}) and ({\x+.8},{\y+3.4}) .. (\x,\y);}
\draw[map] (0,0)--(1.65,.65) node[pos=.52,below=4pt] {$w$};
\draw[map] (1.57,.8)--(.12,.23) node[pos=.5,above=3pt] {$w^{-}$};
\node[point,label=below left:$a$] at (0,0) {};
\node[point,label=above left:$b$] at (1.65,.65) {};
\node[fill=white,inner sep=1pt] at (3.52,1.52) {$u_0$};
\node[right] at (5.32,2.02) {$u_1$};
'''
figs[5]=r'''
\draw[outline] (-.75,.4) .. controls (-.9,1.55) and (.9,1.4) .. (1.55,.35) .. controls (2.05,-.65) and (.8,-1.5) .. (-.15,-.9) .. controls (-.5,-.5) and (-.65,-.2) .. (-.75,.4) -- cycle;
\draw[outline] (1.2,-.15) .. controls (.8,1.65) and (1.65,2.5) .. (2.65,1.6) .. controls (3.25,1) and (4.1,-.35) .. (3.6,-.55) .. controls (3.05,-.7) and (2.45,-1.1) .. (1.7,-.75) .. controls (1.35,-.6) and (1.3,-.35) .. (1.2,-.15) -- cycle;
\draw[outline] (2.45,1.7) .. controls (2.15,2.9) and (3.7,3.45) .. (4.7,2.2) .. controls (5.2,1.6) and (5.6,.2) .. (4.9,-.2) .. controls (4.25,-.65) and (3.25,.45) .. (3.85,.65) .. controls (4.8,.95) and (2.8,.25) .. (2.45,1.7) -- cycle;
\draw[outline] (4.1,2.3) .. controls (3.85,3.35) and (4.7,4.1) .. (5.8,3.9) .. controls (7.15,3.7) and (7.5,2.3) .. (6.5,1.75) .. controls (5.65,1.2) and (4.4,1.4) .. (4.1,2.3) -- cycle;
\draw[outline] (.15,.2) .. controls (1.1,-.5) and (2.2,.65) .. (3.3,1.35) .. controls (4.25,1.95) and (5.3,2.6) .. (6.15,2.5);
\node[point] at (.15,.2) {};\node[above left=2pt] at (.15,.2) {$a=u(0)$};
\node[point] at (6.15,2.5) {};\node[above=4pt] at (6.15,2.5) {$b=u(1)$};
\node at (-.05,1.05) {$U_1$};\node at (1.7,1.9) {$U_2$};\node at (3.25,2.7) {$U_3$};\node at (5.25,3.5) {$U_4$};
\node[point] at (1.45,.04) {};\node[above=4pt,fill=white,inner sep=1pt] at (1.45,.04) {$u(t_1)$};
\node[point] at (2.73,.97) {};\node[below=5pt,fill=white,inner sep=1pt] at (2.73,.97) {$u(t_2)$};
\node[point] at (4.23,1.94) {};\node[above left=2pt,fill=white,inner sep=1pt] at (4.23,1.94) {$u(t_3)$};
'''
figs[6]=r'''
\def\region{(0,0) .. controls (-.9,.9) and (-1.5,1.8) .. (-2.7,1.35) .. controls (-4.25,.9) and (-5,-1) .. (-3.8,-2) .. controls (-3.3,-2.5) and (-2.7,-2.3) .. (-2.25,-3.2) .. controls (-1.25,-4.15) and (.45,-3.35) .. (.65,-2.25) .. controls (.95,-1.25) and (.65,-.65) .. (0,0) -- cycle}
\fill[pattern=north east lines,pattern color=black!40] \region;
\draw[outline] \region;
\draw[outline] (1.25,1.25) circle[radius=1.76777];
\node at (-2.45,.6) {$Y$};\node at (1.25,2.48) {$D$};
\draw[line width=.45pt,black!65] (0,0)--(1.25,1.25);
\node[point,label=below left:$a$] at (0,0) {};
\draw[outline] (.555,.625)--(.695,.625) (.625,.555)--(.625,.695);
\draw[outline] (1.18,1.25)--(1.32,1.25) (1.25,1.18)--(1.25,1.32);
\node[right=4pt] at (.625,.625) {$c$};\node[right=4pt] at (1.25,1.25) {$m$};
'''
for n,body in figs.items():(out/f'fig{n:02}.tex').write_text(head+body+end,encoding='utf-8')
