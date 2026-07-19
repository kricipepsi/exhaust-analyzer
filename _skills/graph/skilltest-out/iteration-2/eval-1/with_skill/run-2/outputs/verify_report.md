# 4dlab-wiki-prep verify report

--=={ 4dlab-wiki-prep: wiki_fix / relations+labels+roster+verify }==--

Source fixture directory: `C:\tmp\gfxskilltest\iteration-2\wiki_fix`
Output directory: `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\_skills\graph\skilltest-out\iteration-2\eval-1\with_skill\run-2\outputs`

| Chunk | Source SHA256 | Output body-prefix SHA256 | Prefix preserved | Relation blocks | Core Entities blocks | Relation lines | Output SHA256 |
|---|---|---|---:|---:|---:|---:|---|
| `dtc_fault_map.md` | `298cb822b13074236337dae15e6a99ee6879343f1e4d0adac09a27679441108d` | `298cb822b13074236337dae15e6a99ee6879343f1e4d0adac09a27679441108d` | yes | 1 | 1 | 6 | `c6c634475f59cef36c07da2ec7d74de3ceaa558fba1aa295bc73efc37e366403` |
| `trim_analytics.md` | `4a4bbb5b47a22ff14ea2c8c9f483fc72b0a5838abcec47cb0a50b409ebd6638b` | `4a4bbb5b47a22ff14ea2c8c9f483fc72b0a5838abcec47cb0a50b409ebd6638b` | yes | 1 | 1 | 6 | `06810fff8fdf657d9e5bc4ae3170389b3201e9da282d878b666a113cb045811f` |

Checks:
- Append-only evidence: for each output, the first N bytes where N is the source byte length hash to the same SHA256 as the fixture file.
- Trailer coverage: each chunk has exactly one `## Graph relations (explicit)` block and exactly one `## Core Entities` block.
- Canonical labels used in trailers: `TrimAnalyticsGate.O2_FAULT_ACTIVE`, `TrimAnalyticsGate.FUEL_TRIM_ACTIVE`, `STUCK_LEAN`, `STUCK_RICH`, `SENSOR_RESPONSE_DEGRADED`.
- Known non-edge preserved as a non-edge: `SUPPRESS_POST_CAT_TRIM` is written as `IS_NOT a TrimAnalyticsGate value`, not as an enum member.