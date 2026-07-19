### Goal ###
Produce the **provisional synthetic C2 data** that unblocks the C2 signal pack: for each of the 22 C2
cases, seed the required columns (`stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct,
mode06_catalyst_margin_pct, catalyst_index_ratio`, + optional pre/post-cat deltas) with
**research-grounded, web-corroborated, tolerance-wide** values derived from each case's **oracle
fault** — flagged `synthetic=true`. This replaces the old "owner supplies real data" gate under the
new provisional-synthetic policy (`4DLab_CLAUDE.md` §Provisional synthetic signals). It does **not**
wire the producer/consumer or score — it produces the labelled data column that `T-V3-P4-C2A`
(dry-run) then simulates and `C2B` commits.

### Policy this task operationalizes (read `4DLab_CLAUDE.md` §Provisional synthetic signals first) ###
1. **Grounded, not gamed:** each value comes from the case's oracle fault via the `cluster2.md`
   signature (rich case → trim in the rich band; catalyst_failure → ~zero trim + failed index), per
   the reveal contract's C2 producer table. **Never back-solve from the consumer rule to force a
   pass.**
2. **Tolerance-wide, not lab-precise:** sample each value from a **band with realistic spread**, not
   a point — real cars vary. State the exact band + spread used per column. The value must land in
   the correct research band for the case's fault **robustly under that spread** (not on a knife-edge).
3. **Web-corroborated before commit:** for each C2 signature band, run web research on real-world
   reported values (documented STFT/LTFT ranges for rich fueling; Mode $06 catalyst index / OSC for
   failed vs healthy cats; decel-sweep CO), and **widen/shift the band to match field reality**;
   cite sources. Prefer the wider spread where the web shows more variance than `cluster2.md`.
4. **Labeled + tracked:** every seeded value carries `synthetic=true` provenance (a manifest keyed by
   case_id + column + source band + citation); downstream scoring keeps a synthetic-vs-real split.
5. **Correctable:** the manifest makes every synthetic value findable for replacement when real user
   data lands post-launch.

### Success criteria ###
1. **Web-corroboration report** `v3/reports/V3_C2_SYNTH_BANDS_2026-07-01.md`: per C2 column, the
   `cluster2.md` band, the real-world reported range found via web research (with **citations**), and
   the final tolerance-wide band used (= max realistic spread of the two). Rich vs catalyst_failure
   bands stated separately.
2. **Seeded data + manifest** `v3/data/c2_synthetic_seed_2026-07-01.{csv,json}`: for all 22 C2 cases,
   the sampled column values + `synthetic=true`, `oracle_fault`, `band_id`, `source_citation`. Values
   reconcile: every case's values sit inside the band for **its own** oracle fault.
3. **No back-solve audit:** the generator keys only on `oracle_fault` + the web-validated band — it
   must **not** read the consumer rule thresholds or the case's current rank. State this in the report
   (the generator's inputs are the oracle label + band table, nothing from `rich_mixture.json`/
   `catalyst_failure.json`).
4. **Tolerance width stated:** the report names the spread (e.g. STFT rich band `-18%…-10%`, σ≈…) and
   shows that a case passes the research band across the **whole** spread, not just at the mean.
5. **Reconciliation:** 22/22 cases seeded; each value's band matches its oracle fault; 0 values
   sourced from the consumer rule. Does **not** touch the live corpus, engine, rules, or yardstick —
   the seed is a **side file** consumed by `C2A`/`C2B`, not written into `cases_petrol_v7.csv` here.
6. `py_compile`+`ruff`+`pyright` clean on the generator.

### Disclosure (what this task must surface, not hide) ###
If web research shows a fault's real-world range is **wider or shifted** vs `cluster2.md`, report the
gap and use the field-realistic band (that is the point of step 3). If any C2 case's oracle fault is
**not** cleanly rich_mixture-vs-catalyst_failure (e.g. an outranked case whose true family is a third
thing), flag it — a synthetic C2 trim/index only helps cases whose ground truth is separable by the
C2 signal; others stay abstained. Never present synthetic-seeded passes as real-world accuracy; the
manifest + scoreboard split must keep them distinguishable.

### Context ###
- Reveal contract (C2 producer bands + consumer map + FT-8 neighbours): `T-V3-P4-C2-PRE` outputs
  `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.{md,json}`.
- Research bands: `v3/research/research_answers/cluster2.md` (Quantitative Signatures / Protocol).
- C2 case list + oracle faults: `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json` (C2, 22 cases)
  and the oracle/expected family per case (OUTRANKED map / acceptance JSON).
- Corpus columns to match (schema only, do NOT write here): `apps/wired/v7/data/cases_petrol_v7.csv`
  (`obd_ltft_cell_vector_json`, `dtc_raw_mode06_json`) and `labs/comlab/registry/corpus_curated.csv`
  (`stft_b1/ltft_b1`). Blank for all 22 today (verified).
- Web research: use `WebSearch`/`web_fetch` for real-world STFT/LTFT and Mode $06 catalyst ranges;
  cite each source.

### Consumer (signal/noise) ###
- **Consumer:** `T-V3-P4-C2A` (simulates the C2 producer/consumer on this seed) and `C2B` (commits).
  This task adds no engine field/state — it produces the labelled provisional data those tasks read.

### Deliverables ###
1. `v3/reports/V3_C2_SYNTH_BANDS_2026-07-01.md` — CREATE. Per-column research vs web-real bands + cites.
2. `v3/data/c2_synthetic_seed_2026-07-01.csv` — CREATE. 22 cases × C2 columns, `synthetic=true`.
3. `v3/data/c2_synthetic_seed_2026-07-01.json` — CREATE. Manifest (case_id → values, band_id, citation).
4. `v3/gen_c2_synth_seed.py` — CREATE. Generator: oracle_fault + web-validated band → sampled values.

### Files to touch ###
- `v3/reports/V3_C2_SYNTH_BANDS_2026-07-01.md` (CREATE)
- `v3/data/c2_synthetic_seed_2026-07-01.csv` (CREATE)
- `v3/data/c2_synthetic_seed_2026-07-01.json` (CREATE)
- `v3/gen_c2_synth_seed.py` (CREATE)

### Out of scope ###
**No write into the live corpus** (`cases_petrol_v7.csv` / `corpus_curated.csv`) — the seed is a side
file; the live corpus write + producer/consumer wiring + re-score + yardstick mint are `C2B`. **No
engine/lab/registry edit. No back-solving values from consumer rules.** No abstain-dial change. Writes
only under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph rebuild. No secrets.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/gen_c2_synth_seed.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/gen_c2_synth_seed.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/gen_c2_synth_seed.py
/agent_workspace/.venv-wired/bin/python v3/gen_c2_synth_seed.py
grep -iE 'synthetic|band|citation|-10%|0.20|tolerance|22' v3/reports/V3_C2_SYNTH_BANDS_2026-07-01.md
```
Gate: 22/22 cases seeded with `synthetic=true`; each column band web-corroborated **with a citation**;
each case's values inside its **own oracle fault's** band across the stated spread; generator provably
does not read consumer-rule thresholds; live corpus/engine/yardstick untouched (`git status` shows
only new files under `v3/`).

### Progress hook ###
PROGRESS.md `T-V3-P4-C2-SYNTH`: Status=done, Files changed=4 (new under v3/), Verification="22 C2
cases seeded with research-grounded, web-corroborated (cited), tolerance-wide synthetic trim/Mode06;
synthetic=true manifest; bands widened to real-world spread; no back-solve; side file only, live
corpus/yardstick untouched".

### Depends on ###
`T-V3-P4-C2-PRE` done (reveal contract / C2 bands). Provisional-synthetic policy in canon. Web access.
Runnable now. **Unblocks `T-V3-P4-C2A`** (dry-run now runs on this seed instead of owner data).
