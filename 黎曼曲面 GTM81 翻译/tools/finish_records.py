from pathlib import Path
r=Path('黎曼曲面 GTM81 翻译')
p=r/'LaTeX/sections/27.tex';s=p.read_text(encoding='utf-8-sig').replace('［提示：考虑$f_\\nu(z)=f(2^{-\\nu}z)$并用27.1。］','［提示：考虑$f_\\nu(z)=f(2^{-\\nu}z)$并用27.1。］\\translatornote{原文写$f_\\nu:U\\to\\C$、$f_\\nu(z)=f(2^\\nu z)$。对于固定穿孔圆盘$U$，后式一般未在整个$U$上定义；此处将指数改为$-\\nu$。}')
p.write_text(s,encoding='utf-8')
terms={
'holomorphic de Rham group':'全纯de Rham群','schlicht function':'单叶函数','elliptic Riemann surface':'椭圆型黎曼曲面','parabolic Riemann surface':'抛物型黎曼曲面','hyperbolic Riemann surface':'双曲型黎曼曲面','crossed homomorphism':'交叉同态','G-module':'G模','vector bundle':'向量丛','line bundle':'线丛','local trivialization':'局部平凡化','linear chart':'线性坐标卡','transition function':'转移函数','holomorphic section':'全纯截面','meromorphic section':'亚纯截面','canonical line bundle':'典范线丛','holomorphic cotangent bundle':'全纯余切丛','holomorphic subbundle':'全纯子丛','multiplicatively automorphic':'乘法自守','factor of automorphy':'自守因子','partition of unity':'单位分解','locally convex space':'局部凸空间','compact mapping':'紧映射','completely continuous mapping':'完全连续映射'}
p=r/'术语表.tsv';s=p.read_text(encoding='utf-8-sig');known={line.split('\t')[0] for line in s.splitlines()};s+='\n'+''.join(k+'\t'+v+'\n' for k,v in terms.items() if k not in known);p.write_text(s,encoding='utf-8')
import json
mapping={'source_pdf_pages':262,'numbering':'PDF pages are one-based; printed pages refer to original book','ranges':[{'printed_start':1,'printed_end':235,'pdf_offset':9},{'printed_start':237,'printed_end':241,'pdf_offset':8},{'printed_start':243,'printed_end':245,'pdf_offset':7},{'printed_start':247,'printed_end':254,'pdf_offset':6}],'preface':{'vii':8,'viii':9},'unnumbered':{'series_front':[2,3],'title':4,'publication':5,'original_contents':[6,7],'series_back':[261,262]},'printed_blank_pages_not_in_source_pdf':[236,242,246]}
(r/'source/page-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf-8')
