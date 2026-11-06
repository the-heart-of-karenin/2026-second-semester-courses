from pathlib import Path
import zipfile,json
roots=[Path('D:/Users/xwechat_files/wxid_82yue0f6x8a722_a33b/msg/file/2026-10/常微分方程期中试卷.zip'),Path('D:/Users/xwechat_files/wxid_82yue0f6x8a722_a33b/temp/RWTemp/2026-10/c152a1c3d45fd637e4c6f83a8ed1fd8f/2023-2024 第 1 学期 常微分方程期中考试及部分题目答案.zip')]
out=Path('ODE/历年试题');out.mkdir(exist_ok=True)
rows=[]
for k,p in enumerate(roots,1):
 z=zipfile.ZipFile(p)
 for j,i in enumerate(z.infolist()):
  if i.is_dir():continue
  ext=Path(i.filename).suffix
  target=out/f'paper{k}-{j:02}{ext}'
  target.write_bytes(z.read(i))
  rows.append({'archive':p.name,'entry':i.filename,'saved':target.name})
  print(k,j,ext,i.file_size)
(out/'archive_map.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
