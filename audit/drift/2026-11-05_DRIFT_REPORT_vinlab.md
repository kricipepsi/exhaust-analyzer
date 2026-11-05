# Drift report - VINLab design documents vs code (2026-11-05, T-AUD-11c)

## labs/vinlab/README.md

- [DIVERGENCE] The README says a 484 MB `mysql_data/` copy sits in the lab folder; the folder is not in the working tree and no file under it is tracked. Doc: `labs/vinlab/README.md:8` "`mysql_data/` (~484 MB) was copied verbatim for now". Code: ABSENT (`ls -d labs/vinlab/mysql_data; git ls-files labs/vinlab/mysql_data | wc -l` -> No such file or directory; 0).

## labs/vinlab/docs/PRD_VINLab.md

- [DIVERGENCE] KR6 says every numeric literal in `vinlab/` carries a citation comment; the year-1996 downstream-O2 rule in the decoder has none. Doc: `labs/vinlab/docs/PRD_VINLab.md:108` "Every numeric literal in `vinlab/` carries a wiki/standard citation comment". Code: `labs/vinlab/vinlab/decoder.py:388` "model_year >= 1996".

## labs/vinlab/docs/HLD_VINLab.md

- [DIVERGENCE] The HLD puts the low-volume manufacturer code at positions 12-13, but the extended WMI key slices positions 12-14. Doc: `labs/vinlab/docs/HLD_VINLab.md:135` "places the manufacturer code at positions 12–13". Code: `labs/vinlab/vinlab/decoder.py:850` "extended = vin[0:3] + vin[11:14]".
- [DIVERGENCE] The HLD says an unresolved engine always grades NONE; when the WMI brand is blank the engine is None but `engine_not_in_csv` is not set, so the grade is PARTIAL. Doc: `labs/vinlab/docs/HLD_VINLab.md:99` "engine None → conf flag (NONE)". Code: `labs/vinlab/vinlab/decoder.py:614` "wmi_brand_missing".
- [UNDOCUMENTED] The year resolver returns None for digit-form type-code VINs of 11 WMIs (for example WDB, VSA, WDF); the HLD lists only the passthrough characters. Doc: `labs/vinlab/docs/HLD_VINLab.md:140` "{0, U, Z}". Code: `labs/vinlab/vinlab/decoder.py:878` "if vin[:3] in _TYPE_CODE_WMIS and vin[3:9].isdigit():".
- [UNDOCUMENTED] Engine resolution flags a VDS match as ambiguous when its `majority_share` is below 0.70 and the HLD does not say so. Doc: `labs/vinlab/docs/HLD_VINLab.md:151` "Returns the CSV row or `None`". Code: `labs/vinlab/vinlab/decoder.py:816` "ms < 0.70".
- [UNDOCUMENTED] A `vref.db` row is discarded when the model year is outside its `my_start`-`my_end` window, which sets the `vref_year_out_of_window` flag; the HLD pipeline has no such step. Doc: `labs/vinlab/docs/HLD_VINLab.md:98` "→ db_row | None". Code: `labs/vinlab/vinlab/decoder.py:610` "vref_year_out_of_window".
- [UNDOCUMENTED] When no applied `vref.db` row states a recognised euro norm, the decoder sets `euro_unknown` and derives the horizon from the model year; the HLD pipeline shows only the euro to horizon map. Doc: `labs/vinlab/docs/HLD_VINLab.md:104` "euro→horizon → stress RPM → CoC overlay". Code: `labs/vinlab/vinlab/decoder.py:690` "euro_unknown".
- [DIVERGENCE] The HLD names the COMLab projector as a caller of `decode`; no file under `labs/comlab` imports `vinlab`, and the callers are `apps/wired` and `apps/ui`. Doc: `labs/vinlab/docs/HLD_VINLab.md:50` "caller (DNALab assembly / COMLab projector / tooling)". Code: `apps/wired/wired/composition.py:75` "from vinlab import decode as decode_vin".

## labs/vinlab/docs/LLD_VINLab.md

- [DIVERGENCE] The LLD shows the 1996 rule with the comment `# source: OBD-II mandate`; the code line has no comment. Doc: `labs/vinlab/docs/LLD_VINLab.md:146` "# source: OBD-II mandate". Code: `labs/vinlab/vinlab/decoder.py:388` "model_year >= 1996".
- [DIVERGENCE] The LLD gives banks as 2 only when `is_v_engine` is set; the code also gives 2 for a BOXER map configuration. Doc: `labs/vinlab/docs/LLD_VINLab.md:145` "_number_of_banks = 2 if db.is_v_engine else 1". Code: `labs/vinlab/vinlab/decoder.py:374` "or csv_config.startswith(".
- [UNDOCUMENTED] The LLD year listing has one early return (passthrough); the code has a second early return for type-code WMIs. Doc: `labs/vinlab/docs/LLD_VINLab.md:120` "if year_char in _YEAR_PASSTHROUGH: return (None, None)". Code: `labs/vinlab/vinlab/decoder.py:878` "if vin[:3] in _TYPE_CODE_WMIS and vin[3:9].isdigit():".
- [UNDOCUMENTED] The O2 derivation takes the model year 2000 when the year is unknown; the LLD does not state this input. Doc: `labs/vinlab/docs/LLD_VINLab.md:196` "year >= 2001 and fuel ∈ {GDI, PORT_INJECTION} → WIDEBAND_AFR". Code: `labs/vinlab/vinlab/decoder.py:384` "model_year if model_year is not None else 2000".

## labs/vinlab/docs/DLD_VINLab.md

- [DIVERGENCE] The DLD derives `has_maf` as `bool(db.has_maf)` whenever the row has it; the code treats a stored 0/0 pair on an injected engine as unknown. Doc: `labs/vinlab/docs/DLD_VINLab.md:208` "has_maf = bool(db.has_maf)". Code: `labs/vinlab/vinlab/decoder.py:510` "db_maf = db_map = None".
- [UNDOCUMENTED] The DLD lists two VDS indexes; the decoder builds four (exact and brand-folded for each path) and a `_fold_brand` helper. Doc: `labs/vinlab/docs/DLD_VINLab.md:188` "{BRAND_VDSFULL → row}". Code: `labs/vinlab/vinlab/decoder.py:222` "self.vds_full_exact_index".
- [UNDOCUMENTED] The DLD confidence flag list omits `vref_year_out_of_window` (decoder.py:610), `euro_unknown` (690), `wmi_brand_missing` (798) and `vds_engine_ambiguous` (817). Doc: `labs/vinlab/docs/DLD_VINLab.md:271` "engine:  engine_not_in_csv | no_engine_code | engine_not_in_vref". Code: `labs/vinlab/vinlab/decoder.py:610` "vref_year_out_of_window".
- [UNDOCUMENTED] The module map lists four data files; the data folder also holds `vref_db1.db`. Doc: `labs/vinlab/docs/DLD_VINLab.md:65` "wmi.csv, years.csv, vds_engine_map.csv, vref.db". Code: ABSENT (`ls labs/vinlab/vinlab/data; grep -rn vref_db1 labs/vinlab/vinlab --include=*.py` -> vds_engine_map.csv vref.db vref_db1.db wmi.csv years.csv; no grep output).
- [UNDOCUMENTED] `lookup_engine_ref` retries with a normalised engine code (uppercase, alphanumeric) after the exact query misses; the DLD shows the exact query only. Doc: `labs/vinlab/docs/DLD_VINLab.md:258` "SELECT * FROM engine_ref WHERE engine_code = ?". Code: `labs/vinlab/vinlab/db/tecdoc_query.py:75` "Fallback: normalized match".
- [DIVERGENCE] The DLD calls `from_json()` the inverse of `to_json()`; `to_json()` returns a JSON string and `from_json()` takes a dict. Doc: `labs/vinlab/docs/DLD_VINLab.md:130` "`to_json()` walks via". Code: `labs/vinlab/vinlab/models.py:256` "def from_json(cls, payload: dict[str, Any]) -> VinDNA:".

## labs/vinlab/docs/BDD_VINLab.md

No drift detected.

## labs/vinlab/docs/VIN_VOCABULARY.md

- [UNDOCUMENTED] The confidence flag table omits `vds_engine_ambiguous` (set when `majority_share` is below 0.70) and `wmi_brand_missing`. Doc: `labs/vinlab/docs/VIN_VOCABULARY.md:126` "| `engine_not_in_csv` | no `vds_full`/`pos_8_only` match | NONE |". Code: `labs/vinlab/vinlab/decoder.py:817` "vds_engine_ambiguous".

## labs/vinlab/docs/ADR_VINLab.md

No drift detected.
