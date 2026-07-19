Both contract documents are in. Verification clean — every cross-reference resolves, 16 enums locked, scaffold still passes.
View the Semantic Contract
View the DNALab → COMLab flow spec
The short answer to "how do we keep DNALab → COMLab semantically unified."
The 4DLab ecosystem now has eight modules being built in parallel — VINLab, SymptomLab, DNALab, GasLab, OBDLab, DTCLab, COMLab, UI — possibly across different cowork accounts. The only way that scales is a binding contract that lives in one place, in one version, and that every module is tested against. That's what SEMANTIC_CONTRACT.md is.
Key rules locked by the contract.
Strict naming (the 2026-05-17 agreement, now codified). Three reserved names: VinDNA (Part A, owned by VINLab), SymptomDNA (Part B, owned by SymptomLab), VehicleDNA (combined, owned by DNALab). No other lab may produce these types; no synonyms allowed in code or docs.
One single source of truth per concern. §3 of the contract is a lookup table — when there's a question about a field name or enum value, you go to exactly one document. The OBD vocabulary wiki owns PID names. The DTC vocabulary wiki owns DTC structure. VehicleDNA.md owns the combined-payload shape. The contract reconciles where they overlap.
The four boundary schemas are JSON only. VinDNA, SymptomDNA, VehicleDNA, and the three lab payloads (GasLabPayload, OBDLivePayload, DTCLabPayload) are all defined as JSON shapes in §4. DNALab is the only lab allowed to import other labs (vinlab + symptomlab), and that's intentional — DNALab's whole purpose is composition. All other labs cross boundaries via JSON, period.
Vocabulary lock-down. §8 of the contract defines 16 sealed Python enums for every cross-lab field that takes one of a known set of values. Producers may only emit values from these enums; consumers must accept all values from these enums. Three larger enums (ChemicalSignature 28 values, DTCRoutingTag 16 values, FaultNode extracted from cases CSV) are also locked but expected to grow over normal release cadence — adding a value is a minor-version bump.
Drift reconciled. Section 6 documents three places where VehicleDNA.md and the OBDLab BP currently disagree on field names: induction_type vs air_metering_strategy, primary_load_calculation vs the same, upstream_o2_type vs upstream_o2_sensor_type. The contract specifies the canonical mapping table and requires VINLab to ship both field forms (with a cross-field consistency test in §9.3). COMLab reads the OBDLab-canonical form.
Three things missing from VehicleDNA.md today that the contract requires VINLab to add. euro_emission_category (needed so COMLab can derive Horizon), stress_idle_rpm_target (the new per-vehicle clinical RPM target from the 2026-05-16 user spec), model_year (needed for fault registry pruning). These are tracked as open actions in §11 of the contract.
Change protocol. Hard to change on purpose. Patches need one reviewer, minor changes (adding enum values or optional fields) need two, major changes (renames, removals) require an RFC and unanimous producer agreement.
What DNALab_TO_COMLab_FLOW.md adds.
The operational spec — exactly which JSON travels, exactly what COMLab does with each field, exactly how failures propagate back as actionable UI errors. Highlights:

The complete OrchestratorInboundRequest shape with every field labeled (§2).
The 8-step assembler pseudocode anyone driving the pipeline must follow (§9).
COMLab's two-stage processing walked through with field paths (§4 — stage A validation gates, stage B routing with polymorphic math driven by air_metering_strategy and upstream_o2_type).
A failure mode table mapping symptom at COMLab → likely upstream cause → what each side should fix (§6).
Operational checklists for DNALab.to_json_payload() (§7) and COMLab.lab_pipeline_aggregator (§8) so each side has a concrete green-light criterion.

Specific things to fix on the DNALab side.
The current VehicleDNA.md uses JSON keys like "PART A: VEHICLE PHYSICAL DNA (From VIN Module)". The contract requires snake_case keys: vin_dna and symptom_dna. DNALab's to_json_payload() should emit the snake_case form. The "PART A:" style is a document heading, not a JSON key.
Status check on what I changed.
The contract docs are pure documentation — they don't change the scaffold code. The scaffold still imports and pytest still reports 4 passes + 16 skips. Phase 0b (vocabulary.py from §8) is the next code task once you green-light the contract.