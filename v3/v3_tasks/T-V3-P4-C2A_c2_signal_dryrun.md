### Goal ###
The first Phase-4 **signal pack**, DISCLOSE half. Once the owner supplies the C2 discriminating
measurement (live fuel trims + Mode $06 catalyst data) as real values for the 22 C2 cases, simulate
— **read-only** — the proposed producer state (which lab state the new columns would drive) and
consumer rule (which rule reads it), and predict exactly which of the 22 flip into top-3 and whether
any neighbour regresses (FT-8 = full-corpus no-regressed-family audit). **No live lab/registry/corpus
edit, no yardstick mint.** It proves the C2 signal actually separates rich_mixture from
catalyst_failure on real data before the commit (`T-V3-P4-C2B`) touches the engine.

### Progressive-disclosure role — the DISCLOSE step ###
C2 is the recommended first pack (`V3_MIN_SIGNAL_SET_2026-07-01.md`): tied-largest yield (22) and
the cheapest acquisition (two Tier-a OBD reads). But "the research says this signal separates them"
is a claim about physics; whether the owner's *actual* measured values, run through a concrete
producer threshold + consumer rule, move these 22 cases without breaking neighbours is only knowable
by simulating on the delivered data. This task discloses that yield + regression risk. The commit
`T-V3-P4-C2B` — add the corpus column, wire the producer into live GASLab/OBDLab, adjust the
consumer rule, re-score, mint a new yardstick — runs only behind this disclosure + owner sign-off.
Reveal first; commit later.

### Data gate (updated — provisional synthetic seed) ###
Under the provisional-synthetic policy (`4DLab_CLAUDE.md` §Provisional synthetic signals), this task
now runs on the **synthetic C2 seed from `T-V3-P4-C2-SYNTH`** (research-grounded, web-corroborated,
tolerance-wide, `synthetic=true`) — not owner data. Report predicted flips as **synthetic-driven**
(keep the synthetic-vs-real split). The required columns, per the acquisition contract:
- Columns (A1_TRIMS + A2_MODE06 catalyst): `stft_idle_pct, ltft_idle_pct, stft_2500_pct,
  ltft_2500_pct, mode06_catalyst_margin_pct, catalyst_index_ratio` and, where available,
  `pre_post_cat_hc_delta_ppm, pre_post_cat_co_delta_pct`. Units/bounds per
  `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md §C2`. Nullable where a vehicle's tool is unsupported.
- Delivered as the `T-V3-P4-C2-SYNTH` side file (`v3/data/c2_synthetic_seed_2026-07-01.*`). Cases the
  research cannot ground stay abstained — do not fill them. Real owner data, when it lands, replaces
  the seed (same simulator).
The 22 C2 cases: CASE-015, CSV-100, CSV-121, CSV-122, EXP-N017, EXT-232, EXT-233, PDF-HI-006,
case_004, era1_017, era2_015, CASE-023, CASE-029, CASE-040, EXT-217, PDF-HI-001, RULE-CO-1,
YAML-PDF_HI_001, case_002, case_015, case_017, era2_019.

### Why this split (the trap it avoids) ###
Wiring a new producer state + consumer weight straight into the live engine risks (a) shipping a
discriminator that is *diagnostically wrong* on real values (worse than a miss — confidently wrong),
and (b) regressing a neighbour that shares the `rich_mixture` / `catalyst_failure` rules or their
`competition_group`. Both are checkable by simulating the proposed producer/consumer as an overlay
over current scores, exactly as `T-V3-4A` simulated reweights read-only. No engine state is mutated.

### Success criteria ###
Produce `v3/reports/V3_C2_SIGNAL_DRYRUN_<date>.{md,json}` from the owner-supplied C2 values:
1. **Producer simulation:** apply the proposed emit rule (TRUE_RICH when sustained negative trims;
   LOW_OSC_OR_HIGH_INDEX when Mode $06 margin/index fails without rich trims — thresholds per
   spec §C2.3) to each of the 22 cases' supplied values; record the state each would emit.
2. **Consumer simulation:** overlay the resulting state onto the C2 consumer rules
   (`rich_mixture.json` RM-001/RM-003/RM-004, `catalyst_failure.json` CF-001/CF-002/CF-006/CF-007)
   and recompute the case's family rank read-only. Record predicted new rank + top-3 membership.
3. **Yield disclosure:** of 22 → how many flip to top-3 (`WOULD_BANK`), how many still miss
   (`STILL_SHORT` — say why: absent tool value / threshold miss / genuine overlap), how many the
   owner could not supply (`ABSTAIN_NO_DATA`).
4. **FT-8 neighbour audit:** enumerate every case that shares a touched rule / `competition_group`
   and simulate whether the overlay changes its family — list any predicted regression by case_id.
5. **Commit scope for C2B:** the exact producer threshold + consumer change the commit should make,
   sized from the simulation (not guessed).
- **Self-check:** zero-overlay (no new state) reproduces current ranks for all 294 (no drift), same
  discipline as `T-V3-4A`, before any C2 case is simulated.
- Inner loop clean on the helper (`py_compile`, `ruff`, `pyright`). `top3_family`, the yardstick,
  the live corpus, and every registry/lab file are **untouched**.

### Disclosure (what this task must surface, not hide) ###
If fewer than 22 flip, that shortfall **is** the finding — separate "signal absent (owner couldn't
measure)" from "signal present but doesn't separate on real values." The second case means the
research discriminator underperforms here; say so plainly rather than forcing a threshold to pass the
22. Name every neighbour the overlay would regress, so `T-V3-P4-C2B` looks exactly as risky as it is.

### Context ###
- C2 contract (columns/units/producer/consumer/thresholds): `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md`
  §C2 + JSON `contracts.C2`.
- Acquisition rationale + why C2 first: `v3/reports/V3_MIN_SIGNAL_SET_2026-07-01.md`.
- Read-only rank-overlay precedent: `v3/tunable_reweight_sim.py` (`T-V3-4A`) — reuse its
  recompute-ranks-from-scores approach; do not import/mutate engine state.
- Current ranks/scores to overlay against: `apps/wired/v7/runs/POST_T_V3_3D/results.json`.
- Consumer rules + neighbour sets: `labs/comlab/registry/rules/rich_mixture.json`,
  `catalyst_failure.json` (`base_weight`, `chemistry_evidence`/`obd_evidence`, `competition_group`,
  `passes_cases`). Query only.

### Consumer (signal/noise) ###
- **Consumer:** the owner's go/no-go on `T-V3-P4-C2B` and its exact producer/consumer scope; the
  FT-8 gate. This task adds **no** live field/state — it *simulates* the C2 producer/consumer the
  commit will add.

### Deliverables ###
1. `v3/reports/V3_C2_SIGNAL_DRYRUN_<date>.md` — CREATE. Per-case producer/consumer sim + verdict.
2. `v3/reports/V3_C2_SIGNAL_DRYRUN_<date>.json` — CREATE.
3. `v3/c2_signal_sim.py` — CREATE, read-only overlay simulator (zero-overlay self-check + per-case
   producer emit + consumer rank recompute). No engine/lab import-mutation.

### Files to touch ###
- `v3/reports/V3_C2_SIGNAL_DRYRUN_<date>.md` (CREATE)
- `v3/reports/V3_C2_SIGNAL_DRYRUN_<date>.json` (CREATE)
- `v3/c2_signal_sim.py` (CREATE, read-only)

### Out of scope ###
**No corpus column committed to the live CSV. No GASLab/OBDLab producer edit. No registry rule edit.
No re-score that mutates a run. No yardstick mint. No synthesized values** (owner-supplied only;
unmeasured → abstain). No abstain-dial change (MARGIN=0.02). Writes only under `v3/`. Never `Vault/`.
GRAPH GUARDRAIL: no `graphify` / frozen-graph rebuild; a fresh offline index for querying is fine.
No secrets in files. (All live wiring is `T-V3-P4-C2B`, gated behind this + owner sign-off.)

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/c2_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/c2_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/c2_signal_sim.py
# zero-overlay self-check reproduces current ranks for all 294 (no drift):
/agent_workspace/.venv-wired/bin/python v3/c2_signal_sim.py --self-check
# simulate on owner-supplied C2 values:
/agent_workspace/.venv-wired/bin/python v3/c2_signal_sim.py --c2-data <owner_file> --write v3/reports/V3_C2_SIGNAL_DRYRUN_<date>.json
```
Gate: self-check drift == 0; all 22 C2 case_ids present with a verdict
(WOULD_BANK / STILL_SHORT / ABSTAIN_NO_DATA); every predicted FT-8 regression named; the C2B commit
scope (producer threshold + consumer change) stated from the sim. `git status` shows only new files
under `v3/` (no registry/lab/engine/CSV file).

### Progress hook ###
PROGRESS.md `T-V3-P4-C2A`: Status=done, Files changed=3 (all new under v3/), Verification="C2 signal
dry-run on owner data: of 22 -> W would-bank / S still-short / A abstain-no-data; producer/consumer
simulated read-only; FT-8 regressions named; C2B commit scope sized; zero-overlay self-check drift=0;
no engine/lab/registry/corpus/yardstick touched".

### Depends on ###
`T-V3-P4-2` done (C2 confirmed first pack + column contract). **Blocked on the owner supplying C2
values** for the 22 cases. Not runnable until that data lands.
