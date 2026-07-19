# T-GPF-RM-4 — Wired app + semantic vocab + OBDLab vocab: drop GPF field/refs

**Pack:** GPF Removal · **Targets:** wired app, semantic pack, obdlab docs · **Blocked by:** T-GPF-RM-1 · **Status:** pending

## Scope (1 paragraph)

Clear the remaining **readers** and documentation references to
`has_particulate_filter` / GPF outside COMLab and DTCLab: the wired composition
layer that surfaces the flag in the UI, the semantic vocabulary mirrors, and the
OBDLab vocabulary note that defines the GPF gate. These are all readers or docs,
so they must be done **before** the source field is removed in RM-5. This task is
parallel-safe with RM-2/RM-3 (different files) but shares the RM-1 prerequisite:
the DTCLab tag must be gone first so the UI/vocab no longer advertise a tag that
cannot be produced.

## Signal/noise / consumer

Removal. After this task `grep -rn "has_particulate_filter\|GPF" labs/semantic apps/wired apps/ui labs/obdlab/docs`
returns zero live hits (regenerated graphs and `_reference/`-marked obsolete docs
excluded).

## Files to change

Wired app:
- `apps/wired/wired/composition.py` — remove the `has_particulate_filter` read /
  pass-through.
- `apps/wired/app.py` — remove the field from any UI surface / payload it builds.
- `apps/wired/tests/test_composition.py` — drop the corresponding assertion(s).

Semantic pack (vocabulary mirrors — keep them in step with COMLab):
- `labs/semantic/vocabul/OBD_VOCABULARY.md`, `labs/semantic/vocabul/DTC_VOCABULARY.md`,
  `labs/semantic/vocabul/SEMANTIC_CONTRACT.md`, `labs/semantic/SAE.md` — remove
  the `GPF_HISTORY` / `has_particulate_filter` / P244A / P2459 rows so the
  semantic mirror matches the post-removal COMLab vocabulary.

OBDLab + UI docs:
- `labs/obdlab/docs/OBD_VOCABULARY.md §13.5` — remove the GPF "Euro 6+ GDI only"
  definition that VINLab's decoder cites as `<WIKI> OBD_VOCABULARY.md §13.5`.
  **Note for RM-5:** once this section is gone, the citation comment in
  `vinlab/decoder.py:379` becomes stale — RM-5 removes that code, so the order
  (RM-4 before RM-5) keeps the citation valid until the code goes.
- `apps/ui/4DLab_UI_FieldMap.md` (and the `UI design/uploads/` copy) — remove the
  GPF/`has_particulate_filter` field-map row.
- `Vault/labs/obdlab/docs/OBD_VOCABULARY.md` and `labs/comlab/docs/wiki/OBD_VOCABULARY.md`
  mirrors — strip the same §13.5 note for consistency.

## Success criteria

- Wired tests green with no `has_particulate_filter` reference.
- Semantic + OBD vocab mirrors carry no GPF tokens.
- VINLab still compiles (its code is untouched here; only the wiki it cites
  changes — RM-5 removes the code next).

## Inner loop (coder)

`ruff check apps/wired` → `pyright apps/wired` → `pytest -x -q apps/wired/tests`.
Docs are prose-only; just confirm no broken in-doc anchors remain.

## VERIFICATION GATE
_(coder fills)_

## CODE REVIEW
_(coder fills)_
