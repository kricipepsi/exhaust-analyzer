### Goal ###
C3-pack PRE-AUTHOR DISCLOSURE (read-only). Instance the **frozen reveal contract**
(`V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md` — template already settled by T-V3-P4-C2-PRE; do NOT
re-derive it) for **C3 — ECU/control-system fault**, the next pack in the pinned sequence
(C2 → **C3** → C6 → C5 → C4 → C9 → C8 → C1 → C7). Output the C3 worked instance:
producer thresholds cited from `cluster3_prepped.md`, consumers named, the 22-case split, and the
FT-8 neighbour union derived live. **No engine/lab/registry/corpus edit; no producer/consumer wired;
no data synthesized.**
### Success criteria ###
Produce `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.md` (+ `.json`) with:
1. **C3 producer extraction (cited to `v3/research/research_answers/cluster3_prepped.md`, lines
   ~183–188 signature table):** Δλ = |λ_OBD − λ_tailpipe| ≥ 0.05 (grounding: **empirical-anecdotal —
   tag it**); LTFT railed ≥ +25% / ≤ −25% with un-correlated tailpipe chemistry; |P_MAP − P_BARO|
   ≥ 5 kPa at KOEO; DLC signal-ground drop > 0.20 V; ground joint > 0.10 V / wire > 0.20 V;
   active-override O2 delta < 0.1 V under ±25% fuel command. Map each to
   `ControlPlausibilityState` and the `CONTROL_REFERENCE_FAULT` emit condition (acq-spec §C3).
2. **Consumer mapping (named, no edit):** `labs/comlab/registry/rules/ecu_fault.json`
   EF-001/EF-002/EF-003, plus `sensor_fault.json` SF-001/SF-002 for dispersion-as-sensor-bias.
   Name the exact evidence field each would read.
3. **Per-case split reconciling to 22:** the 21 acq-spec §C3 rows (18 OUTRANKED_HARD +
   3 PRODUCER_GAP_SIGNAL_REQUIRED: CSV-125, CSV-126, YAML-RULE_NOx_1) + the CASE-039 overlay
   (rerouted from CLASSIFIER_FIXABLE by T-V3-P4-0A). BUILDABLE_NOW vs SCORING_GATED per case.
4. **FT-8 neighbour union derived LIVE** from `ecu_fault.json` + `sensor_fault.json` `passes_cases`
   across both competition groups (never reuse C2's list); name any case that is both C3 target and
   regression-sensitive neighbour.
5. **Confounder disclosure:** cluster3 §Conditions Under Which Signatures May Fail — upstream exhaust
   leaks and severe misfires mimic the control-fault signature. List which of the 22 cases' oracle
   faults are at mimic risk; those are stay-abstained candidates for C3-SYNTH.
6. **Grounding-strength table per threshold** (empirical-anecdotal vs manufacturer-typical vs
   standardized) — weakest-grounded thresholds flagged as producer-tuning risk, not firm constants.
7. **Baseline pinned:** `V3_YARDSTICK_2026-07-05` (csv `3df2e8cb…`, oracle `3088a7c3…`), run
   `apps/wired/v7/runs/POST_T_V3_P4_C2B/results.json`. All sizing in this pack references THIS
   baseline (the C4A dry-run predates C2B and is known-stale — do not copy its numbers).
8. Read-only: `py_compile`+`ruff`+`pyright` clean on any helper; corpus/yardstick/score untouched.
### Context ###
- Research (READ-NARROW): `v3/research/research_answers/cluster3_prepped.md` — signature table
  (~lines 183–188), pre-gate (~line 141), confounders section. Use the **prepped** file; the raw
  `cluster3.md` table is corrupted (thresholds dropped — see `cluster3_PREP_REPORT.md`).
- Contract drafted: `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md §C3` (column contract:
  `koeo_map_baro_delta_kpa, module_voltage_loaded_v, dlc_signal_ground_drop_v, gas_obd_lambda_delta,
  lambda_perception_delta, bidirectional_fuel_response_ok_bool`).
- Ordering + case counts: `V3_MIN_SIGNAL_SET_2026-07-01.md` (C3 = rank 2, 22 with CASE-039;
  action A5 bundle is full-unlock for all 22).
- Worked instance to mirror: the C2 sections of `V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md`;
  extractor pattern `v3/build_reveal_contract.py` (extend if it has cluster-agnostic hooks, else
  CREATE `v3/build_c3_contract.py` — do not fork shared logic silently).
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** the owner (decides C3-SYNTH go/no-go and the stay-abstained set) and
  `T-V3-P4-C3-SYNTH`/`C3A`/`C3B` (inherit bands, consumer map, FT-8 union, baseline pin).
  No engine field/state added here.
### Disclosure ###
Surface, don't hide: thresholds whose grounding is empirical-anecdotal; cases whose oracle fault the
C3 signal cannot separate (mimic risk); any consumer rule shared with non-C3 neighbours; the stale
C4A baseline warning. Tier output essential-first (headline split → per-threshold table → per-case
JSON).
### Deliverables ###
1. `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.md` — CREATE. C3 instance of the frozen template.
2. `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.json` — CREATE. Machine-readable map + case split.
3. `v3/build_c3_contract.py` — CREATE (or surgical extension of `build_reveal_contract.py`).
### Files to touch ###
- `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.md` (CREATE)
- `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.json` (CREATE)
- `v3/build_c3_contract.py` (CREATE) or `v3/build_reveal_contract.py` (MODIFY, surgical)
### Out of scope ###
**No producer/consumer wired. No corpus column. No rule/weight edit. No re-score, no yardstick mint.
No synthesized values** (that is C3-SYNTH). No re-freezing/re-writing the contract TEMPLATE — instance
only. No abstain-dial change (MARGIN=0.02). Writes only under `v3/`. Never `Vault/`. GRAPH GUARDRAIL:
no `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/build_c3_contract.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/build_c3_contract.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/build_c3_contract.py
grep -cE 'EF-00[123]|SF-00[12]|0\.05|5 kPa|0\.20 V|0\.10 V|anecdotal|CASE-039' v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.md
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score   # unchanged: top3_family 212/294, Hash lock: ok
git status --porcelain   # only new files under v3/
```
Gate: 22/22 cases attributed; FT-8 union derived live with the derivation shown; every threshold
carries a grounding tag; baseline pin present; score unchanged.
### Progress hook ###
PROGRESS.md `T-V3-P4-C3-PRE`: Status=done, Files changed=3 (new under v3/), Verification="C3 reveal
contract instanced: thresholds cited+grounding-tagged, EF/SF consumers named, 22-case split
reconciled, FT-8 union derived live, baseline pinned POST_T_V3_P4_C2B; read-only, score unchanged".
### Depends on ###
Nothing pending — runnable now. **Unblocks `T-V3-P4-C3-SYNTH`.**
