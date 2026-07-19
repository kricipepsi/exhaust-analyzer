# DNA family — task ledger (PROGRESS)

Authored 2026-06-11 (architect). Source: the 2026-06-11 rework/answerability audit
and `docs/research/DNAresearch.md`. Pick the first `pending` row whose Blocked-by are
all `done`. One task per session.

## Task log

| ID | Title | Lab | Status | Blocked-by | Signal/noise consumer (named) |
|---|---|---|---|---|---|
| T-DNA-1 | Revised symptom catalog (6×3 reworked pairs) | symptomlab | done | — | COMLab `fault_atlas_router` symptom→family prior (proposal COMLab-A) |
| T-DNA-2 | Add `load_state` environmental axis | symptomlab | done | T-DNA-1 | COMLab context-modifier weights (proposal COMLab-B) |
| T-DNA-3 | Emit `rated_rpm` from VINLab (DBS P14 source) | vinlab | done | — | `projection.py` → `ObdLabDnaView.rated_rpm` → OBDLab RPM ceiling (exists) |
| T-DNA-4 | Formalize CoC fields + reconcile emissions block | vinlab + contract | done | — | GASLab CoC threshold tables via projector (pairs COMLab-C path fix) |
| T-DNA-5 | `model` disposition via DBS variance check (Q8) | vinlab + DBS | done | — | DTCLab `DtcLabDnaView.model` requirement — keep-empty vs drop |
| T-DNA-6 | `fuel_type` proposal (+ altitude_band context note) | vinlab | done | — | GASLab E5/E10 blend-correction context (proposal, gaslab wiki §1.4) |
| T-DNA-7 | Bump `VehicleDNA` schema_version + round-trip new fields | dnalab | done | T-DNA-1, T-DNA-2, T-DNA-3, T-DNA-4, T-DNA-6 | COMLab `OrchestratorInboundRequest.vehicle_dna` ingestion |
| T-DNA-8 | Reconcile symptom catalog to revised 18-pair set (close T-DNA-1 gap) | symptomlab | done | — | COMLab `fault_atlas_router` (proposal COMLab-A) — same 18 keys |
| T-DNA-9 | Add `oil_consumption` symptom (worn rings / valve-stem seals / turbo seal / PCV) | symptomlab | superseded → **T-OIL-1** | T-DNA-8 | COMLab `fault_atlas_router` (proposal COMLab-A extension) |

> **Owner sequencing (2026-06-11):** T-DNA-8 and T-DNA-9 run in a **final cleanup
> session after all other T-DNA tasks are done** (owner decision — do not run them
> mid-pack). See `HANDOFF.md`.

## Test-harness sub-pack (isolation) — T-DNA-TH-*

Authored 2026-06-12 (architect, owner-requested). Gives each DNA-family lab its **own
lab-local** test harness so every module is exercisable **in isolation** — controlled
inputs supplied by the test, not the real sibling labs or production data files.
Owner decisions (2026-06-12): scope = dnalab + vinlab + symptomlab (the last via the
proposed catalog-injection method); mechanism = **test-only doubles, no production
change**; layout = **slim data-lab template** (no generative fault-box folders).
Shared contract: `DNA_ISOLATION_HARNESS.md`. Each row is independent — run one per
session, any order.

| ID | Title | Lab | Status | Blocked-by | Signal/noise consumer (named) |
|---|---|---|---|---|---|
| T-DNA-TH-1 | dnalab assembly isolation harness (fake decode/resolve via monkeypatch) | dnalab | done | — | anti-orphan (test): builders `make_vin_dna`/`make_symptom_dna` + fakes consumed by `tests/unit/test_assembly.py` isolation cases (this diff). No schema field added. |
| T-DNA-TH-2 | vinlab isolation harness (mini fixture `data_dir` + per-module unit tests) | vinlab | done | — | anti-orphan (test): `make_mini_data_dir` + overlay builders consumed by `tests/unit/test_horizon.py`, `test_stress_rpm.py`, `test_switches.py`, `test_decode_isolation.py` (this diff). No schema field added. |
| T-DNA-TH-3 | symptomlab isolation harness (catalog injection via `allowed_path=`) | symptomlab | done | — | anti-orphan (test): good-18 + bad-17 YAML fixtures consumed by `tests/unit/test_validator.py`/`test_resolve_isolation.py` (this diff). No schema field added. **Proposed method — see task file; owner sign-off if not already given.** |

Task files: `T-DNA-TH-1_*` here in `labs/dnalab/tasks/`; `T-DNA-TH-2_*` in
`labs/vinlab/tasks/`; `T-DNA-TH-3_*` in `labs/symptomlab/tasks/` (each beside the code
it touches). Progress notes land in each lab's own `tasks/progress_notes/`.

## Audit-remediation sub-pack (2026-06-12) — T-DNA-10..13

Authored 2026-06-12 (architect, owner-requested) from the tri-module audit
`labs/dnalab/docs/audits/AUDIT_2026-06-12_trimodule_dna_vin_symptom.md`. Each row is
independent — run one per session, any order. Task files sit beside the code they touch.

| ID | Title | Lab | Status | Blocked-by | Signal/noise consumer (named) |
|---|---|---|---|---|---|
| T-DNA-10 | Rename `EngineState` wire value `won_not_start` → `will_not_start` (both ends) + `schema_version` 1.1→1.2 | symptomlab + comlab + dnalab | done | — | `comlab/core/symptom_router.route_symptom` — existing live `engine_state` consumer; rename keeps its code path live (no field added). |
| T-DNA-11 | Forward-register COMLab-B (`load_state`) into `CROSS_LAB_DEPENDENCIES.md` + `comlab/tasks/PROGRESS.md` | comlab (ledger) | done | — | The registration **is** the deliverable: makes `load_state` a ledgered Stage-4 reader (COMLab-B context-modifier, 65% cap) so it's on the S4 anti-orphan checklist. |
| T-DNA-12 | Decompose `decode_vin_payload()` into helper seams (behaviour-preserving) | vinlab | done | — | N/A — no schema field; gate = 173 vin tests green, no test edits. |
| T-DNA-13 | Audit clarity fixes: `to_json` naming (D1) · checksum comment (V2) · magic strings (V3) | vinlab + symptomlab + dnalab | done | — | N/A — no schema field; JSON wire unchanged; gate = all suites green. |

> Task files: `T-DNA-10_*` in `labs/symptomlab/tasks/` (owns the enum); `T-DNA-11_*` in
> `labs/dnalab/tasks/`; `T-DNA-12_*`/`T-DNA-13_*` in `labs/vinlab/tasks/`. T-DNA-10 is one
> coder session despite spanning three labs (small mechanical edits). T-DNA-11 is architect/
> registry bookkeeping — **no code, no COMLab build** (that stays a Stage-4 task).

## Cross-lab dependencies (COMLab — NOT authored here; separate codebase/session)

These are the named consumers the DNA tasks above point to. Each must be registered
in `labs/comlab/comlab/config/proposals/entries.yaml` and shipped in a COMLab session
for the paired DNA change to count as live (not orphan).

| Dep | Pairs with | What COMLab must do |
|---|---|---|
| COMLab-A | T-DNA-1 | Route the revised tier_1/tier_2 strings to fault families in `fault_atlas_router`; replace the legacy 18-pair routing map. |
| COMLab-B | T-DNA-2 | Consume `load_state` in the context-modifier prior; apply the research §"Context-Modifier Shifts" promotions/demotions; enforce the **65% trust-ceiling cap** on the symptom prior (research §"trust ceiling"). |
| COMLab-C | T-DNA-4 | Fix `projection.py` path bug: read CoC fields at **top level** and emissions flags at **`emissions.*`** (today reversed — both project as `None`). |
| COMLab-D | (rework audit) | Realign OBD/DTC lab-mirror enum drift (`upstream_o2_type`, `air_metering_strategy`, `resolved_horizon`, `induction_type`) to canonical contract vocabulary. |

## Owner follow-ups (non-code)

| ID | Item | Decision needed |
|---|---|---|
| OWNER-1 | Commercial paired-repair data (CarMD API / iATN FIX) for empirical prior validation. Free datasets are synthetic or telemetry-only (research §"Feasibility Verdict"). | Procure a license, or ship the prior on research-derived **estimated** bands (flagged estimated) and validate later. |

## Notes

- The symptom-prior probability tables and context-modifier weights themselves live
  in **COMLab**, not the DNA family. This pack supplies the *vocabulary and data*
  they consume; COMLab-A/B own the numbers.
- DNA10 Q2/Q3/Q4 are already answered from DBS (see audit); they are not tasks here.
  Q8 was the only DBS question with an open DNA-side decision and is closed by T-DNA-5.
- **Catalog discrepancy (found by the 2026-06-11 doc audit → T-DNA-8).** T-DNA-1 is
  `done` and its progress note claims "18 total pairs", but the live
  `allowed_combinations.yaml` is **17 pairs** (mtime 2026-05-22, never edited):
  `visible_exhaust_smoke = {black_smoke, blue_oily}`, missing `white_sweet_smell` and
  still on legacy `blue_oily`. The 18-pair invariant therefore raises at validator
  construction, transitively breaking the symptom path (and any DNALab test that builds
  a validator). T-DNA-8 reconciles it. Owner deferred the fix to the final cleanup
  session.
- **`oil_consumption` — RESOLVED 2026-06-12, moved to a dedicated pack.** The open
  structural question (7th tier_1 vs tier_2-under-existing) was decided by the owner as
  **Option A: a 7th tier_1, invariant 18→21 (clean 7×3 grid)**. The two research dossiers
  (`planning/oilconsumption.md`, `OilburnCases.md`) expanded this from a lone
  symptom add into a cross-lab oil-burning set (5 fault cases P_NEW_09…13). It now lives
  in **`planning/oil_consumption/`** (START_HERE + PROGRESS). T-DNA-9 is
  superseded by **T-OIL-1** (symptom side, authored & ready); GASLab signatures, KG
  fault nodes, and COMLab routing are T-OIL-2…5 in that pack.
- **Docs note:** the per-lab `docs/` sets (PRD/HLD/DLD/LLD/ADR/BDD/VOCAB) were authored
  2026-06-11 against the then-live code. Because the pack is closing gaps live
  (`rated_rpm`/T-DNA-3, `load_state`/T-DNA-2 already landed), the SymptomLab and VINLab
  doc sets need a **single refresh pass in the final cleanup session** once all fields
  are in. See `HANDOFF.md`.
