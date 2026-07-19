---
name: md-prep
description: >
  Prepare any .md file for maximum readability by AI agents and human coders.
  Applies six structural rules: YAML frontmatter injection, heading normalization
  (max 3 levels), LaTeX equations with inline fallbacks, table-to-JSON conversion
  for conditional/state data, declarative replacement of ASCII diagrams, and
  mandatory language-tagged code fences. Produces an optimized .md file plus a
  _PREP_REPORT.md summarising every change made.
  Use whenever a .md file must be ingested by an LLM, used as agent reference
  material, or needs to be unambiguous for a coder reading it as documentation.
  Trigger on: "prep this md", "optimize this markdown", "clean up this wiki",
  "make this readable for agents", "prepare doc for LLM", "fix this markdown",
  "this md needs cleanup", any request to improve or standardize a .md file.
allowed-tools: Read, Write, Edit, Bash
metadata:
  version: "1.0"
  domain: universal
---

## Purpose

A .md file that looks fine in a rendered preview can silently lose information
when an LLM tokenizes it — broken equations, split table rows, orphaned code
symbols. This skill applies six deterministic rules that eliminate those failure
modes without changing semantic content.

**Success criteria for a prepared file:**
- A cold LLM can parse every section without ambiguity
- A coder reading raw text (not rendered) can follow every formula and diagram
- Token count is equal to or lower than the original
- Zero information loss — every fact survives the transformation

---

## Step 0 — Identify the input

Accept the file path from `$ARGUMENTS`. If none given, ask the user for it.
Read the file. Check its byte size:

```bash
wc -c "$INPUT_FILE"
wc -l "$INPUT_FILE"
```

If the file exceeds 300 KB (~75 000 tokens), **split it first** — see
`references/split-strategy.md`. Do not optimize a file that is too large
to remain in perfect-recall range; splitting is the correct first step.

---

## Step 1 — Run the automated baseline

```bash
python3 scripts/optimize_markdown.py "$INPUT_FILE" "$OUTPUT_FILE"
```

The script handles:
- YAML frontmatter injection (title, token estimate, key concepts, TOC)
- Heading hierarchy normalization (flags skipped levels)
- Noise removal (redundant blank lines, stray horizontal rules)
- Identification of diagram and equation candidates (logged as `suggested_fixes`)

Read the JSON report it writes to `<output>.report.json`. The `suggested_fixes`
list is your work queue for Steps 2–5.

---

## Step 2 — Apply Rule 1: YAML frontmatter

Every prepared file must start with this block. The script inserts a draft;
verify and complete it:

```yaml
---
title: "<first H1 or filename>"
version: "1.0"
domain: "<module or topic area>"
target_audience: "AI Processing Agent"
tokens: <estimated token count>
optimized_for_llm: true
concepts:
  - <top 5 key concepts extracted from the document>
toc:
  - <H2 heading>
    - <H3 heading>
suggested_fixes: []   # cleared once all fixes applied
---
```

Add `related_docs`, `dependencies`, or `status` only when they have a real
value — do not include placeholder fields.

---

## Step 3 — Apply Rule 2: Heading and size rails

- Maximum nesting depth is three levels (`#`, `##`, `###`).
- If you find `####` or deeper, promote or merge those sub-sections.
- Verify no heading levels are skipped (e.g., `##` followed by `####`).
- File must stay under 300 KB after optimization. If it exceeds that after
  all edits, split using the strategy in `references/split-strategy.md`.

---

## Step 4 — Apply Rule 3: Text layout

Read each paragraph. Rewrite any sentence that:
- Runs longer than ~25 words with multiple subordinate clauses
- Contains an inline code term or formula that wraps across a line break
- Uses a hard line break mid-phrase (common in copy-pasted content)

Break at natural clause boundaries. Do not paraphrase — keep the exact
technical meaning. When in doubt about a rewrite, leave it and flag it in
the report.

---

## Step 5 — Apply Rule 4: Math and equations

**Bad pattern** — ASCII fraction layout:

```text
    [CO₂] + [O₂]
λ = ────────────
    [CO] + [HC]
```

**Required pattern** — LaTeX block + inline fallback immediately below:

```text
$$\lambda = \frac{[CO_2] + [O_2]}{[CO] + [HC]}$$
Inline fallback: lambda = ([CO2] + [O2]) / ([CO] + [HC])
```

Rules:
- Every multi-line ASCII equation becomes a `$$ ... $$` LaTeX block.
- Every LaTeX block gets an inline plain-text fallback on the next line.
- Simple inline expressions stay as inline code: `λ > 1.05`.
- Never use dash-divider (`────`) lines for fractions.

---

## Step 6 — Apply Rule 5: Tables and structured data

Standard Markdown tables survive rendering but break when a text splitter
cuts vertically through rows. Apply this decision:

| Data type | Use |
|---|---|
| Simple limits / thresholds | Bullet list: `* Param: [min, max, unit]` |
| Conditional state mappings | Fenced `json` block |
| Reference lookup tables (3+ columns, stable rows) | Keep as Markdown table but add `<!-- TABLE: name -->` comment above it so an extractor can find it |

**Convert a state-condition table to JSON:**

```json
{
  "state_condition": "LEAN_MIXTURE",
  "thresholds": {
    "hc_ppm": "< 300",
    "co_percent": "< 0.1",
    "o2_percent": "> 2.5",
    "lambda": "> 1.05"
  }
}
```

Do not convert narrative tables that explain concepts — only tables that
encode conditional rules, thresholds, or state machines.

---

## Step 7 — Apply Rule 6: Diagrams and ASCII art

**Bad pattern** — spatial ASCII art:

```text
Input ──► Parser ──► Output
```

**Required pattern** — numbered declarative sequence:

```text
1. Input: raw data enters the pipeline.
2. Parser: data is normalized and validated.
3. Output: clean payload emitted to the consumer.
```

For relationship graphs, use Mermaid inside a fenced block:

```mermaid
graph LR
  A[ComponentA] --> B[ComponentB]
  B --> C[ComponentC]
```

Rules:
- Any `──►`, `─┤`, `┌──`, box-drawing characters → declarative sequence or Mermaid.
- Mermaid is preferred when the diagram has more than 3 nodes.
- Declarative sequences are preferred for linear pipelines.
- Never use bare triple backticks — always tag the language.

---

## Step 8 — Apply Rule 7: Code fences

- Every code block must have a language tag: ` ```python `, ` ```json `, ` ```yaml `, ` ```text `, etc.
- Scan for bare ` ``` ` blocks and tag them with the correct language.
  Use ` ```text ` for plain prose excerpts that are not code.
- Inside prose (not inside code fences), escape: `\*`, `\#`, `\|` when
  these characters are literal and not structural.

---

## Step 9 — Write the prep report

Write `<output_dir>/<filename>_PREP_REPORT.md` with this structure:

```markdown
# Prep Report: <filename>

**Date:** <ISO date>
**Input size:** <bytes> / <lines>
**Output size:** <bytes> / <lines>
**Token delta:** <before> → <after>

## Changes applied

| Rule | Description | Count |
|---|---|---|
| R1 Frontmatter | Injected / updated YAML block | 1 |
| R2 Headings | Promoted N heading levels | N |
| R3 Text layout | Rewrote N long sentences | N |
| R4 Math | Converted N ASCII equations to LaTeX | N |
| R5 Tables | Converted N state tables to JSON | N |
| R6 Diagrams | Replaced N ASCII diagrams | N |
| R7 Code fences | Tagged N bare code blocks | N |

## Items requiring manual review

List any item the script flagged but could not auto-fix, with the line
number and reason.

## Skipped (judgment call)

List any item you chose NOT to change and why.
```

---

## Output locations

Write the optimized file to the same directory as the input, with suffix
`_prepped`:

```
<dir>/<filename>_prepped.md
<dir>/<filename>_PREP_REPORT.md
```

Do not overwrite the original. If the user explicitly asks to overwrite
in-place, confirm once before doing so.

---

## What this skill does NOT do

- It does not change technical content, thresholds, or domain facts.
- It does not rewrite narrative prose for style.
- It does not split files (it flags the need and points to the split guide).
- It does not run graphify or prepare files for KG ingestion.
  For KG ingestion preparation, use the `prep` operation in `4dlab-graph`.

---

## Step 10 — Wall-of-Text Repair (export artifact recovery)

Some documents arrive as export artifacts where all paragraph and heading
line-breaks have been stripped, producing lines of 2 000–54 000 characters.
The `optimize_markdown.py` baseline (Step 1) cannot recover structure from
these — it has nothing to split on. Use the scripts in `scripts/` instead.

### 10.1 — Diagnose first

```bash
python3 scripts/diagnose_wall.py <input_prepped.md>
```

Exit 0 = clean (proceed with Steps 1–9 as normal).
Exit 1 = repair needed. The script prints the archetype:

| Archetype | Signature | Example document |
|---|---|---|
| A — wall + structured section | Wall lines >2 000 chars; a clean section follows a known anchor string | DtcDoc.md |
| B — wall + box-drawing | Wall lines + Unicode box chars U+2500–U+257F | DtcDoc2.md |
| B-lite — box only | No wall lines; only box-drawing diagrams | — |

### 10.2 — Check for a pre-built reconstruction script

Look in `scripts/` for a file named `reconstruct_<docname>.py`. If one exists,
run it directly — it encodes the heading anchors, table blobs, and diagram
replacements for that specific document:

```bash
python3 scripts/reconstruct_<docname>.py
# script reads and writes in-place; paths are hard-coded at the top
```

Verify the output passes the readability gate (Step 0 checks, no box-drawing
chars, no heading skips) and write the PREP_REPORT.

**Pre-built scripts in this skill:**

| Script | Source document | Archetype |
|---|---|---|
| `scripts/reconstruct_dtcdoc.py` | `TestSuite/DTC/DtcDoc_prepped.md` | A |
| `scripts/reconstruct_dtcdoc2.py` | `TestSuite/DTC/DtcDoc2_prepped.md` | B |

### 10.3 — Adapt the template for a new document

If no pre-built script exists, copy and adapt the generic template:

```bash
cp scripts/reconstruct_wall_template.py scripts/reconstruct_<newdoc>.py
```

Edit the CONFIG dict at the top of the copy:

```python
CONFIG = {
    # List of (level, exact_heading_text) pairs in document order.
    # Use the exact string as it appears in the wall — no leading/trailing space.
    "headings": [
        (1, "Title of the document"),
        (2, "First major section"),
        (3, "Subsection"),
    ],

    # List of (blob_string, replacement_markdown) pairs.
    # blob_string: concatenated table cell text exactly as it appears in the wall.
    # replacement_markdown: full Markdown table with <!-- TABLE: name --> comment.
    "table_replacements": [
        ("Col1ACol1BCol1C", "<!-- TABLE: name -->\n| Col1 | A | B | C |\n|---|---|---|---|\n"),
    ],

    # List of (old_ascii_block, new_markdown) pairs for box-drawing art.
    # Use Mermaid graph LR for diagrams with 3+ nodes; bullet list for enumerations.
    "box_drawing_replacements": [],

    # String that marks the start of a pre-structured section 2 (Archetype A only).
    # Set to None for pure-wall documents (Archetype B).
    "sec2_anchor": None,

    # Regex pattern for heading levels to promote in section 2, or None.
    # Example: r'^### (Cluster \d+:)' with replacement r'## \1'
    "promote_headings_regex": None,
}
```

Run with:

```bash
python3 scripts/reconstruct_<newdoc>.py input_prepped.md output.md
```

### 10.4 — Save the new script for reuse

Once the output passes the readability gate, copy the adapted script back into
this skill's `scripts/` directory and update the table in §10.2 above so the
next session can find it without re-deriving anything.

### 10.5 — Common failure modes and fixes

| Symptom | Cause | Fix |
|---|---|---|
| Heading not inserted (WARNING logged) | Anchor text differs from wall (extra space, smart quote vs ASCII) | Print the wall section with `repr()` and find the exact byte sequence |
| Table blob not matched | Cell order or whitespace differs from assumed blob | Extract the blob directly from the wall with a short grep script |
| Block equation split across lines | `$$` not on its own line; `fix_block_equations` regex too greedy | Use `re.sub(r'\$\$(.+?)\$\$', fmt, text, flags=re.DOTALL)` to match the full block |
| `null bytes` in script after Edit tool use | Edit tool appended `\x00` bytes | Strip with `python3 -c "d=open(f,'rb').read(); open(f,'wb').write(d.replace(b'\x00',b''))"` |
| `f-string backslash` SyntaxError | Verification one-liner on Python 3.10 | Use a temp variable: `n = d.count(b'\x00'); print(n)` |
