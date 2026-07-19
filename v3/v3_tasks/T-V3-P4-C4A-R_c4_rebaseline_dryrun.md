### Goal ###
C4 **re-baseline dry-run** — the RE-BASELINE the ledger requires before sizing `T-V3-P4-C4B`.
Re-run the C4 signal simulation **read-only** against the CURRENT baseline
`POST_T_V3_P4_C5B` / `V3_YARDSTICK_2026-07-06-C5B` (csv `c49c17af…`). The original C4A was sized
vs `POST_T_V3_3D` (197/294) — **two generations stale**: C2B, C3B, C6B and C5B have since moved the
ruler to 250/294 and, critically, wired live producer states whose collision/precedence semantics
C4's consumers must now respect as they actually exist in the shim, not as C4A assumed them.
### Progressive-disclosure role — the re-DISCLOSE step ###
C4B cannot be sized from C4A's numbers. This task re-discloses, against the live engine:
1. **Yield re-size:** of the 11 C4 cases, WOULD_BANK / ALREADY_PASS / STILL_SHORT /
   ABSTAIN_NO_DATA. Expect movement in both directions: some may now ALREADY_PASS (the C5B EGR
   trim-prune moved lean/catalyst outranking), some previous banks may shrink under live C5/C6
   collision guards. Report actual, not C4A's 10/11.
2. **Live-interaction audit (new since C4A):** `LeanRootCauseState` (C5B) and
   `SensorDynamicsState` (C6B) are LIVE in the registry shim with C3-precedence and C5/C6-collision
   guards. Simulate C4's ΔSTFT producer + EL/LC/SF consumer overlay **under the live guard
   semantics read from the shim source**, not re-derived from task prose. Any place where C4's
   proposed boost would fight an existing live prune/boost must be named case-by-case.
3. **Column-add evidence, refreshed:** which STILL_SHORT cases require the non-corpus columns
   (`co2_idle_pct` / `downstream_o2_v` / `propane_trim_shift_pct`) vs resolve by honest abstain —
   the C4B add-column-or-abstain decision input. CASE-022 (biased O2) is the known candidate;
   confirm or amend on current margins.
4. **Covered-vs-masked split** at MARGIN=0.02 — running tally for the deferred abstain-cal is
   12 (C3) + 5 (C6); report C4's contribution.
### Data gate ###
C4 target values come from the **C4-SYNTH seed** (`v3/data/c4_synthetic_seed_2026-07-05.{csv,json}`,
owner-pinned value4.1, tolerance-wide, `synthetic=true`, evidence-tier **anecdotal** — a label, not
a blocker). Live corpus columns (C5 trims/load, C6 Mode $06/MAF) are used AS LIVE for neighbours and
collision checks — that is the point of re-baselining. Cases the seed cannot ground stay abstained.
The 11 C4 cases: CSV-129, CSV-130, EXT-238, EXT-239, PDF-HI-007, TC-048, YAML-CSV95, CASE-020,
CASE-022, EXT-211, EXT-212.
### Success criteria ###
Produce `v3/reports/V3_C4_SIGNAL_DRYRUN_REBASE_<date>.{md,json}`:
1. **Zero-overlay self-check first:** drift=0 vs `apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json`
   across all 294. A non-zero drift = stop, report, do not proceed (the C4A lesson, enforced).
2. Producer simulation per case (ΔSTFT idle→2500 emit rule per value4.1) + scenario ladder
   (Scenario 1 shared-columns-only; Scenario 2 + C4-distinct seed columns) — which subset is
   load-bearing NOW.
3. Consumer overlay under live shim guard semantics (§2 above); full-294 sim.
4. **FT-8 neighbour union re-derived LIVE** from `exhaust_leak.json` + `lean_condition.json` +
   `sensor_fault.json` `passes_cases` (post-C5B state — the union has changed since C4A's 35).
   Regressions listed; target empty; currently-passing neighbours broken out.
5. Yield + masked split + column-add table (§Goal 1/3/4). Delta-vs-C4A section: what changed and why.
6. **Commit scope for C4B, sized not guessed:** exact gates, boost/prune deltas, column set,
   and the add-column recommendation with per-case evidence.
- Adapt `v3/c4_signal_sim.py` (new file `v3/c4_signal_sim_rebase.py` or a `--baseline` flag —
  smallest diff wins; py_compile+ruff+pyright clean; keep the original runnable).
- No engine/lab/registry/corpus/scorer/`run_suite.py`/yardstick edit; MARGIN unchanged (0.02);
  `Vault/` untouched; scoreboard `score` still `top3_family 250/294`, `Hash lock: ok`.
### Context ###
- Original dry-run + its report: `T-V3-P4-C4A` / `v3/reports/V3_C4_SIGNAL_DRYRUN_2026-07-05.{md,json}`.
- Seed bands: `v3/reports/V3_C4_SYNTH_BANDS_2026-07-05.md`. Contract: acq-spec §C4 (no new column ask).
- Live guards: registry shim (`labs/comlab/registry/integration_shim.py`) — read, don't edit.
- Baseline: `apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json`; ruler `V3_YARDSTICK_2026-07-06-C5B`.
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
The owner (C4B go/no-go + add-column decision) and `T-V3-P4-C4B` (commit sizing).
### Disclosure ###
Surface, don't hide: ALREADY_PASS conversions; guard conflicts; masked flips; any case where the
re-baseline REDUCES yield vs C4A — that is the finding, not a failure.
### Progress hook ###
Ledger T-V3-P4-C4A-R → done; dual-gate note `progress_notes/T-V3-P4-C4A-R.md`.
### Depends on ###
T-V3-P4-C5B done (live columns + guards) · T-V3-P4-C4-SYNTH done (seed). Runnable now.
