# T-DNA-12 — Decompose `decode_vin_payload()` into helper seams (behaviour-preserving)

**Authored:** 2026-06-12 (architect). **Source:** tri-module audit
`labs/dnalab/docs/audits/AUDIT_2026-06-12_trimodule_dna_vin_symptom.md` §3.3 (V1).
**Type:** pure refactor (no behaviour change, no schema change).

### Goal ###

`vinlab/decoder.py::RobustVINDecoder.decode_vin_payload` is ~290 lines doing ~10 jobs in
one method. Split it along the **comment banners that already mark the seams**, into small
private helpers, so each step is independently testable and the top method reads as an
orchestration. **No output value may change** — the 173 vin tests are the regression gate.

### Named signal/noise consumer ###

N/A — **no schema field added or removed.** Anti-orphan does not apply. The signal/noise of
this change is purely structural; the contract surface (`VinDNA`) is byte-identical before
and after. Gate = existing `tests/` green (173 passed, 15 skipped) with **no test edits**.

### Suggested seams (extract as private methods, keep names descriptive) ###

```
decode_vin_payload()                      # stays: validate → orchestrate → assemble VinDNA
  ├─ _engine_attrs_from_csv(engine_row)   # lines ~322-339  (disp / cyl / banks from CSV)
  ├─ _apply_vref_techmask(db_row, …)      # lines ~340-407  (induction/fuel/euro/emissions + CoC + null-flags)
  ├─ _cylinder_fallback(…)                # lines ~422-442  (T-VL-7 heuristic, last-resort)
  ├─ _derive_air_metering(db_dict, …)     # lines ~444-467
  └─ _compute_confidence(conf_flags)      # lines ~479-485
```

The overlay modules (`air_metering`, `cylinder_heuristic`, `horizon`, `stress_rpm`,
`switches`) are the precedent — this continues the same extraction pattern **inward** into
the monolithic method. Pick the seam set above or an equivalent; the requirement is that
`decode_vin_payload` ends up a short orchestrator, not the specific helper names.

### Success criteria ###

- `decode_vin_payload` body materially shorter; each extracted helper has one job and a
  type-annotated signature returning its slice of the result.
- **Zero diff in behaviour:** `tests/unit/` unchanged and all green; add (optional) thin
  unit tests for the new helpers only if they sharpen isolation — not required to pass.
- All numeric/lookup literals keep their existing source-citation comments (do not drop the
  NHTSA / SAE J853 / ISO 3780 citations during the move).
- Inner loop clean in vinlab (`ruff`/`pyright`/`pytest -x -q`).

### Files to touch ###

- `labs/vinlab/vinlab/decoder.py` (MODIFY — extract helpers; no logic change)
- `labs/vinlab/tests/unit/` (OPTIONAL — new helper-level tests only; do not alter existing)

### Out of scope ###

Any change to decode *results*, the two-path engine resolver, the checksum logic (that is
T-DNA-13/V2), or the overlay modules. No "while I'm here" fixes.

### Verification ###

```bash
cd $HOME/mnt/4DLab/labs/vinlab
ruff check vinlab && pyright vinlab && pytest tests -x -q   # must stay 173 passed / 15 skipped
git diff --stat tests/   # expect: no changes to existing test files
```

### On completion ###

Both gates clean in `progress_notes/T-DNA-12.md`; flip the row → `done`. STOP.
