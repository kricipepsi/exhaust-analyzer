# T-VINA-13a — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. **Source:** the operator named `D:\4DLab\4DLabV2\DBS\1Q2019` and required REA first (2026-11-04). REA 6.7.0
   inspected a SQLite snapshot of 6 tables (`C:/4DApp/recheck/rea_1q2019/REA_LEDGER.md`, schema evidence
   `ev_ce9eaca5…`). REA has no CSV route; the tool reads the CSVs directly.
2. **Measured (P3-P5)** with `C:/4DApp/recheck/scratch/vina13_measure.py` on fix/T-VINA-5 `7ba9368` (2026-11-04):
   5,881 map pairs, 32 in vref.db, 1,412 brand-agreeing TecDoc matches; real VINs 1,115 / 18 / 631.
3. **The old path:** `tools/build_vref_db.py::_extract_tecdoc` reads a MySQL TecDoc with another schema (Russian
   values) and writes synthetic codes `BRAND_<cc>cc_<ind>_TecDoc_<id>`, and guesses years from the euro norm. That is
   the root of the 18-row reach.
4. **vref.db:** 72 rows, `engine_code` PRIMARY KEY; vocab PORT_INJECTION/GDI, NATURALLY_ASPIRATED/TURBOCHARGED,
   euro1-euro6; `valvetrain_type` all NULL.

### Rulings and the tradeoff that lost ###
- Split extract (13a) from merge (13b): the extract is reviewable as a CSV before any decode changes. Lost: one row
  that changes vref.db directly (a bigger diff with downstream effects, harder to review).
- Brand must agree (folded, plus a pinned same-company alias table). Lost: the 670-VIN code-only match, which takes
  another maker's engine on a code collision.
- Platform shares (HYUNDAI/KIA, VAG) are reported, not written. Lost: about 30 more pairs.
- Years from linked cars, never from the euro norm. Lost: a filled my_end on open-ended engines.
- Plan REQUIRED, difficulty 4: new construction with vocabulary mapping choices.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base `248 passed, 8 skipped` (T-VINA-5 review, 2026-11-04) |
| step 2 | DEFERRED | the test file does not exist |
| step 3 | DEFERRED | the tool does not exist; the snapshot build read the same CSVs in under 5 min |
| step 4 | RAN | `coverage.py` on a smoke CSV: `vins_with_code 1115, vref_today 18` |
| step 5 | DEFERRED | ruff and the commits |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-VINA-13a: TecDoc 1Q2019 per-engine extract CSV for the engine map's codes (brand-agreeing), with a coverage report.

### Cold read ###
own pass 2026-11-04: P1-P5 measured · traceability: criteria 1-4 → steps 1-5 · JUDGEMENT: 0.
cold read 2026-11-04: skipped, plan-gated (Plan: REQUIRED; the plan review and its second-model review cover it).

### Correction history ###
- **01 (2026-11-04, plan review; Plan: APPROVED with C1-C6).** Second review (ds-pro, embedded): APPROVE WITH
  CORRECTIONS, 8 findings, re-derived (`C:/4DApp/recheck/scratch/vina13_alias.py`, `vina13_t1check.py`: rows 1,503
  equal the plan). Upheld F2 (all-digit keys, C1), F4 (FAMILY, C2), F5 (twincharger, C3), F6 (C4), F7 (C5), petrol
  order (C6). Not upheld: F1 (whole-X key: my R3 wording, now named), F3 (Genesis is a Hyundai brand), F8 (P4 groups by
  manufacturer set). Record: `corrections/T-VINA-13a_plan_correction_20261104.md`.
