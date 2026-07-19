# VINLab Mini Data Fixture

This fixture is intentionally tiny and exists only for `T-DNA-TH-2` isolation tests.

- `wmi.csv` row `VF1`: source `VINlookup.md`, European WMI checksum-bypass behavior.
- `years.csv` row `2,2002,ERA_2`: source `VINlookup.md` scope note and year-code resolver behavior; `2002` is the model year for the known Renault VIN fixture.
- `vds_engine_map.csv` row `RENAULT,CB05C,D4F,1.1,4,PORT_INJECTION,INLINE`: source `VINlookup.md` dynamic VDS path description; numeric values are controlled fixture values consumed by `tests/unit/test_decode_isolation.py`.
- `seed.sql` row `D4F`: source is the fixture row itself; all numeric CoC values are characterization pins for decoder/`tecdoc_query` isolation, not production truth.
