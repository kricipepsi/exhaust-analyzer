1. Separate GASLab‑Only Test Fixtures from Integration Data
Create a dedicated GASLab test subset, containing only the fields that GASLab actually sees and the expected chemical_state + sample_validity. All other columns belong to other modules and must be stripped away.

2. Build a Proper Test Harness with Pytest
Do not run tests ad‑hoc. Use pytest with parameterized fixtures. Your test harness should:

Load the clean GASLab test cases.

For each row, construct GasReading, GasLabContext, and GasLabDnaView.

Call gaslab.process.process().

Assert that the returned GasLabPayload.chemical_state and sample_validity match the expected values.

3. Use the Ontology as the Single Source of Truth for Synthetic Tests
Do not rely only on the CSV. Generate synthetic test cases directly from gas_lab_ontology.yaml. This ensures every fault signature and every boundary point is covered.

Implementation:

Write a script tools/generate_boundary_grid.py that reads the YAML and outputs a Parquet/CSV with min, max, and mid‑point samples for each gas in each fault.

Also generate invalid samples (triangle sum <14, >18, or CO+CO₂ <6).

Include DNA‑gated variants (same gas pattern but with has_catalyst=True/False etc.).

This synthetic grid becomes your primary test fixture. The CSV from real vehicles can be used as a secondary sanity check, not the main test oracle.

4. Isolate Module Tests from Integration Tests
Your current CSV mixes GASLab‑only expectations with expectations that require OBD or DTC data (e.g., expected_perception_gap column, dtcs column). Those belong to COMLab integration tests, not GASLab unit tests.

5. What to Do with the Existing CSV
Do not delete it – it is valuable for integration testing.

Extract the GASLab‑only rows by filtering to cases where the expected fault is purely chemical (e.g., RICH_MIXTURE, LEAN_MISFIRE, EXHAUST_AIR_LEAK) and where no cross‑lab contradiction is expected (expected_perception_gap = False).

Manually audit a handful of rows to ensure the expected state is reachable with only gas + context + DNA (no OBD/DTC). Remove rows that rely on obd_lambda mismatch or DTC presence to change the verdict.

gaslab/
├── tests/
│   ├── conftest.py                  # shared fixtures
│   ├── test_validity_gates.py
│   ├── test_brettschneider.py
│   ├── test_rule_engine.py
│   ├── test_dna_gates.py
│   ├── test_pure_gas_cases.py       # uses gaslab_test_cases.csv
│   ├── test_synthetic_grid.py       # generates from ontology
│   └── fixtures/
│       ├── gaslab_test_cases.csv    # extracted, cleaned
│       ├── synthetic_grid.parquet   # generated
│       └── ontology.yaml            # link to data/
└── tools/
    ├── extract_gaslab_cases.py      # script to filter CSV
    └── generate_boundary_grid.py    # from ontology
	
	7. Immediate Next Steps
Stop using the CSV as a direct test input for GASLab.

Write the extraction script to produce gaslab_test_cases.csv.

Implement the pytest harness with parameterized tests.

Run the extraction and verify that the first 10–20 rows work.

Generate the synthetic boundary grid from your ontology – this will give you >95% coverage (KR1) and replace most of the CSV’s role.

Reserve the full CSV for COMLab integration tests (where OBD, DTC, and fuel trim data are available).

By isolating GASLab’s test domain, you will eliminate false failures caused by missing OBD data and gain a reliable, fast, and maintainable test suite. The CSV is a good real‑world sanity dataset, but only after you strip away everything that GASLab does not consume.


To go beyond static fixtures, you can generate synthetic data dynamically. This is particularly useful for testing boundaries and simulating sensor noise.

Combinatorial & Boundary Testing: Your test harness could programmatically generate thousands of random points within, near, and outside the 32 fault boxes. For a fault defined with CO: min=1.5, max=3.0, your generator would create points at 1.49, 1.5, 1.51, 2.99, 3.0, and 3.01 to test every edge.

Fault Injection & Noise Simulation: You can create robust test functions that take a "clean" signature for a fault (e.g., IGNITION_MISFIRE) and programmatically add Gaussian noise to each gas value or shift a single gas (like O₂) across its entire plausible range. This validates the system's resilience against non-ideal, real-world readings.

