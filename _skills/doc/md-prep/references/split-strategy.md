# Split Strategy for Large .md Files

Split before optimizing when the file exceeds 300 KB (~75 000 tokens).

## Split rule

Split on `## ` (H2) boundaries only — never mid-section.

```python
import re, pathlib

def split_on_h2(text: str, max_bytes: int = 280_000) -> list[str]:
    """Split text on H2 boundaries, keeping each chunk under max_bytes."""
    sections = re.split(r'(?=^## )', text, flags=re.MULTILINE)
    chunks, current = [], ''
    for section in sections:
        if len((current + section).encode()) > max_bytes and current:
            chunks.append(current)
            current = section
        else:
            current += section
    if current:
        chunks.append(current)
    return chunks
```

## Naming convention

```
GAS_WIKI_part1.md   # §1–§4
GAS_WIKI_part2.md   # §5–§8
GAS_WIKI_part3.md   # §9–§13
```

Each part gets its own YAML frontmatter with `part: N of M` field.
Parts reference each other via `related_docs:` field.

## When splitting for KG ingestion

Use 18 KB chunks (not 280 KB) — graphify truncates above ~20 KB.
The `4dlab-graph prep` operation handles KG-specific chunking automatically.
