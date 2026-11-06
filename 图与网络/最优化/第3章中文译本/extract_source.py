"""从原书 PDF 提取第3章文本，供对照查阅；不会覆盖译稿。"""
from pathlib import Path
import argparse
from pypdf import PdfReader

BASE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("pdf", type=Path, help="原书第三版 PDF 的路径")
args = parser.parse_args()
reader = PdfReader(args.pdf)
target = BASE / "source"
target.mkdir(exist_ok=True)
for printed in range(49, 65):
    # 原书印刷第49页为 PDF 的第60页。
    text = reader.pages[printed + 10].extract_text()
    (target / f"p{printed}.txt").write_text(text or "", encoding="utf-8")
print("已提取原书第49–64页。")
