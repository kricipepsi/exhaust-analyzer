# T-GPF-RM-3 — COMLab: stop reading has_particulate_filter (field readers)

**Pack:** GPF Removal · **Lab:** COMLab (field-reader side) · **Blocked by:** T-GPF-RM-2 · **Status:** pending

## Scope (1 paragraph)

Remove COMLab's reading of the `has_particulate_filter` flag from the VIN DNA.
With the `GPF_HISTORY` tag and registry P-codes gone (T-GPF-RM-2), nothing in
COMLab still consumes this boolean, so the mirrored field can be dropped from the
ingestion boundary (the typed edge where VIN data enters COMLab), the projected
DNA view, and the projection function that copies it across. Kept sequential
after RM-2 so all COMLab edits land in dependency order and the lab stays green
between tasks.

## Signal/noise / consumer

Removal. After this task `grep -rn "has_particulate_filter" labs/comlab/comlab`
returns zero. This is the anti-orphan check in reverse: the field had exactly one
consumer (the GPF routing), now removed, so the field itself must go — a field
read nowhere is the orphan the rule forbids.

## Files to change

- `comlab/schemas/lab_dna_views.py:76` — delete `has_particulate_filter: bool`.
- `comlab/schemas/ingestion.py:67` — delete `has_particulate_filter: bool`.
- `comlab/projection.py:105` — delete the
  `has_particulate_filter=vin.get("has_particulate_filter")` assignment.
- `docs/wiki/SEMANTIC_CONTRACT.md:125,263,600` — remove the
  `has_particulate_filter` example field, the "presence of GPF" mapping row, and
  table-row 4 ("Add has_particulate_filter and model_year to Part A"); keep
  `model_year` (out of scope for this pack).
- `docs/wiki/COMLab_Horizon_Eras.md:83` — remove the "GPF (has_particulate_filter
  = true) may mask some HC readings" line.
- `docs/COMLab_LLD.md:254,540,938` — remove the `has_particulate_filter` rows in
  the mirrored-view / JSON-schema definitions (the routing prose was handled in
  RM-2; this clears the field rows).
- Tests: `tests/unit/test_projection.py:57,88,141` — remove the
  `has_particulate_filter` inputs and the `assert result.has_particulate_filter`
  line; keep the rest of the projection round-trip.

## Success criteria

- No `has_particulate_filter` token anywhere in `labs/comlab/` (graph excluded).
- `projection.py` still round-trips every other VIN-DNA field; `test_projection`
  green.
- Ingestion/lab-DNA-view schemas validate against existing COMLab fixtures
  (the field was a plain bool, no default change needed elsewhere).

## Inner loop (coder)

`ruff check labs/comlab` → `pyright labs/comlab` → `pytest -x -q labs/comlab/tests`.

## VERIFICATION GATE
_(coder fills)_

## CODE REVIEW
_(coder fills)_
