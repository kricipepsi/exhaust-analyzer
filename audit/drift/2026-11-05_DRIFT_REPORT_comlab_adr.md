# COMLab ADR drift report (EGM, docs vs code), 2026-11-05

## labs/comlab/docs/adr/README.md

No drift detected.

## labs/comlab/docs/adr/ADR-0001_comlab_is_the_read_only_fusion_spine.md

- [DIVERGENCE] The ADR says COMLab injects exactly one synthetic tag (POA_HISTORY), but the router also injects EGR_HISTORY when chemical_state is EGR_DILUTION_MISFIRE. Doc: `labs/comlab/docs/adr/ADR-0001_comlab_is_the_read_only_fusion_spine.md:30` "COMLab adds exactly one synthetic signal of its own". Code: `labs/comlab/comlab/core/fault_atlas_router.py:969` "routing_tags.append(egr)".

## labs/comlab/docs/adr/ADR-0002_no_cross_lab_python_imports.md

No drift detected.

## labs/comlab/docs/adr/ADR-0003_signal_noise_every_field_has_a_named_consumer.md

No drift detected.

## labs/comlab/docs/adr/ADR-0004_scope_petrol_1990_2010_euro_1_5.md

- [MODEL] The ADR says Euro 6+ is out of scope and absent from every schema, but EuroEmissionCategory declares EURO_6 and EURO_7 members. Doc: `labs/comlab/docs/adr/ADR-0004_scope_petrol_1990_2010_euro_1_5.md:16` "of scope** and absent from every schema, registry rule, and KG node.". Code: `labs/comlab/comlab/schemas/vocabulary.py:104` "EURO_6".

## labs/comlab/docs/adr/ADR-0005_dnalab_resolves_horizon_comlab_never_parses_vin.md

- [DIVERGENCE] The ADR says the injector loads the era-sensitivity threshold mask, but for HORIZON_MODERN it uses the empty default mask and loads none. Doc: `labs/comlab/docs/adr/ADR-0005_dnalab_resolves_horizon_comlab_never_parses_vin.md:14` "and loads the era-sensitivity threshold mask". Code: `labs/comlab/comlab/core/horizon_context_injector.py:86` "threshold_mask = self._default_mask".

## labs/comlab/docs/adr/ADR-0006_separate_rule_registry_from_fault_atlas_kg.md

No drift detected.

## labs/comlab/docs/adr/ADR-0007_brettschneider_chemistry_is_ground_truth.md

No drift detected.

## labs/comlab/docs/adr/ADR-0008_emitters_emit_channels_fusion_is_comlab_last.md

No drift detected.

## labs/comlab/docs/adr/ADR-0009_two_point_delta_math_lives_in_comlab.md

- [UNDOCUMENTED] The ADR names enable_delta as the only gate, but the router has a second flag, enable_delta_v2, that gates the delta re-rank on the v2 scored_rules path. Doc: `labs/comlab/docs/adr/ADR-0009_two_point_delta_math_lives_in_comlab.md:28` "gated by `enable_delta` and the optional payload field.". Code: `labs/comlab/comlab/core/fault_atlas_router.py:587` "enable_delta_v2: bool = False".

## labs/comlab/docs/adr/ADR-0010_deterministic_five_phase_triage.md

No drift detected.

## labs/comlab/docs/adr/ADR-0011_surface_routing_directive_and_echo_audit.md

No drift detected.
