# T-DNA-3 — Emit `rated_rpm` from VINLab

### Goal ###

VINLab does not emit `rated_rpm`, yet COMLab's projector reads it
(`projection.py:89` → `ObdLabDnaView.rated_rpm`) and OBDLab uses it as the
DNA-relative RPM ceiling (`OBDLab_KG_Wiki §3.1`). Today it always projects as `None` —
a live consumer reading a field its producer never supplies. Close the gap: populate
`rated_rpm` on `VinDNA`.

This is the cleanest task in the pack: the consumer already exists and is live, and
the source data is already local.

### Data source (cite inline) ###

`DBS/docs/vehicles_petrol_specimens.csv` column `P14_rated_rpm`, keyed by
`P15_engine_code` — the same per-engine-code median path already used to populate the
CoC targets (`engine_baseline.csv`). Use the existing baseline-overlay mechanism; do
not invent a new source.

### Named signal/noise consumer ###

`comlab/projection.py` `project(..., target="obd")` → `ObdLabDnaView.rated_rpm`
(already reads `vin.get("rated_rpm")`) → OBDLab DNA-relative RPM ceiling. Consumer is
**existing and live** — no proposal needed; this task makes the read non-`None`.

### Success criteria ###

- `VinDNA` gains `rated_rpm: int | None = None`; `to_json()`/`from_json()` round-trip it.
- The decoder/overlay populates `rated_rpm` from the baseline source for a HIGH/PARTIAL
  confidence decode where the engine_code is known; stays `None` when unknown.
- `tests/test_models.py` (vinlab): a known engine_code yields its `rated_rpm`; an
  unknown one yields `None`.
- `grep` confirms `projection.py` already reads `rated_rpm` (consumer proof); no
  projector edit here.
- Draft `SEMANTIC_CONTRACT.md` §4.1 amendment (add `rated_rpm`, source-noted) in the
  progress note — flagged for COMLab sign-off.
- Inner loop clean on every edited file.

### Files to touch ###

- `labs/vinlab/vinlab/models.py` (MODIFY — add field + serialize)
- `labs/vinlab/vinlab/decoder.py` and/or `vinlab/overlay/` (MODIFY — populate from baseline)
- `labs/vinlab/tests/test_models.py` (MODIFY)

### Out of scope ###

The projector (COMLab, already correct for this field). The CoC/emissions path bug
(→ T-DNA-4). Any OBDLab-side RPM-ceiling logic.

### On completion ###

Both gates clean in `progress_notes/T-DNA-3.md`; flip T-DNA-3 → `done`. STOP.

### Verification ###

```bash
cd $HOME/mnt/4DLab/labs/vinlab
ruff check vinlab/ && pyright vinlab/
grep -rn "rated_rpm" vinlab/                                   # defined + populated, not only declared
grep -rn "rated_rpm" ../comlab/comlab/projection.py            # consumer read confirmed
pytest tests/ -x -q --tb=short
```
