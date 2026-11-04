# T-VINA-17 — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. **Finding:** F-R3-3 (R3 verification, CONFIRMED for VSA): `decode("VSA63823413020157")` → year 2001. WD3, WDA, WDF,
   WDZ and VDB were UNVERIFIABLE on the 1,364 C6 real VINs (no VIN). The C6 corpus has 1 VSA VIN (digit form, `1`).
2. **Measured (P3)** on the Slovenian registry, read-only (`recheck/T-VINA-17/registry.py`, all Mercedes WMIs of
   `wmi.csv`). Digit-form VINs with `1` at position 10 whose first registration is outside 2000-2002, so the `1`
   cannot be the model year 2001: VSA 286/443, WDF 4458/4536, WMX 25/25, 4JG 2/2, VDB 1/1. The 6 T-VINA-2 WMIs
   show the same (WDD 25017/25017, WDB 20409/23391). WHE: 4 digit-form VINs with `2`/`3` that match the registration
   year (years). WDA: 3 VINs, none digit-form. WD3, WDZ: no VIN.
3. **Rehearsed (P2)** on `recheck/T-VINA-17/rh/vinlab` (`make_rh.py`): vinlab `319 passed, 8 skipped`, new file
   `15 passed`, probes `8 passed`, dnalab 27, wired 41, ui 30 (copy on `PYTHONPATH`, `decoder.__file__` checked);
   M1 `6 failed`, M2 `4 failed`; ruff clean with the vinlab config.
4. **Base (P1)** on `e4ad961`: vinlab `313 passed, 8 skipped`; probes `8 passed`; dnalab 27, wired 41, ui 30.

### Rulings and the tradeoff that lost ###
- Add the 5 WMIs with registration evidence. Lost: the whole Mercedes list of `wmi.csv` (WHE's digit-form VINs carry
  real years; WDA, WD3, WDZ have no digit-form evidence).
- Keep `4JG` and `VDB` despite small counts (2 and 1). Lost: a minimum count. Each VIN's registration date rules out
  2001, and the digits condition leaves the 61 letter-form `4JG` VINs their year; the failure mode is `None`, not a
  wrong year.
- Source the registry counts in the code comment and the wiki. Lost: naming position 10's meaning (no source names it;
  T-VINA-2 correction 01 F2).
- Plan NONE, difficulty 2: a measured set extension, rehearsed with mutants.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | copy: `319 passed, 8 skipped` |
| step 2 | SIMULATED | copy: `15 passed` |
| step 3 | SIMULATED | copy on `PYTHONPATH`: `27 passed`, `41 passed`, `30 passed` |
| step 4 | SIMULATED | copy on `PYTHONPATH`: `8 passed, 43 deselected` |
| step 5 | SIMULATED | copy: `2`; base `0` |
| step 6 | SIMULATED (ruff) / DEFERRED (commit) | `All checks passed!` |

### Exclusivity ###
No other implementer runs. Built on `fix/T-AUD-7b` (`e4ad961`).

### Progress hook ###
T-VINA-17: VSA, WDF, WMX, 4JG and VDB digit-form VINs decode with model_year None; letter forms keep the year.

### Cold read ###
own pass 2026-11-04: anchors grep 1 each (`make_rh.py` asserts each old text once) · P1 on the base · P2 on the copy ·
traceability: criteria 1-5 → steps 1-6 · JUDGEMENT criteria: 0.
cold read 2026-11-04: skipped (Plan: NONE, difficulty 2, rehearsed edits).

### Correction history ###
- **01 (2026-11-04, Cowork review of round 1 with the second review; not accepted).** Round 1 equals `make_rh.py`
  byte for byte (`cmp`); Cowork's rerun matches P2. Second review (`second_review.py`, Codex) APPROVE WITH
  CORRECTIONS, re-derived with `recheck/T-VINA-17/non1.py`:
  - HIGH "WDF suppresses real year codes" NOT UPHELD as HIGH: WDF's 5 non-`1` digit-form VINs, none within one year
    of its registration; the 2 `J` VINs (2018) match only on the 30-year cycle, outside the 1990-2010 scope. One
    in-scope VIN (`WDF63981583465221`, `8`, registered 2010) is ambiguous; the rule gives `None`, not a wrong year,
    the trade T-VINA-2 accepted for WDB (4 of 75 match). Recorded as the residue in the wiki wording (R5.1).
  - MEDIUM wording overstates the evidence: UPHELD (R5.1, exact counts, the 2000-2002 ambiguity stated).
  - MEDIUM surviving mutant `vin[9] == "1"`: UPHELD (R5.3, test with `WDF44770323287218`; M3 rehearsed `1 failed`).
  - LOW unsourced model and country labels: UPHELD (R5.1, R5.2).
  Rehearsed (`make_rh2.py` on `rh2/`): vinlab `320 passed, 8 skipped`, new file `16 passed`, M3 `1 failed`, ruff clean,
  doc grep `2`. The first run on a fresh copy printed `65 errors`; the rerun with a new `--basetemp` was clean (copy
  artefact; the branch run was clean).
