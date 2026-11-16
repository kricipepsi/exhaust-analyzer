# T-AUD-24h — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-23c ruling §5 (RK0445, RK0446; `reviews/RULING_T-AUD-23c.md`). Survey by Cowork (difficulty 2: no cold
read; second review kept, code row). Lane: Hydrogen medium.

### Verified context ###
1. **One FIELD_HELP entry serves three widgets with three ranges.** `app.py:536-540` (all `help=FIELD_HELP["obd_upstream_o2_val"]`),
   `ui_payload.py:321-326` (`0.0`-`20.0`, unit empty). Read on d7762aa.
2. **The key must stay** (`test_ui.py::test_field_help_coverage` walks `widgets.get` keys). Read.
3. **UI suite 76 → 79 with R1-R3; the new test fails 3 of 3 before.** Rehearsed and restored (`recheck/T-AUD-24h/`).
4. **No other reader of the entry.** `grep -rn obd_upstream_o2_val apps/ui/*.py`.

### Rulings and the tradeoff that lost ###
- **Keep `obd_upstream_o2_val` as the narrowband entry, add two help-only keys.** Lost: one entry per widget with a
  new widget key each (renames the payload key; touches build_diagnose_payload and five tests).
- **Lost: a dynamic tooltip built from the sensor type in app.py**: it bypasses the shared FIELD_HELP table the
  contract names.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | patch applied: `79 passed` |
| step 2 | SIMULATED | pre `3 failed`; patched `3 passed` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-24h: upstream-O2 tooltips per widget (V, λ, AFR).

### Cold read ###
none (difficulty 2, process 055).

### Correction history ###
(none)
