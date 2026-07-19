# Architecture Decision Records — COMLab

**Status:** Living index (individual records are immutable once Accepted)
**Format:** Nygard template, per `_skills/doc/ADR.md`
**Date:** 2026-06-21
**Code baseline:** COMLab v2 as-built (`labs/comlab/comlab/`)

This directory records the standing architectural decisions that shape COMLab —
the prune→rank fusion spine at the terminal end of 4DLab. Records are numbered
sequentially and, once **Accepted**, are not edited: a later decision supersedes
an earlier one with a new record. Each captures *why*, not *how* — the *how*
lives in `COMLab_HLD.md` / `COMLab_LLD.md` / `COMLab_DLD.md`.

This directory was authored when COMLab's coding tasks completed; several records
formalise decisions that were previously carried only as "open questions for
sign-off" in the v1.0 design drafts and have since been settled in code.

| # | Decision | Status |
|---|----------|--------|
| [ADR-0001](ADR-0001_comlab_is_the_read_only_fusion_spine.md) | COMLab is the read-only prune→rank fusion spine | Accepted |
| [ADR-0002](ADR-0002_no_cross_lab_python_imports.md) | No cross-lab Python imports — mirror types over JSON | Accepted |
| [ADR-0003](ADR-0003_signal_noise_every_field_has_a_named_consumer.md) | Signal/noise — every schema field needs a named, existing consumer | Accepted |
| [ADR-0004](ADR-0004_scope_petrol_1990_2010_euro_1_5.md) | Scope is petrol 1990–2010 (Euro 1–5); Euro 6+ perks out of scope | Accepted |
| [ADR-0005](ADR-0005_dnalab_resolves_horizon_comlab_never_parses_vin.md) | DNALab pre-resolves the horizon; COMLab never parses the VIN | Accepted |
| [ADR-0006](ADR-0006_separate_rule_registry_from_fault_atlas_kg.md) | Separate the rule registry from the Fault-Atlas KG | Accepted |
| [ADR-0007](ADR-0007_brettschneider_chemistry_is_ground_truth.md) | Brettschneider chemistry is ground truth; detect ECU perception contradiction | Accepted |
| [ADR-0008](ADR-0008_emitters_emit_channels_fusion_is_comlab_last.md) | Emitter labs emit channels, not verdicts; fault fusion is COMLab, built last | Accepted |
| [ADR-0009](ADR-0009_two_point_delta_math_lives_in_comlab.md) | Two-operating-point Δ math lives in COMLab; additive with a single-point fallback | Accepted |
| [ADR-0010](ADR-0010_deterministic_five_phase_triage.md) | Deterministic 5-phase triage with a confidence floor and a catalyst-damage override | Accepted |
| [ADR-0011](ADR-0011_surface_routing_directive_and_echo_audit.md) | Surface the routing directive and input-echo audit in the outbound contract | Accepted |

## Maintenance

New decisions append as **ADR-0012+** with status **Proposed**, then **Accepted**
after review. To change an accepted decision, write a new record that
**supersedes** the old one (set the old record's status to *Superseded by
ADR-####*) — never edit an accepted record in place.
