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
│       ├── synthetic_grid.          # generated
│       └── ontology.yaml            # link to data/
└── tools/
    ├── extract_gaslab_cases.py      # script to filter CSV
    └── generate_boundary_grid.py    # from ontology