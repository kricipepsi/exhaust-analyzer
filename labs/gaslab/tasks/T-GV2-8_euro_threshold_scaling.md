# T-GV2-8 — Euro-Threshold Scaling Consumer (`euro_emission_category`)

### Goal ###

Wire the orphan DNA field `euro_emission_category` (`GASLab/gaslab/dna_view.py`
L31 — read in **0** code paths today) to its wiki-named consumer
`CONCEPT_EURO_SCALING`: scale the healthy/fault **CO ceiling (idle)** and **HC
ceiling (2500 RPM)** by Euro class, with Euro-4 as the default baseline.

Wiki source — `GAS_WIKI §4.7` table (`docs/GASLab/wikiNEW/GAS_WIKI.md` L211-219;
named consumer at §1.4 L81: "scales healthy/fault thresholds →
CONCEPT_EURO_SCALING"):

| Euro | CO ceiling idle (with cat) | HC ceiling 2500 |
|---|---|---|
| 1 | 4.5 % | — |
| 2 | 0.5 % | 1200 ppm |
| 3 | 0.3 % | 200 ppm |
| 4–6 | 0.2 % | 200 ppm |
| 6+ | 0.2 % | 100 ppm |

### Steps ###

1. Add a euro-scaling helper mapping `euro_emission_category` →
   `(co_idle_ceiling, hc_2500_ceiling)` from the §4.7 table; default to the
   **Euro-4** row when the field is absent/unknown. Each literal carries a
   `# wiki: docs/GASLab/wikiNEW/GAS_WIKI.md §4.7` citation.
2. Consume it in the `NORMAL_OPERATION`-vs-rich CO classification (idle) and the
   HC ceiling at 2500 RPM. The coder **pins the exact branch**
   (`rule_engine.py` / `resolution.py`) in scope confirmation.
3. Precedence: euro scaling sets the *category default*; the per-vehicle CoC
   override (CHI-1: `co_high_idle` when `confidence == "HIGH"`) still wins where
   populated. Document and test the order.

### Success criteria ###

- `test_euro2_loosens_co_ceiling` — a reading that is rich for Euro-6 classifies
  as `NORMAL_OPERATION` for Euro-2.
- `test_euro6plus_tightens_hc_ceiling_2500`.
- `test_euro_default_is_euro4_when_absent`.
- `test_per_vehicle_coc_overrides_euro_default` — CHI-1 precedence preserved.
- All existing GASLab tests pass.

### Files to touch ###

- `GASLab/gaslab/resolution.py` **or** `rule_engine.py` (MODIFY — coder pins in
  scope confirmation)
- `GASLab/tests/test_rule_engine.py` (MODIFY)

### Signal/noise consumer ###

`euro_emission_category` → euro-scaling helper → CO/HC classification ceilings
(`CONCEPT_EURO_SCALING`, §4.7). **Anti-orphan gate:** after this task, `grep
euro_emission_category` must show a read site in `resolution.py`/`rule_engine.py`,
not only `dna_view.py`.

### Out of scope ###

- Per-vehicle CoC bounds (CHI-1, done). No new DNA field, no enum change.
- Mass-emission conversion (`engine_displacement_liters`, reserved — not v1/v2).
