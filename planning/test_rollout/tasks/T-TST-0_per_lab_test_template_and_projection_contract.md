# T-TST-0 — Canonical per-lab test template + master→per-lab projection contract

**Status:** completed · **Blocked by:** — · **Pack:** `planning/test_rollout/`

## Goal

Establish the single template every lab's `tests/` follows, the contract for
deriving each lab's CSV from `cases_petrol_master_v6.csv`, and the import contract
for the shared generator engine. This is the foundation T-TST-1..10 build on.
No lab code changes; this task produces the template + contract docs and one
reference skeleton, nothing else.

## Success criteria

1. A template doc `planning/test_rollout/TEMPLATE.md` defining the exact
   `labs/<lab>/tests/` tree (below) and what each file/dir holds.
2. A projection contract `planning/test_rollout/PROJECTION_CONTRACT.md`
   that, **per lab (gas/obd/dtc/com)**, enumerates: (a) the master columns that
   lab consumes (inputs + expected-output columns), and (b) the predicate that
   selects the rows that lab can decide **alone** (no cross-lab contradiction).
3. The shared-engine import path is named and stable (currently
   `harness/harness/` — `ModuleDescriptor`, `runner`, `generators/*`).
   The contract states: labs **import** the engine; they do **not** copy it.
4. The generator-applicability matrix (this pack's ledger) is reflected in the
   template as per-lab "which `generative/test_*.py` files exist."

## Canonical template (the tree T-TST-1..5 lay down)

```
labs/<lab>/tests/
├── conftest.py             # shared fixtures; builds the lab's typed input objects from a CSV row
├── fixtures/
│   ├── <lab>_cases.csv     # master-derived projection (T-TST-6/7; data blocked on T-MASTER-RECON)
│   └── descriptor.py       # ModuleDescriptor: schema ranges + fault-box table + process() entry point
├── unit/
│   └── test_*.py           # hand + property unit tests of lab internals (existing tests move here)
├── generative/             # imports the SHARED engine; one file per applicable generator
│   ├── test_boundary.py        # continuous labs only
│   ├── test_combinatorial.py   # all labs
│   ├── test_noise.py           # continuous labs only
│   ├── test_overlap.py         # continuous labs only
│   └── test_fuzz.py            # all labs (JSON-boundary / contract fuzz)
└── test_cases.py           # parametrized over fixtures/<lab>_cases.csv
```

## Projection contract — required content

- **Per-lab consumed columns:** derive from each lab's `schemas/` (input contract)
  + the master's expected-output columns that lab is responsible for. GASLab's set
  is the worked example; obd/dtc/com enumerated from their `schemas/` on disk.
- **Per-lab decidable-row predicate:** the filter that keeps only rows the lab can
  resolve without another lab (e.g. GASLab: purely-chemical fault + no
  perception-gap; see `TestProp.md` §5). State each lab's predicate explicitly.
- **COMLab exception:** COMLab consumes the **full** master (it is the fusion gate),
  so its "projection" is the identity / wired e2e — note this, do not invent a COM
  subset.
- **Data dependency:** the contract (which columns/rows) is authorable **now** from
  the schemas; the actual extracted CSVs (T-TST-6/7) are blocked on `T-MASTER-RECON`
  (master has provably-stale labels, H-10 — `expected_top_fault` matches 0/277).

## Signal/noise consumer

The named consumer of this template is each lab's **forked generative suite**
(`labs/<lab>/tests/generative/`), which runs the descriptor against the shared
engine. No field/column enters a `<lab>_cases.csv` unless the projection contract
names the lab code path that reads it.

## Files to touch

- create `planning/test_rollout/TEMPLATE.md`
- create `planning/test_rollout/PROJECTION_CONTRACT.md`
- (reference only, no edit) `labs/*/schemas/`, `TestProp.md`, `harness/harness/`

## Out of scope

No lab `tests/` edits (that is T-TST-1..5). No CSV extraction (T-TST-6/7). No
engine relocation or harness path-drift cleanup (separate, harness pack).

## Verification

Template tree and projection contract reviewed against each lab's `schemas/` on
disk: every consumed column the contract lists must exist in that lab's input
schema or the master header. Engine import path resolves to a real module.
