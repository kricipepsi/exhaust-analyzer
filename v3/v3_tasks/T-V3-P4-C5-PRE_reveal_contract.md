### Goal ###
C5-pack PRE-AUTHOR DISCLOSURE (read-only). Instance the **frozen reveal contract** for **C5 —
lean-condition root cause**, next in the pinned sequence (C2 ✓ → C3 ✓ → C6 ✓ → **C5** → C4 → C9 →
C8 → C1 → C7). Output the C5 worked instance: producer thresholds cited from `cluster5.md`,
consumers named, the 10-case split, the FT-8 union derived live, and two pack-specific audits —
the **already-live-column audit** (C2B/C6B landed part of C5's contract) and the **C6-MAF-collision
disclosure** (both producers can emit a MAF-underread verdict from the same columns). **No
engine/lab/registry/corpus edit; no wiring; no data synthesized.**
### Success criteria ###
Produce `v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.md` (+ `.json`) with:
1. **C5 producer extraction (cited):** from `cluster5.md` §Multi-Point Diagnostic Acquisition
   Protocol / Signal Evaluation (grep anchors, cite lines), the OBDLab `LeanRootCauseState` emit
   gates per acq-spec §C5.3 — `VACUUM_LEAK_TRIM_PATTERN` (positive trims at idle that RECOVER at
   2500), `FUEL_DELIVERY_SHORTFALL` (lean worsens under load; rail pressure drop > 35 kPa),
   `MAF_UNDERREAD` (peak calculated load < 80% with positive trims). **Grounding-strength tag per
   threshold** (the 35 kPa and 80% literals: manufacturer-typical vs empirical — say which).
2. **ALREADY-LIVE-COLUMN AUDIT (new, mandatory):** of the 11 acq-spec §C5 columns, verify against
   the live CSV header which already exist — expected: the 4 trim columns (C2B) and
   `maf_gps_idle`/`maf_gps_2500` (C6B) are live schema; the genuinely NEW ask is
   `stft_load_pct, ltft_load_pct, calc_load_wot_pct, fuel_rail_pressure_load_kpa,
   wideband_lambda_wot` (5). State per column: live-schema-empty-for-C5-rows vs new. C5-SYNTH seeds
   values for ALL contract columns on the 10 C5 rows; C5B adds only the new 5 to the schema.
3. **C6-MAF-COLLISION DISCLOSURE (new, mandatory):** C6's `SensorDynamicsState` and C5's
   `LeanRootCauseState` can both emit a MAF-underread verdict from the same MAF columns — one
   attributes it to sensor_fault, the other to a lean root cause. Populations are disjoint today
   (14 C6 rows vs 10 C5 rows); state the disambiguation rule C5B must implement (e.g. C6's
   sensor-attribution requires its Mode $06/dynamics evidence; C5's requires the trim+load pattern;
   neither fires on MAF delta alone) and where it lands in `integration_shim.py::_score_rule`
   relative to the C3 and C6 branches. Surface it now; do not let C5B discover it.
4. **Consumer mapping (named, no edit):** `lean_condition.json` LC-001/LC-002/LC-003; state whether
   `vacuum_leak.json` VL-001/002/003 reads `VACUUM_LEAK_TRIM_PATTERN` (the state separates
   lean sub-causes — check which family the corpus oracles actually expect for the 10 cases) and
   the C4 note (EL-001 consumes the shared trims later). Exact evidence field per rule.
5. **Per-case split reconciling to 10:** EXP-N011, EXP-N022, EXP-N029, case_003, case_016
   (DATA_GAP_ACQUISITION_GAP=5); CSV-113, CSV-114, REAL-004, era1_001 (OUTRANKED_HARD=4); era3_015
   (TUNABLE_HELD=1). Oracle-fault mix disclosed (drives the SYNTH separability split; flag
   lookalikes — the C4 exhaust-leak/true-lean collision cases are NOT in this 10 but share columns).
6. **FT-8 neighbour union derived LIVE** from `lean_condition.json` (+ `vacuum_leak.json` if mapped)
   `passes_cases`, both competition groups; dual target+neighbour cases named. Note prior packs'
   sims boosted LC rules for OTHER clusters' cases (C3 lean-bias winners include LC-001/LC-002) —
   the union must include those now-passing rows.
7. **Abstain fallback stated:** single warm-idle trim point only → abstain (acq-spec §C5.6).
8. **Baseline pinned:** `V3_YARDSTICK_2026-07-05-C6B` (csv `bf739368…`, oracle `3088a7c3…`), run
   `apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json`. If anything commits first, STOP and re-pin.
9. Read-only: extractor `py_compile`+`ruff`+`pyright` clean; score unchanged (`top3_family` 241/294,
   `Hash lock: ok`).
### Context ###
- Research (READ-NARROW): `v3/research/research_answers/cluster5.md` — grep the §Multi-Point /
  §Signal Evaluation anchors; cite line ranges. If tables are corrupted (raw-cluster3 pattern),
  STOP and surface; no hand-repair.
- Column contract + case list: `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md §C5` (11 columns, gates,
  abstain rule).
- Live schema to audit: `apps/wired/v7/data/cases_petrol_v7.csv` header (read the header row only).
- Worked instance to mirror: `V3_C6_REVEAL_CONTRACT_2026-07-05.{md,json}` + `v3/build_c6_contract.py`
  (adapt; the interaction-disclosure section format is the C6 §4 precedent).
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** the owner (C5-SYNTH go/no-go + stay-abstained set) and `T-V3-P4-C5-SYNTH`/`C5A`/`C5B`
  (inherit bands, column audit, collision rule, FT-8 union, baseline pin). No engine field/state
  added here.
### Disclosure ###
Surface, don't hide: which C5 columns are already live schema (the ask shrank — say by how much);
the C6-MAF collision rule; LC-rule neighbour exposure from prior packs' commits; weakly-grounded
literals (35 kPa, 80%); oracle lookalikes → stay-abstained candidates; any corrupted research table.
Tier essential-first (headline split → threshold/audit tables → per-case JSON).
### Deliverables ###
1. `v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.md` — CREATE. C5 instance incl. the two new audits.
2. `v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.json` — CREATE. Machine-readable map + case split.
3. `v3/build_c5_contract.py` — CREATE (adapt `build_c6_contract.py`; no silent forks of shared logic).
### Files to touch ###
- `v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.md` (CREATE)
- `v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.json` (CREATE)
- `v3/build_c5_contract.py` (CREATE)
### Out of scope ###
**No producer/consumer wired. No corpus column or value. No rule/weight/shim edit. No re-score, no
yardstick mint. No synthesized values** (C5-SYNTH). No template re-derivation. No abstain-dial change
(MARGIN=0.02). Writes only under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph
rebuild. `run_suite.py` untouched. No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/build_c5_contract.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/build_c5_contract.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/build_c5_contract.py
head -1 apps/wired/v7/data/cases_petrol_v7.csv | tr ',' '\n' | grep -cE 'stft|ltft|maf_gps'   # column audit ground truth
grep -cE 'LC-00[123]|VACUUM_LEAK_TRIM_PATTERN|FUEL_DELIVERY_SHORTFALL|MAF_UNDERREAD|collision|already-live|35 kPa|80' v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.md
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score   # unchanged: top3_family 241/294, Hash lock: ok
git status --porcelain   # only new files under v3/
```
Gate: 10/10 attributed; column audit matches the live header; collision rule stated with its shim
location; FT-8 union live-derived incl. prior-pack LC exposure; thresholds grounding-tagged;
baseline pin present; score unchanged.
### Progress hook ###
PROGRESS.md `T-V3-P4-C5-PRE`: Status=done, Files changed=3 (new under v3/), Verification="C5 reveal
contract instanced: LeanRootCauseState gates cited+tagged, LC consumers named, already-live-column
audit (ask shrank to 5 new), C6-MAF collision rule stated, 10-case split reconciled, FT-8 live,
baseline POST_T_V3_P4_C6B; read-only, score unchanged".
### Depends on ###
`T-V3-P4-C6B` done ✓ (MAF columns live; new baseline minted). Runnable now. **Unblocks
`T-V3-P4-C5-SYNTH`** → `C5A` → `C5B` (forward-registered). After C5B: **C4B re-baseline** becomes
fully unblocked (both its shared-column dependencies live).
