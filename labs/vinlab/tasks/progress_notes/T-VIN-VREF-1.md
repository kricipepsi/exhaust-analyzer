# T-VIN-VREF-1 progress note

Status: done
Date: 2026-07-07

## Delivered tranche

Added three top-traffic automotive petrol engine codes to the reproducible vref override path and checked-in `vref.db`:

| Rank | Engine code | Map-row references | vref row |
|---:|---|---:|---|
| 1 | `EJ20` | 49 | added |
| 2 | `N55B30A` | 45 | added |
| 3 | `B48B20B` | 41 | added |

The implementation touched only the data path:

- `tools/vref_manual_overrides.yaml` — appended the three sourced override rows.
- `vinlab/data/ARCHIVE/vref_pre_VREF1.db` — archived the pre-task database.
- `vinlab/data/vref.db` — seeded the three rows through the builder module's `_load_yaml_entries` parsing and canonical `INSERT_ROW` tuple shape, preserving existing checked-in CoC enrichment because the external DBS petrol CSV is not mounted in this checkout.
- `tests/unit/test_decoder.py` — added a VREF-1 regression covering one representative shipped-map VDS per new code.

No decoder logic, `VinDNA` schema, fuzzy matching, WMI, or VDS map row changed.

## Per-code source table

### `EJ20` — Subaru 2.0 petrol boxer

| Field | Value | Source |
|---|---:|---|
| engine/application | Subaru EJ20 2.0L gasoline flat-four, used in Legacy/Impreza-era applications | MotorReviewer EJ20 spec page: https://www.motorreviewer.com/engine.php?engine_id=52 |
| displacement | 1994 cc | Same MotorReviewer EJ20 spec page |
| induction | `NATURALLY_ASPIRATED` | Same MotorReviewer page states four-stroke naturally aspirated/turbocharged variants; this row is the naturally aspirated tranche for map rows whose shipped CSV fuel is `PORT_INJECTION` |
| fuel delivery | `PORT_INJECTION` | Same MotorReviewer page lists fuel system as fuel injection; shipped `vds_engine_map.csv` rows for `EJ20` are `PORT_INJECTION` |
| VVT | false | Conservative naturally aspirated EJ20 tranche row; the VVT-positive Dual AVCS EJ20X/EJ20Y variants remain separate and are not collapsed into this row: https://en.wikipedia.org/wiki/Subaru_EJ_engine |
| load sensor | MAF present, MAP absent | Subaru Impreza/Legacy MAF replacement/application sources show a MAF on the intake path: https://www.ebay.com/itm/406938777965 and https://www.youtube.com/watch?v=4xE4QvsX0vc |
| upstream O₂ | `WB` | VINLab `derive_upstream_o2_type` maps post-2000 petrol rows with `WB` hints to `WIDEBAND_AFR`; row is Euro 4 / 2000s petrol |
| rated RPM | 6000 | MotorReviewer EJ20 naturally aspirated output range; representative 2.0R/GX applications are rated around 6000 rpm |
| high-idle target / lambda target / natural idle | 2500 RPM / 1.000 / 700 RPM | UK MOT catalyst idle limits define fast idle lambda band around stoichiometric and natural idle test; https://www.gov.uk/guidance/mot-inspection-manual-for-private-passenger-and-light-commercial-vehicles/8-nuisance |
| low/high-idle CO bounds | 0.3% / 0.2% | Same UK MOT catalyst idle limit source |
| type-approval CO / HC / NOx | 1.000 / 0.100 / 0.080 g/km | Euro 4 petrol legal type-approval limits, used as capped pollutant values where vehicle-specific pollutant grams were not available: https://dieselnet.com/standards/eu/ld.php |
| CO₂ | 206.0 g/km | 2005 Subaru Impreza GX Sport 2.0 CO₂ listing: https://vehiclescore.co.uk/co2-emissions-check/subaru/impreza and https://car-emissions.com/cars/view/17231 |

### `N55B30A` — BMW N55 3.0 petrol turbo

| Field | Value | Source |
|---|---:|---|
| engine/application | BMW N55 3.0 inline-six petrol turbo, variant family covering `N55B30A` map rows | FCP Euro N55 guide: https://www.fcpeuro.com/blog/the-definitive-guide-to-the-bmw-n55-engine-common-faults-tech-specs-upgrades |
| displacement | 2979 cc | Same FCP Euro N55 guide; BMWBlog N55 spec corroboration: https://www.bmwblog.com/2023/12/12/bmw-n55-engine-pros-cons-and-reliability/ |
| induction | `TURBOCHARGED` | Same FCP Euro / BMWBlog N55 sources |
| fuel delivery | `GDI` | Same FCP Euro / BMWBlog sources describe direct injection |
| VVT | true | BMWBlog describes Valvetronic / variable valve timing; FCP Euro describes N55 Valvetronic architecture |
| load sensor | MAP present, MAF absent | ICCT/EMISIA report for tested turbocharged gasoline direct-injection BMW notes no MAF and intake-air calculation based on MAP: https://www.duh.de/fileadmin/user_upload/download/Projektinformation/Verkehr/dieselgate/170828_ICCT-Test_Real_World_BMW_2017.pdf |
| upstream O₂ | `WB` | BMW 135i/335i parts application lists DENSO upstream 5-wire wideband oxygen sensor: https://shop.advanceautoparts.com/find/bmw-135i-air-flow-sensors |
| rated RPM | 5800 | FCP Euro N55B30M0 spec table lists horsepower at 5800–6400 RPM |
| high-idle target / lambda target / natural idle | 2500 RPM / 1.000 / 700 RPM | UK MOT catalyst idle limit source: https://www.gov.uk/guidance/mot-inspection-manual-for-private-passenger-and-light-commercial-vehicles/8-nuisance |
| low/high-idle CO bounds | 0.3% / 0.2% | Same UK MOT catalyst idle limit source |
| type-approval CO / HC / NOx | 1.000 / 0.100 / 0.060 g/km | Euro 5 petrol legal type-approval limits: https://dieselnet.com/standards/eu/ld.php |
| CO₂ | 186.0 g/km | 2011 BMW 335i F30 technical page: https://www.carfolio.com/bmw-335i-256938 |

### `B48B20B` — BMW B48 2.0 petrol turbo

| Field | Value | Source |
|---|---:|---|
| engine/application | BMW B48 2.0 inline-four petrol turbo, variant family covering `B48B20B` map rows | BMW B48 overview: https://en.wikipedia.org/wiki/BMW_B48; B48A20B engine guide: https://www.enginecode.uk/bmw/b48a20b-specs |
| displacement | 1998 cc | Same BMW B48 / EngineCode sources |
| induction | `TURBOCHARGED` | Same BMW B48 / EngineCode sources |
| fuel delivery | `GDI` | BMW B48 source lists central high-pressure gasoline direct injection; EngineCode states direct fuel injection |
| VVT | true | BMW B48 source lists Valvetronic and Double VANOS |
| load sensor | MAF present, MAP present | AUTODOC applications list both F30 320i B48 MAF and MAP sensors: https://www.autodoc.co.uk/car-parts/mass-airflow-sensor-airflow-meter-12906/bmw/3er-reihe/3-f30-f35-f80/116010-320-i and https://www.autodoc.co.uk/car-parts/sensor-intake-manifold-pressure-15024/bmw/3er-reihe/3-f30-f35-f80/116010-320-i |
| upstream O₂ | `WB` | VINLab keeps BMW modern GDI/turbo rows wideband; B48 is Euro 6 GDI and the row follows the existing BMW B48 family override |
| rated RPM | 5200 | Existing checked-in `B48B20` vref family row, preserved from prior CoC enrichment, carries 5200 RPM; `B48B20B` is the map variant sibling |
| high-idle target / lambda target / natural idle | 2500 RPM / 1.000 / 700 RPM | UK MOT catalyst idle limit source: https://www.gov.uk/guidance/mot-inspection-manual-for-private-passenger-and-light-commercial-vehicles/8-nuisance |
| low/high-idle CO bounds | 0.3% / 0.2% | Same UK MOT catalyst idle limit source |
| type-approval CO / HC / NOx | 1.000 / 0.100 / 0.060 g/km | Euro 6 petrol legal type-approval limits: https://dieselnet.com/standards/eu/ld.php |
| CO₂ | 159.0 g/km | Existing checked-in `B48B20` vref family row from prior CoC enrichment; BMW Group B48 press page gives B48 combined CO₂ range 175–112 g/km, which contains this family value: https://www.press.bmwgroup.com/global/photo/detail/P90220418/bmw-twinpower-turbo-four-cylinder-petrol-engine-b48-06-2016 |

## Skipped / quarantined codes

These high-count rows were excluded before sourcing because they are not suitable automotive petrol engine-reference rows for GasLab/OBDLab tech-mask recovery:

| Code | Map-row references | Reason |
|---|---:|---|
| `139QMB` | 55 | scooter/powersports engine code, out of automotive scope |
| `4` | 40 | single-character junk / non-engine code |
| `M` | 39 | single-character junk / non-engine code |
| `BN139QMB` | 37 | scooter/powersports engine code, out of automotive scope |
| `B` | 35 | single-character junk / non-engine code |
| `ROTAX 810` | 33 | powersports/kart/Can-Am code, out of automotive petrol tech-mask scope |

## Coverage before / after

Distinct mapped engine codes joining `engine_ref`:

- Before: 23 / 5,363 in this checkout's current DB snapshot (`T-VIN-VREF-1` task text recorded an older audited start of 27; the local executable baseline measured before edit was 23).
- After: 26 / 5,363.
- Database rows: 69 → 72.

Top still-missing non-quarantined codes for the next tranche:

1. `PE` — 41 rows
2. `D4F D7` — 41
3. `HN05` — 39
4. `G4FA` — 37
5. `CBZ` — 36
6. `B38A15A` — 35
7. `B48B20A` — 33
8. `NFU` — 33
9. `N20B20A` — 31
10. `5` — 30 (needs classification before sourcing; may be junk)
11. `K4MA7` — 30
12. `KFW` — 28

## VIN regression disclosure

The regression uses representative VIN strings built from real shipped-map VDS rows because the external petrol specimen corpus is not mounted in this checkout and targeted web searches for public full VINs by VDS/code returned no usable results. Each VDS is from `vinlab/data/vds_engine_map.csv`, has `majority_share=1.000`, and exercises the real decoder path from WMI → VDS → engine code → `vref.db` tech-mask:

| VIN used in test | Make | VDS | Engine code | Result |
|---|---|---|---|---|
| `JF1BC5CL0A1234567` | Subaru | `BC5CL` | `EJ20` | `HIGH`, 1.994 L, NA, port injection, Euro 4, MAF-only, CO₂ 206 |
| `WBA1B9100A1234567` | BMW | `1B910` | `N55B30A` | `HIGH`, 2.979 L, turbo, GDI, Euro 5, MAP-only, CO₂ 186 |
| `WBA1S3100G1234567` | BMW | `1S310` | `B48B20B` | `HIGH`, 1.998 L, turbo, GDI, Euro 6, dual MAF/MAP, CO₂ 159 |

The presentation guard remains green: `VF7SA5FR8AW511081` decodes to `CITROEN`, 1.598 L, `TURBOCHARGED`, `GDI`, `EURO_5`, `HIGH`.

## Verification gate

VERIFICATION GATE — T-VIN-VREF-1
================================
Syntax:         PASS (`python -m py_compile tests/unit/test_decoder.py tools/build_vref_db.py`)
Imports:        PASS (`import vinlab; import vinlab.decoder; import vinlab.db.tecdoc_query` with `DBS_ROOT=/agent_workspace/.vinlab_empty_dbs` for builder import)
Type check:     PASS (`python -m pyright vinlab` — 0 errors, 0 warnings, 0 informations)
Lint:           PASS (`python -m ruff check tools/build_vref_db.py tests/unit/test_decoder.py tests/unit/test_build.py`)
pytest targeted: PASS (`5 passed` — VREF-1 tranche, Citroën guard, overlap count)
pytest Layer-1: PASS (`python -m pytest tests -q` — 200 passed, 8 skipped)
Fast benchmark: SKIP (data-reference task; no model-output benchmark in VINLab)
Diff review:    PASS (data rows, DB archive/seed, decoder tests, progress note only; no decoder/schema/fuzzy-matching change)

Pythonskill checklist items applied:
- Type hints: existing touched test style is untyped; no new production function added.
- Docstrings: existing test class style uses descriptive test names; no public function/class added.
- No mutable defaults: PASS.
- No bare except: PASS.
- No magic numbers: sourced in this progress note and scoped to vref data rows/tests.
- f-strings: no new interpolation.
- Pathlib: existing tooling path style preserved.
- Context managers: DB/data operations used context managers in verification scripts.
- `is None` not `== None`: PASS.
- Sorted imports: no import changes.

## Code review

CODE REVIEW — T-VIN-VREF-1
==========================
Scope: PASS. The diff is confined to the vref data path, checked-in DB artifact/archive, tests, and this progress note.
Dependency rule: PASS. Runtime still reads `vref.db` through `vinlab/db/tecdoc_query.py`; no SQL or cross-lab import was added.
Signal/noise: PASS. New rows feed the existing named consumer `lookup_engine_ref` → `VinDNA` tech-mask; the test proves each row is read by a live decoder path.
Data provenance: WARNING. Engine/equipment and CO₂ values have URL provenance; pollutant CO/HC/NOx values use Euro legal type-approval limits where exact vehicle certificate pollutant grams were not available in the mounted sources. This is disclosed above rather than hidden as specimen-specific data.
Test quality: PASS. Regression asserts behavior visible to downstream consumers: displacement, induction, fuel, Euro class, MAF/MAP architecture, CO₂, and `HIGH` confidence.
Structural craft: PASS. No abstractions, shims, aliases, or decoder branches were added; the boring data path stayed boring.
