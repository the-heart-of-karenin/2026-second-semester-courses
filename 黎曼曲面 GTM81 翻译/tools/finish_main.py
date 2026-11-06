from pathlib import Path
p=Path('黎曼曲面 GTM81 翻译/LaTeX/main.tex')
s=p.read_text(encoding='utf-8-sig').replace('graphicx,enumitem,hyperref','graphicx,enumitem,longtable,multicol,hyperref')
s=s.replace('本稿已收入前言、第四次修订印刷补记、第一章和第二章全部内容，以及第三章引言和第22至26节（含习题），连续译至原书第206页。第27节起及其余未收入的书前书后资料尚未翻译。本稿已编译，未进行成品PDF视觉检查。','本稿已译完原书三章共31节及全部习题，收入前言、第四次修订印刷补记、附录、参考文献、符号索引、人名与主题索引，以及原版出版资料和丛书目录。原书目录以本译稿自动生成的目录对应呈现；书前与书末丛书目录合并列于书末。索引中的页码保留原书页码。\n\n本稿为完整初译稿，完成后对部分公式、编号、插图及排版进行抽查，尚未经逐句、逐公式的全书复核。具体抽查范围与修订见项目中的《校对记录》。')
s=s.replace('\\tableofcontents','\\input{sections/publication.tex}\n\\tableofcontents')
s=s.replace('\\end{document}','\\backmatter\n\\input{sections/appendix.tex}\n\\input{sections/references.tex}\n\\input{sections/symbols.tex}\n\\input{sections/index.tex}\n\\input{sections/series.tex}\n\\end{document}')
p.write_text(s,encoding='utf-8')
