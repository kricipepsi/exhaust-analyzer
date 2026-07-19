Output above document adapted to paste into single Markdown document, ready to paste directly into a .md file.

Rules:
- Start with YAML frontmatter: title, domain, concepts (5), toc.
- Exactly one H1. Headings max 3 levels (#, ##, ###), no skipped levels.
- Every code fence gets a language tag. No bare ```.
- No ASCII art or box-drawing. Use ```mermaid for diagrams, numbered steps for linear procedures.
- Tables: escape any literal pipe inside a cell as \|  (critical for |absolute value| and math). Keep all numeric thresholds with units.
- Equations: use $$...$$ with a plain-text inline fallback on the next line; simple expressions stay inline code.
- No search-result stubs, "Opens in a new window", or citation dumps in the body.
- Write each fact once — never repeat a section.