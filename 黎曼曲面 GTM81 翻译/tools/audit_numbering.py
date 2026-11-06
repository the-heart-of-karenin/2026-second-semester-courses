from pathlib import Path
import re,json
r=Path('黎曼曲面 GTM81 翻译')
src='\n'.join((r/f'source/page-{i:03}.txt').read_text(encoding='utf-8-sig') for i in range(10,245))
report=[]
for n in range(1,32):
 nums=[int(x) for x in re.findall(r'(?m)^'+str(n)+r'\s*\.\s*(\d+)\.',src)]
 tex=(r/f'LaTeX/sections/{n:02}.tex').read_text(encoding='utf-8-sig')
 parts=tex.split('\\subsection*{习题')
 body=[int(x) for x in re.findall(r'\\entry\{'+str(n)+r'\.(\d+)\}',parts[0])]
 ex=[int(x) for x in re.findall(r'\\entry\{'+str(n)+r'\.(\d+)\}',parts[-1])] if len(parts)>1 else []
 report.append(dict(section=n,body_count=len(body),exercise_count=len(ex),source_detected_max=max(nums,default=0),source_detected_numbers=nums,body_contiguous=body==list(range(1,len(body)+1)),exercises_contiguous=ex==list(range(1,len(ex)+1))))
print(json.dumps(report,ensure_ascii=False,indent=1))
(r/'source/final-qa/numbering-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('TOTAL',sum(x['body_count'] for x in report),sum(x['exercise_count'] for x in report))
