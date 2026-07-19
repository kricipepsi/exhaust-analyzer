### Goal ###
Produce the **provisional synthetic C4 data** that unblocks the C4 signal pack. C4 separates three
confusable positive-trim causes — **exhaust leak vs true lean vs biased/lazy O2 sensor** — for its 11
residual cases. Unlike C2, **C4 asks for no new corpus column** (acquisition spec §C4): its
discriminator is the **two-point ΔSTFT idle→2500** *computed from the shared C5 trim columns*, plus
the C4-distinct dilution/bias signals value4.1 leans on. This task seeds, as a side file:
(a) the idle+2500 trim values (shared C5 schema) so ΔSTFT is computable for the 11 C4 cases, and
(b) the C4-distinct columns (idle CO2 dilution, tailpipe O2 elevation, downstream-O2 voltage, propane
trim shift) — all **research-grounded, tolerance-wide**, derived from each case's **oracle fault**,
flagged `synthetic=true`. It does **not** wire producer/consumer or score — it produces the labelled
data `T-V3-P4-C4A` (dry-run) simulates and `C4B` commits.

### Grounding source — read first (this is the DEFINITIVE C4 answer) ###
`v3/research/value_answers/value4.1.md` is the **owner-pinned, definitive C4 value answer** — the
single authoritative source for this seed. It already **incorporates the follow-up**: its
`Specific Gaps — Resolved` section closes the earlier open items (ΔTrim-by-leak-size, speed-density/
turbo calibration, CO2-depression-vs-leak-size, O2-bias-vs-true-lean forced enrichment). **No further
C4 research is pending or required** — do not re-open one. Its Confirmation Matrix, Bands-to-Change
shortlist, and Distribution Guidance are the band table for this seed. Companion context (mechanism,
already fixed): `research_answers/cluster4.md`. (`value4.md` was a superseded first pass — ignore it.)

> **EVIDENCE-TIER LABEL — policy compliance, not a blocker.** value4.1 classifies its own C4 numbers
> as **anecdotal/textbook** (no SAE/EPA/CARB codification of these exact thresholds). This does **not**
> hold the pack up: under the provisional-synthetic policy that is exactly the case the policy is for
> — proceed now with a **tolerance-wide, `synthetic=true`-labelled** seed and calibrate on real user
> data post-launch. The requirement here is only to **carry the tier through** (the bands-report tags
> each C4 value `anecdotal`, the manifest records it) so the synthetic-vs-real scoreboard stays honest
> — not to present the numbers as standardized. Grounding is sufficient to build; tier is a label.

### Policy this task operationalizes (read `4DLab_CLAUDE.md` §Provisional synthetic signals first) ###
1. **Grounded, not gamed:** each value comes from the case's oracle fault via the value4.1 signature
   (exhaust_leak → ΔSTFT collapses ≥8 pt toward 0 at 2500 + CO2<12% + O2 elevated; lean_condition →
   ΔSTFT persists <3–5 pt, trims stay positive across RPM; sensor_fault/biased-O2 → ΔSTFT persists +
   downstream-O2 held high / propane fails to move trims). **Never back-solve from the consumer rule.**
2. **Tolerance-wide, not lab-precise:** sample each value from a band with realistic spread, not a
   point. **Stated tolerance widths (from value4.1):**
   - Two-point ΔSTFT — leak: central −9 pt, band −5…−15 pt, σ≈±3 (P10–P90 −3…−18); lean/bias:
     central −2 pt, band 0…−5 pt, σ≈±2 (P10–P90 0…−6). Seed idle & 2500 STFT so the **derived Δ**
     lands in-band robustly across the spread, not on a knife-edge.
   - Idle CO2 — leak: central 11.5%, band 8…13%, σ≈±1.5 (left-skew); healthy/non-leak ≥14%.
   - Tailpipe O2 elevation — leak: central +2.5%, band +1.0…+5.0%, σ≈±0.8 (≈+1.0% O2 per 5% air).
   - Downstream-O2 voltage — biased-O2: central 0.8 V, band 0.6…0.95 V, σ≈±0.1 (bimodal vs <0.4 V normal).
   - Propane trim shift — responsive sensor: ≤−20% (band −15…−30, σ≈±4); sluggish/biased: >−15%.
3. **Web-corroboration already spent:** value4.1 **is** the web-research pass (Bridge Analyzers,
   ALLDATA, SmogTech, StackExchange). Do **not** redo web research; cite value4.1 as the band source
   and carry its evidence tier (`anecdotal`/`textbook`/`manufacturer-typical`) into the manifest.
4. **Labeled + tracked:** every seeded value carries `synthetic=true` + `oracle_fault` + `band_id` +
   `source=value4.1` provenance; downstream scoring keeps a synthetic-vs-real split.
5. **Correctable:** the manifest makes every synthetic value findable for replacement post-launch.

### Oracle-fault mix for the 11 C4 cases (from acquisition-spec JSON — the generator keys on this) ###
- **exhaust_leak (7):** CSV-129, CSV-130, EXT-238, EXT-239, PDF-HI-007, TC-048, YAML-CSV95
- **lean_condition (3):** CASE-020, EXT-211, EXT-212
- **sensor_fault / biased-O2 (1):** CASE-022
(All 11 currently mis-predicted as sensor_fault or lean_condition — the confusion C4 targets.)

### Progressive-disclosure split (why this is SYNTH-only) ###
ΔSTFT over the **shared C5 trim columns** separates **leak (7)** from **{lean+bias} (4)** with **no
new column** — buildable now. Separating **lean (3)** from **biased-O2 (1)** *within* that group is
what needs the C4-distinct dilution/bias signals (downstream-O2 V, propane), which are **not current
corpus columns**. This task seeds both layers but **commits neither**; whether the extra columns are
actually needed is disclosed by `C4A` and the add-column decision is deferred to `C4B`. Ship the
disclosure; defer the commit.

### Success criteria ###
1. **Bands report** `v3/reports/V3_C4_SYNTH_BANDS_2026-07-01.md`: per C4 signal, the value4.1 band,
   evidence tier (**anecdotal flag mandatory**), and the tolerance-wide band used, with the ΔSTFT
   leak-vs-persist split stated for the 7/3/1 oracle groups.
2. **Seeded data + manifest** `v3/data/c4_synthetic_seed_2026-07-01.{csv,json}`: for all 11 C4 cases,
   the idle+2500 trims (shared C5 schema) + C4-distinct columns + `synthetic=true`, `oracle_fault`,
   `band_id`, `source_citation=value4.1`. Reconcile: each case's derived ΔSTFT and C4 values sit
   inside the band for **its own** oracle fault across the stated spread.
3. **No back-solve audit:** the generator keys only on `oracle_fault` + the value4.1 band table — it
   must **not** read the consumer-rule thresholds (EL/LC/SF) or the case's current rank. State this.
4. **Tolerance width stated** per column (the widths above), showing each case passes its band across
   the **whole** spread, not just at the mean.
5. **Reconciliation:** 11/11 seeded; each value's band matches its oracle fault; 0 values from a
   consumer rule. Does **not** touch the live corpus, engine, rules, or yardstick — side file only.
6. `py_compile`+`ruff`+`pyright` clean on the generator.

### Disclosure (what this task must surface, not hide) ###
- Tag **every** C4 band anecdotal/textbook (§Grounding caveat); do not launder it into "confirmed".
- State that the CO2-dilution / downstream-O2 / propane columns are **not** in the current corpus and
  that adding them is a `C4B` decision gated on `C4A` showing ΔSTFT-alone is insufficient.
- If any C4 case's oracle fault is not cleanly leak/lean/biased-O2 (e.g. a third-family outranked
  case), flag it — a synthetic C4 value only helps cases separable by the ΔSTFT/dilution signal;
  others stay abstained. Never present synthetic-seeded passes as real-world accuracy.

### Context ###
- C4 contract (shared-column note, producer/consumer path, 11 case IDs): `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md` §C4 + JSON `contracts.C4`.
- Shared column schema (idle/2500 trims C4 reuses): §C5 `stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct`; §C6 O2 dynamics.
- Reveal-contract template every pack inherits: `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md` (C2 instance).
- Seed-generator precedent to mirror: `v3/gen_c2_synth_seed.py` + `T-V3-P4-C2-SYNTH`.
- Band source: `v3/research/value_answers/value4.1.md`. Mechanism: `research_answers/cluster4.md`.

### Consumer (signal/noise) ###
- **Consumer:** `T-V3-P4-C4A` (simulates the C4 ΔSTFT producer + EL/LC/SF consumer on this seed) and
  `C4B` (commits). This task adds no engine field/state — it produces the labelled provisional data.

### Deliverables ###
1. `v3/reports/V3_C4_SYNTH_BANDS_2026-07-01.md` — CREATE. Per-signal value4.1 band + anecdotal tier + tolerance band + 7/3/1 split.
2. `v3/data/c4_synthetic_seed_2026-07-01.csv` — CREATE. 11 cases × (shared trims + C4-distinct cols), `synthetic=true`.
3. `v3/data/c4_synthetic_seed_2026-07-01.json` — CREATE. Manifest (case_id → values, band_id, oracle_fault, source=value4.1).
4. `v3/gen_c4_synth_seed.py` — CREATE. Generator: oracle_fault + value4.1 band → sampled values (idle/2500 trims + C4-distinct).

### Files to touch ###
- `v3/reports/V3_C4_SYNTH_BANDS_2026-07-01.md` (CREATE)
- `v3/data/c4_synthetic_seed_2026-07-01.csv` (CREATE)
- `v3/data/c4_synthetic_seed_2026-07-01.json` (CREATE)
- `v3/gen_c4_synth_seed.py` (CREATE)

### Out of scope ###
**No write into the live corpus** (`cases_petrol_v7.csv` / `corpus_curated.csv`) — side file only.
**No new corpus column added here** (the CO2/downstream-O2/propane add-decision is `C4B`, gated on
`C4A`). **No engine/lab/registry edit. No back-solving values from consumer rules.** No abstain-dial
change. No re-run of the C5 seed (C4 seeds its own 11 cases' trims; C5 reconciles later). Writes only
under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph rebuild. No secrets.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/gen_c4_synth_seed.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/gen_c4_synth_seed.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/gen_c4_synth_seed.py
/agent_workspace/.venv-wired/bin/python v3/gen_c4_synth_seed.py
grep -iE 'synthetic|anecdotal|band|value4.1|delta.?stft|tolerance|11' v3/reports/V3_C4_SYNTH_BANDS_2026-07-01.md
```
Gate: 11/11 cases seeded with `synthetic=true`; each column band cited to value4.1 **and tagged
anecdotal**; each case's derived ΔSTFT + C4 values inside its **own oracle fault's** band across the
stated spread; generator provably does not read consumer-rule thresholds; live corpus/engine/yardstick
untouched (`git status` shows only new files under `v3/`).

### Progress hook ###
PROGRESS.md `T-V3-P4-C4-SYNTH`: Status=done, Files changed=4 (new under v3/), Verification="11 C4
cases seeded from owner-pinned value4.1 (anecdotal-tagged), tolerance-wide two-point ΔSTFT + C4
dilution/bias cols; synthetic=true manifest; no new corpus column; no back-solve; side file only,
live corpus/yardstick untouched".

### Depends on ###
value4.1 pinned by owner (done). Provisional-synthetic policy in canon. Reveal-contract template
(`T-V3-P4-C2-PRE`) done. Runnable now. **Unblocks `T-V3-P4-C4A`** (dry-run runs on this seed).
