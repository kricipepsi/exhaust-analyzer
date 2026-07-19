# T-OBDV2-PURGE-2 — trim orphan era / EGR fields from the OBD DNA view

**Status:** `pending` — **NOT coder-runnable yet** · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** `OBDLAB_PURGE_AUDIT_2026-06-08.md` §3 · **Blocked by:** `T-OBDV2-0` (revive/quarantine gate)
**Consumer (signal/noise):** N/A — this task **removes** schema surface. It *restores* the invariant: after it, every field on `ObdLabDnaView` has a named OBDLab consumer. The era/EGR capability is re-homed (not lost) to DNALab→COMLab via proposals `EP-DNA-03` (euro-era-tier-gate) and `EP-FA-06` (EGR insufficient flow); neither names OBDLab as consumer.

### Goal ###

Remove the era/emissions artefacts on `obdlab/schemas/dna_view.py` that are read **nowhere** in OBDLab:
the `EuroEmissionCategory` enum, the `ResolvedHorizon` enum (the "2010-2020" `HORIZON_MODERN` band and its
1990-2010 siblings), the `ObdEmissionsView` model, and the two `ObdLabDnaView` fields that carry them
(`emissions`, `resolved_horizon`). Update `tests/unit/test_dna_view.py` to match. Done when those symbols are
gone from `dna_view.py`, the model has no orphan field, and the suite is green.

### Success criteria ###

- `grep` confirms `EuroEmissionCategory`, `ResolvedHorizon`, `ObdEmissionsView`, `resolved_horizon`, and
  `egr_equipped` no longer appear in `obdlab/` (outside test history).
- `tests/unit/test_dna_view.py::test_obd_lab_dna_view_fields` passes against the **reduced** field set (no
  `emissions`, no `resolved_horizon`).
- `pytest -x -q` green; `pyright obdlab/` clean (no dangling references to the removed types).

### Context ###

Per-symbol grep shows zero references **outside** `dna_view.py`: `resolved_horizon`, `ResolvedHorizon`,
`EuroEmissionCategory`, `EURO_*`, `egr_equipped`, and `emissions` are all defined-but-never-read in OBDLab.
`EuroEmissionCategory` is not even consumed by `ObdLabDnaView` itself (the model carries `resolved_horizon`,
not a euro category). `EURO_7` + the `HORIZON_MODERN` "Euro 5-7, 2010-2020" comment are anachronistic — a
tell they were copied in speculatively and never wired. These are signal/noise breaches.

Exact edit targets in `obdlab/schemas/dna_view.py`:
- `class EuroEmissionCategory` — line 13 (whole class, incl. `EURO_1..EURO_7`, `UNKNOWN`)
- `class ResolvedHorizon` — line 60 (whole class)
- `class ObdEmissionsView` — line 83 (whole class; `egr_equipped` is line 88)
- `ObdLabDnaView.emissions` — line 106 (remove field)
- `ObdLabDnaView.resolved_horizon` — line 107 (remove field)

Exact edit targets in `tests/unit/test_dna_view.py`:
- imports — remove `EuroEmissionCategory` (17), `ObdEmissionsView` (20), `ResolvedHorizon` (22)
- `EnumAnchor` list — remove the `EuroEmissionCategory` anchor (63-64) and the `ResolvedHorizon` anchor (69)
- `test_obd_lab_dna_view_fields` `expected` set (100-106) — drop `"emissions"`, `"resolved_horizon"`
- `test_obd_emissions_view_fields` (109-110) — DELETE the whole test
- `model_validate` fixtures (124-25, 145-46, 160-61) — drop the `"emissions"` and `"resolved_horizon"` keys
- assertions on `view.emissions` (135) and `view.resolved_horizon` (136) — DELETE

**Keep (these DNA-view fields have live consumers — do NOT remove):** `air_metering_strategy`,
`upstream_o2_type`, `induction_type`, `confidence`, `engine_displacement_liters`, `cylinder_count`,
`rated_rpm`, `stress_idle_rpm_target`, and the enums `AirMeteringStrategy`/`O2SensorType`/`InductionType`/`VinConfidence`.

### Deliverables ###

1. `obdlab/schemas/dna_view.py` — remove `EuroEmissionCategory`, `ResolvedHorizon`, `ObdEmissionsView`, and the `emissions` + `resolved_horizon` fields on `ObdLabDnaView`.
2. `tests/unit/test_dna_view.py` — update imports, enum anchors, the field-set expectation, fixtures, and assertions; delete `test_obd_emissions_view_fields`.

### Files to touch ###

- `obdlab/schemas/dna_view.py` (MODIFY)
- `tests/unit/test_dna_view.py` (MODIFY)

### Out of scope ###

Do **not** remove or rename any kept field/enum (list above) — they have live consumers in `ve_engine`,
`o2_normalizer`, `semantic_consistency_checker`, `pid_ingestion_validator`. Do **not** re-home the era/EGR
logic into DNALab/COMLab here — that is the `EP-DNA-03` / `EP-FA-06` proposal track, a separate lab. Do
**not** touch the dead classifier files — that is `T-OBDV2-PURGE-1`. Do **not** edit the wiki (`OBDLab_KG_Wiki.md`
§4 references EGR/era) — wiki edits are architect out-of-band; log the needed wiki follow-up in PROGRESS.md.
Surgical-change rule: every changed line traces to a Deliverable.

### Verification ###

```bash
cd /path/to/4DLab/labs/obdlab

# Inner loop
ruff check obdlab/ tests/
pyright obdlab/

# Structural — symbols gone from package source
grep -rn --include=*.py -E 'EuroEmissionCategory|ResolvedHorizon|ObdEmissionsView|resolved_horizon|egr_equipped' obdlab/ \
  && { echo "FAIL: orphan symbol survives in obdlab/"; exit 1; } || echo "OK symbols gone"

# Functional — reduced field set + full suite
pytest -x -q tests/unit/test_dna_view.py
pytest -x -q
```

All steps must pass.

### Progress hook ###

`tasks/progress_notes/T-OBDV2-PURGE-2.md` opens with the confirmed `## Plan`, then gains `VERIFICATION GATE`
+ `CODE REVIEW`. PROGRESS.md `T-OBDV2-PURGE-2`: Status=done, Files changed=2, Verification="orphan era/EGR
fields removed; dna_view field-set test green; suite green".
