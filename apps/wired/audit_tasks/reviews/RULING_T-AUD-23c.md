# RULING T-AUD-23c — code vs own-wiki suspects (Windows Cowork, 2026-11-16)

Scope: every register claim with a `suspect` note, no verdict, and no `RESOLVED` or `NOT LIVE` tag. There are
63 such claims (comlab 31, gaslab 23, rest 9), on `fix/T-AUD-24g` (`a791719`). No web access was used: each ruling
compares the code with the repo's own text. Corpus = the v7 set (314 cases), `recheck/T-AUD-24f/`. The tip gives 221
of 314 correct by family.

## 1. Not live — tag `NOT LIVE (T-AUD-23c)`, no fix (19)

- v1 registry and KG text (`USE_V2_REGISTRY=0` only; see `RULING_T-AUD-24f_24g.md`):
  CK0757, CK0770, CK0779, CK0788, CK0799, CK0934, CK1024 (`global_fault_registry.json`); CK1098, CK1119, CK1254,
  CK1255, CK1286, CK1315, CK1349, CK1351, CK1353, CK1355 (`config/kg/*.json`).
- `config/proposals/entries.yaml` (CK1517, CK1545): no code loads the file. `fault_atlas_router.py:1114` names it in a
  comment only.

## 2. Covered by an earlier ruling or row (16)

- T-GASA-FEURO (GASLab ledger, deferred): GK0049, GK0051, GK0054, GK0056 (`_EURO_THRESHOLDS`), GK0078, GK0079,
  GK0183, GK0184 (CAM_TIMING_RETARDED_MAP fallback). Its blocker was "fix after the Euro table is source-verified".
  T-GASA-17 verified that table (W0124 PARTLY, W0126/W0129/W0131 CONTRADICTED), so the row is now unblocked.
- T-AUD-23b PARTLY ruling ("wide UI input bounds … block no real reading"): RK0088 (IAT schema -40 to 140 °C),
  RK0249, RK0431 (MAF 500 g/s), RK0404, RK0405 (O2 0.0-1.0 V), RK0434, RK0435 (WOT lambda 0-3).
- T-AUD-17 (cold cutoff 70 vs 75 °C, OBDLab vs the registry FF rule): CK0129.

## 3. Code equals its own wiki — not a drift, no fix (15)

The suspicion comes from the wiki claim, not from a difference between code and wiki. A web verification would be a
new row; none is registered because no verdict depends on these claims.
GK0006, GK0008, GK0062, GK0063, GK0083, GK0112, GK0113, GK0114, GK0139, GK0149, GK0150, GK0162, GK0163, and GK0091 (HC
75-500 ppm: the 75 comes from a superseded v1 range, but the window is only a fallback bound; folded into
T-GASA-FEURO's review of `resolution.py:460`). GK0094 (lambda 0.96 floor at 2500 rpm) goes with GK0091.

## 4. Defensible, no fix (8)

- CK0611 (RM-001 "λ < 0.97"): GASLab RICH_MIXTURE is λ ≤ 0.97 (`gas_lab_ontology.yaml:114`) with CO ≥ 0.5 %; the
  description matches the code. Measured λ 0.95: 0 of 314 change. λ 0.97 is about 3 % rich, so rich is defensible.
- CK0253 (`integration_shim.py:776`, absent CO2 → 15.0): the fill turns off only the `co2 < 12.0` term of an OR. The
  STFT and O2 terms still fire, so the result equals abstaining on that term. Not a defect.
- CK0056, CK0292 (confidence floor 0.70 vs doc ≳ 0.80), CK0085 (bonus bound 1.0 vs LLD 0.5): code-vs-design-doc
  drift with no domain truth behind it; no registry row uses a bonus above 0.5. Too small.
- CK0320, CK0329 (VVT DTC ranges in three rule descriptions): description text only, no gate. Too small.
- CK0397 (EF-005 description "[14,16]"): the description states the VALID band of `rule_engine.py:169-170`, which is
  what the code gates on. Text, no fix.

## 5. Fix rows (5 claims)

- **T-AUD-24h** (difficulty 2, `apps/ui`): RK0445, RK0446. The three upstream-O2 widgets (`app.py:536-540`) share one
  `FIELD_HELP["obd_upstream_o2_val"]` tooltip, `Range: 0.0–20.0` (`ui_payload.py:321-326`), while each widget
  enforces its own range (0-1 V, 0.7-1.3 λ, 10-20 AFR). This breaks `SHIP_UI_CONTRACT_2026-07-07.md` Amendment
  2026-07-08 ("tooltip and widget min/max come from one shared FIELD_HELP table so they cannot drift"). User-visible on
  the public app.
- **T-AUD-24i** (difficulty 2, COMLab rule data, measured 0 of 314 changed):
  CK0592 `overheating.json:14` `ect_c > 110.0` → `108.0`. The rule's own description says "above the
  OVERHEATING_THRESHOLD", and OBD_VOCABULARY §23.1 sets that at 108 °C.
  CK0012 `delta_engine.py:178` `_FLATCAM_ELEV_O2_MIN 2.0` → `2.5`, to match its own comment and delta-relations/07
  GAS-FC-001.
  CK0440 LC-001 description "> 1.03" → "> 1.05", to match GASLab LEAN_MIXTURE (`gas_lab_ontology.yaml:126`).

Lost alternative for section 4: align every value with the vocabulary. With 0 of 314 changed, that would be a change
without evidence of a gain, and two rulings (CK0611, CK0253) find the code right as it is.
