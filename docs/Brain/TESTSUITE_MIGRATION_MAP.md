# TestSuite Migration Map — data to keep vs tooling to retire

**Date:** 2026-06-07 · **Author:** architect · **Scope:** disposition of root `TestSuite/`
(and the two stray copies at repo root) for the 4DLabV2 layout.
Paths are relative to the `4DLab/` repo root.

> **Governing principle (owner, 2026-06-07):** the old per-module suites were not
> good enough to test each module's *real* diagnostic capability. We do **not**
> carry them forward as test tools. We **migrate the truth** (corpus, reference
> readings, per-lab wikis/vocab/contracts, ontology) and **retire the tooling**
> (every `*_suite_runner.py`, every `*_suite_*.csv`, every `_build_*`/`_scratch_*`
> script, and the tests + audits that wrap them).
>
> The replacement test capability already exists in v2:
> - **per-lab unit** → generative harness + filtered projection fixture, in `labs/<lab>/tests/`
> - **full wired integration** → `apps/wired/harness/` against the master corpus

---

## 0. Who reads what today (grounded in code, not docs)

| Consumer | Data it actually reads | Status |
|---|---|---|
| `apps/wired/harness/run_cases.py` (wired integration) | `apps/wired/harness/data/cases_petrol_master_v6.csv` | completed path rewrite; smoke_cases.csv documented as missing |
| `4DLabV2/harness/` (generative, GASLab pilot) | `gaslab_suite_with_dna.csv` (root) | **stale dependency** — reads a DON'T-COPY file; sever via T-TH-10/11 before retiring it |
| `labs/gaslab/` lab + tests | `gas_lab_ontology.yaml` (→ `labs/gaslab/gaslab/data/`) | live; relative paths corrected to local data folder |

---

## 1. KEEP — diagnostic truth / reference (migrate, do not archive)

These are inputs to *authoring* descriptors, fixtures, and the integration gate —
not test tooling. They survive.

| Item (under `TestSuite/`) | What it is | Proposed v2 home |
|---|---|---|
| `cases_petrol_master_v6.csv` | **canonical** master corpus; the wired integration oracle | wired data dir, e.g. `apps/wired/harness/data/` (path then rewritten in `run_cases.py`) |
| `automotive.db` (~17 MB) | source vehicle DB behind the corpus | shared data/reference (decide: `4DLabV2/docs/reference/` or keep at root) |
| `High Idle Gas Readings for Faults.md` / `.txt`, `HighIdle.md`, `HighIdle1.md` | reference gas-reading truth (high-idle L2) | GASLab studies/reference under `labs/gaslab/` |
| `OBD/OBDdata.md`, `OBD/TestTableOBDwiki.md`, `OBD/OBDtestprop.md`, `OBD/TestTableOBD.cvs` | OBD reference data + wiki to author OBDLab's descriptor | `labs/obdlab/` wiki/reference |
| `COM/COMLab_HLD.md`, `COMLab_DLD.md`, `COMLab_LLD.md`, `SEMANTIC_CONTRACT.md`, `DNALab_TO_COMLab_FLOW.md` | COMLab design + the in/out contract | `labs/comlab/` docs (verify not already canonical elsewhere first) |
| `DTC/DTC_WIKI.md`, `DTC_VOCABULARY.md`, `DtcDoc_prepped.md`, `DtcDoc2_prepped.md`, `DTCLabProp.md` | DTC reference + vocab to author DTCLab's descriptor | `labs/dtclab/` wiki/reference |

> Before moving any `.md` here, grep it as a *target* — several may already have a
> canonical home in `docs/` (don't create a second source of truth).

---

## 2. DO NOT COPY — old per-module test tooling (retire → ARCHIVE)

The owner's rule applies directly. These are the suites that did not test real
diagnostic capability. They are superseded by the generative + wired harnesses.

| Item | Type |
|---|---|
| `gaslab_suite_runner.py`, `OBD/obd_suite_runner.py`, `DTC/dtc_suite_runner.py`, `COM/com_suite_runner.py` | suite runners |
| `gaslab_suite_with_dna.csv`, `gaslab_suite_basic_no_dna.csv`, `gaslab_suite_high_idle_with_dna.csv`, `gaslab_suite_high_idle_basic_no_dna.csv` | GASLab suite outputs |
| `OBD/obd_suite_with_dna.csv`, `obd_suite_basic_no_dna.csv`; `DTC/dtc_suite_with_dna.csv`, `dtc_suite_basic_no_dna.csv`; `COM/com_suite.csv` | per-module suite outputs |
| `OBD/_build_with_dna_csv.py`, `_scratch_validate.py`, `_scratch_verify_deltas.py`; `DTC/_scratch_gen_csv.py` | build/scratch generators |
| `tests/test_gaslab_suite_runner.py`, `OBD/tests/`, `DTC/tests/`, `COM/tests/` | tests wrapping the runners |
| `gaslab_suite_AUDIT.md`, `OBD/obd_suite_AUDIT.md`, `DTC/dtc_suite_AUDIT.md`, `COM/com_suite_AUDIT.md` | suite audits |
| `*_SUITE_BUILD_HANDOFF.md`, `*TESTSUITE_PROGRESS.md`, `*TESTSUITE_START_HERE.md` (GAS/OBD/DTC/COM) | suite-build ledgers |
| `tasks/T-GAS-*.md`, `T-CUR-1_*.md` (+ `tasks/progress_notes/`) | old suite-build task ledger |
| `enhancetests.md`, `AddTestCases.md`, `ADDcasesforcvs.md`, `vocab_audit_AddTestCases.md`, `db_coverage_gap_report.md` | suite-build working docs |
| `docs/TestProcedure.md`, `test2.md`, `testmd.md` | old procedure docs |
| `setup_env.ps1`, `_sanity_emit_span.py`, `pyrightconfig.json`, `20260524-204630/`, `.venv*` dirs | suite scaffolding/output |

Disposition: move the whole lot to `ARCHIVE/legacy_testsuite_2026-06/` with a
README banner (matches the Phase-5 archive pattern in `MIGRATION_MANIFEST.md`).

---

## 3. ADJUDICATE — not obviously keep or kill

| Item | Question for owner |
|---|---|
| `cases_petrol_master_v6_backup_2026-06-02.csv`, `…_06-04.csv`, `…csv.ft0_backup` | drop (git is the history) or keep one as a labelled snapshot? |
| `cases_petrol_era_v1.csv` | superseded by v6 → archive? |
| `cases_petrol.html`, `casesextra_new_cases.html` (also at repo root) | source HTML corpus — keep one canonical copy where? |
| `known_anomalies.json` (root + `apps/wired/harness/known_anomalies.json`) | which is canonical; is the root one still read? |
| `PER_MODULE_TESTSUITE_DESIGN_SPEC.md` | **still cited** by `harness/HARNESS_START_HERE.md` (§5 GASLab). Cannot blind-archive — either keep as live spec or rehome + rewrite the citation. |
| `TESTSUITE_CAPABILITY_REPORT.md`, `TESTSUITE_PROGRESS.md`, `TESTSUITE_START_HERE.md` | historical record of the retired approach → archive, or keep as rationale? |

---

## 4. Loose ends any move must close (grounded in §0)

1. **Sever the generative-harness → stale-CSV link.** `4DLabV2/harness/` reads
   `gaslab_suite_with_dna.csv` (a §2 retire item). T-TH-10/11 rebuild a
   master-derived fixture; the old CSV cannot be archived until those land.
2. **Fix the dead ontology ref.** [Closed] Corrected relative path resolutions in `test_ontology.py` and `test_validators.py` under the relocated `unit/` directory to resolve to `labs/gaslab/gaslab/data/gas_lab_ontology.yaml`.
3. **Rewrite the master path on move.** [Closed] Rewritten to point to `apps/wired/harness/data/cases_petrol_master_v6.csv` in `run_cases.py` and `smoke_cases.csv` documented as missing.
4. **Don't blind-archive `PER_MODULE_TESTSUITE_DESIGN_SPEC.md`** (§3) — the
   harness bootstrap still cites it.

---

## 5. Net picture

```
KEEP (truth)                         RETIRE (tooling)              NEW capability (already in v2)
─────────────                        ───────────────              ─────────────────────────────
cases_petrol_master_v6.csv  ───┐     *_suite_runner.py            apps/wired/harness/      (integration)
automotive.db                  │     *_suite_*.csv         ──X──  labs/<lab>/tests/        (per-lab unit)
High-Idle gas readings         ├──>  _build_*/_scratch_*.py        + 4DLabV2/harness/ engine
OBD/DTC/COM wikis+contracts    │     suite tests/audits/ledgers
gas_lab_ontology.yaml       ───┘
```

The old `TestSuite/` is **not** a thing we relocate intact. It is split: a thin
seam of truth migrates into the labs + wired layer; the bulk (the weak tooling)
goes to ARCHIVE. The actual testing is done by the generative per-lab harness and
the wired integration harness — neither of which inherits the old suite code.
