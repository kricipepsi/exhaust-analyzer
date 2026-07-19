# Extracted proposals — index

**Date:** 2026-06-07  ·  **Sources:** (1) `proposals/{AddObdFields,DataFlow,OBD_ImplProp,wikiResearch}.md`; (2) the `sources/` research tree; (3) the `sources/various/` volume sweep (Vol1–8) — rows tagged 🆕 below.

**What this is.** Each row is one discrete enhancement, chunked to its own `.md`. Consumers are *proposed*, not yet wired — every file names a candidate consumer + code path; none verified as a live reader. Architect specs, not code.

**Total proposals:** 70  (🆕 17 added from the volume sweep)

> Not the live registry. When a consumer is pinned, a proposal graduates to `comlab/config/proposals/`.

> Volume-sweep note: some referenced numeric thresholds were image-stripped in the Vol exports; affected files say so and point to `formula-wiki/PENDING_STRIPPED_FORMULAS.md`. No bound was fabricated.


## OBDLab — new input fields

| ID | Proposal | Target | Type |
|---|---|---|---|
| [EP-OBD-IN-01](EP-OBD-IN-01_calculated-load-pid.md) | Add Calculated Engine Load PID (0x04) as an OBDLab input field | OBDLab (input) → COMLab (consumer) | input_field |
| [EP-OBD-IN-02](EP-OBD-IN-02_absolute-load-pid.md) | Add Absolute Load Value PID (0x43) as an OBDLab input field | OBDLab (input) → COMLab (consumer) | input_field |
| [EP-OBD-IN-03](EP-OBD-IN-03_fuel-system-status-pid.md) | Add Fuel System Status PID (0x03 / FUELSYS) as an OBDLab input field | OBDLab (input) → COMLab (Stage A gate) | input_field |
| [EP-OBD-IN-04](EP-OBD-IN-04_control-module-voltage-pid.md) | Add Control Module Voltage PID (0x42 / VPWR) as an OBDLab input field | OBDLab (input) → COMLab (perception_contradiction) | input_field |
| [EP-OBD-IN-05](EP-OBD-IN-05_throttle-position-pids.md) | Add Absolute/Relative Throttle Position PIDs (0x11 / 0x45 — TP / TP_R) | OBDLab (input) → COMLab (fault_atlas idle-leak validator) | input_field |
| [EP-OBD-IN-06](EP-OBD-IN-06_baro-pid.md) | Add Barometric Pressure PID (0x33 / BARO) as an OBDLab input field | OBDLab (input) → COMLab (ambient-pressure calibration) | input_field |
| [EP-OBD-IN-07](EP-OBD-IN-07_per-cylinder-misfire-counts.md) | Add per-cylinder misfire counts (Mode 06 / 200- & 1000-rev) as input fields | OBDLab (input) → COMLab (fault_atlas misfire localiser) | input_field |
| [EP-OBD-IN-08](EP-OBD-IN-08_iat-field.md) | Add Intake Air Temperature (IAT) as an OBDLab input field | OBDLab (input) → OBDLab VE engine + COMLab ECU checker | input_field |
| [EP-OBD-IN-09](EP-OBD-IN-09_gdi-rail-pressure-pids.md) 🆕 | Add GDI high-pressure fuel PIDs (FRP desired/actual, VCV duty) as input fields | OBDLab (input) → COMLab fault_atlas (GDI fuel branch) | input_field |
| [EP-OBD-IN-10](EP-OBD-IN-10_secondary-ignition-waveform.md) 🆕 | Add secondary-ignition waveform feature set (firing/burn line, coil ripples) | OBDLab (manual-entry features) → COMLab fault_atlas ignition | input_field |

## OBDLab — analytics & config

| ID | Proposal | Target | Type |
|---|---|---|---|
| [EP-OBD-10](EP-OBD-10_ve-engine-classifier.md) | VE engine math + validity classifier (FAULT_VE_IDLE_COLLAPSE / SENSOR_SKEW) | OBDLab (core/ve_engine.py) | analytics_module |
| [EP-OBD-11](EP-OBD-11_theoretical-airflow-crosscheck.md) | Speed-density theoretical-airflow MAF/MAP sanity cross-check | OBDLab (core) → COMLab | analytics_module |
| [EP-OBD-12](EP-OBD-12_ltft-cell-matrix.md) | LTFT adaptive cell-matrix mapping (RPM × Load → idle / cruise / WOT cells) | OBDLab (KG) → COMLab load-cell analyzer | analytics_module |
| [EP-OBD-13](EP-OBD-13_bank-asymmetry-audit.md) | Asymmetric bank trim audit (Total B1 vs Total B2 ≥ 20 % divergence) | OBDLab (core/trim_vector_aggregator.py) → COMLab | analytics_module |
| [EP-OBD-14](EP-OBD-14_semantic-consistency-gates.md) | Semantic-consistency physics gates (blown ground trace, trim saturation) | OBDLab (core/semantic_consistency_checker.py) | analytics_module |
| [EP-OBD-15](EP-OBD-15_physical-sensor-bounds-config.md) | Broad physical-sensor-bounds config to survive ECU-fault float values | OBDLab (config/physical_sensor_bounds.json) | config |
| [EP-OBD-16](EP-OBD-16_state-translation-rules.md) | State-translation rules (STABILIZED_IDLE / STRESS_IDLE / COLD_OPEN_LOOP_INVALID) | OBDLab (config/obd_translation_rules.yaml) | config |
| [EP-OBD-17](EP-OBD-17_wideband-offset-failure-mode.md) | WIDEBAND_OFFSET two-stage O₂ failure-mode expression | OBDLab (o2_normalizer.py) → COMLab fusion | enum_value + fault_node |
| [EP-OBD-18](EP-OBD-18_maf-map-tps-rationality.md) 🆕 | MAF/MAP/TPS rationality gate + inferred-BARO calibration check (P0068) | OBDLab (rationality gate) → COMLab fault_atlas | analytics_module |
| [EP-OBD-19](EP-OBD-19_map-cranking-mechanical-test.md) 🆕 | MAP cranking mechanical test (electronic vacuum / relative compression) | OBDLab (mechanical-health module) | analytics_module |

## COMLab — fusion, deltas & gates

| ID | Proposal | Target | Type |
|---|---|---|---|
| [EP-COM-01](EP-COM-01_idle-transition-delta-engine.md) | Idle-transition delta engine (low-idle vs stress-idle Δ across PIDs) | COMLab (analytics/idle_transition_evaluator.py / delta_engine.py) | analytics_module |
| [EP-COM-02](EP-COM-02_dual-frame-stateframe.md) | Dual-frame StateFrame / multi-frame OrchestratorInboundRequest (low + high idle) | COMLab schemas + wired/composition.py | schema + architecture |
| [EP-COM-03](EP-COM-03_lambda-cross-delta-engine.md) | Lambda cross-delta divergence engine (λ_chem vs λ_obd, Δδ) | COMLab (perception_contradiction) | analytics_module |
| [EP-COM-04](EP-COM-04_ecu-hardware-fault-checker.md) | ECU-hardware-fault checker (the named consumer for all internal-ECU fault nodes) | COMLab/OBDLab (new checker) | analytics_module |
| [EP-COM-05](EP-COM-05_semantic-coherence-paradigm.md) | Semantic-coherence vs digital-divergence classification paradigm | COMLab (perception_contradiction / fault_atlas routing policy) | architecture |
| [EP-COM-06](EP-COM-06_traditional-fault-signature-matrix.md) | Traditional-fault PID signature matrix (10 external fault families × PIDs) | COMLab (fault_atlas_router discriminator table) | reference_table + routing |
| [EP-COM-07](EP-COM-07_misfire-vs-fuelling-gate.md) | Misfire-vs-fuelling pre-route gate | COMLab (fault_atlas candidate-pruning) | routing_gate |
| [EP-COM-08](EP-COM-08_prerequisite-dtc-gate.md) | Prerequisite-DTC gate (suppress trim routing under active sensor DTCs) | COMLab (analytics_preconditions) | routing_gate |
| [EP-COM-09](EP-COM-09_ltft-cell-vector-analyzer.md) | LTFT cell-vector analyzer (idle-only / part-throttle-only / global localisation) | COMLab (analytics) | analytics_module |
| [EP-COM-10](EP-COM-10_l5-prognostic-scoring.md) 🆕 | L5 prognostic scoring layer (perception-trust / ECU-consistency / thermal-confidence) | COMLab (L5 decision-fusion) | analytics_module + schema |
| [EP-COM-11](EP-COM-11_tcg-root-source-attribution.md) 🆕 | Temporal Causal Graph (TCG) root-source attribution layer | COMLab (L4 pattern matching) | analytics_module + schema |
| [EP-COM-12](EP-COM-12_load-correction-delta.md) 🆕 | Load-correction delta (MAF-reported load vs gas-calculated load) | COMLab (analytics) | analytics_module |
| [EP-COM-13](EP-COM-13_startup-highload-gates.md) 🆕 | T15 startup + 70% high-load enrichment gates (TrimAnalyticsGate additions) | COMLab (analytics_preconditions) | routing_gate |
| [EP-COM-14](EP-COM-14_no-dtc-pid-profiling.md) 🆕 | No-DTC live-PID profiling mode (two-state baseline diagnosis) | COMLab (diagnosis mode) | analytics_module |
| [EP-COM-15](EP-COM-15_truth-perception-test-corpus.md) 🆕 | 30-case truth-vs-perception test corpus (validation asset) | COMLab (test/validation) + fault_atlas pattern set | test_corpus |

## Internal-ECU hardware fault nodes

| ID | Proposal | Target | Type |
|---|---|---|---|
| [EP-ECU-01](EP-ECU-01_capacitor-leakage.md) | ECU fault node — liquid-electrolyte capacitor leakage / board corrosion | fault-atlas (new node) → COMLab ECU checker | fault_node |
| [EP-ECU-02](EP-ECU-02_injector-driver-fault.md) | ECU fault node — low-side injector-driver failed open / shorted (bank-specific) | fault-atlas (new node) → COMLab ECU checker | fault_node |
| [EP-ECU-03](EP-ECU-03_coil-driver-failure.md) | ECU fault node — high-power ignition-coil driver (IGBT) shorted | fault-atlas (new node) → COMLab ECU checker | fault_node |
| [EP-ECU-04](EP-ECU-04_sensor-ground-trace-blown.md) | ECU fault node — vaporized internal sensor ground trace | fault-atlas (new node) → COMLab ECU checker | fault_node |
| [EP-ECU-05](EP-ECU-05_5v-regulator-collapse.md) | ECU fault node — internal 5 V regulator rail collapse | fault-atlas (new node) → COMLab ECU checker | fault_node |
| [EP-ECU-06](EP-ECU-06_adc-mux-failure.md) | ECU fault node — analog-to-digital converter (ADC) multiplexer / channel failure | fault-atlas (new node) → COMLab ECU checker | fault_node |
| [EP-ECU-07](EP-ECU-07_eprom-bitflip.md) | ECU fault node — EPROM/flash memory cell corruption (localized bit-flip) | fault-atlas (new node) → COMLab ECU checker | fault_node |

## Traditional fault-atlas additions

| ID | Proposal | Target | Type |
|---|---|---|---|
| [EP-FA-01](EP-FA-01_maf-ground-open-failsafe.md) | Fault node — MAF circuit ground-open failsafe (speed-density limp) | fault-atlas (sensor_fault family) → COMLab | fault_node |
| [EP-FA-02](EP-FA-02_thermostat-closedloop-delay.md) | Fault node — thermostat stuck open → delayed closed-loop entry | fault-atlas + analytics_preconditions | fault_node |
| [EP-FA-03](EP-FA-03_injector-thermal-intermittent.md) | Fault node — thermally intermittent injector (cold-only single-bank lean) | fault-atlas (air-fuel metering) | fault_node |
| [EP-FA-04](EP-FA-04_fuel-water-contamination.md) | Fault node — fuel water/contamination (random multi-misfire + positive trim) | fault-atlas (air-fuel metering / misfire) | fault_node |
| [EP-FA-05](EP-FA-05_alternator-ac-ripple.md) | Fault node — alternator AC ripple corrupting sensor references | fault-atlas (charging system) → COMLab | fault_node |
| [EP-FA-06](EP-FA-06_egr-insufficient-flow.md) | Fault node — EGR insufficient flow (commanded-EGR vs observed-trim response) | fault-atlas (EGR / auxiliary emissions) | fault_node |
| [EP-FA-07](EP-FA-07_fuel-restriction-split.md) | Fault refinement — split fuel-delivery restriction (clogged filter vs weak pump) | fault-atlas (refines ERR-LC-003) | fault_refinement |
| [EP-FA-08](EP-FA-08_evap-purge-flow-leak-detection.md) 🆕 | EVAP purge-flow verification + leak-detection logic | fault-atlas (EVAP / auxiliary emissions) → COMLab | fault_node + analytics_module |

## GASLab

| ID | Proposal | Target | Type |
|---|---|---|---|
| [EP-GAS-01](EP-GAS-01_5gas-brettschneider-schema.md) | GASLab 5-gas physical schema + Brettschneider λ for digital-vs-physical divergence | GASLab (schema + chem) → COMLab fusion | schema + analytics_module |
| [EP-GAS-02](EP-GAS-02_misfire-chemistry-resolver.md) | GASLab misfire chemistry resolver (high HC + high O₂ → COMBUSTION_FAIL) | GASLab (chemical ontology) | analytics_module |
| [EP-GAS-03](EP-GAS-03_combustion-integrity-metrics.md) 🆕 | Combustion-integrity + oxygen-usage chemical metrics | GASLab (chemical resolver) → COMLab | analytics_module + schema |
| [EP-GAS-04](EP-GAS-04_two-speed-gas-transition-matrix.md) 🆕 | Two-speed gas transition matrix as a GASLab capability (Δgas low→2500 RPM) | GASLab (per-state frame) → COMLab delta engine | analytics_module + reference_table |
| [EP-GAS-05](EP-GAS-05_5gas-sample-validity-gate.md) 🆕 | 5-gas sample-validity gate (vsum + dilution) | GASLab (ingestion gate) | analytics_module |

## Catalyst

| ID | Proposal | Target | Type |
|---|---|---|---|
| [EP-CAT-01](EP-CAT-01_osc-damping-monitor.md) | Catalyst OSC damping-ratio monitor (post-cat/pre-cat switching ratio) | catalyst (new chunks/catalyst) → COMLab | analytics_module |
| [EP-CAT-02](EP-CAT-02_cat-masking-detection.md) | Catalyst masking detection (Catalyst_Masking_Rich / _Lean) | catalyst + GASLab → COMLab | fault_node |
| [EP-CAT-03](EP-CAT-03_false-p0420-cluster.md) | false_P0420 cluster (demote catalyst-failure when feed-gas is clean) | catalyst → COMLab | routing_gate + fault_node |
| [EP-CAT-04](EP-CAT-04_catalyst-field-tests.md) | Catalyst field-test inputs (backpressure, IR Δ-temp, Mode 06 monitor) | catalyst (input fields) → COMLab | input_field |
| [EP-CAT-05](EP-CAT-05_pre-cat-inference-engine.md) 🆕 | Pre-cat inference engine (model feed-gas from inlet/outlet temp differential) | catalyst + COMLab (L5) | analytics_module |

## DTCLab

| ID | Proposal | Target | Type |
|---|---|---|---|
| [EP-DTC-01](EP-DTC-01_dtc-causal-hierarchy.md) | DTCLab causal hierarchy / companion-code sub-graph | DTCLab (ontology) → COMLab | analytics_module |
| [EP-DTC-02](EP-DTC-02_j2012-fault-taxonomy.md) | SAE J2012 / ISO 15031-6 eight-family fault taxonomy backbone | DTCLab + fault-atlas | reference_taxonomy |
| [EP-DTC-03](EP-DTC-03_dtc-enable-window-gate.md) | DTC enable-criteria / run-condition window gate | DTCLab → COMLab analytics_preconditions | routing_gate |
| [EP-DTC-04](EP-DTC-04_mode06-freezeframe-nostart.md) 🆕 | Mode-06 / Freeze-Frame no-start method + immobilizer/security branch | DTCLab (FF/Mode06 parser) → COMLab fault_atlas (no-start) | analytics_module |

## DNALab

| ID | Proposal | Target | Type |
|---|---|---|---|
| [EP-DNA-01](EP-DNA-01_dynamic-graph-pruning.md) | Dynamic per-lab graph pruning by VehicleDNA (speed-density vs MAF subgraph) | DNALab → OBDLab/GASLab/DTCLab graph selection | architecture |
| [EP-DNA-02](EP-DNA-02_slim-dna-views.md) | Per-lab slim DNA views (e.g. ObdLabDnaView) for sensor topology context | DNALab → translation labs | schema |
| [EP-DNA-03](EP-DNA-03_euro-era-tier-gate.md) 🆕 | Euro-era emissions-tier gate + make/era fault priors | DNALab (tier resolution) → COMLab fault_atlas | analytics_module + schema |

## Architecture

| ID | Proposal | Target | Type |
|---|---|---|---|
| [EP-ARCH-01](EP-ARCH-01_downstream-fusion-isolation.md) | Downstream centralized fusion model + lab isolation contract | architecture (COMLab as central broker) | architecture |
| [EP-ARCH-02](EP-ARCH-02_per-lab-knowledge-graph.md) | Per-lab local knowledge graph + ontology (semantic translation layer) | architecture (GAS/OBD/DTC each) | architecture |
| [EP-ARCH-03](EP-ARCH-03_obd-i-to-ii-trim-conversion.md) | OBD-I ↔ OBD-II fuel-trim scale conversion (PID encoding) | OBDLab / pids-protocol | reference_formula |
