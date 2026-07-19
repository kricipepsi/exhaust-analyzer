# T-V7-2 — Build `cases_petrol_v7.csv` (inputs) from the viable shortlist

**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `deferred` (→ `pending` when T-V7-1 is `done`) · **Blocked by:** T-V7-1
**Mode:** STRICT — adds the CSV + a loader under `apps/wired/v7/`; **no `wired/`/lab/COMLab source edits**. · **Scope owner:** wired-v7.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Objective
Build the v7 test table — **inputs only** — from the `viable` cases T-V7-1 selected,
to the exact column spec T-V7-1 pinned, every value shaped to the **current**
`diagnose()` contract and every row citing its library source. The oracle columns are
left empty for T-V7-3.

## Signal/noise
Adds no domain field or fault. The **named consumer** is the driver T-V7-4 (maps rows
→ `diagnose()`) and the oracle T-V7-3 (fills `expected_*`). A row without a
`source_ref` does not ship; a case missing an essential input is **not** invented —
it stays on the Owner action queue (signal/noise).

## Pinned facts (verified at authoring)
- Column spec + viable shortlist + incomplete list come from
  `apps/wired/v7_tasks/reports/V7_1_RESEARCH_<date>.md` (T-V7-1).
- Input shape = the current fixture schema
  (`apps/wired/tests/fixtures/oil_cases/MW-002.json` + the `obd`/`dtc` optional blocks
  in `apps/wired/tests/test_tracing.py::_obd_inputs`). Do **not** add fields the live
  labs do not read.
- Loader pattern reference: `wired.run_case.load_case`.

## Scope
**IN:**
- Create `apps/wired/v7/data/` and write `cases_petrol_v7.csv` with **exactly** the
  T-V7-1 columns: input columns (mapped to the current contract) + the empty oracle
  columns + bookkeeping (`case_id`, `category`, `source_ref`, `tag`).
- One row per `viable` case, values transcribed from the library facts and mapped to
  the contract (units/field names per the current fixture). Each row carries its
  `category` and a `source_ref` (e.g. `cases_library_v2.html#<section>` or
  `cases_petrol_era_v1.csv:row<N>`).
- Add the **negative/edge/invalid** rows T-V7-1 enumerated (malformed input,
  missing-bank, conflicting signals), tagged so the oracle/scorer treat them as
  HANDLED/abort, not a diagnosis.
- Leave every `expected_*` column **empty** (T-V7-3 fills them) — inputs and oracle
  stay separated so they cannot cross-contaminate.
- Write `apps/wired/v7/load_corpus.py`: load + schema-validate the CSV; expose an
  iterator of `(case_id, raw_inputs, category, source_ref, tag)`; a `--validate` mode
  asserting every row parses, maps to a valid `diagnose()` input, and has a
  `source_ref`. No `diagnose()` call here.
- Any case that turns out to still miss an essential input at transcription time →
  **do not fabricate**: drop it from the CSV and (re)record it in the ledger Owner
  action queue with the missing field; note it in the progress note.

**OUT:** writing any `expected_*`/oracle value (→ T-V7-3); inventing sensor values for
incomplete cases; reading `ARCHIVE/` or the legacy v6 CSV; copying raw library files
into the repo; editing `wired/`/labs/COMLab; running `diagnose()`; `graphify`; `Vault/`.

## Steps
1. Read the T-V7-1 report; take the column spec + viable shortlist + negatives.
2. Create `apps/wired/v7/data/cases_petrol_v7.csv`; transcribe rows with
   `category`/`source_ref`/`tag`; add negatives; leave `expected_*` empty.
3. Write `load_corpus.py`; run `--validate` (all rows parse + map to a valid input +
   have a `source_ref`).
4. Move any still-incomplete case to the Owner action queue (no fabrication).
5. Fill `v7_tasks/progress_notes/T-V7-2.md` gates; STOP. Prompt the owner if the queue
   gained rows.

## Success criteria
- `cases_petrol_v7.csv` has one row per viable case + the negative/edge rows; every
  row maps to a valid current-contract `diagnose()` input and carries a `source_ref`;
  zero rows sourced from `ARCHIVE/`.
- `expected_*` columns are present but empty (oracle is T-V7-3).
- `load_corpus.py --validate` passes (all rows parse + valid input + `source_ref`).
- No fabricated inputs; every dropped/incomplete case is on the Owner action queue.
- `py_compile`/`ruff`/`pyright` clean on `load_corpus.py`; `git status` shows only new
  files under `apps/wired/v7/` + `apps/wired/v7_tasks/`.

## VERIFICATION GATE — T-V7-2
Complete in `v7_tasks/progress_notes/T-V7-2.md`: `--validate` output; row count vs the
T-V7-1 viable list (+ negatives); the dropped/incomplete list; inner-loop results.

## CODE REVIEW — T-V7-2
Complete in `v7_tasks/progress_notes/T-V7-2.md`: no `ARCHIVE/`/legacy-CSV read; every
row cites a library `source_ref`; no `expected_*` filled; no fabricated inputs; no
source edits; `graphify` not run.

## Commit (owner, explicit paths)
```bash
cd /agent_workspace
git add \
  apps/wired/v7/data/cases_petrol_v7.csv \
  apps/wired/v7/load_corpus.py \
  apps/wired/v7_tasks/progress_notes/T-V7-2.md \
  apps/wired/v7_tasks/V7_PROGRESS.md
git commit -m "T-V7-2: build cases_petrol_v7.csv inputs from the viable library shortlist"
```
