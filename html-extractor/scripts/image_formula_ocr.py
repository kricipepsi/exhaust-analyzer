#!/usr/bin/env python3
"""
image_formula_ocr.py — transcribe a folder of small formula/number PNGs into text.

For HTML/PDF exports (e.g. Google Docs) that render every number and equation as an
inline image: nothing in such a page is selectable or searchable. This script OCRs
each image so the values become text. Output is a TSV (filename<TAB>text) that you
can hand-correct and then feed to `html_to_md.py --img-map`.

Requires: tesseract, ImageMagick (`convert`/`montage`), Pillow.
  Linux:  apt-get install tesseract-ocr imagemagick && pip install pillow

Usage:
    python image_formula_ocr.py IMAGES_DIR -o ocr.tsv
    python image_formula_ocr.py IMAGES_DIR -o ocr.tsv --montage sheet.png  # also a contact sheet to eyeball
    python image_formula_ocr.py IMAGES_DIR -o ocr.tsv --upscale 4

WORKFLOW for an image-formula report:
    1. python image_formula_ocr.py ./images -o ocr.tsv --montage check.png
    2. open check.png, fix any wrong rows in ocr.tsv by eye (OCR is ~right on digits,
       weaker on math symbols like subscripts, ×, ∩, λ)
    3. python html_to_md.py report.html --img-map ocr.tsv -o report.md
"""
import argparse, subprocess, tempfile, os, glob, sys

def numkey(p):
    digits = ''.join(c for c in os.path.basename(p) if c.isdigit())
    return int(digits) if digits else 0

def ocr_one(path, upscale):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
        tmp = tf.name
    try:
        subprocess.run(["convert", path, "-resize", f"{upscale*100}%",
                        "-bordercolor", "white", "-border", "6", tmp],
                       check=True, capture_output=True)
        out = subprocess.run(["tesseract", tmp, "stdout", "--psm", "7"],
                             check=True, capture_output=True, text=True)
        return " ".join(out.stdout.split())
    finally:
        os.path.exists(tmp) and os.remove(tmp)

def main():
    ap = argparse.ArgumentParser(description="OCR a folder of formula/number PNGs to a TSV.")
    ap.add_argument("images_dir")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--upscale", type=int, default=3, help="enlarge factor before OCR (default 3)")
    ap.add_argument("--montage", help="also write a labeled contact sheet PNG to eyeball")
    ap.add_argument("--glob", default="*.png", help="image glob (default *.png)")
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.images_dir, a.glob)), key=numkey)
    if not files:
        sys.exit(f"no images matching {a.glob} in {a.images_dir}")

    rows = []
    for f in files:
        try:
            rows.append((os.path.basename(f), ocr_one(f, a.upscale)))
        except subprocess.CalledProcessError as e:
            sys.exit(f"tool failed on {f}: {e.stderr.decode() if e.stderr else e}")

    with open(a.output, "w", encoding="utf-8") as fh:
        for name, txt in rows:
            fh.write(f"{name}\t{txt}\n")
    print(f"wrote {a.output}: {len(rows)} images OCR'd", file=sys.stderr)

    if a.montage:
        subprocess.run(["montage", *files, "-label", "%f", "-tile", "6x",
                        "-geometry", "230x90", "-background", "white",
                        "-bordercolor", "#888", "-border", "1", "-pointsize", "13",
                        a.montage], check=True, capture_output=True)
        print(f"wrote contact sheet {a.montage}", file=sys.stderr)

if __name__ == "__main__":
    main()
