# T-VINA-7c — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/reports/R1_C6_20261017.md` F-C6-10. Rehearsal: `C:/4DApp/recheck/T-VINA-7c/`.

### Verified context ###
1. **Path B has no data:** `csv.DictReader` over `vds_engine_map.csv` → `12987` rows, `0` with `pos_8_only`; the
   decoder's `vds_pos8_index` is empty. An `awk -F,` count says 39 (quoted commas): wrong. Observed.
2. **The docs claim it:** wiki 11 §11.4 ("used by older vehicles"), PRD P0 "Two-path engine resolution", HLD §6.
   The HLD §6 paragraph names the 0.70 ambiguity flag but not the T-VINA-11c weak rule. Observed.
3. **Rehearsal** (restored): `3 files changed, 11 insertions(+), 5 deletions(-)`; `F-C6-10` once per doc; vinlab
   `393 passed, 8 skipped` (unchanged). Observed.

### Rulings and the tradeoff that lost ###
- **Docs follow the data; the code path stays.** Lost: filling Path B (no known per-brand position-8 engine source;
  the builders in `tools/` are not examined) and deleting the code (it is fixture-tested and costs nothing).
- **HLD §6 also names `vds_engine_weak`** (the T-VINA-11c review follow-up). Lost: a separate docs row for one line.
- Docs row: plan NONE, difficulty 1, no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | `12987 0 0` |
| step 2 | SIMULATED | `1` ×3; `1`; `393 passed, 8 skipped` |
| step 3 | SIMULATED | `3 files changed, 11 insertions(+), 5 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-VINA-7c: wiki/PRD/HLD say Path B ships with 0 map rows (F-C6-10); HLD names vds_engine_weak.

### Cold read ###
own pass 2026-11-07: P1-P2 measured (facts 1, 3) · traceability: criteria 1-2 → steps 1-3 · cold read: not
triggered (d1 docs, scripted) · no finding.

### Correction history ###
(none)
