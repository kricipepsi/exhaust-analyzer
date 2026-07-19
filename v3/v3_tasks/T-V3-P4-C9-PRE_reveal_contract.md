### Goal ###
C9 reveal-contract DISCLOSURE (read-only) — instance the frozen signal-pack reveal-contract
template (`V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01`, 5 sections) for **C9 — independent
healthy-confirm** (11 cases), the next pack after C4 in the pinned sequence
`C2✓→C3✓→C6✓→C5✓→C4→C9→C8→C1→C7`. No live edit, no yardstick mint, no synthesized values.
### Progressive-disclosure role — the PRE step ###
C9 is the "prove-healthy" cluster: cases the engine wrongly assigns a fault family because it
cannot positively confirm system health. The contract freezes what a healthy-confirm producer may
claim, from `cluster9.md` + owner-pinned `value9.md`, before any seed or simulation exists.
### Success criteria ###
Produce `v3/reports/V3_C9_REVEAL_CONTRACT_<date>.{md,json}` via a read-only extractor
(`v3/build_c9_contract.py`, adapt `build_c5_contract.py`; py_compile+ruff+pyright clean):
1. **Producer gates** transcribed from `cluster9.md` + `value9.md` with file+line cites and
   grounding tags per threshold (standardized / manufacturer-typical / empirical-anecdotal —
   tags are labels, not blockers). Name the emitted state(s) (healthy-confirm analogue of
   `LeanRootCauseState`; abstain state for unproven health mandatory).
2. **Already-live-column audit (mandatory — the C5-PRE lesson, stronger here):** C9 sits on the
   SAME acquisition actions as prior packs (A1_TRIMS reaches C9; A2_MODE06 reaches C9 —
   min-signal-set §actions). C2B/C6B/C5B landed trims, Mode $06, MAF and load columns live. Audit
   per required signal: already-live vs genuinely-new. Expect the new-column ask to shrink toward
   zero; state the actual residue.
3. **Consumers named** from the live rule files (expected: `no_fault.json` NF-001/NF-002 +
   the fault-family rules C9 cases currently lose to). **Interaction disclosure mandatory:**
   C6B PRUNES NF-001/NF-002 under decisive sensor evidence with C3 precedence — a C9
   healthy-confirm boost must not resurrect an NF verdict those guards killed. Cite the live shim
   semantics (read `integration_shim.py`; don't edit).
4. **Case split:** the 11 C9 case_ids × {BUILDABLE_NOW / SCORING_GATED (DATA_GAP / HARD /
   TUNABLE_HELD)} reconciled against `V3_P4_RESIDUAL` buckets and the P4-1/P4-2 reports (they list
   C9 as 11; reconcile and flag any drift).
5. **FT-8 neighbour union derived LIVE** from the touched rule files' `passes_cases` (post-C5B);
   dual target+neighbour cases named; NF-regression exposure explicit (the C6 pack's NF prunes are
   currently-passing state that a C9 boost could regress).
- Baseline pinned `POST_T_V3_P4_C5B` / `V3_YARDSTICK_2026-07-06-C5B` (csv `c49c17af…`); grep gate on
  the report; scoreboard `score` unchanged (`top3_family` 250/294, `Hash lock: ok`).
- No engine/lab/registry/corpus/scorer/`run_suite.py`/yardstick edit; `Vault/` untouched.
### Context ###
- Template: `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.{md,json}` + worked C5/C6 instances.
- Cluster & values: `v3/research/value_answers/cluster9.md`? — NOTE: cluster9.md does not exist in
  value_answers (C1–C7 only + value9.md); the C9 cluster study may live in the residual/handoff
  reports. **First step: locate the C9 source docs (PHASE4_HANDOFF.md, V3_P4_RESIDUAL, value9.md);
  if no cluster-level study exists, STOP and report — the contract cannot be instanced from values
  alone.** Surface, don't improvise.
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
The owner (C9 pack go/no-go + sequencing vs stop-rule) and `T-V3-P4-C9-SYNTH`/`C9A` (forward).
### Disclosure ###
Surface, don't hide: the already-live-column residue; NF prune/boost tension; any case that is
"healthy-confirm" only by absence of data (belongs in abstain, not in a passing band).
### Progress hook ###
Ledger T-V3-P4-C9-PRE → done; dual-gate note `progress_notes/T-V3-P4-C9-PRE.md`.
### Depends on ###
T-V3-P4-C5B done. Independent of C4A-R — may run in parallel (read-only).
