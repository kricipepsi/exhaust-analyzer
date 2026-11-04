# T-VINA-12 — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. **Finding:** F-R3-2 (CONFIRMED): `JTE`, `JTM` decode as Subaru, `KNE` as Hyundai. Cause: `build_wmi_map.py`
   `_load_vpic_wmis` keeps the last make per WMI (dict overwrite); vPIC lists several makes (P6).
2. **Measured (P1)** on the Slovenian registry (cp1250; the first UTF-8 pass mis-read `ŠKODA`): 176 WMIs disagree
   with the registry majority, mostly two-wheelers. The 11 car WMIs of P1 carry 34 real C6 VINs.
3. **Measured (P2, P3):** the engine join on held-out file 3. The naive re-brand drops W matches 1001 → 398: the map
   was built under the wrong brands. So R2 is binding, and the floors include a control set C.
4. Map spellings: TOYOTA 292, KIA 226, JEEP 74, CHRYSLER 55, NISSAN 111, RENAULT 843, MG 13 rows (`grep -c`).

### Rulings and the tradeoff that lost ###
- Fix the make and hold the engine join with floors on held-out file 3. Lost: the naive re-brand (P3, a 60 % loss of
  matches) and a display-only make column (a second brand per WMI, which every reader would have to choose between).
- The plan chooses R2's mechanism. Lost: dictating T-VINA-5's vote (the plan may find a cheaper exact rule; the floors
  and the held-out file bind either way).
- Scope: the 11 car WMIs. Lost: all 176 (two-wheelers are out of the decoder's scope; `WBY` BMW I and `VX1` Yugo are
  sub-brand or historical names, not defects).
- Difficulty 4, plan REQUIRED: a data change with a measured regression risk.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | REHEARSED (base) | `320 passed, 8 skipped` on `fix/T-VINA-17` (T-VINA-17 review) |
| step 2 | DEFERRED | the plan's tests |
| step 3 | REHEARSED (base) | `27 passed`, `41 passed`, `30 passed` |
| step 4 | DEFERRED | the plan measures the base count (`-k f2_` alone: `6 passed`) |
| step 5 | REHEARSED (base) | `join_base.out`: W 1667/1125/1001/213, C 9215/5071/4388/3192 |
| step 6 | DEFERRED | ruff and the commits |

### Exclusivity ###
No other implementer runs. Built on `fix/T-VINA-17` (`8e8d121`).

### Progress hook ###
T-VINA-12: 11 car WMIs decode with the registry make; file-3 engine matches W ≥ 1001, C ≥ 4388.

### Cold read ###
own pass 2026-11-04: P1-P6 measured today · floors from `join_base.out` · traceability: criteria 1-4 → steps 1-6 ·
JUDGEMENT criteria: 0 (the plan's predictions become the expected values at the plan gate).
cold read 2026-11-04: skipped (Plan: REQUIRED; the plan gate reviews the mechanism).

### Correction history ###
- **01 (2026-11-04, plan gate; Plan: APPROVED with C1-C6).** Plan re-derived (`join_check.py` on `plan/data`: W
  1126/1004, C identical). Second review (Codex) APPROVE WITH CORRECTIONS; rulings in
  `corrections/T-VINA-12_plan_correction_20261104.md` (vote and tie rule not upheld; encoding, delete assert, `build()`
  test, untested renames, Path B upheld). Cowork added control set N to `join_check.py` (base = plan, 40056 matches).
