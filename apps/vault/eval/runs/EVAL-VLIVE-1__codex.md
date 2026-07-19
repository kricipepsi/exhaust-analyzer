# EVAL-VLIVE-1 — codex

Start: 2026-06-29T09:09:00Z
End: 2026-06-29T09:12:34Z

## P1 — Blast radius

### Answer

Downstream consumers of DTCLab output / routing tags:

1. `labs/comlab/comlab/schemas/ingestion.py::DTCLabPayload` — COMLab boundary model for DTCLab output; validates DTC lists and coerces/validates `routing_tags` as `DTCRoutingTag` enum values, rejecting invalid strings with `ERR-CONTRACT-002`.
2. `labs/comlab/comlab/core/lab_pipeline_aggregator.py::LabPipelineAggregator.process` — reads `request.dtc_lab_output.confirmed_dtcs` to derive `rich_dtc_present` for the compensated-rich detector, then passes the full `dtc_lab_output` through `_build_sanitized_payload()` for the router.
3. `labs/comlab/comlab/core/fault_atlas_router.py::_resolve_pid` / `FaultAtlasRouter.execute_triage_loop` / `_prune_candidates` — uses DTCLab output for freeze-frame PID fallbacks, DTC/MIL gate verification, routing-tag candidate pruning, POA/EGR synthetic routing-tag injection, incomplete-oxidation confidence caps, routing-tag discriminator score lift, and optional no-start branch evidence from `mode_06_monitors` + freeze-frame cut-state.
4. `labs/comlab/comlab/config/tag_discriminator.yaml` — config consumed by `FaultAtlasRouter.execute_triage_loop`; maps `dtc_lab_output.routing_tags` to bounded fault-family prior lifts.
5. `apps/wired/wired/composition.py` — **not live**. The DTCLab consumer is planned as `DTCLabPayload` mapping in Wired composition, but the path does not exist under `apps/wired/` in this checkout; only `apps/wired/WIRING_PREP.md` and the wired skill describe the pending mapping.

DTCLab tests guarding this area:

1. `labs/dtclab/tests/unit/test_routing_tag_mapper.py` — direct `RoutingTagMapper` fan-out, DNA gates, enum-order determinism, POA non-emission, unmapped DTC behavior, unknown-gate fail-open coverage gap, and comprehensive fan-out spot checks.
2. `labs/dtclab/tests/unit/test_vocabulary.py` — `DTCRoutingTag` enum drift guard.
3. `labs/dtclab/tests/unit/test_payload.py` — `DTCLabPayload.routing_tags` type enforcement and invalid-tag rejection.
4. `labs/dtclab/tests/unit/test_family_map.py` — `DTCRoutingTag` to canonical-family mapping and POA context-only behavior.
5. `labs/dtclab/tests/unit/test_rank_candidates.py` — Phase-2 ranking reads `DTCLabPayload.routing_tags` with DTC state / Mode 06 confidence weights.
6. `labs/dtclab/tests/unit/test_classify_top3.py` — Phase-2 top-3 emission from `routing_tags`.
7. `labs/dtclab/tests/integration/test_dtclab_pipeline.py` — end-to-end sanitizer output assertions for `routing_tags` and DNA suppression/emission.
8. `labs/dtclab/tests/generative/test_combinatorial.py` — exemplar DTC per `DTCRoutingTag`, DNA gate axis, cross-field tag cases.
9. `labs/dtclab/tests/regression/test_dtclab_regression.py` — fixture-level exact `expected_routing_tags` equality.

### Source/Method

- `read /agent_workspace/labs/dtclab/docs/LLD_DTCLab.md:22-41` and `read /agent_workspace/labs/dtclab/docs/DLD_DTCLab.md:22-40` for framed consumers / drift guards.
- `grep "dtc_lab_output|DTCLabPayload|routing_tags|confirmed_dtcs|mode_06_monitors|historical_fault_context|freeze_frame|mil_flashing" paths=[/agent_workspace/labs/comlab/comlab,/agent_workspace/apps/wired]` for live COMLab/Wired readers.
- `read /agent_workspace/labs/comlab/comlab/schemas/ingestion.py:288-307,488-505` for `DTCLabPayload` and `OrchestratorInboundRequest.dtc_lab_output`.
- `read /agent_workspace/labs/comlab/comlab/core/lab_pipeline_aggregator.py:418-441,588-615` for `confirmed_dtcs` compensated-rich and payload handoff.
- `read /agent_workspace/labs/comlab/comlab/core/fault_atlas_router.py:489-561,825-987,993-1125,1414-1448` for freeze-frame PID resolution, tag pruning/injection, DTC gate/scoring, discriminator, and no-start branch.
- `read /agent_workspace/labs/comlab/comlab/config/tag_discriminator.yaml` via grep hits at lines 7-24 for routing-tag discriminator purpose.
- `read /agent_workspace/apps/wired` showed no `wired/` package or `composition.py`; grep hits in `apps/wired/WIRING_PREP.md:22-31` and `_wired_skills/wired-composition-contract/SKILL.md:55-89` identify this as pending.
- `grep "DTCRoutingTag|routing_tags|RoutingTagMapper|routing_tag_map|family_map|classify_top3|rank_candidates" paths=/agent_workspace/labs/dtclab/tests` for the test list.

## P2 — Cross-lab trace

### Answer

COMLab places that actually read DNALab's `VehicleDNA` envelope:

1. `labs/comlab/comlab/projection.py::project(vehicle_dna_json, target=...)` — reads `vehicle_dna_json["vin_dna"]`, then projects fields into `GasLabDnaView`, `ObdLabDnaView`, or `DtcLabDnaView`; `project_all()` calls `project()` for all three targets.
2. `labs/comlab/comlab/core/horizon_context_injector.py::HorizonContextInjector.from_vehicle_dna(vehicle_dna)` — reads `vehicle_dna.vin_dna.resolved_horizon`, `cylinder_count`, and `number_of_banks`, then loads the matching threshold mask.

### Source/Method

- `grep "VehicleDNA" paths=[/agent_workspace/labs/comlab,/agent_workspace/labs/dnalab]` found the COMLab code readers and the DNALab frontmatter consumers.
- `read /agent_workspace/labs/comlab/comlab/projection.py:42-126` for `project()` and `project_all()` reads of `vehicle_dna_json["vin_dna"]`.
- `read /agent_workspace/labs/comlab/comlab/core/horizon_context_injector.py:41-99` for `from_vehicle_dna()` field reads.
- `ast_grep pat="$X: VehicleDNA" paths=[/agent_workspace/labs/comlab/**/*.py]` and `ast_grep pat="VehicleDNA($$$ARGS)" paths=[/agent_workspace/labs/comlab/**/*.py]` returned no additional COMLab call/annotation readers beyond the imports/read sites found by grep/read.

## P3 — Test selection

### Answer

Tests to run after editing `labs/vinlab/vinlab/overlay/horizon.py`:

1. `labs/vinlab/tests/unit/test_horizon.py` — direct unit tests for `euro_to_horizon()` and `_year_to_horizon()`.
2. `labs/vinlab/tests/unit/test_decoder.py` — decoder imports `euro_to_horizon()` and emits `resolved_horizon` into `VinDNA`; the test file also asserts year-to-horizon cases.
3. `labs/vinlab/tests/unit/test_models.py` — `VinDNA.resolved_horizon` defaults / JSON emission / derived horizon behavior.
4. `labs/vinlab/tests/unit/test_vindna_from_json.py` — legacy payloads without `resolved_horizon` derive it from `euro_emission_category`, invalid horizon rejects.
5. `labs/vinlab/tests/unit/test_contract_conformance.py` — `resolved_horizon` remains part of the VinDNA contract field set.
6. `labs/vinlab/tests/unit/test_decode_isolation.py` — decode isolation fixture asserts `resolved_horizon == HORIZON_ADAPTIVE`.

Downstream sanity-checks in other labs:

1. DNALab: `labs/dnalab/dnalab/assembly.py::build_vehicle_dna` and `labs/dnalab/dnalab/models.py::VehicleDNA.new` / `to_json_payload` / `from_json_payload` — make sure the VINLab `resolved_horizon` survives DNALab envelope assembly and round-trip.
2. COMLab: `labs/comlab/comlab/projection.py::project` / `project_all` — make sure `VehicleDNA.vin_dna.resolved_horizon` still projects into Gas/OBD/DTC DNA views.
3. COMLab: `labs/comlab/comlab/core/horizon_context_injector.py::from_vehicle_dna` — make sure horizon masks are selected from `vehicle_dna.vin_dna.resolved_horizon`.
4. COMLab: `labs/comlab/comlab/core/fault_atlas_router.py::_prune_candidates` / `execute_triage_loop` — sanity-check horizon pruning of registry rows and downstream execution metadata.
5. DTCLab: `labs/dtclab/dtclab/schemas/dna_view.py::DtcLabDnaView.resolved_horizon` — sanity-check mirror compatibility; current grep found only schema carriage, not live DTCLab branching on horizon.

### Source/Method

- `read /agent_workspace/labs/vinlab/vinlab/overlay/horizon.py:10-37` for edited functions.
- `grep "euro_to_horizon|_year_to_horizon|resolved_horizon|HORIZON_LEGACY|HORIZON_ADAPTIVE|HORIZON_MODERN" paths=/agent_workspace/labs/vinlab/tests` for test selection.
- `grep "euro_to_horizon|_year_to_horizon|resolved_horizon" paths=/agent_workspace/labs/vinlab/vinlab/decoder.py` showed decoder imports/calls at lines 33 and 646-669.
- `read /agent_workspace/labs/vinlab/tests/unit/test_horizon.py:1-46` for direct horizon unit coverage.
- `read /agent_workspace/labs/vinlab/docs/DLD_VINLab.md:16-30` for framed cross-lab consumers and drift guards.
- `read /agent_workspace/labs/dnalab/dnalab/assembly.py:14-48` and `read /agent_workspace/labs/dnalab/dnalab/models.py:21-108` for DNALab envelope carriage.
- `grep "resolved_horizon|Horizon|horizon" paths=[/agent_workspace/labs/comlab,/agent_workspace/labs/dtclab/dtclab,/agent_workspace/labs/gaslab/gaslab,/agent_workspace/labs/obdlab/obdlab,/agent_workspace/labs/dnalab]` for downstream readers; GasLab/OBDLab code returned no direct matches, DTCLab code only carried the field in `schemas/dna_view.py`.

## P4 — Governance

### Answer

No. `cold_start_enrichment_pct` on the GASLab→COMLab payload is not shippable as "future use".

It must ship with one of:

1. a named existing live COMLab consumer in analytics or fault-atlas routing, identified as an exact `file.py::function` code path, plus the schema mirror and tests for that reader; or
2. a same-change proposal under `labs/comlab/comlab/config/proposals/` that names the target consumer and ships the consumer in the same change.

Because it is a new optional payload field, the semantic contract change protocol also requires a minor-version change process: updated test suite plus two reviewers, including the COMLab owner and at least one producer-lab owner.

### Source/Method

- `read /agent_workspace/labs/comlab/docs/COMLab_HLD.md:380-384` — every field must be bound to a named consumer; signal/noise strikes fields without one.
- `read /agent_workspace/labs/comlab/docs/COMLab_HLD.md:705-708` — "Future use" is not a consumer; field and consumer land together.
- `read /agent_workspace/labs/comlab/_comlab_skills/comlab-code-review/SKILL.md:50-58` — blank/vague/future-use consumers and unread contracted fields are blocking; no-consumer additions need a same-change proposal.
- `read /agent_workspace/labs/comlab/_comlab_skills/comlab-python/SKILL.md:62-65` — new field/enum/fault ships only with named existing consumer or proposal; "Future use" is never a consumer.
- `read /agent_workspace/labs/comlab/comlab/config/proposals/README.md:9-35,54-77` — proposal fields and lifecycle require a named code consumer.
- `read /agent_workspace/labs/comlab/docs/Vocabulary/SEMANTIC_CONTRACT.md:596-604` — new optional field is a minor contract change with updated tests and two reviewers.

## P5 — Applied sketch only

### Answer

The silent-pass path I found is an unknown `dna_gate`, not an unknown enum `tag`: unknown `entry["tag"]` already fails in `_load_map()` via `DTCRoutingTag(entry["tag"])`. To replace the silent pass with a typed error:

- File + function to change: `labs/dtclab/dtclab/core/routing_tag_mapper.py::RoutingTagMapper._check_high_confidence_gate`.
- Add typed error in same file: `UnknownDnaGateError(ValueError)`.
- Single test file: `labs/dtclab/tests/unit/test_routing_tag_mapper.py`; replace `test_unknown_gate_fail_open` with a `pytest.raises(UnknownDnaGateError, match="unknown_dna_gate")` assertion.

Sketch diff, not applied:

```diff
--- a/labs/dtclab/dtclab/core/routing_tag_mapper.py
+++ b/labs/dtclab/dtclab/core/routing_tag_mapper.py
@@
 logger = logging.getLogger(__name__)
+
+
+class UnknownDnaGateError(ValueError):
+    """Raised when routing_tag_map.yaml names an unsupported dna_gate."""
@@
-        # Unknown gate — defensive: emit (fail open).
-        logger.warning("unknown_dna_gate: gate=%s", gate_name)
-        return True
+        raise UnknownDnaGateError(f"unknown_dna_gate: {gate_name}")
```

```diff
--- a/labs/dtclab/tests/unit/test_routing_tag_mapper.py
+++ b/labs/dtclab/tests/unit/test_routing_tag_mapper.py
@@
-from dtclab.core.routing_tag_mapper import RoutingTagMapper
+from dtclab.core.routing_tag_mapper import RoutingTagMapper, UnknownDnaGateError
@@
-def test_unknown_gate_fail_open(tmp_path, caplog):
-    """An unknown dna_gate name triggers the fail-open branch.
-...
-    assert caplog.records[0].levelname == "WARNING"
+def test_unknown_gate_raises_typed_error(tmp_path):
+    """An unknown dna_gate name rejects the routing map instead of fail-opening."""
+    map_path = tmp_path / "routing_tag_map.yaml"
+    map_path.write_text(_bogus_gate_yaml(), encoding="utf-8")
+    mapper = RoutingTagMapper(map_path, dna_view=_dna_view(confidence=VinConfidence.HIGH))
+
+    with pytest.raises(UnknownDnaGateError, match="unknown_dna_gate: not_a_real_gate"):
+        mapper.map(["P0420"])
```

### Source/Method

- `read /agent_workspace/labs/dtclab/dtclab/core/routing_tag_mapper.py:78-87,93-135` for `_load_map()` enum conversion and unknown-gate fail-open behavior.
- `read /agent_workspace/labs/dtclab/tests/unit/test_routing_tag_mapper.py:224-260` for existing unknown-gate coverage.
- `read /agent_workspace/labs/dtclab/dtclab/schemas/vocabulary.py` via grep/read for `DTCRoutingTag` enum source; `_load_map()` already calls `DTCRoutingTag(entry["tag"])`.
