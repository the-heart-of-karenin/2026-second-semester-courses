"""Build the two selected Chinese translations with XeLaTeX.

Run from any directory: python build.py [samper|bjorner|all]
Requires a TeX installation with ctex and XeLaTeX (Windows fonts).
"""
from pathlib import Path
import argparse
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "源码"
TARGETS = {
    "samper": "Samper_有序单纯复形的拟拟阵类_中文选译.pdf",
    "bjorner": "Bjorner_拓扑方法_第6、7、9、11节_中文选译.pdf",
}

def build(name):
    destination = ROOT / "build" / name
    destination.mkdir(parents=True, exist_ok=True)
    command = ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
               "-file-line-error", "-output-directory=" + str(destination), name + ".tex"]
    for _ in range(2):
        result = subprocess.run(command, cwd=SOURCES, capture_output=True)
        (destination / "console.log").write_bytes(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f"Compilation failed; see {destination / 'console.log'}")
    output = ROOT / "output" / "pdf" / TARGETS[name]
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(destination / (name + ".pdf"), output)
    print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", choices=[*TARGETS, "all"], default="all")
    args = parser.parse_args()
    for target in TARGETS if args.target == "all" else [args.target]:
        build(target)
