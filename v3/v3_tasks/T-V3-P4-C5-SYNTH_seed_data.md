### Goal ###
Produce the **provisional synthetic C5 seed**: for each of the 10 C5 cases, seed the 11 acq-spec §C5
columns (`stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, stft_load_pct, ltft_load_pct,
calc_load_wot_pct, maf_gps_idle, maf_gps_2500, fuel_rail_pressure_load_kpa, wideband_lambda_wot`)
with **research-grounded, web-corroborated, tolerance-wide** values derived from each case's
**oracle fault** — `synthetic=true`, side file under `v3/data/`. Per the contract §5 column audit:
6 of the 11 are already live schema (4 trims from C2B, 2 MAF from C6B) but **empty for C5 rows** —
the seed covers **ALL 11** columns on the 10 C5 rows; `C5B` adds only the new 5 to the schema.
Policy: `4DLab_CLAUDE.md` §Provisional synthetic signals. Does **not** wire or score —
`T-V3-P4-C5A` simulates on this seed; `C5B` commits.
### Policy (mirror C3/C6-SYNTH; full mechanics in the wired-signal-pack skill) ###
1. **Grounded, not gamed:** the oracle mix is uniform at family level (`{'lean_condition': 10}`),
   so `expected_fault_family` discriminates NOTHING here — key on **`expected_fault_code`**:
   **6 × `ERR-LC-001` (vacuum_leak_post_maf)** + **4 × `ERR-LC-005` (egr_stuck_open)**. Answer key
   only — **no back-solve** from LC/VL/EL rules, MF-001's current win, or current ranks.
2. **Tolerance-wide + grounding-tagged (contract §9, not laundered):** ΔTFT idle→2500 recovery =
   **empirical** (direction strong; the +15%/+10% figures are provisional, NOT fail lines — seed
   the direction robustly with wide spread, never knife-edge); 35 kPa WOT rail-pressure drop =
   **manufacturer-typical** (port-injection typical; DI rails run higher targets — state per-case
   architecture); WOT calc load < 80% = **manufacturer-typical / empirical-inferred** (altitude
   variance — seed shortfalls robustly beyond the bound); WOT wideband lambda > 1.05 =
   **standardized**. State all of this in the manifest.
3. **EGR-lookalike honesty (contract §8):** `CSV-113, CSV-114, REAL-004, era1_001` are
   `ERR-LC-005` EGR-stuck-open, currently winning `misfire/MF-001`. EGR-stuck-open is **not one of
   the three C5 emit paths** (VACUUM_LEAK_TRIM_PATTERN / FUEL_DELIVERY_SHORTFALL / MAF_UNDERREAD).
   Decide their band from research (`cluster5.md` confusable-set + separation-mechanism sections),
   not from the desire to bank them: if the dynamic trim pattern cannot separate EGR-stuck-open
   from a vacuum leak **with cited grounds**, they join **stay-abstained**, honestly. Banking the
   right family via the wrong sub-cause signature is a back-solve — do not do it.
4. **Architecture honesty (C6-PRE §7 precedent):** a case modeled as speed-density gets MAF columns
   **empty (None)**; a case whose rail-pressure PID is absent (Tier C mechanical gauge) gets
   `fuel_rail_pressure_load_kpa` None; wideband-vs-switching applicability stated per case. State
   per case which sub-signal carries it. **Static-only seeding is forbidden** — every separable
   case must carry the multi-point dynamics its gate needs, or stay abstained (contract §10:
   single warm-idle trim point → abstain at MARGIN=0.02).
5. **C6-MAF-collision guard (contract §4):** `maf_gps_idle/2500` are shared with C6. Any MAF
   values seeded on C5 rows must **not** clear C6's `SensorDynamicsState` sensor-attribution gates
   (which require Mode $06 / O2-dynamics evidence these rows don't carry) — C5's MAF_UNDERREAD
   requires the trim+load pattern; neither producer fires on MAF delta alone; C5 precedence when
   both present. Add an assert-style self-check for this on all 10 rows.
6. **C3 interaction (contract §6):** no C3 control-reference columns touched; C3 prune precedence
   is C5B's implementation concern, but the seed must not create static-only evidence patterns.
7. **Web-corroborated + labelled + correctable:** field-reported trim levels for post-MAF vacuum
   leaks (idle vs 2500), EGR-stuck-open trim/idle behaviour, WOT rail-pressure-drop and lambda
   enrichment norms, WOT calculated-load norms; cite every source; prefer the wider spread.
   `synthetic=true` manifest keyed case_id + column + band_id + grounding_tag + citation;
   synthetic-vs-real scoreboard split preserved.
### Success criteria ###
1. `v3/reports/V3_C5_SYNTH_BANDS_2026-07-06.md` — per column: contract band, web-reported range
   (citations), final tolerance-wide band + spread; bands stated per oracle sub-code group
   (ERR-LC-001 vs ERR-LC-005) AND per emit path (VACUUM_LEAK_TRIM_PATTERN vs
   FUEL_DELIVERY_SHORTFALL vs MAF_UNDERREAD vs stay-abstained).
2. `v3/data/c5_synthetic_seed_2026-07-06.{csv,json}` — 10/10 seeded; every value inside the band
   for **its own** oracle sub-code across the stated spread; all 11 columns addressed per case
   (value or None-with-stated-reason).
3. **Separability split disclosed:** N C5-separable vs M stay-abstained = 10. The 4 EGR cases'
   treatment stated with research grounds (see Policy 3); `era3_015` (TUNABLE_HELD, PCV
   pressure-sensor drift per contract §8) disclosed explicitly whichever side it lands.
4. **No back-solve audit:** generator inputs = oracle sub-code + band table only; assert-style
   self-check that separable cases clear their designed gate across the whole band, stay-abstained
   cases clear none, and no C5 row clears a C6 sensor gate (Policy 5).
5. Deterministic generator (`v3/gen_c5_synth_seed.py`): rerun byte-identical. Side file only; live
   corpus/engine/rules/yardstick untouched. `py_compile`+`ruff`+`pyright` clean.
### Context ###
- Bands/gates/case split/collision/FT-8: `v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.{md,json}`
  (READ FIRST — §2 producer table, §4 C6-MAF collision, §5 column audit, §6 case split + oracle
  mix + C3 note, §8 confounders + per-case mimic risk, §9 grounding, §10 abstain fallback).
- Research (READ-NARROW): `v3/research/research_answers/cluster5.md` — the line ranges the
  contract cites (~127–141 gates, 155–159, 166) plus §Confusable Set (line ~37) and §Fault
  Separation mechanisms (lines ~77–83) for the EGR/speed-density decisions.
- Column contract + abstain rule: `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md` §C5 (line 13, §C5
  block at line 46; C4-shared-column note lines 106–112).
- Generator pattern: `v3/gen_c3_synth_seed.py` (oracle-code keying, deterministic PRNG per
  case_id, stay-abstained handling) + `v3/gen_c6_synth_seed.py` (None-column architecture
  handling, manifest schema).
- The 10 cases (contract §6): EXP-N011, EXP-N022, EXP-N029, case_003, case_016
  (DATA_GAP_ACQUISITION_GAP) | CSV-113, CSV-114, REAL-004, era1_001 (OUTRANKED_HARD, all
  ERR-LC-005) | era3_015 (TUNABLE_HELD). Sub-code mix: 6 ERR-LC-001 + 4 ERR-LC-005.
- Dual target+neighbour (contract §7): `EXP-N011, case_003` — their seeds also move them as FT-8
  neighbours of LC rules; disclose, don't special-case.
- Web research: `WebSearch`/`web_fetch`; cite each source.
- Baseline (unchanged by this task): `V3_YARDSTICK_2026-07-05-C6B` / `POST_T_V3_P4_C6B`
  (csv `bf739368…`, oracle `3088a7c3…`). **If anything commits first, STOP and re-pin.**
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** `T-V3-P4-C5A` (in-memory dry-run) and `C5B` (commit, owner-sign-off-gated). No
  engine field/state added — wiring is C5B's diff per contract §3 (LC-001/002/003, VL-001/002/003,
  EL-001 evidence fields; C6-collision rule + C3-prune precedence land in
  `integration_shim.py::_score_rule` after the C3 and C6 branches).
### Disclosure ###
Surface, don't hide: the 4 EGR lookalikes' band decision and its grounds; sub-causes the trim
pattern cannot separate; every manufacturer-typical limit (35 kPa, 80%) seeded wide with the
variance risk stated; speed-density / Tier-C / wideband architecture choices per case; era3_015's
TUNABLE_HELD status; the FT-8 union (68 neighbours) this seed will later expose at C5A/C5B. Never
present synthetic-seeded passes as real accuracy.
### Deliverables ###
1. `v3/reports/V3_C5_SYNTH_BANDS_2026-07-06.md` — CREATE. Bands + web corroboration + cites + split.
2. `v3/data/c5_synthetic_seed_2026-07-06.csv` — CREATE. 10 cases × 11 columns, `synthetic=true`.
3. `v3/data/c5_synthetic_seed_2026-07-06.json` — CREATE. Manifest (values, band_id, tag, citation).
4. `v3/gen_c5_synth_seed.py` — CREATE. Deterministic generator.
### Files to touch ###
- `v3/reports/V3_C5_SYNTH_BANDS_2026-07-06.md` (CREATE)
- `v3/data/c5_synthetic_seed_2026-07-06.csv` (CREATE)
- `v3/data/c5_synthetic_seed_2026-07-06.json` (CREATE)
- `v3/gen_c5_synth_seed.py` (CREATE)
### Out of scope ###
**No write into the live corpus; no engine/lab/registry/shim edit; no back-solving; no abstain-dial
change.** No C3 or C6 column/state logic touch (the collision + precedence rules are implemented at
C5B, not here). No schema addition (C5B adds the 5 new columns). Writes only under `v3/`. Never
`Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph rebuild. No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/gen_c5_synth_seed.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/gen_c5_synth_seed.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/gen_c5_synth_seed.py
/agent_workspace/.venv-wired/bin/python v3/gen_c5_synth_seed.py && /agent_workspace/.venv-wired/bin/python v3/gen_c5_synth_seed.py   # rerun byte-identical
grep -icE 'synthetic|band|citation|manufacturer|vacuum|EGR|lookalike|abstain|None|collision' v3/reports/V3_C5_SYNTH_BANDS_2026-07-06.md
git status --porcelain   # only new files under v3/
```
Gate: 10/10 seeded; split reconciles to 10; the 4 EGR cases' band decision research-grounded (or
stay-abstained); no C5 row clears a C6 sensor gate; None columns carry stated reasons; every band
cited + grounding-tagged; no consumer thresholds read; rerun byte-identical; live state untouched.
### Progress hook ###
PROGRESS.md `T-V3-P4-C5-SYNTH`: Status=done, Files changed=4 (new under v3/), Verification="10 C5
cases seeded across 11 columns (6 live-empty + 5 new), research+web-grounded (cited),
tolerance-wide, grounding-tagged, synthetic=true; separability split + EGR-lookalike decision
disclosed; C6-collision self-check green; no back-solve; side file only".
### Depends on ###
`T-V3-P4-C5-PRE` done ✓ (contract instanced, baseline pinned). Web access. **Unblocks
`T-V3-P4-C5A`** (dry-run w/ column-subset scenario ladder) → `C5B` (commit, owner-sign-off-gated).
