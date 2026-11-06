from pathlib import Path
import json,argparse
from PIL import Image, ImageChops

work=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--current',default='qa_round3')
parser.add_argument('--previous',default='qa_round2')
args=parser.parse_args()
current=work/args.current
previous=work/args.previous
pages=sorted(current.glob('page-*.png'),key=lambda p:int(p.stem.split('-')[1]))
same=[];changed=[]
for path in pages:
    number=int(path.stem.split('-')[1])
    old=previous/path.name
    identical=False
    if old.exists():
        with Image.open(old) as before,Image.open(path) as after:
            identical=before.size==after.size and ImageChops.difference(before.convert('RGB'),after.convert('RGB')).getbbox() is None
    (same if identical else changed).append(number)
report={'total_pages':len(pages),'identical_to_previously_inspected_pages':same,'new_or_changed_pages_requiring_visual_inspection':changed}
(current/'visual-delta.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report))
