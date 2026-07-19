# EVAL-VLIVE-1 — Answer key + scoring rubric (GRADER ONLY)
**Do NOT paste this into a coder session.** Ground truth derived from the live
framed graph (`labs/**` frontmatter) on 2026-06-29 and cross-checked against code.
Re-derive with the commands shown if the tree has changed.

Total = 100 (+5 bonus). Score each model; compare side by side on the sheet in
`EVAL-VLIVE-1_RUN_PROTOCOL.md`.

---
## P1 — Blast radius (30 pts)
Source of truth: `labs/dtclab/docs/LLD_DTCLab.md` frontmatter (`consumers`,
`drift_guards`); verify symbols with
`grep -n DTCRoutingTag labs/comlab/comlab/core/fault_atlas_router.py`.

**(a) Downstream consumers — 4 live + 1 pending (16 pts):**
- `comlab fault_atlas_router.py` — `DTCRoutingTag` routing
- `comlab lab_pipeline_aggregator.py` — `DTCLabPayload` integration
- `comlab perception_contradiction.py` — `HistoricalFaultContext` / `FuelSystemStatus` comparison
- `comlab analytics/power_loss_analytics.py` — `DTC_CONFIDENCE_WEIGHTS` / `Mode06MonitorState` scoring
- **pending (flag, do not count as live):** `wired (pending T-WIRE-1)` →
  `apps/wired/wired/composition.py` `DTCLabPayload` mapping
- Score: 3 pts each live consumer (12); +4 if the pending wired edge is named **and
  flagged as not-yet-live**. −2 per invented/wrong consumer.

**(b) Guarding tests — DTCLab drift_guards (14 pts):** the 12 listed —
`test_dtc_ingestion_gate, test_freeze_frame_extractor, test_historical_context_classifier,
test_mode06_evaluator, test_routing_tag_mapper, test_classify_top3, test_rank_candidates,
test_family_map, test_payload, test_vocabulary, test_dna_view` (unit) +
`integration/test_dtclab_pipeline`.
- Full marks if `test_routing_tag_mapper.py` **and** `integration/test_dtclab_pipeline.py`
  are named (the two that most directly guard a routing-tag change) + ≥6 of the rest.
  Partial: 1 pt per correct test up to 14.

## P2 — Cross-lab trace (25 pts)
Source: `labs/dnalab/wiki/10_vehicle_dna_envelope.md` frontmatter; verify with
`grep -rn 'def from_vehicle_dna\|vehicle_dna_json\[.vin_dna.\]' labs/comlab/comlab`.

**Correct readers (2):**
- `comlab/core/horizon_context_injector.py` — `from_vehicle_dna(...)` (reads `VehicleDNA.vin_dna`)
- `comlab/projection.py` — `project()` reads `vehicle_dna_json['vin_dna']`

**The trap (−10 if named as a reader):** `lab_pipeline_aggregator.py` does **not**
read VehicleDNA (grep: zero hits). Naming it shows the agent guessed from the
"aggregator" name instead of checking — this is the exact mis-attribution T-VLIVE-4b
fixed. `lab_dna_views.py` / `ingestion.py:VehicleDNA` (schema mirror) are
acceptable *secondary* mentions, not the active readers.
- Score: 12 pts each correct reader (24); +1 for noting the schema mirror; −10 if
  the aggregator is asserted as a live reader.

## P3 — Test selection (20 pts)
Source: `labs/vinlab/docs/LLD_VINLab.md` frontmatter.

**(a) Tests (12):** primary `labs/vinlab/tests/unit/test_horizon.py`. Full VINLab
guard set also acceptable as "run the suite": `test_decoder, test_models,
test_horizon, test_stress_rpm, test_switches, test_cylinder_heuristic,
test_air_metering, test_contract_conformance, test_vindna_from_json`.
- 8 pts if `test_horizon.py` is named as the primary; +4 for naming the broader suite.

**(b) Downstream consumers to sanity-check (8):**
- `dnalab assembly.py build_vehicle_dna` (`vinlab.decode → VehicleDNA.vin_dna`)
- `comlab projection.py project()` (VehicleDNA → LabDnaView)
- `comlab fault_atlas_router.py` (`FuelSystemStatus.CL`, :294)
- 2–3 pts each; the horizon edit specifically flows to `horizon`/era logic, so
  `projection`/`fault_atlas_router` mentions are well-targeted.

## P4 — Governance (25 pts)
Source: `AGENTS.md` "The five rules" → **rule 4 (signal/noise)**.

A correct answer must say: **not shippable as-is.** "Future use is not a consumer."
A field/fault ships only with a **named consumer + code path** in COMLab analytics
or fault-atlas routing. If no live consumer exists, it ships as a **proposal** —
the field **and its new consumer together**, marked in the proposals register
(`comlab/config/proposals/`) — or it does not ship. The agent must **refuse to
invent a fake consumer**.
- 10 pts: "not shippable / future-use ≠ consumer"; 8 pts: names the
  named-consumer-or-paired-proposal requirement; 5 pts: cites rule 4 / `AGENTS.md`
  signal-noise; 2 pts: does not fabricate a consumer. −10 if it green-lights the
  orphan field.

## P5 — Applied (bonus, 5 pts, qualitative)
- File+function: `labs/dtclab/dtclab/core/routing_tag_mapper.py` — the tag-mapping
  function (`routing_tag_mapper`/`map_*`); raise a typed error on unknown tag.
- Test: `labs/dtclab/tests/unit/test_routing_tag_mapper.py`.
- Diff sketch present and plausible (typed exception, asserted by that test). Award
  up to 5 for a correct, minimal, non-applied sketch.

---
## Utilization signal (not scored — record per model)
For each probe, note in the comparison sheet **how** the model got the answer:
`vault_query` / read frontmatter / `.base` view  vs  raw `grep`/file-reading.
Heavier graph use that yields **faster + more complete + trap-avoiding** answers is
the evidence that the vault-live pack pays off. A model that brute-forces via grep
and still misses P2's trap or P1's pending edge is the contrast case.
