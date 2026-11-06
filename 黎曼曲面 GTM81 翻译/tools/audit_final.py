from pathlib import Path
import re,json,pymupdf as fitz
root=Path('黎曼曲面 GTM81 翻译')
log=(root/'LaTeX/build/main.log').read_text(encoding='utf-8',errors='replace')
for l in log.splitlines():
 if any(x in l for x in ['Overfull','Missing character','undefined','Warning']):print(l)
doc=fitz.open(root/'黎曼曲面讲义_中文译稿.pdf')
print('PDF pages:',len(doc))
print('size', (root/'黎曼曲面讲义_中文译稿.pdf').stat().st_size)
for n in range(1,32):
 s=(root/f'LaTeX/sections/{n:02}.tex').read_text(encoding='utf-8-sig')
 entries=re.findall(r'\\entry\{'+str(n)+r'\.(\d+)\}',s)
 body=s.split('\\subsection*{习题')[0]
 nums=[int(x) for x in re.findall(r'\\entry\{'+str(n)+r'\.(\d+)\}',body)]
 print(n,len(s),nums,'ex',len(entries)-len(nums))
qa=root/'source/final-qa';qa.mkdir(exist_ok=True)
# search pages with images and selected section headings
keys=['27.6','29.13','31.5','13.3','14.4','17.9','19.2','图1','图2','图3','图4','图5','图6','符号索引','数学研究生教材丛书目录']
for key in keys:
 hits=[i+1 for i,p in enumerate(doc) if key in p.get_text()]
 print(key,hits)
# render selected pages after inspecting list
(root/'source/final-qa/pdf-text.txt').write_text('\n\n'.join(f'PDF PAGE {i+1}\n'+p.get_text() for i,p in enumerate(doc)),encoding='utf-8')
