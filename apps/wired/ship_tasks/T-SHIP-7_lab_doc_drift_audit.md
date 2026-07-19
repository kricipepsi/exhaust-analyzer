# T-SHIP-7 — lab doc drift audit vs v3 code (READ-ONLY disclose)
**Pack:** ship · **Status row:** `ship_tasks/SHIP_PROGRESS.md` · **Blocked by:** —
**Lane:** coder · **Write scope:** ONE report `apps/wired/ship_tasks/reports/DOC_DRIFT_2026-07-08.md`
(+ progress note `progress_notes/T-SHIP-7.md`). **No doc, source, test, corpus, rule, or
yardstick file may change in THIS task** — the fixes are T-SHIP-8, blocked on this audit.

## Why
The labs' top-level docs predate the v3 finish line: e.g. `labs/comlab/README.md` and
`labs/dnalab/README.md` still read "_Status: scaffold placeholder_" while comlab carries
527 tests + the 73-rule registry. Before (or right after) the GitHub push, the repo's
front doors should describe the code that ships. Disclose-first: inventory the drift and
CLASSIFY it, so T-SHIP-8 fixes only what a coder may legally touch.

## Boundary (HARD — from `4DLab_CLAUDE.md`)
The wiki is the repo's **source of truth for domain facts** (gas bands, trim grammar,
fault signatures). A doc-vs-code mismatch on a DOMAIN fact is never "doc drift" — it is a
conflict to SURFACE to the owner, not edit. Only CODE-FACING claims (statuses, counts,
paths, module names, contracts, build-stage notes) are candidate fixes.

## Steps (read-only; interpreter `.venv-wired/bin/python` where a count needs running)
1. **Inventory.** For each lab — `gaslab` · `obdlab` · `dtclab` · `dnalab` · `comlab`
   (+ `registry`) · `vinlab` — read (a) `README.md`; (b) the wiki index (`wiki/00_index.md`
   or equivalent) plus any top-level status/contract doc it points to; (c) the design set
   in `labs/<lab>/docs/`: `PRD_* / HLD_* / DLD_* / LLD_* / BDD_*` — these describe the
   code and are FULLY in scope. Special handling inside `docs/`:
   - `ADR_*` are **immutable by their own header** — a stale ADR is never edited; if code
     genuinely superseded a decision, list it as a **new-ADR proposal** (own subsection of
     the report), not an A-list edit.
   - `*_VOCABULARY.md` are drift-guarded domain surfaces (comlab's has a test) —
     mismatches there default to **B** (owner), A only if purely mechanical (a path or
     count, no term/meaning change).
   - `docs/audits/`, `docs/ARCHIVE/`, dated process docs (handoffs, `*_2026-*.md`
     reports, research prompts): skip — archives are not retconned. Never open `Vault/`.
2. **Compare** each checkable claim against v3 code on disk: status lines, test/rule/field
   counts (registry = 73 rules / 16 files; ChemicalSignature = 34 values; scoreboard
   identity 269/294, 191/78 split), file paths, entry points, stage/"placeholder" notes,
   boundary statements (no cross-lab imports), consumer names.
3. **Classify** every mismatch: **A — code-facing drift** (doc describes code and is
   stale) → goes on the T-SHIP-8 fix list with file, line, current text, correct text +
   the code citation proving it; **B — domain-fact conflict** (wiki fact vs code
   behaviour) → owner decision row material, cite both sides, DO NOT propose a doc edit;
   **C — historical/ambiguous** → leave, one-line reason.
4. **Report:** per-lab table (claims checked / A / B / C), the full A fix list (this is
   T-SHIP-8's spec input), B conflicts (if any) drafted as owner decision rows, C log.
   Fill both gate blocks in the progress note.

## Success criteria
- Every lab covered; every A item carries file+line+correct text+code citation (T-SHIP-8
  must be executable from the list alone, no re-research).
- Zero edits outside report+note (`git status` delta proves it).
- Any B item is quoted verbatim from both wiki and code — no silent resolution.
FORBIDDEN: editing any doc/source; touching `Vault/`; running `graphify`; git actions.
