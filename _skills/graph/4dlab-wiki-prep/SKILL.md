---
name: 4dlab-wiki-prep
description: >
  Prepare 4DLab WIKI / PROSE chunks for graphify knowledge-graph ingestion (Pass 3 / LLM semantic
  extraction). Makes implied relationships explicit so graphify tags them EXTRACTED (confidence 1.0)
  instead of INFERRED — by appending explicit relation lines, canonicalising entity labels, and
  adding a Core Entities roster, append-only, without altering sourced prose.
  Use this skill whenever the user mentions preparing/enhancing a wiki for ingestion, prepping
  research chunks, a wiki KG / v2_wiki build, making relations explicit, canonical entity labels,
  proof-set readiness, or asks why graphify edges came back INFERRED/AMBIGUOUS instead of EXTRACTED.
  Use it for GASLab, OBDLab, DTCLab, COMLab, DNALab wiki/research corpora.
  This is the WIKI counterpart to 4dlab-code-prep: 4dlab-code-prep prepares SOURCE CODE (Pass 1,
  AST); THIS skill prepares WIKI/PROSE (Pass 3, LLM). If the input is a .py package, use
  4dlab-code-prep. To actually run graphify after prep, use 4dlab-graphify-run. Supersedes the
  prep half of the retired 4dlab-graph skill.
allowed-tools: Read, Grep, Glob, Bash, Write
metadata:
  version: "0.1"
  argument-hint: "[operation] [chunks-dir] — operations: relations, labels, roster, verify"
  model: sonnet
  context: fork
---

## Purpose

graphify ingests prose with its **LLM semantic pass (Pass 3)**: Claude subagents read each chunk
and emit nodes/edges. A relation is tagged **`EXTRACTED` (confidence 1.0) only when it is stated
directly in the text**; otherwise it is `INFERRED` (0.55–0.95) or `AMBIGUOUS`. So the single most
effective wiki-prep move is to **make implied links explicit in the text** — then graphify extracts
them as facts rather than guessing.

This is the **proven** OBDLab approach (`research/CHUNK_ENHANCEMENT_PREP_REPORT.md`): it built the
live `graph/v2_wiki/` (451 nodes, 408 EXTRACTED) by appending two clearly-marked trailer sections to
every chunk and changing **nothing** in the sourced body.

> **What this skill deliberately does NOT do** (these failed the graphify-docs check and are dropped
> from the retired `4dlab-graph`):
> - No hard ≤18 KB chunking. graphify chunks Pass-3 input itself by `--token-budget`; only split a
>   file if truncation is actually observed, not pre-emptively.
> - No `KG_RELATION_VOCAB` headers, `<!-- ENTITY -->`, or `<!-- TABLE -->` markers injected into
>   files. They are not graphify features; the proven run never used them. Explicit relation lines
>   do the job cleanly.
> - No Option-3 patch that writes `confidence: EXTRACTED, 1.0` edges into `graph.json`. Stamping
>   "extracted" on edges graphify never extracted breaks graphify's honesty model. The honest fix is
>   to make the relation explicit in the text (rule below) and let graphify extract it.

**Operations:**
- `relations` — **highest leverage**: append a `## Graph relations (explicit)` block of
                `**SUBJECT** PREDICATE **OBJECT**` lines for relations that currently live only in
                table-adjacency or prose.
- `labels`    — canonicalise entity labels byte-identically across every chunk.
- `roster`    — append a `## Core Entities` checklist (canonical entities + named consumer).
- `verify`    — confirm each chunk carries exactly one of each trailer, no empty blocks, canonical
                tokens consistent, and that known doc-bugs are written as non-edges.

If no operation is given, run `relations` then `verify`.

---

## Boundary — wiki vs code (do not cross the streams)

| | **This skill — wiki KG** | **`4dlab-code-prep` — code map** |
|---|---|---|
| Input | `.md` wiki / prose chunks | `.py` source package |
| graphify pass | Pass 3 — LLM subagents, costs tokens | Pass 1 — tree-sitter AST, offline |
| Prep lever | explicit relation lines, canonical labels | imports, `__all__`, type hints, enums |
| Output graph | `graph/v2_wiki/` | `graph/v2_code/` |

Never prep code with this skill (no relation lines in `.py`), and never inject prose-prep markers
into source. Running graphify itself is `4dlab-graphify-run`, not this skill.

---

## Step 1 — `relations` (make implied links EXTRACTED)

For each chunk, find relationships the text *implies* but does not state as a clean subject-predicate
sentence — usually table-adjacency ("this DTC row sits next to this fault") or scattered prose — and
append them to a single trailer block:

```markdown
## Graph relations (explicit)

**P0131** INDICATES **STUCK_LEAN**
**VACUUM_LEAK** PRODUCES_NEGATIVE **DELTA_TRIM**
**control_module_voltage_v** CONSUMED_BY **COMLab electrical-health pre-check**
```

Rules that keep this honest and on-spec:
- **Append-only.** Never alter sourced prose, numeric literals, tables, citations, or frontmatter.
  The trailer is a pure append (open files in append mode).
- **No invented edges.** State only relations the chunk actually supports. Where the source carries a
  known doc bug, state the **non-edge** instead, e.g.
  `**SUPPRESS_POST_CAT_TRIM** IS_NOT a **TrimAnalyticsGate** value (doc bug O2-FU-2)` — do not assert
  it as a real edge.
- **Preserve proposal vs active status.** Forward-progress entities stay labelled as proposals with
  their named consumers; do not promote a proposal to live.
- **Pick precise predicates.** Prefer a specific verb over a generic one. See the relation reference
  at the end for the domain vocabulary; `conceptually_related_to` is a last resort.
  (`semantically_similar_to` is fine where genuinely apt — graphify uses it to shape Leiden
  communities — but do not use it as a lazy stand-in for a real relation.)

---

## Step 2 — `labels` (byte-identical entity names)

graphify keys nodes by surface label; the same concept spelled two ways becomes two nodes. Apply one
canonical form everywhere it appears in trailers:

- DTC codes as-is: `P0171`, `P0131`.
- Failure modes `ALLCAPS_UNDERSCORE`: `STUCK_LEAN`, `STUCK_RICH`, `BIASED_OFFSET`,
  `WIDEBAND_OFFSET_CANDIDATE`, `HEATER_FAULT`, `SENSOR_FAULT`.
- Trims: `STFT`, `LTFT`, `TOTAL_TRIM`, `DELTA_TRIM`.
- Dotted enum values **exactly as the shipped enum spells them**:
  `TrimAnalyticsGate.O2_FAULT_ACTIVE`, `DownstreamTrimRole.CATALYST_MONITOR_ONLY`,
  `FuelSystemStatus.CLOSED_LOOP`. (Grep the live enum before writing — never guess casing.)

---

## Step 3 — `roster` (Core Entities checklist)

Append one `## Core Entities` block per chunk listing its canonical entities and each one's named
consumer, so the extractor has an explicit roster and skips nothing important. This is opt-in — the
owner chose to include it on OBDLab. Keep it consistent with each entity's existing
`consumer_status` (live vs proposal); it is not a place to introduce new entities.

---

## Step 4 — `verify`

Confirm, across the corpus:
- every chunk has **exactly one** `## Graph relations (explicit)` and (if rostering) **exactly one**
  `## Core Entities` block — no missing, no duplicate appends;
- **zero** empty relation blocks; report the total relation-line count;
- trailers were appended only (original bytes unchanged — diff the body region);
- canonical-token spot-check: each enum value appears with identical spelling/casing across files.

Report counts and any chunk that fails a check. Do not "fix" by inventing content — flag for the
author.

---

## Output conventions

- Section header: `--=={ 4dlab-wiki-prep: CORPUS / OPERATION }==--`
- Always report per-chunk coverage (which chunks touched, relation-line counts).
- Never alter sourced content; never inject vocab/entity/table markers; never write to `graph.json`.

## Relation reference (predicate vocabulary)

Use the most specific that fits: `routes_to`, `gated_by`, `monitored_by`, `escalates_to`,
`tailpipe_signature_identical_to`, `differential_diagnosis_of`, `disambiguated_by`, `sub_mode_of`,
`confirmed_by`, `enumerates`, `overrides`, `suppresses`, `mirrors_contract_in`, `evaluates_state_of`,
`describes`, `maps_to`. These are names for relations you make explicit; graphify still only tags a
line EXTRACTED if the chunk's text supports it.

## Reference

- `labs/obdlab/research/CHUNK_ENHANCEMENT_PREP_REPORT.md` — the proven run this skill encodes.
- graphify pipeline + confidence tags — `https://github.com/safishamsi/graphify/blob/v8/docs/how-it-works.md`.
