---
name: html-extractor
description: >-
  Convert saved HTML pages into clean, readable, extractable Markdown — especially
  when a naive tag-strip loses content. Use when a saved web page, exported report,
  or research deliverable (.html) must become .md and it contains any of: KaTeX/MathML
  math, numbers or equations rendered as inline images (common in Google Docs/PDF
  exports), or JavaScript-app shells like Google Gemini / Angular Material where the
  real content is buried in component markup. Triggers: "convert this html to
  markdown", "the formulas/numbers aren't selectable", "extract the report from this
  saved page", "the equations are images".
---

# html-extractor

Turn a saved `.html` page into clean Markdown that preserves the parts plain
extraction usually drops: **math**, **image-rendered numbers/formulas**, **tables**,
and the **actual content of JS-rendered app pages**.

## When to use

- A saved web page or exported report needs to become readable/searchable `.md`.
- Copy/paste or a naive `strip-tags` gives text with **holes** where numbers,
  percentages, or equations should be — they were rendered as `<img>` or KaTeX.
- The page is a **Google Gemini / Google Docs / Angular** export wrapped in app
  chrome (scripts, sidebars, citation chips) and you only want the report body.

## Scripts

Both live in `scripts/`. `html_to_md.py` is **stdlib-only**. `image_formula_ocr.py`
needs `tesseract`, ImageMagick (`convert`/`montage`), and Pillow.

### 1. `html_to_md.py` — the converter

```
python scripts/html_to_md.py INPUT.html -o OUT.md [options]
```

| Option | Use it when |
|---|---|
| (none) | Normal page — converts headings, paragraphs, lists, tables, bold/italic. |
| `--panels` | Google Gemini / Angular save — keeps only the rendered response panels (`markdown markdown-main-panel`) and discards the app shell. |
| `--img-map FILE` | Numbers/formulas are images — substitutes each `<img>` with text from a TSV/JSON map (produce it with script 2). |
| `--heading-offset N` | Push every heading down N levels (e.g. so the doc has one top `#`). |
| `--drop-citations` | Strip `<sup>` citation markers instead of keeping them as `[n]`. |

Math is automatic: KaTeX `data-math` is recovered to inline `$...$` and block `$$...$$`.

### 2. `image_formula_ocr.py` — for image-rendered numbers/formulas

```
python scripts/image_formula_ocr.py IMAGES_DIR -o ocr.tsv --montage check.png
```

OCRs each PNG (upscaled, `tesseract --psm 7`) into a `filename<TAB>text` TSV, and
optionally builds a labeled contact sheet so you can eyeball/verify. OCR is reliable
on digits, weaker on math symbols (subscripts, ×, ∩, λ) — **always spot-check the
TSV against the contact sheet before trusting it.**

## Recommended workflow

**Plain or math-heavy page (incl. Gemini):**

```
python scripts/html_to_md.py page.html --panels -o report.md
```

**Page where numbers/equations are images** (the `images/` folder sits next to the html):

```
# 1) OCR the image formulas + make a sheet to check
python scripts/image_formula_ocr.py ./images -o ocr.tsv --montage check.png
# 2) open check.png, correct any wrong rows in ocr.tsv by hand
# 3) build the markdown with the values substituted in
python scripts/html_to_md.py report.html --img-map ocr.tsv -o report.md
```

## Verify before declaring done

- `grep -c '$' OUT.md` and confirm display equations survived (e.g. `grep frac`).
- Confirm no leftover holes: scan for double spaces / blanks where numbers belong;
  if numbers are still missing, the page is image-based — run script 2.
- For `--panels`, confirm headings look like the report, not nav/sidebar text.

## Limits

- Recovers math only when the page stored it as KaTeX `data-math` or MathML; math
  baked purely into a raster image needs script 2 (OCR) and hand-correction.
- `WebFetch` returns un-rendered HTML for JS apps; save the fully-rendered page from
  the browser first, then run this skill on the local file.
