# Graph Report - C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\obdlab\obdlab  (2026-06-09)

## Corpus Check
- 16 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 188 nodes · 492 edges · 11 communities (8 shown, 3 thin omitted)
- Extraction: 51% EXTRACTED · 49% INFERRED · 0% AMBIGUOUS · INFERRED: 243 edges (avg confidence: 0.53)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Code Community 0|Code Community 0]]
- [[_COMMUNITY_Code Community 1|Code Community 1]]
- [[_COMMUNITY_Code Community 2|Code Community 2]]
- [[_COMMUNITY_Code Community 3|Code Community 3]]
- [[_COMMUNITY_Code Community 4|Code Community 4]]
- [[_COMMUNITY_Code Community 5|Code Community 5]]
- [[_COMMUNITY_Code Community 6|Code Community 6]]
- [[_COMMUNITY_Code Community 7|Code Community 7]]
- [[_COMMUNITY_Code Community 8|Code Community 8]]
- [[_COMMUNITY_Code Community 9|Code Community 9]]
- [[_COMMUNITY_Code Community 10|Code Community 10]]

## God Nodes (most connected - your core abstractions)
1. `ObdLabDnaView` - 32 edges
2. `PIDValidationError` - 31 edges
3. `RpmStateBucket` - 25 edges
4. `VEEngine` - 22 edges
5. `PIDIngestionValidator` - 21 edges
6. `FuelSystemStatus` - 21 edges
7. `LinearityAccumulator` - 20 edges
8. `SensorSignalTranslator` - 20 edges
9. `SemanticConsistencyChecker` - 19 edges
10. `O2Normalizer` - 18 edges

## Surprising Connections (you probably didn't know these)
- `AnalyticsPreconditions` --uses--> `FuelSystemStatus`  [INFERRED]
  core/analytics_preconditions.py → schemas/vocabulary.py
- `AnalyticsPreconditions` --uses--> `TrimAnalyticsGate`  [INFERRED]
  core/analytics_preconditions.py → schemas/vocabulary.py
- `O2Normalizer` --uses--> `ObdLabDnaView`  [INFERRED]
  core/o2_normalizer.py → schemas/dna_view.py
- `O2Normalizer` --uses--> `FuelSystemStatus`  [INFERRED]
  core/o2_normalizer.py → schemas/vocabulary.py
- `Any` --uses--> `ObdLabDnaView`  [INFERRED]
  core/o2_normalizer.py → schemas/dna_view.py

## Import Cycles
- None detected.

## Communities (11 total, 3 thin omitted)

### Community 0 - "Code Community 0"
Cohesion: 0.16
Nodes (31): AirMeteringStrategy, Any, Any, ObdLabDnaView, RpmStateBucket, VE computation engine per OBDLab_KG_Wiki.md §10.  Implements the Speed-Density, Standard VE formula §10.1 — both MAF and MAP present., Emulate MAF from MAP+RPM+Displacement, then compute VE.          Emulated_MAF (+23 more)

### Community 1 - "Code Community 1"
Cohesion: 0.11
Nodes (22): Any, ObdLabDnaView, RpmStateBucket, ObdLabError, OBDLab custom exception hierarchy., Raised when a Physics Gate (§4) fails.      Source: OBDLab_KG_Wiki.md §4., Base exception for all OBDLab errors., SemanticConsistencyError (+14 more)

### Community 2 - "Code Community 2"
Cohesion: 0.10
Nodes (16): ObdLabDnaView, PIDIngestionValidator, PID ingestion validator per OBDLab_KG_Wiki.md §3.  Source: OBDLab_KG_Wiki.md §3., Validate and ferry per_cylinder_misfire_counts.          Must be a dict[int, int, Validate and map fuel_system_status/fuel_sys_status manual input to FuelSystemSt, Convert alternate-unit fields to canonical form per §3.2.          When both an, Validate each field against §3.1 bounds. Raise PIDValidationError on violation., DNA-relative RPM boundary per NewArchProposal §3.3.          HIGH:     strict — (+8 more)

### Community 3 - "Code Community 3"
Cohesion: 0.10
Nodes (19): BaseModel, ObdLabDnaView, AnalyticsPreconditions, Analytics precondition gate per OBDLab_KG_Wiki.md §9.  Evaluates the 8 precondit, Evaluate the 8 analytics-precondition gates per §9.      Returns the first gate, calculate_sensor_error_delta(), calculate_w_theo(), MAF linearity and theoretical airflow calculation helper.  Source: research/chun (+11 more)

### Community 4 - "Code Community 4"
Cohesion: 0.20
Nodes (20): Any, ObdLabDnaView, PIDValidationError, Raised when a PID violates physical_sensor_bounds.json (§3.1)., O2Normalizer, O2 sensor normalisation layer per OBDLab_KG_Wiki.md §11.  Routes on dna_view.ups, 3-zone narrowband voltage → lambda mapping per §11.1.          Reads pid_oxygen_, Direct wideband pass-through per §11.2.          Reads pid_wideband_equivalence_ (+12 more)

### Community 5 - "Code Community 5"
Cohesion: 0.19
Nodes (10): Any, Any, Evaluate preconditions and return TrimAnalyticsGate.          Args:, FuelSystemStatus, OBDLab canonical vocabulary — 7 StrEnums from OBDLab_KG_Wiki.md §6.  All values, Analytics precondition gate per OBDLab_KG_Wiki.md §6.5 / §9.      Source: OBDLab, Fuel system loop status mirror per DTC_VOCABULARY.md §8.      No cross-lab impor, Coerce raw wire-format string or enum to FuelSystemStatus enum. (+2 more)

### Community 6 - "Code Community 6"
Cohesion: 0.27
Nodes (11): Any, ObdLabDnaView, RpmStateBucket, compute_bucket(), _condition_matches(), _load_rules(), Engine state bucketing per OBDLab_KG_Wiki.md §8.2.  Loads obd_translation_rules., Determine engine state bucket from sanitized PIDs and optional DNA view.       P (+3 more)

### Community 7 - "Code Community 7"
Cohesion: 0.28
Nodes (7): Any, Trim vector aggregator per OBDLab_KG_Wiki.md §12.  Computes total_trim_correctio, Aggregate STFT + LTFT per bank into trim correction deltas.      Source: OBDLab_, Compute per-bank total_trim_correction_delta from sanitized PID dict.          A, Coerce value to float, raising PIDValidationError on None., _safe_float(), TrimVectorAggregator

## Knowledge Gaps
- **1 isolated node(s):** `Any`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PIDValidationError` connect `Code Community 4` to `Code Community 0`, `Code Community 1`, `Code Community 2`, `Code Community 3`, `Code Community 7`?**
  _High betweenness centrality (0.185) - this node is a cross-community bridge._
- **Why does `ObdLabDnaView` connect `Code Community 1` to `Code Community 0`, `Code Community 2`, `Code Community 3`, `Code Community 4`, `Code Community 6`?**
  _High betweenness centrality (0.161) - this node is a cross-community bridge._
- **Why does `SemanticConsistencyChecker` connect `Code Community 1` to `Code Community 0`, `Code Community 3`, `Code Community 4`, `Code Community 5`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Are the 29 inferred relationships involving `ObdLabDnaView` (e.g. with `AirMeteringStrategy` and `Any`) actually correct?**
  _`ObdLabDnaView` has 29 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `PIDValidationError` (e.g. with `Any` and `ObdLabDnaView`) actually correct?**
  _`PIDValidationError` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `RpmStateBucket` (e.g. with `AirMeteringStrategy` and `Any`) actually correct?**
  _`RpmStateBucket` has 22 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `VEEngine` (e.g. with `Any` and `ObdLabDnaView`) actually correct?**
  _`VEEngine` has 13 INFERRED edges - model-reasoned connections that need verification._