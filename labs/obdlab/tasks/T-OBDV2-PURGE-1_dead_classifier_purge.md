# T-OBDV2-PURGE-1 — remove the dead OBDLabSimple classifier layer

**Status:** `pending` — **NOT coder-runnable yet** · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** `OBDLAB_PURGE_AUDIT_2026-06-08.md` §2.1 · **Blocked by:** `T-OBDV2-0` (revive/quarantine gate)
**Consumer (signal/noise):** N/A — this task **removes** code; it adds no field/enum/fault. Net effect: the only classifier surface left in OBDLab is the live analytics-channel emitter.

### Goal ###

Delete the orphaned fault-family classifier layer that fed the archived `OBDLabSimple`/`COMLabSimple`
top-3 composition path. Concretely: remove `obdlab/ranking.py` and `obdlab/family_map.py` and their three
unit-test modules. Done when those five files no longer exist, no live import references them, and the
full suite is green. This is the visible source of the ">95% NO_FAULT" behaviour — `family_map.signature_to_family()`
collapses every non-discriminating signature to `no_fault` for a consumer that no longer exists.

### Success criteria ###

- `git`/`grep` confirm the five files are gone and **no non-test module** references `obdlab.ranking`,
  `obdlab.family_map`, `classify_top3`, `rank_candidates`, or `signature_to_family`.
- `python3.14 -c "import obdlab; obdlab.SensorSignalTranslator"` still imports clean (public surface unchanged).
- `pytest -x -q` green after deletion (the three deleted test modules go with the code; remaining suite passes).

### Context ###

The live OBDLab entry point is `obdlab/core/sensor_signal_translator.py::SensorSignalTranslator.translate()`,
which returns an `OBDLivePayload` and **never calls** the ranking/family layer (verified: the only imports of
`obdlab.ranking` / `obdlab.family_map` are `ranking.py` itself and the three deleted tests). The public surface
`obdlab/__init__.py` (lines 8-10) exports only `SensorSignalTranslator` + `OBDLivePayload` — it does **not**
re-export the classifier, so deletion does not change the public API. `DECISIONS.md` **D-V2-10** condemns all
`*Simple/` variants (incl. `OBDLabSimple`) to ARCHIVE; the only historical live importer was `4DLabWired`'s
`composition.py` top-3 line, cut on copy by `T-RM-3-WIRED`. DTCLab has its *own, separate, live* `ranking.py`
(`labs/dtclab/dtclab/ranking.py`, wired to `T-DTW-1`) — **do not touch it**; it is unrelated.

Files to delete (LOC for sizing): `obdlab/ranking.py` (266), `obdlab/family_map.py` (80),
`tests/unit/test_ranking.py` (133), `tests/unit/test_classify_top3.py` (152), `tests/unit/test_family_map.py` (78).

`obdlab.egg-info/SOURCES.txt` lists the deleted files but is a build artefact (regenerated on next build) —
do **not** hand-edit it.

### Deliverables ###

1. `obdlab/ranking.py` — DELETE
2. `obdlab/family_map.py` — DELETE
3. `tests/unit/test_ranking.py` — DELETE
4. `tests/unit/test_classify_top3.py` — DELETE
5. `tests/unit/test_family_map.py` — DELETE

### Files to touch ###

- `obdlab/ranking.py` (DELETE)
- `obdlab/family_map.py` (DELETE)
- `tests/unit/test_ranking.py` (DELETE)
- `tests/unit/test_classify_top3.py` (DELETE)
- `tests/unit/test_family_map.py` (DELETE)

### Out of scope ###

Do **not** touch DTCLab's `ranking.py`/`classify_top3` (separate, live). Do **not** alter
`sensor_signal_translator.py`, the schemas, or any analytics module — this task only removes dead files.
Do **not** edit `obdlab.egg-info/`. Do **not** trim the orphan era/EGR DNA fields — that is `T-OBDV2-PURGE-2`.
Surgical-change rule: every removed line traces to a Deliverable; any adjacent dead code you spot goes to the
PROGRESS.md "Unplanned follow-ups" table, not into this diff.

### Verification ###

```bash
cd /path/to/4DLab/labs/obdlab   # repo: 4DLab; lab: labs/obdlab

# Inner loop (lab root)
ruff check obdlab/ tests/
pyright obdlab/

# Structural — files gone, no live references
for f in obdlab/ranking.py obdlab/family_map.py tests/unit/test_ranking.py \
         tests/unit/test_classify_top3.py tests/unit/test_family_map.py; do
  test ! -e "$f" && echo "OK gone: $f" || { echo "FAIL still present: $f"; exit 1; }
done
# Must return NOTHING (no live reference survives)
grep -rn --include=*.py -E 'obdlab\.(ranking|family_map)|classify_top3|rank_candidates|signature_to_family' obdlab/ tests/ \
  && { echo "FAIL: live reference survives"; exit 1; } || echo "OK no references"

# Public surface intact
python3.14 -c "import obdlab; obdlab.SensorSignalTranslator; obdlab.OBDLivePayload; print('surface OK')"

# Functional
pytest -x -q
```

All steps must pass.

### Progress hook ###

`tasks/progress_notes/T-OBDV2-PURGE-1.md` opens with the confirmed `## Plan`, then gains `VERIFICATION GATE`
+ `CODE REVIEW`. PROGRESS.md `T-OBDV2-PURGE-1`: Status=done, Files changed=5 (all deletions),
Verification="dead classifier removed; surface intact; suite green".
