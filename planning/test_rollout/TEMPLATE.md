# Canonical Per-Lab Test Directory Template

This document defines the standard folder and file structure for each diagnostic lab's test suite under `labs/<lab>/tests/`. All labs (gaslab, obdlab, dtclab, comlab) must conform to this layout.

## Directory Tree

```
labs/<lab>/tests/
├── conftest.py             # Shared fixtures; builds the lab's typed input objects from a CSV row
├── fixtures/
│   ├── <lab>_cases.csv     # Master-derived CSV projection (columns consumed × decidable rows)
│   └── descriptor.py       # ModuleDescriptor: schema ranges + fault-box table + process() entry point
├── unit/
│   └── test_*.py           # Hand-crafted and property unit tests of lab internals (pre-existing tests)
├── generative/             # Imports the shared generative engine
│   ├── test_boundary.py        # Continuous labs only: tests boundaries of numeric fault boxes
│   ├── test_combinatorial.py   # All labs: combinatorial coverage of nominal/fault states
│   ├── test_noise.py           # Continuous labs only: simulates sensor noise resilience
│   ├── test_overlap.py         # Continuous labs only: checks handling of overlapping signature boxes
│   └── test_fuzz.py            # All labs: JSON boundary / input contract fuzzing
└── test_cases.py           # Parameterized integration tests over fixtures/<lab>_cases.csv
```

## File Responsibilities

### 1. `conftest.py`
Contains pytest fixtures shared across the lab's test suite. It is responsible for:
- Reading rows from `fixtures/<lab>_cases.csv`.
- Instantiating the lab's Pydantic models (e.g., input payload, DNA views) from a raw CSV dict row.
- Providing helper fixtures to mock or configure the shared test engine.

### 2. `fixtures/`
- **`<lab>_cases.csv`**: The local CSV containing test cases derived from `cases_petrol_master_v6.csv`. It contains only the columns consumed by this lab and only the rows that are decidable by this lab alone.
- **`descriptor.py`**: Declares the `ModuleDescriptor` subclass for the lab. This maps the input schemas, declares the nominal/fault state box boundaries, and wires the `process` entry point (e.g., `translate` for OBDLab, `sanitize` for DTCLab, `process` for GASLab/COMLab) to the test runner.

### 3. `unit/`
Holds standard pytest files containing unit tests of internal functions, math libraries, normalizers, and business logic. All pre-existing unit tests are moved here to keep the root clean.

### 4. `generative/`
Contains generative test modules that import the shared generative engine from `harness.harness`. Rather than copying engine files, these tests instantiate the shared engine generators using the lab's `ModuleDescriptor`.
- **`test_boundary.py`**, **`test_noise.py`**, **`test_overlap.py`** are only applicable to continuous signal domains (GASLab, OBDLab).
- **`test_combinatorial.py`**, **`test_fuzz.py`** are applicable to all labs (including discrete domains like DTCLab, COMLab).

### 5. `test_cases.py`
A parameterized test file that iterates over every test case in `fixtures/<lab>_cases.csv`. It runs the inputs through the lab's orchestrator and verifies that the output payload fields (e.g. verdicts, statuses) match the expected columns.

## Shared-Engine Import path
The shared generative engine is located in:
`harness/harness/`

Modules should import:
- `from harness.descriptor import ModuleDescriptor`
- `from harness.runner import run_generative_suite`
- Generators from `harness.generators.boundary`, `harness.generators.combinatorial`, etc.
