# Generative Test Harness — Progress Ledger

**Source spec:** `TestSuite/harness/HARNESS_PROPOSAL.md` ·
`TestSuite/PER_MODULE_TESTSUITE_DESIGN_SPEC.md` (the fork model this plugs into)
**Tasks dir:** `TestSuite/harness/harness_tasks/`
**Mode:** STRICT (dual-gate: VERIFICATION GATE + CODE REVIEW clean before `done`)
**Last updated:** 2026-06-05 — authored T-TH-10..13 (master→per-lab fixture split). Decoupled the GASLab unit gate from the master: per-lab CSVs are filtered projections of `cases_petrol_master_v6.csv` (GASLab-decidable rows + consumed columns only); master stays canonical and becomes the wired integration gate (T-TH-12). T-TH-10 (build GASLab fixture + adjudicate H-3..H-6 drift) → T-TH-11 (retarget parity gate, drop dead `ctx_secondary_air_injection_active`, close T-TH-0). TestProp.md "additional tests beyond CSV" map to existing T-TH-1..4 (built) + T-TH-5/6/7 (pending) — no new generator rows. **CORRECTION 2026-06-05 (coder-caught at T-TH-10):** the master→GASLab projection is unbuildable as specced — `expected_top_fault` matches 0/277 `ChemicalSignature` values and has malformed rows (H-10). T-TH-10/11 → `blocked` behind new `T-MASTER-RECON` (upstream relabel + column-integrity fix, owner-adjudicated, wiring stage). Descriptor dead-field cleanup (H-9) moved T-TH-11 → T-TH-14 so timing-family validation runs now. **Next harness task = T-TH-14, not T-TH-10.**

**DISPOSITION 2026-07-07 (T-SHIP-4, ship pack — architect, owner-authorized):** this pack is
**superseded by the wired v7 accuracy harness** (`apps/wired/v7/`: 294-case corpus, wiki-grounded
oracle, hash-locked yardstick `V3_YARDSTICK_2026-07-06-C9B`) and the per-lab test suites, all green
2026-07-07 (`apps/wired/ship_tasks/reports/SHIP_VERIFY_2026-07-07.md`). Every non-`done` row below is
flipped `deferred (superseded by wired-v7 harness — reopen only by owner instruction)`; the master-CSV
track (T-MASTER-RECON, `cases_petrol_master_v6.csv`) is not on any live path. Rows kept, not deleted
(archive, don't delete). Next harness task: none.

This is the only file `HARNESS_START_HERE.md` reads to find the next task.
Keep under ~120 lines. Bulk notes (Plan, gate blocks, review blocks) live in
`harness_tasks/progress_notes/<task-id>.md`, not here.

**Project north star:** add a reusable, lab-agnostic harness that *generates*
and *analyses* tests from a `ModuleDescriptor` (schema ranges + fault-box table +
entry point), consumed by each per-lab forked suite (GASLab first) and the wired
suite — replacing hand-authored static CSV rows for boundary/combinatorial/noise/
overlap/metamorphic/fuzz/regression coverage.

**Signal/noise principle (harness variant):** every generator ships only with a
**named, existing consumer** — a forked suite that actually runs it. The pilot
consumer is the **built GASLab fork**. No generator ships "for later"; descriptor
rollout to other labs (T-TH-8) is gated on those forks existing.

**Isolation:** `TestSuite/harness/` is test-only tooling; it imports **no lab**.
A fork importing its own lab is not a cross-lab import. This does not breach the
"no cross-lab Python imports" runtime rule.

---

## Task log

| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| T-TH-0 | `harness_tasks/T-TH-0_core_descriptor_runner.md` | deferred (superseded 2026-07-07, see DISPOSITION) | T-TH-10, T-TH-11 | 2026-06-04 | — | **REOPENED 2026-06-04; resolution path set 2026-06-05.** Parity gate RED (4 mismatches) vs contracted "0 mismatches" — unmeetable against the stale `gaslab_suite_with_dna.csv`. Resolution: T-TH-10 rebuilds a clean GASLab-decidable fixture from the master + adjudicates H-3..H-6; T-TH-11 retargets the gate to it and closes this row. Do not flip `done` outside T-TH-11. | **Foundation.** `ModuleDescriptor` + generic runner + `.md` report emitter; GASLab descriptor from `gaslab/contracts.py` + `ChemicalSignature` box table. |
| T-TH-1 | `harness_tasks/T-TH-1_boundary_generator.md` | done | T-TH-0 | 2026-06-04 | — | 10/10 pass; ruff + pyright clean. GASLab run: 427/1020 match geometric oracle (41.9%); SAMPLE_INVALID dominates mismatches (validity gate pre-empt). Overlap caveat → T-TH-2. | Boundary / edge-point generator: per dim per box `min−ε, min, min+ε, max−ε, max, max+ε`; oracle = box membership; seeded. Catches `>=`/`>` inclusivity + off-by-ε. |
| T-TH-2 | `harness_tasks/T-TH-2_box_overlap_analyzer.md` | done | T-TH-0 | 2026-06-04 | — | 16/16 pass; ruff + pyright clean. GASLab run: 331/561 overlapping pairs, 21 identical-gas-signature pairs, 100% discrimination ceiling (SAMPLE_INVALID + 5 envelope-only boxes claim full space). Report at progress_notes/T-TH-2_overlap_report.md. | **Highest leverage.** Box-overlap & coverage-gap analyzer → `.md`: which box pairs intersect in feature space + which plausible regions fall into no box. Targets the discrimination ceiling. Consumer: GASLab fork + fault-atlas routing. |
| T-TH-3 | `harness_tasks/T-TH-3_combinatorial_generator.md` | deferred (superseded 2026-07-07, see DISPOSITION) | T-TH-1 | 2026-06-04 | — | **REOPENED 2026-06-04 — re-verify only.** Completed as the 4th task in a one-task-per-session breach (see Unplanned H-7), past the ≤50%-context budget — quality least-trustworthy. Files kept; re-run the full gate in a fresh isolated session to confirm before `done`. (Prior self-report: 11/11 pass; ruff+pyright clean on `.venv-wired`; GASLab run 174/1360 match, overlap caveat; report at progress_notes/T-TH-3_combinatorial_report.md.) | t-wise (pairwise) combinatorial corner coverage; catches multi-dimension interaction bugs a per-axis sweep misses. Consumer: GASLab fork. |
| T-TH-4 | `harness_tasks/T-TH-4_noise_characterization.md` | done | T-TH-0 | 2026-06-04 | — | 7/7 pass; ruff + pyright clean (`.venv-wired`, sandbox mount stale). GASLab run: 34 box curves, mean retention 100%→93%→83%→73%→57% across a=0.0..1.0; 7 brittle boxes (RICH_MIXTURE 32% … WORN_PISTON_RINGS 48% @ a=0.25); 30/34 centroids are overlap artifacts (retention anchored to observed centroid label, not signature — isolates noise from the T-TH-2 ceiling). `--collect-only` 62 tests clean; new-files-only ⇒ no regression. Report at progress_notes/T-TH-4_noise_report.md. | Noise / fault-injection characterization → `.md` degradation report (seeded; amplitude sweep). **Not** an inner-loop pass/fail gate. |
| T-TH-5 | _author at start_ | deferred (superseded 2026-07-07, see DISPOSITION) | T-TH-1 | — | — | — | Metamorphic / monotonicity property suite (directional domain relations; no exact oracle needed). |
| T-TH-6 | _author at start_ | deferred (superseded 2026-07-07, see DISPOSITION) | T-TH-0 | — | — | — | Contract / schema fuzz at the JSON boundary (malformed/missing/NaN/out-of-type/out-of-range → typed error, not crash). Consumer: each fork's input-validation contract. |
| T-TH-7 | _author at start_ | deferred (superseded 2026-07-07, see DISPOSITION) | T-TH-0 | — | — | — | Golden-corpus regression harness: seeded corpus snapshot + enumerate label deltas between versions (generalizes T-GV2-3 / T-GAS-10 delta discipline). |
| T-TH-8 | _author at start_ | deferred (superseded 2026-07-07, see DISPOSITION) | T-TH-0..7; per-lab fork existing | — | — | — | Per-lab descriptor rollout OBD → DTC → VIN → Symptom → COM, one descriptor per session. Gated on each lab's fork existing (`TESTSUITE_PROGRESS` §phase-gates: OBD/DTC/DNA/COM forks still unscoped). |
| T-TH-9 | _optional, on instruction_ | deferred | T-TH-0 | — | — | — | Confidence-calibration harness (reliability curve: higher confidence ↔ correctness). Build once a stable confidence/score surface exists. |
| T-TH-10 | `harness_tasks/T-TH-10_master_to_gaslab_projection.md` | deferred (superseded 2026-07-07, see DISPOSITION) | T-MASTER-RECON | 2026-06-05 | — | — | **BLOCKED — design invalid against the master (2026-06-05, coder-caught).** The filter `expected_top_fault ∈ ChemicalSignature` yields **0 of 277 rows**: master `expected_top_fault` is not GASLab enums and is not one vocabulary — family-level (`rich_mixture`), scenario-level (`Exhaust_Air_Leak_Pre_Cat`, `ECU_Logic_Inversion_*`), 61 perception-gap rows, and malformed cells (`single`×25, blank×14 = column misalignment, see H-10). Needs `T-MASTER-RECON` (owner-adjudicated upstream relabel + column-integrity fix) first — **not** an inline mapping table. Do NOT run until T-MASTER-RECON done. Spec must be re-authored post-recon. |
| T-TH-11 | `harness_tasks/T-TH-11_retarget_parity_gate.md` | deferred (superseded 2026-07-07, see DISPOSITION) | T-TH-10 | 2026-06-05 | — | — | Retarget `test_parity_replays_existing_csv` to the rebuilt fixture; redefine "0 mismatches" against the GASLab-decidable fixture; flip T-TH-0 → done. **NOTE 2026-06-05:** the descriptor dead-field cleanup (`ctx_secondary_air_injection_active`, H-9) is being **moved out of this task into T-TH-14** so timing-family validation isn't blocked behind the master-fixture chain. Blocked transitively via T-TH-10. |
| T-TH-12 | `harness_tasks/T-TH-12_master_wired_integration_gate.md` | deferred (superseded 2026-07-07, see DISPOSITION) | T-TH-11; 4DLabWired seam | 2026-06-05 | — | — | Master corpus as the **wired** end-to-end gate (L1→L5, assert top_fault/family/state/perception_gap). Owner call on stale-label rows: reconcile vs quarantine. Gated on the integration seam (`project_jaeger_deferred`). |
| T-TH-13 | `harness_tasks/T-TH-13_perlab_projection_rollout.md` | deferred (superseded 2026-07-07, see DISPOSITION) | T-TH-10..11; per-lab fork | 2026-06-05 | — | — | Generalise the projection to OBD/DTC/COM/DNA-VIN via `extract_lab_cases.py --lab <name>`, one lab/session, each gated on its fork (folds with T-TH-8). COMLab fixture inverts the filter (keeps perception-gap rows). |
| T-TH-14 | `harness_tasks/T-TH-14_dual_rpm_faultbox_extension.md` | deferred (superseded 2026-07-07, see DISPOSITION) | descriptor dead-field cleanup (H-9) — **decoupled from T-TH-11 2026-06-05** | 2026-06-05 | — | — | **Next harness task — validates the v2 timing family; master-independent.** Now also absorbs the `ctx_secondary_air_injection_active` removal (H-9) so it no longer waits on the blocked master-fixture chain (T-TH-10/11). Extend `FaultBox` with `dimensions_high` + `delta_directions` (idle→2500 two-point signature) + `dual_rpm_oracle`; populate the 3 CAM_TIMING boxes from 06b/§8.9 (replaces TBD-envelope placeholders). Breaks the T-TH-2 100% discrimination ceiling for RPM-differential families. Backward-compatible. Wiki-grounded ⇒ not blocked on v2 code or the master. |
| T-MASTER-RECON | `tasks/T-MASTER-RECON_master_relabel.md` | **done** | — | 2026-06-09 | — | VERIFICATION GATE + CODE REVIEW clean. 3 rows quarantined (blank family+pg); 17 `invalid_input` families → `no_fault`; 40 blank perception_gap → False; `lab_decidability` column added. Ruff + pyright clean. Report at `TestSuite/MASTER_RECON_REPORT.md`. | **Keystone — prerequisite for every master-derived fixture (T-TH-10/11/12, T-TST-6/7).** Owner ratified the 3 decisions 2026-06-09: (1) `expected_top_fault_family` → 12-value `FaultFamily` enum (SEMANTIC_CONTRACT §8 + EP-DTC-02 backbone; new values via `comlab/config/proposals/`); (2) 61 perception-gap rows = distinct fusion-only class + new `lab_decidability` column; (3) misaligned rows → `master_quarantine.csv`, OBD expecteds = characterization (master gains no OBD ground-truth columns). Also absorbs the master→OBD column-name inventory (FU-RECON-1). |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred`
**Blocked by:** comma-separated task IDs that must reach `done` first, or `—`.

> **Sequencing:** T-TH-0 → **T-TH-1 + T-TH-2** (prove the highest-value pair on
> the GASLab fork) → T-TH-3..7 → T-TH-8 rollout. One task per session; each ≤50%
> of a fresh context. Author each task file at the start of its own session
> (`_author at start_`), except T-TH-0 which is authored now as the entry point.

---

## Unplanned follow-ups

Discovered mid-prep. Logged here, **not** fixed inside a task unless that task
lists the file as a Deliverable.

| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| H-1 | proposal | The fault-box table is not yet a single canonical artefact — GASLab signatures are spread across `GAS_VOCABULARY` + per-signature wiki pages. T-TH-0 must define where the descriptor reads boxes from (extract once into a descriptor input, cite each box). | open — resolve in T-TH-0 scope |
| H-2 | proposal | OBD/DTC/DNA/COM forks are still unscoped (`TESTSUITE_PROGRESS` phase-gates). T-TH-8 rollout cannot run for a lab until its fork CSV+runner exist. | open — gated |
| H-3 | T-TH-0 parity gate | GAS-EAL-001: expected EXHAUST_AIR_LEAK, actual RICH_MISFIRE — collision-rule vsum threshold or rule ordering changed since CSV built. | open — CSV drift |
| H-4 | T-TH-0 parity gate | GAS-IOX-001: expected INCOMPLETE_OXIDATION, actual INCOMPLETE_COMBUSTION — partial-combustion routing changed. | open — CSV drift |
| H-5 | T-TH-0 parity gate | GAS-WVT-001: expected WRONG_VALVE_TIMING, actual RICH_MISFIRE — WRONG_VALVE_TIMING removed from ChemicalSignature enum; pri-82 rule gone. | open — CSV drift |
| H-6 | T-TH-0 parity gate | GAS-ESO-001: expected EGR_STUCK_OPEN, actual INCOMPLETE_COMBUSTION — EGR-gated fault routing changed. | open — CSV drift |
| H-7 | T-TH-0 | Existing `gaslab_suite_runner.py` broken: passes `secondary_air_injection_active` to `GasLabContext`, which no longer accepts it (removed from dataclass). Runner crashes with TypeError on first row. Harness correctly matches current GasLabContext signature. | open — pre-existing; harness side fixed in T-TH-11 |
| H-8 | T-TH-10 prep | TestProp.md §3 wants synthetic tests sourced from `gas_lab_ontology.yaml`; the harness generators (T-TH-1..4) source the box table from `gaslab/contracts.py` + `ChemicalSignature`. Verify the two sources agree (same bounds) — if they diverge, the box table or the ontology is stale. Not a new task unless they diverge. | open — verify |
| H-9 | T-TH-14 prep | The descriptor still carries the dead `ctx_secondary_air_injection_active` FieldRange (descriptor.py:312). **Re-homed 2026-06-05:** removal **moved from T-TH-11 into T-TH-14** so timing validation isn't blocked behind the master-fixture chain. | open — now resolved by T-TH-14 |
| H-10 | T-TH-10 (coder-caught, 2026-06-05) | **Master `expected_top_fault` is not a usable GASLab label source.** 0/277 rows match `ChemicalSignature`; the column mixes family-level (`rich_mixture`), scenario-level (`Exhaust_Air_Leak_Pre_Cat`, `ECU_Logic_Inversion_*`), 61 perception-gap rows, and **malformed cells** — `single`×25 and blank×14 indicate **column misalignment** (unescaped commas shifting fields). A mapping table cannot repair misaligned columns. Blocks T-TH-10 until `T-MASTER-RECON` normalises the vocabulary + fixes integrity upstream. | open — drives T-MASTER-RECON |

---

## Architect-level out-of-band patches

Convention edits applied directly outside the per-task diff.

| Date | File | Patch | Reason |
|---|---|---|---|
| 2026-06-04 | `TestSuite/harness/HARNESS_PROPOSAL.md` | created — design + test menu + task drafts | proposal, user-approved |
| 2026-06-04 | `TestSuite/harness/HARNESS_START_HERE.md` + `HARNESS_PROGRESS.md` | created pack | registration (own-pack decision, 2026-06-04) |
| 2026-06-04 | `CLAUDE.md` (root) | add harness row to Session bootstrap table → `HARNESS_START_HERE.md` | make pack auto-discoverable on a fresh session |
| 2026-06-04 | `TestSuite/harness/HARNESS_START_HERE.md` | §2 — add explicit path `GASLab/_gaslab_skills/<name>/SKILL.md`; clarify the 4 skills are read-by-path, not registered under `~/.claude/skills/` | coder reported "skills not found" (searched the registry); skills exist as files — fix discoverability |
| 2026-06-04 | `CLAUDE.md` (root) → Git ritual | add PowerShell backtick (`` ` ``) line-continuation convention for the commit block (multi-path `git add`); backtick at EOL, no `\`, no `;` joins | owner direction — make the user-pasted commit command paste-safe in PowerShell |
