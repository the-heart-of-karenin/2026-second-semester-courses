"""Extract text, verify numbering, and render page contact sheets for visual review."""
from pathlib import Path
import re
import subprocess
from pypdf import PdfReader
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output" / "pdf"
QA = ROOT / "build" / "检查"
QA.mkdir(parents=True, exist_ok=True)

for pdf in sorted(OUT.glob("*.pdf")):
    name = "bjorner" if pdf.name.startswith("Bjorner") else "samper"
    reader = PdfReader(pdf)
    texts = [page.extract_text() or "" for page in reader.pages]
    (QA / f"{name}-text.txt").write_text("\n\f\n".join(texts), encoding="utf-8")
    if any("\ufffd" in t for t in texts):
        raise ValueError(f"Replacement character in {pdf.name}")
    if name == "bjorner":
        required = [f"9.{i}" for i in [1,2,3,4,9,10,11,15,16,17,18,19,20]]
        required += [f"11.{i}" for i in range(1,15)]
        required += [f"9.{i}" for i in [5,6,7,8,12,13,14]]
    else:
        required = ["2.1", "2.2", "3.1", "3.2", "3.3", "3.4", "3.5"]
        required += [f"4.{i}" for i in range(1,15)]
    fulltext = "\n".join(texts)
    missing = [x for x in required if x not in fulltext]
    if missing:
        raise ValueError(f"Missing numbered items: {missing}")
    subprocess.run(["pdftoppm", "-scale-to", "1100", "-png", str(pdf),
                    str(QA / name)], check=True, capture_output=True)
    imgs = sorted(QA.glob(name + "-*.png"))
    columns, tile_w, tile_h = 4, 270, 405
    for start in range(0, len(imgs), 12):
        group = imgs[start:start+12]
        sheet = Image.new("RGB", (columns*tile_w, 3*tile_h), "#dddddd")
        draw = ImageDraw.Draw(sheet)
        for k, path in enumerate(group):
            img = Image.open(path).convert("RGB")
            img.thumbnail((tile_w-10, tile_h-25))
            x, y = (k%columns)*tile_w+5, (k//columns)*tile_h+20
            sheet.paste(img, (x,y))
            draw.text((x,y-17), str(start+k+1), fill="black")
        sheet.save(QA / f"contact-{name}-{start//12+1}.jpg", quality=92)
    print(name, "pages:", len(reader.pages), "characters:", sum(map(len,texts)),
          "numbered items:", len(required), "OK")
