**Scope**
- Desk review of the embedded diffs, plan corrections, and `rekey.py`. Shell execution is blocked in this environment, so counts below are re-derived arithmetically/structurally rather than re-run.

**Verified**
- R1: exactly the 10 brand-cell-only edits plus `LSJ,MG,CHINA,modern`; no other `wmi.csv` row changes (11+/10-).
- R2/C2: W `1004/1126`, C `4388/5071`, N `40056/44941` all meet floors; populations unchanged (`1667/9215/50439`).
- R3: `_pick_vpic_make`, `_registry_majority`, `--registry-csv`, and `build(..., registry_make)` are wired; with no registry the pick falls through to `makes[-1]`, preserving prior behavior.
- C1-C6: all present — cp1250 reads in both scripts, N floor, `deleted_rows == vote_old` (17==17), `build()` test and `_pick_vpic_make([])->""`, 7 C5 VINs with M7, Path B counts recorded (base 0 / plan 0).
- Map diff is 82+/23- under the six new brands only; no old-brand row is touched; the 17 removed-and-replaced rows match the 17 old-wins keys, consistent with C3.

**Findings**
- **MEDIUM — 17-char filter mutant is not killed.** In `test_build_wmi_map.py`, the lone short row `"JTMBD31V00515799;SUBARU;P",  # 16 characters: not counted` is not decisive. A `_registry_majority` mutant that drops `if len(vin) == 17 and brand:` (i.e. counts the 16-char VIN) produces `JTM` = TOYOTA 2 / SUBARU 2; `Counter.most_common(1)` returns the first-seen `TOYOTA`, so `{"JTM": "TOYOTA", ...}` still passes. Fix: add a second 16-char SUBARU P row (`"JTMBD31V00515798;SUBARU;P"`), making the mutant yield SUBARU 3 vs TOYOTA 2 and fail the test.
- **LOW — `_registry_majority` counts replacement-char brands.** `errors="replace"` (line `with path.open(encoding="cp1250", errors="replace", newline="")`) can turn an undefined cp1250 byte (e.g. 0x98) in `D1-Znamka` into `�`; the `�` brand is then counted and could be returned as the majority, and `_pick_vpic_make` would silently fall back to the last vPIC make, regenerating the pre-fix brand. Fix: skip brands containing `\ufffd`, mirroring `rekey.py`'s `quarantined`.
- **LOW — JTE assertion is non-discriminating.** In `test_load_vpic_wmis_uses_registry_majority`, `_vpic_db(..., {"JTE": ["Subaru", "Toyota"]})` plus `assert got["JTE"]["brand"] == "Toyota"` passes even for a mutant returning `makes[-1]` (Toyota is both the registry majority and the last make). Fix: use makes `["Toyota", "Lexus", "Subaru"]` with registry `"LEXUS"` and expect `"Lexus"`, so the case actually distinguishes override from last-make.
- **LOW — CLI parsing edge.** In `__main__`, `if arg == "--registry-csv" and i < len(sys.argv) - 1:` misparses `--petrol-csv --registry-csv file1.csv` (assigns the flag token as the petrol value) and silently ignores a trailing flag with no value. Fix: validate values / use `argparse`.
- **LOW — aggregate W floor can hide per-WMI regression.** `5TD`, `ZAC`, `1C4`, `3C4`, `1C3`, `3N1`, `LSJ` each have only a decode-make case and no engine-resolution floor; the W total could stay ≥ floor while one of them collapses. Accepted by A2, so record as residual risk, not a defect.
- **LOW — independent gate rerun pending.** The held-out file-3 join totals in the note are the implementer's run; the note marks Cowork's rerun as pending. Recommend completing that rerun before closeout.

APPROVE WITH CORRECTIONS