# EVAL-VLIVE-1 Run Report — agy
**Start Time:** 2026-06-29 09:04 UTC  
**End Time:** 2026-06-29 09:45 UTC  
**Duration:** ~41 minutes  

---

## P1 — Blast radius

### (a) Downstream Consumers
1. **`labs/comlab/comlab/core/fault_atlas_router.py`**
   - **Status:** Live
   - **Role/Behavior:** Consumes `DTCRoutingTag` via `dtc_lab_output.routing_tags` to prune rule candidates from the global fault registry (e.g. `row.routing_tag in routing_tags`). It also applies a routing-tag discriminator (additive score lift). In addition, it injects synthetic routing tags (`POA_HISTORY` and `EGR_HISTORY`) dynamically based on the parsed chemical state, runs the no-start triage branch (`MONITOR_ABORTED` state and `ff_fuel_spark_cut_at_crank` flag), resolves freeze-frame parameters from `dtc_lab_output.freeze_frame` to match PIDs, and checks confirmed DTCs/MIL in operator checks.
2. **`labs/comlab/comlab/core/lab_pipeline_aggregator.py`**
   - **Status:** Live
   - **Role/Behavior:** Extracts `confirmed_dtcs` from `request.dtc_lab_output` to check if rich DTC codes (P0172/P0175) are present. It passes the resulting `rich_dtc_present` boolean flag to the compensated-rich detector `detect_compensated_rich`. It also packages and serializes the complete `dtc_lab_output` payload into the orchestrator request/response via `.model_dump()`.
3. **`labs/comlab/comlab/core/perception_contradiction.py`**
   - **Status:** **Not Live (Documentation-only / phantom mapping)**
   - **Role/Behavior:** Listed in the LLD frontmatter as consuming `HistoricalFaultContext / FuelSystemStatus comparison`. However, checking the source code reveals it does not actually reference these types or compare them. (It only receives the pre-calculated `rich_dtc_present` boolean from `lab_pipeline_aggregator.py` to gate compensated-rich detection).
4. **`labs/comlab/comlab/analytics/power_loss_analytics.py`**
   - **Status:** **Not Live (Documentation-only / phantom mapping)**
   - **Role/Behavior:** Listed in the LLD frontmatter as consuming `DTC_CONFIDENCE_WEIGHTS / Mode06MonitorState scoring`. However, checking the source code reveals it contains no references to DTCs, confidence weights, or Mode 06 monitors.
5. **`apps/wired/wired/composition.py`**
   - **Status:** **Not Live (Pending T-WIRE-1)**
   - **Role/Behavior:** Listed in frontmatter as consuming `DTCLabPayload mapping`. However, it is not yet live as `T-WIRE-1` is pending, and the package structure/file does not exist in the codebase.

**Source/Method:** 
- Frontmatter of `labs/dtclab/docs/LLD_DTCLab.md` (`consumers` block) and `labs/dtclab/docs/DLD_DTCLab.md`.
- Validated via workspace-wide AST search: `/agent_workspace/.venv-wired/bin/python _skills/graph/4dlab-vault/scripts/vault_query.py --vault Vault consumers` and `grep -rn 'dtc_lab_output\|DTCLabPayload\|DTCRoutingTag' labs/comlab/comlab/core/`.

---

### (b) Guarding Tests
The primary test files guarding a routing-tag change are:
- `labs/dtclab/tests/unit/test_routing_tag_mapper.py` (directly asserts DTC-to-tag mappings, DNA-gate configurations, and fallbacks).
- `labs/dtclab/tests/integration/test_dtclab_pipeline.py` (verifies full pipeline compilation and tag resolution).

The full list of DTCLab `drift_guards` mapping to this area is:
- `labs/dtclab/tests/unit/test_dtc_ingestion_gate.py`
- `labs/dtclab/tests/unit/test_freeze_frame_extractor.py`
- `labs/dtclab/tests/unit/test_historical_context_classifier.py`
- `labs/dtclab/tests/unit/test_mode06_evaluator.py`
- `labs/dtclab/tests/unit/test_classify_top3.py`
- `labs/dtclab/tests/unit/test_rank_candidates.py`
- `labs/dtclab/tests/unit/test_family_map.py`
- `labs/dtclab/tests/unit/test_payload.py`
- `labs/dtclab/tests/unit/test_vocabulary.py`
- `labs/dtclab/tests/unit/test_dna_view.py`
- `labs/dtclab/tests/generative/test_combinatorial.py`
- `labs/dtclab/tests/generative/test_fuzz.py`
- `labs/dtclab/tests/regression/test_dtclab_regression.py`

**Source/Method:**
- Frontmatter of `labs/dtclab/docs/LLD_DTCLab.md` (`drift_guards` block).
- Validated via directory listing: `glob` on `labs/dtclab/tests/**/*.py`.

---

## P2 — Cross-lab trace

DNALab's `VehicleDNA` envelope is actively read by the following downstream components:

1. **`labs/comlab/comlab/core/horizon_context_injector.py`**
   - **Function:** `HorizonContextInjector.from_vehicle_dna(self, vehicle_dna: VehicleDNA) -> HorizonContext`
   - **Reads:** Reads `vehicle_dna.vin_dna` to construct the `HorizonContext` object (retrieving `resolved_horizon`, `cylinder_count`, and `number_of_banks`).
2. **`labs/comlab/comlab/projection.py`**
   - **Function:** `project(vehicle_dna_json: VehicleDnaJson, *, target: Literal["gas", "obd", "dtc"]) -> GasLabDnaView | ObdLabDnaView | DtcLabDnaView`
   - **Reads:** Reads keys directly from `vehicle_dna_json["vin_dna"]` (e.g. `engine_displacement_liters`, `cylinder_count`, `number_of_banks`, `euro_emission_category`, `fuel_delivery_type`, `induction_type`, `upstream_o2_type`, `has_catalyst`, `egr_equipped`, `target_lambda_v112`, `co_low_idle`, `co_high_idle`, `confidence`, `resolved_horizon`, `rated_rpm`, `stress_idle_rpm_target`, `air_metering_strategy`, `make`, `model_year`, `egr_equipped`).

### Trap Warning
- `labs/comlab/comlab/core/lab_pipeline_aggregator.py` **does not read** `VehicleDNA` (zero hits on grep for `VehicleDNA` or `vehicle_dna` inside this file). It only accesses the pre-resolved `resolved_horizon` and flat metadata fields from `request.metadata` (which is a `SessionMetadata` Pydantic model). 
- `comlab/schemas/ingestion.py` defines the Pydantic schema `VehicleDNA` mirroring the DNALab payload structure, and `comlab/schemas/lab_dna_views.py` describes the projected view schemas, but they are schema definitions rather than active logical readers.

**Source/Method:**
- `labs/dnalab/wiki/10_vehicle_dna_envelope.md` frontmatter (`consumers` block).
- Validated with: `grep -rn 'def from_vehicle_dna\|vehicle_dna_json\[.vin_dna.\]' labs/comlab/comlab`.

---

## P3 — Test selection

### (a) Unit test(s) to run in vinlab
- **Primary test file:** `labs/vinlab/tests/unit/test_horizon.py` (specifically test assertions for `euro_to_horizon` and `_year_to_horizon`).
- **Broader unit test suite:**
  - `labs/vinlab/tests/unit/test_decoder.py`
  - `labs/vinlab/tests/unit/test_models.py`
  - `labs/vinlab/tests/unit/test_stress_rpm.py`
  - `labs/vinlab/tests/unit/test_switches.py`
  - `labs/vinlab/tests/unit/test_cylinder_heuristic.py`
  - `labs/vinlab/tests/unit/test_air_metering.py`
  - `labs/vinlab/tests/unit/test_contract_conformance.py`
  - `labs/vinlab/tests/unit/test_vindna_from_json.py`
  - `labs/vinlab/tests/unit/test_vindna_roundtrip.py`

### (b) Downstream consumers in other labs to sanity-check
1. **DNALab:** `labs/dnalab/dnalab/assembly.py` inside function `build_vehicle_dna` (verifies that `vinlab.decode` correctly yields the `vin_dna` part containing `resolved_horizon`).
   - *Tests to run:* `labs/dnalab/tests/unit/test_assembly.py` and `labs/dnalab/tests/unit/test_assembly_integration.py`.
2. **COMLab:** `labs/comlab/comlab/projection.py` inside function `project()` (verifies that the `VehicleDNA` payload correctly maps to `LabDnaView`).
   - *Tests to run:* `labs/comlab/tests/unit/test_projection.py`.
3. **COMLab:** `labs/comlab/comlab/core/fault_atlas_router.py` (verifies `FuelSystemStatus.CL` gating at line 294, and other horizon-dependent routing).
4. **COMLab:** `labs/comlab/comlab/core/horizon_context_injector.py` (verifies that `resolved_horizon` maps to the correct sensitivity threshold mask).
   - *Tests to run:* `labs/comlab/tests/unit/test_horizon_context_injector.py`.

**Source/Method:**
- `labs/vinlab/docs/LLD_VINLab.md` frontmatter (`consumers` and `drift_guards` blocks).
- Validated via `grep -rn 'euro_to_horizon' labs/vinlab/` to see that `decoder.py` imports and relies on it.

---

## P4 — Governance

- **Verdict:** **Not shippable as-is.** "Future use" is not a consumer.
- **Requirement:** Under this repository's governance, every field in a contract payload must have a **named, live consumer + code path** in COMLab analytics or fault-atlas routing. If no live consumer exists, the field and its consumer must ship together as a **proposal** inside the proposals registry (e.g. `comlab/config/proposals/` / `entries.yaml`), accompanied by its task spec. Fake/stub consumers must not be fabricated just to bypass the gate.
- **Rule Citation:** **Rule 4 (Signal/noise governs every field — and v2 progresses forward)** of the repository's five rules defined in `/agent_workspace/AGENTS.md`.

**Source/Method:**
- `/agent_workspace/AGENTS.md` (section: "The five rules (in priority order)", Rule 4).
- Checked against `labs/obdlab/docs/ADR_OBDLab.md` ("Signal/noise rule is non-negotiable") and `labs/comlab/docs/COMLab_HLD.md` §5.4.

---

## P5 — Applied

To make `RoutingTagMapper` reject an unknown tag with a typed error (e.g., a custom `UnknownRoutingTagError` subclassing `ValueError`):

- **File + Function to change:** `labs/dtclab/dtclab/core/routing_tag_mapper.py` inside `RoutingTagMapper._load_map` (where YAML tag strings are cast to the `DTCRoutingTag` enum).
- **Single test file to assert the new behavior:** `labs/dtclab/tests/unit/test_routing_tag_mapper.py`

### Sketch of the Diff

**In `labs/dtclab/dtclab/core/routing_tag_mapper.py`:**
```python
class UnknownRoutingTagError(ValueError):
    """Raised when an unknown routing tag is found in the mapping configuration."""
    pass

# Modify _load_map function to validate and raise the typed error:
    def _load_map(self, map_path: Path) -> list[_RoutingRule]:
        with open(map_path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        rules: list[_RoutingRule] = []
        for entry in data["entries"]:
            patterns = tuple(re.compile(p) for p in entry["patterns"])
            try:
                tag = DTCRoutingTag(entry["tag"])
            except ValueError as e:
                raise UnknownRoutingTagError(
                    f"Unknown routing tag {entry['tag']!r} in mapping configuration."
                ) from e
            gate = entry.get("dna_gate")
            rules.append(_RoutingRule(patterns, tag, gate))
        return rules
```

**In `labs/dtclab/tests/unit/test_routing_tag_mapper.py`:**
```python
from dtclab.core.routing_tag_mapper import UnknownRoutingTagError

def test_load_map_with_unknown_tag_raises_typed_error(tmp_path):
    bad_yaml = tmp_path / "bad_map.yaml"
    bad_yaml.write_text("entries:\n  - patterns: [^P0000$]\n    tag: INVALID_TAG_NAME", encoding="utf-8")
    with pytest.raises(UnknownRoutingTagError, match="Unknown routing tag 'INVALID_TAG_NAME'"):
        RoutingTagMapper(bad_yaml, dna_view=None)
```
