# T-VINA-3 — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. **Finding:** F-C6-4 (`audit/reports/R1_C6_20261017.md`): `my_start`/`my_end` are read nowhere; Subaru 1995/1996
   with the EJ20 row (1998-2010) get Euro 4, wideband, HIGH.
2. **Split:** the old ledger row T-VINA-3 named F-C6-1, F-C6-4 and F-D1-13. F-C6-1 changes 36 corpus runs downstream
   (era_sweep) and needs a plan gate, so it moves with F-D1-13 to T-VINA-10. F-C6-4 is self-contained.
3. **Rehearsed (P2)** on `recheck/T-VINA-3/rh3/vinlab` (`make_rh.py`): vinlab `229 passed, 8 skipped`; new file
   `3 passed`; probes f3/f8 `8 passed` (WBA4W9C5ZLYYYYYYY now refused-or-plausible); M1 `4 failed`; dnalab 27,
   wired 41, ui 30 against the copy (rh2, same decoder).
4. **Base (P1)** on `aa69249`: vinlab `225 passed, 8 skipped`; probes `1 failed, 7 passed`.
5. **In-window population (P4):** 9 real VINs; `VF7SA5FR8AW511081` is the one HIGH GDI case, used for the db_row tests.

### Rulings and the tradeoff that lost ###
- Drop the row and flag it. Lost: keep the row and only downgrade the grade: the Euro 4 targets and the wideband
  sensor would still reach GASLab and OBDLab (F-C2-8, F-C5-9).
- A `None` year keeps the row. Lost: drop it too: nothing contradicts the row, and T-VINA-2 makes more years `None`.
- The fixture is regenerated. Lost: hand-editing its fields (T-VINA-1 style): the tech-mask changes about 20 fields.
- Plan NONE, difficulty 2: a rehearsed guard.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | copy: `229 passed, 8 skipped` |
| step 2 | SIMULATED | copy: `3 passed` |
| step 3 | SIMULATED | copy on `PYTHONPATH`: `27 passed`, `41 passed`, `30 passed` |
| step 4 | SIMULATED | copy on `PYTHONPATH`: `8 passed` |
| step 5 | DEFERRED | R5's doc line |
| step 6 | DEFERRED | ruff and the commit |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-VINA-3: a vref.db row is applied only inside its my_start-my_end window; outside, flag vref_year_out_of_window.

### Cold read ###
own pass 2026-11-04: anchors grep 1 each · P1 on the base · P2 on the copy · traceability: criteria 1-5 → steps 1-6 ·
JUDGEMENT criteria: 0.
cold read 2026-11-04: skipped (Plan: NONE, difficulty 2, rehearsed edits).

### Correction history ###
