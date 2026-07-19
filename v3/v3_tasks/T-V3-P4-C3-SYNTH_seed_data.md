### Goal ###
Produce the **provisional synthetic C3 seed** that unblocks the C3 signal pack: for each of the 22 C3
cases, seed the acq-spec §C3 columns (`koeo_map_baro_delta_kpa, module_voltage_loaded_v,
dlc_signal_ground_drop_v, gas_obd_lambda_delta, lambda_perception_delta,
bidirectional_fuel_response_ok_bool`) with **research-grounded, web-corroborated, tolerance-wide**
values derived from each case's **oracle fault** — flagged `synthetic=true`, as a **side file** under
`v3/data/`. Policy: `4DLab_CLAUDE.md` §Provisional synthetic signals. It does **not** wire the
producer/consumer or score — `T-V3-P4-C3A` simulates on this seed; `C3B` commits.
### Policy (mirror T-V3-P4-C2-SYNTH; full mechanics in the wired-signal-pack skill) ###
1. **Grounded, not gamed:** values come from the oracle fault via the C3-PRE band table
   (control-fault case → divergence/ground-drop band; sensor-bias-presenting case → perception-delta
   band; non-C3-separable case → healthy/NA band + stay-abstained flag). **Never back-solve** from
   EF/SF rule thresholds or the case's current rank.
2. **Tolerance-wide, not lab-precise:** per-column band with realistic spread, stated in the report;
   values must sit in the correct band robustly across the whole spread.
3. **Web-corroborated:** research real-world reported ranges (ground-offset voltage drops, KOEO
   MAP-vs-BARO plausibility splits, gas-vs-OBD lambda divergence, trim-rail behaviour); widen/shift
   bands to field reality; cite every source.
4. **Grounding-strength tagged, not laundered:** Δλ ≥ 0.05 is **empirical-anecdotal** and the DMM
   voltage-drop limits are **standardized** — carry C3-PRE's per-threshold tags into the manifest.
   The bool column (`bidirectional_fuel_response_ok_bool`) is deterministic per fault, not sampled —
   state that.
5. **Labelled + correctable:** `synthetic=true` manifest keyed case_id + column + band_id + citation;
   synthetic-vs-real scoreboard split preserved downstream.
### Success criteria ###
1. `v3/reports/V3_C3_SYNTH_BANDS_2026-07-05.md` — per column: C3-PRE band, web-reported real-world
   range (with citations), final tolerance-wide band + spread; bands stated separately per oracle
   fault group.
2. `v3/data/c3_synthetic_seed_2026-07-05.{csv,json}` — all 22 cases seeded; manifest carries
   `synthetic=true, oracle_fault, band_id, grounding_tag, source_citation` per value; every value
   inside the band for **its own** oracle fault across the stated spread.
3. **Separability split disclosed:** N C3-separable vs M stay-abstained (mimic-risk cases from
   C3-PRE §confounders — exhaust-leak / severe-misfire lookalikes — are NOT seeded into a passing
   band). Reconcile N + M = 22.
4. **No back-solve audit:** generator inputs = oracle label + band table only; state that nothing is
   read from `ecu_fault.json`/`sensor_fault.json` thresholds or run results.
5. Deterministic generator (`v3/gen_c3_synth_seed.py`): rerun is byte-identical. Side file only —
   live corpus/engine/rules/yardstick untouched. `py_compile`+`ruff`+`pyright` clean.
### Context ###
- Bands + consumer map + case split + FT-8 union: `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.{md,json}`
  (T-V3-P4-C3-PRE output — READ THIS FIRST; it pins everything this task samples from).
- Research (READ-NARROW): `v3/research/research_answers/cluster3_prepped.md` signature table
  (~lines 183–188) + worked ground-offset example (~lines 83–97).
- Generator pattern to mirror: `v3/gen_c2_synth_seed.py` (oracle+band → sample; deterministic) and
  `v3/gen_c4_synth_seed.py` (grounding-tag handling for weak bands).
- Case list (22): CASE-039, CSV-041, CSV-045, CSV-123, CSV-124, CSV-125, CSV-126, ECU-001, ECU-009,
  EXP-N002, EXP-N004, EXP-N005, EXP-N018, EXP-N019, EXT-221, TC-021, YAML-CSV41, YAML-CSV45,
  YAML-RULE_NOx_1, YAML-TC47, case_001, case_013.
- Web research: `WebSearch`/`web_fetch`; cite each source in the bands report.
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** `T-V3-P4-C3A` (in-memory dry-run on this seed) and `C3B` (commit). No engine
  field/state added here — the producer/consumer wiring is C3B's diff, per the acq-spec §C3 contract.
### Disclosure ###
Surface, don't hide: bands where the web shows wider variance than the research answer (use the wider);
any case whose oracle fault makes the C3 signal non-separating (stay-abstained, named); the
empirical-anecdotal grounding of the Δλ threshold. Never present synthetic-seeded passes as real-world
accuracy — the manifest + scoreboard split keeps them distinguishable.
### Deliverables ###
1. `v3/reports/V3_C3_SYNTH_BANDS_2026-07-05.md` — CREATE. Bands + web corroboration + cites + split.
2. `v3/data/c3_synthetic_seed_2026-07-05.csv` — CREATE. 22 cases × C3 columns, `synthetic=true`.
3. `v3/data/c3_synthetic_seed_2026-07-05.json` — CREATE. Manifest (values, band_id, tag, citation).
4. `v3/gen_c3_synth_seed.py` — CREATE. Deterministic generator (oracle fault + band → values).
### Files to touch ###
- `v3/reports/V3_C3_SYNTH_BANDS_2026-07-05.md` (CREATE)
- `v3/data/c3_synthetic_seed_2026-07-05.csv` (CREATE)
- `v3/data/c3_synthetic_seed_2026-07-05.json` (CREATE)
- `v3/gen_c3_synth_seed.py` (CREATE)
### Out of scope ###
**No write into the live corpus** (`cases_petrol_v7.csv` / `corpus_curated.csv`) — corpus write +
wiring + re-score + yardstick mint are `C3B`. **No engine/lab/registry edit. No back-solving. No
abstain-dial change.** Writes only under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/
frozen-graph rebuild. No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/gen_c3_synth_seed.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/gen_c3_synth_seed.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/gen_c3_synth_seed.py
/agent_workspace/.venv-wired/bin/python v3/gen_c3_synth_seed.py && /agent_workspace/.venv-wired/bin/python v3/gen_c3_synth_seed.py   # rerun byte-identical
grep -icE 'synthetic|band|citation|anecdotal|standardized|abstain' v3/reports/V3_C3_SYNTH_BANDS_2026-07-05.md
git status --porcelain   # only new files under v3/
```
Gate: 22/22 seeded; every band cited; separability split reconciles to 22; generator provably reads no
consumer thresholds; rerun byte-identical; live corpus/yardstick untouched.
### Progress hook ###
PROGRESS.md `T-V3-P4-C3-SYNTH`: Status=done, Files changed=4 (new under v3/), Verification="22 C3
cases seeded, research-grounded + web-corroborated (cited), tolerance-wide, grounding-tagged,
synthetic=true; separability split disclosed; no back-solve; side file only".
### Depends on ###
`T-V3-P4-C3-PRE` done (bands, split, FT-8 union, baseline pin). Web access.
**Unblocks `T-V3-P4-C3A`** (dry-run, forward-registered) → `C3B` (commit, owner-sign-off-gated).
