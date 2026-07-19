# Per-Lab Test-Harness Rollout — Ledger

> **Session start → read `TEST_ROLLOUT_START_HERE.md` first** (coder bootstrap:
> sandbox Python + local `_skills/` + the ledger-picks-the-task rule). This
> ledger is the source of truth for *which* task; START_HERE is *how* to run it.

**Date:** 2026-06-07 · **Author:** architect · **Pack home:** `planning/test_rollout/`
**Companion:** `TESTSUITE_MIGRATION_MAP.md` (data-keep vs tooling-retire),
`harness/HARNESS_PROGRESS.md` (the shared generative engine + GASLab pilot).

## What this pack delivers

Each diagnostic lab gets its **own** test harness — its own `ModuleDescriptor`,
its own master-derived CSV, its own forked generative suite — laid out on one
**canonical template**. The wired layer gets the matching integration folder.

**Governing model (owner-confirmed 2026-06-07):**
- The **generator engine is universal** (boundary/combinatorial/noise/overlap/fuzz
  operate on numeric ranges + box membership). It is **not** duplicated per lab.
- **Tailored per lab:** the `ModuleDescriptor` (schema ranges, fault-box table,
  `process()` entry point), the input-adapter, the oracle, and **which generators
  apply** (continuous labs use all; discrete labs use a subset).
- Each lab's CSV is a **projection of `cases_petrol_master_v6.csv`**: the columns
  that lab consumes × the rows that lab can decide alone. The **full** master is
  the *wired* integration gate (COMLab/e2e), not a per-lab fixture.

**Scope (owner-confirmed):** gaslab, obdlab, dtclab, comlab + wired.
`dnalab/symptomlab/vinlab` are data/lookup labs — out of scope (no fault-box harness).

## Premise correction (disk-verified 2026-06-07)

The migration manifest called obd/dtc/com "README placeholders." **On disk they
are forked**: obdlab 2060 LOC, dtclab 1582, comlab 4353, each with `schemas/`
contracts + `core/` + a `tests/` tree. So the real gate for a lab's *harness build*
is **v2 contract stability/green**, not "fork exists." Per-lab gates:
- **obdlab** — revive-vs-quarantine **resolved `revive` (emitter) 2026-06-08**; the harness
  (T-TST-8) is now gated on the obdlab **code-freeze** (`audit_backlog` FIX-2..7 + ARCH-2),
  the same set that blocks `T-KG-OBD-2`. The >95% NO_FAULT was a PID-less-corpus artefact.
- **dtclab** — blocked on the `T-FX-13` hex-regex contract gap.
- **comlab** — Stage-4 (last); its generative harness is thin (combinatorial over
  upstream verdicts) and overlaps the wired e2e gate.

## Generator applicability per lab

| Lab | boundary | combinatorial | noise | overlap | fuzz | Rationale |
|---|---|---|---|---|---|---|
| gaslab | ✓ | ✓ | ✓ | ✓ | ✓ | continuous gas concentrations + fault boxes |
| obdlab | ✓ | ✓ | ✓ | ✓ | ✓ | continuous PID/trim ranges |
| dtclab | — | ✓ | — | — | ✓ | discrete DTC codes/rules; ε-boundary & Gaussian noise N/A |
| comlab | — | ✓ | — | — | ✓ | input space = upstream verdicts; real gate is wired e2e |

## Task log

| ID | Task file | Status | Blocked by | Notes |
|---|---|---|---|---|
| T-TST-0 | `tasks/T-TST-0_per_lab_test_template_and_projection_contract.md` | completed | — | Canonical `tests/` template + master→per-lab projection contract (consumed-columns × decidable-rows per lab) + shared-engine import contract. Foundation for all rows below. |
| T-TST-1 | `tasks/T-TST-1_gaslab_align_to_template.md` | completed | T-TST-0 | Reconcile gaslab's existing `tests/` to the template; wire shared-engine import. Generative build itself stays in the T-TH series (don't duplicate). |
| T-TST-2 | `tasks/T-TST-2_obdlab_scaffold.md` | completed | T-TST-0 | Lay the template tree into `labs/obdlab/tests/` (structure + conftest + descriptor stub). Structure only — no live CSV/generators yet. |
| T-TST-3 | `tasks/T-TST-3_dtclab_scaffold.md` | completed | T-TST-0 | Same for `labs/dtclab/tests/`; generative slots limited to combinatorial+fuzz. |
| T-TST-4 | `tasks/T-TST-4_comlab_scaffold.md` | completed | T-TST-0 | Same for `labs/comlab/tests/` (it already has conftest/e2e — align, don't clobber). |
| T-TST-5 | `tasks/T-TST-5_wired_test_folder.md` | completed | T-TST-0 | Confirm/scaffold `apps/wired/tests/` + `apps/wired/harness/data/` as the master-CSV integration home; pin the master path. |
| T-TST-6 | `tasks/T-TST-6_obdlab_cases_csv.md` | done | — | 194 OBD-decidable rows projected. Script `labs/obdlab/tests/scripts/project_obdlab_cases.py`; output `labs/obdlab/tests/fixtures/obdlab_cases.csv`. Both gates clean in `progress_notes/T-TST-6.md`. Unblocks T-TST-8. |
| T-TST-7 | `tasks/T-TST-7_dtclab_cases_csv.md` | done | — | 194 DTC-decidable rows projected via `labs/dtclab/tests/scripts/project_dtclab_cases.py` to `labs/dtclab/tests/fixtures/dtclab_cases.csv`. Columns pinned to the master's real names (`dtcs`, `ff_*`, `ff_dtcs`, `fuel_status`); expected-output columns empty and marked `gt_method=characterization`. Both gates clean in `progress_notes/T-TST-7.md`. Unblocks authoring T-TST-9 once the separate DTC_REGEX gap is closed. |
| T-TST-8 | `tasks/T-TST-8_obdlab_decision_rate_harness.md` | done | — | Mode A complete: A1 0.0% bounce rate (26 signal-bearing), A2 100% gated rate (6 boxes), negative control proves fail-closed (100% bounce). 388 passed, 2 skipped. Progress note: `progress_notes/T-TST-8.md`. |
| T-TST-8W | _author at unblock_ | blocked — **waits on COMLab v2 rework stage** (`T-COMV2-*` pack, not yet started); **not** a cue to build COMLab here | COMLab v2 rework readers (`T-COMV2-*`), T-TST-8 (done) | **Decision-rate harness — Mode B, OBD→COMLab connected.** Floor (`FLOOR_CONNECTED`) is pinned from the first characterization run *after* S4 readers are live — do not pin it against the un-reworked COMLab. See "Implementation sequence & testing logic". Home `apps/wired/tests/` over the master corpus via `apps/wired/harness/run_cases.py`. Actionable-verdict rate on OBD-decidable rows ≥ FLOOR_CONNECTED (pinned from first characterization run when S4 readers are live). Forward-registered companion to T-TST-8. |
| T-TST-9 | `tasks/T-TST-9_dtclab_generative_harness.md` | done | T-TST-7 (done) | Build dtclab generative harness (combinatorial + fuzz only). **Engine reality pinned 2026-06-11:** the shared engine is gas-pilot — `CombinatorialGenerator` is `GAS_DIMS`-hardcoded (0 cases for discrete DTC input) and **no fuzz generator exists** (gaslab's `test_fuzz.py` is a skipped stub). Owner-confirmed route: **lab-local discrete combinatorial + fuzz** in `labs/dtclab/tests/generative/`, reusing the engine only for `ModuleDescriptor`/`run_suite`; engine generalization is forward proposal **FU-TST9-1**, not this row. Entry point `DataFusionSanitizer.sanitize`; exact §4 routing-tag oracle (no invented decision-rate floor). **Not** blocked by `T-FX-DTCHEX-1` (COMLab-side, connected-path only); dtclab's own regex is hex-correct. 575 tests pass (288 pre-existing + 287 new). Both gates clean in `progress_notes/T-TST-9.md`. |
| T-FX-DTCHEX-1 | `tasks/T-FX-DTCHEX-1_comlab_dtc_regex_hex_widening.md` | done | — | COMLab `DTC_REGEX` widened `[0-9]{3}`→`[0-9A-F]{3}` (matches wiki §2.3 + DTCLab). Both gates clean in `progress_notes/T-FX-DTCHEX-1.md`. |
| T-TST-10 | _author at unblock_ | blocked — **waits on COMLab v2 rework stage** (`T-COMV2-*` pack, not yet started); **not** a cue to build COMLab here | COMLab v2 rework start (`T-COMV2-*`) | Build comlab generative harness (thin: combinatorial over upstream verdicts) + reconcile with wired e2e (T-TH-12). Do not build against the un-reworked v1 COMLab. See "Implementation sequence & testing logic". |

**GASLab generative harness + GASLab master-derived CSV are NOT re-authored here** —
they are the in-flight `T-TH-10/11/14` rows in `harness/HARNESS_PROGRESS.md`.
T-TST-1 only aligns gaslab's folder to the shared template.

## Implementation sequence & testing logic (read before sequencing a coder)

**Optimal coder order** (one task per session; blockers respected):

1. **T-TST-7** — `dtclab_cases.csv` projection. Runnable now (spec authored). *(dtclab)*
2. **DTC hex-regex fix** — re-ID'd **`T-FX-DTCHEX-1`** (spec authored 2026-06-11). The
   gap lives in **comlab** (its `DTC_REGEX` is decimal-only), **not** dtclab. It gates the
   **connected** rows (T-TST-8W/T-TST-10), **not** the isolated T-TST-9. *(gate — connected only)*
3. **T-TST-9** — dtclab generative harness (combinatorial + fuzz only). Needs **1 only**
   (T-TST-7, done) — the step-2 fix is *not* a prerequisite for the isolated harness.
4. **COMLab v2 rework** (`T-COMV2-*` pack) — the bottleneck that releases 5 and 6. **Its
   own Stage-4 program, not a test-rollout deliverable.** *(external gate)*
5. **T-TST-8W** — Mode B, OBD→COMLab connected (wired). Releases once S4 readers are live
   (T-TST-8 already done).
6. **T-TST-10** — comlab generative harness, reconciled with the wired e2e gate.

Steps 1–3 are the only rows runnable without COMLab; 4 gates both 5 and 6.

**Isolated vs connected — why the COMLab-gated tail is a *wait*, not a *build trigger*:**

- **Per-lab (isolated) tests need no COMLab.** Each lab is tested against its own
  fault-box table through its own `process()` entry point (typed-JSON boundary, no
  cross-lab import). A reworked v2 lab is fully testable on its own — obdlab already is
  (T-TST-8 `done`); dtclab will be at T-TST-9. None of steps 1–3 touch COMLab.
- **Connected (fusion) tests have nothing to test until the spine exists.** T-TST-8W and
  T-TST-10 check that a lab's output, *fused* by COMLab, yields the right final verdict.
  Until COMLab is v2-reworked there is no fusion to assert against. T-TST-8W therefore
  **withholds its pass/fail floor** (`FLOOR_CONNECTED`) until "S4 readers are live" — it
  deliberately refuses to characterize a connected number against the un-reworked v1
  COMLab, because that number would be meaningless.
- **The two traps to avoid** (both are wording mistakes, not sequencing ones):
  (a) reading step 4 as a *test-rollout task* — it is not; the rollout's COMLab rows are
  downstream consumers of the COMLab rework and only wait for it. (b) building T-TST-10 /
  pinning T-TST-8W's floor against today's v1-era COMLab.
- **Why the COMLab rework is genuinely owed (product reason, not a test reason):** reworked
  obdlab v2 emits new fields (`lambda_perception_delta`, `per_bank_trim_delta`, `ve_pct`/
  `ve_validity`, `o2_failure_mode`) that are currently **orphaned** — every `T-COMV2-*` row
  is "the named reader that closes anti-orphan on `<field>` at S4." They shipped only
  because their consumers were *named and forward-registered*; the consumers aren't built.
  COMLab v2 is what both consumes and (via 5/6) tests them. So COMLab rework is owed on its
  **own** Stage-4 track, driven by the orphaned-field debt — the test rollout simply
  consumes it when it lands.

```
Per-lab (isolated) — testable now, COMLab irrelevant:
   gaslab ✓   obdlab ✓ (T-TST-8)   dtclab → T-TST-9
Connected (fusion) — needs the spine:
   obdlab ─┐
   gaslab ─┼─► COMLab v2 spine ─► verdict   ◄─ T-TST-8W / T-TST-10 test HERE
   dtclab ─┘   (not reworked yet)
```

## Unblocked-now path

T-TST-0 → then T-TST-1..5 (each its own session). T-TST-6..10 are authored in full
only when their blocker clears (matches the `T-TH-12` "author at unblock" pattern).

## Follow-ups (not in this diff)

- Add a bootstrap row for this pack to root `CLAUDE.md` (owner edits the HARD-RULE file).
- Resolve the `harness/` path drift (`HARNESS_START_HERE.md`/`HARNESS_PROGRESS.md`
  still cite `TestSuite/harness/`) and the `tasks/` vs `harness_tasks/` duplication —
  tracked separately in the harness pack, not here.
- **FU-TST7-1** — `PROJECTION_CONTRACT.md` DTCLab consumed-input list
  (`dtcs_mode_03/07/0a`, `mode_06_monitor_results`, `codes_cleared`, `active_mil`,
  `mil_flashing`) does not match the master's real columns (`dtcs`, `ff_*`,
  `ff_dtcs`, `fuel_status`). Reconcile contract to disk (same drift class as FU-TST6-1).
- **FU-TST7-2** — DTCLab payload fields `active_mil`/`mil_flashing`/`mode_06_monitors`
  have no master source column; populated by `T-TST-9` characterization, not projected.
- **FU-TST9-1 (proposal → harness pack).** The shared engine is gas-pilot only:
  `harness/harness/generators/combinatorial.py` is `GAS_DIMS`-hardcoded (yields 0 cases
  for discrete/PID labs) and there is **no fuzz generator** (gaslab's `test_fuzz.py` is a
  skipped stub). **Proposal:** add a discrete/enum combinatorial mode (keyed on
  `FieldRange.enum_values`) + a real fuzz generator so gaslab/obdlab/dtclab/comlab
  converge on one engine. **Named consumer:** the four labs' `tests/generative/` suites;
  dtclab's lab-local generators (T-TST-9) are the reference shape. Track as a `T-TH-*`
  harness-pack row — **not** a test-rollout deliverable.
- **FU-TST9-2 (doc drift).** `TEST_ROLLOUT_START_HERE.md` §1.3 + `TEMPLATE.md` cite
  `from harness.runner import run_generative_suite`; the runner exports **`run_suite`**.
  Reconcile both pack docs to the real symbol.
- **FU-TST7-3 (ID-collision hazard) — RESOLVED 2026-06-11.** Re-ID'd to
  **`T-FX-DTCHEX-1`** with spec `tasks/T-FX-DTCHEX-1_comlab_dtc_regex_hex_widening.md`.
  Two corrections from the disk check: (a) the fix is **COMLab-side** (its `DTC_REGEX` is
  decimal-only vs its own hex wiki + DTCLab), not a DTCLab fix; (b) it gates the
  **connected** path (T-TST-8W/T-TST-10), **not** the isolated T-TST-9 — so T-TST-9 was
  never truly blocked by it. The colliding `T-FX-13` is VINLab's *done* lookup task and is
  no longer referenced for this gap.
