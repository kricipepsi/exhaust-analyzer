# T-TST-7 — Derive dtclab_cases.csv from the reconciled master

**Status:** `authored` · ready for coder · **Blocked by:** `T-MASTER-RECON` (done), `T-TST-3` (done) ·
**Pack:** `planning/test_rollout/` · **Mode:** STRICT
**Load skills (session start):** read `TEST_ROLLOUT_START_HERE.md`; sandbox Python 3.14; mandatory pair +
`_skills/codingskills/ecc-subset/python-testing`.

## Goal

Project the reconciled `cases_petrol_master_v6.csv` into `labs/dtclab/tests/fixtures/dtclab_cases.csv`:
**DTC-consumed columns × DTC-decidable rows**, per `PROJECTION_CONTRACT.md` (DTCLab section), *as corrected
below to the master's real column names*. This is the data fixture the DTCLab generative harness (`T-TST-9`)
will consume; it is the DTCLab twin of `obdlab_cases.csv` (T-TST-6).

This is a **pure projection** — stdlib `csv`, no DTCLab code invoked. The `dtcs` values are carried through as
**raw strings**; the projection does **not** exercise `DTC_REGEX`. So the open DTCLab hex-regex gap (the
"T-FX-13" item — see the contract note below) gates `T-TST-9`, **not** this task. T-TST-7 is runnable now.

## Files

- **Create:** `labs/dtclab/tests/scripts/project_dtclab_cases.py` (the projection script).
- **Create:** `labs/dtclab/tests/fixtures/dtclab_cases.csv` (the output fixture).
- **Read-only inputs:** the reconciled master `TestSuite/cases_petrol_master_v6.csv` (post `T-MASTER-RECON`)
  + `PROJECTION_CONTRACT.md` DTCLab rules.

## Scope — columns pinned to the REAL master (disk-verified 2026-06-10)

`PROJECTION_CONTRACT.md`'s DTCLab list names columns the master does **not** carry. Use these actual columns;
do **not** invent the contract's missing ones.

**Consumed input columns (exist in master → project byte-for-byte):**

| Master column | Carried as | Named live DTCLab consumer (code path) |
|---|---|---|
| `dtcs` | `dtcs` (raw string; 1 code, or comma-separated) | `dtclab/core/dtc_ingestion_gate.py::validate_dtc_list` → `dtclab/core/routing_tag_mapper.py::RoutingTagMapper.map(confirmed_dtcs)` |
| `ff_dtcs` | `ff_dtcs` | `dtclab/core/freeze_frame_extractor.py::extract_freeze_frame` (Mode $02 snapshot) |
| `ff_ect` | `ff_ect` | `freeze_frame_extractor.py::evaluate_coolant_dtc_context` (+ `_derive_iat_ect_bias`) |
| `ff_rpm` | `ff_rpm` | `freeze_frame_extractor.py::_derive_load_high_low_rpm` |
| `ff_load` | `ff_load` | `freeze_frame_extractor.py::_derive_load_high_low_rpm` |
| `ff_map` | `ff_map` | `freeze_frame_extractor.py::extract_freeze_frame` (context PID) |
| `ff_stft_b1` | `ff_stft_b1` | `freeze_frame_extractor.py::extract_freeze_frame` (context PID) |
| `ff_ltft_b1` | `ff_ltft_b1` | `freeze_frame_extractor.py::extract_freeze_frame` (context PID) |
| `fuel_status` | `fuel_status` | `freeze_frame_extractor.py::_derive_open_loop` |

**Consumed expected-output columns (NOT in master → emit empty, `gt_method=characterization`):**
`expected_routing_tags` (consumer: `RoutingTagMapper.map`), `expected_historical_context`
(consumer: `dtclab/core/historical_context_classifier.py::classify_historical_context`),
`expected_freeze_frame_status` (consumer: `freeze_frame_extractor.py::extract_freeze_frame`).
Same pattern as T-TST-6: master carries no DTCLab ground truth, so these are the regression net populated by
`T-TST-9`'s first characterization run — but each column already has a named live reader, so it ships.

**Columns the contract names but the master LACKS — do NOT fabricate** (log as follow-up, do not ship a guessed
column): `dtcs_mode_03` / `dtcs_mode_07` / `dtcs_mode_0a` (master has a single `dtcs`), `mode_06_monitor_results`,
`codes_cleared`, `active_mil`, `mil_flashing`. The DTCLab payload defines `active_mil`/`mil_flashing`/`mode_06`,
but there is **no master source** to project them from — leaving them out is correct (signal/noise: no source,
no column).

## Row predicate (use the reconciled column directly — do NOT re-derive)

Project rows where `lab_decidability` **contains `"DTC"`**. On the reconciled master this is the
`GASLab|OBD|DTC` set = **194 rows** (disk-verified). Of these, 115 have a non-empty `dtcs`; 1 has a non-empty
`ff_dtcs`. Empty-`dtcs` rows are kept (they are the no-DTC / NO_FAULT control rows the harness needs).

## Parsing rule (pin so the coder doesn't guess)

`dtcs` / `ff_dtcs` cells: split on comma, `.strip()` each token, drop empties. Single-code cells (e.g. `P0172`)
yield a one-element list. Carry the **raw cell string** into the CSV unchanged (the harness, not this fixture,
parses it) — this keeps the projection byte-consistent with the master and avoids touching `DTC_REGEX`.

## Success criteria

1. Exactly the 194 DTC-decidable rows projected (none dropped, none added), selected via the reconciled
   `lab_decidability` column — not a re-derivation.
2. The 9 input columns above are **byte-consistent** with the master (projection, not re-authoring).
3. The 3 expected-output columns are present, empty, and every row's `gt_source` carries
   `gt_method=characterization` with a per-column `:characterization` annotation (mirror T-TST-6's `build_gt_source`).
4. The CSV loads via `csv.DictReader` and `labs/dtclab/tests/test_cases.py` collects over it without error.
5. Script is self-contained (stdlib only), touches no `dtclab/` code, schema, or `PROJECTION_CONTRACT.md`.

## Out of scope

The relabel (`T-MASTER-RECON`). The DTCLab descriptor/generators/harness and any characterization values
(`T-TST-9`). The DTCLab hex-regex gap. Any `dtclab/` code change. Updating `PROJECTION_CONTRACT.md` (follow-up only).

## Signal/noise consumer

`dtclab_cases.csv` is consumed by **`T-TST-9`** (the DTCLab generative harness — combinatorial + fuzz over the
projected DTC inputs) and immediately by `labs/dtclab/tests/test_cases.py` (collection). Every projected column
has a named live reader in `dtclab/core/*` (table above) or in those two consumers. A column with no consumer
does not ship.

## Unplanned follow-ups to log (not in this diff)

| ID | Finding |
|---|---|
| FU-TST7-1 | `PROJECTION_CONTRACT.md` DTCLab consumed-input list (`dtcs_mode_03/07/0a`, `mode_06_monitor_results`, `codes_cleared`, `active_mil`, `mil_flashing`) does not match the master's real columns (`dtcs`, `ff_*`, `ff_dtcs`, `fuel_status`). Contract should be reconciled to disk — same class of drift as FU-TST6-1. |
| FU-TST7-2 | DTCLab payload fields `active_mil` / `mil_flashing` / `mode_06_monitors` have no master source column; they will be populated by `T-TST-9`'s characterization run, not projected here. |

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-TST-7.md`, opening with the confirmed `## Plan`.)
