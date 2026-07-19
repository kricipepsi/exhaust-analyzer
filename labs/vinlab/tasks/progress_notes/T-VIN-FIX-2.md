# T-VIN-FIX-2 progress note

Status: done
Date: 2026-06-21

## Delivered tranche

The initial sourced tranche is one engine code: `5FR`. This is the presentation
engine and the only priority code for which every confidence-critical value was
sourced in this session. The next missing-code ranking is recorded below; no other
engine was populated from generic assumptions.

`5FR` now has a reproducible manual-override row and a baked `vref.db` row:

| Field | Value | Source |
|---|---:|---|
| engine/application | Citroën DS3 THP, `5FR (EP6DT)`, 2010–2015 | AUTODOC application listing: https://www.autodoc.parts/spares/citroen/ds3/ds3-2009/32035-1-6-thp-155 |
| displacement | 1598 cc | Citroën DS3 technical data: https://www.autoevolution.com/cars/citroen-ds3-2009.html |
| induction | `TURBOCHARGED` | Same Citroën DS3 technical data; fuel system is listed as turbocharged direct injection |
| fuel delivery | `GDI` | Same source. `GDI` is VINLab’s locked enum for direct injection; `DIRECT_INJECTION` is not a valid runtime enum |
| VVT | true | Existing canonical `EP6CDT` override plus the PSA/BMW Prince engine technical family |
| Euro class | Euro 5 | UK VCA-derived DS3 THP 155 record: https://www.fuelscandal.com/emissions-data/citroen/ds3/thp-155-244 |
| load sensor | MAP present, MAF absent | 5FR-specific MAP application: https://www.autodoc.parts/car-parts/sensor-intake-manifold-pressure-15024/citroen/ds3/ds3-2009/32035-1-6-thp-155 |
| upstream O₂ | `NB` | DENSO’s DS3 THP application maps to DOX-2005; DOX-2005 is a switching-type planar sensor: https://assets.denso-am.eu/production/attachments/DENSO-Lambda-Sensors-Product-Catalogue-2024.pdf and https://www.trodo.com/lambda-sensor-denso-dox-2005 |
| rated RPM | 6000 | Citroën DS3 technical data above |
| high-idle target | 2500 RPM | Existing VINLab manual-override/build contract default |
| lambda target | 1.000 | Existing VINLab manual-override/build contract default |
| normal idle | 700 RPM | EP6 technical adjustment data: https://www.scribd.com/document/862927138/EP6-specifications |
| low/high-idle CO bounds | 0.5% / 0.3% | Same EP6 technical adjustment data |
| type-approval CO / HC / NOx / CO₂ | 0.256 / 0.020 / 0.018 / 155.0 g/km | 2011 DS3 THP 150/156 technical record matching the early 5FR calibration: https://astradecarsales.co.uk/citroen_ds3_1.6_16v_thp_150hp_dsport_-id8795-.htm |

The source task requested rounded `1600 cc`; the row uses the authoritative exact
value `1598 cc`. It also requested `DIRECT_INJECTION`; the database uses the
contract-valid enum `GDI`.

## Reproducible build path

- Added `5FR` to `tools/vref_manual_overrides.yaml`.
- Extended `tools/build_vref_db.py` manual override loading so explicitly sourced
  MAP/MAF, rated-RPM, CoC, noise, and type-approval fields survive a rebuild.
- Seeded the checked-in database through the builder’s `_load_yaml_entries` and
  canonical `INSERT_ROW` path. Existing 68 rows and their CoC enrichment were
  preserved because the external bulk petrol CSV is not mounted in this checkout.

## Traffic ranking for the next sourced tranche

Ranked by `vds_engine_map.csv` row references after excluding codes already in
`vref.db`:

1. `PE` — 41 rows
2. `R2` — 29
3. `LF` — 22
4. `B3` — 18
5. `WL` — 15
6. `L8` — 15
7. `Y6`, `PY`, `FS` — 14 each
8. `P5`, `B6` — 13 each
9. `G4LA` — 12

These codes remain unseeded until per-code induction, Euro, O₂, and CoC values are
sourced. Reference-count ranking is not sufficient evidence for equipment values.

## Verification gate

- `python -m ruff check tools/build_vref_db.py tests/unit/test_build.py tests/unit/test_decoder.py` — passed.
- `python -m pyright vinlab` — 0 errors, 0 warnings.
- `python -m pytest tests -x -q` — 192 passed, 8 skipped.
- `vref.db` — 69 rows; 20 of 3,343 mapped engine codes now overlap.
- `VF7SA5FR8AW511081` — `CITROEN`, 1.598 L, `TURBOCHARGED`, `GDI`,
  `EURO_5`, `NARROWBAND`, `HIGH`.
- `VF3WB5FR8CE025644` — `Peugeot`, same authoritative `5FR` equipment,
  `HIGH`.

No `labs/vinlab/tasks/PROGRESS.md` ledger exists in this checkout, so there was no
ledger row to flip.
