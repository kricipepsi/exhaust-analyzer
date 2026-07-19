# T-V7-1 — Case-library research + viability map (read-only)

**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `pending` · **Blocked by:** —
**Mode:** READ-ONLY — research only; **no source/data/test edits**. · **Scope owner:** wired-v7.
**Load skills:** wired-python, wired-verification-loop, html-extractor.

## Objective
Turn the owner's curated case libraries into a **buildable spec**: which cases are
viable for the **current** wired engine, what columns the v7 CSV needs, whether every
reachable fault family is covered, and which cases are missing essential input (→
owner queue). This report **bounds** T-V7-2..5.

## Signal/noise
Adds no domain field or fault. The **named consumer** is T-V7-2 (builds the CSV to
this spec) + T-V7-3 (oracle) + the owner (fills the incomplete-case queue). Artifact:
`apps/wired/v7_tasks/reports/V7_1_RESEARCH_<date>.md`.

## Pinned facts (verified at authoring)
- **Case source (read natively, do not copy in):** `/home/m/Desktop/casesextra/`.
  Primary `cases_library_v2.html` — cases by root-cause category (Mechanical / ECU /
  Sensor / Fuel / Ignition / Emissions); per case a 5-gas physical-truth table, an
  OBD PID/trim table, a Conclusion, tiered confidence, truth-vs-perception gates, and
  a "Missing Cases / Status" coverage index. Secondary: `cases_library.html`,
  `cases_library_research.html`, `cases_petrol_era_v1.csv` (55 rows),
  `cases/cases_petrol_master_v5.csv`.
- **Current engine truth (in-repo):** input contract = the shape of
  `apps/wired/tests/fixtures/oil_cases/MW-002.json` (+ optional `obd`/`dtc` blocks per
  `apps/wired/tests/test_tracing.py::_obd_inputs`); fault taxonomy =
  `labs/comlab/comlab/schemas/vocabulary.py` + `core/fault_atlas_kg.py`; verdict =
  `comlab.schemas.response.OrchestratorFinalUIOutput.diagnostic_verdict`; REG-V2
  (73 rules).
- **No `ARCHIVE/`** and **no `diagnose()`-derived expectations** in this task.

## Scope
**IN:**
- Convert the HTML libraries to clean markdown (`html-extractor`) into a scratch area
  **outside the repo** (or `/tmp`); mine them — do not commit the conversions.
- Build the **candidate inventory**: every library case with its category, its input
  facts (5-gas idle/2500, OBD trims, freeze-frame, symptom, VIN bits where given), and
  its documented conclusion (the library's expected fault).
- **Viability tag** per candidate against the current engine:
  - `viable` — all inputs the current contract needs are present and the conclusion's
    fault family exists in the current vocabulary;
  - `incomplete` — references a fault the engine supports but **missing an essential
    input** the contract requires → add to the `INCOMPLETE_CASES` quarantine (owner
    fills it); name the exact missing field(s);
  - `out-of-scope` — conclusion targets a fault family the current engine does **not**
    reach (defined-but-unreached or absent) → defer with the reason.
- **Coverage matrix:** list every **reachable** fault family (from the atlas/vocab,
  cross-checked with REG-V2 rules + the wired-forwarded lab signals) and map how many
  `viable` candidates cover each — flag families with **zero** viable cases as gaps
  (these are where the suite would be blind to errors). Include the negative/edge/
  invalid classes the suite must carry (malformed input, missing-bank, conflicting
  signals) so the suite can "catch all possible errors".
- **v7 column spec:** the exact CSV columns — input columns mapped to the current
  `diagnose()` contract (name them), plus the oracle columns T-V7-3 will fill
  (`expected_fault_family`, `expected_fault_code?`, `expected_state?`,
  `expected_confidence_min/max?`, `expected_perception_gap?`,
  `expected_demotion_note_contains?`), plus bookkeeping (`case_id`, `category`,
  `source_ref`, `tag`).
- Write `apps/wired/v7_tasks/reports/V7_1_RESEARCH_<date>.md` with: candidate
  inventory summary, viability tally, the coverage matrix (+ gaps), the column spec,
  and the `INCOMPLETE_CASES` list; mirror the incomplete list into the ledger's
  **Owner action queue**.

**OUT:** writing the CSV (→ T-V7-2); writing any `expected_*` value (→ T-V7-3);
running `diagnose()` to derive expectations; copying raw library files into the repo;
any source/data/test edit; `ARCHIVE/`; `graphify`; `Vault/`.

## Steps
1. `html-extractor` the three HTML libraries to scratch markdown; skim the category
   structure + the Missing-Cases index.
2. Enumerate candidates with inputs + documented conclusion.
3. Read `vocabulary.py`/`fault_atlas_kg.py` for the reachable family set; tag each
   candidate `viable`/`incomplete`/`out-of-scope`.
4. Build the coverage matrix + gap list + the negative/edge class list.
5. Pin the v7 column spec; write the report; populate the Owner action queue.
6. Fill `v7_tasks/progress_notes/T-V7-1.md` gates; STOP. **If the queue is non-empty,
   prompt the owner in the session summary.**

## Success criteria
- Candidate inventory + per-case viability tag, each citing its library `source_ref`;
  zero facts sourced from `ARCHIVE/`.
- Coverage matrix lists every reachable family with its viable-case count; gaps
  (families with zero viable cases) are named; the negative/edge/invalid classes are
  enumerated.
- A concrete v7 CSV column spec is stated (input columns mapped to the current
  contract + oracle columns + bookkeeping).
- `INCOMPLETE_CASES` cases each name the exact missing essential field and appear in
  the ledger Owner action queue.
- `git status` shows only new files under `apps/wired/v7_tasks/`; no raw library
  copies, no source/data edits.

## VERIFICATION GATE — T-V7-1
Complete in `v7_tasks/progress_notes/T-V7-1.md`: the viability tally; the coverage
matrix + gap list; the column spec; the incomplete-case list; confirm no `ARCHIVE/`
and no `diagnose()`-derived expectations.

## CODE REVIEW — T-V7-1
Complete in `v7_tasks/progress_notes/T-V7-1.md`: read-only; truth from libraries +
`vocabulary.py`/`fault_atlas_kg.py`/wikis only; no engine-derived expectations; raw
libraries not committed; `graphify` not run.

## Commit (owner, explicit paths)
```bash
cd /agent_workspace
git add \
  apps/wired/v7_tasks/reports/V7_1_RESEARCH_<date>.md \
  apps/wired/v7_tasks/progress_notes/T-V7-1.md \
  apps/wired/v7_tasks/V7_PROGRESS.md
git commit -m "T-V7-1: case-library research + viability map for the v7 suite"
```
