### Goal ###
Produce the **provisional synthetic C6 seed**: for each of the 14 C6 cases, seed the 9 acq-spec §C6
columns (`mode06_o2_response_margin_pct, o2_rich_to_lean_ms, o2_lean_to_rich_ms,
maf_actual_calc_delta_pct_idle, maf_actual_calc_delta_pct_2500, maf_gps_idle, maf_gps_2500,
calc_airflow_gps_idle, calc_airflow_gps_2500`) with **research-grounded, web-corroborated,
tolerance-wide** values derived from each case's **oracle fault** — `synthetic=true`, side file under
`v3/data/`. Policy: `4DLab_CLAUDE.md` §Provisional synthetic signals. Does **not** wire or score —
`T-V3-P4-C6A` simulates on this seed; `C6B` commits.
### Policy (mirror C3-SYNTH; full mechanics in the wired-signal-pack skill) ###
1. **Grounded, not gamed:** values come from the oracle label via the C6-PRE band table. The C3-SYNTH
   precedent applies: if `expected_fault_family` alone cannot discriminate sub-bands (13 of 14 are
   `sensor_fault`), key on the finer **`expected_fault_code`** — answer key, never consumer
   thresholds. **No back-solve** from SF/NF rules or current ranks.
2. **Tolerance-wide + grounding-tagged (C6-PRE §8, not laundered):** Mode $06 margin =
   standardized-transport but the numeric limit is **manufacturer-specific** (seed the margin
   RELATIVE to the vehicle limit, wide spread); O2 response times = **manufacturer-typical** —
   direction strong, the 849 ms / <150 ms figures are examples, NOT universal fail lines (state
   this in the manifest); MAF underread 10–15% = **empirical-inferred** (seed shortfalls robustly
   beyond 15% at BOTH points, not knife-edge at 10%).
3. **Architecture honesty (C6-PRE §7):** a case modeled as MAF-less/speed-density gets MAF columns
   **empty (None)**, not invented values — its band must be decided by O2 dynamics or stay-abstained.
   Same for wideband-vs-switching applicability. State per case which sub-signal carries it.
4. **Web-corroborated:** field-reported Mode $06 O2 monitor margins, O2 response-time ranges
   (healthy vs lazy), MAF gram-per-second idle/2500 norms and underread behaviour; cite every source;
   prefer the wider spread.
5. **Labelled + correctable:** `synthetic=true` manifest keyed case_id + column + band_id +
   grounding_tag + citation; synthetic-vs-real scoreboard split preserved.
### Success criteria ###
1. `v3/reports/V3_C6_SYNTH_BANDS_2026-07-05.md` — per column: C6-PRE band, web-reported range
   (citations), final tolerance-wide band + spread; bands stated per oracle sub-fault group AND per
   emit path (O2_LAZY_OR_BIASED vs MAF_UNDERREAD).
2. `v3/data/c6_synthetic_seed_2026-07-05.{csv,json}` — 14/14 seeded; every value inside the band for
   **its own** oracle fault across the stated spread; MAF-less cases carry None MAF columns.
3. **Separability split disclosed:** N C6-separable vs M stay-abstained = 14. **`PDF-4G-05` is a
   named lookalike (oracle `misfire`, engine currently says sensor_fault)** — it MUST be seeded
   below every C6 gate (healthy dynamics), never into a sensor pass; C6's job for it is to STOP
   supporting the wrong sensor verdict, not to bank it. Any other sub-code the dynamics cannot
   separate joins stay-abstained, honestly.
4. **No back-solve audit:** generator inputs = oracle label + band table only; assert-style
   self-check that separable cases clear their designed gate across the whole band and stay-abstained
   cases clear none.
5. Deterministic generator (`v3/gen_c6_synth_seed.py`): rerun byte-identical. Side file only; live
   corpus/engine/rules/yardstick untouched. `py_compile`+`ruff`+`pyright` clean.
### Context ###
- Bands/gates/case split/interaction/FT-8: `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.{md,json}`
  (READ FIRST — §2 producer table, §5 case split + oracle mix, §7 confounders, §8 grounding).
- Research (READ-NARROW): `v3/research/research_answers/cluster6.md` §Question One/Three/Four
  Answers + §Candidate Signature Table (lines ~110–174, as cited by the contract).
- Generator pattern: `v3/gen_c3_synth_seed.py` (oracle-code keying, deterministic PRNG per case_id,
  stay-abstained handling) + `v3/gen_c6...` follows its manifest schema.
- The 14 cases (contract §5): CASE-045, CASE-048, YAML-TC46 | CASE-014, EXT-229, EXT-230,
  YAML-CSV25, case_046, era1_006 | CSV-025, EXP-N020, PDF-4G-05, TC-046, era2_012.
  Oracle mix: 13 sensor_fault (sub-codes discriminate) + 1 misfire (PDF-4G-05).
- Web research: `WebSearch`/`web_fetch`; cite each source.
- Baseline (unchanged by this task): `V3_YARDSTICK_2026-07-05-C3B` / `POST_T_V3_P4_C3B`.
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** `T-V3-P4-C6A` (in-memory dry-run) and `C6B` (commit). No engine field/state added —
  wiring is C6B's diff per the contract §3 map (SF-005/008 boost, SF-001/002 bias path, NF-001/002
  healthy split, C3-prune precedence per contract §4).
### Disclosure ###
Surface, don't hide: sub-codes the dynamics cannot separate; every manufacturer-specific limit seeded
as a relative margin (say so); the non-universal ms thresholds; MAF-less/wideband architecture choices
per case; PDF-4G-05's lookalike handling. Never present synthetic-seeded passes as real accuracy.
### Deliverables ###
1. `v3/reports/V3_C6_SYNTH_BANDS_2026-07-05.md` — CREATE. Bands + web corroboration + cites + split.
2. `v3/data/c6_synthetic_seed_2026-07-05.csv` — CREATE. 14 cases × 9 columns, `synthetic=true`.
3. `v3/data/c6_synthetic_seed_2026-07-05.json` — CREATE. Manifest (values, band_id, tag, citation).
4. `v3/gen_c6_synth_seed.py` — CREATE. Deterministic generator.
### Files to touch ###
- `v3/reports/V3_C6_SYNTH_BANDS_2026-07-05.md` (CREATE)
- `v3/data/c6_synthetic_seed_2026-07-05.csv` (CREATE)
- `v3/data/c6_synthetic_seed_2026-07-05.json` (CREATE)
- `v3/gen_c6_synth_seed.py` (CREATE)
### Out of scope ###
**No write into the live corpus; no engine/lab/registry/shim edit; no back-solving; no abstain-dial
change.** No C3 column or C3-state logic touch (the interaction rule is implemented at C6B, not
here). Writes only under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph rebuild.
No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/gen_c6_synth_seed.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/gen_c6_synth_seed.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/gen_c6_synth_seed.py
/agent_workspace/.venv-wired/bin/python v3/gen_c6_synth_seed.py && /agent_workspace/.venv-wired/bin/python v3/gen_c6_synth_seed.py   # rerun byte-identical
grep -icE 'synthetic|band|citation|manufacturer|underread|lookalike|abstain|None' v3/reports/V3_C6_SYNTH_BANDS_2026-07-05.md
git status --porcelain   # only new files under v3/
```
Gate: 14/14 seeded; split reconciles to 14; PDF-4G-05 below every gate; MAF-less cases carry None;
every band cited + grounding-tagged; no consumer thresholds read; rerun byte-identical; live state
untouched.
### Progress hook ###
PROGRESS.md `T-V3-P4-C6-SYNTH`: Status=done, Files changed=4 (new under v3/), Verification="14 C6
cases seeded, research+web-grounded (cited), tolerance-wide, grounding-tagged, synthetic=true;
separability split disclosed; PDF-4G-05 lookalike honest; no back-solve; side file only".
### Depends on ###
`T-V3-P4-C6-PRE` done ✓. Web access. **Unblocks `T-V3-P4-C6A`** (dry-run w/ column-subset scenario
ladder) → `C6B` (commit, owner-sign-off-gated).
