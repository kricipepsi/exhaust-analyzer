#!/usr/bin/env python3
"""
html_to_md.py — convert a saved HTML page into clean, readable, *extractable* Markdown.

Handles the cases that break naive "strip the tags" extraction:
  * KaTeX math  -> recovered from `data-math` attributes (inline `$...$`, block `$$...$$`)
  * Image-rendered numbers/formulas -> substituted from a map file (see image_formula_ocr.py)
  * JS-rendered exports (Google Gemini / Angular Material) -> optionally keep only the
    response panels (`--panels`) instead of the whole app shell
  * Tables, lists, headings, bold/italic, and citation superscripts

Stdlib only. Usage:
    python html_to_md.py INPUT.html -o OUTPUT.md
    python html_to_md.py page.html --panels -o report.md          # Gemini/Angular save
    python html_to_md.py report.html --img-map ocr.tsv -o out.md  # image-formula report
    python html_to_md.py in.html --heading-offset 1 --drop-citations -o out.md
"""
import re, html, argparse, sys, json, os

def load_img_map(path):
    """Accept TSV (filename<TAB>text) or JSON ({"image1.png": "62%"})."""
    if not path:
        return {}
    txt = open(path, encoding="utf-8").read()
    if path.lower().endswith(".json"):
        return {os.path.basename(k): v for k, v in json.loads(txt).items()}
    m = {}
    for line in txt.splitlines():
        if "\t" in line:
            k, v = line.split("\t", 1)
            m[os.path.basename(k.strip())] = v.strip()
    return m

def recover_math(s):
    """Replace KaTeX <span/div ... data-math="LATEX" ...>...</span|div> with $LATEX$ / $$LATEX$$."""
    out, i = [], 0
    pat = re.compile(r'<(span|div)[^>]*?data-math="([^"]*)"[^>]*>', re.I)
    while True:
        m = pat.search(s, i)
        if not m:
            out.append(s[i:]); break
        out.append(s[i:m.start()])
        tag, latex = m.group(1).lower(), html.unescape(m.group(2))
        depth, j = 0, len(s)
        for sm in re.finditer(r'<(/?)' + tag + r'\b[^>]*>', s[m.start():], re.I):
            depth += 1 if sm.group(1) == '' else -1
            if depth == 0:
                j = m.start() + sm.end(); break
        out.append(f'<p>$$ {latex} $$</p>' if tag == 'div' else f' ${latex}$ ')
        i = j
    return ''.join(out)

def substitute_images(s, imgmap):
    def rep(m):
        return ' ' + imgmap.get(os.path.basename(m.group(1)), '') + ' '
    return re.sub(r'<img[^>]*src="([^"]*)"[^>]*>', rep, s)

def match_block(s, start, tag):
    """Return inner html of the element starting at `start` (an opening <tag ...>)."""
    depth = 0
    for m in re.finditer(r'<(/?)' + tag + r'\b', s[start:], re.I):
        depth += 1 if m.group(1) == '' else -1
        if depth == 0:
            return s[s.index('>', start) + 1: start + m.start()]
    return s[start:start + 200000]

def extract_panels(s):
    """Keep only Angular/Gemini rendered response panels (class 'markdown markdown-main-panel')."""
    anchors = [m.start() for m in re.finditer(r'markdown markdown-main-panel', s)]
    if not anchors:
        return s
    starts = sorted({s.rfind('<div', 0, a) for a in anchors})
    return "\n".join(f'<div>{match_block(s, st, "div")}</div>' for st in starts)

def inline(t, drop_citations):
    t = re.sub(r'(?is)<(strong|b)\b[^>]*>(.*?)</\1>',
               lambda m: '**' + re.sub(r'<[^>]+>', '', m.group(2)).strip() + '**', t)
    t = re.sub(r'(?is)<(em|i)\b[^>]*>(.*?)</\1>',
               lambda m: '*' + re.sub(r'<[^>]+>', '', m.group(2)).strip() + '*', t)
    if drop_citations:
        t = re.sub(r'(?is)<sup\b[^>]*>.*?</sup>', '', t)
    else:
        t = re.sub(r'(?is)<sup\b[^>]*>\s*(\d+)\s*</sup>', r'[\1]', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    t = re.sub(r'[ \t\n]+', ' ', t).strip()
    t = re.sub(r'\s+([,.;:])', r'\1', t)
    t = re.sub(r'\*\*\s*\*\*', '', t)
    return t

def cell(t, drop):
    return inline(t, drop).replace('|', '\\|')

def convert(body, heading_offset, drop):
    out = []
    for m in re.finditer(r'(?is)<(h[1-6]|p|ul|ol|table)\b[^>]*>(.*?)</\1>', body):
        tag, b = m.group(1).lower(), m.group(2)
        if tag[0] == 'h':
            t = inline(b, drop)
            if t:
                out.append('\n' + '#' * min(int(tag[1]) + heading_offset, 6) + ' ' + t + '\n')
        elif tag == 'p':
            t = inline(b, drop)
            if t:
                out.append(t + '\n')
        elif tag in ('ul', 'ol'):
            for i, it in enumerate(re.findall(r'(?is)<li\b[^>]*>(.*?)</li>', b)):
                t = inline(it, drop)
                if t:
                    out.append((f'{i+1}. ' if tag == 'ol' else '- ') + t)
            out.append('')
        elif tag == 'table':
            grid = [[cell(c, drop) for c in re.findall(r'(?is)<t[dh]\b[^>]*>(.*?)</t[dh]>', r)]
                    for r in re.findall(r'(?is)<tr\b[^>]*>(.*?)</tr>', b)]
            grid = [g for g in grid if g]
            if not grid:
                continue
            nc = max(len(r) for r in grid)
            grid = [r + [''] * (nc - len(r)) for r in grid]
            out += ['', '| ' + ' | '.join(grid[0]) + ' |', '|' + '|'.join(['---'] * nc) + '|']
            for r in grid[1:]:
                out.append('| ' + ' | '.join(r) + ' |')
            out.append('')
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip()

def main():
    ap = argparse.ArgumentParser(description="Convert saved HTML to clean, extractable Markdown.")
    ap.add_argument("input")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--panels", action="store_true",
                    help="keep only Angular/Gemini response panels (for JS-app saves)")
    ap.add_argument("--img-map", help="TSV/JSON mapping image filename -> text (image-formula reports)")
    ap.add_argument("--heading-offset", type=int, default=0, help="add N to every heading level")
    ap.add_argument("--drop-citations", action="store_true", help="remove <sup> citation markers")
    a = ap.parse_args()

    raw = open(a.input, encoding="utf-8", errors="replace").read()
    raw = re.sub(r'(?is)<(script|style|head|svg)\b[^>]*>.*?</\1>', ' ', raw)
    raw = recover_math(raw)
    raw = substitute_images(raw, load_img_map(a.img_map))
    if a.panels:
        raw = extract_panels(raw)
    md = convert(raw, a.heading_offset, a.drop_citations)
    open(a.output, "w", encoding="utf-8").write(md + "\n")
    print(f"wrote {a.output}: {len(md.split())} words, "
          f"{md.count('|---')} table-cols, {md.count('$')//2} math spans", file=sys.stderr)

if __name__ == "__main__":
    main()
