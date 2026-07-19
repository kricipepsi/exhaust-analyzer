# Graph Report - C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\vinlab\vinlab  (2026-06-13)

## Corpus Check
- Corpus is ~6,181 words - fits in a single context window. You may not need a graph.

## Summary
- 150 nodes · 255 edges · 21 communities (13 shown, 8 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]

## God Nodes (most connected - your core abstractions)
1. `RobustVINDecoder` - 23 edges
2. `_displacement_fallback()` - 18 edges
3. `CylinderHint` - 17 edges
4. `VINDecodeError` - 15 edges
5. `from_json()` - 13 edges
6. `ChassisNumberError` - 12 edges
7. `InductionType` - 9 edges
8. `EuroEmissionCategory` - 8 edges
9. `AirMeteringStrategy` - 8 edges
10. `FuelDeliveryType` - 8 edges

## Surprising Connections (you probably didn't know these)
- `VINDecodeError` --uses--> `VinDNA`  [INFERRED]
  decoder.py → models.py
- `ChassisNumberError` --uses--> `VinDNA`  [INFERRED]
  decoder.py → models.py
- `RobustVINDecoder` --uses--> `AirMeteringArchitecture`  [INFERRED]
  decoder.py → models.py
- `RobustVINDecoder` --uses--> `AirMeteringStrategy`  [INFERRED]
  decoder.py → models.py
- `RobustVINDecoder` --uses--> `Emissions`  [INFERRED]
  decoder.py → models.py

## Communities (21 total, 8 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.12
Nodes (32): StrEnum, ChassisNumberError, Apply the tech-mask and CoC measurements from vref.db or fall back to CSV-only d, Raised when a VIN cannot be decoded within VINLab's supported scope., Raised when input length != 17 — likely a pre-VIN chassis/frame number.      Cal, VINDecodeError, AirMeteringArchitecture, AirMeteringStrategy (+24 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (12): Adaptive VIN decoder with position-8 fallback and L-year disambiguation.      Lo, Return True if checksum validation should be skipped for this VIN.          Chec, Extract displacement, cylinders, and bank count from CSV engine_row., Apply last-resort cylinder heuristic fallback (T-VL-7).          Fires only as l, Derive air metering strategy and architecture from DB dict, fuel system, and ind, Compute VIN decode confidence based on collection of confidence flags., Decode a 17-char VIN into a VinDNA dataclass.          Zero network, zero MySQL., NHTSA modulo-11 checksum with bypass paths.          Per VINlookup.md §1: the NH (+4 more)

### Community 2 - "Community 2"
Cohesion: 0.24
Nodes (11): _induction(), _infer_bmw(), _infer_vw_audi(), _is_turbo_bmw(), _make_disp_hint_with_induction(), Cylinder-count inference from engine code + displacement + brand.  Last-resort r, BMW: [NBMS]XX pattern — first of the two digits encodes cylinders.      2→4, 4→4, VW/Audi: use displacement bands (code prefixes are unreliable).      Per T-VL-7 (+3 more)

### Community 3 - "Community 3"
Cohesion: 0.20
Nodes (10): _displacement_fallback(), infer_cylinder(), _infer_mercedes(), _infer_renault(), _infer_toyota(), Toyota: family prefix → cylinder count., Mercedes: MXXX engine-code lookup table., Renault/Dacia: family lookup table. (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (7): _is_non_petrol(), _normalise_euro(), pre_clean_vin(), RobustVINDecoder — per VINlookup.md (patched) with overlay rules.  Adaptive VIN, Normalise a raw euro_norm string to the contract enum form., Check any value for non-petrol fuel keywords (H1 guard)., Substitute visually ambiguous characters before VIN validation.      Replaces ``

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (8): CylinderHint, _infer_honda(), _infer_hyundai_kia(), _infer_mazda(), Hyundai/Kia: G[cyl] prefix — second char is the cylinder digit., Honda: J-series (≥3.0L) is V6; most others are I4., Inferred engine attributes from brand naming + displacement fallback.      Args:, Mazda: B/F/P/K prefix → I4.

### Community 6 - "Community 6"
Cohesion: 0.29
Nodes (6): euro_to_horizon(), euro_emission_category -> Horizon enum mapping per SEMANTIC_CONTRACT §6.4., Map EuroEmissionCategory to architecture horizon per contract §6.4.      EURO_1,, Map a calendar year to its architecture horizon.      Used only when euro_emissi, _year_to_horizon(), ValueError

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (5): _coerce_enum_values(), Decoded vehicle profile produced by vinlab.decode().      Schema governed by SEM, Serialize to a JSON-safe dict matching SEMANTIC_CONTRACT.md §4.1.          Uses, Recursively convert Enum members to their .value form., VinDNA

### Community 8 - "Community 8"
Cohesion: 0.33
Nodes (5): lookup_engine_ref(), open_vref_readonly(), SQL isolation layer for vref.db — all SQL strings live here (H8).  The decoder c, Query vref.db engine_ref for tech-mask and CoC measurements.      Args:, Open vref.db in read-only mode via URI.      The decoder calls this once in __in

### Community 9 - "Community 9"
Cohesion: 0.40
Nodes (5): AirMeteringClassification, classify_air_metering(), Air metering classification — single deep module replacing two parallel switches, One classification for the (has_maf, has_map) fact.      Contract §8:       prim, Return both air-metering labels from a single classification of (has_maf, has_ma

### Community 10 - "Community 10"
Cohesion: 0.40
Nodes (5): decode(), _get_decoder(), VINLab — VIN decoder module.  Decodes a 17-character VIN into a structured VinDN, Return a RobustVINDecoder for `data_dir`. Cached per distinct data_dir., Decode a 17-char VIN into a VinDNA. Offline, no network, no MySQL.

### Community 11 - "Community 11"
Cohesion: 0.50
Nodes (3): engine class -> stress_idle_rpm_target mapping.  Per OBD_VOCABULARY.md §3.2: the, Return the stress-idle RPM target for a given vehicle profile.      Args:, stress_idle_rpm()

### Community 12 - "Community 12"
Cohesion: 0.50
Nodes (3): derive_upstream_o2_type(), Derived field computation for upstream O2 sensor type., Return the upstream O2 sensor type per contract §8 UpstreamO2Type enum.      Arg

## Knowledge Gaps
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RobustVINDecoder` connect `Community 1` to `Community 0`, `Community 10`, `Community 4`, `Community 7`?**
  _High betweenness centrality (0.166) - this node is a cross-community bridge._
- **Why does `VinDNA` connect `Community 7` to `Community 0`, `Community 1`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `euro_to_horizon()` connect `Community 6` to `Community 1`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `RobustVINDecoder` (e.g. with `AirMeteringArchitecture` and `AirMeteringStrategy`) actually correct?**
  _`RobustVINDecoder` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `VINDecodeError` (e.g. with `AirMeteringArchitecture` and `AirMeteringStrategy`) actually correct?**
  _`VINDecodeError` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `RobustVINDecoder — per VINlookup.md (patched) with overlay rules.  Adaptive VIN`, `Raised when a VIN cannot be decoded within VINLab's supported scope.`, `Raised when input length != 17 — likely a pre-VIN chassis/frame number.      Cal` to the rest of the system?**
  _73 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.12299465240641712 - nodes in this community are weakly interconnected._