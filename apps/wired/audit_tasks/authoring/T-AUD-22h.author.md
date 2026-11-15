# T-AUD-22h — authoring sidecar (Windows Cowork, 2026-11-15)

Input: ledger row T-AUD-22; T-AUD-22g accepted (360918e, pushed): the `rest` labs covered (RK0001-RK0210). Last
`rest` slice; app row on the Hydrogen lane (difficulty 3 -> gemini-4-hydrogen-high). Cowork tool change in the spec
commit: `check_code_claims.py` gains `OUT_OF_SCOPE` (one file) and prints `out_of_scope N`.

### Verified context ###
1. **Non-auto `apps/` candidates: 338 = `_sample_app_reference.py` 129 + `ui_payload.py` 93 + `app.py` 58 +
   `composition.py` 40 + `load_corpus.py` 11 + `run_suite.py` 6 + `registry_guard.py` 1.** Observed 2026-11-15 on
   360918e (Counter over `candidates_rest.csv`).
2. **`_sample_app_reference.py` is imported by nothing and imports `engine`, which does not exist in the clone.**
   Observed: `grep -rn _sample_app_reference --include=*.py` hits only the file itself; `ls engine apps/ui/engine`
   absent; `audit/reports/P1_static_sweep_20261026.md:19` says "imported by nothing".
3. **After the checker change: `--group rest` prints `CLAIMS FAIL 209 error(s)`; `--files 'apps/*'` the same; `--files
   'labs/*'` prints `out_of_scope 129 candidate(s) in 1 file(s)` and `CLAIMS OK ... candidates 202 covered claims
   210`; gaslab 188/195 and comlab 1427/1614 still OK; ruff clean.** Observed.
4. **Cited documents exist: `apps/ui/4DLab_UI_FieldMap.md`, `apps/wired/ship_tasks/reports/SHIP_UI_CONTRACT_2026-07-07.md`,
   `labs/dtclab/docs/DTC_VOCABULARY.md`, `labs/gaslab/docs/GAS_VOCABULARY.md`** (DTC/GAS vocabularies have 4-5 copies;
   R6 names the owning lab's copy). Observed.
5. **`composition.py:110-125` holds six fuel-trim bounds `(-127.0, 127.0, float)`; `ui_payload.py:50` has
   `FF_TRIM_MAX = 99.22`.** Observed. RK0181-RK0210 are the OBDLab `physical_sensor_bounds.json` claims.

### Rulings and the tradeoff that lost ###
- **`_sample_app_reference.py` out of scope by a checker list, not by rows.** The operator's order covers production
  code; this file never runs. Lost: 129 `NON_DOMAIN` rows (misuses the class, ~20 min of implementer time, no audit
  value) and classifying them as claims (puts dead values into the verification population).
- **One slice for 209 candidates.** T-AUD-22g did 202 in 11 min. Lost: a ui/wired split (two runs for one register).
- **R7 cross-checks UI bounds against the OBDLab RK bounds**: the UI feeds the labs, so a mismatch is a finding.
- **Lane run: no commit by the implementer**; promote commits on fix/T-AUD-22h.
- Difficulty 3. Survey = facts 1-5. Plan NONE. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | PASS | run 1 (`5f2726f`): `CLAIMS OK group=rest scope=apps/* candidates 209 covered claims 451` |
| step 2 | PASS | run 1: `suspect 38`, `CLAIMS OK group=rest candidates 411 covered claims 451` (P6 pre-state) |
| step 3 | PASS | `CLAIMS OK group=rest scope=labs/* candidates 202 covered claims 210` (P5) |
| step 4 | DEFERRED | `0` removed lines against `79c1e1b`; the CSV, note and RESULT in status |
| step 5 | PASS (both arms) | pre-state `R9 FAIL [] [] [RK0247, RK0249, RK0384, RK0386, RK0394]`; five rows marked: `R9 OK changed 5 missing none` (restored) |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-22h: apps/ui and apps/wired literals (209 lines) classified; CLAIMS OK group=rest (the T-AUD-22 inventory complete).

### Cold read ###
cold read 2026-11-15 FOCUSED reader: 0 findings; 1 UNSETTLED (header "commit locally" vs lane no-commit) — RULED: the lane go prompt overrides the header, as for T-AUD-22d-22g (C:/4DApp/recheck/scratch/T-AUD-22h_coldread.md) — 4 calls

### Correction history ###
- DELTA cold read 2026-11-15: 0 findings; UNSETTLED R9 line break inside `lineterminator` fixed before dispatch (C:/4DApp/recheck/scratch/T-AUD-22h_coldread_c1.md).
- **Correction 1 (2026-11-15, after run 1 promoted as `5f2726f`).** Run 1 met every criterion (re-run by Cowork: 209 /
  411 / 202 OK, 0 removed lines, 7 min) but missed R7's lab-bound comparison on five rows (P7): MAF max 500 vs RK0188
  655.35, FF RPM 16383 vs RK0182 8000, FF ECT 215 vs RK0184 140, FF IAT 215 vs RK0204 140. Added R9, P6, P7, criteria
  4-6, step 4 against `79c1e1b`, step 5 (rehearsed: pre-state `R9 FAIL ... [5 rows]`; with the five marked `R9 OK
  changed 5 missing none`). Lost alternative: accept and carry the five into the verification row (leaves the
  register, the verification input, wrong). Noted but not ruled defects: CO2/O2 input max 22 % (above the physical
  ~15.7 % / 20.9 %), downstream O2 max 1.5 V (J1979 1.275 V); left to the verification row as candidates.
